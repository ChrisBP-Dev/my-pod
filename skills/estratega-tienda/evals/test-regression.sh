#!/usr/bin/env bash
# Suite de contrato de estratega-tienda (creada 2026-10-19, Propuesta 2
# de la auditoría de adopción docs/AUDITORIA-ADOPCION-V0110.md).
# La salida máquina de la estratega es data/tiendas/29222324/config-propuestas.json,
# cuyo contrato vive en docs/CONTRATO-TIPO-PRODUCTO.md. Esta suite
# valida el config VIGENTE contra ese contrato: campos obligatorios,
# tipo_lote válido, componentes presentes según el track, reparto y
# temas sumando N, y vigencia de 7 días exactos con formato de fecha.
# No juzga la estrategia (eso es la puerta humana del dueño); verifica
# que el artefacto que consume el cron de propuestas sea consumible.
# Falla (exit != 0) si el config rompe el contrato.
set -u
SKILL="$(cd "$(dirname "$0")/.." && pwd)"
APP="$(cd "$SKILL/../.." && pwd)"

python3 - "$APP/data/tiendas/29222324/config-propuestas.json" << 'EOF'
import json, sys
from datetime import date
ok = fail = 0
def check(nombre, cond):
    global ok, fail
    if cond: ok += 1
    else: fail += 1; print(f"FALLA: {nombre}")
cfg = json.load(open(sys.argv[1]))
for campo in ["flujo_bifurcado", "tipo_lote", "n_propuestas_dia", "temas",
              "vigencia_desde", "vigencia_hasta", "version"]:
    check(f"campo obligatorio {campo}", campo in cfg)
check("flujo_bifurcado siempre true", cfg.get("flujo_bifurcado") is True)
check("tipo_lote válido", cfg.get("tipo_lote") in ("mpl", "single", "mixto"))
n = cfg.get("n_propuestas_dia", 0)
check("N positivo", isinstance(n, int) and n > 0)
if cfg.get("tipo_lote") in ("mpl", "mixto"):
    comps = (cfg.get("mpl") or {}).get("componentes") or []
    check("mpl.componentes no vacío", len(comps) >= 1)
if cfg.get("tipo_lote") == "mixto":
    rep = (cfg.get("mixto") or {}).get("reparto") or {}
    check("mixto.reparto suma N", sum(rep.values()) == n)
temas = cfg.get("temas") or []
check("temas suman N", sum(t.get("n", 0) for t in temas) == n)
try:
    d1 = date.fromisoformat(cfg["vigencia_desde"]); d2 = date.fromisoformat(cfg["vigencia_hasta"])
    check("vigencia de 7 días exactos (hasta - desde = 7)", (d2 - d1).days == 7)
except Exception:
    check("vigencia con fechas ISO válidas", False)
print(f"--- {ok} ok, {fail} fallas ---")
sys.exit(0 if fail == 0 else 1)
EOF
