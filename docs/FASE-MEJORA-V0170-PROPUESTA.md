# Fase de mejora post-migración v0.17.0 — PROPUESTA (2026-10-21)

Abierta automáticamente al cerrar la migración a Rameli
v0.17.0, como manda `rameli/MIGRACIONES.md`, con la
**auditoría de adopción completa** como primer insumo —
en esta migración era **no diferible** (el delta trae
capacidad nueva) y se corrió:
`docs/AUDITORIA-ADOPCION-V0170.md`. Una brecha (B1-17) y
una observación (el ritual de los lunes).

**Estado: EJECUTADA COMPLETA (2026-10-21).** El dueño
ordenó la actualización completa (2026-10-21 08:50 EDT)
y delegó en Jarvis la aprobación de estas propuestas;
Jarvis las aprobó ambas y quedaron ejecutadas en la
misma operación: **P1** vía el framework — Rameli
**v0.18.0** (PR #9: declaración `repo_datos` + ámbito de
instancia del chequeo 4), adoptada por esta app en su
migración a v0.18.0 — y **P2** en la unidad de cierre de
alineación de esta app (evidencia de función propia del
ritual frente a la investigación semanal; rutas
corregidas al layout vigente, sin retirar el cron).
Registro completo: `docs/MIGRACION-RAMELI-V0180.md`.
El texto original de la propuesta se conserva debajo,
como historia.

---

**Estado original al abrirla: PROPUESTA — nada se ejecuta sin el dale del
dueño.** La migración misma y la separación de registros
D1 se ejecutaron con el dale del paquete completo
(2026-10-21 01:09 EDT); estas dos propuestas nacen DE la
auditoría de esta unidad y esperan su palabra, cada una
en su ámbito (framework y flujo, respectivamente).

## P1 — Declarar el repo de registros en el framework (B1-17)

- **Qué:** proponer a Rameli, por la vía de contribución
  (`rameli/docs/CONTRIBUCIONES.md`), dos piezas que la
  separación D1 dejó al descubierto: (1) un campo de
  declaración en `rameli.json → datos` para el respaldo de
  registros de la instancia (p. ej. el repo de datos que la
  instancia usa), de modo que el sistema declare dónde
  viven sus registros en vez de saberlo solo su operador;
  y (2) que el chequeo 4 trate el hogar de unidad presente
  pero sin registros — en una app que declara separación —
  con **ámbito de instancia** (AVISO: «registros sin
  restaurar en esta copia»), como ya hace con
  `historial_instancia`, en vez de FALLO de hogar
  incompleto. Hoy la instancia restaurada (sistema + datos
  + `registros-datos.py pull`) valida 0/0 y el clon
  solo-sistema marca FALLO: la señal es honesta pero ciega
  a la causa.
- **Impacto:** cualquier app que adopte D1 valida con la
  semántica correcta en los dos estados (con y sin
  registros restaurados), y la declaración del repo de
  datos viaja con el sistema: un clon frío sabe dónde
  buscar los registros de su instancia. Evidencia de que
  la necesidad es real: My Channels, en su propia unidad
  de separación (cerrada la misma noche), ya declaró un
  puntero `repo_datos` en su `rameli.json` por su cuenta —
  dos apps inventando el mismo campo es la señal de que
  el campo debe ser del framework, no de cada app.
- **Riesgo:** bajo-medio — toca el validador del framework
  (chequeo 4) y el esquema de `rameli.json`; exige sus
  fixtures en la regresión del framework y versión nueva
  de Rameli. No toca datos ni operación de la tienda.
- **Orden:** 1 — cuando el dueño lo apruebe; nace como
  contribución desde esta app, no como parche local.

## P2 — Revisar las rutas del ritual de los lunes (H04)

- **Qué:** el cron `pod-ritual-lunes-h04` referencia
  bancos y fichas en `docs/investigacion/keywords/` y
  `docs/investigacion/nichos/` — rutas que no existen en
  este repo desde el reorden de datos (2026-10-19); su
  insumo real hoy vive en `data/tiendas/29222324/
  investigaciones/` y `data/banco-keywords/`. Revisar su
  cuerpo contra el layout vigente y corregir las rutas
  (o declarar el ritual retirado, si el flujo ya lo
  absorbió la investigación semanal). No commitea
  registros en `my-pod`, por lo que quedó fuera del
  inventario D1 de esta unidad; se detectó en su
  inventario de Paso 0.
- **Impacto:** el ritual vuelve a leer insumos reales (o
  deja de correr en vacío cada lunes).
- **Riesgo:** bajo — es un cuerpo de cron; el cuidado es
  no duplicar el trabajo de `equipo-pod-investigacion-
  semanal`, que corre el mismo lunes.
- **Orden:** 2 — con la palabra del dueño sobre si el
  ritual sigue vivo como flujo propio.

## Lo que esta fase NO propone

- Tocar la operación comercial (listings, ofertas,
  precios): esta fase es de sistema, como la migración
  que la abrió.
- Mover el esqueleto de datos: su forma actual
  (`.gitkeep` de hogares declarados, sin contenido) es la
  verificada en la prueba de frío de esta unidad; cambiarla
  es consecuencia de P1, no una propuesta separada.
- Reabrir D2: la decisión de respaldo quedó cerrada por
  el dueño el 2026-10-21 (registros → repo de datos;
  medios sin respaldo externo, por decisión explícita).

## Ejecución (2026-10-21, cierre de alineación v0.18.0)

- **P1 — EJECUTADA vía framework.** Contribución a Rameli
  por la vía de `CONTRIBUCIONES.md`: Rameli **v0.18.0**
  (PR #9, fusión `bbb587c`) trae el campo
  `datos.repo_datos` (forma canónica en
  `rameli/docs/DATOS-INSTANCIA.md` §4) y el ámbito de
  instancia por separación del chequeo 4, con su
  regresión (24 ok, 0 fallos). Esta app lo adoptó en su
  migración a v0.18.0: declaración en `rameli.json` y
  validación probada en los dos estados (instancia
  restaurada 0/0; clon de solo sistema sin FALLO de
  hogar, con AVISO; hogar parcial sigue FALLO). La
  brecha **B1-17 queda CERRADA**.
- **P2 — EJECUTADA en esta app.** Evidencia (corridas
  registradas del 2026-10-19): el ritual valida **un
  nicho por lunes** con el ritual H04 (veredicto +
  ficha + banco), mientras `equipo-pod-investigacion-
  semanal` produce la investigación general de la tienda
  (ledger, SEO, tendencias, top 5) — funciones y salidas
  distintas, **sin duplicación total**: el ritual sigue
  vivo como flujo propio y sus rutas se corrigieron al
  layout vigente (`data/banco-keywords/`,
  `data/tiendas/29222324/investigaciones/` y directriz,
  `docs-migrados/nichos/`), sumándole la mecánica de
  commit en la misma corrida que le faltaba. Detalle y
  tabla de mapeo: `docs/MIGRACION-RAMELI-V0180.md`.
