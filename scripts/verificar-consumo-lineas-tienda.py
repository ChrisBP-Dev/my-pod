#!/usr/bin/env python3
"""verificar-consumo-lineas-tienda.py — chequeo de consumo de las
líneas vigentes de una tienda (2026-10-27, recalibración de
alineación a Rameli).

La ficha declara líneas vigentes (config.json → lineas_vigentes);
el config-propuestas semanal ASIGNA contra ellas. Este helper
verifica, sin juicio, que ninguna línea abierta se pierda en el
paso ficha → asignación semanal (el hueco real: la personalización
estaba decidida desde el 2026-10-20 y el config vigente declaraba
cupo 0 sin que ninguna puerta lo cruzara contra una declaración
de la ficha).

Reglas por línea de la ficha:
- tipo "foco" con estado operativa|piloto: el config-propuestas
  debe traer su bloque de asignación con cupo > 0, O un
  `asignacion_nota` no vacío que declare la pausa y su motivo.
  Sin bloque, o cupo 0 sin nota = FALLO.
- tipo "metodo" con estado operativo: su `doctrina_ref` debe
  existir como texto en la ficha misma (la doctrina vive
  declarada) — sin cupo que asignar. Solo se reporta.

Uso: python3 scripts/verificar-consumo-lineas-tienda.py --shop <id>
     [--config-propuestas <ruta>] [--ficha <ruta>]  (fixtures)
Sale 0 (PASS) o 1 (FAIL con causas nombradas).
"""
import argparse
import json
import pathlib
import sys

APP = pathlib.Path(__file__).resolve().parent.parent

# Bloque de asignación semanal por línea (contrato de la app).
BLOQUES = {"personalizacion": "personalizados"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shop", required=True)
    ap.add_argument("--ficha", default=None)
    ap.add_argument("--config-propuestas", default=None)
    args = ap.parse_args()

    base = APP / "data" / "tiendas" / args.shop
    ficha_path = pathlib.Path(args.ficha) if args.ficha else base / "config.json"
    cp_path = pathlib.Path(args.config_propuestas) if args.config_propuestas \
        else base / "config-propuestas.json"
    for p, nombre in [(ficha_path, "ficha"), (cp_path, "config-propuestas")]:
        if not p.exists():
            print(f"FAIL: no existe {nombre}: {p}")
            return 1
    ficha = json.loads(ficha_path.read_text(encoding="utf-8"))
    config = json.loads(cp_path.read_text(encoding="utf-8"))
    lineas = ficha.get("lineas_vigentes") or {}
    if not lineas:
        print("FAIL: la ficha no declara lineas_vigentes (ninguna "
              "línea abierta — si es correcto, se declara el bloque "
              "vacío con su nota)")
        return 1

    fallas, avisos = [], []
    for lid, linea in lineas.items():
        if not isinstance(linea, dict):
            continue
        tipo, estado = linea.get("tipo"), linea.get("estado")
        if tipo == "foco" and estado in ("operativa", "piloto"):
            bloque_nombre = BLOQUES.get(lid, lid)
            bloque = config.get(bloque_nombre)
            if not isinstance(bloque, dict):
                fallas.append(
                    f"línea «{lid}» ({estado}) sin bloque de "
                    f"asignación «{bloque_nombre}» en el "
                    "config-propuestas: la línea no llegó a la "
                    "asignación semanal")
                continue
            cupo = bloque.get("cupo_en_flujo_diario")
            nota = (bloque.get("asignacion_nota") or "").strip()
            if (cupo or 0) > 0:
                avisos.append(f"línea «{lid}»: asignación {cupo}/día")
            elif nota:
                avisos.append(
                    f"línea «{lid}»: asignación 0 con pausa "
                    "declarada (asignacion_nota)")
            else:
                fallas.append(
                    f"línea «{lid}» ({estado}) con cupo 0 y SIN "
                    "asignacion_nota: asignación ausente en "
                    "silencio — o se asigna, o se declara la "
                    "pausa con su motivo y su dale")
        elif tipo == "metodo" and estado in ("operativo", "operativa"):
            if not linea.get("doctrina_ref"):
                fallas.append(
                    f"método «{lid}» operativo sin doctrina_ref "
                    "declarada en la ficha")
            else:
                avisos.append(f"método «{lid}»: doctrina declarada")

    for a in avisos:
        print(f"OK: {a}")
    if fallas:
        for f in fallas:
            print(f"FAIL: {f}")
        return 1
    print("PASS: toda línea vigente de la ficha llegó a la "
          "asignación semanal o declaró su pausa")
    return 0


if __name__ == "__main__":
    sys.exit(main())
