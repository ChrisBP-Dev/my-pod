# Migración a Rameli v0.14.0 — registro de ejecución (2026-10-19)

Encargo del dueño 2026-10-19, vía el orquestador de la sesión:
migrar My POD de Rameli v0.12.1 a v0.14.0 cerrando el flujo
completo de `rameli/MIGRACIONES.md`, con autorización para
fusionar la rama a `main` SOLO si las puertas comparadas
(lint y regresión, antes/después) y el registro quedan como
manda el sistema. Ejecutada en worktree aislado sobre la rama
`migracion-rameli-v0140`, desde `main` en `1e73e16` (árbol
limpio, `main == origin/main`, una sola rama y un solo
worktree al abrir — verificado, no de memoria).

**Fusión a main: ejecutada el 2026-10-19 bajo la
autorización del encargo** (fusionar SOLO si las puertas
comparadas y el registro quedan como manda el sistema —
cumplido: lint y regresión idénticos byte a byte, verdes):
antes de fusionar se re-verificó que `main` no se hubiera
movido (seguía en `1e73e16`, árbol limpio, pese a los crons
de la app que commitean sobre `main`); fast-forward
`1e73e16 → 77a7243`, pin 0.14.0 verificado en el árbol
principal tras la fusión. Rama borrada (local y remota) y
worktree retirado al cerrar, verificado con `git status` y
`git branch -a`. Verificación post-fusión: sección al final
de «Verificación».

**Verificación previa contra los repos (hechos, no memoria):**
- Rameli: `main` en `6c478f3` = `origin/main`, `VERSION` =
  **0.14.0** (última publicada; tags anotados remotos
  verificados con `ls-remote`: `v0.13.0` sobre `17aea91` y
  `v0.14.0` sobre `6c478f3`). Los Releases de GitHub de estas
  versiones no se re-verificaron por API desde esta VM (repo
  privado, `gh` sin autenticar) — se registra la salvedad,
  como en la migración anterior; consta el tag remoto.
- My POD: pineada a **0.12.1** en `rameli.json`; `main` en
  `1e73e16` = `origin/main`. Ese commit ya declara el mapa
  de datos (clave `datos`) que el estándar de v0.14.0 pide:
  esta migración lo registra como **adopción, no lo re-decide**
  (el mapa no se tocó).
- Delta confirmado con `rameli migrate --to 0.14.0` desde la
  app: v0.13.0 (validación de colocación: comando
  `rameli validar` + protocolo de cierre con registro) +
  v0.14.0 (estándar de datos multi-unidad +
  chequeo 4 de `rameli validar`). **Sin cambios rompientes;
  ningún skill existente queda en violación** (notas de
  migración v0.13.0 y v0.14.0 en `rameli/MIGRACIONES.md`).

## Alcance aplicado

- `rameli.json`: pin 0.12.1 → 0.14.0 + nota de migración
  fechada. La clave `datos` queda **intacta**.
- `README.md`: pin y sección de esta migración. La tabla de
  skills se contrastó contra el frontmatter vigente de los 9
  skills: las 9 versiones coinciden (sin correcciones).
- Los **9 skills**: `framework_version: "0.14.0"` en su
  frontmatter.
- Tres CHANGELOG de skill cuya línea viva declara el pin
  ("Pineado a Rameli v0.12.1") actualizados a v0.14.0
  (puerta-arte-propuesta, puerta-pinterest-pin,
  estratega-pinterest). Las entradas fechadas de los demás
  CHANGELOG son historia y no se tocaron.
- Registro de adopción del delta (sección siguiente) +
  primera corrida registrada de `rameli validar` con su
  protocolo de cierre (sección de verificación).
- El gemelo máquina de la ficha de la tienda (`config.json`)
  NO cambió. **Ningún dato se tocó: el diff de la rama
  contiene 0 archivos bajo `data/` y 0 cambios al mapa
  `datos`.** Nada se tocó fuera del repo (ni Etsy, ni
  Printify, ni Pinterest, por API ni por navegador).

## Registro de adopción — delta v0.13.0 / v0.14.0

Las notas de migración mandan: adopción = proceso general
(pin, regresión comparada, registro de adopción); ningún
skill queda en violación. Este delta trae capacidades
nuevas, así que la **auditoría de adopción NO es diferible**:
se corrió como primer insumo de la fase de mejora que esta
migración abre (`docs/AUDITORIA-ADOPCION-V0140.md`) y su
primer entregable es la propuesta
(`docs/FASE-MEJORA-V0140-PROPUESTA.md`).

