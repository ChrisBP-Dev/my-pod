#!/usr/bin/env python3
"""Limpieza de counters rellenos (fondo atrapado dentro de letras).

Caso origen: p046 "ICU: I Care U" (cazado por el dueño en Printify,
2026-10-20). El PNG nació "transparente" y pasaba TODAS las puertas,
pero los huecos cerrados de las letras de "Care" (C, a, r, e) traían
el fondo crema-blanco HORNEADO como píxeles opacos: el quitado de
fondo original limpió el exterior y el blanco puro, pero el fondo
encerrado no es blanco puro (media ~249/245/237) ni toca el borde,
así que ningún gate lo veía — sin_blanco_puro medía 0.0% y
sin_blancos_interiores 0.69% (los rellenos son chicos contra el
bbox completo del diseño).

Detector calibrado (2026-10-20, contra artes buenos y el malo):
- Semilla: píxel opaco (alfa>128) claro acromático (media>=200,
  spread<=18) — el canon de color de la app: los claros DE DISEÑO
  son crema cálido (spread>18); lo acromático claro es fondo o
  damero, nunca diseño (misma base que la limpieza del damero,
  SKILL.md regla 2026-10-17).
- Un componente de semilla es RELLENO si área >= 1500px Y densidad
  (área / bbox) >= 0.25: es una mancha maciza encerrada, no un
  brillo de trazo ni un sliver de borde.
- Calibración: conocidos-buenos (vitals canónico, p036 v3, p037 v2,
  p028 y p033 publicados) — ningún componente >=1500px supera
  densidad 0.108. p046 malo: sus 4 rellenos miden área 2245-51632 y
  densidad 0.42-0.68. La puerta (gate sin_counters_rellenos en
  verificar-arte.py) usa este mismo detector.
- Cobertura honesta: rellenos chicos (<1500px), tenues o de tono
  cálido NO los caza este detector — siguen en el gate humano.

Limpieza (determinista, solo toca los rellenos detectados):
1. Crece cada relleno sobre píxeles candidatos contiguos (alfa>0,
   media>=150, spread<=55): la franja de transición hacia el
   contorno oscuro. El contorno (oscuro y saturado) no es candidato
   y actúa de pared: el crecimiento no cruza a los rellenos crema
   del trazo, que viven tras el contorno.
2. Residuo: cualquier componente opaco remanente cuyo bbox quede
   ENTERO dentro del bbox de un relleno expandido 6px y con área
   < 1500px (manchas de la textura del fondo que el crecimiento no
   alcanzó) se elimina también y se reporta.
3. Reporta por relleno: bbox, px de semilla y px totales quitados.
   El resto de la imagen queda byte-idéntico (verificable por diff).

Uso: limpiar-counters.py --archivo ARTE.png --salida ARTE-v2.png
Sin --salida NO escribe (solo reporta los rellenos detectados).
"""
import argparse
import json

import numpy as np
from PIL import Image

SEED_MEDIA_MIN = 200
SEED_SPREAD_MAX = 18
RELLENO_AREA_MIN = 1500
RELLENO_DENSIDAD_MIN = 0.25
CRECE_MEDIA_MIN = 150
CRECE_SPREAD_MAX = 55
RESIDUO_PAD = 6


def _componentes(mask):
    """[(l, t, w, h, area, mascara_local)] por componente conexo."""
    import cv2
    n, lab, stats, _c = cv2.connectedComponentsWithStats(
        mask.astype("uint8"), 8)
    out = []
    for i in range(1, n):
        l, t, w, h, area = (int(stats[i, j]) for j in range(5))
        out.append({"id": i, "l": l, "t": t, "w": w, "h": h,
                    "area": area, "lab": lab})
    return out, lab


def detectar_rellenos(a):
    """Rellenos según el detector calibrado, sobre el array RGBA."""
    rgb = a[..., :3].astype(int)
    media = rgb.mean(axis=2)
    spread = rgb.max(axis=2) - rgb.min(axis=2)
    semilla = (a[..., 3] > 128) & (media >= SEED_MEDIA_MIN) \
        & (spread <= SEED_SPREAD_MAX)
    comps, lab = _componentes(semilla)
    rellenos = []
    for c in comps:
        densidad = c["area"] / float(c["w"] * c["h"])
        if c["area"] >= RELLENO_AREA_MIN and densidad >= RELLENO_DENSIDAD_MIN:
            rellenos.append({**c, "densidad": round(densidad, 3),
                             "mascara": lab == c["id"]})
    return rellenos, semilla


def limpiar(path_in, path_out):
    im = Image.open(path_in).convert("RGBA")
    a = np.array(im)
    rellenos, _ = detectar_rellenos(a)
    if not rellenos:
        return {"rellenos": [], "eliminados_px": 0}
    rgb = a[..., :3].astype(int)
    media = rgb.mean(axis=2)
    spread = rgb.max(axis=2) - rgb.min(axis=2)
    candidato = (a[..., 3] > 0) & (media >= CRECE_MEDIA_MIN) \
        & (spread <= CRECE_SPREAD_MAX)
    comps_c, lab_c = _componentes(candidato)
    quitar = np.zeros(a.shape[:2], dtype=bool)
    zonas = []
    for r in rellenos:
        ids = set(np.unique(lab_c[r["mascara"]])) - {0}
        crecida = np.isin(lab_c, list(ids)) if ids else r["mascara"]
        quitar |= crecida
        zonas.append({"bbox": [r["l"], r["t"], r["w"], r["h"]],
                      "semilla_px": r["area"],
                      "densidad": r["densidad"],
                      "quitado_px": int(crecida.sum())})
    # Residuo: componentes opacos chicos enteramente dentro de la
    # zona de un relleno (manchas de textura del fondo).
    resto = (a[..., 3] > 128) & ~quitar
    comps_r, lab_r = _componentes(resto)
    n_residuo = 0
    for c in comps_r:
        if c["area"] >= RELLENO_AREA_MIN:
            continue
        for z in zonas:
            l, t, w, h = z["bbox"]
            if (c["l"] >= l - RESIDUO_PAD and c["t"] >= t - RESIDUO_PAD
                    and c["l"] + c["w"] <= l + w + RESIDUO_PAD
                    and c["t"] + c["h"] <= t + h + RESIDUO_PAD):
                quitar |= lab_r == c["id"]
                n_residuo += c["area"]
                break
    total = int(quitar.sum())
    a[quitar, 3] = 0
    if path_out:
        Image.fromarray(a).save(path_out)
    for z in zonas:
        z["quitado_px"] += 0  # el residuo se reporta agregado, no por zona
    return {"rellenos": zonas, "residuo_px": n_residuo,
            "eliminados_px": total}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--archivo", required=True)
    ap.add_argument("--salida", default=None,
                    help="sin --salida solo reporta (no escribe)")
    args = ap.parse_args()
    res = limpiar(args.archivo, args.salida)
    res["escribio"] = bool(args.salida)
    print(json.dumps(res, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
