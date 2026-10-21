# Auditoría de adopción — My POD × Rameli v0.15.0 (2026-10-20)

> Primer insumo de la fase de mejora abierta al cerrar la
> migración a Rameli v0.15.0 (`docs/MIGRACION-RAMELI-V0150.md`),
> como manda `rameli/MIGRACIONES.md`. En esta migración la
> auditoría **no es diferible** (el delta trae capacidad
> nueva) y la nota de migración v0.15.0 exige expresamente la
> fila del **corte en las puertas que la ficha declara**
> (¿qué flujos cortan briefs/unidades?, ¿dónde quedó el
> chequeo?, ¿qué flujos registraron no-aplica y por qué?).
> Método: matriz de capacidades vigentes × flujos, con
> veredicto y evidencia en el repositorio por celda — nada de
> memoria. Donde la evidencia no alcanza, la celda dice
> **sin evidencia**. La propuesta vive en
> `docs/FASE-MEJORA-V0150-PROPUESTA.md`.

## Método y bases verificadas

- **Framework de referencia:** repo `rameli`, `main` en
  `3576a02` = `origin/main`, `VERSION` = **0.15.0**; tag
  anotado remoto `v0.15.0` verificado con `ls-remote`;
  Release de GitHub publicado desde ese tag en la sesión de
  la contribución (PR #8).
- **Aplicación auditada:** repo `my-pod`, `main` en
  `9ba2776` al abrir (pin **0.14.0**), migración en worktree
  aislado sobre la rama `migracion-rameli-v0150`.
- **Verificaciones corridas en vivo para esta auditoría**
  (2026-10-20): `rameli lint` sobre los 9 skills → **verde
  total** antes del pin; `rameli validar` → **0 fallos,
  0 avisos** antes del pin (el FALLO del chequeo 3 de
  v0.14.0 quedó cerrado en su fase de mejora: el canónico de
  la suite de arte vive en `evals/fixtures/` desde entonces);
  estado de crons consultado en vivo (propuestas **pausado**,
  Pinterest **activo**, estratega/investigación/rituales/
  trend-scan **activos**, watchdog **activo**, cron del
  31-oct **activo**); estado del lote de publicación leído
  de su checkpoint (ver §2, «trabajo en vuelo»).
- **Precedente:** `docs/AUDITORIA-ADOPCION-V0140.md`
  (matriz contra v0.14.0, brechas B1–B3, ejecutadas y
  cerradas en su fase de mejora el 2026-10-19). Esta
  auditoría **confirma** los veredictos cuyas evidencias
  siguen en pie, y **agrega** la capacidad nueva del delta:
  **C24**. La numeración C1–C23 se conserva por
  comparabilidad.

## Leyenda de veredictos

| Código | Significado |
|---|---|
| **P** | Adoptado y probado — evidencia de uso real |
| **A** | Adoptado sin estrenar — escrito/instanciado, sin corrida real |
| **NA** | No aplica — con motivo declarado |
| **B** | Brecha real — remite a la propuesta de la fase de mejora |
| **SE** | Sin evidencia — el repo no permite verificarlo |

## 1. La capacidad nueva del delta

- **C24 — Corte en las puertas que la ficha declara (NUEVA,
  v0.15.0, PR #8 de Rameli).** Antes de escribir un brief, el
  orquestador lee la ficha de la unidad y extrae las
  declaraciones que la gobiernan (etapa o fase, puertas entre
  pasos, modo de trabajo o equivalente); el brief se corta
  en la siguiente puerta declarada y declara su corte; la
  ausencia de puertas declaradas se registra, no se presume.
  (`rameli/docs/EJECUCION-POR-WORKERS.md`, sección «El corte
  en las puertas que la ficha declara».) Caso origen: una
  aplicación hermana, cuyo documento de modos declara puerta
  humana en cada etapa para su modo más supervisado y cuya
  ficha viva declara ese modo — un brief empaquetó una
  producción completa cruzando las puertas.

## 2. Trabajo en vuelo al abrir la migración (verificación expresa)

La orden de la sesión mandó verificarlo antes de migrar,
porque un lote de publicación POD se gestionaba desde otro
chat. Evidencia, no memoria:

- **El lote Thanksgiving (manifiesto de 11 MPLs: p039, p040,
  p042, p043, p045, p046, p052–p056) está CERRADO.** Su
  checkpoint (`data/tiendas/29222324/estado-publicacion.json`,
  capa fina local) registra `cerrado: "2026-10-20: lote
  completo 11/11 publicado_completo con Fase C PASS y
  registro commiteado"`, sin ninguna fase `en_curso`, y su
  última corrección (video2 de p046, regenerado en la
  fuente) quedó commiteada a las 20:23 EDT
  (`9ba2776`, el HEAD de `main` al abrir esta migración) —
  minutos antes de que esta misión empezara (20:45 EDT).
- `main` estaba limpia y sincronizada (`main == origin/main`
  en `9ba2776`), sin ramas de trabajo abiertas y con un solo
  worktree. Único rastro ajeno: `tmp/
  paso1-investigacion-personalizacion.md` **sin trackear**
  (investigación de personalización de otro trabajo,
  2026-10-19): esta migración **no lo toca** — no se commitea,
  no se mueve, no se borra.
- Los crons vivos de la app (Pinterest diario, dirección
  semanal, watchdog) operan sobre datos y no escriben código
  ni declaraciones de pin; el cron de propuestas sigue
  **pausado** por orden del dueño. Ninguno pisa una migración
  de pin, que se ejecutó además en worktree aislado y se
  fusionó con fast-forward tras re-verificar que `main` no
  se había movido.

**Conclusión:** no hay trabajo en vuelo que la migración
pueda pisar; la secuenciación quedó: lote cerrado y
commiteado → migración en worktree → fusión verificada.

## 3. Matriz de la capacidad nueva (C24) por flujo

Flujos según el inventario de la auditoría anterior,
actualizado con el estado verificado hoy.

| Flujo | ¿Corta briefs/unidades contra una ficha? | Veredicto C24 | Evidencia / motivo |
|---|---|---|---|
| **F1 Propuestas (flujo v2, cron pausado)** | No — lo despierta el reloj; su «brief» es el cuerpo fijo del cron, no lo corta un orquestador por corrida | **NA** (con puerta equivalente operando) | La puerta que gobierna vive DENTRO del flujo y está escrita en sus skills: Fase A (arte + puerta) → **aprobación del dueño por diseño** → Fase B (drafts/MPL solo de aprobados). El worker no puede cruzarla: la Fase B exige aprobados registrados. El deber de C24 nace para quien empaqueta el alcance; aquí el alcance viene prefijado por el sistema, no empaquetado por corrida. |
| **F2 Publicación por lote** (`publicador-lote`) | **Sí** — el agente principal resuelve el manifiesto (el corte) y lanza un worker por lote | **B — brecha real (B1)** | El corte existe y su puerta es la aprobación del dueño (M2 de `publicar-printify-etsy`), pero `publicador-lote` v0.1.5 **no manda leer la ficha de la tienda ni las declaraciones que gobiernan el lote antes de cortar**, ni exige que el manifiesto declare su corte. El riesgo ya ocurrió: el 2026-10-20 un lote mezcló remanentes nunca revisados por el dueño con el lote aprobado (criterio corregido por el dueño ese día: solo entra lo que él revisó como MPL; el remanente no es aprobación) — el criterio vive en la memoria del sistema, no en el paso de invocación del skill que corta. |
| **F3 Pinterest diario** (cron activo) | No — unidad prefijada por su skill (parrilla del día) y su checkpoint | **NA** | El reloj no orquesta (delimitación ya adoptada); nadie empaqueta alcance por corrida. Su puerta (`puerta-pinterest-pin`) se ejecuta dentro de la unidad. |
| **F4 Dirección semanal** (crons activos) | No — produce la directriz; no despacha workers | **NA** | Sin briefs que cortar. La directriz es insumo declarado de F1, no una unidad de worker. |
| **F5 Onboarding de tienda** | No — guiado interactivo con el dueño en vivo | **NA** | Vía directa declarada en el registro de adopción de workers (v0.11.0): no hay worker frío ni brief; el dueño está en cada paso en persona, que es la puerta misma. |
| **F6 Conexión Etsy API por tienda** | No — interactivo, con el clic OAuth del dueño en vivo | **NA** | Vía directa declarada (v0.11.0); sin unidad de worker que cortar. |
| **F7 Operación comercial por API/scripts** | No — órdenes directas del dueño y cron de un solo uso programado por él (31-oct) | **NA** | No hay orquestador empaquetando alcance: la orden ES la autorización, caso por caso. |
| **F8 Puertas transversales** (arte, pin, paquete, publicar) | No — ejecutan DENTRO de las unidades que otros flujos abren | **NA** | No cortan; son las puertas mismas. |
| **F9 Mantenimiento del sistema / flujos ad-hoc multi-paso** | **Sí** — los flujos ad-hoc de varios pasos con brief limpio y chat nuevo están adoptados desde v0.11.0 (registro en `docs/MIGRACION-RAMELI-V0110.md`) | **B — brecha real (B1, misma raíz)** | `docs/EJECUCION-Y-RELEVO.md` (la adopción local de la doctrina) **no declara el corte**: ningún texto de la app manda que un brief ad-hoc se corte en la siguiente puerta que la ficha de la tienda declare (p. ej. la aprobación previa a publicar, registrada en el registro de flujo) ni que declare su corte. |

## 4. El resto de la matriz

Se **confirman** los veredictos de la auditoría v0.14.0 con
la evidencia de hoy: lint verde total, `rameli validar`
0/0 (su FALLO histórico del chequeo 3 quedó cerrado en la
fase de mejora v0.14.0 y la puerta lo re-verificó hoy), mapa
de datos sin cambios y chequeo 4 sin hallazgos, ruta de
lectura vigente en `FLUJO-PIPELINE.md` (suma el puntero a
los registros de esta migración). Ninguna capacidad previa
cambia de veredicto por este delta.

## 5. Brechas

- **B1 (C24 × F2/F9) — El deber de C24 no está escrito donde
  esta app corta.** Ni el paso de invocación de
  `publicador-lote` ni la adopción local de la doctrina
  (`docs/EJECUCION-Y-RELEVO.md`) mandan leer la ficha de la
  tienda y cortar en la puerta declarada, con el corte
  declarado. Propuesta P1 en
  `docs/FASE-MEJORA-V0150-PROPUESTA.md`.
