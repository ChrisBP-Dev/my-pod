# CHANGELOG — paquete-listing-etsy

## v0.2.1 (2026-10-23) — colores leídos del borrador (criterio del dueño)
- Paso 2: los **colores del paquete se leen del borrador de Printify por API** (los que el dueño dejó aprobados en su revisión) y con esa lectura se llena `--colores`. Prohibido escribirlos a mano o tomarlos de una lista guardada o del ejemplo del script: **no existe paleta canónica** (ver `publicar-printify-etsy` v0.10.0, §Selección de colores del diseño). Si el borrador cambia, el paquete se regenera.

## v0.2.0 (2026-10-14)
- REGLA DE COHERENCIA paquete-vs-arte (lección cara): antes de generar, abrir el
  arte print aprobado y verificar que concepto/hook/descripción hablen del diseño
  real. Caso: p005 figuraba "ICU Halloween" cuando el arte ya era un carrito
  navideño; p004 describía "enfermera" cuando el arte era un búho. La puerta
  mecánica no detecta incoherencia semántica (solo formato).
- Paquetes p004/p005 regenerados contra el arte real y re-validados con la puerta.

## v0.1.0 (2026-10-14)
- Migración inicial desde el sistema anterior (paquetes manuales en
  `goals/pod-etsy-sistema-operativo-q4-2026/files/paquete-etsy-*.md`).
- Skill genera: título (fórmula SEO), descripción estructurada
  (hook → disclosure IA → made-to-order → DETAILS/FIT), 13 tags, copy.
- Puerta mecánica: valida título ≤140, 13 tags ≤20 car., sin duplicados,
  disclosure IA presente, secciones obligatorias.
- Fuente de keywords: `data/banco-keywords/<nicho>.md` (migrado).
