# Migración a Rameli v0.12.1 — registro de ejecución (2026-10-19)

Encargo del dueño 2026-10-19: migrar My POD a la última versión
publicada de Rameli, ejecutando la migración completa en el chat
de la migración. Ejecutada en worktree aislado sobre la rama
`migracion-rameli-v0121` (el árbol principal tenía 3 archivos de
`data/` con cambios sin commitear de otros frentes —
`data/config-propuestas.json`, `data/direccion-tienda.md`,
`data/registro-listings.json` — que esta migración no toca),
según `rameli/MIGRACIONES.md` y el CHANGELOG del framework entre
la versión pineada y la objetivo.

**Verificación previa contra los repos (hechos, no memoria):**
- Rameli: `main` en `e4d76f8` = `origin/main`, `VERSION` =
  **0.12.1** (última publicada; tags anotados remotos verificados
  con `ls-remote`: `v0.12.0` y `v0.12.1`, este último sobre
  `e4d76f8`). El CHANGELOG de v0.12.1 declara que sus Releases de
  GitHub retroactivos (v0.8.0 → v0.12.1) quedaron publicados y
  verificados como Latest en su propio cierre; el repo es
  privado y esta VM no tiene `gh` autenticado, así que el Release
  en sí no se re-verificó por API desde aquí — se registra la
  salvedad, no se afirma como verificado en vivo.
- My POD: pineada a **0.11.1** en `rameli.json`; `main` en
  `56d8325` = `origin/main`.
- Delta confirmado con `rameli migrate --to 0.12.1` desde la
  app: v0.12.0 (ruta de lectura por tarea, auditoría de adopción
  obligada en la fase de mejora, delimitación de orquestación) +
  v0.12.1 (parche: el cierre de versión del framework exige
  Release de GitHub). **Sin cambios rompientes; ningún skill
  existente queda en violación** (nota de migración v0.12.0 en
  `rameli/MIGRACIONES.md`).

**Fusión a main: pendiente del dale del dueño** (paso 4 del
proceso del framework), con este registro como resultado
verificado presentado en el chat de la migración. Al fusionar,
la rama se borra (local y remota) y el worktree se retira.

## Alcance aplicado

- `rameli.json`: pin 0.11.1 → 0.12.1 + nota de migración fechada.
- `README.md`: pin y sección de esta migración. La tabla de
  skills se contrastó contra el frontmatter vigente de los 9
  skills: las 9 versiones coinciden (sin correcciones esta vez).
- Los **9 skills**: `framework_version: "0.12.1"` en su
  frontmatter.
- Tres CHANGELOG de skill cuya línea viva declara el pin
  ("Pineado a Rameli v0.11.1") actualizados a v0.12.1
  (puerta-arte-propuesta, puerta-pinterest-pin,
  estratega-pinterest). Las entradas fechadas de los demás
  CHANGELOG son historia y no se tocaron.
- Registro de adopción del delta (sección siguiente).
- El gemelo máquina de la ficha de la tienda (`config.json`) NO
  cambió. **Ningún dato se tocó: el diff de la rama contiene
  0 archivos bajo `data/`.**

## Registro de adopción — delta v0.12.0 / v0.12.1

La nota de migración v0.12.0 manda: adopción = proceso general
(pin, regresión comparada, registro de adopción); ningún skill
queda en violación.

