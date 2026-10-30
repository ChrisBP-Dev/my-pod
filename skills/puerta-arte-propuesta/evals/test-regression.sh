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
# Regresión 2026-10-30 (franja de limpieza, p087-p091): la salida de
# la puerta exige SIEMPRE el zoom de franja sobre fondo oscuro (paso
# 2d) y emite el resumen de zonas de adjudicación (paso 2c).
out=$(python3 "$V" --archivo "$SKILL/evals/fixtures/arte-plano-bordado.png" --metodo bordado 2>/dev/null)
if echo "$out" | python3 -c "
import json, sys
d = json.load(sys.stdin)
assert 'FONDO OSCURO' in d['gate_humano_pendiente']
za = d['mediciones']['zonas_adjudicacion']
assert za['zoom_fondo_oscuro_siempre'] is True
assert isinstance(za['duros'], int) and isinstance(za['sospechosos'], int)
" 2>/dev/null; then ok=$((ok+1));
else fail=$((fail+1)); echo "FALLA: REG-2026-10-30 gate_humano sin exigencia de zoom de franja o sin zonas_adjudicacion"; fi
# F9: autotrim seguro conserva el extremo fino (barra 601x13 de baja
# masa unida al bloque): con bbox seguro la salida mide 1409x809 y lo
# declara; con el bbox por masa histórico saldría 1384 de ancho.
out=$(python3 "$V" --archivo "$SKILL/evals/fixtures/arte-extremo-fino.png" --autotrim --salida /tmp/trim-f9.png 2>/dev/null)
tipo=$(echo "$out" | python3 -c "import json,sys; print(json.load(sys.stdin)['autotrim_bbox'])")
tam=$(python3 -c "from PIL import Image; print(Image.open('/tmp/trim-f9.png').size)")
if [[ "$tipo" == "seguro" && "$tam" == "(1409, 809)" ]]; then ok=$((ok+1));
else fail=$((fail+1)); echo "FALLA: F9 autotrim seguro esperaba seguro/(1409, 809), dio '$tipo'/'$tam'"; fi

# Calibración 2026-10-20 (p046 "ICU: I Care U", cazado por el dueño en
# Printify): counters de letras con el fondo horneado — pasaba TODAS las
# puertas (% global de blanco casi cero). El gate mide componentes:
# mancha acromática clara maciza (área>=1500, densidad>=0.25).
# Buenos de referencia medidos: vitals/p036v3/p037v2/p028/p033 <= 0.108.
run "F10 counters rellenos" FAIL counters_rellenos --archivo "$SKILL/evals/fixtures/arte-counters-rellenos.png" --ancho-pulgadas 10.5
run "P5 counters limpios" PASS None --archivo "$SKILL/evals/fixtures/arte-counters-limpios.png" --ancho-pulgadas 10.5
# P6: líneas finas brillantes de diseño (caso real p043: radio <=2.8,
# densidad hasta 0.55) NO son rellenos: salen como sospechosos y pasan.
run "P6 lineas finas de diseno" PASS None --archivo "$SKILL/evals/fixtures/arte-lineas-finas.png" --ancho-pulgadas 10.5
# Sin --adjudicado el script NO escribe (seguridad del barrido
# 2026-10-20: la mayoría de los duros del registro eran diseño).
rm -f /tmp/counters-f10c.png
python3 "$SKILL/scripts/limpiar-counters.py" --archivo "$SKILL/evals/fixtures/arte-counters-rellenos.png" --salida /tmp/counters-f10c.png >/dev/null 2>&1
if [[ ! -f /tmp/counters-f10c.png ]]; then ok=$((ok+1));
else fail=$((fail+1)); echo "FALLA: F10c sin --adjudicado no debio escribir"; fi
# La limpieza de counters rescata el fixture malo y la puerta lo pasa.
python3 "$SKILL/scripts/limpiar-counters.py" --archivo "$SKILL/evals/fixtures/arte-counters-rellenos.png" --salida /tmp/counters-f10.png --adjudicado >/dev/null 2>&1
out=$(python3 "$V" --archivo /tmp/counters-f10.png --ancho-pulgadas 10.5 2>/dev/null)
got=$(echo "$out" | python3 -c "import json,sys; print(json.load(sys.stdin)['veredicto'])")
if [[ "$got" == "PASS" ]]; then ok=$((ok+1));
else fail=$((fail+1)); echo "FALLA: F10b limpieza de counters esperaba PASS tras limpiar, dio '$got'"; fi

# Calibración 2026-10-27 (F5: la doctrina de fuente plana de bordado
# pasó de prosa a puerta mecánica — gate 14 de verificar-arte.py):
# la fuente plana sintética (4 colores) pasa como bordado; el canónico
# DTG a todo color, medido como bordado, cae por no plano (448+
# dominantes medidos en artes reales del registro; p070/p071 planos
# reales miden 5 y 4 y pasan).
run "P14 bordado fuente plana" PASS None --archivo "$K/arte-plano-bordado.png" --ancho-pulgadas 10.5 --metodo bordado
run "F14 bordado fuente no plana" FAIL fuente_bordado_no_plana --archivo "$K/vitals-stable-print-300dpi.png" --ancho-pulgadas 10.5 --metodo bordado

echo "--- $ok ok, $fail fallas ---"
[[ $fail -eq 0 ]]
