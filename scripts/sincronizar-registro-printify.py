#!/usr/bin/env python3
"""Sincroniza el registro local contra la verdad de Printify (solo lectura de Printify).

Problema que resuelve (falla repetida 2026-10-18): una corrida crea drafts en
Printify por navegador pero el registro local (data/tiendas/29222324/registro-listings.json) y el
checkpoint (data/tiendas/29222324/estado-propuestas.json) quedan atrás porque registrar era un
paso manual del agente, diferido al final de la corrida. Si la corrida se corta,
Printify y el registro divergen y nadie sabe qué existe de verdad.

Este script es la fuente de reconciliación determinista: lee los productos
reales de la tienda vía el CLI `printify` (comando `products`, solo lectura),
empareja por título exacto de diseño + blueprint + fecha, y rellena los IDs
faltantes del registro + drafts_ok del checkpoint. NUNCA crea ni modifica nada
en Printify, NUNCA sobrescribe un ID ya registrado que difiera (reporta
CONFLICTO), y por defecto corre en seco (--aplicar para escribir).

Emparejamiento (verificado contra la tienda 29222324):
- sudadera Gildan 18000  -> blueprint_id 49, título == <titulo del diseño>
- playera Bella+Canvas 3001 -> blueprint_id 12, título == <titulo> + " T-Shirt"
- Se prefieren productos creados en/después de fecha_propuesta. Si el único
  match es ANTERIOR a la fecha, se reporta SOSPECHOSO y NO se registra
  (probable draft huérfano de otro lote con el mismo título).

Completitud: track mpl exige sus componentes (default ambos); track single
exige los suyos (campo `componentes` de la entrada; default: el que exista).

Limitación conocida: el CLI devuelve la página 1 (50 productos más recientes).
Un diseño no hallado se reporta NO_ENCONTRADO (puede estar en la página 2):
nunca se afirma que no existe. Con --verificar-ids, los IDs ya registrados se
confirman uno a uno con `printify products --product-id` (vale para cualquier
página).

Escritura: atómica (tmp + rename) y conservando el formato de cada archivo
(registro indent=2, estado indent=1) para no generar diffs artificiales.

Uso:
  python3 scripts/sincronizar-registro-printify.py [--fecha YYYY-MM-DD]
          [--aplicar] [--verificar-ids]
Salida: una línea por diseño + resumen. Exit 0 sin conflictos, 2 con conflictos.
"""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
# La tienda se declara SIEMPRE al invocar (--shop o MY_POD_SHOP_ID):
# sin default quemado (fuga de colocación corregida 2026-10-24,
# Programa Estándar F4 — antes traía el ID de una tienda y rutas
# previas a la separación D1, y reventaba con FileNotFoundError).
# Las rutas viven bajo data/tiendas/<shop>/ (layout D1, 2026-10-21).
BP_SUDADERA = 49   # Gildan 18000 — hecho de catálogo Printify
BP_PLAYERA = 12    # Bella+Canvas 3001 — hecho de catálogo Printify
CAMPOS = {  # nombre de componente -> (campo registro, sufijo título, blueprint)
    "gildan-18000": ("draft_sweatshirt_id", "", BP_SUDADERA),
    "bella-canvas-3001": ("draft_tshirt_id", " T-Shirt", BP_PLAYERA),
}


def listar_productos(shop_id):
    out = subprocess.run(
        ["printify", "products", "--shop-id", shop_id],
        capture_output=True, text=True, timeout=180,
    )
    if out.returncode != 0:
        sys.exit(f"ERROR: printify products falló: {out.stderr.strip()[:300]}")
    body = json.loads(out.stdout)["body"]
    return body["data"], body.get("total")


def obtener_producto(shop_id, pid):
    out = subprocess.run(
        ["printify", "products", "--shop-id", shop_id, "--product-id", pid],
        capture_output=True, text=True, timeout=60,
    )
    if out.returncode != 0:
        return None
    try:
        body = json.loads(out.stdout)["body"]
        return body if body.get("id") == pid else None
    except Exception:
        return None


