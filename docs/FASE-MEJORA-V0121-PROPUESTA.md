# Fase de mejora post-migración v0.12.1 — PROPUESTA (2026-10-19)

Abierta automáticamente al cerrar la migración a Rameli
v0.12.1, como manda `rameli/MIGRACIONES.md`, con la **auditoría
de adopción completa** como primer insumo — en esta migración
era **no diferible** (el delta trae capacidades nuevas) y se
corrió: `docs/AUDITORIA-ADOPCION-V0121.md`. **Este documento es
la propuesta: nada de lo siguiente se ejecuta sin el dale del
dueño, y con dale corre como fase propia (rama y puertas
propias), no como apéndice de la migración.** Si se difiere o
se rechaza, queda registrado aquí y reaparece en la siguiente
migración.

Punto de partida verificado en vivo el 2026-10-19: lint en
**cero** fallos, regresión **verde total** (47 casos), pin
0.12.1 vigente en todas las declaraciones vivas. Las brechas de
esta fase no son de formato ni de pin: son **una capacidad nueva
sin adoptar (B1)** y **una fuga de higiene que degrada la
confiabilidad de la regresión (B2)**.

## P1 — Adoptar la ruta de lectura por tarea (B1, C20)

**Qué cambia:** `FLUJO-PIPELINE.md` gana su sección de **ruta de
lectura**: por cada flujo vivo (F1–F9) y tipo de tarea, los
punteros puros a las lecturas mínimas gobernantes — skill
rector, doc que manda, ficha/registro que aplica — sin copiar
contenido. La sección "Skills activos" (hoy 4 de 9 skills) se
absorbe o se corrige en la misma pasada: la ruta es el índice
de lo vivo y su cobertura se verifica mecánicamente al cerrar:
**los 9 skills vivos aparecen en al menos una ruta y todo
puntero resuelve a un archivo existente** (las dos
comprobaciones que el canon declara).

**Impacto:** un orquestador o chat frío que retome la app sabe
qué leer para cada tarea sin inferirlo de inventarios viejos —
el modo de fallo exacto del caso origen del canon (un flujo
eliminado cuyo skill sobrevivió como "legacy" y gastó trabajo
real en dos migraciones). También convierte la ruta en el lugar
único donde retirar un flujo obliga a retirar su lectura.

**Riesgo: bajo.** Solo documentación, con punteros como único
contenido; mitigación: la verificación de cobertura y de
punteros resolviendo es mecánica y se corre antes de cerrar.

## P2 — Cerrar la fuga de temporales de `verificar-video.py` (B2, C5/C9)

**Qué cambia:** `scripts/verificar-video.py::extract_frames`
pasa de `tempfile.mkdtemp()` sin limpieza a un directorio con
ciclo de vida cerrado (`TemporaryDirectory()` o borrado en
`finally`, el patrón que `generar-video-listing.py` ya usa
bien). Y la suite que lo invoca gana un caso de higiene: tras
correr, no quedan directorios nuevos del script en el TMPDIR.
Ningún criterio de la puerta cambia: mismos frames, mismas
mediciones, mismos umbrales.

**Impacto:** las corridas de regresión dejan de fugar ~143 MB
por pasada; desaparece el modo de fallo ya observado en vivo
(hoy: 4 FAIL espurios en la suite de Pinterest con `/tmp`
lleno). La regresión vuelve a ser repetible en cualquier orden
y cualquier número de veces — condición para que un FAIL
signifique siempre "la puerta encontró algo".

**Riesgo: bajo.** Cambio acotado a la gestión del directorio
temporal de un helper; los frames ya viven en memoria tras la
extracción. Verificación: suite completa verde dos corridas
seguidas sin crecimiento de temporales.

## Orden sugerido

| Orden | Propuesta | Por qué ahí |
|---|---|---|
| 1 | **P2** — fuga de `verificar-video.py` | Fix conocido, rápido y seguro; toda verificación posterior (incluida la de P1 y cualquier corrida futura) depende de que la regresión no se corrompa por el ambiente. |
| 2 | **P1** — ruta de lectura en `FLUJO-PIPELINE.md` | Es la adopción que la nota de migración de v0.12.0 cobra en esta fase; documental, con su verificación mecánica propia. |

## Inventario arrastrado (decisiones del dueño, fuera de esta propuesta)

Reaparecen por la regla de la fase (registrados en
`docs/AUDITORIA-ADOPCION-V0121.md` §5), **no** forman parte de
las propuestas de ejecución de arriba:

- **Reactivación del cron `equipo-pod-propuestas-diarias`**
  (pausado desde 2026-10-18): con la puerta completa invocada,
  el flujo v2 vigente y el piloto Fase A en PASS, solo espera su
  dale.
- **Los 4 drafts con la incidencia neck** (p055 playera, p056
  sudadera, p057 ambos): esperan su decisión (recomendación
  registrada en el sistema: recrearlos duplicando un hermano
  sano, con dale nuevo).

De la fase post-v0.11.0 no queda nada abierto: sus cinco
propuestas cerraron (P5 por decisión del dueño, cuyo resultado
— las contribuciones — es hoy framework vigente v0.12.0/v0.12.1).
