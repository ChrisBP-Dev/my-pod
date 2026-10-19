# CHANGELOG — publicador-lote

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
