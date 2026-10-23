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

# F4–F7: puerta de conteo de variantes (v0.11.0, 2026-10-23 —
# colores SIN techo: la guía 3–4 y la extensión 5–6 no detienen;
# 7 colores = OK con AVISO INFORMATIVO; SOLO el límite técnico
# detiene: >400 variantes totales o >70 opciones). El caso viejo
# «5 colores = AVISO/detener» se ELIMINÓ en v0.11.0.
# Fixtures sintéticos (contar SOLO is_enabled):
VV="$SKILL/scripts/verificar-variantes.py"
FIX="$(mktemp -d)"
python3 - "$FIX" <<'PYEOF'
import json, sys
d = sys.argv[1]
COLS = ["White", "Sand", "Sport Grey", "Navy", "Maroon", "Black",
        "Forest Green", "Red"]
def prod(nombre, hab, deshab=(), tallas=5):
    vals = [{"id": 100+i, "title": c} for i, c in enumerate(COLS)]
    variantes = []
    vid = 1
    for c in hab:
        for t in range(tallas):
            variantes.append({"id": vid, "title": f"T{t} / {c}",
                              "options": [100 + COLS.index(c), 15],
                              "is_enabled": True})
            vid += 1
    for c in deshab:
        variantes.append({"id": vid, "title": f"S / {c}",
                          "options": [100 + COLS.index(c), 15],
                          "is_enabled": False})
        vid += 1
    return {"title": nombre,
            "options": [{"type": "color", "name": "Colors", "values": vals},
                        {"type": "size", "name": "Sizes",
                         "values": [{"id": 15, "title": "S"}]}],
            "variants": variantes}
json.dump(prod("fixture-5", COLS[:5], ["Sport Grey"] * 13),
          open(f"{d}/cinco.json", "w"))
json.dump(prod("fixture-6", COLS[:6]), open(f"{d}/seis.json", "w"))
json.dump(prod("fixture-7", COLS[:7]), open(f"{d}/siete.json", "w"))
json.dump(prod("fixture-401", ["White"], tallas=401),
          open(f"{d}/cuatrocientosuno.json", "w"))
PYEOF
out="$(python3 "$VV" --desde-json "$FIX/cinco.json" 2>&1)"; rc=$?
if [[ $rc -eq 0 && "$out" == *"5 colores"* && "$out" == *"OK"* && "$out" != *"DETENCIÓN"* ]]; then
  ok=$((ok+1))
else
  fail=$((fail+1)); echo "FALLA: 5 colores no dio OK sin detención (rc=$rc)"; echo "$out" | head -5
fi
out="$(python3 "$VV" --desde-json "$FIX/seis.json" 2>&1)"; rc=$?
if [[ $rc -eq 0 && "$out" == *"6 colores"* && "$out" == *"OK"* ]]; then
  ok=$((ok+1))
else
  fail=$((fail+1)); echo "FALLA: 6 colores no dio OK (rc=$rc)"; echo "$out" | head -5
fi
out="$(python3 "$VV" --desde-json "$FIX/siete.json" 2>&1)"; rc=$?
if [[ $rc -eq 0 && "$out" == *"7 colores"* && "$out" == *"AVISO INFORMATIVO"* && "$out" == *"OK"* ]]; then
  ok=$((ok+1))
else
  fail=$((fail+1)); echo "FALLA: 7 colores no dio OK con aviso informativo (rc=$rc)"; echo "$out" | head -5
fi
out="$(python3 "$VV" --desde-json "$FIX/cuatrocientosuno.json" 2>&1)"; rc=$?
if [[ $rc -eq 2 && "$out" == *"DETENCIÓN"* && "$out" == *"401 variantes"* ]]; then
  ok=$((ok+1))
else
  fail=$((fail+1)); echo "FALLA: 401 variantes no detuvo por límite técnico (rc=$rc)"; echo "$out" | head -5
fi

# F8–F11: manifiesto de mockups + puerta de cobertura (v0.11.0).
# F8 manifiesto generado válido → PASS. F9 pose repetida en otro
# color → FAIL. F10 toma a evitar → FAIL. F11 color sin
# representación NO declarado → FAIL.
GM="$SKILL/scripts/generar-manifiesto-mockups.py"
VM="$SKILL/scripts/verificar-mockups.py"
python3 - "$FIX" "$APP" <<'PYEOF'
import json, sys
d, app = sys.argv[1], sys.argv[2]
def cat(ruta):
    p = json.load(open(f"{app}/data/productos/{ruta}"))
    return {"tomas": p["tomas_preferidas"]["tomas"],
            "tomas_a_evitar": p["tomas_a_evitar"] +
                              [{"id": "toma-fea", "motivo": "fixture"}]}
