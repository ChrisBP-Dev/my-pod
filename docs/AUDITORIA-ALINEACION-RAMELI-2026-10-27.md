# Auditoría de alineación a Rameli — flujo de dirección y decisiones de tienda

**Fecha:** 2026-10-27 · **Pedido del dueño:** antes de dar dale al
diseño F1 (`DISENO-MECANISMO-DECISIONES-TIENDA.md`), verificar si
ese diseño se alinea a los criterios del framework, si el framework
no estaba tan pulido como se creía, o si My POD nunca se aplicó
como debía. **Método:** lectura de los docs canónicos de Rameli
(v0.19.0) y del estado real de la app (skills, FLUJO-PIPELINE,
contratos, crons vivos, registros), con evidencia citada.
**Este documento REEMPLAZA la ruta del diseño F1** (que queda como
historia fechada en la misma rama, no como plan).

## 1. Lo que Rameli SÍ prescribe (el framework no está vacío)

1. **Capas y prueba de colocación:** mecanismo → framework/app
   (skills); valores → ficha de la unidad. (`AGENTS.md` global;
   `rameli/docs/DATOS-MULTIUNIDAD.md` §2.)
2. **Un skill declara propósito, entradas, salidas y puerta
   mecánica.** Intake de la fábrica de skills, Fase 2: «N skills
   atómicos: propósito declarado, entradas, salidas y puerta
   mecánica de cada uno. **El que no declara su puerta no
   existe**.» (`rameli/skills/fabrica-skills/INTAKE.md`.)
   Extensiones del formato: puertas mecánicas declaradas, reglas
   con motivo, «helpers antes que prosa» — lo mecánico vive en
   `scripts/`, no en párrafos. (`rameli/docs/formato-skills.md`.)
3. **Las decisiones viven en el sistema, con hogar asignado:**
   doctrina de workers — «las decisiones y los veredictos del
   dueño, con fecha» son contenido mínimo del **registro de
   flujo** versionado; la **ficha declara** los valores y las
   puertas que gobiernan la unidad, y todo brief se corta en
   ellas. «El chat no es la memoria del flujo.»
   (`rameli/docs/EJECUCION-POR-WORKERS.md`.)
4. **Datos multi-unidad:** hogar por unidad declarado en el mapa
   de `rameli.json`; «el registro referencia; no copia»; ciclo de
   vida de activos. (`DATOS-MULTIUNIDAD.md`.)
5. **`rameli validar` verifica COLOCACIÓN, no contenido ni
   consumo.** Su propio doc: «Lo que la puerta no puede ver — si
   el contenido de un hogar es correcto… — lo cubre el protocolo
   de cierre (inventario + prueba de frío).»
   (`VALIDACION-COLOCACION.md` §3.1/§4.) **Un validar en verde
   nunca significó «los flujos consumen bien las decisiones»**;
   tratarlo así fue un error de lectura nuestro, no una promesa
   del framework.

## 2. Lo que Rameli NO prescribe (hueco real del framework)

- Ningún estándar de **«línea estratégica vigente de una
  instancia»** como sección de ficha: la ficha declara valores,
  pero no hay patrón canónico para «esto es una línea abierta del
  dueño, con estado, hasta que él la cierre» ni para cómo una
  salida periódica (directriz semanal) debe **reflejarla**.
- Ninguna **puerta de consumo**: el intake exige declarar
  entradas/salidas por skill, pero nada verifica que la salida de
  un productor sea entrada declarada de su consumidor, ni que un
  valor de ficha declarado llegue al artefacto que debe
  ejecutarlo. La ruta de lectura por tarea (que My POD adoptó en
  `FLUJO-PIPELINE.md`) es un doc de la app, manual.
- Nada sobre **inventario de agendas de una app**: las agendas
  (crons) viven en el sistema de scheduling del entorno, fuera
  del repo de la app; el framework no declara quién las inventaría
  ni cómo se audita que su cuerpo sigue al skill vigente (el caso
  B3 de My POD ya demostró la deriva).

Conclusión parcial: el framework está pulido en colocación,
formato y ejecución por workers; **está incompleto en consumo
declarado↔consumido y en líneas vigentes de instancia**. Por la
vía de `CONTRIBUCIONES.md`, eso se corrige primero en la app como
adopción y se propone upstream documentado — no inventando en la
app un sistema paralelo.

## 3. Lo que My POD SÍ tiene alineado (los buenos resultados eran reales)

- **Ruta de lectura por tarea** (`FLUJO-PIPELINE.md`, adoptada
  2026-10-19 del canon de la fábrica): por flujo, las lecturas
  gobernantes — es el índice «quién lee qué» de la app.
