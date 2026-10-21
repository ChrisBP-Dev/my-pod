# Migración a Rameli v0.18.0 — cierre de alineación completo (2026-10-21)

> Actualización oficial de la app a **Rameli v0.18.0**,
> ejecutada como **actualización completa** por mandato
> del dueño (2026-10-21 08:50 EDT: encargarse de todo y
> dejarlo perfecto, sin huecos — nada roto, nada
> apuntando a rutas muertas, nada guiando trabajo de forma
> incorrecta). Bajo ese mandato, Jarvis revisó las
> propuestas de la fase de mejora v0.17.0 y decidió:
> **P1 aprobada** (ejecutada como framework: Rameli
> v0.18.0) y **P2 aprobada** (ejecutada en esta unidad).
> Brief de la unidad:
> `~/workspace/migraciones-v0170/brief-my-pod-cierre-alineacion.md`.
> Proceso: `rameli/MIGRACIONES.md` (nota 0.17.0 → 0.18.0 y
> doctrina de actualización completa) y canon
> `rameli/docs/DATOS-INSTANCIA.md` §4. Auditoría de
> adopción (no diferible):
> `docs/AUDITORIA-ADOPCION-V0180.md`.

## Paso 0 — guardas e inventario

- **Precondición verificada antes de empezar:** Rameli
  **v0.18.0 publicado** — repo `rameli` en `bbb587c`
  (fusión del PR #9), tag `v0.18.0` presente en el remoto
  (`git ls-remote`), `VERSION` = 0.18.0, regresión del
  framework **24 ok, 0 fallos** (su CHANGELOG); Release
  de GitHub v0.18.0 Latest verificado por el orquestador
  al abrir la operación y confirmado en la verificación
  por navegador de esta unidad.
- **Línea base (sobre `main` en `af00e35`, pin 0.17.0):**
  lint **VERDE** total; regresión **53 casos, 0 fallas**
  (13+4+3+18+15), 4 avisos preexistentes de skills sin
  `evals/`; `rameli validar` **0 fallos, 0 avisos**. El
  archivo sin trackear de otro trabajo
  (`tmp/paso1-investigacion-personalizacion.md`, sha256
  `6dc145e9…`) se preserva intacto, verificado antes y
  después.
- **Sin tocar la operación comercial:** nada de listings,
  precios, ofertas ni Printify/Etsy se modificó en esta
  unidad. Nada de media ni de registros se borró.

## La migración a v0.18.0 (delta y adopción)

- **Delta 0.17.0 → 0.18.0** (del `CHANGELOG.md` de Rameli
  y la nota en `MIGRACIONES.md`): aditivo, sin cambios
  rompientes — (1) la **declaración del repo de
  registros** (`repo_datos`) en el estándar de datos de
  instancia (§4); (2) el **ámbito de instancia por
  separación** en el chequeo 4 de `rameli validar`; (3)
  la doctrina de **actualización completa** en
  `MIGRACIONES.md`.
- **Adopción — pin 0.18.0:** `rameli.json`
  (`framework_version` + nota de migración), los **9
  frontmatter** de skills y las **3 líneas vivas** de
  pin en los CHANGELOG de skill (`estratega-pinterest`,
  `puerta-arte-propuesta`, `puerta-pinterest-pin`), más
  la sección nueva del `README.md`.
- **Adopción — declaración `datos.repo_datos`:** la
  separación D1 (ejecutada en v0.17.0) gana su forma
  canónica: objeto en `rameli.json → datos` con
  `nombre: my-pod-datos`,
  `url: git@github.com:ChrisBP-Dev/my-pod-datos.git`,
  `contiene: data` y `nota` (mecánica del puente,
  decisiones D1/D2, par local). Con esto la brecha
  **B1-17 queda CERRADA** (era la P1 de la fase de
  mejora v0.17.0, ejecutada vía el framework).

## Puertas — validación en los dos estados

Corridas con el validador de Rameli v0.18.0 sobre clones
frescos en `/tmp/clon-v0180` (desechables; la evidencia
es esta tabla):

| Estado | Resultado |
|---|---|
| Instancia viva restaurada (sistema + registros físicos) | **0 fallos, 0 avisos** |
| Clon frío restaurado (clon sistema + clon `my-pod-datos` + `registros-datos.py pull` → 144 registros) | **0 fallos**, 1 aviso de ámbito (`data/auditoria-2026-10-15`, media de instancia que no viaja en ningún repo; mismo aviso de la unidad v0.17.0) |
| Clon de solo sistema (solo el esqueleto `.gitkeep`) | **0 fallos** — AVISO «hogar presente pero sin registros en esta copia» por la separación declarada (antes de v0.18.0: FALLO de hogar incompleto), más los avisos de ámbito de los registros globales y de `historial_instancia` |
| Control: clon solo-sistema con hogar **parcial** (solo `config.json`) | **FALLO** «hogar incompleto» (3 fallos) — el ámbito no disfraza un hogar roto, como manda el canon |

- **Lint y regresión post-migración:** idénticos a la
  línea base — lint VERDE total; regresión **53 casos,
  0 fallas**, mismos 4 avisos preexistentes.
- **Ciclo «escribir = commitear» verificado:** puente
  `scripts/registros-datos.py` — `estado`: **144
  registros físicos = 144 en el clon de datos**, repo de
  datos sin ahead; `pull` probado en el clon frío (144
  restaurados); `commit` probado sin cambios (nada que
  commitear) y en producción real el mismo día (la
  corrida de Pinterest del 2026-10-21 commiteó su
  registro vía el puente: `my-pod-datos` en `0843bcb`,
  sin ahead).

## P2 — el ritual de los lunes (ejecutada, con evidencia)

**Evidencia primero** (corridas registradas de ambos
crones, mismo lunes):

- `pod-ritual-lunes-h04` (lun 07:50) — su corrida del
  2026-10-19 evaluó **un** nicho candidato («gift for
  nurse mom») con el ritual H04: veredicto DESCARTADO
  2/5 (colisión semántica, precios bajo COGS, 0 señales
  de venta), creó su ficha de nicho y actualizó el banco
  de nichos. Función: **validación de nichos, uno por
  lunes, con veredicto binario y banco H05**.
- `equipo-pod-investigacion-semanal` (lun 08:50) — su
  corrida del 2026-10-19 produjo la investigación
  general de la tienda: ventas/ledger, registro, SEO
  interno, tendencias Etsy/Pinterest y top 5 prioridades
  para la estratega. Función: **investigación amplia y
  prioridades**, sin validación de nichos ni bancos.

**Decisión (regla del brief):** las salidas y el trabajo
son **distintos** — no hay duplicación total — así que
el ritual **se conserva y se corrigen sus rutas** al
layout vigente. No se retira ningún cron.

**Corrección aplicada** (`cron.update` sobre
`pod-ritual-lunes-h04`, verificada con `cron.view`;
horario, dueño y entrega intactos — lun 07:50, próxima
corrida lun 2026-10-26):

| Ruta muerta (del workspace del goal) | Ruta vigente (esta app) |
|---|---|
| `docs/investigacion/keywords/` (bancos POR VALIDAR) | `~/workspace/my-pod/data/banco-keywords/` (bancos; estado en su encabezado) + fichas con banco en borrador en `docs-migrados/nichos/` |
| `docs/investigacion/calendario-12-meses.md` (ángulo alternativo) | Investigaciones recientes de la tienda (`data/tiendas/29222324/investigaciones/`) + estacionalidad de la directriz vigente (`data/tiendas/29222324/direccion-tienda.md`) — el calendario no tiene equivalente portado; su función la cubren esos dos insumos, que son los que la estratega ya consume |
| `docs/investigacion/ritual-validacion.md` (método H04) | Los 3 pasos y el test de 5 puntos viven en la plantilla vigente: `docs-migrados/nichos/_plantilla.md` |
| `docs/investigacion/nichos/` (ficha del nicho) | `docs-migrados/nichos/<slug>.md` (casa de las fichas desde el portado del 2026-10-11; la referencia el skill `onboarding-tienda`) |
| `docs/propuestas/loop.md` («Estado de insumos») | Sin equivalente como archivo: el estado de insumos queda registrado en la propia ficha y en el encabezado del banco — la fuente que leen la estratega y el paquete de listings (paso 4 reescrito con esa mecánica) |

Además el cuerpo ganó la mecánica que le faltaba y que
todos sus crons hermanos ya tenían desde D1: **commit
en la misma corrida** (la ficha, sistema → git directo
en `my-pod`; el banco, registro → repo de datos vía
`scripts/registros-datos.py commit`). Todas las rutas
nuevas se verificaron físicamente existentes.

## Barrido de referencias muertas (inventario completo)

Alcance: crons vivos de la operación POD (cuerpos leídos
con `cron.view`), skills (SKILL.md y CHANGELOG), scripts
de la app y de los skills, y docs operativos (las
secciones históricas de migración/auditoría y las notas
de procedencia no son punteros operativos y se
clasifican como tales).

**Corregidos en esta unidad:**

1. `pod-ritual-lunes-h04` — 5 rutas muertas → P2 (arriba).
2. `equipo-pod-propuestas-diarias` (pausado) — su cuerpo
   declaraba «Rameli v0.17.0 — pineado en rameli.json»:
   actualizado a **v0.18.0**. Verificado por diff contra
   el cuerpo previo: cambia solo esa línea.
3. `docs-migrados/nichos/_plantilla.md` — su instrucción
   operativa «Copiar como `docs/investigacion/nichos/
   <slug>.md`» apuntaba a la ruta del workspace del
   goal: corregida a `docs-migrados/nichos/<slug>.md`,
   con nota de la corrección.
4. `printify-upload-watch` — describía el PNG de prueba
   como «69 bytes»; el archivo real
   (`~/workspace/pod-etsy/printify-upload-test.png`,
   1×1) pesa **68 bytes**: corregido (diff verificado:
   solo ese dato; la predicción de permisos del conector
   quedó restaurada tras la actualización).

**Marcado para el dueño (decisión de producto, no de
alineación — no se resolvió en silencio):**

5. `pod-ritual-viernes-h12` — lee las reglas H11/H13 en
   `docs/operacion/ledger-registros.md`, `ledger.md` y
   `ads.md` del workspace del goal (en esta app no hay
   equivalente portado) y regenera el centro de comando
   con una ruta relativa de ese mismo workspace. Tres
   problemas en uno: (a) su `ledger-registros.md` quedó
   en **14 filas del 2026-10-16**, frente al registro
   vivo de la tienda en `data/tiendas/29222324/`; (b)
   sus reglas H11 (kill **60 días** / observación
   **30 días**) difieren de las que enuncia
   `equipo-pod-revision-viernes` (matar «sin tracción en
   30 días»), que corre a la misma hora y escribe su
   acta en la misma carpeta `revisiones/`; (c) qué
   fuente de reglas manda es decisión suya. El ritual
   **no** se retiró: tiene funciones no duplicadas
   (condiciones de activación de Ads H13, fee bleed
   mensual, centro de comando) y su salida/commits ya
   fueron re-apuntados a esta app en D1. Opciones:
   portar H11/H13 a `docs-migrados/` y re-apuntar el
   ritual al registro vivo, unificar las reglas en la
   revisión de viernes, o retirar el ritual conservando
   sus funciones únicas en otro cron.
6. `equipo-pod-estratega-semanal` — su cuerpo conserva
   una «NOTA 2026-10-19» anclada a la reevaluación del
   override de esa semana (ya ejecutada: la directriz
   del 2026-10-19 salió de esa corrida). No es una ruta
   muerta y su sustancia (proponer el reparto en cada
   corrida) ya vive en el cuerpo principal; se deja
   constancia aquí en vez de editar el cuerpo de la
   estratega en una unidad de alineación.

**Verificado sin hallazgo:**

7. Todo `scripts/` nombrado por un skill existe
   físicamente: **20/20** (en `scripts/` de la app o en
   el `scripts/` del propio skill). Las dos copias de
   `verificar-pin.py` (app y skill) son **byte-idénticas**.
8. Los demás crons vivos (`equipo-pod-estratega-semanal`,
   `equipo-pod-investigacion-semanal`, `pod-trend-scan`,
   `equipo-pod-revision-viernes`,
   `equipo-pod-pinterest-diario`, `equipo-pod-watchdog`,
   `etsy-sale-25-to-20-oct31`,
   `cyber-specials-decision-2026-10-26`): todos sus
   punteros a rutas, scripts y archivos resuelven a algo
   existente y vigente (incluidas las rutas de reintento
   que apuntan a los archivos de definición de los
   propios crons).
9. Rutas absolutas en skills, scripts y docs operativos:
   resuelven todas; los únicos patrones con comodín son
   plantillas reales (`data/banco-keywords/pinterest-
   <nicho>.md` → existe `pinterest-enfermeria.md`;
   `~/.config/my-pod/etsy-api-<shop>.json` → existe el
   archivo real de credenciales). `tmp/videos-pendientes/`
   en `README.md`/`FLUJO-PIPELINE.md` es el caso
   fundacional histórico de la regla de staging, no un
   puntero: la carpeta no existe, como manda la regla.
10. Sin referencias a rutas muertas en `skills/` ni en
    los docs operativos tras las correcciones 1–4: el
    barrido automático (extracción de rutas de crons,
    skills, scripts y docs) quedó limpio salvo los
    falsos positivos clasificados arriba.

## Fase de mejora v0.17.0 — EJECUTADA (cierre)

Con esta unidad, la fase de mejora abierta en la
migración a v0.17.0 queda **ejecutada completa** y su
documento (`docs/FASE-MEJORA-V0170-PROPUESTA.md`) pasa a
registrarlo: **P1** ejecutada vía el framework (Rameli
v0.18.0, PR #9 — declaración `repo_datos` + ámbito de
instancia del chequeo 4) y adoptada aquí; **P2**
ejecutada arriba. Nada de la fase queda pendiente; los
hallazgos marcados 5–6 del barrido son temas nuevos que
nacen de esta unidad, no restos de la fase.

## Cierre y fusión

- **Rama y fusión:** la unidad se trabajó en la rama
  `migracion-rameli-v0180` (commits `9b72c0a` — pin,
  declaración `repo_datos`, README y corrección de la
  plantilla — y `6118939` — registro, auditoría y fase de
  mejora ejecutada), fusionada a `main` por
  **fast-forward** bajo la autorización del brief
  (`af00e35 → 6118939`), rama local borrada (nunca se
  empujó al remoto) y push verificado: `git status -sb` =
  `## main...origin/main` **sin ahead ni behind**;
  `my-pod-datos` igual, sin ahead (su HEAD del día,
  `0843bcb`, es de la operación normal vía el puente).
- **Verificación post-fusión en `main`:** `rameli
  validar` **0 fallos, 0 avisos**; pin **0.18.0** y
  `datos.repo_datos` leídos de `rameli.json` ya fusionado;
  el archivo sin trackear de otro trabajo
  (`tmp/paso1-investigacion-personalizacion.md`, sha256
  `6dc145e9…`) intacto antes y después.
- **Crons tocados en esta unidad (3):**
  `pod-ritual-lunes-h04` (P2: rutas corregidas +
  mecánica de commit; verificado con `cron.view`,
  próxima corrida lun 2026-10-26 07:50),
  `equipo-pod-propuestas-diarias` (pin v0.18.0 en su
  cuerpo; sigue **pausado**, como estaba) y
  `printify-upload-watch` (dato del PNG corregido a 68
  bytes; predicción de permisos del conector
  restaurada). Ningún otro cron cambió.
- **Estado final:** app en Rameli **v0.18.0** con la
  separación de registros **declarada**; fase de mejora
  v0.17.0 **ejecutada completa**; barrido cerrado con
  cero referencias muertas conocidas en la app, salvo
  los dos hallazgos marcados para el dueño (§Barrido,
  ítems 5–6), que son decisiones de producto y quedan
  vivos en este registro hasta que él los resuelva.
