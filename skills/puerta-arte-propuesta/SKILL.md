---
name: "puerta-arte-propuesta"
description: "Puerta del arte-propuesta: valida el PNG del diseño ANTES de generar ningún mockup — fondo transparente, 300 DPI y dimensiones de impresión. Lo más barato de rechazar."
plantilla: false
license: "Apache-2.0"
compatibility: "framework >= 0.4.0"
metadata:
  version: "0.3.0"
  framework_version: "0.8.0"
  regression_suite: "evals/"
---

# Puerta de Arte-Propuesta

**Versión: v0.3.0** · Primera puerta del flujo POD: la propuesta se valida
antes de generar ningún mockup. Un arte con fondo se rechaza aquí, no
después de 12 mockups.

## Cuándo usarme

- Al recibir la propuesta del diseño (PNG), antes de aprobar el arte.
- Si FAIL, el diseño vuelve a corrección. No se genera flat-lay.

## Procedimiento estándar (2026-10-15, endurecido)

1. **Generar** el PNG con el brief (fondo transparente, sin backdrop).
2. **Limpiar** SIEMPRE: `scripts/limpiar-fondo.py --archivo ARTE.png`
   (elimina blanco puro global — método canónico; no es opcional).
3. **Correr** `scripts/verificar-arte.py` (`--archivo`, `--ancho-pulgadas`).
4. **PASS** → el arte pasa a aprobación humana (ojo: counters).
   **FAIL** → se devuelve con el criterio violado. Si falla
   `sin_blanco_puro`, repetir paso 2 y re-verificar.
5. **Draft en Printify** → el dueño revisa ubicación en gris.
6. **Mockups** salen de Printify. Nada propio.

## Puertas mecánicas

- **formato**: PNG con canal alfa.
- **fondo_limpio**: las 4 esquinas alfa = 0 (atrapa el PNG con fondo
  de un color aplanado).
- **recorte_ajustado**: el bbox del contenido deja ≤32px transparentes
  (criterio del dueño: recortado exacto al arte, sin bordes vacíos —
  los bordes vacíos distorsionan el área de impresión).
- **Reparación** `--autotrim`: recorta al bbox + 4px y re-verifica.
- **sin_blanco_puro**: blanco puro ≤0.3% (método canónico 2026-10-15).
- **dpi**: ≥300 al ancho de impresión del producto.
- **dimensiones**: lado menor ≥3000px (archivo de impresión).
- **sin_blancos_interiores**: blanco/casi-blanco opaco dentro del bbox ≤8%
  (atrapa el fondo sin limpiar: p022 mancha crema entre los elfos, p024
  disco blanco, 2026-10-15). Entre 2% y 8% → adjudicación visual (puede
  ser blanco de diseño: papel, copos — no se destruye con key global).
- **cabe_en_area_impresion**: INFORMATIVO, no bloquea (corrección suya
  2026-10-15): los diseños altos están permitidos; el criterio va en la
  COLOCACIÓN (scale-to-fit en publicar-printify-etsy) — el diseño debe
  verse COMPLETO en el mockup, nada cortado.
- **Método de limpieza canónico (2026-10-15, aprendido del rescate p021-p026):**
  en estos artes el diseño usa CREMA/blanco roto para sus elementos claros
  (rellenos de letras, luna, taza, cofia — nunca blanco puro) mientras que
  los restos de fondo son BLANCO PURO (min RGB ≥250, dispersión ≤18).
  Limpiar blanco puro globalmente elimina TODO el fondo —incluidos counters
  y espacios encerrados entre letras— sin tocar el diseño. Verificado en los
  6 artes: blanco puro 0% tras limpiar, diseño intacto.
- **Brief de generación (2026-10-15, pedido suyo):** fondo 100% transparente
  sin halo ni resplandor, sin backdrop/papel/viñeta detrás del diseño.
  El diseño debe mostrarse completo visualmente.
- **Criterios de generación (2026-10-15, de lo aprendido en el rescate):**
  el generador debe apuntar bien desde el inicio, no depender de la limpieza:
  1. **Fondo**: transparente real en TODAS partes —incluidos counters de
     letras (a, e, o, P, R) y espacios encerrados entre letras. Sin blanco
     ni crema en zonas que no sean elemento del diseño.
  2. **Disciplina de color**: los elementos claros del diseño usan CREMA /
     blanco roto cálido (nunca blanco puro #FFFFFF). Así el blanco puro,
     si aparece, es inconfundiblemente fondo y se elimina sin riesgo.
  3. **Resolución**: 300 DPI al tamaño de impresión (p. ej. 10" de ancho
     → ≥3000 px de ancho).
  4. **Composición completa**: el diseño entero visible, nada cortado en
     los bordes del PNG. Los diseños altos están permitidos.
  5. **Texto**: ortografía exacta, letras legibles, sin artefactos.
  6. **Sin halo**: bordes del diseño limpios, sin resplandor blanco
     alrededor de los elementos.
  **Fragmento para el prompt de imagen** (copiar tal cual al generar):
  > "isolated on a fully transparent background, no backdrop, no paper,
  > no vignette, no glow or halo around the design; light-colored areas
  > in warm cream/off-white tones (never pure white); transparent inside
  > letter counters and enclosed gaps; complete composition, nothing
  > cropped at the edges"
- **Gate humano**: counters — agujeros de letras (a, e, o, P...) sin fondo
  metido. El código no distingue un counter limpio de un diseño sin letras;
  va en el checklist del aprobador.

## Calibraciones (mecanismo vs instancia)

- `MECANISMO:` validar el arte antes del primer mockup (costo de rechazo
  mínimo) — universal.
- `MECANISMO:` fondo transparente medido por bbox alfa — universal.
- `CALIBRACIÓN:` MARGEN_MAX 32px, LADO_MIN 3000px, DPI_MIN 300 —
  calibrados en vitals-stable-print-300dpi.png (margen 22px), 2026-10-13.
  Revalidar si cambia el producto (otro ancho de impresión).
- `MECANISMO:` verifier-repair — el recorte es determinista y seguro,
  la puerta lo repara y re-verifica en vez de solo bloquear.

## Reglas con motivo

- (2026-10-13, errores recurrentes suyos) Los errores típicos: PNG con
  fondo de un color, fondo metido dentro de las letras. El primero lo
  atrapa `fondo_limpio`; el segundo lo revisa el ojo (gate humano
  declarado, no promesa falsa del código).
