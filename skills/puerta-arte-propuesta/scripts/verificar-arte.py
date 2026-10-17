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
  3. recorte_ajustado: el bbox del contenido REAL (alfa>=128) deja, EN
     CADA LADO por separado, <= max(MARGEN_MAX px, MARGEN_MAX_PCT% del
     lado) transparentes (criterio del dueño: el arte viene recortado
     exacto, sin bordes vacíos — los bordes vacíos distorsionan el área
     de impresión en Printify). CORRECCIÓN 2026-10-17: la versión
     anterior medía el margen MENOR de los 4 lados (min) — un arte con
     aire enorme en 3 lados y pegado en 1 pasaba; y el canónico
     vitals-stable trae 22px como MÍNIMO pero 50px de máximo, así que
     el "≤32px" histórico nunca midió lo que decía. Ahora se mide el
     margen de cada lado contra su tope.
  4. dpi: ancho_px / ancho_pulgadas >= 300.
  5. dimensiones: lado menor >= LADO_MIN px (archivo de impresión).
  6. sin_blancos_interiores: blanco opaco dentro del bbox <= 8% (atrapa el
     fondo sin limpiar: p022 mancha entre los elfos, 2026-10-15). Entre 2%
     y 8% se marca para adjudicación visual (puede ser blanco de diseño:
     papel, copos — no se destruye con key global).
  7. aspecto_informativo: se mide h/w pero NO bloquea (corrección suya
     2026-10-15): los diseños altos están permitidos; el criterio va en la
     COLOCACIÓN (scale-to-fit): el diseño debe verse COMPLETO, nada cortado.
  8. sin_blanco_puro: blanco puro (min RGB>=250, spread<=18) <= 0.3%
     (método canónico 2026-10-15): el diseño usa crema, nunca blanco puro;
     blanco puro = fondo sin limpiar en counters y espacios encerrados.
     Si falla: correr scripts/limpiar-fondo.py y re-verificar.
  9. dpi_al_zoom (SOLO con --exigir-margen-zoom, corrección del dueño
     2026-10-17): el dueño agranda la colocación en su revisión (~+20%)
     y un arte que apenas pasa 300 DPI al ancho nominal cae a
     250-260 DPI al agrandarlo — "ya no lo puedo jugar". Este gate exige
     que el ANCHO DEL CONTENIDO (bbox alfa>=128, no el lienzo) rinda
     >=300 DPI al ancho máximo de colocación (ancho nominal x
     ZOOM_HEADROOM=1.20). Si falla: escalar el arte
     (scripts/upscale-arte-fsrcnn.py) y re-verificar ANTES del draft.

Reparación: --autotrim --salida <png> recorta al bbox + 4px y verifica
el resultado (verifier-repair). Limpieza: scripts/limpiar-fondo.py
elimina el blanco puro global (ver método canónico en SKILL.md).

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

MARGEN_MAX = 48    # px por lado: más que esto (y más que el % de abajo)
                   # es "bordes vacíos". (Antes: 32px medidos como MÍNIMO
                   # entre lados — mal; vitals-print trae máx 50px por lado.)
MARGEN_MAX_PCT = 4.0  # % del lado correspondiente (el tope efectivo por
                      # lado es max(MARGEN_MAX, MARGEN_MAX_PCT% del lado);
                      # calibrado 2026-10-17: vitals máx 84px=2.7% PASS,
                      # lote de ayer 137-302px=4.3-9.4% FAIL)
ALFA_CONTENIDO = 128  # el bbox de contenido se mide con alfa>=128: píxeles
                      # casi transparentes (ruido/antialias) no son diseño
                      # y no deben inflar el bbox ni esconder el aire real
MASA_BORDE_PCT = 0.05  # % de la masa de contenido que debe acumularse desde
                      # cada lado para fijar el borde (mata píxeles sueltos
                      # y slivers de borde sin tocar el cuerpo del diseño)
ZOOM_HEADROOM = 1.20  # el dueño agranda la colocación ~+20% al revisar:
                      # el arte debe rendir 300 DPI a ese ancho, no solo
                      # al nominal (corrección suya 2026-10-17)
TRIM_PAD = 4     # px de aire al recortar
LADO_MIN = 3000
DPI_MIN = 300
BLANCO_UMBRAL = 225       # min(R,G,B) >= esto = "casi-blanco" (atrapa también
                           # el crema/beige del fondo sin limpiar, p022 2026-10-15)
BLANCO_SPREAD_MAX = 45     # max-min <= esto (un color saturado no es "blanco")
BLANCO_INTERIOR_MAX = 8.0  # % del bbox: más que esto = fondo sin limpiar (FAIL)
BLANCO_ADJUDICAR = 2.0     # % del bbox: entre esto y el max = adjudicación visual
# (ASPECTO_MAX eliminado 2026-10-15: el aspecto no bloquea — corrección suya)


