#!/usr/bin/env python3
"""Upscale x2 de arte RGBA para impresión POD (My POD, 2026-10-16).

El generador de imágenes entrega 1600x1600 RGB sin alfa; la puerta exige
lado menor >= 3000px. Pipeline:
  1. limpiar-fondo.py (canónico) -> RGBA con fondo transparente
  2. FSRCNN-small x2 sobre RGB + cv2.resize Lanczos sobre el alfa
     (receta verificada 2026-10-08 en TOOLS.md)
  3. alfa < 16 -> 0 (limpia la franja de 1px que deja el resize)
  4. verificar-arte.py --ancho-pulgadas 10.5

Uso: upscale-arte-fsrcnn.py --archivo p028-print-300dpi.png
Sobrescribe el archivo (el original de 1600px no se necesita conservar).
"""
import argparse
import subprocess
import sys

import cv2
import numpy as np
from PIL import Image

MODEL = "/home/hatch/.cache/superres/FSRCNN-small_x2.pb"
LIMPIAR = "/home/hatch/workspace/my-pod/skills/puerta-arte-propuesta/scripts/limpiar-fondo.py"
VERIFICAR = "/home/hatch/workspace/my-pod/skills/puerta-arte-propuesta/scripts/verificar-arte.py"
ANCHO_PULGADAS = 10.5


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--archivo", required=True)
    args = ap.parse_args()
    path = args.archivo

    r = subprocess.run([sys.executable, LIMPIAR, "--archivo", path],
                       capture_output=True, text=True)
    print(r.stdout.strip() or r.stderr.strip())

    im = Image.open(path).convert("RGBA")
    a = np.array(im)
    rgb, alpha = a[..., :3], a[..., 3]

    sr = cv2.dnn_superres.DnnSuperResImpl_create()
    sr.readModel(MODEL)
    sr.setModel("fsrcnn", 2)
    rgb_up = sr.upsample(cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR))
    rgb_up = cv2.cvtColor(rgb_up, cv2.COLOR_BGR2RGB)
    alpha_up = cv2.resize(alpha, None, fx=2, fy=2,
                         interpolation=cv2.INTER_LANCZOS4)
    alpha_up[alpha_up < 16] = 0

    out = np.dstack([rgb_up, alpha_up]).astype(np.uint8)
    Image.fromarray(out).save(path)
    print(f"upscale x2: {a.shape[1]}x{a.shape[0]} -> "
          f"{out.shape[1]}x{out.shape[0]}")

    r = subprocess.run(
        [sys.executable, VERIFICAR, "--archivo", path,
         "--ancho-pulgadas", str(ANCHO_PULGADAS)],
        capture_output=True, text=True)
    print(r.stdout.strip())
    if r.stderr.strip():
        print(r.stderr.strip(), file=sys.stderr)
    sys.exit(r.returncode)


if __name__ == "__main__":
    main()
