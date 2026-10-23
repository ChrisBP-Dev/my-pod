# CHANGELOG — My POD (aplicación)

## v1.1.0 (2026-10-23) — migración a Rameli v0.19.0 (sin rompientes = MENOR)

- **Pin del framework: 0.18.0 → 0.19.0**, ejecutada como
  actualización completa por mandato del dueño (migración +
  auditoría de adopción + fase de mejora encadenada, según
  `rameli/MIGRACIONES.md`). El delta trae solo la doctrina
  de **versionado de aplicaciones** (Rameli,
  `docs/VERSIONADO-APLICACIONES.md`, PR #10): sin cambios
  rompientes, sin mecanismo nuevo y sin cambios de
  comportamiento en ningún skill.
- **Adopción verificada contra el canon** en
  `docs/AUDITORIA-ADOPCION-V0190.md`: la v1.0.0 abierta hoy
  cumple cada regla (semver propio en `rameli.json`,
  CHANGELOG propio, tag anotado sobre el commit que la
  declara, Release verificado como Latest, repo de
  registros sin versionar) — veredicto conforme, sin
  brechas; la fase de mejora no encontró nada que ejecutar.
- **Pin aplicado** en `rameli.json` (con su nota de
  migración), en el frontmatter de los 9 skills y en las 3
  declaraciones vivas «Pineado a Rameli» de los CHANGELOG
  de skill. Registro: `docs/MIGRACION-RAMELI-V0190.md`.
- **Skills incluidos (versiones al cierre):** las mismas de
  v1.0.0 — ningún skill cambió de versión en esta liberación;
  solo cambió su pin del framework.

## v1.0.0 (2026-10-23) — primera versión formal de la aplicación

- **Apertura del versionado propio** (doctrina de Rameli
  v0.19.0, `docs/VERSIONADO-APLICACIONES.md`): hasta hoy la
  aplicación no tenía versión — se nombraba por el pin del
  framework. Esta v1.0.0 fija el estado del sistema que ya
  opera: sistema operativo de print-on-demand × Etsy sobre
  Rameli v0.18.0 (pin, sin cambio), tienda MyNightShiftShop
  vía Printify, con separación de registros (repo privado
  `my-pod-datos`), flujo Printify-first, vitrina de revisión
  de propuestas como superficie única de la Fase A y
  producción por Multi-Product Listings.
- **Skills incluidos (versiones al cierre):**
  conectar-etsy-api 0.1.1 · estratega-pinterest 0.1.4 ·
  estratega-tienda 0.6.1 · onboarding-tienda 0.1.5 ·
  paquete-listing-etsy 0.2.0 · publicador-lote 0.1.6 ·
  publicar-printify-etsy 0.9.1 ·
  puerta-arte-propuesta 0.8.7 · puerta-pinterest-pin 0.4.1.
- **Estado de la instancia al cierre:** los 10 diseños
  aprobados del lote 2026-10-19 existen como borradores MPL
  sin publicar en Printify, a la espera de la revisión de
  ubicación del dueño (Etapa 3).
