#!/usr/bin/env python3
"""Puerta de conteo de variantes (criterio del dueño, 2026-10-23).

Cuenta, por producto de Printify, los colores HABILITADOS y las
variantes HABILITADAS, y el total del conjunto (un MPL). Es la
única puerta mecánica de colores del flujo: NO compara contra
ninguna lista — no existe paleta canónica. Solo verifica topes:

  - colores habilitados por item  > TOPE_COLORES (default 4) → AVISO
  - variantes totales del conjunto > LIMITE_MPL  (default 400) → AVISO

Exit 0 = dentro de topes. Exit 2 = algún tope superado (avisar al
dueño y detenerse; corrige él o manda corregir).

⚠️ El GET de Printify lista TAMBIÉN las variantes deshabilitadas
y el universo completo de opciones del blueprint. Contar sin
filtrar por `is_enabled` reporta el catálogo entero como si
estuviera habilitado (error ya cometido el 2026-10-23). Esta
puerta cuenta SOLO variantes con is_enabled verdadero, y el
color se resuelve por el id de opción de la variante, no por
el título (el orden título varía por blueprint).

Uso en vivo (vía el CLI de Printify, sin tocar tokens):
    verificar-variantes.py --shop 29222324 ID1 ID2 [...]
Uso con fixtures (regresión):
    verificar-variantes.py --desde-json a.json b.json [...]
"""
import argparse
import json
import subprocess
import sys


def colores_y_conteo(producto):
    """Devuelve (set de colores habilitados, n variantes habilitadas)."""
    id2color = {}
    for opt in producto.get("options", []):
        if opt.get("type") == "color":
            for val in opt.get("values", []):
                id2color[val["id"]] = val["title"]
    colores = set()
    n = 0
    for var in producto.get("variants", []):
        if not var.get("is_enabled"):
            continue
        n += 1
        color = None
        for oid in var.get("options", []) or []:
            if oid in id2color:
                color = id2color[oid]
                break
        if color is None:  # respaldo: el título trae el color
            titulo = var.get("title", "")
            for nombre in id2color.values():
                if nombre in titulo:
                    color = nombre
                    break
        if color:
            colores.add(color)
    return colores, n


def cargar_en_vivo(shop, pid):
    out = subprocess.run(
        ["printify", "request", "--method", "GET",
         "--path", f"/shops/{shop}/products/{pid}.json"],
        capture_output=True, text=True, check=True)
    return json.loads(out.stdout)["body"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="*", help="IDs de producto (modo en vivo)")
    ap.add_argument("--shop", default="29222324")
    ap.add_argument("--desde-json", nargs="*", default=[],
                    help="archivos JSON de producto (modo fixture)")
    ap.add_argument("--tope-colores", type=int, default=4)
    ap.add_argument("--limite-total", type=int, default=400)
    args = ap.parse_args()

    productos = []
    for ruta in args.desde_json:
        with open(ruta) as f:
            productos.append((ruta, json.load(f)))
    for pid in args.ids:
        productos.append((pid, cargar_en_vivo(args.shop, pid)))
    if not productos:
        print("sin productos que verificar")
        return 2

    total = 0
    avisos = []
    for nombre, prod in productos:
        colores, n = colores_y_conteo(prod)
        total += n
        linea = (f"{prod.get('title', nombre)}: {len(colores)} colores "
                 f"habilitados {sorted(colores)} · {n} variantes")
        print(linea)
        if len(colores) > args.tope_colores:
            avisos.append(
                f"AVISO: {prod.get('title', nombre)} tiene "
                f"{len(colores)} colores habilitados (> {args.tope_colores})")
    print(f"TOTAL conjunto: {total} variantes habilitadas "
          f"(límite MPL: {args.limite_total})")
    if total > args.limite_total:
        avisos.append(
            f"AVISO: el conjunto suma {total} variantes "
            f"(> {args.limite_total} del MPL)")
    for a in avisos:
        print(a)
    if avisos:
        print("RESULTADO: AVISO AL DUEÑO — detenerse antes de publicar")
        return 2
    print("RESULTADO: OK — dentro de topes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
