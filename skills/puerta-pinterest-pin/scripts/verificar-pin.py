#!/usr/bin/env python3
"""
verificar-pin.py — Puerta mecánica de pins de Pinterest (v2, 2026-10-18).

ÚNICA implementación del gate: la copia en
skills/puerta-pinterest-pin/scripts/verificar-pin.py es byte-idéntica
(deuda de divergencia cerrada el 2026-10-18). APP_ROOT se resuelve
subiendo directorios hasta encontrar data/registro-listings.json, así
el mismo archivo funciona desde scripts/ y desde el skill.

Valida un pin.json contra el registro de listings y el banco de
keywords antes de que entre a data/cola-pins/.

Uso: python3 scripts/verificar-pin.py --pin pin.json
Salida: PASS (exit 0) o FAIL (exit 1) con el check violado.

Tipos de pin:
  1 hero-lifestyle   imagen principal del listing
  2 lifestyle-alt    otro modelo/pose/color
  3 detalle          close-up del diseño, o frente plano (front-flat)
                     SOLO si el título no afirma "close-up"
  4 video            MP4 1:1 de Etsy, SIN recortar
  5 folded-decorado  doblada ambientada

Checks:
  schema            campos requeridos presentes y tipo válido
  asset_final       el asset está registrado como FINAL de ese listing
                    (tipos 1/2/3/5: imagen en assets_finales;
                     tipo 4: MP4 en data/videos/ con manifest)
  video_specs       (solo tipo 4) existe el .manifest.json del video
  mapa_assets       (tipos imagen) el listing tiene mapa_assets
                    verificado visualmente en el registro; el asset
                    está clasificado en ese mapa. Sin mapa NO hay pin
                    de imagen: la clase de un asset JAMÁS se infiere
                    por su posición/número (caso 2026-10-18: el orden
                    no es uniforme — en p032 la doblada es -5 y -10 es
                    tabla de tallas; en p034 la doblada es -10).
  clase_tipo        pin.json declara `clase_asset`; debe coincidir
                    EXACTO con la clase del mapa y ser compatible con
                    el tipo de pin (matriz TIPO_CLASES). La clase
                    `tabla-tallas` está PROHIBIDA para todo tipo: una
                    tabla de tallas nunca es un pin.
  claims            lo que el título/descripción AFIRMAN debe ser lo
                    que la imagen ES: "close-up" exige clase close-up;
                    "folded" exige folded-decorado; "size chart /
                    size guide / tabla de tallas" está prohibido en
                    el texto de un pin.
  url_listing       coincide exactamente con la registrada para el slug
  keywords_banco    título+descripción contienen ≥1 keyword multi-palabra
                    del banco citado en keywords_fuente (que existe)
  tablero           declarado (no vacío)

Calibración (2026-10-18, suite evals/test-regression.sh):
  conocidos-MALOS que deben dar FAIL: pin real p032-5 publicado
  (tipo 5 + asset tabla de tallas), pin real p030-3 (tipo 3 "Close-Up"
  + asset modelo-playera), pin real p028-3 (mismo defecto, 2026-10-17).
  conocidos-BUENOS que deben dar PASS: p032 tipo 5 con su doblada real
  (-5), p030 tipo 3 con front-flat (-3) sin afirmar close-up, y p034
  tipo 5 con su doblada real (-10) — el mismo número -10 que en p032
  es tabla: el mapa por listing manda, no la posición.
"""

import argparse
import json
import os
import re
import sys


def find_app_root():
    d = os.path.dirname(os.path.abspath(__file__))
    for _ in range(6):
        if os.path.isfile(os.path.join(d, "data", "registro-listings.json")):
            return d
        d = os.path.dirname(d)
    raise SystemExit("ERROR: no se encontró data/registro-listings.json "
                     "subiendo desde el script")


APP_ROOT = find_app_root()
REGISTRO_PATH = os.path.join(APP_ROOT, "data", "registro-listings.json")
VIDEOS_DIR = os.path.join(APP_ROOT, "data", "videos")

