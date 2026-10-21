# Auditoría de adopción — My POD × Rameli v0.17.0 (2026-10-21)

> Primer insumo de la fase de mejora abierta al cerrar la
> migración a Rameli v0.17.0 (`docs/MIGRACION-RAMELI-V0170.md`),
> como manda `rameli/MIGRACIONES.md`. En esta migración la
> auditoría **no es diferible**: la nota de migración de
> v0.17.0 trae capacidad nueva (el ciclo de vida del staging)
> y la propia nota de v0.16.0 dejó la fila de datos de
> instancia cobrable en la siguiente fase — esta unidad la
> cobra ejecutando la separación de registros (D1). Método:
> matriz de capacidades vigentes × flujos, con veredicto y
> evidencia en el repositorio por celda — nada de memoria.
> Donde la evidencia no alcanza, la celda dice **sin
> evidencia**. La propuesta vive en
> `docs/FASE-MEJORA-V0170-PROPUESTA.md`.

## Método y bases verificadas

- **Framework de referencia:** repo `rameli`, `VERSION` =
  **0.17.0** (tag anotado `v0.17.0` y Release de GitHub
  verificados el 2026-10-21); delta 0.16.x → 0.17.0 en su
  `CHANGELOG.md` y la nota en `MIGRACIONES.md`.
- **Aplicación auditada:** repo `my-pod`, `main` en
  `85c75fa` al abrir (pin **0.16.0**); la unidad ejecuta en
  la misma pasada la separación de registros D1 autorizada
  por el dueño (decisiones D1/D2 del 2026-10-21).
- **Verificaciones corridas en vivo para esta auditoría**
  (2026-10-21): `rameli lint` sobre los 9 skills → **verde
  total** antes y después; `rameli test` → **53 casos,
  0 fallas** antes y después (13+4+3+18+15, con los mismos
  4 avisos de skills sin `evals/`); `rameli validar` →
  **0 fallos, 0 avisos** antes y después; censo de
  registros trackeados bajo `data/` (**143 archivos de
  texto**: 104 json, 35 md, 4 `.gitkeep`; **0 medios** en
  árbol y **0 rutas de medios bajo `data/` en los 164
  commits**); manifiesto sha256 de `data/` (**551
  archivos, 1,770,117,400 bytes**) idéntico antes y
  después; inventario de crons vivos de la tienda (Paso 0
  del registro de migración).
- **Precedente:** `docs/AUDITORIA-ADOPCION-V0160.md`
  (matriz contra v0.16.0, brechas B1–B3 y observación
  `.webp`). Esta auditoría **confirma** los veredictos cuyas
  evidencias siguen en pie, **agrega** la capacidad nueva
  del delta (**C26**) y **cobra** las brechas de C25: B1 y
  B3 se cierran en esta unidad (ver §4).

## Leyenda de veredictos

| Código | Significado |
|---|---|
| **P** | Adoptado y probado — evidencia de uso real |
| **A** | Adoptado sin estrenar — escrito/instanciado, sin corrida real |
| **NA** | No aplica — con motivo declarado |
| **B** | Brecha real — remite a la propuesta de la fase de mejora |
| **SE** | Sin evidencia — el repo no permite verificarlo |

## 1. La capacidad nueva del delta

- **C26 — Ciclo de vida del staging (NUEVA, v0.17.0).**
  (`rameli/docs/DATOS-INSTANCIA.md` §8.) El staging es un
  **estado**, no una cuarta clase: la zona se **declara**
  en `rameli.json → datos.zonas_staging`, **no se
  trackea**, su **cierre = purga** (al cerrar el flujo
  verificado, el staging se elimina como parte del cierre)
  y solo **sobrevive con un consumidor vivo declarado**
  (responsable + fecha de revisión o vencimiento). El
  chequeo 5 de `rameli validar` suma el aviso: zona
  declarada con archivos trackeados → **AVISO** con el
  conteo, nunca FALLO. Caso origen: una app guardaba
  versionada su carpeta de staging de videos con el flujo
  terminado y publicado días atrás — **esta app**, cuyo
  remanente (`tmp/videos-pendientes/`) originó el criterio.

## 2. Matriz de la capacidad nueva (C26) por flujo

| Flujo | Veredicto C26 | Evidencia / motivo |
|---|---|---|
| **F1 Propuestas (flujo v2)** | **P** | Su única zona de staging histórica (`tmp/videos-pendientes/`, staging de los videos de Etsy del 2026-10-16) se **purgó al cierre** el 2026-10-21 (decisión del dueño: flujo completado + validado + salidas publicadas ⇒ remanente; ver P2 de la fase v0.16.0). La regla de ciclo de vida vive en `FLUJO-PIPELINE.md` §5.1 y `rameli.json` declara `datos.zonas_staging: []` — ninguna zona viva. |
| **F2 Publicación por lote** | **NA** | No mantiene zonas de staging propias; consume assets finales de su hogar canónico. |
| **F3 Pinterest diario** | **P** | Su cola (`data/cola-pins/`) es staging transitorio **declarado por comportamiento**: nace con el pin validado y se vacía al publicar (los pin.json se mueven a `data/pins-publicados/`); su contenido nunca se versionó (solo el `.gitkeep`) y tras D1 sigue sin versionarse en ningún repo. |
| **F4 Dirección semanal** | **NA** | No produce staging. |
| **F5 Onboarding de tienda** | **A** | El playbook no crea zonas de staging; si un flujo futuro abre una, nace bajo la regla (declarar en `zonas_staging` + purgar al cierre, escrita en `FLUJO-PIPELINE.md` §5.1). Sin estrenar. |
| **F6 Conexión Etsy API** | **NA** | Sin staging. |
| **F7 Operación comercial** | **NA** | Sus CSV crudos (`data/ventas-csv/`) son importación regenerable ignorada, no staging de un flujo con cierre. |
| **F8 Puertas transversales** | **NA** | Verifican archivos en su hogar; no mantienen staging. |
| **F9 Mantenimiento del sistema** | **P** | Esta auditoría ES la verificación: barrido de zonas — `tmp/` contiene únicamente el archivo sin trackear de otro trabajo (`tmp/paso1-investigacion-personalizacion.md`, intacto, sha256 verificado) y ninguna carpeta de staging; `rameli validar` sin aviso de staging (no hay zonas declaradas ni trackeados en zona alguna). |

