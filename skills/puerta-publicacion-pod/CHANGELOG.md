# CHANGELOG — puerta-publicacion-pod

## v0.2.3 (2026-10-19)
- Fase de mejora P2: creadas las calibraciones de base doblada
  `data/bases-doblada/gildan-18000-{white,sand,sportgrey}.json`
  (escala 1.30, calibrada contra el golden set aprobado; el
  directorio estaba declarado en ARQUITECTURA-DATOS.md pero los
  archivos nunca llegaron a la app limpia — los 3 casos G1 de
  doblada fallaban "sin calibración de base doblada"). Validado:
  golden PASS ×3, negativos FAIL ×3 en todo el rango 1.23–1.36.
- La ruta de la calibración se resuelve desde la raíz de la app
  (sin `~/workspace/my-pod` quemado en el código).
- Diagnóstico G1 onmodel (queda ABIERTO, decisión del dueño):
  el método de gap por color no es válido en fotos on-model
  reales (pelo/piel/fondo saturan desde el cuello; el cuello
  default 30% no coincide con la base ≈40%) — los 3 golden están
  visualmente bien colocados (gap real ≈16%).

## v0.1.0 (2026-10-13)
- Nace como piloto del formato Rameli nuevo: valida mockups antes de
  publicar (dimensiones 2000×2000, DPI del arte ≥ 300, placement del diseño
  contra la referencia aprobada, todo medido por código).
- Puertas mecánicas: `scripts/verificar-publicacion.py` (SIFT + RANSAC con
  semilla fija; determinista e invariante al color de la prenda).
- Validación: 12/12 del golden set en PASS, 3/3 fixtures negativos en FAIL
  con criterio nombrado, DPI del arte 301.7, corridas bit-idénticas.
- Pineado a Rameli v0.6.0 (`framework_version` en el frontmatter).

## v0.2.0 (2026-10-13)
- La puerta acepta `--referencia` = flat-lay aprobado DE ESE DISEÑO
  (criterio canónico de colocación 2026-10-13). El modo golden set por
  estilo/color queda como heredado (solo diseños del kit).
- Retirada la calibración fosilizada gap/ancho-cuello 0.41 como número
  universal: era una medición puntual. La discrepancia 0.41 vs 0.25 queda
  disuelta (ningún número vale en general).
- Nueva sección "Calibraciones (mecanismo vs instancia)" en SKILL.md:
  cada umbral declara su naturaleza y su disparador de revalidación.
- Nueva suite ejecutable `evals/test-regression.sh` (G1/G2/F1/F2/F3 + R1/R2
  del modo --referencia).

## v0.2.1 (2026-10-13)
- `cargar_arte` acota el arte a 1600px para SIFT (SIFT_ARTE_MAX): un arte
  de 4500px (upscales p002/p004/p005) mataba el proceso por OOM. La
  medición es invariante a escala; suite 18/18 re-verificada.

## v0.2.2 (2026-10-13)
- FIX: crash por división por cero cuando el bbox de referencia es inválido
  (ahora falla con mensaje claro en vez de romperse).
- NUEVO: verificación específica para doblada (`gate_doblada_placement`).
  El SIFT no sirve con oclusión del doblez; se verifica el método:
  calibración de la base existe + hay contenido de diseño en la zona
  esperada (varianza de color ≥2x la tela pura). Las 9 dobladas (p002/p004/p005
  × 3 colores) pasan.
