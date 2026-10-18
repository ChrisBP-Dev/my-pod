---
name: "estratega-pinterest"
description: "Estratega de Pinterest para My POD: decide la parrilla diaria de 5 pins (qué listings, qué mix de tipos imagen/video, qué tableros, con qué keywords del banco Pinterest). La puerta-pinterest-pin valida; este skill decide."
plantilla: false
license: "Apache-2.0"
compatibility: "framework >= 0.4.0"
metadata:
  version: "0.1.1"
  framework_version: "0.8.0"
---

# Estratega de Pinterest

**Versión 0.1.1** (2026-10-18: elegibilidad por CLASE de asset del
mapa verificado — la parrilla se arma desde el `mapa_assets` del
listing, nunca por posición del archivo) · 0.1.0 (2026-10-16).
Rama de publicidad: Pinterest es un
buscador con intención de compra planificada (no una red social). El
tráfico externo reporta señales de calidad al listing de Etsy.

Decisiones del dueño (2026-10-16): **5 pins/día** (antes 1). Videos
**sin recortar**: se usan los MP4 1:1 de Etsy tal cual. **3-5 pins por
listing**: hero lifestyle, lifestyle alternativo, detalle/close-up,
video pin.

## Rol

No generas assets: decides la parrilla diaria. Qué listings se pinean
hoy, con qué mix de tipos, en qué tableros y con qué keywords del banco
Pinterest (distintas a las de Etsy: descubrimiento, no transacción).

## Entradas (leer todas antes de decidir)

1. `data/registro-listings.json` — listings `publicado_completo`, sus
   `assets_finales`, `url`, `videos_pendientes`.
2. `data/direccion-tienda.md` — foco de la semana (reparto de temas).
3. `data/banco-keywords/pinterest-<nicho>.md` — keywords de Pinterest
   del nicho. Si no existe el banco Pinterest del nicho, se crea con el
   método documentado ahí antes de pinear (nunca se reutiliza el banco
   de Etsy: el lenguaje de descubrimiento es distinto).
4. `data/ledger-ventas.json` — cuando tenga datos: prioriza listings
   con ventas/favoritos (lo que tracciona, se empuja).
5. `data/pins-publicados/` — qué ya se pineó: ningún asset se repite
   en <30 días.

## Método

1. **Elegibilidad.** Solo listings `publicado_completo` CON
   `mapa_assets` verificado en el registro (si falta, se construye
   por inspección visual antes de incluir el listing — ver
   puerta-pinterest-pin v0.4.0). **Cada tipo exige que el listing
   tenga un asset de la clase correspondiente en su mapa**: tipo 1 →
   hero-lifestyle; tipo 2 → lifestyle-alt/modelo-playera; tipo 3 →
   close-up, o front-flat si no hay close-up (los MPL de
   Thanksgiving NO traen close-up: su tipo 3 es front-flat y el
   texto nunca dice "close-up"); tipo 5 → folded-decorado. Si el
   listing no tiene la clase del slot, el slot pasa a otro listing
   que sí la tenga — jamás se sustituye por "el asset que haya"
   manteniendo el tipo o el título. El tipo 4
   (video) requiere video MP4 1:1 generado (`data/videos/` +
   manifest). Si un listing aún no tiene video, su slot de video va a
   otro listing — no se inventa ni se recorta nada.
2. **Rotación.** Los más recientes primero; ciclo completo por todos
   los elegibles antes de repetir listing. Máximo 2 pins del mismo
   listing por día (no saturar un tablero con un solo diseño).
3. **Mix diario (5 pins).** Exactamente:
   - **Tipo 1 — hero lifestyle:** imagen principal del listing.
   - **Tipo 2 — lifestyle alternativo:** otro modelo/pose/color.
   - **Tipo 3 — detalle/close-up:** zoom al diseño.
   - **Tipo 4 — video pin:** MP4 1:1 de Etsy, sin recortar.
   - **Tipo 5 — folded decorado:** doblada ambientada (nunca sobre
     blanco plano).
4. **Tableros por nicho/intención, no genéricos.** Ej. enfermería:
   `Christmas Nurse Gifts`, `Funny Nurse Shirts`, `Night Shift Nurse
   Life`. Crear el tablero si no existe es gate humano (la API de
   Pinterest no está conectada); el pin igual entra a la cola con el
   tablero declarado.
5. **Keywords Pinterest.** Del banco `pinterest-<nicho>.md`: título
   keyword-rich + ángulo (ocasión/destinatario); descripción de 2-3
   frases naturales con keywords, sin hashtags (formato Pinterest, no
   Instagram). Pinterest premia intención futura: en octubre se pinean
   keywords de Navidad (ventana de planificación ~2 meses).
6. **Videos.** Título/descripción con las mismas reglas que imagen.
   El asset es el MP4 tal cual salió del pipeline de video de Etsy.

## Salida

5 archivos `pin.json` en `data/cola-pins/`, cada uno con
`slug, tipo (1-5), clase_asset (la del mapa verificado), asset (ruta
absoluta), titulo, descripcion, url_listing, tablero,
keywords_fuente`. Todos deben pasar `scripts/verificar-pin.py`
(v0.4.0: incluye mapa/clase/claims) antes de entrar a la cola. Sin
PASS no hay cola.

## Reglas

- Un pin = un link (nunca se agrupan listings en un pin).
- El asset es siempre FINAL del registro; el video es siempre el 1:1
  sin recortar. Nada generado ad-hoc.
- Si Pinterest prefiere 2:3 y el asset es cuadrado, se publica el
  cuadrado tal cual. Una versión rediseñada requiere aprobación del
  dueño.
- Consistencia > volumen: 5 pins todos los días, no 20 un día y cero
  al siguiente.
- Nada de teoría: cada parrilla cita qué listings rotaron y por qué.

## Calibraciones (mecanismo vs instancia)

- `MECANISMO:` 5 pins/día con mix fijo de tipos 1-5 — universal para
  la tienda; volumen y mix los fijó el dueño 2026-10-16.
- `MECANISMO:` rotación con ciclo completo antes de repetir —
  universal; evita saturar tableros.
- `CALIBRACIÓN:` no repetir asset en <30 días — umbral razonable,
  2026-10-16. Revalidar cuando haya datos de impresiones.
