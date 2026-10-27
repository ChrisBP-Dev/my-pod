#!/usr/bin/env bash
# Suite de regresión de investigacion-tienda (v1.0.0, 2026-10-27).
# Calibración en ambos sentidos contra fixtures neutros:
# el reporte bien formado pasa; el que re-propone una línea
# vigente (el hueco real del 2026-10-26) y el que no declara
# fuentes/líneas deben FALLAR.
set -u
SKILL="$(cd "$(dirname "$0")/.." && pwd)"
APP="$(cd "$SKILL/../.." && pwd)"
V="$APP/scripts/verificar-investigacion.py"
F="$SKILL/evals/fixtures"
FICHA="$F/ficha-ficticia.json"
ok=0; fail=0
run() { # run <nombre> <esperado PASS|FAIL> <reporte>
  python3 "$V" --reporte "$3" --shop ficticia --ficha "$FICHA" >/dev/null 2>&1
  local rc=$? got="FAIL"; [[ $rc -eq 0 ]] && got="PASS"
  if [[ "$got" == "$2" ]]; then ok=$((ok+1));
  else fail=$((fail+1)); echo "FALLA: $1 esperaba $2, dio $got"; fi
}
run "reporte bueno" PASS "$F/reporte-bueno.md"
run "re-propone línea vigente" FAIL "$F/reporte-malo-repropone.md"
run "sin fuentes ni líneas" FAIL "$F/reporte-malo-sin-fuentes.md"
# El cuerpo del skill declara entradas, salida y puerta (intake de la fábrica)
for s in "## Entradas" "## Salida" "## Puertas mecánicas" "lineas_vigentes"; do
  if grep -q "$s" "$SKILL/SKILL.md"; then ok=$((ok+1)); else fail=$((fail+1)); echo "FALLA: SKILL.md no declara «$s»"; fi
done
echo "--- $ok ok, $fail fallas ---"
[[ $fail -eq 0 ]]
