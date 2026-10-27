#!/usr/bin/env python3
"""Puerta: la descripción viva en Etsy lista EXACTAMENTE los colores
habilitados en Printify, por componente (publicar-printify-etsy §M8).

Fuente esperada (la verdad): los colores habilitados por API en cada
componente del listing, tal como el dueño los dejó en su revisión
(§M2). Contra eso se comparan las líneas «Colors: …» de la descripción
del listing en Etsy, en el orden de los componentes del registro
(primero el principal). Cualquier color de más (retirado) o de menos
(vendido y no listado) es FALLO.

Nace del incidente p046 (2026-10-27): el dueño cambió los colores en
una actualización, la selección de mockups se rehízo desde los
colores nuevos, pero la descripción republicó la lista vieja
(Sport Grey / Athletic Heather) porque ningún paso la sincronizaba
ni la verificaba contra una fuente escrita.

Uso:
    verificar-descripcion-colores.py --diseno p046 [--tienda 29222324]
"""
import argparse
import json
import os
import subprocess
import sys
import urllib.request

BASE = os.path.expanduser("~/workspace/my-pod")
sys.path.insert(0, os.path.join(BASE, "scripts"))


def colores_habilitados(tienda, producto_id):
    """Colores (títulos) de las variantes habilitadas del producto."""
    r = subprocess.run(
        ["printify", "request", "--method", "GET",
         "--path", f"/shops/{tienda}/products/{producto_id}.json"],
        capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"printify request falló para {producto_id}: {r.stderr[:200]}")
    d = json.loads(r.stdout)["body"]
    color_ids = {}
    for opt in d.get("options", []):
        if opt.get("type") == "color":
            for v in opt.get("values", []):
                color_ids[v["id"]] = v["title"]
    colores = set()
    for var in d.get("variants", []):
        if var.get("is_enabled"):
            for oid in var.get("options", []):
                if oid in color_ids:
                    colores.add(color_ids[oid])
    return colores


def lineas_colores_descripcion(listing_id):
    """Líneas «Colors: a, b, c» de la descripción viva en Etsy, en orden."""
    from etsy_auth import get_headers
    req = urllib.request.Request(
        f"https://api.etsy.com/v3/application/listings/{listing_id}",
        headers=get_headers())
    with urllib.request.urlopen(req, timeout=30) as resp:
        desc = json.load(resp).get("description", "")
    lineas = []
    for linea in desc.splitlines():
        if "Colors:" in linea:
            resto = linea.split("Colors:", 1)[1]
            resto = resto.split("·")[0].strip()
            lineas.append({c.strip() for c in resto.split(",") if c.strip()})
    return lineas


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--diseno", required=True)
    ap.add_argument("--tienda", default="29222324")
    args = ap.parse_args()

    reg_path = os.path.join(
        BASE, "data", "tiendas", args.tienda, "registro-listings.json")
    with open(reg_path) as f:
        registro = json.load(f)
    entrada = registro["disenos"][args.diseno] if "disenos" in registro else registro[args.diseno]

    componentes = []
    for clave, valor in entrada.get("printify", {}).items():
        if "draft" in clave and "mpl" not in clave and isinstance(valor, str):
            componentes.append((clave, valor))
    if not componentes:
        print(f"FALLO: {args.diseno} no declara componentes draft en el registro")
        return 1
    listing_id = entrada.get("id_etsy")
    if not listing_id:
        print(f"FALLO: {args.diseno} no tiene id_etsy en el registro")
        return 1

    lineas = lineas_colores_descripcion(listing_id)
    errores = []
    if len(lineas) != len(componentes):
        errores.append(
            f"la descripción trae {len(lineas)} líneas «Colors:» y el listing "
            f"tiene {len(componentes)} componentes")
    for i, (clave, pid) in enumerate(componentes):
        esperados = colores_habilitados(args.tienda, pid)
        if i >= len(lineas):
            break
        en_desc = lineas[i]
        sobran = en_desc - esperados
        faltan = esperados - en_desc
        if sobran:
            errores.append(f"{clave}: en la descripción pero NO habilitados: {sorted(sobran)}")
        if faltan:
            errores.append(f"{clave}: habilitados pero NO en la descripción: {sorted(faltan)}")

    if errores:
        print(f"Descripción de {args.diseno} (Etsy {listing_id}) NO sincronizada:")
        for e in errores:
            print(f"  ✗ {e}")
        return 1
    print(f"PASS — descripción de {args.diseno} (Etsy {listing_id}) lista "
          f"exactamente los colores habilitados en sus {len(componentes)} componentes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
