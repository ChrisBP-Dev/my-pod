#!/usr/bin/env python3
"""verificar-investigacion.py — puerta mecánica del skill
investigacion-tienda (2026-10-27, recalibración de alineación).

Verifica la FORMA consumible de un reporte de investigación semanal,
sin juzgar su contenido: que exista, que declare sus fuentes de la
ficha, que traiga prioridades y que ninguna PROP-INV re-proponga
como nueva una línea que la ficha ya tiene vigente (ese fue el
hueco real del 2026-10-26: la personalización, ya decidida, volvió
como PROP-INV-2026-10-26-04 no aplicada).

Uso:
    python3 scripts/verificar-investigacion.py \
        --reporte data/tiendas/<id>/investigaciones/<fecha>-investigacion.md \
        --shop <id>

Sale 0 (PASS) o 1 (FAIL con causas). Lee la ficha física de la
tienda (el llamador corre `registros-datos.py pull` antes, camino
de lectura canónica).
"""
import argparse
import json
import pathlib
import re
import sys

APP = pathlib.Path(__file__).resolve().parent.parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reporte", required=True)
    ap.add_argument("--shop", required=True)
    ap.add_argument("--ficha", default=None,
                    help="ruta alternativa a la ficha (fixtures)")
    args = ap.parse_args()

    fallas = []
    reporte = pathlib.Path(args.reporte)
    if not reporte.is_absolute():
        reporte = APP / reporte
    if not reporte.exists():
        print(f"FAIL: el reporte no existe: {reporte}")
        return 1
    texto = reporte.read_text(encoding="utf-8")

    ficha_path = pathlib.Path(args.ficha) if args.ficha else \
        APP / "data" / "tiendas" / args.shop / "config.json"
    if args.ficha and not ficha_path.is_absolute():
        ficha_path = APP / ficha_path
    if not ficha_path.exists():
        print(f"FAIL: no existe la ficha de la tienda: {ficha_path}")
        return 1
    ficha = json.loads(ficha_path.read_text(encoding="utf-8"))
    lineas = (ficha.get("lineas_vigentes") or {})
    ids_lineas = [k for k, v in lineas.items()
                  if isinstance(v, dict) and v.get("estado") in
                  ("operativa", "operativo", "piloto")]

    # 1. Fuentes de ficha declaradas
    if "## Fuentes" not in texto:
        fallas.append("sin sección «## Fuentes» (la investigación "
                      "declara qué leyó de la ficha y del registro)")
    # 2. Prioridades presentes
    if not re.search(r"prioridades", texto, re.IGNORECASE):
        fallas.append("sin prioridades declaradas (top 5 o su "
                      "equivalente explícito)")
    # 3. Líneas vigentes citadas o ausencia declarada
    citadas = [i for i in ids_lineas if i in texto]
    if ids_lineas and not citadas and \
            "sin líneas aplicables" not in texto:
        fallas.append(
            f"la ficha tiene líneas vigentes {ids_lineas} y el "
            "reporte no cita ninguna ni declara «sin líneas "
            "aplicables»")
    # 4. Ninguna PROP-INV re-propone una línea ya vigente como nueva
    for m in re.finditer(r"PROP-[A-Z0-9\-]+[^\n]*", texto):
        linea = m.group(0)
        for lid in ids_lineas:
            terminos = {"personalizacion": ("personaliz",),
                        "bordado": ("bordad",)}.get(
                            lid, (lid.replace("_", " "),))
            if any(t in linea.lower() for t in terminos) and \
                    lid not in linea and "línea" not in linea.lower():
                fallas.append(
                    f"PROP re-propone la línea vigente «{lid}» sin "
                    f"citarla como línea de ficha: {linea.strip()}")

    if fallas:
        for f in fallas:
            print(f"FAIL: {f}")
        return 1
    print(f"PASS: reporte consumible (líneas citadas: "
          f"{citadas or 'ninguna — ausencia declarada'})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
