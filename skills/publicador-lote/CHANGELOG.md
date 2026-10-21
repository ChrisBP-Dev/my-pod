# CHANGELOG — publicador-lote

## v0.1.6 (2026-10-20)
- Chequeo previo al corte (## Invocación, paso 0): antes de
  resolver el manifiesto, el agente principal lee la ficha de
  la tienda (`data/tiendas/<id>/config.json`) y su
  `registro-flujo.md` y corta el manifiesto EN la puerta de
  aprobación del dueño — solo MPLs unpublished revisados y
  aprobados; un producto suelto nunca vuelto MPL es un
  remanente, no entra y se reporta aparte al cerrar; el
  manifiesto declara su corte. Mecanismo de Rameli v0.15.0
  (el corte en las puertas que la ficha declara); cierra la
  brecha B1 de `docs/AUDITORIA-ADOPCION-V0150.md`.
- Nota de registro: las entradas v0.1.4 (checkpoint en dos
  tiempos por listing) y v0.1.5 (la regla «no regenerar»
  protege videos válidos) no se escribieron en su día en
  este CHANGELOG; sus cambios viven documentados en el
  encabezado de versión del SKILL.md, que es la fuente
  completa de ambas. Este desfase se detectó en esta fase de
  mejora y queda registrado aquí; no se reconstruyen
  entradas retroactivas.

## v0.1.3 (2026-10-19)
- El checkpoint del lote vive en `data/tiendas/<tienda-id>/estado-publicacion.json` (reorden de datos por tienda, 2026-10-19).

## v0.1.2 (2026-10-19)
- Watchdog obligatorio al lanzar el lote: vigilancia programada
  sobre `data/estado-publicacion.json` que despierta al
  orquestador ante freno o fallo en silencio; se retira al cerrar
  el lote (fase de mejora post-v0.11.0, P4; doctrina en
  `docs/EJECUCION-Y-RELEVO.md`).

## v0.1.1 (2026-10-16)
- Enrutamiento API-first hecho explícito: el skill ahora apunta al canon
  `docs/ESTANDAR-ETSY-API-VS-NAVEGADOR.md` y exige la vía API donde
  exista (antes lo heredaba implícitamente de publicar-printify-etsy).

## v0.1.0 (2026-10-16)
- Skill nuevo: formaliza el flujo de publicación post-aprobación (antes
  funcionaba por accidente, sin vehículo diseñado). Un side chat por
  lote aprobado, manifiesto explícito de aprobados (slug+IDs, nunca
  "todo lo pendiente"), pipeline por listing sobre publicar-printify-ety
  M3→M9, P1/P2 de resiliencia, videos en paralelo y nunca regenerados,
  fallos aislados sin bloquear el lote, protocolo de rollback y reporte
  con formato `📦 POD — Publicación · <fecha>`.
