#!/usr/bin/env bash
# Suite de regresión de puerta-pinterest-pin (v0.4.0, 2026-10-18).
# Calibración: casos conocidos-MALOS reales (los pins defectuosos que
# llegaron a publicarse) deben dar FAIL y los conocidos-BUENOS, PASS.
# Falla (exit != 0) si algún caso no da el veredicto esperado.
set -u
SKILL="$(cd "$(dirname "$0")/.." && pwd)"
APP="$(cd "$SKILL/../.." && pwd)"
V="$APP/scripts/verificar-pin.py"
VSKILL="$SKILL/scripts/verificar-pin.py"
M="$APP/data/mockups"
BANCO="data/banco-keywords/pinterest-enfermeria.md"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
ok=0; fail=0

# Las dos copias del gate deben ser byte-idénticas (convergencia 2026-10-18)
if cmp -s "$V" "$VSKILL"; then ok=$((ok+1)); else fail=$((fail+1)); echo "FALLA: las copias del gate difieren"; fi

run() { # run <nombre> <veredicto-esperado> <pin.json>
  local nombre="$1" esperado="$2" pin="$3"
  python3 "$V" --pin "$pin" >/dev/null 2>&1; local rc=$?
  local got="FAIL"; [[ $rc -eq 0 ]] && got="PASS"
  if [[ "$got" == "$esperado" ]]; then ok=$((ok+1));
  else fail=$((fail+1)); echo "FALLA: $nombre esperaba $esperado, dio $got"; python3 "$V" --pin "$pin" 2>&1 | head -3; fi
}

mk() { # mk <archivo> <slug> <tipo> <clase|-> <asset> <titulo> <desc> <url> <tablero>
  python3 - "$@" <<'EOF'
import json, sys
_, path, slug, tipo, clase, asset, titulo, desc, url, tablero = sys.argv
p = {"slug": slug, "tipo": int(tipo), "asset": asset, "titulo": titulo,
     "descripcion": desc, "url_listing": url, "tablero": tablero,
     "keywords_fuente": "data/banco-keywords/pinterest-enfermeria.md"}
if clase != "-":
    p["clase_asset"] = clase
json.dump(p, open(path, "w"))
EOF
}

U28="https://mynightshiftshop.etsy.com/listing/4597477587"
U30="https://mynightshiftshop.etsy.com/listing/4597491807"
U32="https://mynightshiftshop.etsy.com/listing/4597597346"
U34="https://mynightshiftshop.etsy.com/listing/4597592457"

# ---------- conocidos BUENOS (PASS) ----------
# P1: p032 tipo 5 con su doblada REAL (-5)
mk "$TMP/p1.json" p032 5 folded-decorado "$M/p032/p032-5.jpg" \
  "Nurse Appreciation Gifts: Code Turkey Folded Thanksgiving ER Sweatshirt" \
  "Nurse appreciation gifts for the ER nurse: a turkey in scrubs pushing a crash cart, folded and ready for fall. Funny nurse shirts energy for Thanksgiving." \
  "$U32" "Funny Nurse Shirts"
run "P1 p032 folded real" PASS "$TMP/p1.json"

# P2: p034 tipo 5 con su doblada REAL (-10 en ESTE listing: el mapa manda)
mk "$TMP/p2.json" p034 5 folded-decorado "$M/p034/p034-10.jpg" \
  "Nurse Appreciation Gifts: ER Turkey Trot Folded Thanksgiving Sweatshirt" \
  "Nurse appreciation gifts for the ER nurse who never stops moving: a turkey in scrubs sprinting past the ER sign, folded and ready for fall. Funny nurse shirts energy for Thanksgiving." \
  "$U34" "Funny Nurse Shirts"
run "P2 p034 folded real (-10)" PASS "$TMP/p2.json"

# P3: p030 tipo 3 detalle con front-flat (-3), sin afirmar close-up
mk "$TMP/p3.json" p030 3 front-flat "$M/p030/p030-3.jpg" \
  "Cute Nurse Sweatshirt Front Detail: Pumpkin Spice and IV Drips Design" \
  "The front print of this cute nurse sweatshirt, shown flat on the sport grey crewneck: pumpkin spice cup and autumn leaves. Sweet nurse gift ideas for Thanksgiving." \
  "$U30" "Thanksgiving Nurse Gifts"
run "P3 p030 detalle front-flat" PASS "$TMP/p3.json"

# P4: p030 tipo 1 hero (-1)
mk "$TMP/p4.json" p030 1 hero-lifestyle "$M/p030/p030-1.jpg" \
  "Nurse Gift Ideas: Pumpkin Spice and IV Drips Thanksgiving Nurse Sweatshirt" \
  "Nurse gift ideas for fall: pumpkin spice coffee meets IV drips on a cozy Thanksgiving crewneck. Nurse appreciation gifts for RNs who run on caffeine and compassion." \
  "$U30" "Thanksgiving Nurse Gifts"
run "P4 p030 hero" PASS "$TMP/p4.json"

# ---------- conocidos MALOS reales (FAIL) ----------
# F1: EL pin defectuoso publicado 2026-10-18 — p032 tipo 5 con tabla de tallas (-10)
mk "$TMP/f1.json" p032 5 folded-decorado "$M/p032/p032-10.jpg" \
  "Nurse Appreciation Gifts: Code Turkey Folded Thanksgiving ER Sweatshirt" \
  "Nurse appreciation gifts for the ER nurse: a turkey in scrubs pushing a crash cart, folded and ready for fall. Funny nurse shirts energy for Thanksgiving." \
  "$U32" "Funny Nurse Shirts"
