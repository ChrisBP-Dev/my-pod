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

BASE = os.path.expanduser("~/workspace/my-pod")
SECRETS = os.path.expanduser("~/.config/my-pod/etsy-api.json")
API = "https://openapi.etsy.com/v3/application"
SHOP_ID = "68433437"

TABLA = {  # (producto, talla) -> precio USD
    ("Sweatshirt", "S"): 40.99, ("Sweatshirt", "M"): 40.99,
    ("Sweatshirt", "L"): 40.99, ("Sweatshirt", "XL"): 40.99,
    ("Sweatshirt", "2XL"): 44.99, ("Sweatshirt", "3XL"): 46.99,
    ("T-Shirt", "S"): 25.99, ("T-Shirt", "M"): 25.99,
    ("T-Shirt", "L"): 25.99, ("T-Shirt", "XL"): 25.99,
    ("T-Shirt", "2XL"): 28.99, ("T-Shirt", "3XL"): 32.99,
}


def api_get(path):
    sec = json.load(open(SECRETS))
    req = urllib.request.Request(
        API + path,
        headers={"x-api-key": sec["keystring"] + ":" + sec["shared_secret"],
                 "Authorization": "Bearer " + sec["access_token"]})
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
            if not size or "/" not in size:
                continue
            prod, talla = [s.strip() for s in size.split("/", 1)]
            esperado = TABLA.get((prod, talla))
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
