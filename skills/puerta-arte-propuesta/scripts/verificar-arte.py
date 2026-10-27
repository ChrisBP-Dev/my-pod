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
 10. composicion_completa (SOLO con --es-original, sobre el CRUDO de
     generación, ANTES de cualquier recorte — corrección 2026-10-18):
     el contenido que toca el borde del lienzo original es señal de
     truncamiento (la generación cortó el diseño, o un paso posterior
     lo desbordó). Se mide con el bbox SEGURO (componentes reales, ver
     bbox_seguro) por lado: cada margen debe ser >= max(6px, 0.4% del
     lado). Calibración 2026-10-18 (lote p038-p057): los 16 crudos
     completos dejan >= 0.86% por lado; los 16 prints mutilados tocan
     el borde (margen seguro 0) en los CUATRO lados. Un elemento que
     llega al borde con trazo ACABADO (motivo de diseño, p. ej. una
     línea EKG que cruza) se adjudica VISUALMENTE — la puerta marca,
     el humano decide; no se asume completo ni cortado.
 11. contenido_intacto (finales): el bbox seguro del archivo final NO
     puede tocar el borde del lienzo (margen seguro >= 2px por lado).
     Este flujo es recorte-al-contenido + pad: si el contenido toca el
     borde del archivo, algo fue rebanado. Calibración: prints
     mutilados del lote = 0px en los 4 lados (16/16); buenos conocidos
     todos >= 12px (v2 corregidos = su pad de 12px; vitals canónico
     24-50px; p036/p037 126-258px).
 12. fidelidad_recorte (SOLO con --original <crudo>): el archivo final
     debe contener TODO el contenido del crudo. Dos mediciones
     deterministas sobre los bbox seguros: (a) el aspecto del contenido
     final vs el del crudo no puede desviarse > 1.5% (un recorte
     anisotrópico deforma); (b) pérdida por banda: normalizando ambas
     máscaras a su bbox seguro en una rejilla 200x200, el contenido del
     crudo en su banda externa (3%) debe tener contraparte en el final
     (tolerancia 1 celda); pérdida > 2% en cualquier lado = FAIL.
     Calibración 2026-10-18: pares fieles (crudo -> v2 corregido)
     pérdida 0.0 en los 16 y aspecto <= 0.5%; pares mutilados: esta
     puerta caza 10/16 (los desbordes tipo fill y los recortes con
     pérdida de banda/aspecto). Los 6 restantes (amputaciones finas
     del trim por masa y el desborde más leve, p052) no los separa
     esta métrica a esa magnitud (medido: el registro por template
     tiene piso de ruido ~0.5%/lado, igual que las pérdidas leves) —
     pero los 16/16 caen en contenido_intacto (gate 11: tocan el
     borde del archivo) y la clase se previene en el MECANISMO:
     --autotrim usa el bbox SEGURO. No se declara cobertura que no hay.
 13. sin_counters_rellenos (2026-10-20, caso p046 "ICU: I Care U"
     cazado por el dueño en Printify): los huecos CERRADOS de las
     letras pueden traer el fondo horneado como píxeles opacos sin
     que ningún gate anterior lo vea — el fondo encerrado no es
     blanco puro (media ~249/245/237: sin_blanco_puro medía 0.0%) ni
     pesa contra el bbox completo (sin_blancos_interiores medía
     0.69%). Detector: componentes de la semilla acromática clara
     (alfa>128, media>=200, spread<=18 — el canon de color de la app:
     los claros de diseño son crema cálido, spread>18; lo acromático
     claro es fondo o damero) con área >= 1500px, densidad
     (área/bbox) >= 0.25 Y grosor (radio inscrito máximo) >= 13px =
     mancha maciza en ambas dimensiones (relleno). Calibración
     2026-10-20: conocidos-buenos (vitals canónico, p036 v3, p037
     v2, p028 y p033 publicados) — ningún componente >=1500px supera
     densidad 0.108; p046 malo — 4 rellenos: área 2245-51632,
     densidad 0.42-0.68, radio 14.0-99.5. Recalibración del mismo
     día (barrido de todo el registro): la densidad sola daba
     falsos positivos — líneas decorativas (p043, radio <=2.8) y
     brillos finos (p045/p062, <=12.8) con densidad hasta 0.66; el
     grosor los separa de lo macizo. Sin grosor suficiente, el
     componente sale en mediciones como counters_sospechosos y NO
     bloquea: zona gris medida (rellenos chicos reales de p052
     conviven con brillos de diseño de p054) que adjudica el ojo.
     Si falla: scripts/limpiar-counters.py (solo limpia rellenos
     duros; los sospechosos exigen --incluir-sospechosos tras
     adjudicar) y re-verificar. Cobertura honesta: rellenos chicos
     (<1500px), tenues o de tono cálido NO los caza este gate —
     siguen en el gate humano de counters.

 14. fuente_plana_bordado (SOLO con --metodo bordado, 2026-10-27,
     unidad F5 de la recalibración — la doctrina vivía en prosa en el
     SKILL y ninguna puerta la medía): la fuente de un bordado es
     PLANA, máx. 6 colores sólidos (doctrina del dueño 2026-10-26 en
     la ficha de la tienda). Medición: sobre una reducción por
     vecino-más-cercano (conserva la paleta exacta), píxeles con
     alfa>=128 cuantizados a cubos de 16 por canal; se cuentan los
     colores dominantes que cubren el 99.5% del contenido (el 0.5%
     restante es el antialiasing de los bordes). Más de 6 dominantes
     = la fuente trae degradados, textura o paleta de DTG: FAIL
     «fuente_bordado_no_plana». Si el concepto nació texturizado, la
     fuente se regenera plana (ver SKILL), no se posteriza.

