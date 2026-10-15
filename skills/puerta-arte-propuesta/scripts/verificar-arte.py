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
  6. sin_blancos_interiores: blanco opaco dentro del bbox <= 8% (atrapa el
     fondo sin limpiar: p022 mancha entre los elfos, 2026-10-15). Entre 2%
     y 8% se marca para adjudicación visual (puede ser blanco de diseño:
     papel, copos — no se destruye con key global).
  7. cabe_en_area_impresion: aspecto h/w <= 1.10 (el área Gildan 18000 es
     1.14; un arte más alto se CORTA al colocarlo — caso 2026-10-15).

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
BLANCO_UMBRAL = 225       # min(R,G,B) >= esto = "casi-blanco" (atrapa también
                           # el crema/beige del fondo sin limpiar, p022 2026-10-15)
BLANCO_SPREAD_MAX = 45     # max-min <= esto (un color saturado no es "blanco")
BLANCO_INTERIOR_MAX = 8.0  # % del bbox: más que esto = fondo sin limpiar (FAIL)
BLANCO_ADJUDICAR = 2.0     # % del bbox: entre esto y el max = adjudicación visual
ASPECTO_MAX = 1.10         # h/w máximo: el área de impresión Gildan 18000 es
                           # 1.14 (4398/3852 px); con margen queda 1.10.
                           # Un arte más alto se CORTA al colocarlo al 78% de
                           # ancho (caso 2026-10-15: ratios hasta 1.93).


def blancos_interiores(im, bbox):
    """% del bbox que es blanco opaco + % conectado al borde del bbox.
    El fondo sin limpiar toca el borde del diseño (p022: mancha entre los
    elfos); los blancos DE DISEÑO (papel, copos) quedan encerrados."""
    import numpy as np
    a = np.array(im)
    l, t, r, b = bbox
    region = a[t:b, l:r]
    rgb = region[..., :3].astype(int)
    alfa = region[..., 3]
    mn = rgb.min(axis=2)
    mx = rgb.max(axis=2)
    blanco = (mn >= BLANCO_UMBRAL) & ((mx - mn) <= BLANCO_SPREAD_MAX) & (alfa > 128)
    total = blanco.size
    pct = 100.0 * blanco.sum() / total if total else 0.0
    # conectividad al borde del bbox (flood fill manual por BFS)
    h, w = blanco.shape
    visit = np.zeros_like(blanco, dtype=bool)
    stack = []
    for x in range(w):
        if blanco[0, x]: stack.append((0, x))
        if blanco[h - 1, x]: stack.append((h - 1, x))
    for y in range(h):
        if blanco[y, 0]: stack.append((y, 0))
        if blanco[y, w - 1]: stack.append((y, w - 1))
    while stack:
        y, x = stack.pop()
        if y < 0 or y >= h or x < 0 or x >= w or visit[y, x] or not blanco[y, x]:
            continue
        visit[y, x] = True
        stack += [(y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)]
    pct_borde = 100.0 * visit.sum() / total if total else 0.0
    return round(pct, 2), round(pct_borde, 2)


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
    # G6: sin blancos interiores (fondo sin limpiar dentro del diseño)
    if bbox is None:
        g6, med["blanco_interior_pct"] = False, 0.0
    else:
        pct, pct_borde = blancos_interiores(im, bbox)
        pct, pct_borde = float(pct), float(pct_borde)
        med["blanco_interior_pct"] = pct
        med["blanco_conectado_borde_pct"] = pct_borde
        g6 = bool(pct <= BLANCO_INTERIOR_MAX)
        # entre BLANCO_ADJUDICAR y MAX: el blanco puede ser de diseño
        # (papel, copos) → no FAIL automático, pero se marca para adjudicar
        med["blanco_requiere_adjudicacion"] = bool(BLANCO_ADJUDICAR < pct <= BLANCO_INTERIOR_MAX)
    gates["sin_blancos_interiores"] = {"pass": g6, "maximo_pct": BLANCO_INTERIOR_MAX}
    violado = violado or (None if g6 else "fondo_sin_limpiar_en_interiores")
    # G7: el arte cabe en el área de impresión (no se corta al colocarlo)
    aspecto = h / w if w else 0
    med["aspecto_h_w"] = round(aspecto, 3)
    g7 = aspecto <= ASPECTO_MAX
    gates["cabe_en_area_impresion"] = {"pass": g7, "maximo": ASPECTO_MAX}
    violado = violado or (None if g7 else "arte_mas_alto_que_el_area")
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
