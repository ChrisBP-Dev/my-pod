#!/usr/bin/env python3
"""Actualiza precios por variación vía API de Etsy (PUT inventory).

Requiere scope listings_w. Fuente de verdad de la tabla:
scripts/precios_comunes.py (replica de estrategia_precios del config
de la tienda).

Modos:
  --no-op <listing_id>   PUT con los precios SIN cambiar (prueba de
                         seguridad: verifica que el PUT no deslinkea
                         imágenes de variación ni altera nada).
  --aplicar              Aplica la tabla a los 14 listings activos.
  --aplicar --solo <id>  Aplica a un solo listing.

El PUT reescribe el inventario completo: se hace GET primero, se
cambian SOLO los precios y se devuelve el resto idéntico
(property_id/value_ids intactos => las imágenes de variación se
conservan, según la documentación de Etsy).
"""
import json
import os
import sys
import urllib.request
import urllib.error

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from precios_comunes import precio_esperado  # noqa: E402

BASE = os.path.expanduser("~/workspace/my-pod")
API = "https://openapi.etsy.com/v3/application"
SHOP_ID = "68433437"


def resolve_secrets():
    cfg = os.path.expanduser(
        os.environ.get("MY_POD_TIENDA_CONFIG",
                       "~/workspace/my-pod/data/tiendas/29222324/config.json"))
    try:
        c = json.load(open(cfg))
        p = (c.get("etsy_api") or {}).get("secrets_file")
        if p:
            return os.path.expanduser(p)
    except Exception:
        pass
    return os.path.expanduser("~/.config/my-pod/etsy-api.json")


def headers(sec):
    return {"x-api-key": sec["keystring"] + ":" + sec["shared_secret"],
            "Authorization": "Bearer " + sec["access_token"],
            "Content-Type": "application/json"}


def api_get(sec, path):
    req = urllib.request.Request(API + path, headers={
        "x-api-key": sec["keystring"] + ":" + sec["shared_secret"],
        "Authorization": "Bearer " + sec["access_token"]})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def api_put(sec, path, body):
    req = urllib.request.Request(API + path, data=json.dumps(body).encode(),
                                 headers=headers(sec), method="PUT")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def size_of(product):
    for pv in product.get("property_values", []):
        if pv.get("property_name") == "Size":
            return (pv.get("values") or ["?"])[0]
    return "?"


def build_payload(inv, cambiar_precios):
    """Reconstruye el payload del PUT desde el GET. Si cambiar_precios
    es False, los precios quedan idénticos (no-op)."""
    products = []
    for p in inv.get("products", []):
        size = size_of(p)
        ofertas = []
        for off in p.get("offerings", []):
            pr = off.get("price", {})
            actual = pr.get("amount", 0) / (pr.get("divisor") or 100)
            esp = precio_esperado(size)
            nuevo = esp if (cambiar_precios and esp is not None) else actual
            ofertas.append({"price": round(nuevo, 2),
                            "quantity": off.get("quantity", 999),
                            "is_enabled": off.get("is_enabled", True),
                            "readiness_state_id": off.get("readiness_state_id")})
        products.append({
            "sku": p.get("sku") or "",
            "property_values": [
                {"property_id": pv["property_id"],
                 "property_name": pv.get("property_name"),
                 "value_ids": pv.get("value_ids", []),
                 "values": pv.get("values", [])}
                for pv in p.get("property_values", [])
            ],
            "offerings": ofertas,
        })
    return {"products": products,
            "price_on_property": inv.get("price_on_property", []),
            "quantity_on_property": inv.get("quantity_on_property", []),
            "sku_on_property": inv.get("sku_on_property", [])}


def variation_images(sec, lid):
    d = api_get(sec, f"/shops/{SHOP_ID}/listings/{lid}/variation-images")
    return sorted((v.get("image_id"), v.get("property_id"), v.get("value_id"))
                  for v in d.get("results", []))


def cmd_noop(lid):
    sec = json.load(open(resolve_secrets()))
    inv_antes = api_get(sec, f"/listings/{lid}/inventory")
    imgs_antes = variation_images(sec, lid)
    precios_antes = {}
    for p in inv_antes.get("products", []):
        off = p.get("offerings", [{}])[0]
        pr = off.get("price", {})
        precios_antes[p.get("product_id")] = pr.get("amount", 0) / (pr.get("divisor") or 100)
    api_put(sec, f"/listings/{lid}/inventory",
            build_payload(inv_antes, cambiar_precios=False))
    inv_desp = api_get(sec, f"/listings/{lid}/inventory")
    imgs_desp = variation_images(sec, lid)
    ok = True
    for p in inv_desp.get("products", []):
        off = p.get("offerings", [{}])[0]
        pr = off.get("price", {})
        ahora = pr.get("amount", 0) / (pr.get("divisor") or 100)
        antes = precios_antes.get(p.get("product_id"), -1)
        if abs(ahora - antes) > 0.005:
            print(f"  PRECIO CAMBIÓ en {size_of(p)}: {antes} -> {ahora}")
            ok = False
    if imgs_antes != imgs_desp:
        print(f"  IMÁGENES DE VARIACIÓN CAMBIARON: {len(imgs_antes)} -> {len(imgs_desp)}")
        ok = False
    print(f"no-op {lid}: precios intactos={ok} | "
          f"imágenes variación {len(imgs_antes)}->{len(imgs_desp)}")
    return 0 if ok else 1


def cmd_aplicar(solo=None):
    sec = json.load(open(resolve_secrets()))
    listings = api_get(sec, f"/shops/{SHOP_ID}/listings/active?limit=100")["results"]
    if solo:
        listings = [l for l in listings if str(l["listing_id"]) == str(solo)]
    total = 0
    for l in listings:
        lid = l["listing_id"]
        inv = api_get(sec, f"/listings/{lid}/inventory")
        cambios = 0
        for p in inv.get("products", []):
            s = size_of(p)
            esp = precio_esperado(s)
            off = p.get("offerings", [{}])[0]
            pr = off.get("price", {})
            actual = pr.get("amount", 0) / (pr.get("divisor") or 100)
            if esp is not None and abs(actual - esp) > 0.005:
                cambios += 1
        if cambios:
            api_put(sec, f"/listings/{lid}/inventory",
                    build_payload(inv, cambiar_precios=True))
            print(f"{lid}: {cambios} variaciones actualizadas")
            total += cambios
        else:
            print(f"{lid}: ya estaba correcto")
    print(f"Total variaciones actualizadas: {total}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--no-op":
        sys.exit(cmd_noop(sys.argv[2]))
    if sys.argv[1:] == ["--aplicar"]:
        sys.exit(cmd_aplicar())
    if len(sys.argv) == 4 and sys.argv[1] == "--aplicar" and sys.argv[2] == "--solo":
        sys.exit(cmd_aplicar(solo=sys.argv[3]))
    print("Uso: --no-op <listing_id> | --aplicar [--solo <id>]")
    sys.exit(2)
