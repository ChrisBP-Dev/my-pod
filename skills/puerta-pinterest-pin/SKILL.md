---
name: "puerta-pinterest-pin"
description: "Puerta de pins de Pinterest: valida que cada pin use un asset FINAL del listing, keywords del banco con fuente citada y enlace correcto al listing de Etsy antes de entrar a la cola de publicación."
plantilla: false
license: "Apache-2.0"
compatibility: "framework >= 0.4.0"
metadata:
  version: "0.2.0"
  framework_version: "0.8.0"
  regression_suite: "evals/"
---

# Puerta de Pinterest Pin

**Versión: v0.1.0** · Rama de publicidad del sistema POD: el tráfico
externo (Pinterest) reporta señales de calidad al listing, pero solo si el
pin muestra exactamente lo que el comprador encuentra en la tienda.

## Cuándo usarme

- Al generar los pins de un listing recién publicado (mix imagen/video).
- En el slot diario: cada pin de contenido antes de programarse.
- Si el pin no pasa, no entra a la cola. Sin excepciones.

## Procedimiento

1. **Armar el paquete** `pin.json`: slug, asset (ruta absoluta),
   título, descripción, url_listing, tablero, keywords_fuente.
2. **Correr** `scripts/verificar-pin.py --pin pin.json`.
   El registro de assets finales vive en `data/registro-listings.json`;
   el banco de keywords en `data/banco-keywords/<nicho>.md`.
3. **PASS** → el pin entra a la cola (`data/cola-pins/`).
   **FAIL** → se corrige el campo violado y se reintenta.

## Puertas mecánicas

- **asset_final**: el asset existe y está registrado como FINAL de ese
  listing. Nada generado ad-hoc, nada de mockups viejos no-finales.
- **url_listing**: `https://www.etsy.com/listing/<id>` y el id coincide
  con el registrado para el slug.
- **keywords_banco**: título+descripción contienen ≥1 keyword multi-palabra
  del banco del nicho; `keywords_fuente` cita el archivo (que existe).
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
