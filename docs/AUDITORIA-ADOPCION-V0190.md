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
- **Avisos de `rameli test` — 4 skills sin suite en
  `evals/`, REVALIDADOS en esta unidad (2026-10-23, a
  pregunta del dueño):** conectar-etsy-api,
  estratega-pinterest, onboarding-tienda y
  publicador-lote no tienen suite determinista. No es un
  olvido ni una validación ausente: los 9 skills pasan
  `rameli lint` y `rameli validar`; lo que estos 4 no
  tienen es **regresión automática**, y su estado es una
  **decisión registrada**, no un arrastre:
  - **Historia:** la auditoría de adopción v0.11.0
    (2026-10-19) lo cazó como brecha **B2** — entonces
    eran 7 los afectados y dos declaraban una suite que
    estaba vacía (declaración sin sostén). Su Propuesta 2
    se **ejecutó** (commit `407522a`): suites reales para
    paquete-listing-etsy, publicar-printify-etsy y
    estratega-tienda (contrato), y para estos 4, la
    opción (b) de la propuesta: **declaración explícita
    de «sin suite — motivo»** en la sección «Regresión»
    de cada SKILL.md. El validador del framework trata la
    ausencia como **AVISO, no FALLO** (`bin/rameli`: sin
    `evals/` → aviso y sigue), en tensión conocida con la
    regla dura de `docs/formato-skills.md` («sin evals,
    el skill no se acepta»): la declaración motivada es la
    salida que el sistema adoptó.
  - **Revalidación de los 4 motivos (evidencia de hoy):**
    (1) *conectar-etsy-api* — el flujo sigue siendo
    interactivo (OAuth con clic del dueño, tokens que
    rotan); su cobertura declarada es la verificación en
    vivo de cada conexión. Motivo **vivo**.
    (2) *estratega-pinterest* — su salida sigue siendo
    una decisión (la parrilla); lo mecánico lo cubre la
    suite de `puerta-pinterest-pin`, corrida hoy: **15/15**.
    Motivo **vivo**. (3) *onboarding-tienda* — playbook
    guiado con el dueño; su «suite» declarada es la Fase 6
    (verificación y cierre contra la tienda real), que
    existe y está vigente en el skill (§ «Fase 6»).
    Motivo **vivo**. (4) *publicador-lote* — orquesta
    sistemas externos vivos; su verificación declarada es
    el pipeline por listing con las puertas de
    `publicar-printify-etsy`, cuya suite existe y corrió
    hoy (3 casos, dentro de los 53). Motivo **vivo**.
  - **Corrección de esta auditoría:** la primera versión
    de este documento trató los 4 avisos como «estado
    heredado» y los **difirió** a la siguiente fase sin
    traer su historia ni revalidar sus motivos —
    exactamente el patrón que la doctrina prohíbe
    (inventariar sin cerrar). Corregido en la misma rama,
    antes del merge: la deuda no es «crear las suites»
    (eso lo decidió la Propuesta 2 con evidencia), es
    **revalidar las declaraciones cuando una auditoría
    las toca** — hecho aquí. Si un motivo muere (un skill
    gana una parte determinista, como el propio
    conectar-etsy-api anticipa en su declaración), la
    suite nace en esa sesión.
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