**Validación de colocación (v0.13.0) — ADOPTADA y estrenada
en este cierre:** el comando `rameli validar <dir-app>` se
corrió antes y después (resultado clasificado abajo) y el
protocolo de cierre con registro se cumple con la sección
«Validación de colocación — registro de cierre» de este
documento (inventario de herramientas de la fase + prueba de
frío por escrito). Los hallazgos **no bloquean la
migración** (alcance cerrado, como manda la nota v0.13.0):
alimentan la fase de mejora.

**Datos multi-unidad (v0.14.0) — ADOPTADO, con el mapa ya
declarado:** la app declara en `rameli.json → datos` su
raíz (`data`), sus unidades (`data/tiendas`), el hogar
requerido por tienda (`config.json`,
`registro-listings.json`, `ledger-ventas.json`,
`direccion-tienda.md`), sus globales y su historial
(`data/auditoria-2026-10-15`) — declaración hecha en el
commit `1e73e16`, durante la construcción de la versión del
framework, y registrada aquí como adopción. Verificación del
chequeo 4 en la primera corrida (abajo): **sin hallazgos** —
hogar de la única tienda completo (4/4 requeridos), ningún
código en el espacio de datos, ninguna entrada de la raíz
sin declarar. La fila de datos multi-unidad entra a la
matriz de la auditoría de adopción, como manda la nota
v0.14.0.

**`rameli init` con esqueleto `datos` (acompañante de
v0.14.0) — NO APLICA a esta app:** es la vía de nacimiento
de apps nuevas; esta app ya declara su mapa completo.

## Verificación (antes vs después)

Antes = árbol principal sobre `main` (`1e73e16`, pin
0.12.1); después = worktree de la rama, mismo contenido
salvo el delta de la migración.

- `rameli lint` sobre los 9 skills: **VERDE total** antes y
  después; salidas **idénticas byte a byte** (diff vacío).
- Regresión (`rameli test`): **VERDE total** antes y
  después; salidas **idénticas byte a byte** — 48 casos ok /
  0 fallas (estratega-tienda 13, paquete-listing 4,
  publicar-printify-etsy 3, puerta-arte-propuesta 13,
  puerta-pinterest-pin 15), con los avisos preexistentes de
  skills sin `evals/` (conectar-etsy-api, estratega-pinterest,
  onboarding-tienda, publicador-lote — los cuatro con su
  declaración explícita en su `SKILL.md`, como cerró la fase
  post-v0.11.0). Las corridas se hicieron con `TMPDIR`
  propio fuera de `/tmp`: **0 crecimiento de temporales**
  (la fuga de `verificar-video.py` sigue cerrada).

### `rameli validar` — primera corrida registrada, resultado clasificado

Corrida con el framework v0.14.0 sobre la app (antes, pin
0.12.1; el comando no depende del pin):

```
AVISO: scripts/procesar-arte-propuesta.py: script de app no nombrado en ningún SKILL.md ni doc vivo
AVISO: scripts/reparar-fondo-casi-blanco.py: script de app no nombrado en ningún SKILL.md ni doc vivo
AVISO: scripts/reporte-seo.py: script de app no nombrado en ningún SKILL.md ni doc vivo
FALLO: skills/puerta-arte-propuesta/evals/test-regression.sh:6: la variable K apunta fuera del repo
       ($HOME/workspace/goals/pod-etsy-sistema-operativo-q4-2026/files/disenos/canonicos):
       los insumos de calibración viven dentro del repo
validar: 1 fallos, 3 avisos en 9 skills de my-pod — ROJO: colocación no verificada
```

Clasificación (protocolo de `rameli/docs/VALIDACION-COLOCACION.md`):

