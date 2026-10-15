#!/usr/bin/env python3
"""Puerta: verifica que un diseño está listo para publicar (flujo Printify-first).

Revisa que todos los assets existan y pasen sus puertas:
- Arte print (300 DPI, puerta-arte-propuesta)
- Videos generados desde mockups de Printify (pasan verificar-video.py)
- Paquete comercial (pasa verificar-paquete.py)

Los mockups NO se verifican como archivos locales: salen de Printify.
Se verifica en el navegador al momento de publicar (checklist en SKILL.md).

Uso:
    verificar-listos-publicar.py --diseno p002
"""
import argparse
import glob
import os
import subprocess
import sys

BASE = os.path.expanduser("~/workspace/my-pod")


def check_arte(diseno):
    errors = []
    p = f"{BASE}/data/artes-print/{diseno}-print-300dpi.png"
    if not os.path.isfile(p):
        errors.append(f"falta arte: {p}")
    return errors


def check_videos(diseno):
    errors = []
    vids = glob.glob(f"{os.path.expanduser('~')}/workspace/your_files/{diseno}-video*-printify-*.mp4")
    if len(vids) < 2:
        errors.append(f"se requieren 2 videos Printify-first para {diseno} (hay {len(vids)})")
    for v in vids:
        r = subprocess.run(
            ["python3", f"{BASE}/scripts/verificar-video.py", "--video", v],
            capture_output=True, text=True,
        )
        if r.returncode != 0:
            errors.append(f"video {v} no pasa la puerta:\n{r.stdout}")
    return errors


def check_paquete(diseno):
    errors = []
    p = f"{BASE}/data/paquetes-listing/{diseno}-paquete.md"
    if not os.path.isfile(p):
        errors.append(f"falta paquete: {p}")
        return errors
    r = subprocess.run(
        ["python3", f"{BASE}/skills/paquete-listing-etsy/scripts/verificar-paquete.py",
         "--paquete", p],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        errors.append(f"paquete {diseno} no pasa la puerta:\n{r.stdout}")
    return errors


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--diseno", required=True)
    a = ap.parse_args()

    errors = []
    errors += check_arte(a.diseno)
    errors += check_videos(a.diseno)
    errors += check_paquete(a.diseno)

    if errors:
        print(f"FAIL: {a.diseno} no está listo:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    print(f"PASS: {a.diseno} listo para publicar")
    sys.exit(0)


if __name__ == "__main__":
    main()