entrada = {
  "diseno": "fixture-mockups", "total_imagenes": 10,
  "tabla_tallas_por_producto": 1,
  "items": [
    {"producto": "gildan-18000", "rol_en_listing": "principal",
     "espacios_visuales": 5, "color_prioritario": "Navy",
     "colores": [{"nombre": "White", "tono": "claro"},
                 {"nombre": "Navy", "tono": "oscuro"},
                 {"nombre": "Black", "tono": "oscuro"}],
     "catalogo": cat("gildan-18000.json")},
    {"producto": "bella-canvas-3001", "rol_en_listing": "secundario",
     "espacios_visuales": 3, "color_prioritario": "White",
     "colores": [{"nombre": "White", "tono": "claro"},
                 {"nombre": "Athletic Heather", "tono": "claro"},
                 {"nombre": "Navy", "tono": "oscuro"}],
     "catalogo": cat("bella-canvas-3001.json")}]}
json.dump(entrada, open(f"{d}/entrada-mockups.json", "w"),
          ensure_ascii=False)
PYEOF
python3 "$GM" --desde-json "$FIX/entrada-mockups.json" --salida "$FIX/manifiesto.json" >/dev/null 2>&1
out="$(python3 "$VM" --manifiesto "$FIX/manifiesto.json" --desde-json "$FIX/entrada-mockups.json" 2>&1)"; rc=$?
if [[ $rc -eq 0 && "$out" == *"PASS"* ]]; then
  ok=$((ok+1))
else
  fail=$((fail+1)); echo "FALLA: manifiesto válido no dio PASS (rc=$rc)"; echo "$out" | head -6
fi
python3 - "$FIX" <<'PYEOF'
import json, sys
d = sys.argv[1]
m = json.load(open(f"{d}/manifiesto.json"))
repetido = json.loads(json.dumps(m))
repetido["espacios"][1]["toma_id"] = repetido["espacios"][0]["toma_id"]
json.dump(repetido, open(f"{d}/manifiesto-repetido.json", "w"))
evitar = json.loads(json.dumps(m))
evitar["espacios"][2]["toma_id"] = "toma-fea"
json.dump(evitar, open(f"{d}/manifiesto-evitar.json", "w"))
sin_declarar = json.loads(json.dumps(m))
sin_declarar["colores_sin_representacion"] = []
json.dump(sin_declarar, open(f"{d}/manifiesto-sin-declarar.json", "w"))
PYEOF
out="$(python3 "$VM" --manifiesto "$FIX/manifiesto-repetido.json" --desde-json "$FIX/entrada-mockups.json" 2>&1)"; rc=$?
if [[ $rc -eq 1 && "$out" == *"pose/modelo repetida"* ]]; then
  ok=$((ok+1))
else
  fail=$((fail+1)); echo "FALLA: pose repetida en otro color no dio FAIL (rc=$rc)"; echo "$out" | head -6
fi
out="$(python3 "$VM" --manifiesto "$FIX/manifiesto-evitar.json" --desde-json "$FIX/entrada-mockups.json" 2>&1)"; rc=$?
if [[ $rc -eq 1 && "$out" == *"toma a evitar"* ]]; then
  ok=$((ok+1))
else
  fail=$((fail+1)); echo "FALLA: toma a evitar no dio FAIL (rc=$rc)"; echo "$out" | head -6
fi
out="$(python3 "$VM" --manifiesto "$FIX/manifiesto-sin-declarar.json" --desde-json "$FIX/entrada-mockups.json" 2>&1)"; rc=$?
if [[ $rc -eq 1 && "$out" == *"NO declarado"* ]]; then
  ok=$((ok+1))
else
  fail=$((fail+1)); echo "FALLA: color sin representación no declarado no dio FAIL (rc=$rc)"; echo "$out" | head -6
fi
rm -rf "$FIX"

echo "--- $ok ok, $fail fallas ---"
[[ $fail -eq 0 ]]