| # | Hallazgo | Clase | Destino |
|---|---|---|---|
| 1 | **Chequeo 3 — FALLO:** la suite de arte lee el diseño canónico `vitals-stable-print-300dpi.png` desde `$HOME/.../disenos/canonicos` (variable `K`, casos P1 y F6), fuera del repo | Hallazgo vigente ya conocido (registrado en `rameli/MIGRACIONES.md` al integrar v0.13.0). **Decisión vigente del dueño: insumo de la fase de mejora — en esta migración NO se mueve ningún archivo de diseño** | Fase de mejora: brecha **B1** de la auditoría, propuesta **P1** con opciones |
| 2 | **Chequeo 1 — 3 AVISOS:** `scripts/procesar-arte-propuesta.py`, `scripts/reparar-fondo-casi-blanco.py` y `scripts/reporte-seo.py` no están nombrados en ningún `SKILL.md` ni doc vivo | No son entradas de cron (verificado: ningún cron de la app los nombra) ni código huérfano: son herramientas reales con uso registrado en git (2026-10-16/17) que viven en su casa correcta (`scripts/` compartidos de la app). La brecha es de **declaración**, no de colocación: un chat frío no las descubre desde el sistema | Fase de mejora: brecha **B2**, propuesta **P2** |
| 3 | **Chequeo 4 — SIN hallazgos** sobre el árbol principal: hogar completo, sin código en datos, sin entradas sin declarar | El estándar de datos multi-unidad (v0.14.0) se verifica en verde en su primera corrida | Adoptado (ver adopción arriba) |
| 4 | **Chequeo 2 — SIN hallazgos:** ninguna declaración muerta en los documentos vivos de los 9 skills | — | — |

Nota de corrida en el worktree: la corrida «después» dio el
mismo FALLO y los mismos 3 avisos, **más un cuarto aviso** —
`data/cola-pins: declarado en el mapa de datos pero no
existe`. Es un artefacto del worktree, verificado:
`data/cola-pins/` es un directorio vacío cubierto por
`.gitignore` (la cola local de pins), existe en el disco del
árbol principal pero no en git, así que un clon o worktree
nuevo nace sin él. No es una divergencia de la migración; sí
es un matiz real del mapa (una declaración que un clon frío
no puede satisfacer hasta que el flujo crea el directorio),
y queda registrado como brecha menor **B3** de la auditoría
con sus opciones — **el mapa no se re-decide en esta
migración**.

- Barrido final de pin viejo: `0.12.1` solo queda citando el
  delta o como historia — la nota fechada de `rameli.json`,
  la sección histórica «Migración a Rameli v0.12.1» del
  README, los docs históricos de la migración y la
  auditoría v0.12.1, y dos comentarios fechados de código
  (`scripts/verificar-video.py`,
  `skills/publicar-printify-etsy/evals/test-regression.sh`,
  que nombran la fase de mejora v0.12.1 que los originó).
  Ninguna declaración viva queda en 0.12.1.

### Verificación post-fusión (sobre `main`, tras el fast-forward)

- `rameli lint`: **VERDE total, idéntico byte a byte** al
  antes/después de la rama.
- Regresión (`rameli test`): **VERDE total (48 casos),
  idéntica byte a byte**, con `TMPDIR` propio y 0 fuga de
  temporales.
- `rameli validar`: **1 FALLO, 0 avisos** — el mismo FALLO
  del chequeo 3 (B1, sin cambio), pero los 3 avisos del
  chequeo 1 **ya no se reproducen en `main` fusionado**.
  Causa verificada en el código del validador: su corpus de
  «documentos vivos» es `README.md` + todo `docs/*.md` +
  los `SKILL.md`, y los documentos de esta migración y su
  auditoría **nombran** a los tres scripts — con eso la
  capa mecánica los da por nombrados. Esto **no cierra B2**:
  la brecha sustantiva es que ningún skill gobernante ni la
  ruta de lectura los declara (un chat frío que sigue la
  ruta sigue sin encontrarlos); solo significa que la señal
  mecánica quedó enmascarada por el propio registro.
  Queda anotado en la brecha B2 y en la verificación de la
  propuesta P2: su cierre se comprueba contra el skill y la
  ruta, no contra la salida de `rameli validar`.

## Validación de colocación — registro de cierre (protocolo v0.13.0)

**Inventario de herramientas de esta fase:** qué se usó como
puerta o mecanismo, y dónde vive cada cosa.

