#!/usr/bin/env bash
# Suite de regresión de puerta-pinterest-pin.
# Falla (exit != 0) si algún caso no da el veredicto esperado.
set -u
SKILL="$(cd "$(dirname "$0")/.." && pwd)"
V="$SKILL/scripts/verificar-pin.py"
REG="$SKILL/../../data/registro-listings.json"
BANCO="$SKILL/../../data/banco-keywords/enfermeria.md"
ASSET_SANTAS="$HOME/workspace/goals/pod-etsy-sistema-operativo-q4-2026/files/disenos/mockups-santas-favorite-nurse/02-flatlay-white-2000.jpg"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
ok=0; fail=0

run() { # run <nombre> <veredicto-esperado> <pin.json>
  local nombre="$1" esperado="$2" pin="$3"
  local got rc
  got=$(python3 "$V" --pin "$pin" --registro "$REG" 2>/dev/null | python3 -c "import json,sys; print(json.load(sys.stdin)['veredicto'])")
  rc=$?
  if [[ "$got" == "$esperado" ]]; then ok=$((ok+1));
  else fail=$((fail+1)); echo "FALLA: $nombre esperaba $esperado, dio '$got' (rc=$rc)"; fi
}

pin_base() { # escribe pin.json base válido en $1
  python3 - "$1" <<'EOF'
import json, sys, os
base = {
  "slug": "santas-favorite-nurse",
  "asset": os.path.expanduser("~/workspace/goals/pod-etsy-sistema-operativo-q4-2026/files/disenos/mockups-santas-favorite-nurse/02-flatlay-white-2000.jpg"),
  "titulo": "Funny Nurse Crewneck Sweatshirt | Christmas Gift for Night Shift Nurse",
  "descripcion": "Night shift nurse sweatshirt, funny RN crewneck — perfect christmas gift for night shift nurse. Soft crewneck for long shifts.",
  "url_listing": "https://www.etsy.com/listing/4589992085",
  "tablero": "Nurse Gifts",
  "keywords_fuente": os.path.expanduser("~/workspace/pod-limpio/data/banco-keywords/enfermeria.md"),
}
json.dump(base, open(sys.argv[1], "w"))
EOF
}

# P1: pin válido
pin_base "$TMP/p1.json"; run "P1 valido" PASS "$TMP/p1.json"

# F1: asset no-final (existe pero no está en el registro)
python3 - "$TMP/p1.json" "$TMP/f1.json" <<'EOF'
import json, sys, os
p = json.load(open(sys.argv[1])); p["asset"] = os.path.expanduser("~/workspace/goals/pod-etsy-sistema-operativo-q4-2026/files/disenos/mockups/faithful/comparativa-prop1-contraste.jpg")
json.dump(p, open(sys.argv[2], "w"))
EOF
run "F1 asset no-final" FAIL "$TMP/f1.json"

# F2: URL de otro listing
python3 - "$TMP/p1.json" "$TMP/f2.json" <<'EOF'
import json, sys
p = json.load(open(sys.argv[1])); p["url_listing"] = "https://www.etsy.com/listing/4591617678"
json.dump(p, open(sys.argv[2], "w"))
EOF
run "F2 url otro listing" FAIL "$TMP/f2.json"

# F3: sin keywords del banco
python3 - "$TMP/p1.json" "$TMP/f3.json" <<'EOF'
import json, sys
p = json.load(open(sys.argv[1])); p["titulo"] = "Lindo suéter"; p["descripcion"] = "Suéter bonito para regalo"
json.dump(p, open(sys.argv[2], "w"))
EOF
run "F3 sin keywords" FAIL "$TMP/f3.json"

# F4: slug desconocido
python3 - "$TMP/p1.json" "$TMP/f4.json" <<'EOF'
import json, sys
p = json.load(open(sys.argv[1])); p["slug"] = "diseno-fantasma"
json.dump(p, open(sys.argv[2], "w"))
EOF
run "F4 slug desconocido" FAIL "$TMP/f4.json"

# F5: tablero vacío
python3 - "$TMP/p1.json" "$TMP/f5.json" <<'EOF'
import json, sys
p = json.load(open(sys.argv[1])); p["tablero"] = ""
json.dump(p, open(sys.argv[2], "w"))
EOF
run "F5 tablero vacio" FAIL "$TMP/f5.json"

echo "--- $ok ok, $fail fallas ---"
[[ $fail -eq 0 ]]
