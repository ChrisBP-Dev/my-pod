#!/usr/bin/env python3
"""Sincroniza el registro local contra la verdad de Printify (solo lectura de Printify).

Problema que resuelve (falla repetida 2026-10-18): una corrida crea drafts en
Printify por navegador pero el registro local (data/registro-listings.json) y el
checkpoint (data/estado-propuestas.json) quedan atrás porque registrar era un
paso manual del agente, diferido al final de la corrida. Si la corrida se corta,
Printify y el registro divergen y nadie sabe qué existe de verdad.

Este script es la fuente de reconciliación determinista: lee los productos
reales de la tienda vía el CLI `printify` (comando `products`, solo lectura),
empareja por título exacto de diseño y blueprint, y rellena los IDs faltantes
del registro + drafts_ok del checkpoint. NUNCA crea ni modifica nada en
Printify, NUNCA sobrescribe un ID ya registrado que difiera (reporta
CONFLICTO), y por defecto corre en seco (--aplicar para escribir).

Emparejamiento (track mpl, verificado contra la tienda 29222324):
- sudadera Gildan 18000  -> blueprint_id 49, título == <titulo del diseño>
- playera Bella+Canvas 3001 -> blueprint_id 12, título == <titulo> + " T-Shirt"

Limitación conocida: el CLI devuelve la página 1 (50 productos más recientes).
Un diseño no encontrado puede estar en la página 2; el script lo reporta como
NO_ENCONTRADO, nunca como inexistente.

Uso:
  python3 scripts/sincronizar-registro-printify.py [--fecha YYYY-MM-DD] [--aplicar]
Salida: una línea por diseño + resumen. Exit 0 sin conflictos, 2 con conflictos.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
REGISTRO = BASE / "data" / "registro-listings.json"
ESTADO = BASE / "data" / "estado-propuestas.json"
SHOP_ID = "29222324"
BP_SUDADERA = 49   # Gildan 18000
BP_PLAYERA = 12    # Bella+Canvas 3001


def listar_productos(shop_id):
    out = subprocess.run(
        ["printify", "products", "--shop-id", shop_id],
        capture_output=True, text=True, timeout=180,
    )
    if out.returncode != 0:
        sys.exit(f"ERROR: printify products falló: {out.stderr.strip()[:300]}")
    body = json.loads(out.stdout)["body"]
    return body["data"], body.get("total"), body.get("last_page")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fecha", help="fecha_propuesta a sincronizar (default: lote_actual del checkpoint)")
    ap.add_argument("--aplicar", action="store_true", help="escribe los archivos (default: seco)")
    args = ap.parse_args()

    registro = json.loads(REGISTRO.read_text())
    estado = json.loads(ESTADO.read_text()) if ESTADO.exists() else {}
    lote = estado.get("lote_actual", {})
    fecha = args.fecha or lote.get("fecha")
    if not fecha:
        sys.exit("ERROR: sin --fecha y sin lote_actual.fecha en el checkpoint")

    productos, total, last_page = listar_productos(SHOP_ID)
    por_titulo = {}
    for p in productos:
        por_titulo.setdefault(p.get("title", ""), []).append(p)

    cambios = []
    conflictos = []
    drafts_ok = set(estado.get("lote_actual", {}).get("drafts_ok", []))

    for slug, e in registro.items():
        if not isinstance(e, dict) or e.get("fecha_propuesta") != fecha:
            continue
        titulo = e.get("titulo")
        if not titulo:
            continue
        pf = e.setdefault("printify", {})
        hallazgos = {}
        for campo, titulo_draft, bp in (
            ("draft_sweatshirt_id", titulo, BP_SUDADERA),
            ("draft_tshirt_id", titulo + " T-Shirt", BP_PLAYERA),
        ):
            for p in por_titulo.get(titulo_draft, []):
                if p.get("blueprint_id") == bp:
                    hallazgos[campo] = p["id"]
                    break
        linea = [slug]
        for campo, pid in hallazgos.items():
            actual = pf.get(campo)
            if actual is None:
                pf[campo] = pid
                cambios.append(f"{slug}.{campo}={pid}")
                linea.append(f"{campo.split('_')[1]}=+{pid}")
            elif actual != pid:
                conflictos.append(f"{slug}.{campo}: registro={actual} printify={pid}")
                linea.append(f"{campo.split('_')[1]}=CONFLICTO")
            else:
                linea.append(f"{campo.split('_')[1]}=ok")
        faltan = [c for c in ("draft_sweatshirt_id", "draft_tshirt_id") if not pf.get(c)]
        if not faltan:
            if slug not in drafts_ok:
                drafts_ok.add(slug)
                cambios.append(f"checkpoint.drafts_ok+={slug}")
            linea.append("=> COMPLETO en Printify")
        elif len(faltan) == 1 and hallazgos:
            linea.append(f"=> PARCIAL (falta {faltan[0]})")
        else:
            linea.append("=> SIN drafts en la página 1")
        print(" ".join(linea))

    if cambios and args.aplicar:
        REGISTRO.write_text(json.dumps(registro, ensure_ascii=False, indent=1))
        if estado.get("lote_actual"):
            estado["lote_actual"]["drafts_ok"] = sorted(drafts_ok)
            ESTADO.write_text(json.dumps(estado, ensure_ascii=False, indent=1))
    print(f"RESUMEN fecha={fecha} productos_pagina1={len(productos)}/{total} "
          f"cambios={len(cambios)} conflictos={len(conflictos)} "
          f"modo={'APLICADO' if (cambios and args.aplicar) else 'SECO'}")
    for c in conflictos:
        print("CONFLICTO:", c)
    return 2 if conflictos else 0


if __name__ == "__main__":
    sys.exit(main())
