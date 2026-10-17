#!/usr/bin/env python3
"""Puerta de Pinterest — valida un paquete de pin antes de entrar a la cola.

Gates mecánicos (código):
  1. asset_final: el asset existe Y está registrado como FINAL del listing.
     (Caso 2026-10-12: dos pins salieron con mockups faithful viejos,
     no-finales. El pin muestra lo que el comprador encuentra en la tienda.)
  2. url_listing: formato rastreable de Share & Save
     (<tienda>.etsy.com/.../<id>) o clásico (etsy.com/listing/<id>),
     y el id coincide con el registrado para ese slug.
  3. keywords: título+descripción contienen ≥1 keyword del banco del nicho,
     y keywords_fuente cita el archivo del banco (que debe existir).
  4. tablero: no vacío. (La existencia real del tablero es gate humano:
     la API de Pinterest no está conectada.)

Uso:
  verificar-pin.py --pin pin.json [--registro data/registro-listings.json]

pin.json:
  {"slug": "...", "asset": "/ruta/absoluta.jpg",
   "titulo": "...", "descripcion": "...",
   "url_listing": "https://<tienda>.etsy.com/listing/<id>",
   "tablero": "...", "keywords_fuente": "/ruta/banco.md"}

Salida: JSON {"veredicto": "PASS"|"FAIL", "criterio_violado": ...}.
Exit 0 = PASS, 1 = FAIL, 2 = error de uso.
"""
import argparse
import json
import os
import re
import sys

APP = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
REG_DEFAULT = os.path.join(APP, "data", "registro-listings.json")


def cargar_banco_kw(path):
    """Extrae keywords del banco: líneas de listas y frases entre backticks."""
    txt = open(path, encoding="utf-8").read().lower()
    kws = set()
    for m in re.finditer(r"`([^`]{4,80})`", txt):
        kws.add(m.group(1).strip())
    for m in re.finditer(r"^\s*\d+\.\s+(.+)$", txt, re.M):
        frase = m.group(1).strip().lower()
        if 4 <= len(frase) <= 80:
            kws.add(frase)
    return {k for k in kws if len(k.split()) >= 2}  # solo multi-palabra


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pin", required=True)
    ap.add_argument("--registro", default=REG_DEFAULT)
    a = ap.parse_args()

    pin = json.load(open(a.pin, encoding="utf-8"))
    reg = json.load(open(a.registro, encoding="utf-8"))
    slug = pin.get("slug", "")
    gates, violado = {}, None

    # G1: asset final del listing
    info = reg.get(slug)
    asset = pin.get("asset", "")
    g1 = bool(info) and os.path.exists(asset) and asset in info["assets_finales"]
    gates["asset_final"] = {"pass": g1, "asset": os.path.basename(asset)}
    if not g1:
        violado = "asset_no_final" if info else "slug_desconocido"

    # G2: URL del listing (clásica o rastreable Share & Save)
    url = pin.get("url_listing", "")
    m = re.fullmatch(r"https://www\.etsy\.com/listing/(\d+)(/.*)?", url or "")
    if not m:
        m = re.fullmatch(r"https://[a-z0-9-]+\.etsy\.com/listing/(\d+)(/.*)?",
                         url or "")
    g2 = bool(m) and bool(info) and m.group(1) == info["id_etsy"]
    gates["url_listing"] = {"pass": g2, "url": url}
    violado = violado or (None if g2 else "url_listing_invalida")

    # G3: keywords del banco con fuente citada
    fuente = pin.get("keywords_fuente", "")
    texto = f"{pin.get('titulo','')} {pin.get('descripcion','')}".lower()
    kws = cargar_banco_kw(fuente) if fuente and os.path.exists(fuente) else set()
    usadas = sorted(k for k in kws if k in texto)
    g3 = bool(usadas) and bool(fuente) and os.path.exists(fuente)
    gates["keywords_banco"] = {"pass": g3, "keywords_usadas": usadas,
                               "fuente": os.path.basename(fuente) if fuente else ""}
    violado = violado or (None if g3 else "keywords_sin_fuente")

    # G4: tablero declarado (existencia real = gate humano)
    g4 = bool((pin.get("tablero") or "").strip())
    gates["tablero"] = {"pass": g4, "tablero": pin.get("tablero", "")}
    violado = violado or (None if g4 else "tablero_vacio")

    veredicto = "PASS" if violado is None else "FAIL"
    print(json.dumps({"veredicto": veredicto, "criterio_violado": violado,
                      "gates": gates,
                      "mediciones": {"slug": slug,
                                     "origen": "registro" if info else "desconocido"}},
                     ensure_ascii=False, indent=1))
    return 0 if veredicto == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
