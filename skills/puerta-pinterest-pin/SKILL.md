---
name: "puerta-pinterest-pin"
description: "Puerta de pins de Pinterest: valida que cada pin use un asset FINAL del listing, keywords del banco con fuente citada y enlace correcto al listing de Etsy antes de entrar a la cola de publicación."
plantilla: false
license: "Apache-2.0"
compatibility: "framework >= 0.4.0"
metadata:
  version: "0.4.1"
  framework_version: "0.12.1"
  regression_suite: "evals/"
  gate_script: "scripts/verificar-pin.py"
---

# Puerta de Pinterest Pin

**Versión: v0.4.0** (2026-10-18: mapa de assets verificado por listing
+ clase declarada + claims — ver "La lección del 2026-10-18") ·
v0.3.0: tipos de pin 1-5, gate real en `scripts/verificar-pin.py`,
video pins 1:1 sin recortar · Rama de publicidad del sistema POD: el
tráfico externo (Pinterest) reporta señales de calidad al listing,
pero solo si el pin muestra exactamente lo que el comprador encuentra
en la tienda.

## Cuándo usarme

- Al generar los pins de un listing recién publicado (mix imagen/video).
- En el slot diario: cada pin de contenido antes de programarse.
- La parrilla del día la decide `estratega-pinterest`; yo solo valido.
- Si el pin no pasa, no entra a la cola. Sin excepciones.

## Tipos de pin (v0.3.0)

| Tipo | Nombre | Asset |
|---|---|---|
| 1 | hero-lifestyle | imagen principal del listing (assets_finales) |
| 2 | lifestyle-alt | otro modelo/pose/color (assets_finales) |
| 3 | detalle | close-up del diseño, o frente plano (front-flat) si el listing no tiene close-up — sin afirmar "close-up" en el texto (assets_finales) |
| 4 | video | MP4 1:1 de Etsy, **sin recortar**, con su `.manifest.json` |
| 5 | folded-decorado | doblada ambientada (assets_finales) |

## La lección del 2026-10-18 (causa raíz, no repetir)

Tres pins salieron MAL publicados (p028-3 el 17-oct; p030-3 y p032-5
el 18-oct): la imagen no era lo que el tipo y el título afirmaban
(tabla de tallas como "folded", modelo de playera como "close-up").
La puerta vieja daba PASS porque solo verificaba que el asset
estuviera *registrado* como final — nunca qué ES la imagen. Las
tablas de tallas están dentro de `assets_finales` (son imágenes del
listing) y la clase del asset se **infirió por su posición** en la
carpeta. Eso es inválido, con contraejemplo medido: en p032 la
doblada es `-5` y `-10` es tabla de tallas; en p034 la doblada ES
`-10` y las tablas son `-8`/`-9`. **El orden de assets no es
uniforme entre listings: la clase jamás se infiere por posición,
nombre de archivo ni analogía con otro listing.**

Además: los MPL de Thanksgiving **no traen close-up** entre sus
imágenes (se sabía desde el 2026-10-16 y no estaba en el sistema).
Conocimiento que vive en un log y no en la puerta es deuda: por eso
ahora vive en el `mapa_assets` del registro y en el gate.

## Mapa de assets (obligatorio antes de pinear un listing)

Cada listing con pins de imagen necesita `mapa_assets` en
`data/tiendas/<tienda-id>/registro-listings.json`: `{basename: clase}` con clase ∈
{hero-lifestyle, lifestyle-alt, lifestyle, front-flat,
folded-decorado, modelo-playera, tee-flat, close-up, tabla-tallas},
más `mapa_assets_fuente` citando la evidencia. Se construye UNA vez
por listing así:

1. Hoja de contacto de TODOS los assets finales del listing
   (miniaturas numeradas con su basename).
2. Inspección visual de la hoja, asset por asset (ojos, no posición).
3. Registrar el mapa + la fuente (fecha y método).

Si el listing no tiene mapa, el gate da FAIL y el trabajo es
construirlo primero — nunca adivinarlo. Al registrar mockups nuevos
de un listing ya publicado se construye/actualiza su mapa en ese
momento (queda como paso del flujo de publicación, no de Pinterest).

## Procedimiento

1. **Armar el paquete** `pin.json`: slug, tipo (1-5), **clase_asset**
   (qué ES la imagen según el mapa verificado), asset (ruta del
   asset; forma canónica relativa a la app, `data/...` — la puerta
   normaliza antes de comparar contra el registro), título,
   descripción, url_listing, tablero,
   keywords_fuente (banco **Pinterest** del nicho:
   `data/banco-keywords/pinterest-<nicho>.md`, no el de Etsy).
2. **Correr** `scripts/verificar-pin.py --pin pin.json` (gate real,
   construido 2026-10-16; antes esta puerta solo existía en papel).
   Hay UNA sola implementación: `scripts/verificar-pin.py` (raíz de
   la app) y la copia de este skill son byte-idénticas y la suite lo verifica
   (la divergencia entre copias era deuda registrada desde v0.3.1 y
   se cerró en v0.4.0). El registro de assets finales vive en
   `data/tiendas/<tienda-id>/registro-listings.json`; el banco de keywords Pinterest en
   `data/banco-keywords/`. Suite de calibración:
   `evals/test-regression.sh` — incluye como casos conocidos-malos los
   TRES pins defectuosos reales de 2026-10-17/18 y como buenos sus
   correcciones; sin suite verde la puerta no se declara calibrada.
3. **PASS** → el pin entra a la cola (`data/cola-pins/`).
   **FAIL** → se corrige el campo violado y se reintenta.

## Puertas mecánicas

