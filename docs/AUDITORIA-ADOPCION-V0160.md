# Auditoría de adopción — My POD × Rameli v0.16.0 (2026-10-20)

> Primer insumo de la fase de mejora abierta al cerrar la
> migración a Rameli v0.16.0 (`docs/MIGRACION-RAMELI-V0160.md`),
> como manda `rameli/MIGRACIONES.md`. En esta migración la
> auditoría **no es diferible** (el delta trae capacidad
> nueva) y la nota de migración v0.16.0 exige expresamente la
> fila de **datos de instancia** (¿política declarada?,
> ¿medios fuera del repo?, ¿zonas de historial de instancia
> declaradas donde existan?). Método: matriz de capacidades
> vigentes × flujos, con veredicto y evidencia en el
> repositorio por celda — nada de memoria. Donde la evidencia
> no alcanza, la celda dice **sin evidencia**. La propuesta
> vive en `docs/FASE-MEJORA-V0160-PROPUESTA.md`.

## Método y bases verificadas

- **Framework de referencia:** repo `rameli`, `main` en
  `cf421e3` = `origin/main`, `VERSION` = **0.16.0**; tag
  anotado remoto `v0.16.0` y Release de GitHub verificados
  la misma noche del dale.
- **Aplicación auditada:** repo `my-pod`, `main` en
  `65c2721` al abrir (pin **0.15.0**), migración ejecutada
  con cirugía de historial sobre la historia completa
  (161 commits) y pin aplicado en la rama
  `migracion-rameli-v0160`.
- **Verificaciones corridas en vivo para esta auditoría**
  (2026-10-20): `rameli lint` sobre los 9 skills → **verde
  total** antes y después; `rameli test` → **53 casos,
  0 fallas** antes y después (idénticos); `rameli validar`
  → **0 fallos, 1 aviso** antes (adopción de la política
  pendiente) y **0 fallos, 0 avisos** después; censo de
  medios por `ls-tree` de los 161 commits antes (407 rutas
  bajo `data/` + 1 `.webp`) y después (**0 rutas**);
  manifiesto sha256 de `data/` antes/después de la cirugía
  (**551/551 idénticos**, 1,770,117,400 bytes); inventario
  de crons en vivo (detalle en el registro de la migración,
  Paso 0).
- **Precedente:** `docs/AUDITORIA-ADOPCION-V0150.md`
  (matriz contra v0.15.0, brecha B1 cerrada en su fase de
  mejora). Esta auditoría **confirma** los veredictos cuyas
  evidencias siguen en pie y **agrega** la capacidad nueva
  del delta: **C25**.

## Leyenda de veredictos

| Código | Significado |
|---|---|
| **P** | Adoptado y probado — evidencia de uso real |
| **A** | Adoptado sin estrenar — escrito/instanciado, sin corrida real |
| **NA** | No aplica — con motivo declarado |
| **B** | Brecha real — remite a la propuesta de la fase de mejora |
| **SE** | Sin evidencia — el repo no permite verificarlo |

## 1. La capacidad nueva del delta

- **C25 — Datos de instancia (NUEVA, v0.16.0).**
  (`rameli/docs/DATOS-INSTANCIA.md`.) Toda aplicación
  clasifica sus datos en tres clases — **sistema** (skills,
  docs, scripts: el repo que se comparte), **registros de la
  instancia** (texto liviano: fichas, config, registros,
  ledgers; su respaldo versionado es de la instancia, nunca
  mezclado con el sistema) y **medios** (binarios pesados:
  locales en su hogar canónico, **nunca** en el repo del
  sistema, ni en su historial) —, declara la política en
  `rameli.json → datos.politica_instancia.medios_en_git:
  false`, nace con el `.gitignore` de medios bajo su raíz de
  datos, y lo verifica la puerta (chequeo 5 de
  `rameli validar`, con el ámbito de instancia del chequeo
  4 para `historial_instancia`). El layout físico no cambia;
  las herramientas verifican **existencia física**, no
  estado de tracking. Caso origen medido: esta app
  versionaba 1.62 GB de imágenes de su tienda (`.git` de
  1.82 GB) dentro del repo del sistema.

## 2. Matriz de la capacidad nueva (C25) por flujo

| Flujo | Veredicto C25 | Evidencia / motivo |
|---|---|---|
| **F1 Propuestas (flujo v2, cron pausado)** | **P** | Es el flujo que más medios produce (artes en `data/artes-print/`, mockups en `data/mockups/`). Desde hoy sus medios nacen locales: el bloque de `.gitignore` los cubre (`git check-ignore -v` verificado sobre artes y mockups) y el chequeo 5 fallaría si uno entrara al repo. Sus registros (el `porque`, el checkpoint) siguen trackeados — ver B1. |
| **F2 Publicación por lote** (`publicador-lote`) | **P** | Consume medios por **existencia física** (videos y assets finales en su hogar); el barrido de consumidores no halló ningún uso de `git ls-files` en scripts/skills/docs vivos, y la regresión post-cirugía (que verifica diseños y videos reales de `data/`) corre verde idéntica contra la media restaurada. |
| **F3 Pinterest diario** (cron activo) | **P** | Lee assets finales físicos y el registro; su commit de cierre versiona solo texto (registro y `pin.json`) — con la política nueva, ningún medio puede colarse en ese commit por accidente de `git add`. |
| **F4 Dirección semanal** (crons activos) | **P** | Opera sobre registros de texto; sin producción de medios. |
| **F5 Onboarding de tienda** | **A** | El playbook crea la estructura de una tienda nueva dentro de `data/tiendas/<id>/` — desde esta migración, una tienda nueva nace ya bajo la política (`.gitignore` de la app + mapa declarado). Sin estrenar: no se ha onboardado una tienda desde la adopción. |
| **F6 Conexión Etsy API por tienda** | **NA** | No produce ni consume medios ni datos bajo la raíz; tokens y registro viven en el `config.json` de la tienda (registro de instancia, ver B1). |
| **F7 Operación comercial por API/scripts** | **P** | Los CSV de ventas ya vivían ignorados (`data/ventas-csv/*.csv`); los scripts leen y escriben archivos físicos sin depender del tracking (barrido `ls-files`: cero usos). |
| **F8 Puertas transversales** (arte, pin, paquete, publicar) | **P** | Las puertas verifican archivos físicos (DPI, fondo, hashes de manifiesto donde aplica). La suite de `puerta-arte-propuesta` conserva sus fixtures canónicos **dentro del repo** en `skills/…/evals/fixtures/` (15 `.png` del sistema, no de la instancia — colocación correcta: son insumo de calibración del sistema, no medios de producción de la tienda; el chequeo 5 solo mira bajo la raíz de datos). |
| **F9 Mantenimiento del sistema / migración misma** | **P** | Esta migración ES la adopción: política declarada, `.gitignore` canónico, cirugía con respaldo verificado y puerta (chequeo 5) corrida antes/después. |