Reparación: --autotrim --salida <png> recorta al bbox SEGURO + 4px
(antes: bbox por masa 0.05% — amputaba extremos de baja masa: hojas
finas, guirnaldas, iconos; causa raíz del lote A 2026-10-18) y
verifica el resultado (verifier-repair). Si el bbox seguro no se
puede calcular (sin cv2/scipy), cae al bbox por masa y lo declara en
la salida ("autotrim_bbox"). Limpieza: scripts/limpiar-fondo.py
elimina el blanco puro global (ver método canónico en SKILL.md).

Gate humano (lo que el código no cubre):
  - counters: los rellenos GRANDES acromáticos los caza el gate 13;
    quedan para el ojo los chicos, tenues o de tono cálido, y la
    adjudicación de cualquier mancha dudosa.

Uso:
  verificar-arte.py --archivo crudo.png --es-original
  verificar-arte.py --archivo arte.png --ancho-pulgadas 10.5
  verificar-arte.py --archivo arte.png --autotrim --salida arte-trim.png
  verificar-arte.py --archivo arte.png --original crudo.png

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
BORDADO_COLORES_MAX = 6      # colores sólidos dominantes (doctrina de la ficha)
BORDADO_COBERTURA = 0.995    # cobertura de los dominantes (resto = antialiasing)
BORDADO_CUBO = 16            # cuantización por canal para contar dominantes
BLANCO_INTERIOR_MAX = 8.0  # % del bbox: más que esto = fondo sin limpiar (FAIL)
BLANCO_ADJUDICAR = 2.0     # % del bbox: entre esto y el max = adjudicación visual
# (ASPECTO_MAX eliminado 2026-10-15: el aspecto no bloquea — corrección suya)
# --- bbox SEGURO y puertas de composición/fidelidad (2026-10-18) ---
COMP_AREA_MIN = 150   # px: un componente menor es ruido/speck, no diseño
COMP_DIM_MIN = 8      # px: min(ancho, alto) del componente — filtra los
                      # slivers de borde (p. ej. el speck 144x4 de p041,
                      # residuo de borde que NO es contenido cortado)
COMP_MARGEN_MIN_PX = 6     # margen seguro mínimo por lado en el crudo
COMP_MARGEN_MIN_PCT = 0.4  # % del lado (el tope efectivo es el mayor)
TOQUE_BORDE_MIN = 2   # px: margen seguro mínimo del FINAL por lado
FID_ASPECTO_MAX_PCT = 1.5  # desviación de aspecto crudo->final tolerada
FID_BANDA_MAX = 0.02  # fracción del contenido de la banda externa que
                      # puede faltar en el final (pares fieles = 0.0)
