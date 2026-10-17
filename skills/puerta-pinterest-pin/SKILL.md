---
name: "puerta-pinterest-pin"
description: "Puerta de pins de Pinterest: valida que cada pin use un asset FINAL del listing, keywords del banco con fuente citada y enlace correcto al listing de Etsy antes de entrar a la cola de publicación."
plantilla: false
license: "Apache-2.0"
compatibility: "framework >= 0.4.0"
metadata:
  version: "0.3.1"
  framework_version: "0.8.0"
  regression_suite: "evals/"
  gate_script: "scripts/verificar-pin.py"
---

# Puerta de Pinterest Pin

**Versión: v0.3.0** (2026-10-16: tipos de pin 1-5, gate real en
`scripts/verificar-pin.py`, video pins 1:1 sin recortar) · Rama de
publicidad del sistema POD: el tráfico externo (Pinterest) reporta
señales de calidad al listing, pero solo si el pin muestra exactamente
lo que el comprador encuentra en la tienda.

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
| 3 | detalle | close-up del diseño (assets_finales) |
| 4 | video | MP4 1:1 de Etsy, **sin recortar**, con su `.manifest.json` |
| 5 | folded-decorado | doblada ambientada (assets_finales) |

## Procedimiento

1. **Armar el paquete** `pin.json`: slug, tipo (1-5), asset (ruta
   absoluta), título, descripción, url_listing, tablero,
   keywords_fuente (banco **Pinterest** del nicho:
   `data/banco-keywords/pinterest-<nicho>.md`, no el de Etsy).
2. **Correr** `scripts/verificar-pin.py --pin pin.json` (gate real,
   construido 2026-10-16; antes esta puerta solo existía en papel).
   El registro de assets finales vive en `data/registro-listings.json`;
   el banco de keywords Pinterest en `data/banco-keywords/`.
3. **PASS** → el pin entra a la cola (`data/cola-pins/`).
   **FAIL** → se corrige el campo violado y se reintenta.

## Puertas mecánicas

- **schema**: pin.json trae slug, tipo (1-5), asset, titulo,
  descripcion, url_listing, tablero, keywords_fuente.
- **asset_final**: tipos 1/2/3/5 → el asset existe y está registrado
  como FINAL de ese listing. Tipo 4 → el asset es el MP4 1:1 del
  listing en `data/videos/`. Nada generado ad-hoc, nada de mockups
  viejos no-finales.
- **video_specs** (solo tipo 4): existe el `.manifest.json` del video
  y corresponde al asset (el video se usa tal cual, sin recortar —
  decisión del dueño 2026-10-16).
- **url_listing**: debe coincidir EXACTAMENTE con la `url` registrada
  para el slug en `data/registro-listings.json`. Si la tienda está
  inscrita en Share & Save, esa URL es el link rastreable
  (`<tienda>.etsy.com/...`); todos los pines usan el formato
  rastreable, sin excepción.
- **keywords_banco**: título+descripción contienen ≥1 keyword
  multi-palabra del banco **Pinterest** del nicho;
  `keywords_fuente` cita el archivo (que existe).
- **tablero**: declarado. La existencia real del tablero en la cuenta es
  gate humano (la API de Pinterest no está conectada).

## Calibraciones (mecanismo vs instancia)

- `MECANISMO:` el pin muestra el asset final del listing (trazabilidad
  por registro) — universal; caso 2026-10-12.
- `MECANISMO:` keywords con fuente citada del banco — universal.
- `CALIBRACIÓN:` ≥1 keyword multi-palabra — umbral mínimo razonable,
  2026-10-13. Revalidar si el banco cambia de formato.
- Sin cuenta publicada: la cola persiste; nada se pierde ni se inventa.

## Reglas con motivo

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
4. Registrar URLs de pins publicados en `data/registro-listings.json`.

## Criterio de pins (investigación 2026-10-14)

- **Pin héroe:** imagen lifestyle principal del listing
- **Pin lifestyle:** otra variante/modelo
- **Pin detalle:** flat o folded mostrando el diseño
- Títulos: keyword del banco + ángulo (ocasión/destinatario)
- Descripciones: keyword-rich, sin hashtags
- Consistencia: mejor pocos pins constantes que muchos esporádicos
