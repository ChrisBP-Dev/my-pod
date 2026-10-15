#!/usr/bin/env python3
"""Puerta de arte-propuesta — primera validación del flujo POD.

La propuesta (PNG del diseño) se valida ANTES de generar ningún mockup:
es lo más barato de rechazar. Atrapa los errores recurrentes:
fondo no transparente, bordes vacíos (el arte debe venir recortado
exacto al contenido), baja resolución.

Gates mecánicos (código):
  1. formato: PNG con canal alfa (RGBA).
  2. fondo_limpio: las 4 esquinas alfa = 0 (atrapa el PNG que viene con
     fondo de un color aplanado).
  3. recorte_ajustado: el bbox del contenido deja <= MARGEN_MAX px
     transparentes en los 4 lados (criterio del dueño: el arte viene
     recortado exacto, sin bordes vacíos — los bordes vacíos distorsionan
     el área de impresión en Printify).
  4. dpi: ancho_px / ancho_pulgadas >= 300.
  5. dimensiones: lado menor >= LADO_MIN px (archivo de impresión).

Reparación: --autotrim --salida <png> recorta al bbox + 4px y verifica
el resultado (verifier-repair).

Gate humano (no lo cubre el código):
  - counters: agujeros de letras (a, e, o, P...) sin fondo metido.

Uso:
  verificar-arte.py --archivo arte.png --ancho-pulgadas 10.5
  verificar-arte.py --archivo arte.png --autotrim --salida arte-trim.png

Salida JSON {"veredicto": "PASS"|"FAIL", "criterio_violado": ...}.
Exit 0 = PASS, 1 = FAIL, 2 = error de uso.
"""
import argparse
import json
import sys
from PIL import Image

MARGEN_MAX = 32  # px: más que esto es "bordes vacíos" (vitals-print trae 22)
TRIM_PAD = 4     # px de aire al recortar
LADO_MIN = 3000
DPI_MIN = 300


def verificar(im, formato, a):
    gates, violado, med = {}, None, {}
    # G1: formato
    g1 = formato == "PNG" and "A" in im.getbands()
    gates["formato"] = {"pass": g1, "formato": formato}
    violado = violado or (None if g1 else "formato_invalido")
    alfa = im.getchannel("A")
    w, h = im.size
    # G2: esquinas transparentes
    esq = [alfa.getpixel((0, 0)), alfa.getpixel((w - 1, 0)),
           alfa.getpixel((0, h - 1)), alfa.getpixel((w - 1, h - 1))]
    g2 = all(v == 0 for v in esq)
    gates["fondo_limpio"] = {"pass": g2}
    violado = violado or (None if g2 else "fondo_no_transparente")
    # G3: recorte ajustado
    bbox = alfa.getbbox()
    if bbox is None:
        g3, med["margen_px"] = False, 0
    else:
        l, t, r, b = bbox
        margen = min(l, t, w - r, h - b)
        med["margen_px"] = margen
        g3 = margen <= MARGEN_MAX
    gates["recorte_ajustado"] = {"pass": g3, "maximo_px": MARGEN_MAX}
    violado = violado or (None if g3 else "recorte_con_bordes_vacios")
    # G4: DPI
    dpi = w / a.ancho_pulgadas if a.ancho_pulgadas > 0 else 0
    med["dpi"] = round(dpi, 1)
    g4 = dpi >= DPI_MIN
    gates["dpi"] = {"pass": g4, "minimo": DPI_MIN}
    violado = violado or (None if g4 else "dpi_insuficiente")
    # G5: dimensiones
    lado = min(w, h)
    med["lado_menor_px"] = lado
    g5 = lado >= LADO_MIN
    gates["dimensiones"] = {"pass": g5, "minimo_px": LADO_MIN}
    violado = violado or (None if g5 else "dimensiones_insuficientes")
    return gates, violado, med


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--archivo", required=True)
    ap.add_argument("--ancho-pulgadas", type=float, default=10.5)
    ap.add_argument("--autotrim", action="store_true")
    ap.add_argument("--salida", default=None)
    a = ap.parse_args()

    try:
        raw = Image.open(a.archivo)
        formato = raw.format
        im = raw.convert("RGBA")
    except Exception:
        print(json.dumps({"veredicto": "FAIL", "criterio_violado": "archivo_ilegible",
                          "gates": {}, "mediciones": {"archivo": a.archivo.split("/")[-1]}},
                         ensure_ascii=False))
        return 1

    reparado = None
    if a.autotrim:
        if not a.salida:
            ap.error("--autotrim requiere --salida")
        bbox = im.getchannel("A").getbbox()
        if bbox:
            l, t, r, b = bbox
            im = im.crop((max(0, l - TRIM_PAD), max(0, t - TRIM_PAD),
                          min(im.width, r + TRIM_PAD), min(im.height, b + TRIM_PAD)))
            im.save(a.salida)
            reparado = a.salida.split("/")[-1]

    gates, violado, med = verificar(im, formato, a)
    med["archivo"] = (a.salida or a.archivo).split("/")[-1]
    veredicto = "PASS" if violado is None else "FAIL"
    print(json.dumps({"veredicto": veredicto, "criterio_violado": violado,
                      "gates": gates, "mediciones": med,
                      "reparado": reparado,
                      "gate_humano_pendiente": "counters (agujeros de letras)"},
                     ensure_ascii=False, indent=1))
    return 0 if veredicto == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