- **schema**: pin.json trae slug, tipo (1-5), asset, titulo,
  descripcion, url_listing, tablero, keywords_fuente.
- **asset_final**: tipos 1/2/3/5 → el asset existe y está registrado
  como FINAL de ese listing. Tipo 4 → el asset es el MP4 1:1 del
  listing en `data/videos/`. Nada generado ad-hoc, nada de mockups
  viejos no-finales.
- **mapa_assets** (v0.4.0, tipos imagen): el listing tiene
  `mapa_assets` verificado en el registro y el asset está clasificado
  en él. Sin mapa no hay pin de imagen de ese listing.
- **clase_tipo** (v0.4.0): la `clase_asset` declarada en el pin.json
  debe coincidir EXACTO con la del mapa y ser compatible con el tipo
  (1→hero-lifestyle/lifestyle; 2→lifestyle-alt/modelo-playera/
  lifestyle; 3→close-up/front-flat; 5→folded-decorado). La clase
  **tabla-tallas está prohibida para todo tipo**: una tabla de tallas
  nunca es un pin.
- **claims** (v0.4.0): el texto afirma solo lo que la imagen es —
  "close-up" exige clase close-up; "folded/doblada" exige
  folded-decorado; mencionar tabla/guía de tallas en el texto es FAIL.
- **video_specs** (solo tipo 4): existe el `.manifest.json` del video
  y corresponde al asset (el video se usa tal cual, sin recortar —
  decisión del dueño 2026-10-16).
- **url_listing**: debe coincidir EXACTAMENTE con la `url` registrada
  para el slug en `data/tiendas/<tienda-id>/registro-listings.json`. Si la tienda está
  inscrita en Share & Save, esa URL es el link rastreable
  (`<tienda>.etsy.com/...`); todos los pines usan el formato
  rastreable, sin excepción.
- **keywords_banco**: título+descripción contienen ≥1 keyword
  multi-palabra del banco **Pinterest** del nicho;
  `keywords_fuente` cita el archivo (que existe).
- **tablero**: declarado. La existencia real del tablero en la cuenta es
  gate humano (la API de Pinterest no está conectada).

## Calibraciones (mecanismo vs aplicación)

- `MECANISMO:` el pin muestra el asset final del listing (trazabilidad
  por registro) — universal; caso 2026-10-12.
- `MECANISMO:` keywords con fuente citada del banco — universal.
- `CALIBRACIÓN:` ≥1 keyword multi-palabra — umbral mínimo razonable,
  2026-10-13. Revalidar si el banco cambia de formato.
- Sin cuenta publicada: la cola persiste; nada se pierde ni se inventa.

## Reglas con motivo

- (2026-10-18, caso real) La clase de un asset sale SOLO del
  `mapa_assets` verificado visualmente de ESE listing. Ni posición,
  ni nombre, ni analogía: p034 desmiente cualquier patrón posicional.
- (2026-10-18, caso real) Publicación SOLO por **subida de archivo**.
  PROHIBIDO "Save from URL": el pin nace como guardado ajeno — su
  link destino NO es editable después y queda en formato clásico
  www.etsy.com, sin rastreable Share & Save (pasó en la primera
  republicación correctiva del 2026-10-18: hubo que borrar y
  republicar por subida de archivo). Si la subida de archivo falla,
  se detiene y se reporta; nunca se cae a Save from URL como atajo.
- (2026-10-18) Verificación visual POST-publicación obligatoria
  contra la clase declarada: si un pin publicado no coincide con su
  clase/título, se corrige EN LA MISMA CORRIDA (borrar + republicar
  con el asset de la clase correcta, paquete nuevo por la puerta) y
  se reporta como corrección — no queda como "decisión pendiente del
  dueño": el criterio ya lo dio él (borrar/republicar lo que no
  coincide con la tienda; precedente 2026-10-12). Pinterest no
  permite cambiar la imagen de un pin publicado.
- (2026-10-12, caso real) Dos pins se publicaron con mockups faithful
  viejos (no-finales): el comprador veía algo distinto a la tienda.
  Por eso el gate de asset_final es bloqueante, no advertencia.
- (2026-10-12) Si Pinterest prefiere 2:3 y el asset final es cuadrado, se
  publica el cuadrado tal cual. Una versión rediseñada requiere su
  aprobación explícita.
- Títulos keyword-rich, sin hashtags (formato Pinterest, no Instagram).

## Publicación por navegador (2026-10-14)

No hay conector API de Pinterest. La publicación se hace por navegador:

1. Los pins validados entran a `data/cola-pins/` (JSON por pin).
2. Se publican por navegador en pinterest.com:
   - Subir imagen del asset final
   - Título keyword-rich (del banco)
   - Descripción con keywords
   - Link directo al listing de Etsy
   - Tablero temático (crear si no existe)
3. Estrategia validada por investigación:
   - Un pin = un link (no se agrupan listings)
   - Múltiples pins por producto (3-5), cada uno con diferente imagen/ángulo
   - Tableros por nicho/intención, no genéricos
   - Para POD (reproducible): link directo al listing está bien
   - Formato vertical 2:3 rinde mejor; si el asset es cuadrado se publica tal cual
4. Registrar URLs de pins publicados en `data/tiendas/<tienda-id>/registro-listings.json`.

## Criterio de pins (investigación 2026-10-14)

- **Pin héroe:** imagen lifestyle principal del listing
- **Pin lifestyle:** otra variante/modelo
- **Pin detalle:** flat o folded mostrando el diseño
- Títulos: keyword del banco + ángulo (ocasión/destinatario)
- Descripciones: keyword-rich, sin hashtags
- Consistencia: mejor pocos pins constantes que muchos esporádicos
