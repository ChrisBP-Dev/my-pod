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

# G1–G3 (Programa Estándar F4, 2026-10-23): el generador ya NO
# trae default de detalle de producto (antes era la descripción
# de un producto concreto y se heredaba en silencio).
# G1 sin detalle ni --producto → error claro. G2 con --producto
# lee `detalle_listing` de la ficha (árbol fixture propio).
# G3 con --producto-detalle explícito genera.
G="$SKILL/scripts/generar-paquete.py"
GTMP="$(mktemp -d)"
mkdir -p "$GTMP/data/banco-keywords" "$GTMP/data/productos"
printf '# banco fixture\nkeyword principal: Test Keyword\n' > "$GTMP/data/banco-keywords/fixture.md"
printf '{"slug": "prod-fixture", "detalle_listing": "Producto Fixture de prueba (100%% algodón de mentira)"}\n' > "$GTMP/data/productos/prod-fixture.json"
TAGS=(t1 t2 t3 t4 t5 t6 t7 t8 t9 t10 t11 t12 t13)
BASE=(--diseno px --nicho fixture --descripcion "diseno de prueba" --hook "hook de prueba" --descripcion-larga "descripcion larga de prueba" --colores White --tallas S-3XL --precio 10.00 --keyword "Test Keyword" --tags "${TAGS[@]}")
out="$(cd "$GTMP" && python3 "$G" "${BASE[@]}" --salida "$GTMP/sin.md" 2>&1)"; rc=$?
if [[ $rc -ne 0 && "$out" == *"falta el detalle del producto"* ]]; then
  ok=$((ok+1))
else
  fail=$((fail+1)); echo "FALLA: G1 sin detalle no dio el error esperado (rc=$rc)"; echo "$out" | head -3
fi
out="$(cd "$GTMP" && python3 "$G" "${BASE[@]}" --producto prod-fixture --salida "$GTMP/con-ficha.md" 2>&1)"; rc=$?
if [[ $rc -eq 0 && "$out" == *"paquete generado"* ]] && grep -q "Producto Fixture de prueba" "$GTMP/con-ficha.md"; then
  ok=$((ok+1))
else
  fail=$((fail+1)); echo "FALLA: G2 --producto no leyó detalle_listing de la ficha (rc=$rc)"; echo "$out" | head -3
fi
out="$(cd "$GTMP" && python3 "$G" "${BASE[@]}" --producto-detalle "Detalle explícito de prueba" --salida "$GTMP/explicito.md" 2>&1)"; rc=$?
if [[ $rc -eq 0 && "$out" == *"paquete generado"* ]] && grep -q "Detalle explícito de prueba" "$GTMP/explicito.md"; then
  ok=$((ok+1))
else
  fail=$((fail+1)); echo "FALLA: G3 --producto-detalle explícito no generó (rc=$rc)"; echo "$out" | head -3
fi
rm -rf "$GTMP"

# Conocido-bueno real: el paquete de p002, publicado y válido.
run "P1 paquete real p002" PASS "$APP/data/paquetes-listing/p002-paquete.md"
# Conocido-bueno sintético mínimo.
run "P2 fixture válido" PASS "$FIX/paquete-valido.md"
# Conocidos-malos: un defecto cada uno, criterio nombrado.
run "F1 tag >20 caracteres" FAIL "$FIX/paquete-tag-largo.md" "caracteres > 20"
run "F2 sin disclosure de IA" FAIL "$FIX/paquete-sin-disclosure.md" "disclosure de IA"

echo "--- $ok ok, $fail fallas ---"
[[ $fail -eq 0 ]]
