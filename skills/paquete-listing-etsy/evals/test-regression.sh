#!/usr/bin/env bash
# Suite de regresión de paquete-listing-etsy (creada 2026-10-19,
# Propuesta 2 de la auditoría de adopción docs/AUDITORIA-ADOPCION-V0110.md:
# el skill declaraba regression_suite "evals/" con la carpeta vacía).
# Casos: un paquete real publicado (p002, conocido-bueno) debe PASS;
# los fixtures con un defecto mecánico conocido deben FAIL nombrando
# el criterio. Falla (exit != 0) si algún caso no da el veredicto esperado.
set -u
SKILL="$(cd "$(dirname "$0")/.." && pwd)"
APP="$(cd "$SKILL/../.." && pwd)"
V="$SKILL/scripts/verificar-paquete.py"
FIX="$SKILL/evals/fixtures"
ok=0; fail=0

run() { # run <nombre> <veredicto> <paquete> [criterio-esperado]
  local nombre="$1" esperado="$2" pq="$3" criterio="${4:-}"
  local out rc got="FAIL"
  out="$(python3 "$V" --paquete "$pq" 2>&1)"; rc=$?
  [[ $rc -eq 0 ]] && got="PASS"
  if [[ "$got" != "$esperado" ]]; then
    fail=$((fail+1)); echo "FALLA: $nombre esperaba $esperado, dio $got"; echo "$out" | head -3; return
  fi
  if [[ -n "$criterio" && "$out" != *"$criterio"* ]]; then
    fail=$((fail+1)); echo "FALLA: $nombre no nombró el criterio '$criterio'"; echo "$out" | head -3; return
  fi
  ok=$((ok+1))
}

# Conocido-bueno real: el paquete de p002, publicado y válido.
run "P1 paquete real p002" PASS "$APP/data/paquetes-listing/p002-paquete.md"
# Conocido-bueno sintético mínimo.
run "P2 fixture válido" PASS "$FIX/paquete-valido.md"
# Conocidos-malos: un defecto cada uno, criterio nombrado.
run "F1 tag >20 caracteres" FAIL "$FIX/paquete-tag-largo.md" "caracteres > 20"
run "F2 sin disclosure de IA" FAIL "$FIX/paquete-sin-disclosure.md" "disclosure de IA"

echo "--- $ok ok, $fail fallas ---"
[[ $fail -eq 0 ]]