**Delimitación de orquestación (PR #5) — ADOPTADA, ya declarada:**
la app ya declara la doctrina única de workers fríos y presenta
la Pieza 4 como capacidades disponibles del entorno, "no una
doctrina rival ni una alternativa", en su doc vivo
`docs/DELIMITACIONES-ADOPCION.md` §2 (reescrito el 2026-10-19
por corrección del dueño, antes de que el framework integrara la
delimitación). Verificado por barrido: ningún **registro vivo**
de adopción presenta la Pieza 4 como camino rival. La auditoría
histórica `docs/AUDITORIA-ADOPCION-V0110.md` conserva en su
tabla de cierre la redacción de su época ("no-adopción
deliberada de las primitivas") — es historia fechada, no se
toca; el doc vivo que manda es DELIMITACIONES §2.

**Ruta de lectura por tarea (PR #3) — NO adoptada aún; pasa a la
fase de mejora:** la app no declara todavía una ruta de lectura
en su doc de flujo (verificado: ninguna sección de ruta en
`FLUJO-PIPELINE.md` ni en otro doc vivo; el canon manda
punteros puros en el doc de flujo propio, no contenido). La
auditoría anterior ya fijó el destino de adopción: agregar la
ruta por flujo a `FLUJO-PIPELINE.md`
(`docs/AUDITORIA-ADOPCION-V0110.md`, nota tras B8: "si el PR #3
se integra, la ruta de lectura por flujo se adopta entonces" —
el PR #3 se integró en v0.12.0). Adoptarla es un cambio de
documentación de flujo con cobertura que verificar (todo skill
vivo en alguna ruta, todo puntero resolviendo): pertenece a la
fase de mejora, no a esta migración de alcance cerrado.

**Auditoría de adopción obligada (PR #4) — ADOPTADA como
proceso, con su cobro fijado:** esta migración cierra abriendo
la fase de mejora cuyo **primer insumo es la auditoría de
adopción completa** (matriz capacidades vigentes × flujos, con
evidencia en el repo por celda). Para esta migración **NO es
diferible**: el delta trae capacidades nuevas (así lo exige la
nota v0.12.0, y la matriz debe incluir expresamente la ruta de
lectura — ¿declarada en el doc de flujo?, ¿cubre todos los
skills vivos? — y la delimitación de orquestación — ¿algún
registro presenta la Pieza 4 como camino rival?).

**Parche v0.12.1 (PR #6) — SIN EFECTO en la app:** regla del
cierre de versiones del propio framework (tag + Release
verificado como Latest). La app no publica versiones propias con
ese mecanismo; se registra solo como parte del delta migrado.

## Verificación (antes vs después, mismo árbol: el worktree)

- `rameli lint` sobre los 9 skills: **VERDE total** antes y
  después; salidas **idénticas byte a byte** (diff vacío). La
  migración introduce cero fallos nuevos y no hereda fallos: la
  fase de mejora post-v0.11.0 ya había llevado el lint a cero.
- Regresión (`rameli test`): **VERDE total** antes y después;
  salidas **idénticas byte a byte** — 13 ok / 0 fallas, 4 ok /
  0 fallas, 2 ok / 0 fallas, 13 ok / 0 fallas, 15 ok / 0 fallas
  (47 ok en total), con los 3 avisos preexistentes de skills sin
  `evals/` (conectar-etsy-api, estratega-pinterest,
  onboarding-tienda) y publicador-lote con suite parcial. Sin la
  divergencia worktree/árbol principal de migraciones anteriores:
  la portabilidad del registro (fase de mejora post-v0.11.0, P3)
  hace que la suite de Pinterest dé 15/15 también en el worktree.
- La misma corrida sobre el árbol principal (ANTES, con los
  datos vivos) dio el mismo resultado: lint VERDE total,
  regresión VERDE total.
- Barrido final de pin viejo: `0.11.1` solo queda citando el
  delta o como historia — la nota fechada de `rameli.json`, la
  línea del delta y la sección histórica "Migración a Rameli
  v0.11.1" del README, el doc histórico
  `docs/AUDITORIA-ADOPCION-V0110.md` y el registro
  `docs/MIGRACION-RAMELI-V0110.md`. Ninguna declaración viva
  queda en 0.11.1.

## Huecos del sistema detectados

Ninguno nuevo en el proceso: MIGRACIONES.md trae la nota de
adopción de v0.12.0 explícita, el delta salió completo de
`rameli migrate` y del CHANGELOG, y el precedente inmediato
(pin 0.11.1 vía auditoría) fijó la forma de las declaraciones
vivas. La única salvedad registrada es la de arriba: el Release
de GitHub de v0.12.1 no se pudo re-verificar por API desde esta
VM (repo privado, `gh` sin autenticar); consta por el propio
CHANGELOG del framework y por el tag anotado remoto.

## Fase de mejora — se abre al cerrar esta migración

Como manda `rameli/MIGRACIONES.md`, al fusionar esta migración
se abre sola la fase de mejora: su primer insumo es la
**auditoría de adopción completa (no diferible en esta
migración)**, y su primer entregable es la PROPUESTA al dueño —
qué cambia, impacto, riesgo y orden. **Nada se ejecuta sin su
dale aparte**, y con dale corre como fase propia. Insumos ya
conocidos que la auditoría debe cobrar:

- **Ruta de lectura por tarea:** adoptarla en
  `FLUJO-PIPELINE.md` (punteros puros; cobertura: los 9 skills
  vivos en alguna ruta, todo puntero resolviendo) o declarar el
  motivo si se difiere.
- **Inventario arrastrado:** lo que la fase de mejora
  post-v0.11.0 haya dejado diferido o rechazado reaparece aquí
  por la regla del framework (propuestas registradas en
  `docs/FASE-MEJORA-V0110-PROPUESTA.md` y
  `docs/AUDITORIA-ADOPCION-V0110.md`), sin asumirse resuelto.
- Lint y regresión parten de **cero fallos**: la auditoría no
  hereda deuda de puertas; sus brechas serán de adopción, no de
  formato.
