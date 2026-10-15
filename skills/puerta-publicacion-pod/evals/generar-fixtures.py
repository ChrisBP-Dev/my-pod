#!/usr/bin/env python3
"""Regenera los fixtures sintéticos de regresión (F2, F3).

Lee el flat-lay aprobado del golden set, extrae el diseño en su bbox medido,
rellena el hueco por inpaint y re-pega el diseño con la desviación indicada.
Determinista: OpenCV inpaint (TELEA) y resize (LANCZOS) no usan azar.

Uso: generar-fixtures.py --golden-root <dir> --salida <dir>
"""
import argparse, os
import cv2
import numpy as np

# bbox medido del diseño en el flat-lay aprobado (ver references/flat-lay.md)
X, Y, W, H = 715, 570, 526, 534


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--golden-root", required=True)
    ap.add_argument("--salida", required=True)
    a = ap.parse_args()
    src = os.path.join(a.golden_root, "flatlay-prop2-white-v1-2000.jpg")
    img = cv2.imread(src)
    if img is None:
        raise SystemExit(f"no se encontró el flat-lay aprobado: {src}")
    os.makedirs(a.salida, exist_ok=True)
    patch = img[Y:Y + H, X:X + W].copy()
    mask = np.zeros(img.shape[:2], np.uint8)
    cv2.rectangle(mask, (X - 8, Y - 8), (X + W + 8, Y + H + 8), 255, -1)
    base = cv2.inpaint(img, mask, 21, cv2.INPAINT_TELEA)

    f2 = base.copy()  # F2: diseño movido +120 px en X
    f2[Y:Y + H, X + 120:X + 120 + W] = patch
    cv2.imwrite(os.path.join(a.salida, "desplazado-dx120.jpg"), f2,
                [cv2.IMWRITE_JPEG_QUALITY, 95])

    f3 = base.copy()  # F3: diseño al 85%, centrado en el centro original
    nw, nh = int(W * 0.85), int(H * 0.85)
    chico = cv2.resize(patch, (nw, nh), interpolation=cv2.INTER_LANCZOS4)
    cx, cy = X + W // 2, Y + H // 2
    f3[cy - nh // 2:cy - nh // 2 + nh, cx - nw // 2:cx - nw // 2 + nw] = chico
    cv2.imwrite(os.path.join(a.salida, "encogido-85.jpg"), f3,
                [cv2.IMWRITE_JPEG_QUALITY, 95])
    print("fixtures F2 y F3 generados en", a.salida)


if __name__ == "__main__":
    main()
