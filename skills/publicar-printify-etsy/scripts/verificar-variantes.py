#!/usr/bin/env python3
"""Puerta de conteo de variantes (criterio del dueño, 2026-10-23,
reescrita en v0.11.0: colores SIN techo).

Cuenta, por producto de Printify, los colores HABILITADOS, las
variantes HABILITADAS y las opciones del conjunto (un MPL). Es la
única puerta mecánica de colores del flujo: NO compara contra
ninguna lista — no existe paleta canónica — y NO limita cuántos
colores puede tener un item. La guía de producción es 3–4 colores
por prenda (5–6 = extensión válida con nota; el dueño en su
revisión §M2 cambia colores sin límite del sistema).

Comportamiento:
  - DETIENE (exit 2) SOLO por el límite técnico del MPL:
      * variantes habilitadas totales del conjunto
        > LIMITE_VARIANTES (default 400), o
      * opciones del conjunto > LIMITE_OPCIONES (default 70).
        «Opciones del conjunto» = suma, por producto, de los
        valores de opción DISTINTOS (ids) presentes en sus
        variantes habilitadas (colores + tallas que de verdad
        se venden; es la lectura operativa del límite de
        70 opciones por MPL).
  - INFORMA sin detener: el conteo por item, y un
    AVISO INFORMATIVO si un item pasa de AVISO_COLORES
    (default 6) colores habilitados. El aviso queda en el
    reporte de la corrida y el flujo SIGUE (exit 0).

Exit codes:
  0 = OK (dentro de los límites técnicos; puede llevar avisos
      informativos impresos).
  2 = detención (límite técnico superado, o error de uso:
      no se pasó ningún producto).

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
    """Devuelve (set de colores habilitados, n variantes
    habilitadas, n valores de opción distintos en variantes
    habilitadas)."""
    id2color = {}
    for opt in producto.get("options", []):
        if opt.get("type") == "color":
            for val in opt.get("values", []):
                id2color[val["id"]] = val["title"]
    colores = set()
    opciones = set()
    n = 0
    for var in producto.get("variants", []):
        if not var.get("is_enabled"):
            continue
        n += 1
        for oid in var.get("options", []) or []:
            opciones.add(oid)
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
    return colores, n, len(opciones)


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
    ap.add_argument("--aviso-colores", type=int, default=6,
                    help="aviso informativo (sin detener) si un item "
                         "pasa de N colores habilitados (default 6)")
    ap.add_argument("--limite-variantes", type=int, default=400,
                    help="límite técnico de variantes totales del "
                         "MPL (default 400); superarlo detiene")
    ap.add_argument("--limite-opciones", type=int, default=70,
                    help="límite técnico de opciones del conjunto "
                         "(default 70); superarlo detiene")
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

    total_variantes = 0
    total_opciones = 0
    informativos = []
    detenciones = []
    for nombre, prod in productos:
        colores, n, n_opciones = colores_y_conteo(prod)
        total_variantes += n
        total_opciones += n_opciones
        linea = (f"{prod.get('title', nombre)}: {len(colores)} colores "
                 f"habilitados {sorted(colores)} · {n} variantes · "
                 f"{n_opciones} opciones")
        print(linea)
        if len(colores) > args.aviso_colores:
            informativos.append(
                f"AVISO INFORMATIVO (no detiene): "
                f"{prod.get('title', nombre)} tiene {len(colores)} "
                f"colores habilitados (> {args.aviso_colores}); "
                f"queda registrado y el flujo sigue")
    print(f"TOTAL conjunto: {total_variantes} variantes habilitadas "
          f"(límite técnico MPL: {args.limite_variantes}) · "
          f"{total_opciones} opciones (límite técnico MPL: "
          f"{args.limite_opciones})")
    if total_variantes > args.limite_variantes:
        detenciones.append(
            f"DETENCIÓN — límite técnico: el conjunto suma "
            f"{total_variantes} variantes (> {args.limite_variantes} "
            f"del MPL)")
    if total_opciones > args.limite_opciones:
        detenciones.append(
            f"DETENCIÓN — límite técnico: el conjunto suma "
            f"{total_opciones} opciones (> {args.limite_opciones} "
            f"del MPL)")
    for a in informativos:
        print(a)
    for d in detenciones:
        print(d)
    if detenciones:
        print("RESULTADO: DETENIDO — límite técnico del MPL superado")
        return 2
    print("RESULTADO: OK — dentro de los límites técnicos "
          "(los colores no tienen techo)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
