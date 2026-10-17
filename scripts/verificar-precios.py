#!/usr/bin/env python3
"""Verifica que los precios por variación de los listings activos
coincidan con la tabla de la estrategia de precios de la tienda
(data/tiendas/<id>/config.json -> estrategia_precios).

Uso: python3 scripts/verificar-precios.py
Sale 0 si todo coincide; 1 si hay diferencias (las lista).
"""
import json
import os
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from precios_comunes import precio_esperado, normalizar, SHOP_ID  # noqa: E402
from etsy_auth import get_headers  # noqa: E402 (refresca el token si venció)

API = "https://openapi.etsy.com/v3/application"


def api_get(path):
    req = urllib.request.Request(API + path, headers=get_headers())
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def main():
    listings = api_get(f"/shops/{SHOP_ID}/listings/active?limit=100")["results"]
    errores = []
    revisados = 0
    for l in listings:
        lid = l["listing_id"]
        inv = api_get(f"/listings/{lid}/inventory")
        for p in inv.get("products", []):
            size = color = None
            for pv in p.get("property_values", []):
                if pv.get("property_name") == "Size":
                    size = (pv.get("values") or ["?"])[0]
                elif pv.get("property_name") == "Color":
                    color = (pv.get("values") or ["?"])[0]
            if not size:
                continue
            esperado = precio_esperado(size)
            if esperado is None:
                errores.append(f"{lid} {size}/{color}: talla no mapeada")
                continue
            precio = None
            for off in p.get("offerings", []):
                pr = off.get("price", {})
                if isinstance(pr, dict):
                    precio = pr.get("amount", 0) / 100.0
            revisados += 1
            if abs((precio or 0) - esperado) > 0.005:
                errores.append(
                    f"{lid} {size}/{color}: ${precio:.2f} != ${esperado:.2f}")
    print(f"Listings: {len(listings)} | variaciones revisadas: {revisados} | "
          f"diferencias: {len(errores)}")
    for e in errores[:30]:
        print("  DIFF:", e)
    return 1 if errores else 0


if __name__ == "__main__":
    sys.exit(main())