## 3. Respuestas expresas a la nota de migración v0.16.0

- **¿Política declarada?** Sí:
  `rameli.json → datos.politica_instancia.medios_en_git:
  false`.
- **¿Medios fuera del repo?** Sí, verificado por censo de
  historial completo (161 commits por `ls-tree`): **0 rutas
  de medios bajo `data/`** (antes: 407 rutas + 1 `.webp`);
  `git ls-files data/` sin medios; `.git` de 1.82 GiB a un
  pack de 65.21 MiB. La media física permanece en su hogar
  (551 archivos, sha256 idénticos).
- **¿Zonas de historial de instancia declaradas donde
  existan?** Sí: `data/auditoria-2026-10-15` — la única zona
  de `historial` que tenía la app — reclasificada a
  `historial_instancia`, porque es el historial de
  auditoría de esta tienda y no viaja con el sistema. En la
  prueba de frío su ausencia en el clon se comporta como
  **aviso de ámbito de instancia**, no como fallo ni
  declaración podrida (verificado).

## 4. El resto de la matriz

Se **confirman** los veredictos de la auditoría v0.15.0 con
la evidencia de hoy: lint verde total, regresión idéntica
(53 casos), `rameli validar` 0/0 (mejora sobre el 0/1 de la
apertura: el aviso retirado es la adopción de C25), el
mapa de datos de C23 sin cambios de layout (solo gana la
política y la reclasificación de la zona de auditoría), y
C24 (el corte en las puertas que la ficha declara) operando
tal como lo dejó la fase de mejora v0.15.0 (publicador-lote
v0.1.6 + regla local en `docs/EJECUCION-Y-RELEVO.md`; el
barrido de esta auditoría no halló cortes nuevos sin
declarar). Ninguna capacidad previa cambia de veredicto por
este delta.

## 5. Brechas

- **B1 (C25 × registros de la instancia) — Los registros de
  texto de la tienda siguen versionados en el repo del
  sistema.** El estándar ubica los registros de la instancia
  (fichas/config, `registro-listings.json`, ledgers,
  investigaciones, `registro-flujo.md`) en el respaldo
  versionado **de la instancia** (repo privado propio),
  nunca mezclados con el sistema que se distribuye. La
  adopción exigible de esta migración (nota de migración +
  brief) es la política de **medios** — declarada, purgada y
  con puerta —; separar los registros es una cirugía mayor
  (toca el ciclo «escribir = commitear» de todos los crons
  de la tienda y el hogar de cada registro) que excede el
  alcance cerrado y requiere decisión del dueño.
  Propuesta P1 en `docs/FASE-MEJORA-V0160-PROPUESTA.md`.
- **B2 (C25 × `tmp/`) — Medios de producción trackeados
  fuera de la raíz de datos.** `tmp/videos-pendientes/`
  (50 archivos físicos, 37 MB) conserva **30 `.jpg`
  trackeados** de producción de videos. El chequeo 5 no los
  ve (su ámbito es la raíz de datos) y ningún script, skill
  o doc vivo referencia esa carpeta (barrido completo): es
  un área de trabajo que quedó versionada, contra el
  espíritu del estándar (los medios no viven en el repo del
  sistema, vivan donde vivan). No se tocó en esta migración:
  el brief preserva `tmp/` tal cual y la purga era solo bajo
  `data/`. Propuesta P2.
- **B3 (C25 × responsabilidad de respaldo de medios) — El
  respaldo de los medios quedó solo local.** Al salir de
  git, los medios pierden el «respaldo» implícito que era
  GitHub. Hoy su copia íntegra vive en
  `~/workspace/respaldos/my-pod-pre-v0160-2026-10-20/` — la
  misma máquina — y las piezas finales tienen además su
  copia en las plataformas (Printify/Etsy). El estándar
  (§6) no impone el medio de respaldo, pero exige que su
  ausencia sea **decisión, no accidente**: falta la
  decisión del dueño sobre respaldo externo de medios.
  Propuesta P3.
- **Observación (no brecha): el `.webp` no está en la lista
  canónica.** El bloque de `rameli init` y el chequeo 5
  cubren 10 extensiones; el historial de esta app contenía
  un `.webp` (purgado en la cirugía por mandato del brief:
  «cualquier otra presente»). Si un flujo volviera a
  producir `.webp` bajo `data/`, el `.gitignore` canónico
  no lo detendría ni la puerta lo marcaría. Hoy no existe
  ningún `.webp` físico bajo `data/`. Queda registrado como
  P4 (micro-decisión) en la propuesta.
