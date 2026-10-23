# Migración a Rameli v0.19.0 — actualización completa (2026-10-23)

> Actualización oficial de la app a **Rameli v0.19.0**,
> ejecutada como **actualización completa** por mandato
> del dueño (2026-10-23, desde el chat de Su Voluntad
> P-18: «la actualización de My POD a la versión más
> reciente del framework, Rameli v0.19.0, y todo lo que
> conlleva», en este chat). Bajo ese mandato la operación
> es una sola: migración → auditoría de adopción →
> propuesta de fase de mejora → ejecución, con las
> decisiones delegadas registradas; las **puertas de
> merge** se piden al dueño en este chat con la evidencia
> lista, como manda `rameli/MIGRACIONES.md`.
> Auditoría de adopción: `docs/AUDITORIA-ADOPCION-V0190.md`
> (veredicto: conforme, sin brechas).

## Paso 0 — guardas e inventario

- **Precondición verificada antes de empezar:** Rameli
  **v0.19.0 publicado** — repo `rameli` en `dad390b`
  (cierre de versión, PR #10 fusionado en `fa9455a`),
  `VERSION` = 0.19.0, tag anotado `v0.19.0` presente en el
  remoto (`git ls-remote`, deref a `dad390b`), Release de
  GitHub v0.19.0 verificado como Latest por API en su
  corrida de cierre (2026-10-23).
- **Línea base (sobre `main` en `c95fe72`, pin 0.18.0):**
  `rameli validar` **0 fallos, 0 avisos**; lint **VERDE**
  total; regresión **53 casos, 0 fallas** (13+4+3+18+15),
  con los 4 avisos preexistentes de skills sin `evals/`.
  El archivo sin trackear de otro trabajo
  (`tmp/paso1-investigacion-personalizacion.md`) se
  preserva intacto.
- **Sin tocar la operación comercial:** nada de listings,
  precios, ofertas ni Printify/Etsy se modificó en esta
  unidad. Nada de media ni de registros se borró. Sin
  servicios pagos nuevos.

## La migración a v0.19.0 (delta y adopción)

- **Delta 0.18.0 → 0.19.0** (del `CHANGELOG.md` de Rameli
  y `docs/VERSIONADO-APLICACIONES.md`): una sola cosa —
  la **doctrina de versionado de aplicaciones** (semver
  propio `app_version`, `CHANGELOG.md` de la app, cierre
  con tag anotado + Release verificado como Latest; los
  repos de registros no se versionan; primera versión =
  v1.0.0). **Sin cambios rompientes, sin mecanismo nuevo
  y sin cambios de comportamiento**: el propio canon
  declara que «el pin del framework no se toca» para
  adoptar la doctrina — el pin se mueve aquí porque esta
  unidad ES la migración ordinaria de la app a la versión
  vigente, no porque la doctrina lo exija.
- **Adopción previa (de hecho, 2026-10-23):** My POD ya
  había abierto su línea propia — `app_version: 1.0.0`,
  `CHANGELOG.md`, tag anotado `v1.0.0` sobre `c95fe72` y
  Release verificado como Latest. La auditoría de esta
  unidad la verificó contra el canon: **conforme, sin
  brechas** (matriz en `docs/AUDITORIA-ADOPCION-V0190.md`).
- **Adopción — pin 0.19.0:** `rameli.json`
  (`framework_version` + nota de migración), los **9
  frontmatter** de skills y las **3 líneas vivas** «Pineado
  a Rameli» en los CHANGELOG de skill (`estratega-pinterest`,
  `puerta-arte-propuesta`, `puerta-pinterest-pin`), más la
  sección nueva del `README.md`.

## Puertas — antes / después

| Puerta | Antes (main, pin 0.18.0) | Después (rama, pin 0.19.0) |
|---|---|---|
| `rameli validar` | 0 fallos, 0 avisos | 0 fallos, 0 avisos |
| `rameli lint` (9 skills) | VERDE total | VERDE total |
| `rameli test` (9 skills) | 53 casos, 0 fallas | **53 casos, 0 fallas** (13+4+3+18+15), REGRESIÓN VERDE, mismos 4 avisos preexistentes |

Sin regresión atribuible al pin: el delta no cambia
comportamiento y las puertas deben quedar idénticas a la
línea base.

## Fase de mejora (encadenada, actualización completa)

- **Propuesta:** sin brechas que ejecutar — la auditoría
  no encontró ninguna. Los 4 avisos de `rameli test`
  (skills sin suite en `evals/`) no son una brecha de
  este delta ni un pendiente diferido: son declaraciones
  «sin suite — motivo» adoptadas al ejecutar la
  Propuesta 2 de la auditoría v0.11.0 (2026-10-19), y esta
  unidad las **revalidó una por una con evidencia** a
  pregunta del dueño (los 4 motivos siguen vivos;
  registro completo en `docs/AUDITORIA-ADOPCION-V0190.md`,
  § fase de mejora). El otro insumo es la mejora futura
  del lado del framework que el propio canon difiere (que
  `rameli validar` compruebe `app_version`/CHANGELOG).
- **Decisión:** registrada en la auditoría — fase de
  mejora **sin ejecución** por falta de objeto, no por
  omisión. Nada queda pendiente disfrazado de cierre.

## Liberación de la app — My POD v1.1.0

Según el canon nuevo, la migración sin rompientes se
libera como **MENOR**:

- `app_version` → **1.1.0** en `rameli.json` (en esta
  rama) y entrada **v1.1.0** en el `CHANGELOG.md` de la
  app, con las notas de esta migración.
- Tras el **dale de puerta** del dueño en el chat de la
  unidad: merge de `migracion-rameli-v0190` a `main`,
  push verificado, tag anotado **v1.1.0** sobre el commit
  de merge, Release de GitHub desde ese tag verificado
  como **Latest**, y borrado de la rama (local + remota).

_(Cierre: se completa con los hashes y la verificación
final cuando la puerta se ejecute.)_