- **Estratega** declara 10 entradas y su salida dual
  (directriz + config) con la regla «deben decir lo mismo»;
  investigación escribe en `investigaciones/` y la estratega la
  consume el mismo lunes; el contrato
  `CONTRATO-TIPO-PRODUCTO.md` tipa la salida semanal.
- **Puertas mecánicas con evals** en los skills de producción;
  **registro-flujo** adoptado de la plantilla de Rameli;
  **prueba de frío** ejecutada (2026-10-23);
  **INVENTARIO-VALORES-FICHA** (valor → consumidor → paso
  productor); **PUERTA-CIERRE** de la app (2026-10-23: colocación,
  consumidores alineados, huecos hacia adelante) — la app tiene
  más disciplina de cierre que el mínimo del framework.

El flujo que el dueño describe (calibración → investigación que
consume la ficha → estratega que revisa lo investigado →
propuestas que leen directriz y ficha → puerta que juzga con
criterio de ficha) **es exactamente el flujo F4→F1 de esta app**
y funcionó: de ahí salieron los lotes con esencia que él aprobó.

## 4. Dónde My POD NO está alineado (evidencia)

**A. La investigación no es un skill: es una agenda con prompt.**
El cron `equipo-pod-investigacion-semanal` vive en el workspace
del goal (fuera del repo de la app), y su cuerpo **hardcodea** la
ruta de la tienda y hasta el nicho («tendencias del nicho
(enfermería)») en vez de leer la ficha; no instruye leer
`config.json` (nicho, líneas, decisiones). La estratega, en
cambio, sí es skill y su cron se limita a invocarlo («leerlo
completo antes de actuar») — el patrón correcto ya existe en la
misma app; la investigación es la excepción. Contra el intake:
un rol sin skill que declare entradas/salidas/puerta no existe
como sistema — existe como prompt en una agenda. Es el mismo
patrón ya cazado dos veces en esta app: F7 sin dueño (auditoría
v0.11.0, B6) y el cron de propuestas desactualizado frente a la
puerta (B3: «el skill está bien; el consumidor quedó atrás»).

**B. Las decisiones del dueño dejaron de entrar a su hogar.**
El `registro-flujo.md` de la tienda se adoptó el 2026-10-19 y su
sección «Decisiones y veredictos» **se detiene el 2026-10-19**:
ninguna decisión del 20–27 de octubre (piloto de personalización,
bordado plano, veredictos del piloto, Etapa 7) entró ahí. La
doctrina de workers lo asigna ahí y a la ficha; en la práctica
vivieron en notas del config semanal, en docs de fase y en
conversación. El registro existe; **dejó de mantenerse**, y
ninguna puerta mide su frescura.

**C. La colocación del estado de personalización fue una
decisión de la app, no del framework.** La fase de
personalización (2026-10-20) colocó «cupo + tabla del piloto» en
`config-propuestas.json` y el contrato semanal ganó el campo
`personalizados.estado` como estado canónico
(`docs/FASE-PERSONALIZACION.md`, tabla «Qué quedó escrito y
dónde»). Un estado permanente dentro de un artefacto de 7 días
contradice la lógica de capas de la propia app (la ficha manda;
la directriz obedece) — y se hizo **antes** de que existiera la
PUERTA-CIERRE (2026-10-23), que es la puerta que lo habría
cazado. El `INVENTARIO-VALORES-FICHA.md` aún lista la
personalización como «pendiente_investigacion / sin configurar»:
el inventario también quedó viejo sin que nadie lo notara.

**D. Hardcodeo de instancia en el mecanismo.**
`FLUJO-PIPELINE.md` nombra `data/tiendas/29222324/…` literal en
su ruta de lectura (12 menciones) en vez de `<tienda-id>`; los
cuerpos de cron también. Con una segunda tienda, la ruta de
lectura — el índice maestro — apunta a la tienda equivocada.

## 5. Qué sobra y qué se corrige del diseño F1

**Sobra (duplica mecanismos existentes):** el registro nuevo
`decisiones_estrategicas` como sistema paralelo y la puerta
nueva como artefacto separado. Las decisiones ya tienen hogar
(registro-flujo + ficha), el «quién lee qué» ya tiene índice
(ruta de lectura), y el «consumidor alineado» ya es ítem de la
PUERTA-CIERRE.

**Se conserva (el hueco genuino, §2):** que nada verifica, al
cerrar la estratega cada semana, que una línea vigente de la
ficha llegue al contrato semanal. Eso es un **helper + un ítem
de cierre en los dueños existentes**, no un sistema nuevo.

## 6. Ruta corregida propuesta (alineación primero; para su dale)

