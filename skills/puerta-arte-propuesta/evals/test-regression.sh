#!/usr/bin/env bash
# Suite de regresión de puerta-arte-propuesta.
set -u
SKILL="$(cd "$(dirname "$0")/.." && pwd)"
V="$SKILL/scripts/verificar-arte.py"
# K = insumos canónicos de calibración, DENTRO del repo (fase de mejora
# v0.14.0, P1 — antes vivían en $HOME/.../disenos/canonicos, fuera del
# repo: el FALLO del chequeo 3 de `rameli validar`).
# vitals-stable-print-300dpi.png: copia de calibración del canónico de
# producción (que sigue viviendo en su hogar, la carpeta de diseños
# canónicos del goal POD × Etsy); origen copiado el 2026-10-19,
# sha256 6549b13b1672535ae678da35035607a6a764d10727bdc4522ef920b29327a135.
# Si el canónico se regenera, re-copiar y actualizar este hash.
K="$SKILL/evals/fixtures"
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
# Calibración 2026-10-17 (corrección del dueño: recorte con aire + DPI al zoom):
# F5 caza el bug min-vs-por-lado: aire enorme en 2 lados, pegado en los otros 2.
run "F5 aire asimetrico" FAIL recorte_con_bordes_vacios --archivo "$SKILL/evals/fixtures/arte-aire-asimetrico.png" --ancho-pulgadas 3.0
run "P2 zoom con margen" PASS None --archivo "$SKILL/evals/fixtures/arte-zoom-ok.png" --ancho-pulgadas 10.5 --exigir-margen-zoom
run "F6 sin margen zoom" FAIL dpi_sin_margen_zoom --archivo "$K/vitals-stable-print-300dpi.png" --ancho-pulgadas 10.5 --exigir-margen-zoom
# Calibración 2026-10-18 (lote de recortes mutilados p038-p057):
# composición completa sobre el crudo, fidelidad crudo->final y
# autotrim SEGURO (el de masa amputaba extremos de baja masa).
run "P3 composicion crudo completo" PASS None --archivo "$SKILL/evals/fixtures/crudo-completo.png" --es-original
run "F7 composicion toca borde" FAIL composicion_toca_borde --archivo "$SKILL/evals/fixtures/crudo-toca-borde.png" --es-original
run "P4 final fiel a su crudo" PASS None --archivo "$SKILL/evals/fixtures/final-fiel.png" --ancho-pulgadas 10.5 --original "$SKILL/evals/fixtures/crudo-completo.png"
run "F8 final mutilado vs crudo" FAIL fidelidad_recorte_perdida --archivo "$SKILL/evals/fixtures/final-mutilado.png" --ancho-pulgadas 10.5 --original "$SKILL/evals/fixtures/crudo-completo.png"
# F9: autotrim seguro conserva el extremo fino (barra 601x13 de baja
# masa unida al bloque): con bbox seguro la salida mide 1409x809 y lo
# declara; con el bbox por masa histórico saldría 1384 de ancho.
out=$(python3 "$V" --archivo "$SKILL/evals/fixtures/arte-extremo-fino.png" --autotrim --salida /tmp/trim-f9.png 2>/dev/null)
tipo=$(echo "$out" | python3 -c "import json,sys; print(json.load(sys.stdin)['autotrim_bbox'])")
tam=$(python3 -c "from PIL import Image; print(Image.open('/tmp/trim-f9.png').size)")
if [[ "$tipo" == "seguro" && "$tam" == "(1409, 809)" ]]; then ok=$((ok+1));
else fail=$((fail+1)); echo "FALLA: F9 autotrim seguro esperaba seguro/(1409, 809), dio '$tipo'/'$tam'"; fi

echo "--- $ok ok, $fail fallas ---"
[[ $fail -eq 0 ]]
