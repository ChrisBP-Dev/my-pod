"""Canon de precios por variación — módulo compartido.

Fuente de verdad: data/tiendas/<id>/config.json -> estrategia_precios
(doctrina "precio con colchón", 2026-10-16). Esta TABLA la replica;
si la doctrina cambia, se actualiza AQUÍ y los scripts la heredan.

Los nombres de Size en Etsy varían por listing ("Sweatshirt / 2XL" vs
"Unisex Heavy Blend™ Crewneck Sweatshirt / 2XL"), así que la
normalización es por contenido, no por igualdad exacta.
"""

# (producto, talla) -> precio USD
TABLA = {
    ("Sweatshirt", "S"): 40.99, ("Sweatshirt", "M"): 40.99,
    ("Sweatshirt", "L"): 40.99, ("Sweatshirt", "XL"): 40.99,
    ("Sweatshirt", "2XL"): 44.99, ("Sweatshirt", "3XL"): 46.99,
    ("T-Shirt", "S"): 25.99, ("T-Shirt", "M"): 25.99,
    ("T-Shirt", "L"): 25.99, ("T-Shirt", "XL"): 25.99,
    ("T-Shirt", "2XL"): 28.99, ("T-Shirt", "3XL"): 32.99,
}

_TALLAS = ("S", "M", "L", "XL", "2XL", "3XL")


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
