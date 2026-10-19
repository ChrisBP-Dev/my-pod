# Migración a Rameli v0.11.0 — registro de ejecución (2026-10-19)

Pedido del dueño 2026-10-19: migrar en un chat nuevo, como prueba de
que el sistema escrito basta para hacerla bien. Ejecutada en worktree
aislado sobre la rama `migracion-rameli-v0110` (el árbol principal
tenía artefactos sin commitear de la corrección de recortes MPL),
según `rameli/MIGRACIONES.md` y el CHANGELOG v0.9.0 → v0.11.0 del
framework (v0.10.0: ejecución por workers + contribuciones, aditivo;
v0.11.0: fase de mejora post-migración; sin cambios rompientes, sin
cambios de datos ni de comportamiento). Delta confirmado además con
`rameli migrate --to 0.11.0`. **Fusión a main: pendiente del dale
explícito del dueño en el chat de la migración.**

## Alcance aplicado

- `rameli.json`: pin 0.9.0 → 0.11.0 + nota de migración.
- `README.md`: pin, sección de esta migración, bullet de adopción de
  workers en Principios operativos, y dos celdas de versión de la
  tabla corregidas contra su SKILL.md (patrón del precedente v0.9.0):
  `estratega-pinterest` v0.1.0 → v0.1.1 y `puerta-arte-propuesta`
  v0.4.0 → v0.5.0 (desactualizadas desde antes de esta migración).
- Los 10 skills: `framework_version: "0.11.0"` en su frontmatter.
- Dos CHANGELOG de skill cuya primera línea es una declaración viva
  de pin ("Pineado a Rameli v0.9.0") actualizados a v0.11.0
  (puerta-arte-propuesta, puerta-pinterest-pin). Las entradas
  fechadas de los demás CHANGELOG son historia y no se tocaron.
- Registro de adopción del modelo de workers (sección siguiente).
- El gemelo máquina de la ficha de la tienda (`config.json`) NO
  cambió de nombre ni de formato. Ningún dato se tocó: el diff de la
  rama contiene 0 archivos bajo `data/`.

## Registro de adopción — ejecución por workers (nota v0.10.0)

La nota de migración v0.10.0 manda adoptar el modelo **por flujo y
deliberadamente**, no como requisito. Estado por flujo de esta app:

**Adoptado — ya operaba así, se declara:**
- **Publicación de lote** (`publicador-lote`): un lote = un side
  chat = un worker frío = un reporte; el manifiesto explícito del
  dueño hace de brief y el checkpoint fino vive local en
  `data/estado-publicacion.json` (gitignoreado — la capa que el
  framework distingue del registro de flujo). No usa la plantilla
  `templates/registro-flujo.md`: para un flujo de una sola corrida
  por lote, manifiesto + checkpoint + reporte son el registro.
- **Crons diarios** (propuestas, Pinterest): workers programados;
  sus insumos versionados (`data/config-propuestas.json`,
  `data/direccion-tienda.md`, ficha de la tienda) hacen de brief
  permanente; checkpoints locales `data/estado-*.json` con resume
  (patrones P1/P2/P3 de `docs/PATRONES-RESILIENCIA.md`); entrega en
  chat nuevo según `docs/REGLA-DELIVERY-CHATS.md`; el flujo de
  propuestas lleva watchdog (orden del dueño, 2026-10-18).
- **Investigación y estrategia semanal**: la producción de los
  reportes corre en workers de cron; la deliberación y los
  veredictos quedan en el chat principal con el dueño — fuera del
  worker, como manda el propio documento del framework.

**Adoptado desde esta migración:**
- **Flujos ad-hoc multi-paso** (reparaciones, auditorías,
  migraciones): brief limpio, ejecución en chat nuevo y registro en
  el repo. Evidencia inmediata: esta misma migración.
- **Relevo del orquestador**: el estado de los flujos continuos vive
  en el repo (dirección, checkpoints, registros), no en el hub; el
  hub puede rotar entre fases sin perder el flujo. Umbral concreto
  de rotación: sin fijar todavía (calibración, ver fase de mejora).

**No adoptado — con motivo (queda para el inventario de mejora):**
- **Puertas** (arte-propuesta, publicación, Pinterest): son gates
  mecánicos que corren DENTRO de cualquier flujo, no unidades de
  producción. Vía directa siempre.
- **Tareas de 1–2 pasos** (precios por API, consultas, correcciones
  acotadas): el propio documento del framework las excluye; montar
  un worker ahí es ceremonia sin beneficio.
- **Conectar Etsy API por tienda**: flujo interactivo — el paso
  OAuth exige el clic del dueño y credenciales en vivo; se ejecuta
  guiado con el dueño presente, no con un worker desatendido. Se
  re-evalúa si se conecta una segunda tienda.
