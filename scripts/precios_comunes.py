"""Canon de precios por variación — módulo compartido (CAPA SISTEMA).

Este módulo es PORTABLE: no contiene ningún valor de tienda quemado.
- La TABLA se lee de `data/tiendas/<id>/config.json → estrategia_precios.tabla_variaciones`
  (la tienda se resuelve vía MY_POD_TIENDA_CONFIG o el default).
- El SHOP_ID (Etsy) se lee de `etsy_api.shop_id` del mismo config.
- `normalizar()` es MECANISMO universal: los nombres de Size en Etsy
  varían por listing ("Sweatshirt / 2XL" vs "Unisex Heavy Blend™ Crewneck
  Sweatshirt / 2XL"), así que la normalización es por contenido, no por
  igualdad exacta.
"""

import json
import os

_CONFIG_DEFAULT = os.path.expanduser(
    "~/workspace/my-pod/data/tiendas/29222324/config.json")

# config: nombre de producto en español -> nombre detectado en Etsy
_PRODUCTO_CONFIG = {"sudadera": "Sweatshirt", "playera": "T-Shirt"}


def _cargar_config():
    path = os.path.expanduser(os.environ.get("MY_POD_TIENDA_CONFIG",
                                             _CONFIG_DEFAULT))
    with open(path) as f:
        return json.load(f)


_CONFIG = _cargar_config()

# Shop ID de Etsy: del config de la tienda, nunca hardcodeado.
SHOP_ID = str((_CONFIG.get("etsy_api") or {}).get("shop_id", ""))

# (producto, talla) -> precio USD, construido desde el config.
TABLA = {}
for prod_es, tallas in ((_CONFIG.get("estrategia_precios") or {})
                        .get("tabla_variaciones", {})).items():
    prod = _PRODUCTO_CONFIG.get(prod_es, prod_es)
    for talla, precio in tallas.items():
        TABLA[(prod, talla)] = float(precio)


def normalizar(size_str):
    """'Unisex Heavy Blend™ Crewneck Sweatshirt / 2XL' -> ('Sweatshirt','2XL').
    Devuelve (None, None) si no se reconoce."""
    s = (size_str or "").lower()
    if "sweatshirt" in s or "crewneck" in s:
        prod = "Sweatshirt"
    elif "t-shirt" in s or "tshirt" in s or "tee" in s or "jersey" in s:
        prod = "T-Shirt"
    else:
        return None, None
    for t in ("2XL", "3XL", "XL", "S", "M", "L"):  # orden: los largos primero
        if s.rsplit("/", 1)[-1].strip() == t.lower():
            return prod, t
    return None, None


def precio_esperado(size_str):
    prod, talla = normalizar(size_str)
    if prod is None:
        return None
    return TABLA.get((prod, talla))
