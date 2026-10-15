#!/bin/bash
# test-regression.sh — puerta-publicacion-pod v0.2.0
# G1: 12 del golden set (modo golden) -> PASS
# G2: arte final -> DPI PASS
# F1/F2/F3: negativos -> FAIL con criterio nombrado
# R1: --referencia (flat-lay propio como referencia) -> PASS
# R2: --referencia + desplazado -> FAIL placement
set -u
SKILL="$(cd "$(dirname "$0")/.." && pwd)"
V="$SKILL/scripts/verificar-publicacion.py"
KIT="$HOME/workspace/goals/pod-etsy-sistema-operativo-q4-2026/files/disenos/mockups/vitals-stable-kit"
FIX="$SKILL/evals/fixtures"
ARTE="$HOME/workspace/goals/pod-etsy-sistema-operativo-q4-2026/files/disenos/canonicos/vitals-stable-final.png"
CANON="$HOME/workspace/goals/pod-etsy-sistema-operativo-q4-2026/files/disenos/canonicos"
pass=0; fail=0

run() { # $1=nombre $2=esperado(PASS|FAIL) resto=args
  local nombre="$1" esperado="$2"; shift 2
  local out rc v
  out=$(python3 "$V" "$@" 2>/dev/null); rc=$?
  v=$(echo "$out" | python3 -c "import json,sys; print(json.load(sys.stdin)['veredicto'])" 2>/dev/null)
  if [ "$v" = "$esperado" ]; then pass=$((pass+1)); # echo "ok: $nombre -> $v"
    :
  else fail=$((fail+1)); echo "FALLA: $nombre esperaba $esperado, dio '$v' (rc=$rc)"; fi
}

# G1: los 12 del golden set (modo golden heredado)
declare -A ESTILOS=( [flatlay]="flatlay-prop2" [doblada]="doblada-prop2" [closecrop]="closecrop-prop2" )
for e in flatlay doblada closecrop; do
  for c in white sand sportgrey; do
    f=$(ls "$KIT/${ESTILOS[$e]}-${c}-v1-2000.jpg" "$KIT/${ESTILOS[$e]}-${c}-v2-2000.jpg" 2>/dev/null | head -1)
    run "G1 $e/$c" PASS mockup --candidato "$f" --estilo "$e" --color "$c"
  done
done
for c in white sand sportgrey; do
  f=$(ls "$KIT"/onmodel-*-prop2-${c}-canon*-2000.jpg 2>/dev/null | head -1)
    run "G1 onmodel/$c" PASS mockup --candidato "$f" --estilo onmodel --color "$c"
done

# G2: DPI del arte (archivo de impresión 3168 px, no el RGBA de trabajo)
run "G2 dpi" PASS arte --archivo "$CANON/vitals-stable-print-300dpi.png" --ancho-pulgadas 10.5

# F1/F2/F3 negativos (modo golden)
run "F1 dimensiones" FAIL mockup --candidato "$FIX/flatlay-v7-historico.webp" --estilo flatlay --color white
run "F2 desplazado" FAIL mockup --candidato "$FIX/desplazado-dx120.jpg" --estilo flatlay --color white
run "F3 encogido" FAIL mockup --candidato "$FIX/encogido-85.jpg" --estilo flatlay --color white

# R1/R2: modo --referencia (criterio v2: flat-lay propio del diseño)
REF="$KIT/flatlay-prop2-white-v1-2000.jpg"
run "R1 referencia propia" PASS mockup --candidato "$REF" --referencia "$REF" --arte "$ARTE"
run "R2 referencia+desplazado" FAIL mockup --candidato "$FIX/desplazado-dx120.jpg" --referencia "$REF" --arte "$ARTE"

echo "--- $pass ok, $fail fallas ---"
[ "$fail" -eq 0 ]
