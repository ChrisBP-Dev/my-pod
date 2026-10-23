# Auditoría de adopción — My POD × Rameli v0.19.0 (2026-10-23)

> Pieza de la actualización completa a Rameli v0.19.0
> (mandato del dueño, 2026-10-23). El delta 0.18.0 → 0.19.0
> trae una sola capacidad nueva — la doctrina de
> **versionado de aplicaciones** (`rameli/docs/
> VERSIONADO-APLICACIONES.md`, PR #10) — así que esta
> auditoría verifica la **conformidad** de la adopción que
> My POD ya hizo de hecho hoy (su v1.0.0) contra ese canon,
> celda por celda y con evidencia en el repositorio. No
> rehace la adopción ni re-audita capacidades que el delta
> no tocó: el `CHANGELOG.md` de Rameli entre v0.18.0 y
> v0.19.0 se leyó completo y no contiene ningún otro cambio
> (sin rompientes, sin mecanismo, sin comportamiento).
> Registro de la unidad: `docs/MIGRACION-RAMELI-V0190.md`.

## Bases verificadas (en vivo, 2026-10-23)

- **Framework:** repo `rameli`, `VERSION` = **0.19.0**,
  commit de cierre `dad390b`; tag anotado `v0.19.0`
  verificado por `git ls-remote` (objeto `877d07f…`,
  deref a `dad390b`); Release de GitHub v0.19.0 verificado
  como Latest por API (registro del 2026-10-23 en la
  crónica del proyecto).
- **Aplicación al abrir:** repo `my-pod`, `main` en
  `c95fe72` (el commit de la v1.0.0), pin **0.18.0**,
  `app_version` **1.0.0**; rama de la unidad:
  `migracion-rameli-v0190`.
- **Línea base (sobre `main`, antes del pin):** `rameli
  validar` **0 fallos, 0 avisos**; `rameli lint` **VERDE**
  total; `rameli test` **53 casos, 0 fallas**
  (13+4+3+18+15 — idéntica a la línea base de la migración
  a v0.18.0), con los 4 avisos preexistentes de skills sin
  `evals/` (conectar-etsy-api, estratega-pinterest,
  onboarding-tienda, publicador-lote).
  El archivo sin trackear de otro trabajo
  (`tmp/paso1-investigacion-personalizacion.md`) se
  preserva intacto.

## Matriz — canon de versionado de aplicaciones × My POD

| # | Regla del canon (VERSIONADO-APLICACIONES.md) | Veredicto | Evidencia |
|---|---|---|---|
| 1 | Semver propio en la raíz de `rameli.json` (`app_version`), independiente del pin y de los skills | **Adoptado y probado** | `rameli.json`: `"app_version": "1.0.0"` junto a `"framework_version": "0.18.0"` — dos claves distintas, el pin sin cambio al abrir la línea, como declara la entrada v1.0.0 |
| 2 | `CHANGELOG.md` de la aplicación en la raíz del repo del sistema: una entrada por versión, la más nueva primero, con fecha y notas | **Adoptado y probado** | `CHANGELOG.md` en la raíz: entrada `v1.0.0 (2026-10-23)` con notas y el caso (apertura del versionado propio); es la única y por tanto la primera |
| 3 | Cierre de versión = tag anotado `vX.Y.Z` sobre el commit de `main` que la declara, empujado y verificado contra el remoto | **Adoptado y probado** | `git cat-file -t v1.0.0` = `tag` (anotado, 2026-10-23 07:24 -0400, «My POD v1.0.0 — primera versión formal de la aplicación»); `v1.0.0^{}` = `c95fe72` = HEAD de `main`, el commit que declara `app_version`; `git ls-remote` confirma el tag en el remoto apuntando a ese commit |
| 4 | Release de GitHub publicado desde ese tag y verificado como **Latest** | **Adoptado y probado** | Release «v1.0.0 — Primera versión formal de My POD» publicado y verificado como Latest vía API de GitHub el 2026-10-23 (registro de la corrida de apertura; el CLI `gh` no está autenticado en la VM, la verificación fue por el conector de GitHub) |
| 5 | Semántica: MAYOR rompiente / MENOR capacidad nueva o migración sin rompientes / PARCHE correcciones; se libera en los cierres, no por cada bump de skill; las notas citan los bumps incluidos | **Adoptado y probado** | La entrada v1.0.0 cita los 9 skills con su versión; verificado en vivo: los 9 coinciden uno a uno con el `version:` real de cada frontmatter (0.1.1 · 0.1.4 · 0.6.1 · 0.1.5 · 0.2.0 · 0.1.6 · 0.9.1 · 0.8.7 · 0.4.1). La liberación de esta migración aplica la misma semántica: sin rompientes = **MENOR → v1.1.0** |
| 6 | Los repos de registros no se versionan | **Adoptado y probado** | `git tag -l` en `~/workspace/my-pod-datos` = vacío; su `main` sigue su ciclo continuo escribir = commitear |
| 7 | Primera versión de una app que ya opera = **v1.0.0** | **Adoptado y probado** | La línea se abrió en v1.0.0 (no en 0.x): el sistema que ya opera, como manda el canon |

## Veredicto

**Conforme, sin brechas.** La adopción de hecho del
2026-10-23 cumple las siete reglas del canon tal como
quedaron escritas en Rameli v0.19.0. Nada que rehacer,
nada que corregir.

## Fase de mejora — insumos y decisión (actualización completa)

Insumos revisados bajo el mandato de actualización
completa (la orden del dueño ES el dale de la operación;
las decisiones quedan registradas aquí):

- **Brechas de adopción:** ninguna (matriz de arriba).
- **Fallos vigentes de lint/regresión:** ninguno; las
  puertas quedan idénticas a la línea base tras el pin
  (ver `docs/MIGRACION-RAMELI-V0190.md`).
- **Avisos preexistentes:** 4 skills sin `evals/`
  señalados por `rameli test` (conectar-etsy-api,
  estratega-pinterest, onboarding-tienda,
  publicador-lote). Son el estado heredado ya
  registrado en auditorías anteriores, no un efecto de
  este delta; crear sus evals es trabajo de capacidad de
  cada skill, no de esta migración. Queda **inventariado**
  para la siguiente fase de mejora ordinaria — no se
  mezcla con esta unidad (alcance cerrado de migración).
- **Mejora futura que el propio canon nombra:** que
  `rameli validar` compruebe `app_version` y CHANGELOG —
  el canon la deja «fuera de esta contribución» y es del
  lado del framework, no de esta aplicación. Sin acción
  aquí; si el dueño la quiere, va por el circuito de
  contribuciones de Rameli.

**Decisión (delegada por el mandato, registrada):**
propuesta de fase de mejora = **sin ejecución** — no hay
brechas que cerrar ni deuda nueva que este delta haya
creado. La actualización completa queda completa con la
migración y su liberación v1.1.0; no queda fase pendiente
disfrazada de cierre.
