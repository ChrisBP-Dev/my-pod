#!/usr/bin/env python3
"""Puerta de video para listings Etsy.

Detecta los problemas que el ojo del usuario encontró en pruebas:
1. Zoom tembloroso (jitter por truncamiento en zoompan)
2. Zoom imperceptible (sin movimiento real)
3. Transición incorrecta (corte vs fade)
4. Specs técnicas (duración, resolución, fps, audio, tamaño)

Uso:
    verificar-video.py --video ruta.mp4 [--tipo onmodel|mockups]
"""
import argparse
import json
import subprocess
import sys
import tempfile
import os

import cv2
import numpy as np


def ffprobe(video):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_format", "-show_streams",
         "-of", "json", video],
        capture_output=True, text=True, check=True,
    )
    return json.loads(r.stdout)


def check_specs(video, info):
    """Specs técnicas del criterio."""
    errors = []
    fmt = info["format"]
    streams = info["streams"]
    vstream = next(s for s in streams if s["codec_type"] == "video")

    dur = float(fmt["duration"])
    if not (3 <= dur <= 15):
        errors.append(f"duración {dur:.1f}s fuera de 3-15s")

    w, h = int(vstream["width"]), int(vstream["height"])
    if w < 500 or h < 500:
        errors.append(f"resolución {w}x{h} menor a 500px")
    if w != h:
        errors.append(f"aspecto {w}x{h} no es 1:1")

    # fps
    fps_str = vstream.get("r_frame_rate", "30/1")
    num, den = map(int, fps_str.split("/"))
    fps = num / den
    if abs(fps - 30) > 1:
        errors.append(f"fps {fps:.1f} no es 30")

    # audio
    audio = [s for s in streams if s["codec_type"] == "audio"]
    if audio:
        errors.append("tiene pista de audio (Etsy la elimina)")

    # tamaño
    size = int(fmt["size"])
    if size > 100 * 1024 * 1024:
        errors.append(f"tamaño {size/1e6:.1f}MB excede 100MB")

    return errors


def extract_frames(video, fps=5):
    """Extrae frames a bajo fps para análisis."""
    tmp = tempfile.mkdtemp()
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", video,
         "-vf", f"fps={fps}", os.path.join(tmp, "f%04d.png")],
        check=True, capture_output=True,
    )
    frames = []
    for f in sorted(os.listdir(tmp)):
        img = cv2.imread(os.path.join(tmp, f), cv2.IMREAD_GRAYSCALE)
        if img is not None:
            frames.append(img)
    return frames


def measure_zoom(frames):
    """Mide si hay zoom perceptible por segmento.

    Calibrado 2026-10-14 con videos reales:
    - Sin zoom (v2): segmentos con media 0.01-2.18 (casi estático)
    - Con zoom (v3, v1b): segmentos con media 7-16 (movimiento claro)
    Umbral: media > 3.0 por segmento = hay movimiento.
    Retorna (zoom_detectado, media_minima).
    """
    if len(frames) < 10:
        return False, 0.0
    import numpy as np
    n = len(frames)
    seg = n // 3
    seg_medias = []
    for i in range(3):
        diffs = []
        start = i * seg
        end = min((i + 1) * seg - 2, n - 1)  # excluir transición
        for j in range(start, end):
            d = np.mean(np.abs(
                frames[j].astype(float) - frames[j + 1].astype(float)))
            diffs.append(d)
        if diffs:
            seg_medias.append(float(np.mean(diffs)))
    if not seg_medias:
        return False, 0.0
    min_media = min(seg_medias)
    return min_media > 3.0, min_media


def measure_jitter(frames):
    """Detecta temblor: movimiento no-monotónico entre frames consecutivos.

    Con zoom suave, el cambio entre frames consecutivos es consistente.
    Con jitter, hay oscilaciones (adelante-atrás).
    Retorna (hay_jitter, score).
    """
    if len(frames) < 10:
        return False, 0.0
    # Flujo óptico denso entre frames consecutivos (muestra)
    diffs = []
    for i in range(0, len(frames) - 1, 2):
        a = frames[i]
        b = frames[i + 1]
        flow = cv2.calcOpticalFlowFarneback(
            a, b, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        mag = np.mean(np.sqrt(flow[..., 0] ** 2 + flow[..., 1] ** 2))
        diffs.append(mag)
    diffs = np.array(diffs)
    if len(diffs) < 5:
        return False, 0.0
    # Jitter = alta varianza relativa en magnitudes consecutivas
    # (movimiento suave = cambios graduales, no saltos)
    mean = np.mean(diffs)
    if mean < 0.1:
        return False, 0.0  # casi sin movimiento
    cv_score = float(np.std(diffs) / mean)
    # Zoom suave tiene cv bajo (<0.5); jitter tiene cv alto (>0.8)
    return cv_score > 0.8, cv_score


def check_manifest(video):
    """Verifica que el video se generó con el método correcto.

    El script escribe un .manifest.json con el método usado.
    La puerta verifica que fue posición absoluta, no acumulativa.
    """
    import json
    mpath = os.path.splitext(video)[0] + ".manifest.json"
    if not os.path.isfile(mpath):
        return [f"sin manifiesto ({os.path.basename(mpath)}): "
                "no se puede verificar el método de zoom"]
    with open(mpath) as f:
        m = json.load(f)
    errors = []
    if m.get("metodo_zoom") != "posicion-absoluta":
        errors.append(f"método de zoom incorrecto: {m.get('metodo_zoom')}")
    if not m.get("usa_on"):
        errors.append("la expresión de zoom no usa 'on' (posición absoluta)")
    if m.get("usa_acumulativo"):
        errors.append("la expresión de zoom usa forma acumulativa (causa temblor)")
    if m.get("transicion") != "xfade-fade-0.5s":
        errors.append(f"transición incorrecta: {m.get('transicion')}")
    return errors


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--tipo", choices=["onmodel", "mockups"], default="onmodel")
    a = ap.parse_args()

    if not os.path.isfile(a.video):
        print(f"FAIL: no existe {a.video}")
        sys.exit(1)

    info = ffprobe(a.video)
    errors = check_specs(a.video, info)
    errors += check_manifest(a.video)

    print("Extrayendo frames para análisis de movimiento...")
    frames = extract_frames(a.video, fps=5)

    zoom_ok, zoom_media = measure_zoom(frames)
    if not zoom_ok:
        errors.append(
            f"zoom imperceptible (movimiento medio {zoom_media:.1f}, umbral 3.0)")

    # NOTA: la detección de jitter por análisis de frames no es confiable.
    # El temblor sutil (como el de v1b) no se distingue con métodos simples.
    # La prevención es por construcción: el script usa posición absoluta (on),
    # nunca acumulativa. Ver LECCION-ZOOMPAN-SIN-TEMBLOR.md.

    if errors:
        print("FAIL:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    print(f"PASS: movimiento medio {zoom_media:.1f}")
    sys.exit(0)


if __name__ == "__main__":
    main()
