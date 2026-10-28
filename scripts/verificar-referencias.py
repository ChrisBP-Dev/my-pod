#!/usr/bin/env python3
"""verificar-referencias.py — integridad de referencias del sistema My POD.

Nace el 2026-10-27 (pedido del dueño): el cuerpo de la agenda de
propuestas referenciaba un script retirado (generar-datos-vitrina.py)
y NINGUNA puerta lo vio — `rameli validar` cubre el repo de la app,
pero los cuerpos de las agendas viven fuera del repo (sistema de
agendas) y los skills/docs se citan entre sí sin chequeo. Este
verificador escanea los textos que ORDENAN trabajo (cuerpos de
agendas de la app, SKILL.md de los skills y FLUJO-PIPELINE.md) y
comprueba que cada `scripts/<x>.py` y `skills/<s>/...` citado EXISTA
en el disco. Sale 1 (FAIL) nombrando cada referencia muerta.

Uso:
  python3 scripts/verificar-referencias.py [--agendas DIR]
        [--extra FILE...]
Por defecto escanea las agendas del goal POD (proyecciones en
workspace/goals/pod-etsy-sistema-operativo-q4-2026/crons), los
SKILL.md de la app y FLUJO-PIPELINE.md.
"""
import argparse
import os
import re
import sys

APP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOME = os.path.expanduser("~")
DEF_AGENDAS = os.path.join(
    HOME, "workspace/goals/pod-etsy-sistema-operativo-q4-2026/crons")

PAT_SCRIPT = re.compile(r"scripts/([A-Za-z0-9_.\-]+\.py)")
PAT_SKILLDIR = re.compile(r"skills/([A-Za-z0-9_.\-]+)/")


def existe_script(nombre):
    if os.path.exists(os.path.join(APP, "scripts", nombre)):
        return True
    skills = os.path.join(APP, "skills")
    if os.path.isdir(skills):
        for s in os.listdir(skills):
            if os.path.exists(os.path.join(skills, s, "scripts", nombre)):
                return True
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--agendas", default=DEF_AGENDAS)
    ap.add_argument("--extra", nargs="*", default=[])
    a = ap.parse_args()

    textos = []  # (ruta_legible, contenido)
    if os.path.isdir(a.agendas):
        for raiz, _, files in os.walk(a.agendas):
            for f in files:
                if f.endswith(".md"):
                    p = os.path.join(raiz, f)
                    textos.append((p, open(p, encoding="utf-8").read()))
    skills_dir = os.path.join(APP, "skills")
    for s in sorted(os.listdir(skills_dir)):
        p = os.path.join(skills_dir, s, "SKILL.md")
        if os.path.exists(p):
            textos.append((p, open(p, encoding="utf-8").read()))
    flujo = os.path.join(APP, "FLUJO-PIPELINE.md")
    if os.path.exists(flujo):
        textos.append((flujo, open(flujo, encoding="utf-8").read()))
    for p in a.extra:
        textos.append((p, open(p, encoding="utf-8").read()))

    muertas = []
    for ruta, txt in textos:
        corta = ruta.replace(HOME + "/", "~/")
        # Scripts: se ignoran las menciones históricas en líneas que
        # declaran el script retirado (no ordenan trabajo).
        vivos = "\n".join(
            ln for ln in txt.splitlines() if "retirad" not in ln.lower())
        for nombre in sorted(set(PAT_SCRIPT.findall(vivos))):
            if not existe_script(nombre):
                muertas.append(f"{corta}: scripts/{nombre} NO existe")
        # Skills: solo rutas de ESTA app — se saltan las precedidas
        # por "/" (ruta de otro repo, p. ej. ../rameli/skills/...) o
        # "(" (enumeración en prosa, p. ej. «(skills/docs/scripts)»).
        for m in PAT_SKILLDIR.finditer(txt):
            if m.start() > 0 and txt[m.start() - 1] in "/(":
                continue
            s = m.group(1)
            if not os.path.isdir(os.path.join(skills_dir, s)):
                muertas.append(f"{corta}: skills/{s}/ NO existe")

    # Invocación: el inventario de agendas del FLUJO declara qué
    # skill invoca cada agenda; el cuerpo guardado de cada agenda
    # recurrente debe NOMBRAR ese skill (invoca, no duplica: si el
    # cuerpo no lo nombra, el método vive en el cuerpo y derivará).
    # Las filas que declaran «sin skill propio» son la excepción
    # declarada y se saltan.
    fallos_inv = []
    flujo_txt = ""
    if os.path.exists(flujo):
        flujo_txt = open(flujo, encoding="utf-8").read()
    for m in re.finditer(r"\| `([a-z0-9\-]+)`[^|]*\|([^|]*)\|", flujo_txt):
        agenda, invoca = m.group(1), m.group(2)
        sm = re.search(r"skills/([A-Za-z0-9_.\-]+)", invoca)
        if not sm:
            continue
        skill = sm.group(1)
        cuerpos = []
        for raiz, _, files in os.walk(a.agendas):
            if "runonce" in raiz:
                continue
            for f in files:
                if f.startswith(agenda + "__") and f.endswith(".md"):
                    cuerpos.append(os.path.join(raiz, f))
        if not cuerpos:
            fallos_inv.append(f"agenda «{agenda}»: sin cuerpo guardado "
                              f"en {a.agendas}")
            continue
        if not any(skill in open(p, encoding="utf-8").read()
                   for p in cuerpos):
            fallos_inv.append(f"agenda «{agenda}»: su cuerpo no nombra "
                              f"el skill que invoca ({skill})")

    if muertas or fallos_inv:
        for m in muertas + fallos_inv:
            print(f"FAIL: {m}")
        return 1
    print(f"PASS: {len(textos)} textos con órdenes de trabajo, "
          f"sin referencias muertas a scripts ni skills, y toda "
          f"agenda recurrente nombra el skill que invoca")
    return 0


if __name__ == "__main__":
    sys.exit(main())