FID_GRID = 200        # rejilla de normalización para la banda
FID_BANDA_PCT = 3.0   # ancho de la banda externa, % del lado
# --- gate sin_counters_rellenos (2026-10-20, caso p046) ---
COUNTER_MEDIA_MIN = 200     # semilla: claro acromático (media>=200,
COUNTER_SPREAD_MAX = 18     # spread<=18) = fondo/damero, no diseño
COUNTER_AREA_MIN = 1500     # px: un relleno es mancha, no un brillo
COUNTER_DENSIDAD_MIN = 0.25  # área/bbox (buenos <=0.108; p046 0.42-0.68)
COUNTER_RADIO_MIN = 13      # grosor (radio inscrito máx): macizo en
                             # AMBAS dimensiones. Recalibración
                             # 2026-10-20 (barrido del registro): la
                             # densidad sola daba falsos positivos —
                             # líneas decorativas (p043, radio <=2.8) y
                             # brillos finos (p045/p062, <=12.8) con
                             # densidad 0.27-0.66. Rellenos p046:
                             # radio 14.0-99.5. Sin grosor suficiente
                             # el componente es SOSPECHOSO (se reporta
                             # en mediciones, no bloquea): zona gris
                             # medida donde conviven rellenos chicos
                             # reales (p052, radio 7.6-14.8) y diseño
                             # legítimo (brillo de ojo p054, 20.8).


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


