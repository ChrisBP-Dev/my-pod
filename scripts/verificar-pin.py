#!/usr/bin/env python3
"""
verificar-pin.py — Puerta mecánica de pins de Pinterest (M1).

Valida un pin.json contra el registro de listings y el banco de keywords
antes de que entre a data/cola-pins/.

Uso: python3 scripts/verificar-pin.py --pin pin.json
Salida: PASS (exit 0) o FAIL (exit 1) con el check violado.

Tipos de pin:
  1 hero-lifestyle   imagen principal del listing
  2 lifestyle-alt     otro modelo/pose/color
  3 detalle           close-up del diseño
  4 video             MP4 1:1 de Etsy, SIN recortar
  5 folded-decorado   doblada ambientada

Checks:
  schema            campos requeridos presentes y tipo válido
  asset_final       el asset está registrado como FINAL de ese listing
                    (tipos 1/2/3/5: imagen en assets_finales;
                     tipo 4: MP4 en data/videos/ con manifest)
  video_specs       (solo tipo 4) existe el .manifest.json del video
  url_listing       coincide exactamente con la registrada para el slug
  keywords_banco    título+descripción contienen ≥1 keyword multi-palabra
                    del banco citado en keywords_fuente (que existe)
  tablero           declarado (no vacío)
"""

import argparse
import json
import os
import re
import sys

APP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTRO_PATH = os.path.join(APP_ROOT, "data", "registro-listings.json")
VIDEOS_DIR = os.path.join(APP_ROOT, "data", "videos")

TIPOS = {1: "hero-lifestyle", 2: "lifestyle-alt", 3: "detalle",
         4: "video", 5: "folded-decorado"}
IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".webp")

REQUIRED = ["slug", "tipo", "asset", "titulo", "descripcion",
            "url_listing", "tablero", "keywords_fuente"]


def fail(check, msg):
    print(f"FAIL [{check}]: {msg}")
    return False


def extract_keywords(bank_path):
    """Extrae frases candidatas del banco: listas numeradas y tablas."""
    phrases = []
    with open(bank_path, encoding="utf-8") as f:
        for line in f:
            m = re.match(r"^\s*\d+\.\s+(.+?)\s*$", line)
            if m:
                phrases.append(m.group(1).strip())
                continue
            m = re.match(r"^\s*\|\s*\d+\s*\|\s*([^|]+?)\s*\|", line)
            if m:
                phrases.append(m.group(1).strip())
    # multi-palabra, sin duplicados, ordenadas por longitud desc
    seen, out = set(), []
    for p in phrases:
        p = p.strip().lower()
        if " " in p and p not in seen:
            seen.add(p)
            out.append(p)
    return sorted(out, key=len, reverse=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pin", required=True)
    args = ap.parse_args()

    with open(args.pin, encoding="utf-8") as f:
        pin = json.load(f)

    ok = True

    # schema
    for field in REQUIRED:
        if field not in pin or pin[field] in (None, ""):
            ok = fail("schema", f"falta campo requerido: {field}") and ok
    if pin.get("tipo") not in TIPOS:
        ok = fail("schema", f"tipo debe ser 1-5, vino: {pin.get('tipo')}") and ok
    if not ok:
        return 1
    tipo = pin["tipo"]

    with open(REGISTRO_PATH, encoding="utf-8") as f:
        reg = json.load(f)
    slug = pin["slug"]
    if slug not in reg:
        fail("schema", f"slug '{slug}' no está en registro-listings.json")
        return 1
    entry = reg[slug]

    # asset_final
    asset = pin["asset"]
    if tipo == 4:
        if not asset.lower().endswith(".mp4"):
            ok = fail("asset_final", "tipo 4 (video) requiere asset .mp4") and ok
        elif not os.path.isfile(asset):
            ok = fail("asset_final", f"video no existe: {asset}") and ok
        elif not asset.startswith(VIDEOS_DIR):
            ok = fail("asset_final",
                      f"video fuera de data/videos/: {asset}") and ok
    else:
        if not asset.lower().endswith(IMAGE_EXTS):
            ok = fail("asset_final",
                      f"tipo {tipo} requiere imagen {IMAGE_EXTS}") and ok
        elif asset not in entry.get("assets_finales", []):
            ok = fail("asset_final",
                      f"asset no registrado como FINAL de '{slug}'") and ok
        elif not os.path.isfile(asset):
            # registrado pero el archivo no está: FAIL igual (trazabilidad rota)
            ok = fail("asset_final",
                      f"asset registrado pero archivo ausente: {asset}") and ok

    # video_specs (solo tipo 4): manifest del video 1:1 sin recortar
    if tipo == 4 and ok:
        base = os.path.splitext(os.path.basename(asset))[0]
        manifest = os.path.join(VIDEOS_DIR, base + ".manifest.json")
        if not os.path.isfile(manifest):
            ok = fail("video_specs", f"sin manifest: {manifest}") and ok
        else:
            with open(manifest, encoding="utf-8") as f:
                mf = json.load(f)
            if mf.get("video") != os.path.basename(asset):
                ok = fail("video_specs",
                          "manifest no corresponde al asset") and ok

    # url_listing
    if pin["url_listing"] != entry.get("url"):
        ok = fail("url_listing",
                  f"URL no coincide con la registrada: {entry.get('url')}") and ok

    # keywords_banco
    bank_rel = pin["keywords_fuente"]
    bank_path = bank_rel if os.path.isabs(bank_rel) else os.path.join(APP_ROOT, bank_rel)
    if not os.path.isfile(bank_path):
        ok = fail("keywords_banco", f"banco no existe: {bank_rel}") and ok
    else:
        phrases = extract_keywords(bank_path)
        texto = (pin["titulo"] + " " + pin["descripcion"]).lower()
        if not any(p in texto for p in phrases):
            ok = fail("keywords_banco",
                      "título+descripción sin keyword multi-palabra del banco") and ok

    # tablero
    if not pin["tablero"].strip():
        ok = fail("tablero", "tablero vacío") and ok

    if ok:
        print(f"PASS [tipo {tipo} {TIPOS[tipo]}] slug={slug}")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
