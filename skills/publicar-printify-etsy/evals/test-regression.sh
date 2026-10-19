#!/usr/bin/env bash
# Suite de regresión de publicar-printify-etsy (creada 2026-10-19,
# Propuesta 2 de la auditoría de adopción docs/AUDITORIA-ADOPCION-V0110.md:
# el skill declaraba regression_suite "evals/" con la carpeta vacía).
# La puerta verificar-listos-publicar.py usa rutas del árbol principal
# (BASE fija), así que los casos corren contra activos reales:
#  - Un diseño inexistente debe FAIL nombrando lo que falta.
#  - p002 (publicado, con arte y paquete válidos) debe FAIL SOLO por
#    los videos: el glob de videos también captura las variantes de
#    entrega "-etsy.mp4", que no llevan manifiesto de zoom y la puerta
#    de video las rechaza. Comportamiento verificado 2026-10-19; si
#    la puerta se corrige para excluir variantes de entrega, este
#    caso debe actualizarse en la misma sesión (eso es la regresión).
# Falla (exit != 0) si algún caso no da el veredicto esperado.
# Nota: el caso p002 extrae frames de video; la suite tarda ~1 min.
set -u
SKILL="$(cd "$(dirname "$0")/.." && pwd)"
APP="$(cd "$SKILL/../.." && pwd)"
V="$SKILL/scripts/verificar-listos-publicar.py"
ok=0; fail=0

# F1: diseño inexistente → FAIL con los tres criterios de ausencia
out="$(python3 "$V" --diseno p999-inexistente 2>&1)"; rc=$?
if [[ $rc -ne 0 && "$out" == *"falta arte"* && "$out" == *"falta paquete"* && "$out" == *"se requieren 2 videos"* ]]; then
  ok=$((ok+1))
else
  fail=$((fail+1)); echo "FALLA: inexistente no falló con los criterios esperados (rc=$rc)"; echo "$out" | head -5
fi

# F2: p002 → FAIL solo por manifiesto de las variantes -etsy
out="$(python3 "$V" --diseno p002 2>&1)"; rc=$?
if [[ $rc -ne 0 && "$out" == *"sin manifiesto"* && "$out" != *"falta arte"* && "$out" != *"falta paquete"* ]]; then
  ok=$((ok+1))
else
  fail=$((fail+1)); echo "FALLA: p002 no dio el veredicto esperado (rc=$rc)"; echo "$out" | head -8
fi

echo "--- $ok ok, $fail fallas ---"
[[ $fail -eq 0 ]]