def bbox_contenido(im):
    """BBox del contenido REAL, robusto a píxeles sueltos.

    Medido sobre alfa >= ALFA_CONTENIDO y recortando desde cada lado
    hasta acumular MASA_BORDE_PCT% de la masa total de contenido.
    Motivo (verificado 2026-10-17 sobre el lote p028-p037): el bbox
    ingenuo (getbbox, cualquier alfa>0 — y también alfa>=128) lo define
    UN píxel suelto: los PNG traen slivers de borde (una columna de
    ~128px semitransparentes en x=0) y neblina alfa baja en todo el
    lienzo, así que el bbox daba el lienzo entero, el margen medía 0
    y el aire real del diseño (p. ej. p030: ~275px de aire puro a la izquierda, 4-9% por lado en el lote
    puro) era invisible para la puerta. La masa acumulada mide el
    borde que el ojo ve: el aire puro aporta 0 y un sliver aporta
    ~0.003%, el cuerpo del diseño aporta el resto."""
    try:
        import numpy as np
        a = np.array(im.getchannel("A"))
        mask = a >= ALFA_CONTENIDO
        total = int(mask.sum())
        if total == 0:
            return None
        umbral = total * MASA_BORDE_PCT / 100.0
        col = mask.sum(axis=0)
        row = mask.sum(axis=1)
        xs = np.where(np.cumsum(col) >= umbral)[0]
        xs_fin = np.where(np.cumsum(col[::-1]) >= umbral)[0]
        ys = np.where(np.cumsum(row) >= umbral)[0]
        ys_fin = np.where(np.cumsum(row[::-1]) >= umbral)[0]
        if not len(xs) or not len(ys):
            return None
        l = int(xs[0]); r = int(len(col) - xs_fin[0])
        t = int(ys[0]); b = int(len(row) - ys_fin[0])
        return (l, t, r, b)
    except Exception:
        a = im.getchannel("A").point(
            lambda v: 255 if v >= ALFA_CONTENIDO else 0)
        return a.getbbox()


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
    # G3: recorte ajustado — POR LADO (corrección 2026-10-17: antes min())
    bbox = bbox_contenido(im)
    if bbox is None:
        g3, med["margen_px"] = False, 0
    else:
        l, t, r, b = bbox
        margenes = {"izq": l, "arr": t, "der": w - r, "aba": h - b}
        med["margenes_px"] = margenes
        med["margen_px"] = max(margenes.values())
        tope_x = max(MARGEN_MAX, MARGEN_MAX_PCT / 100.0 * w)
        tope_y = max(MARGEN_MAX, MARGEN_MAX_PCT / 100.0 * h)
        g3 = (margenes["izq"] <= tope_x and margenes["der"] <= tope_x
              and margenes["arr"] <= tope_y and margenes["aba"] <= tope_y)
    gates["recorte_ajustado"] = {"pass": g3, "maximo_px": MARGEN_MAX,
                                 "maximo_pct": MARGEN_MAX_PCT}
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
    # G8: sin blanco PURO (2026-10-15, método canónico): el diseño usa crema,
    # nunca blanco puro (min>=250, spread<=18). Blanco puro = fondo sin limpiar,
    # incluidos counters y espacios encerrados. Umbral estricto: >0.3% = FAIL.
    # Si falla, correr scripts/limpiar-fondo.py y re-verificar.
    if bbox is None:
        g8, med["blanco_puro_pct"] = False, 0.0
    else:
        import numpy as _np
        arr = _np.array(im)
        rgb8 = arr[..., :3].astype(int)
        mn8 = rgb8.min(axis=2); sp8 = rgb8.max(axis=2) - mn8
        puro = (mn8 >= 250) & (sp8 <= 18) & (arr[..., 3] > 128)
        pct_puro = float(100 * puro.sum() / (arr.shape[0] * arr.shape[1]))
        med["blanco_puro_pct"] = round(pct_puro, 3)
        g8 = bool(pct_puro <= 0.3)
    gates["sin_blanco_puro"] = {"pass": g8, "maximo_pct": 0.3}
    violado = violado or (None if g8 else "blanco_puro_fondo_sin_limpiar")
    # G7: aspecto (INFORMATIVO, no bloquea — corrección suya 2026-10-15)
    # Los diseños altos están permitidos; el criterio va en la COLOCACIÓN
    # (scale-to-fit en publicar-printify-etsy): el diseño debe verse
    # COMPLETO en el mockup, nada cortado. El arte no se rechaza por alto.
    aspecto = h / w if w else 0
    med["aspecto_h_w"] = round(aspecto, 3)
    g7 = True
    gates["aspecto_informativo"] = {"pass": g7, "valor": round(aspecto, 3)}
    # G9: DPI al zoom (solo si se exige margen de zoom — flujo propuestas)
    # El dueño agranda la colocación ~+20% en su revisión; el contenido
    # (no el lienzo) debe rendir >=300 DPI a ese ancho máximo.
    if getattr(a, "exigir_margen_zoom", False):
        ancho_max = a.ancho_pulgadas * ZOOM_HEADROOM
        if bbox is None:
            g9, med["dpi_al_zoom"] = False, 0.0
        else:
            ancho_contenido = bbox[2] - bbox[0]
            med["ancho_contenido_px"] = ancho_contenido
            med["dpi_al_zoom"] = round(ancho_contenido / ancho_max, 1) \
                if ancho_max > 0 else 0.0
            g9 = med["dpi_al_zoom"] >= DPI_MIN
        med["ancho_max_pulgadas"] = round(ancho_max, 2)
        gates["dpi_al_zoom"] = {"pass": g9, "minimo": DPI_MIN,
                                 "headroom": ZOOM_HEADROOM}
        violado = violado or (None if g9 else "dpi_sin_margen_zoom")
    return gates, violado, med


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--archivo", required=True)
    ap.add_argument("--ancho-pulgadas", type=float, default=10.5)
    ap.add_argument("--exigir-margen-zoom", action="store_true",
                    help="exige 300 DPI del contenido al ancho nominal x1.20 "
                         "(el dueño agranda la colocación al revisar)")
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
        bbox = bbox_contenido(im)
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
