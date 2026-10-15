#!/usr/bin/env python3
"""Limpieza canónica de fondo para artes POD (My POD, 2026-10-15).

Método verificado en el rescate p021-p026:
- El diseño usa CREMA/blanco roto para sus elementos claros (nunca blanco puro).
- Los restos de fondo son BLANCO PURO (min RGB >= 250, dispersión <= 18).
- Eliminar blanco puro globalmente quita TODO el fondo —incluidos counters
  y espacios encerrados entre letras— sin tocar el diseño.

Uso: limpiar-fondo.py --archivo ARTE.png [--salida SALIDA.png]
Si no se da --salida, sobrescribe el archivo (el original debe estar en git).
"""
import argparse
import numpy as np
from PIL import Image

PURO_MIN = 250
PURO_SPREAD = 18


def limpiar(path_in, path_out):
    im = Image.open(path_in).convert("RGBA")
    a = np.array(im)
    rgb = a[..., :3].astype(int)
    mn = rgb.min(axis=2)
    mx = rgb.max(axis=2)
    puro = (mn >= PURO_MIN) & ((mx - mn) <= PURO_SPREAD) & (a[..., 3] > 128)
    n = int(puro.sum())
    a[puro, 3] = 0
    Image.fromarray(a).save(path_out)
    total = a.shape[0] * a.shape[1]
    return {"eliminados_px": n, "pct": round(100 * n / total, 3)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--archivo", required=True)
    ap.add_argument("--salida", default=None)
    args = ap.parse_args()
    out = args.salida or args.archivo
    res = limpiar(args.archivo, out)
    print(f"blanco puro eliminado: {res['eliminados_px']} px ({res['pct']}%) -> {out}")


if __name__ == "__main__":
    main()