run "F1 p032 tabla como folded (defecto real 2026-10-18)" FAIL "$TMP/f1.json"

# F2: EL pin defectuoso publicado 2026-10-18 — p030 tipo 3 'Close-Up' con modelo playera (-6)
mk "$TMP/f2.json" p030 3 close-up "$M/p030/p030-6.jpg" \
  "Cute Nurse Sweatshirt Detail: Pumpkin Spice and IV Drips Close-Up" \
  "A close-up of this cute nurse sweatshirt: pumpkin spice cup, ECG steam and autumn leaves in warm fall tones. Sweet nurse gift ideas for Thanksgiving." \
  "$U30" "Thanksgiving Nurse Gifts"
run "F2 p030 close-up falso (defecto real 2026-10-18)" FAIL "$TMP/f2.json"

# F3: EL pin defectuoso publicado 2026-10-17 — p028 tipo 3 'Close-Up' con modelo playera (-6)
mk "$TMP/f3.json" p028 3 close-up "$M/p028/p028-6.jpg" \
  "Cute Nurse Sweatshirt Detail: Thankful Nurse Turkey Design Close-Up" \
  "A close-up of the cute nurse sweatshirt everyone will be thankful for: watercolor turkey, pumpkins and fall leaves. Night shift nurse gifts this Thanksgiving." \
  "$U28" "Thanksgiving Nurse Gifts"
run "F3 p028 close-up falso (defecto real 2026-10-17)" FAIL "$TMP/f3.json"

# F4: clase declarada no coincide con el mapa (dice folded, es front-flat)
mk "$TMP/f4.json" p032 5 folded-decorado "$M/p032/p032-3.jpg" \
  "Nurse Appreciation Gifts: Code Turkey Folded Thanksgiving ER Sweatshirt" \
  "Nurse appreciation gifts for the ER nurse, folded and ready for fall. Funny nurse shirts energy for Thanksgiving." \
  "$U32" "Funny Nurse Shirts"
run "F4 clase declarada != mapa" FAIL "$TMP/f4.json"

# F5: sin clase_asset declarada
mk "$TMP/f5.json" p032 5 - "$M/p032/p032-5.jpg" \
  "Nurse Appreciation Gifts: Code Turkey Folded Thanksgiving ER Sweatshirt" \
  "Nurse appreciation gifts for the ER nurse, folded and ready for fall. Funny nurse shirts energy for Thanksgiving." \
  "$U32" "Funny Nurse Shirts"
run "F5 sin clase_asset" FAIL "$TMP/f5.json"

# F6: front-flat válido pero el título afirma 'Close-Up' (claims)
mk "$TMP/f6.json" p030 3 front-flat "$M/p030/p030-3.jpg" \
  "Cute Nurse Sweatshirt Detail: Pumpkin Spice and IV Drips Close-Up" \
  "The front print of this cute nurse sweatshirt, shown flat on the sport grey crewneck. Sweet nurse gift ideas for Thanksgiving." \
  "$U30" "Thanksgiving Nurse Gifts"
run "F6 claim close-up con front-flat" FAIL "$TMP/f6.json"

# F7: URL de otro listing
mk "$TMP/f7.json" p030 1 hero-lifestyle "$M/p030/p030-1.jpg" \
  "Nurse Gift Ideas: Pumpkin Spice and IV Drips Thanksgiving Nurse Sweatshirt" \
  "Nurse gift ideas for fall: pumpkin spice coffee meets IV drips. Nurse appreciation gifts for RNs." \
  "$U32" "Thanksgiving Nurse Gifts"
run "F7 url otro listing" FAIL "$TMP/f7.json"

# F8: sin keywords del banco
mk "$TMP/f8.json" p030 1 hero-lifestyle "$M/p030/p030-1.jpg" \
  "Lindo suéter otoñal" "Suéter bonito para regalo" \
  "$U30" "Thanksgiving Nurse Gifts"
run "F8 sin keywords" FAIL "$TMP/f8.json"

# F9: slug sin mapa_assets (p021 aún no tiene mapa verificado) → FAIL por mapa
mk "$TMP/f9.json" p021 5 folded-decorado "$APP/data/mockups/p021/folded2-sand.jpg" \
  "Funny Nurse Shirts: Twelve Shifts of Christmas Folded Crewneck" \
  "Funny nurse shirts for Christmas: folded and ready. Nurse appreciation gifts for night shift." \
  "https://mynightshiftshop.etsy.com/listing/4596086167" "Funny Nurse Shirts"
run "F9 slug sin mapa verificado" FAIL "$TMP/f9.json"

# F10: asset no-final (no está en assets_finales del slug)
mk "$TMP/f10.json" p030 1 hero-lifestyle "$M/p032/p032-1.jpg" \
  "Nurse Gift Ideas: Pumpkin Spice and IV Drips Thanksgiving Nurse Sweatshirt" \
  "Nurse gift ideas for fall: pumpkin spice coffee meets IV drips. Nurse appreciation gifts for RNs." \
  "$U30" "Thanksgiving Nurse Gifts"
run "F10 asset de otro listing" FAIL "$TMP/f10.json"

echo "--- $ok ok, $fail fallas ---"
[[ $fail -eq 0 ]]