def escribir_atomico(path, obj, indent):
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=indent))
    os.replace(tmp, path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fecha", help="fecha_propuesta a sincronizar (default: lote_actual del checkpoint)")
    ap.add_argument("--aplicar", action="store_true", help="escribe los archivos (default: seco)")
    ap.add_argument("--verificar-ids", action="store_true", help="confirma por ID los ya registrados")
    ap.add_argument("--shop", default=os.environ.get("MY_POD_SHOP_ID"),
                    help="ID de la tienda Printify (o variable MY_POD_SHOP_ID); sin default quemado")
    args = ap.parse_args()
    if not args.shop:
        # Fallback de INSTANCIA (mismo patrón que los scripts
        # operativos de la raíz): si el despliegue tiene UNA sola
        # tienda bajo data/tiendas/, es esa; con varias, se exige
        # declarar cuál. Ningún ID va quemado aquí.
        tiendas = sorted(d.name for d in
                         (BASE / "data" / "tiendas").glob("*")
                         if d.is_dir()) \
            if (BASE / "data" / "tiendas").exists() else []
        if len(tiendas) == 1:
            args.shop = tiendas[0]
        else:
            sys.exit("ERROR: falta --shop (o MY_POD_SHOP_ID): la tienda "
                     "se declara al invocar, nunca va quemada en el "
                     "script; el fallback de instancia única no aplica "
                     f"(tiendas encontradas: {tiendas or 'ninguna'})")
    SHOP_ID = args.shop
    REGISTRO = BASE / "data" / "tiendas" / SHOP_ID / "registro-listings.json"
    ESTADO = BASE / "data" / "tiendas" / SHOP_ID / "estado-propuestas.json"
    if not REGISTRO.exists():
        sys.exit(f"ERROR: no existe el registro de la tienda {SHOP_ID}: {REGISTRO}")

    registro = json.loads(REGISTRO.read_text())
    estado = json.loads(ESTADO.read_text()) if ESTADO.exists() else {}
    lote = estado.get("lote_actual", {})
    fecha = args.fecha or lote.get("fecha")
    if not fecha:
        sys.exit("ERROR: sin --fecha y sin lote_actual.fecha en el checkpoint")

    productos, total = listar_productos(SHOP_ID)
    por_titulo = {}
    for p in productos:
        por_titulo.setdefault(p.get("title", ""), []).append(p)

    cambios, conflictos, sospechosos = [], [], []
    drafts_ok = set(lote.get("drafts_ok", []))

    for slug, e in registro.items():
        if not isinstance(e, dict) or e.get("fecha_propuesta") != fecha:
            continue
        titulo = e.get("titulo")
        if not titulo:
            continue
        pf = e.setdefault("printify", {})
        componentes = e.get("componentes") or list(CAMPOS)
        if e.get("track") == "single" and not e.get("componentes"):
            componentes = list(CAMPOS)  # basta el que exista (ver completitud)
        linea = [slug]
        for comp in componentes:
            campo, sufijo, bp = CAMPOS[comp]
            actual = pf.get(campo)
            if actual and args.verificar_ids:
                if obtener_producto(SHOP_ID, actual) is None:
                    conflictos.append(f"{slug}.{campo}: ID {actual} no confirmado por API")
                    linea.append(f"{campo.split('_')[1]}=ID-NO-CONFIRMADO")
                else:
                    linea.append(f"{campo.split('_')[1]}=ok-verificado")
                continue
            if actual:
                linea.append(f"{campo.split('_')[1]}=ok")
                continue
            candidatos = [p for p in por_titulo.get(titulo + sufijo, [])
                          if p.get("blueprint_id") == bp]
            vigentes = [p for p in candidatos
                        if str(p.get("created_at", ""))[:10] >= fecha]
            if vigentes:
                pid = vigentes[0]["id"]
                pf[campo] = pid
                cambios.append(f"{slug}.{campo}={pid}")
                linea.append(f"{campo.split('_')[1]}=+{pid}")
            elif candidatos:
                sospechosos.append(f"{slug}.{campo}: match anterior a {fecha} "
                                   f"({candidatos[0]['id']}, creado {candidatos[0].get('created_at')})")
                linea.append(f"{campo.split('_')[1]}=SOSPECHOSO")
            else:
                linea.append(f"{campo.split('_')[1]}=no-encontrado")
        # Completitud según track
        ids = {c: pf.get(CAMPOS[c][0]) for c in componentes}
        if e.get("track") == "single" and not e.get("componentes"):
            completo = any(ids.values())
        else:
            completo = all(ids.values())
        if completo:
            if slug not in drafts_ok:
                drafts_ok.add(slug)
                cambios.append(f"checkpoint.drafts_ok+={slug}")
            linea.append("=> COMPLETO en Printify")
        elif any(ids.values()):
            linea.append("=> PARCIAL")
        else:
            linea.append("=> NO_ENCONTRADO en página 1 (no afirmar inexistencia)")
        print(" ".join(linea))

    if cambios and args.aplicar:
        escribir_atomico(REGISTRO, registro, indent=2)
        if estado.get("lote_actual"):
            estado["lote_actual"]["drafts_ok"] = sorted(drafts_ok)
            escribir_atomico(ESTADO, estado, indent=1)
    print(f"RESUMEN fecha={fecha} productos_pagina1={len(productos)}/{total} "
          f"cambios={len(cambios)} conflictos={len(conflictos)} "
          f"sospechosos={len(sospechosos)} "
          f"modo={'APLICADO' if (cambios and args.aplicar) else 'SECO'}")
    for c in conflictos:
        print("CONFLICTO:", c)
    for s in sospechosos:
        print("SOSPECHOSO:", s)
    return 2 if conflictos else 0


if __name__ == "__main__":
    sys.exit(main())
