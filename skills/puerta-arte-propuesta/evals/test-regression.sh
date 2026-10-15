#!/usr/bin/env bash
# Suite de regresión de puerta-arte-propuesta.
set -u
SKILL="$(cd "$(dirname "$0")/.." && pwd)"
V="$SKILL/scripts/verificar-arte.py"
K="$HOME/workspace/goals/pod-etsy-sistema-operativo-q4-2026/files/disenos/canonicos"
ok=0; fail=0

run() { # run <nombre> <veredicto-esperado> <criterio-esperado> <args...>
  local nombre="$1" esperado="$2" criterio="$3"; shift 3
  local out got crit
  out=$(python3 "$V" "$@" 2>/dev/null)
  got=$(echo "$out" | python3 -c "import json,sys; print(json.load(sys.stdin)['veredicto'])")
  crit=$(echo "$out" | python3 -c "import json,sys; print(json.load(sys.stdin)['criterio_violado'])")
  if [[ "$got" == "$esperado" && "$crit" == "$criterio" ]]; then ok=$((ok+1));
  else fail=$((fail+1)); echo "FALLA: $nombre esperaba $esperado/$criterio, dio '$got'/'$crit'"; fi
}

run "P1 print limpio 300dpi" PASS None --archivo "$K/vitals-stable-print-300dpi.png" --ancho-pulgadas 10.5
run "F1 fondo aplanado" FAIL fondo_no_transparente --archivo "$SKILL/evals/fixtures/arte-con-fondo.png" --ancho-pulgadas 10.5
run "F2 baja resolucion" FAIL dpi_insuficiente --archivo "$SKILL/evals/fixtures/arte-chico-margen.png" --ancho-pulgadas 10.5
run "F3 bordes vacios" FAIL recorte_con_bordes_vacios --archivo "$SKILL/evals/fixtures/arte-margen-amplio.png" --ancho-pulgadas 3.0
run "F4 blanco puro interior" FAIL blanco_puro_fondo_sin_limpiar --archivo "$SKILL/evals/fixtures/arte-blanco-puro-interior.png" --ancho-pulgadas 10

echo "--- $ok ok, $fail fallas ---"
[[ $fail -eq 0 ]]
