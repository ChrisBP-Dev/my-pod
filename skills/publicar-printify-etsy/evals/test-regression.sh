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

# F3: higiene de temporales (2026-10-19, fase de mejora v0.12.1 P2 —
# brecha B2 de docs/AUDITORIA-ADOPCION-V0121.md): la puerta de video
# no debe fugar directorios temporales. Se corre el mismo caso p002
# con TMPDIR controlado y el directorio debe quedar VACÍO: antes del
# fix, verificar-video.py (extract_frames con mkdtemp sin borrado)
# fugaba 4 directorios / ~142 MB por corrida de esta suite, y con
# /tmp lleno las suites siguientes daban fallas espurios.
TMPH="$(mktemp -d)"
TMPDIR="$TMPH" python3 "$V" --diseno p002 >/dev/null 2>&1
if [[ -z "$(ls -A "$TMPH")" ]]; then
  ok=$((ok+1))
else
  fail=$((fail+1)); echo "FALLA: la puerta de video fugó temporales:"; ls "$TMPH"
fi
rm -rf "$TMPH"

# F4/F5: puerta de conteo de variantes (2026-10-23, criterio del
# dueño: sin paleta canónica, solo topes — 4 colores/item y 400
# variantes/MPL; contar SOLO is_enabled). Fixtures sintéticos:
# un producto con 3 colores habilitados (y 40 deshabilitados que
# NO deben contarse) → OK; uno con 5 colores habilitados → AVISO.
VV="$SKILL/scripts/verificar-variantes.py"
FIX="$(mktemp -d)"
python3 - "$FIX" <<'PYEOF'
import json, sys
d = sys.argv[1]
def prod(nombre, hab, deshab):
    vals = [{"id": 100+i, "title": c} for i, c in enumerate(
        ["White", "Sand", "Sport Grey", "Navy", "Maroon", "Black"])]
    variantes = []
    vid = 1
    for c in hab:
        for t in ["S", "M"]:
            variantes.append({"id": vid, "title": f"{t} / {c}",
                              "options": [100 + ["White", "Sand", "Sport Grey", "Navy", "Maroon", "Black"].index(c), 15],
                              "is_enabled": True})
            vid += 1
    for c in deshab:
        variantes.append({"id": vid, "title": f"S / {c}",
                          "options": [100 + ["White", "Sand", "Sport Grey", "Navy", "Maroon", "Black"].index(c), 15],
                          "is_enabled": False})
        vid += 1
    return {"title": nombre,
            "options": [{"type": "color", "name": "Colors", "values": vals},
                        {"type": "size", "name": "Sizes",
                         "values": [{"id": 15, "title": "S"}]}],
            "variants": variantes}
json.dump(prod("fixture-ok", ["White", "Sand", "Navy"],
               ["Sport Grey", "Maroon", "Black"] * 13),
          open(f"{d}/ok.json", "w"))
json.dump(prod("fixture-aviso", ["White", "Sand", "Navy", "Maroon", "Black"],
               []), open(f"{d}/aviso.json", "w"))
PYEOF
out="$(python3 "$VV" --desde-json "$FIX/ok.json" 2>&1)"; rc=$?
if [[ $rc -eq 0 && "$out" == *"3 colores"* && "$out" == *"OK"* ]]; then
  ok=$((ok+1))
else
  fail=$((fail+1)); echo "FALLA: fixture-ok no dio OK con 3 colores (rc=$rc)"; echo "$out" | head -5
fi
out="$(python3 "$VV" --desde-json "$FIX/aviso.json" 2>&1)"; rc=$?
if [[ $rc -eq 2 && "$out" == *"AVISO"* && "$out" == *"5 colores"* ]]; then
  ok=$((ok+1))
else
  fail=$((fail+1)); echo "FALLA: fixture-aviso no dio AVISO con 5 colores (rc=$rc)"; echo "$out" | head -5
fi
rm -rf "$FIX"

echo "--- $ok ok, $fail fallas ---"
[[ $fail -eq 0 ]]
