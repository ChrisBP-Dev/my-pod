#!/usr/bin/env bash
# Suite de contrato de estratega-tienda (creada 2026-10-19, Propuesta 2
# de la auditoría de adopción docs/AUDITORIA-ADOPCION-V0110.md;
# DESACOPLADA DE LA INSTANCIA el 2026-10-23, Programa Estándar My POD
# F4: antes validaba el config-propuestas REAL de una tienda concreta
# y otra instancia no podía correrla; ahora corre contra FIXTURES
# NEUTROS propios en evals/fixtures/ — tienda ficticia, sin leer
# ningún dato real).
# La salida máquina de la estratega es config-propuestas.json de la
# tienda activa, cuyo contrato vive en docs/CONTRATO-TIPO-PRODUCTO.md.
# Esta suite valida FIXTURES contra ese contrato: campos
# obligatorios, tipo_lote válido, componentes presentes según el
# track, reparto y temas sumando N, y vigencia de 7 días exactos con
# formato de fecha. No juzga la estrategia (eso es la puerta humana
# del dueño); verifica que el artefacto sea consumible.
# Casos: fixture válida → el validador pasa; fixture inválida
# (temas no suman N) → el validador falla nombrando el criterio.
# Falla (exit != 0) si algún caso no da el veredicto esperado.
set -u
SKILL="$(cd "$(dirname "$0")/.." && pwd)"
FIX="$SKILL/evals/fixtures"
ok=0; fail=0

validar() { # validar <ruta> → stdout del validador; rc en $?
python3 - "$1" << 'EOF'
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
}

out="$(validar "$FIX/config-propuestas-ficticia-valida.json" 2>&1)"; rc=$?
if [[ $rc -eq 0 && "$out" == *"0 fallas"* ]]; then
  ok=$((ok+1))
else
  fail=$((fail+1)); echo "FALLA: fixture válida no pasó el contrato (rc=$rc)"; echo "$out" | tail -4
fi
out="$(validar "$FIX/config-propuestas-ficticia-invalida.json" 2>&1)"; rc=$?
if [[ $rc -ne 0 && "$out" == *"temas suman N"* ]]; then
  ok=$((ok+1))
else
  fail=$((fail+1)); echo "FALLA: fixture inválida no falló nombrando 'temas suman N' (rc=$rc)"; echo "$out" | tail -4
fi
# --- Consumo de líneas vigentes (v0.8.0, 2026-10-27) ---
# El helper de la app contra fixtures: línea de ficha con pausa
# declarada → PASS; la misma asignación en 0 sin nota → FAIL
# (el hueco real del 2026-10-26, calibrado también contra el
# config real previo a la recalibración).
APP="$(cd "$SKILL/../.." && pwd)"
HELPER="$APP/scripts/verificar-consumo-lineas-tienda.py"
if python3 "$HELPER" --shop ficticia --ficha "$FIX/ficha-ficticia-con-linea.json" --config-propuestas "$FIX/config-consumo-con-nota.json" >/dev/null 2>&1; then
  ok=$((ok+1))
else
  fail=$((fail+1)); echo "FALLA: consumo con pausa declarada debía pasar"
fi
if python3 "$HELPER" --shop ficticia --ficha "$FIX/ficha-ficticia-con-linea.json" --config-propuestas "$FIX/config-consumo-sin-nota.json" >/dev/null 2>&1; then
  fail=$((fail+1)); echo "FALLA: consumo con cupo 0 y sin nota debía fallar"
else
  ok=$((ok+1))
fi
echo "--- $ok ok, $fail fallas ---"
[[ $fail -eq 0 ]]