1. **Ficha manda (sin esquema nuevo):** el estado de cada línea
   vigente de la tienda vive en `config.json` siguiendo el patrón
   ya existente de `estrategia_precios` (bloque con nota «decisión
   del dueño <fecha>», estado, última calibración,
   `recalibrar_si`). Personalización y bordado se declaran ahí;
   `config-propuestas` conserva solo la **asignación semanal**
   (cuánto esta semana) y pierde el rol de estado canónico
   (enmienda al `CONTRATO-TIPO-PRODUCTO.md`).
2. **Registro-flujo al día y con dueño:** se backfillean las
   decisiones 2026-10-20→27; la corrida de la estratega lo
   actualiza al cerrar cuando hubo dale (se declara en su skill,
   que ya declara «escribir = commitear»).
3. **Investigación se vuelve skill de la app**
   (`investigacion-tienda`): entradas = ficha (nicho, líneas
   vigentes), registro, ledger; salida = `investigaciones/` con
   PROP-INV que citan la línea de ficha que tocan o piden alta;
   puerta = el reporte existe, cita sus fuentes de ficha y no
   re-propone lo ya decidido. El cron se reduce a invocarlo,
   como ya hace el de la estratega. **El inventario de agendas
   de la app se declara en `FLUJO-PIPELINE.md`** (qué agenda
   invoca qué skill), para que la deriva tipo B3 sea detectable.
4. **Chequeo de consumo en el cierre existente:** helper en
   `scripts/` de la app — línea de ficha `operativa|piloto` con
   asignación 0 o ausente en el config semanal sin nota de pausa
   = fallo — invocado por el cierre de la estratega y listado en
   la PUERTA-CIERRE. Calibrado en ambos sentidos contra el estado
   real de hoy (debe fallar: cupo 0) y el estado corregido.
5. **Des-hardcodeo de la ruta de lectura:** `29222324` →
   `<tienda-id>` + declaración de tienda activa, en
   `FLUJO-PIPELINE.md` y cuerpos de cron del equipo POD.
6. **Contribución a Rameli (documentada, separada):** patrón
   «línea vigente de instancia en la ficha + chequeo de consumo
   en la salida periódica» y «agenda que invoca skill vs agenda
   con prompt», por `CONTRIBUCIONES.md`. No se aplica al
   framework en esta unidad.

Con esto, F2 (declarar los focos) se ejecuta sobre los puntos
1–2, F3 (datos/investigación) sobre el 3, y F4 (estratega) cierra
con el 4 corriendo. F5–F7 sin cambio.

**EJECUCIÓN (2026-10-27, dale del dueño a esta ruta; rama
`recalibracion-decisiones-tienda`, pendiente de su palabra para
fusionar):** los 6 puntos ejecutados — (1) líneas en la ficha
(commit de datos `a06705a`+corrección de formato `a1ac125`),
CONTRATO enmendado, INVENTARIO corregido; (2) backfill del
registro-flujo (commit de datos `bafd8c2`) y dueño de
actualización declarado en `estratega-tienda` v0.8.0; (3) skill
`investigacion-tienda` v1.0.0 con puerta
`scripts/verificar-investigacion.py` (suite 7/7) y la agenda
reducida a invocarlo (verificado por `cron.view`); inventario
de agendas en `FLUJO-PIPELINE.md`; (4) helper
`scripts/verificar-consumo-lineas-tienda.py` calibrado en ambos
sentidos (FAIL contra el config real previo al arreglo, PASS
contra el estado alineado; casos permanentes en la suite de la
estratega) e integrado a su cierre y a la PUERTA-CIERRE;
(5) ruta de lectura sin id en duro + declaración de tienda
activa; (6) contribución documentada en
`docs/CONTRIBUCION-RAMELI-CONSUMO-Y-LINEAS.md`, sin aplicar al
framework. Verificación: lint VERDE (10 skills), regresión
completa VERDE, `rameli validar` 0/0, helper en vivo PASS.

## 7. Veredicto en una línea por capa

- **Framework:** sólido en colocación/formato/workers;
  incompleto en consumo y líneas vigentes (§2) — se le propone,
  no se le parchea desde la app.
- **Aplicación:** el flujo y sus criterios existen y son los que
  produjeron los buenos resultados; la desalineación es
  concreta y chica: una agenda sin skill (investigación), un
  registro adoptado y abandonado (registro-flujo), un estado
  colocado en el artefacto semanal (personalización, 2026-10-20)
  y hardcodeo de instancia en la ruta maestra.
- **Mi diseño F1:** acertó el síntoma y el hueco de consumo;
  erró el remedio al inventar un registro paralelo sin auditar
  primero los hogares que el framework y la app ya asignan.
  Queda supersedido por esta ruta.
