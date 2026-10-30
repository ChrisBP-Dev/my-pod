#!/usr/bin/env python3
"""verificar-estado-entrega.py — puerta de FORMA del estado tras una entrega.

Nace el 2026-10-28 del incidente «vitrina en cero»: la corrida de
prueba entregó el lote p072–p081 escribiendo `lote_actual` SIN la
clave `entregados`, y la vitrina — que deriva su universo de esa
clave — leyó cero con el lote íntegro en el repo. Ninguna puerta
lo notó porque nadie verificaba la FORMA del estado que la
entrega deja escrito.

La puerta comprueba, para la tienda dada:
  1. Si `lote_actual.disenos` trae slugs, `lote_actual.entregados`
     existe y nombra exactamente ese lote (ni vacío ni parcial).
  2. Cada slug entregado del lote existe en el registro con
     bloque `vitrina` completo (arte_ref + previas declaradas).
Sale 1 (FAIL) nombrando cada desviación: la entrega NO cierra
con la puerta en FAIL.

Uso: python3 scripts/verificar-estado-entrega.py --shop <id>
"""
import argparse
import json
import os
import sys

APP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shop", required=True)
    ap.add_argument("--estado", default=None,
                    help="ruta alternativa al estado (para calibración)")
    ap.add_argument("--registro", default=None,
                    help="ruta alternativa al registro (para calibración)")
    a = ap.parse_args()

    base = os.path.join(APP, "data", "tiendas", a.shop)
    estado_p = a.estado or os.path.join(base, "estado-propuestas.json")
    registro_p = a.registro or os.path.join(base, "registro-listings.json")
    estado = json.load(open(estado_p, encoding="utf-8"))
    registro = json.load(open(registro_p, encoding="utf-8"))

    fallos = []
    la = estado.get("lote_actual") or {}
    disenos = la.get("disenos") or []
    entregados = la.get("entregados")
    if disenos:
        if not entregados:
            fallos.append(
                f"lote_actual trae {len(disenos)} diseños pero "
                f"`entregados` está ausente o vacío — la vitrina "
                f"derivaría cero (incidente 2026-10-28)")
        elif set(entregados) != set(disenos):
            fallos.append(
                f"`entregados` no nombra exactamente el lote: "
                f"faltan {sorted(set(disenos) - set(entregados))}, "
                f"sobran {sorted(set(entregados) - set(disenos))}")
    for slug in (entregados or []):
        e = registro.get(slug)
        if e is None:
            fallos.append(f"{slug}: entregado sin entrada en el registro")
            continue
        v = e.get("vitrina") or {}
        for campo in ("arte_ref", "previa_oscura", "previa_clara"):
            if not v.get(campo):
                fallos.append(f"{slug}: bloque vitrina sin `{campo}`")

    if fallos:
        for f in fallos:
            print(f"FAIL: {f}")
        return 1
    print(f"PASS: forma del estado íntegra (lote actual: "
          f"{len(disenos)} diseños, entregados canónicos, previas "
          f"declaradas)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
