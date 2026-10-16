#!/usr/bin/env python3
"""Repara fondos casi-blancos no puros en artes ya limpiados (My POD, 2026-10-16).

El generador a veces entrega fondo casi-blanco neutro (244-249) que el key
canónico (blanco puro, min>=250) no atrapa. Este script elimina por
flood-fill desde el borde solo píxeles neutros casi-blancos
(min>=230, dispersión<=25, alfa>128): el fondo está conectado al borde;
los blancos de diseño (crema cálido, encerrados) se preservan.

Uso: reparar-fondo-casi-blanco.py --archivo ARTE.png [--verificar]
"""
import argparse
import subprocess
import sys
from collections import deque

import numpy as np
from PIL import Image

MIN_NEAR = 230
SPREAD_NEAR = 25
VERIFICAR = "/home/hatch/workspace/my-pod/skills/puerta-arte-propuesta/scripts/verificar-arte.py"


def reparar(path):
    im = Image.open(path).convert("RGBA")
    a = np.array(im)
    h, w = a.shape[:2]
    rgb = a[..., :3].astype(int)
    al = a[..., 3]
    mn = rgb.min(axis=2)
    mx = rgb.max(axis=2)
    near = (mn >= MIN_NEAR) & ((mx - mn) <= SPREAD_NEAR) & (al > 128)

    seen = np.zeros((h, w), dtype=bool)
    q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if near[y, x] and not seen[y, x]:
                seen[y, x] = True
                q.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if near[y, x] and not seen[y, x]:
                seen[y, x] = True
                q.append((y, x))
    n = 0
    while q:
        y, x = q.popleft()
        a[y, x, 3] = 0
        n += 1
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            yy, xx = y + dy, x + dx
            if 0 <= yy < h and 0 <= xx < w and near[yy, xx] and not seen[yy, xx]:
                seen[yy, xx] = True
                q.append((yy, xx))
    Image.fromarray(a).save(path)
    print(f"fondo casi-blanco (flood-fill borde): {n} px "
          f"({100*n/(h*w):.3f}%) -> {path}")
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--archivo", required=True)
    ap.add_argument("--verificar", action="store_true")
    args = ap.parse_args()
    reparar(args.archivo)
    if args.verificar:
        r = subprocess.run(
            [sys.executable, VERIFICAR, "--archivo", args.archivo,
             "--ancho-pulgadas", "10.5"], capture_output=True, text=True)
        print(r.stdout.strip())
        sys.exit(r.returncode)


if __name__ == "__main__":
    main()