def mascara_contenido(im):
    """Máscara booleana del contenido (numpy), para alfa o para opaco.

    - Con transparencia real (fracción de alfa<250 apreciable): alfa>=128.
    - Opaco (crudo de generación sobre fondo sólido): distancia RGB al
      color de fondo (mediana de las 4 esquinas) > 40. Sirve para fondos
      claros u oscuros; solo se usa para MEDIR márgenes/extensión."""
    import numpy as np
    arr = np.array(im)
    alfa = arr[..., 3]
    if float((alfa < 250).mean()) > 0.001:
        return alfa >= ALFA_CONTENIDO
    rgb = arr[..., :3].astype(float)
    h, w = rgb.shape[:2]
    p = min(24, h // 4, w // 4)
    esquinas = np.concatenate([
        rgb[:p, :p].reshape(-1, 3), rgb[:p, -p:].reshape(-1, 3),
        rgb[-p:, :p].reshape(-1, 3), rgb[-p:, -p:].reshape(-1, 3)])
    fondo = np.median(esquinas, axis=0)
    return np.sqrt(((rgb - fondo) ** 2).sum(axis=2)) > 40


def _stats_componentes(mask):
    """Stats (l, t, w, h, area) por componente conexo. cv2 -> scipy ->
    None (sin librería de componentes, el bbox seguro no es calculable
    y las puertas que lo necesitan lo declaran, no lo inventan)."""
    try:
        import cv2
        n, _lab, stats, _c = cv2.connectedComponentsWithStats(
            mask.astype("uint8"), 8)
        return [(int(stats[i, cv2.CC_STAT_LEFT]), int(stats[i, cv2.CC_STAT_TOP]),
                 int(stats[i, cv2.CC_STAT_WIDTH]), int(stats[i, cv2.CC_STAT_HEIGHT]),
                 int(stats[i, cv2.CC_STAT_AREA])) for i in range(1, n)]
    except ImportError:
        pass
    try:
        from scipy import ndimage
        lab, n = ndimage.label(mask)
        out = []
        for i, sl in enumerate(ndimage.find_objects(lab), start=1):
            if sl is None:
                continue
            hh = sl[0].stop - sl[0].start
            ww = sl[1].stop - sl[1].start
            out.append((int(sl[1].start), int(sl[0].start), int(ww), int(hh),
                        int((lab[sl] == i).sum())))
        return out
    except ImportError:
        return None


def bbox_seguro(im):
    """BBox del contenido REAL por componentes: unión de los componentes
    con área >= COMP_AREA_MIN y min(ancho, alto) >= COMP_DIM_MIN.

    A diferencia del bbox por masa (que recorta hasta acumular 0.05% y
    AMPUTA los extremos de baja masa: la punta de una guirnalda, una
    hoja fina, un icono pequeño), el bbox seguro conserva TODO
    componente real — es el bbox que el ojo ve. Devuelve (l, t, r, b)
    o None si no hay componentes que califiquen o no se pudo calcular."""
    mask = mascara_contenido(im)
    stats = _stats_componentes(mask)
    if not stats:
        return None
    kept = [s for s in stats
            if s[4] >= COMP_AREA_MIN and min(s[2], s[3]) >= COMP_DIM_MIN]
    if not kept:
        return None
    l = min(s[0] for s in kept)
    t = min(s[1] for s in kept)
    r = max(s[0] + s[2] for s in kept)
    b = max(s[1] + s[3] for s in kept)
    return (l, t, r, b)


def margenes_de_bbox(bbox, w, h):
    l, t, r, b = bbox
    return {"izq": l, "arr": t, "der": w - r, "aba": h - b}


def _normalizada(mask, bbox):
    """Máscara recortada a su bbox y reescalada a FID_GRID x FID_GRID
    (bool, umbral 0.35 tras interpolar): base de la pérdida por banda."""
    import numpy as np
    from PIL import Image as _Im
    l, t, r, b = bbox
    crop = (mask[t:b, l:r].astype("uint8") * 255)
    img = _Im.fromarray(crop, "L").resize((FID_GRID, FID_GRID), _Im.BILINEAR)
    return np.array(img) >= int(0.35 * 255)


def _dilatar3(m):
    """Dilatación 3x3 (tolerancia de 1 celda en la banda)."""
    import numpy as np
    p = np.pad(m, 1)
    out = np.zeros_like(m)
    for dy in range(3):
        for dx in range(3):
            out |= p[dy:dy + m.shape[0], dx:dx + m.shape[1]]
    return out


def perdida_por_banda(mask_o, bbox_o, mask_f, bbox_f):
    """Fracción del contenido del crudo en su banda externa sin
    contraparte en el final, por lado. Pares fieles miden 0.0."""
    A = _normalizada(mask_o, bbox_o)
    B = _dilatar3(_normalizada(mask_f, bbox_f))
    banda = max(1, int(round(FID_GRID * FID_BANDA_PCT / 100.0)))
    res = {}
    zonas = {"izq": A[:, :banda], "der": A[:, -banda:],
             "arr": A[:banda, :], "aba": A[-banda:, :]}
    zonas_b = {"izq": B[:, :banda], "der": B[:, -banda:],
               "arr": B[:banda, :], "aba": B[-banda:, :]}
    for lado, zona in zonas.items():
        tot = int(zona.sum())
        res[lado] = round(float((zona & ~zonas_b[lado]).sum()) / tot, 4) \
            if tot else 0.0
    return res


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


def colores_dominantes(im):
    """Colores dominantes del contenido (alfa>=128): reduce por
    vecino-más-cercano (la paleta se conserva exacta), cuantiza a
    cubos de BORDADO_CUBO por canal y devuelve cuántos colores
    hacen falta para cubrir BORDADO_COBERTURA del contenido."""
    from collections import Counter
    mini = im.copy()
    mini.thumbnail((700, 700), Image.NEAREST)
    conteo = Counter()
    total = 0
    for r, g, b, al in mini.getdata():
        if al >= 128:
            conteo[(r // BORDADO_CUBO, g // BORDADO_CUBO,
                    b // BORDADO_CUBO)] += 1
            total += 1
    if total == 0:
        return 0
    acumulado, n = 0, 0
    for _, c in conteo.most_common():
        acumulado += c
        n += 1
        if acumulado / total >= BORDADO_COBERTURA:
            break
    return n


def verificar(im, formato, a):
    gates, violado, med = {}, None, {}
    # G1: formato
    g1 = formato == "PNG" and "A" in im.getbands()
    gates["formato"] = {"pass": g1, "formato": formato}
    violado = violado or (None if g1 else "formato_invalido")
    # Modo --es-original: SOLO composición completa sobre el crudo.
    # El crudo es opaco o trae aire por diseño; las puertas de final
    # (fondo_limpio, recorte, dpi...) no aplican aquí.
    if getattr(a, "es_original", False):
        w0, h0 = im.size
        bs0 = bbox_seguro(im)
        if bs0 is None:
            gates["composicion_completa"] = {
                "pass": False, "motivo": "bbox_seguro_no_calculable"}
            violado = violado or "composicion_no_evaluable"
        else:
            marg0 = margenes_de_bbox(bs0, w0, h0)
            med["margenes_seguros_px"] = marg0
            med["margenes_seguros_pct"] = {
                k: round(100.0 * v / (w0 if k in ("izq", "der") else h0), 2)
                for k, v in marg0.items()}
            tope_x = max(COMP_MARGEN_MIN_PX, COMP_MARGEN_MIN_PCT / 100.0 * w0)
            tope_y = max(COMP_MARGEN_MIN_PX, COMP_MARGEN_MIN_PCT / 100.0 * h0)
            fallan = [k for k in ("izq", "der") if marg0[k] < tope_x] \
                + [k for k in ("arr", "aba") if marg0[k] < tope_y]
            g10 = not fallan
            gates["composicion_completa"] = {
                "pass": g10, "lados_que_tocan": fallan,
                "minimo_px": COMP_MARGEN_MIN_PX,
                "minimo_pct": COMP_MARGEN_MIN_PCT}
            violado = violado or (None if g10 else "composicion_toca_borde")
        return gates, violado, med
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
    # G13: sin counters rellenos (2026-10-20, caso p046): manchas
    # macizas de fondo acromático claro encerradas en huecos de
    # letras. Los gates de % global no las ven (0.0% blanco puro,
    # 0.69% interiores en p046); este mide COMPONENTES: semilla
    # acromática clara con área y densidad de mancha. Si falla,
    # correr scripts/limpiar-counters.py y re-verificar.
    if bbox is None:
        g13, med["counters_rellenos"] = False, []
        med["counters_sospechosos"] = []
    else:
        import numpy as _np2
        arr13 = _np.array(im)
        rgb13 = arr13[..., :3].astype(int)
        media13 = rgb13.mean(axis=2)
        spread13 = rgb13.max(axis=2) - rgb13.min(axis=2)
        semilla13 = (arr13[..., 3] > 128) & (media13 >= COUNTER_MEDIA_MIN) \
            & (spread13 <= COUNTER_SPREAD_MAX)
        rellenos13, sospechosos13 = [], []
        try:
            import cv2 as _cv2
            n13, lab13, stats13, _c13 = _cv2.connectedComponentsWithStats(
                semilla13.astype("uint8"), 8)
            comps13 = [(int(stats13[i, _cv2.CC_STAT_LEFT]),
                        int(stats13[i, _cv2.CC_STAT_TOP]),
                        int(stats13[i, _cv2.CC_STAT_WIDTH]),
                        int(stats13[i, _cv2.CC_STAT_HEIGHT]),
                        int(stats13[i, _cv2.CC_STAT_AREA]), i)
                       for i in range(1, n13)]
        except ImportError:
            lab13 = None
            comps13 = [(l, t, w, h, ar, None)
                       for (l, t, w, h, ar) in (_stats_componentes(semilla13)
                                                or [])]
        for (l13, t13, w13, h13, area13, id13) in comps13:
            dens13 = area13 / float(w13 * h13) if w13 and h13 else 0.0
            if area13 < COUNTER_AREA_MIN or dens13 < COUNTER_DENSIDAD_MIN:
                continue
            radio13 = None
            if lab13 is not None and id13 is not None:
                import cv2 as _cv2b
                import numpy as _np3
                local13 = (lab13[t13:t13 + h13, l13:l13 + w13] == id13)
                # Acolchar con 1px de ceros: un componente que llena
                # su bbox (línea rectangular) sin ceros alrededor
                # hace que distanceTransform devuelva FLT_MAX
                # (bug cazado por el fixture P6, 2026-10-20).
                radio13 = float(_cv2b.distanceTransform(
                    _np3.pad(local13.astype("uint8"), 1),
                    _cv2b.DIST_L2, 5).max())
            item13 = {"bbox": [l13, t13, w13, h13], "area_px": area13,
                      "densidad": round(dens13, 3),
                      "radio": round(radio13, 1) if radio13 is not None
                      else None}
            # Sin grosor medible o insuficiente -> sospechoso (no
            # bloquea): la zona gris la adjudica el ojo, declarado.
            if radio13 is not None and radio13 >= COUNTER_RADIO_MIN:
                rellenos13.append(item13)
            else:
                sospechosos13.append(item13)
        med["counters_rellenos"] = rellenos13
        med["counters_sospechosos"] = sospechosos13
        g13 = not rellenos13
    gates["sin_counters_rellenos"] = {
        "pass": g13, "area_min_px": COUNTER_AREA_MIN,
        "densidad_min": COUNTER_DENSIDAD_MIN,
        "radio_min_px": COUNTER_RADIO_MIN}
    violado = violado or (None if g13 else "counters_rellenos")
    # G11: contenido intacto — el bbox SEGURO del final no puede tocar
    # el borde del lienzo (flujo recorte-al-contenido + pad: tocar el
    # borde = algo fue rebanado). Calibración 2026-10-18: mutilados
    # 0px en los 4 lados (16/16); buenos conocidos >= 12px.
    bs = bbox_seguro(im)
    if bs is None:
        gates["contenido_intacto"] = {
            "pass": True, "motivo": "sin_componentes_calificados"}
        med["margenes_seguros_px"] = None
    else:
        marg_s = margenes_de_bbox(bs, w, h)
        med["margenes_seguros_px"] = marg_s
        tocan = [k for k, v in marg_s.items() if v < TOQUE_BORDE_MIN]
        g11 = not tocan
        gates["contenido_intacto"] = {"pass": g11, "lados_que_tocan": tocan,
                                       "minimo_px": TOQUE_BORDE_MIN}
        violado = violado or (None if g11 else "contenido_toca_borde")
    # G12: fidelidad de recorte contra el crudo (solo con --original):
    # aspecto del contenido + pérdida por banda externa. Si no se puede
    # verificar, NO pasa (fidelidad no demostrada != fidelidad).
    orig_path = getattr(a, "original", None)
    if orig_path:
        try:
            oim = Image.open(orig_path).convert("RGBA")
        except Exception:
            oim = None
        bso = bbox_seguro(oim) if oim is not None else None
        if oim is None or bs is None or bso is None:
            gates["fidelidad_recorte"] = {
                "pass": False, "motivo": "original_ilegible_o_sin_bbox_seguro"}
            violado = violado or "fidelidad_no_verificable"
        else:
            ao = (bso[2] - bso[0]) / max(1, (bso[3] - bso[1]))
            af = (bs[2] - bs[0]) / max(1, (bs[3] - bs[1]))
            desv = abs(ao - af) / ao * 100.0
            perd = perdida_por_banda(mascara_contenido(oim), bso,
                                     mascara_contenido(im), bs)
            med["fidelidad_desviacion_aspecto_pct"] = round(desv, 2)
            med["fidelidad_perdida_banda"] = perd
            g12 = desv <= FID_ASPECTO_MAX_PCT \
                and max(perd.values()) <= FID_BANDA_MAX
            gates["fidelidad_recorte"] = {
                "pass": g12, "aspecto_max_pct": FID_ASPECTO_MAX_PCT,
                "banda_max": FID_BANDA_MAX}
            violado = violado or (None if g12 else "fidelidad_recorte_perdida")
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
    # G14: fuente plana de bordado (SOLO con --metodo bordado): la
    # doctrina de la ficha (máx. 6 colores sólidos, sin degradados ni
    # textura) medida por colores dominantes del contenido.
    if getattr(a, "metodo", None) == "bordado":
        n_dom = colores_dominantes(im)
        med["bordado_colores_dominantes"] = n_dom
        g14 = n_dom <= BORDADO_COLORES_MAX
        gates["fuente_plana_bordado"] = {
            "pass": g14, "maximo_colores": BORDADO_COLORES_MAX,
            "cobertura": BORDADO_COBERTURA}
        violado = violado or (None if g14 else "fuente_bordado_no_plana")
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
    ap.add_argument("--es-original", action="store_true",
                    help="modo crudo: solo composición completa (el "
                         "contenido no puede tocar el borde del lienzo "
                         "de generación); correr ANTES de procesar")
    ap.add_argument("--original", default=None,
                    help="crudo de origen: activa fidelidad_recorte "
                         "(el final debe contener todo el contenido "
                         "del crudo: aspecto + banda externa)")
    ap.add_argument("--metodo", default=None, choices=["dtg", "bordado"],
                    help="método declarado del diseño (el de su entrada "
                         "en el registro): con 'bordado' activa la "
                         "puerta fuente_plana_bordado (máx. 6 colores "
                         "sólidos dominantes)")
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
    autotrim_bbox = None
    if a.autotrim:
        if not a.salida:
            ap.error("--autotrim requiere --salida")
        # Recorte al bbox SEGURO (componentes reales): el bbox por masa
        # amputaba extremos de baja masa (lote A, 2026-10-18). Si el
        # seguro no se puede calcular, se cae al de masa y se declara.
        bbox = bbox_seguro(im)
        autotrim_bbox = "seguro" if bbox else None
        if bbox is None:
            bbox = bbox_contenido(im)
            autotrim_bbox = "masa_fallback" if bbox else None
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
                      "reparado": reparado, "autotrim_bbox": autotrim_bbox,
                      "gate_humano_pendiente": "counters chicos/tenues o de tono calido (la puerta caza los rellenos grandes acromaticos); adjudicar cualquier relleno dudoso"},
                     ensure_ascii=False, indent=1))
    return 0 if veredicto == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
