# Prueba de frío multitienda — 2026-10-23 (Programa Estándar My POD, F7)

**Qué es:** una corrida con una **SEGUNDA tienda ficticia** usando
solo el repo (sistema + fixtures), sin tocar datos reales ni
ninguna cuenta. Objetivo: verificar que ningún mecanismo asume
la tienda 1, que las puertas detectan fichas sin configurar y
que las suites son portables. Convierte «multitienda» de diseño
declarado en comportamiento probado (hasta donde una prueba con
fixtures puede: la disponibilidad real de tomas por color en
Printify sigue siendo del piloto en vivo, frente F8).

**Fixtures (en el repo del sistema, no en los datos reales):**
`skills/publicar-printify-etsy/evals/fixtures/frio/` —
`config-sin-configurar.json` y `config-configurada.json` (tienda
ficticia 99999999), fichas `hoodie-ficticio.json` y
`playera-ficticia.json` (composición distinta a la de la tienda
real: hoodie + playera), `entrada-manifesto-frio.json` y
`producto-printify-ficticio.json`.

## Punto 1 — La puerta de completitud visual detecta la ficha sin configurar ✅

- Con la config ficticia **sin** `estado` (y productos con
  catálogo `configurado`): `verificar-ficha-visual.py` →
  **exit 2, DETENIDO**, nombrando exactamente el campo
  (`config → mpl.esquema_mockups.estado`) y el paso que lo
  llena («Calibración visual de la tienda» de onboarding-tienda,
  Fase 1/Fase 4). No inventó ningún valor.
- Con la misma tienda ya `configurado` → **exit 0, operación
  normal**.

## Punto 2 — La puerta de conteo no asume tienda ✅

- `verificar-variantes.py <id>` **sin `--shop`** → **exit 2**:
  «ERROR DE USO: falta --shop — el modo en vivo exige el shop id
  explícito de la tienda activa». Antes de F4 habría corrido
  contra la tienda 29222324 en silencio.
- En modo fixture con el producto ficticio → corre y da OK
  (3 colores, 12 variantes, dentro de límites técnicos).

## Punto 3 — Manifiesto para una composición distinta ⚠️ con hallazgo

- Con presupuesto **consistente** con los pesos de la fixture
  (total 11 = 5+4 visuales + 2 tablas): el generador produce el
  manifiesto para hoodie+playera usando solo el repo y la
  puerta de cobertura da **PASS** (9 visuales, 2 tablas, 0
  colores sin representación, imagen principal correcta). ✅
- **HALLAZGO (real, no forzado a verde):** con la fixture en su
  primera forma — presupuesto de ficha `total_imagenes: 14`
  pero pesos que suman 11 espacios — el generador produce 11
  espacios (manda los pesos) y la puerta de cobertura **FAIL**
  por conteo («11 espacios, esperados 14»). Causa: el mecanismo
  trata `total_imagenes` como **conteo exacto** en la puerta,
  pero el generador deriva los espacios **solo de los pesos**;
  en la composición de la tienda real ambos números coinciden
  por construcción (5+3+2=10) y la inconsistencia nunca se
  había visto. La semántica no está declarada en ningún doc:
  falta decidir (y escribir) si el total es **techo** (el
  generador puede producir menos) o **meta exacta** (la ficha
  debe cuadrar: total = Σ pesos + tablas, y la puerta de
  completitud debería verificar ese cuadre ANTES, no la de
  cobertura después). El comportamiento actual ante la
  inconsistencia es seguro (detiene, no inventa), pero la
  detección es tardía y el mensaje no nombra la causa.
  **Queda como hallazgo para decisión** (Jarvis/dueño), no
  resuelto en esta corrida.
- Residual corregido en esta misma corrida: `verificar-mockups.py`
  traía su propio default `total_imagenes = 10` si la entrada no
  lo declaraba (el generador ya lo había perdido en F3); ahora
  la puerta falla nombrando la ausencia, sin asumir total.

## Punto 4 — Suites de regresión de los skills tocados ✅

Corrida final de esta prueba (2026-10-23), todas en verde:

| Skill | Suite | Resultado |
|---|---|---|
| publicar-printify-etsy | evals/test-regression.sh | **18 ok, 0 fallas** |
| paquete-listing-etsy | evals/test-regression.sh | **7 ok, 0 fallas** |
| puerta-arte-propuesta | evals/test-regression.sh | **18 ok, 0 fallas** |
| estratega-tienda | evals/test-regression.sh (fixtures neutros, F4) | **2 ok, 0 fallas** |
| onboarding-tienda | sin suite determinista — **declarado** en su SKILL.md («Regresión»: su suite es la Fase 6) | n/a declarado |

## Veredicto

La prueba de frío **pasa en sus puntos 1, 2 y 4**, y en el
punto 3 pasa para fichas consistentes y deja **un hallazgo de
semántica** (total = techo vs meta exacta + cuadre de ficha
temprano) documentado con su causa. Ningún mecanismo asumió la
tienda 1 en ninguna corrida. Lo que esta prueba NO prueba (y no
finge): comportamiento con cuentas reales de una segunda
tienda, disponibilidad real de tomas por color en Printify, ni
la experiencia de otro dueño con su propia instancia — eso es
distribución, pendiente declarado del programa (F8 es el
piloto en vivo de la tienda 1).