| Herramienta / medición | Uso en esta fase | Dónde vive |
|---|---|---|
| `rameli lint` | Puerta de formato, antes/después | Framework: `rameli/bin/rameli` + `rameli/skills/fabrica-skills/scripts/verificar-skill.sh` — fuera del repo de la app **por ser el framework pineado**, declarado en `rameli.json` y en la ruta de lectura F9 |
| `rameli test` | Regresión comparada | Ídem; las suites viven en `skills/*/evals/` de la app |
| `rameli validar` | Puerta de colocación, antes/después | Framework: `rameli/skills/fabrica-skills/scripts/verificar-colocacion.py` |
| `rameli migrate --to 0.14.0` | Delta entre versiones | Framework (`bin/rameli`) |
| `git worktree` / `git` | Rama aislada y cierre verificado | Entorno (sistema), sin artefactos propios |
| Edición del pin (script puntual) | Reemplazo mecánico de `framework_version` y líneas de pin | Corrida efímera sin archivo: no es puerta ni mecanismo, no calibra nada y no queda nada que archivar |

Ninguna herramienta de esta fase vive en el entorno del
asistente fuera de los dos repos (framework + app). Las
salidas de las puertas se guardaron en `/tmp` solo como
evidencia de trabajo de la corrida; **ningún artefacto que
calibre vive ahí**: los veredictos y las salidas de
`rameli validar` quedan transcritos en este registro.

**Prueba de frío (por escrito):** ¿puede otra IA, con solo
el repo (app + framework pineado), ejecutar el flujo que
esta fase tocó? **Para la migración, sí:** el proceso sale
de `rameli/MIGRACIONES.md` + CHANGELOG + `rameli migrate`,
y esta app ya lo demostró en cuatro migraciones seguidas.
**Con una excepción conocida y registrada:** la suite de
arte no es fría — sus casos P1 y F6 leen el diseño canónico
desde una ruta `$HOME` fuera de ambos repos (hallazgo #1,
brecha B1). En esta VM pasa porque esa ruta existe; en un
clon frío fallaría. Esa es exactamente la deuda que la fase
de mejora cobra con su propuesta P1. Los 3 scripts sin
declarar (hallazgo #2) son la segunda deuda de frío: existen
y funcionan, pero el sistema no los presenta.

**Artefactos que calibran:** ningún set dorado, referencia
ni medición nueva se creó en esta fase. El único artefacto
de calibración en juego es preexistente — el diseño
canónico de la suite de arte — y su colocación fuera del
repo es el hallazgo #1, no un hecho nuevo de esta corrida.

## Huecos del sistema detectados

Ninguno nuevo en el proceso: `MIGRACIONES.md` trae las notas
de adopción de v0.13.0 y v0.14.0 explícitas, el delta salió
completo de `rameli migrate` y del CHANGELOG, y la forma de
las declaraciones vivas viene fijada por las migraciones
anteriores. La única salvedad registrada es la de arriba:
los Releases de GitHub de v0.13.0/v0.14.0 no se pudieron
re-verificar por API desde esta VM (repo privado, `gh` sin
autenticar); constan los tags anotados remotos.

## Fase de mejora — se abre al cerrar esta migración

Como manda `rameli/MIGRACIONES.md`, al fusionar esta
migración se abre sola la fase de mejora: su primer insumo
es la **auditoría de adopción completa (no diferible en
esta migración)**, corrida y registrada en
`docs/AUDITORIA-ADOPCION-V0140.md`, y su primer entregable
es la PROPUESTA al dueño, en
`docs/FASE-MEJORA-V0140-PROPUESTA.md` — qué cambia, impacto,
riesgo y orden. **Nada se ejecuta sin su dale aparte**, y
con dale corre como fase propia. Insumos que la auditoría
cobra:

- **B1 (chequeo 3):** la suite de arte lee diseños canónicos
  desde fuera del repo — con sus opciones; en esta
  migración no se movió ningún archivo de diseño.
- **B2 (chequeo 1):** los 3 scripts de `scripts/` sin
  declarar en ningún documento vivo.
- **B3 (chequeo 4, menor):** `data/cola-pins` declarado en
  el mapa pero inexistente en un clon frío (directorio
  vacío gitignored).
- **Inventario arrastrado:** lo diferido o pendiente del
  dueño en fases anteriores reaparece en la auditoría (§5)
  sin asumirse resuelto — en particular el cron de
  propuestas, que sigue pausado a la espera de su secuencia
  (personalización pulida → reactivación como prueba
  integral).
- Lint y regresión parten de **cero fallos** y el chequeo 4
  de **cero hallazgos**: las brechas de esta fase son de
  colocación y declaración, no de formato ni de datos.