- **Onboarding de tienda**: flujo por fases con decisión del dueño
  en cada una (nicho, nombre, branding) — hoy guiado. Los crons que
  el onboarding crea sí nacen bajo el modelo (worker + checkpoint +
  watchdog según su propia tabla).
- **Registro de flujo versionado único** (plantilla
  `templates/registro-flujo.md`) para los flujos continuos de
  propuestas y Pinterest: hoy su estado se reconstruye de checkpoint
  local + reportes diarios + dirección de tienda. Adoptar la
  plantilla es un cambio de comportamiento: pertenece a la fase de
  mejora, no a esta migración de alcance cerrado.

## Verificación (antes vs después, mismo árbol: el worktree)

- `rameli lint` sobre los 10 skills: salida **idéntica byte a byte**
  antes y después (3 VERDE: las tres puertas; 17 fallos repartidos en
  los otros 7 skills: conectar-etsy-api 2, estratega-pinterest 4,
  estratega-tienda 3, onboarding-tienda 3, paquete-listing-etsy 1,
  publicador-lote 3, publicar-printify-etsy 1). La migración
  introduce cero fallos nuevos. El lint sobre el árbol principal
  vivo dio el mismo resultado (17) antes de crear el worktree.
- Regresión (`rameli test`): salida **idéntica byte a byte** antes y
  después en el worktree — puerta-arte-propuesta 13 ok / 0 fallas;
  puerta-publicacion-pod 12 ok / 6 fallas (las mismas 6 G1
  preexistentes); puerta-pinterest-pin 11 ok / 4 fallas "asset no
  registrado como FINAL" (p030, p032, p034) porque el worktree lee
  el registro commiteado y no el estado vivo — sobre el árbol
  principal la misma suite da 15/15, verificado en el ANTES.
  Diferencia de datos entre árboles, no de la migración (mismo
  fenómeno registrado en la migración v0.9.0).
- Barrido final de pin viejo: `0.9.0` solo queda citando el delta o
  como historia — la sección histórica de migración v0.9.0 del
  README, el registro `docs/MIGRACION-RAMELI-V090.md`, este registro
  y la nota de adopción fechada 2026-10-18 en `rameli.json`. Ninguna
  declaración viva queda en 0.9.0.

## Huecos del sistema detectados (esta migración es también su prueba)

1. **Del framework:** `rameli/docs/EJECUCION-POR-WORKERS.md` en main
   (v0.11.0) conserva el encabezado "PROPUESTA v2 — rama
   `contribucion-ejecucion-por-workers`, 2026-10-18", aunque la
   contribución se integró (PR #1 → v0.10.0) y la rama se borró. Un
   lector frío no puede saber desde el propio documento que es
   doctrina vigente; lo supo por el CHANGELOG y MIGRACIONES. La
   corrección le toca al framework por la vía de CONTRIBUCIONES, no
   a esta aplicación.
2. **Del framework (menor):** `bin/rameli` está versionado con modo
   100644 (sin bit de ejecución) aunque README y MIGRACIONES lo
   presentan como ejecutable directo; en la práctica se invoca
   `bash bin/rameli`.
3. Todo lo demás necesario **sí estaba escrito**: proceso
   (MIGRACIONES.md), delta (CHANGELOG + `rameli migrate`), nota de
   adopción por flujo, plantillas y precedente de forma. Ningún
   hecho de esta migración salió de fuera de los repos y el brief.

## Deuda preexistente que la migración NO toca (inventario de la fase de mejora)

Al cerrar esta migración se abre la **fase de mejora** que manda
`rameli/MIGRACIONES.md` (v0.11.0): su primer entregable es la
PROPUESTA al dueño; nada se ejecuta sin su dale aparte. Inventario
de partida, verificado en vivo en esta migración:

- Los **17 fallos de lint** en 7 skills (descripciones sobre el
  máximo de 220 caracteres y secciones "Cuando usarme" / "Puertas
  mecánicas" ausentes en skills anteriores al lint), con el reparto
  por skill de la sección de verificación.
- La regresión de **puerta-publicacion-pod: 6 casos G1 en rojo**,
  idénticos antes y después.
- La divergencia entre el registro commiteado y el estado vivo que
  hace fallar 4 casos de puerta-pinterest-pin fuera del árbol
  principal (assets FINAL de p030/p032/p034 no commiteados).
- Los **no adoptados** del registro de adopción: plantilla de
  registro de flujo para flujos continuos, watchdog explícito en
  `publicador-lote` (su skill no lo declara; el cierre hoy depende
  de que el orquestador vuelva), y el umbral de relevo del
  orquestador sin calibrar.