## 3. Respuestas expresas a la nota de migración v0.17.0

- **¿Zonas de staging declaradas?** Sí: `datos.zonas_staging:
  []` — la app no reconoce ninguna zona viva, verificado
  por el barrido de §2 (la única histórica se purgó como
  manda la regla, antes incluso de que el canon la
  escribiera: el caso origen es de esta app).
- **¿Cómo adopta?** Declaración + `rameli validar` corrido:
  **0 fallos, 0 avisos** — sin aviso de staging, consistente
  con cero zonas declaradas y cero trackeados en staging.
- **¿El pin se actualiza?** Sí, en esta migración ordinaria:
  `rameli.json`, los 9 frontmatter y las 3 líneas vivas de
  CHANGELOG pasan a **0.17.0**.

## 4. El resto de la matriz — y el cobro de C25

Se **confirman** los veredictos de la auditoría v0.16.0 con
la evidencia de hoy (lint verde, regresión idéntica de 53
casos, `rameli validar` 0/0, mapa de datos sin cambios de
layout). Cambian dos celdas de **C25 (datos de instancia)**,
por ejecución en esta unidad:

- **La fila de registros de C25 pasa a P en todos los
  flujos.** La brecha **B1** de la auditoría v0.16.0 (los
  registros de texto versionados en el repo del sistema)
  queda **CERRADA**: repo privado `my-pod-datos` creado,
  historia de registros separada por rutas (88 commits;
  árbol idéntico blob a blob, 143/143), repo del sistema
  reescrito sin registros en árbol ni en historial con su
  esqueleto, y el ciclo «escribir = commitear» re-apuntado
  (skills estratega-tienda v0.6.1, estratega-pinterest
  v0.1.4, onboarding-tienda v0.1.4; `ARQUITECTURA-DATOS.md`;
  cuerpos de los crons vivos; puente
  `scripts/registros-datos.py`). Evidencia completa en
  `docs/MIGRACION-RAMELI-V0170.md`.
- **La brecha B3 (respaldo de medios) queda RESUELTA por
  decisión, no por ejecución:** la decisión **D2** del
  dueño (2026-10-21) — el respaldo de los registros ES el
  repo de datos en GitHub (gratis, el sistema commitea
  solo) y los medios quedan **sin respaldo externo por
  decisión explícita** (finales en las plataformas,
  intermedios regenerables, staging purgado al cierre).
  El estándar (§6) exige exactamente eso: que la ausencia
  sea decisión, no accidente.
- **La observación `.webp` queda cerrada por el
  framework:** v0.16.1 extendió la lista del chequeo 5
  (webp/avif/heic/heif/gif/bmp/tif/tiff) y v0.17.0 la trae
  consigo; esta app corre el validador desde el framework
  en 0.17.0, así que la lista extendida ya aplica (y el
  único `.webp` del historial se purgó el 2026-10-21).

## 5. Brechas y observaciones nuevas

- **B1-17 (C25 × clon solo-sistema) — Un clon frío del
  repo del sistema, sin restaurar su repo de datos, no es
  una instancia operable, y el chequeo 4 lo marca FALLO
  si el esqueleto crea el hogar de la tienda.** El
  esqueleto de esta app incluye los `.gitkeep` de
  `investigaciones/` y `revisiones/` dentro de
  `data/tiendas/29222324/` (estructura declarada por el
  playbook de onboarding); con el hogar presente pero sin
  sus registros, el chequeo 4 reporta «hogar incompleto».
  La instancia completa se restaura clonando también
  `my-pod-datos` y corriendo
  `scripts/registros-datos.py pull` (verificado en la
  prueba de frío combinada de esta unidad: `rameli
  validar` 0 fallos sobre la instancia restaurada). El
  FALLO en el clon sin restaurar es una señal honesta,
  pero el framework no conoce la separación: no hay campo
  en `rameli.json` que declare el repo de registros, ni
  ámbito de instancia para hogares. Propuesta P1 en
  `docs/FASE-MEJORA-V0170-PROPUESTA.md` (contribución a
  Rameli; decisión del dueño).
- **Observación (no brecha de esta app): el cron
  `pod-ritual-lunes-h04` referencia rutas
  `docs/investigacion/…` que no existen en este repo.**
  Su cuerpo no commitea registros en `my-pod` (no es parte
  del inventario D1) y sus rutas parecen de un layout
  anterior al reorden del 2026-10-19. Se registra como P2
  de la fase de mejora para que su flujo lo revise; no se
  tocó en esta unidad.
- **Micro-corrección registrada (no brecha):** el
  frontmatter de `estratega-pinterest` venía en v0.1.2 con
  su CHANGELOG ya en v0.1.3; esta unidad lo deja en fase
  (v0.1.4 en ambos) al re-apuntar su regla de commit.
