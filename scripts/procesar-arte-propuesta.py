#!/usr/bin/env python3
"""Procesa arte crudo de propuesta -> PNG print-ready con puerta.

Pipeline por diseno:
  1. Carga PNG RGB (fondo blanco generado por el modelo).
  2. Remueve fondo por flood-fill desde las 4 esquinas (tolerancia) -> alfa.
  3. Limpia alfa<16 -> 0 (leccion esquinas, TOOLS.md).
  4. Upscale: FSRCNN-small x2 en RGB + Lanczos x2 en alfa; luego Lanczos
     hasta el tamano objetivo.
  5. Guarda <id>-print-300dpi.png y corre la puerta con --autotrim.

Uso: procesar-arte-propuesta.py --entrada raw.png --salida p021-print-300dpi.png
"""
import argparse
import subprocess
import sys

import cv2
import numpy as np
from PIL import Image

FSRCNN_MODEL = "/home/hatch/.cache/superres/FSRCNN-small_x2.pb"
TOL = 24          # tolerancia flood-fill fondo blanco
OBJETIVO_ANCHO = 4000   # px para retrato (margen de zoom 2026-10-17: el
                        # contenido debe rendir >=300 DPI al ancho nominal
                        # x1.20 -> >=3780px a 10.5"; 3600 se quedaba corto)
OBJETIVO_CUADRADO = 4400


def fondo_a_alfa(img_rgb):
    """Flood-fill desde las 4 esquinas sobre pixeles casi-blancos -> canal alfa."""
    h, w = img_rgb.shape[:2]
    mascara = np.zeros((h + 2, w + 2), np.uint8)
    # fondo de referencia: mediana de un borde de 8px
    borde = np.concatenate([
        img_rgb[:8, :, :].reshape(-1, 3), img_rgb[-8:, :, :].reshape(-1, 3),
        img_rgb[:, :8, :].reshape(-1, 3), img_rgb[:, -8:, :].reshape(-1, 3),
    ])
    ref = np.median(borde, axis=0).astype(np.uint8)
    dist = np.linalg.norm(img_rgb.astype(np.int16) - ref.astype(np.int16), axis=2)
    cerca_blanco = (dist <= TOL * 1.73).astype(np.uint8) * 255  # ~tolerancia euclidiana

    # flood fill desde esquinas sobre la mascara de "casi blanco"
    ff_mask = np.zeros((h + 2, w + 2), np.uint8)
    semilla = cerca_blanco.copy()
    for x0, y0 in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]:
        if semilla[y0, x0]:
            cv2.floodFill(semilla, ff_mask, (x0, y0), 128)
    fondo = (semilla == 128)
    alfa = np.where(fondo, 0, 255).astype(np.uint8)
    # antialias: pixeles casi-blancos conectados al fondo pero no puros -> semi
    borde_suave = (dist <= TOL * 1.73) & fondo
    alfa_suave = np.clip(255 - (dist * 4).astype(np.int32), 0, 255).astype(np.uint8)
    alfa = np.where(borde_suave, np.minimum(alfa, alfa_suave), alfa)
    alfa[alfa < 16] = 0
    return alfa


def upscale(rgb, alfa):
    sr = cv2.dnn_superres.DnnSuperResImpl_create()
    sr.readModel(FSRCNN_MODEL)
    sr.setModel("fsrcnn", 2)
    rgb2 = sr.upsample(cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR))
    rgb2 = cv2.cvtColor(rgb2, cv2.COLOR_BGR2RGB)
    h2, w2 = rgb2.shape[:2]
    alfa2 = cv2.resize(alfa, (w2, h2), interpolation=cv2.INTER_LANCZOS4)
    return rgb2, alfa2


def main():
    a = argparse.ArgumentParser()
    a.add_argument("--entrada", required=True)
    a.add_argument("--salida", required=True)
    a.add_argument("--ancho-pulgadas", type=float, default=10.5)
    args = a.parse_args()

    im = Image.open(args.entrada).convert("RGB")
    rgb = np.array(im)
    w, h = im.size
    print(f"entrada: {w}x{h}")

    alfa = fondo_a_alfa(rgb)
    pct_transp = (alfa == 0).mean() * 100
    print(f"fondo removido: {pct_transp:.1f}% transparente")

    try:
        rgb2, alfa2 = upscale(rgb, alfa)
        print(f"FSRCNN x2: {rgb2.shape[1]}x{rgb2.shape[0]}")
    except Exception as e:
        print(f"FSRCNN fallo ({e}), usando solo Lanczos x2")
        rgb2 = cv2.resize(rgb, (w * 2, h * 2), interpolation=cv2.INTER_LANCZOS4)
        alfa2 = cv2.resize(alfa, (w * 2, h * 2), interpolation=cv2.INTER_LANCZOS4)

    h2, w2 = rgb2.shape[:2]
    if w2 == h2:
        objetivo = (OBJETIVO_CUADRADO, OBJETIVO_CUADRADO)
    else:
        escala = OBJETIVO_ANCHO / w2
        objetivo = (OBJETIVO_ANCHO, round(h2 * escala))
    rgb3 = cv2.resize(rgb2, objetivo, interpolation=cv2.INTER_LANCZOS4)
    alfa3 = cv2.resize(alfa2, objetivo, interpolation=cv2.INTER_LANCZOS4)
    alfa3[alfa3 < 16] = 0

    rgba = np.dstack([rgb3, alfa3])
    Image.fromarray(rgba).save(args.salida)
    print(f"guardado: {args.salida} {objetivo[0]}x{objetivo[1]}")

    # puerta con autotrim
    cmd = [sys.executable,
           "/home/hatch/workspace/my-pod/skills/puerta-arte-propuesta/scripts/verificar-arte.py",
           "--archivo", args.salida, "--ancho-pulgadas", str(args.ancho_pulgadas),
           "--autotrim", "--salida", args.salida]
    r = subprocess.run(cmd, capture_output=True, text=True)
    print(r.stdout.strip())
    print(r.stderr.strip()[-500:] if r.returncode not in (0, 1) else "", file=sys.stderr)
    sys.exit(r.returncode)


if __name__ == "__main__":
    main()
