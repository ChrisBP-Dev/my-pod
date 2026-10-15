#!/usr/bin/env python3
"""Genera video de listing Etsy según el estándar del último listing aprobado.

NO inventa parámetros. Usa los del script que generó el video de referencia
(sleighin-12-hour-shift-video1-v4.mp4):
- scale=2160:2160, zoompan a 1080 (suave, no tiembla)
- Zoom OUT: 1.12 -> 1.0 (no zoom in)
- 3.5s por clip, 30fps
- Transición xfade fade 0.5s (no corte directo)

Uso:
    generar-video-listing.py --tipo onmodel --diseno p002 \\
        --imagenes img1.jpg img2.jpg img3.jpg --salida /tmp/video.mp4
"""
import argparse
import os
import subprocess
import tempfile

FPS = 30
DUR = 3.5
FRAMES = int(FPS * DUR)  # 105
SIZE = 1080
WORK = 2160
# Zoom IN 1.0 -> 1.25 con posición ABSOLUTA por frame (on), NO acumulativa.
# Por qué: zoompan trunca a píxeles enteros; con 'zoom+step' el error se acumula
# y se ve temblor. Con '1+0.25*on/105' cada frame calcula su posición exacta.
ZOOM_EXPR = f"1+0.25*on/{FRAMES}"


def build_segment(img_path, out_path):
    # NOTA 2026-10-15 (hallazgo verificado en producción): Etsy RECHAZA MP4 con
    # yuvj420p (rango completo) con un error genérico "having trouble uploading".
    # El script ya pasaba -pix_fmt yuv420p pero el filtro igual emitía yuvj420p.
    # La conversión explícita out_range=limited + format=yuv420p SÍ produce el
    # yuv420p de rango limitado que Etsy acepta (verificado: p004-video2).
    vf = (
        f"scale={WORK}:{WORK},"
        f"zoompan=z='{ZOOM_EXPR}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
        f"d={FRAMES}:s={SIZE}x{SIZE}:fps={FPS},"
        f"scale=out_range=limited,format=yuv420p"
    )
    return vf


def make_segment(img_path, out_path):
    vf = build_segment(img_path, out_path)
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-loop", "1", "-i", img_path,
        "-vf", vf,
        "-t", str(DUR),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium",
        out_path,
    ]
    subprocess.run(cmd, check=True, capture_output=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tipo", required=True, choices=["onmodel", "mockups"])
    ap.add_argument("--diseno", required=True)
    ap.add_argument("--imagenes", nargs=3, required=True)
    ap.add_argument("--salida", required=True)
    a = ap.parse_args()

    for p in a.imagenes:
        if not os.path.isfile(p):
            raise SystemExit(f"no existe: {p}")

    with tempfile.TemporaryDirectory() as tmp:
        clips = []
        for i, img in enumerate(a.imagenes):
            clip = os.path.join(tmp, f"clip-{i}.mp4")
            make_segment(img, clip)
            clips.append(clip)
        # xfade fade 0.5s entre clips
        # clip0 (3.5s) + clip1 con fade offset 3.0 -> v1 (6.5s)
        # v1 + clip2 con fade offset 6.0 -> final (9.5s)
        v1 = os.path.join(tmp, "v1.mp4")
        subprocess.run([
            "ffmpeg", "-y", "-loglevel", "error",
            "-i", clips[0], "-i", clips[1],
            "-filter_complex",
            "[0:v][1:v]xfade=transition=fade:duration=0.5:offset=3.0[v]",
            "-map", "[v]", "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-preset", "medium", v1,
        ], check=True, capture_output=True)
        out = a.salida
        os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
        subprocess.run([
            "ffmpeg", "-y", "-loglevel", "error",
            "-i", v1, "-i", clips[2],
            "-filter_complex",
            "[0:v][1:v]xfade=transition=fade:duration=0.5:offset=6.0[v]",
            "-map", "[v]", "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-preset", "medium", out,
        ], check=True, capture_output=True)

    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "format=duration,size", "-show_entries", "stream=width,height",
         "-of", "default=noprint_wrappers=1", out],
        capture_output=True, text=True, check=True,
    )
    print(f"video {a.tipo} {a.diseno}: {out}")
    print(r.stdout.strip())

    # Manifiesto: registra el método exacto usado para que la puerta
    # pueda verificar que se usó posición absoluta (no acumulativa).
    import json
    from datetime import datetime, timezone
    manifest = {
        "video": os.path.basename(out),
        "tipo": a.tipo,
        "diseno": a.diseno,
        "imagenes": [os.path.basename(p) for p in a.imagenes],
        "metodo_zoom": "posicion-absoluta",
        "zoom_expr": ZOOM_EXPR,
        "usa_on": "on" in ZOOM_EXPR,
        "usa_acumulativo": "zoom+" in ZOOM_EXPR or "zoom-" in ZOOM_EXPR,
        "work_res": WORK,
        "transicion": "xfade-fade-0.5s",
        "generado": datetime.now(timezone.utc).isoformat(),
        "script": "generar-video-listing.py",
    }
    mpath = os.path.splitext(out)[0] + ".manifest.json"
    with open(mpath, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"manifiesto: {mpath}")


if __name__ == "__main__":
    main()