TIPOS = {1: "hero-lifestyle", 2: "lifestyle-alt", 3: "detalle",
         4: "video", 5: "folded-decorado"}
IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".webp")

# Matriz tipo → clases de asset compatibles (del mapa verificado).
# tipo 2 acepta lifestyle-alt, modelo-playera y lifestyle genérico;
# tipo 3 acepta close-up, o front-flat como "detalle del frente"
# (el claim "close-up" queda bloqueado por el check de claims).
TIPO_CLASES = {
    1: {"hero-lifestyle", "lifestyle"},
    2: {"lifestyle-alt", "modelo-playera", "lifestyle"},
    3: {"close-up", "front-flat"},
    5: {"folded-decorado"},
}
CLASES_PROHIBIDAS = {"tabla-tallas"}

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

    # mapa_assets + clase_tipo (solo tipos imagen) — puerta nueva 2026-10-18
    clase_real = None
    if tipo != 4 and asset.lower().endswith(IMAGE_EXTS):
        mapa = entry.get("mapa_assets")
        base = os.path.basename(asset)
        if not mapa:
            ok = fail("mapa_assets",
                      f"'{slug}' no tiene mapa_assets verificado en el "
                      "registro. Construirlo por inspección visual (hoja "
                      "de contacto del listing) ANTES de pinear: la clase "
                      "nunca se infiere por posición.") and ok
        elif base not in mapa:
            ok = fail("mapa_assets",
                      f"asset {base} sin clasificar en el mapa de "
                      f"'{slug}': clasificarlo visualmente y registrarlo "
                      "antes de pinear") and ok
        else:
            clase_real = mapa[base]
            if clase_real in CLASES_PROHIBIDAS:
                ok = fail("clase_tipo",
                          f"asset {base} es '{clase_real}': PROHIBIDO "
                          "como pin para cualquier tipo") and ok
            declarada = pin.get("clase_asset")
            if not declarada:
                ok = fail("clase_tipo",
                          "pin.json debe declarar `clase_asset` (qué ES "
                          "la imagen, según el mapa verificado)") and ok
            elif declarada != clase_real:
                ok = fail("clase_tipo",
                          f"clase declarada '{declarada}' != clase real "
                          f"del mapa '{clase_real}' para {base}") and ok
            elif clase_real not in TIPO_CLASES.get(tipo, set()):
                ok = fail("clase_tipo",
                          f"tipo {tipo} ({TIPOS[tipo]}) incompatible con "
                          f"clase '{clase_real}' de {base}; compatibles: "
                          f"{sorted(TIPO_CLASES.get(tipo, set()))}") and ok

    # claims: el texto afirma solo lo que la imagen es
    texto = f"{pin.get('titulo','')} {pin.get('descripcion','')}".lower()
    if re.search(r"size chart|size guide|tabla de tallas|gu[ií]a de tallas",
                 texto):
        ok = fail("claims",
                  "el texto del pin menciona tabla/guía de tallas: eso "
                  "no es un pin de producto") and ok
    if tipo != 4 and clase_real is not None:
        if re.search(r"close[-\s]?up", texto) and clase_real != "close-up":
            ok = fail("claims",
                      f"el texto afirma 'close-up' pero la clase real "
                      f"del asset es '{clase_real}'") and ok
        if re.search(r"\bfolded\b|doblada", texto) \
                and clase_real != "folded-decorado":
            ok = fail("claims",
                      f"el texto afirma 'folded/doblada' pero la clase "
                      f"real del asset es '{clase_real}'") and ok

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
        texto_kw = (pin["titulo"] + " " + pin["descripcion"]).lower()
        if not any(p in texto_kw for p in phrases):
            ok = fail("keywords_banco",
                      "título+descripción sin keyword multi-palabra del banco") and ok

    # tablero
    if not pin["tablero"].strip():
        ok = fail("tablero", "tablero vacío") and ok

    if ok:
        extra = f" clase={clase_real}" if clase_real else ""
        print(f"PASS [tipo {tipo} {TIPOS[tipo]}] slug={slug}{extra}")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
