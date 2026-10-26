# Propuesta — Vitrina de lectura en vivo (sin siembra)

**Pedido del dueño (2026-10-26):** reemplazar el mecanismo interno de la
vitrina de revisión por el modelo ya logrado en My Channels con el Centro
de gestión — lectura en vivo del repositorio, sin sembrado — preservando
intactos su aspecto visual y su gestión. Alcance de esta etapa: **solo la
vitrina**. La migración mayor (gestión a nivel tienda, con la configuración
de la tienda visible y sus flujos ahí) es etapa posterior; esta deja su base.

**Estado:** **F0 DADO por el dueño (2026-10-26, con las dos decisiones
de §8 aceptadas como recomendadas)** y **F1 EJECUTADA** el mismo día en
esta rama (verificación en el commit de F1): el puente
`registros-datos.py` reclasificó `estado-propuestas.json` como
registro y las previas del hogar declarado como entregable
versionable; el repo de datos ya versiona el estado vivo y el
registro de decisiones vacío (commit `7b79083` en su `main` — ese
repo commitea sus registros a main por su propio flujo, y el cambio
es inerte hasta que esta rama se fusione); `puerta-arte-propuesta`
v0.9.0 trae la entrega y la recogida-aplicación nuevas; el contrato
vive en `docs/VITRINA-VIVA.md`. La vitrina viva no se ha tocado; su
bandeja está en cero (verificado hoy por `getboard`: 0 diseños, 0
decisiones), así que el corte no pone en riesgo ninguna decisión en
curso. Sigue F2 (construcción en ensayo) con la puerta de fase
cumplida.

---

## 1. Auditoría — cómo funciona hoy la vitrina (evidencia, 2026-10-26)

La cadena vigente (plantilla v2.3, `docs/VITRINA-REVISION.md`; skill
`puerta-arte-propuesta` §§«Entrega» y «Recogida») tiene **cinco saltos**
entre que un arte pasa la puerta y que la decisión del dueño queda firme
en el sistema:

1. **Generación del paquete.** `scripts/generar-datos-vitrina.py` (294
   líneas) lee el registro y el checkpoint locales, parte el porqué,
   mide el PNG y compone las previas (fondo oscuro/claro) →
   `datos-vitrina.json` + JPGs sueltos en una carpeta de trabajo.
2. **Compilación de previas en la instancia.** Las previas no viajan con
   la siembra: viven **horneadas en el código de la instancia**
   (`client/src/assets/`, 6,5 MB medidos hoy para el lote piloto). Cada
   lote nuevo y cada regeneración exigen **editar la instancia** para
   compilar la previa de ese `arte_ref` antes de sembrar; sin ese paso,
   la vitrina muestra «Previa de esta versión aún no cargada».
3. **Siembra.** La acción `seedlote` inserta los diseños en la **base de
   datos propia del artefacto**. La instancia declara 9 acciones
   (`getboard`, `seedlote`, `setdecision`, `savenota`, `cleardecision`,
   `enviardecisiones`, `leerdecisiones`, `leerestadorevision`,
   `confirmarrecogida`): todo el estado de revisión vive ahí, no en el
   sistema.
4. **Decisiones en el artefacto.** El dueño decide y marca listas; las
   decisiones quedan **solo en la BD de la instancia** hasta que alguien
   las recoge (el propio sistema ya vigila este riesgo: «decisiones
   enviadas sin recoger por más de 24 h = alerta», porque viven solo en
   la vitrina).
5. **Recogida manual por chat.** Con el aviso del dueño, Jarvis lee
   `leerdecisiones`, valida, vuelca al checkpoint
   (`estado-propuestas.json`) y al registro, commitea, y confirma con
   `confirmarrecogida` para que aprobados/rechazados salgan de la
   instancia y los «mejorar» queden en espera.

**Costos y riesgos verificados de este modelo** (todos ya ocurridos, no
hipotéticos): la resurrección del lote recogido (2026-10-22, la instancia
se auto-sembró al abrir vacía → regla de siembra correctiva); la previa
vieja servida como «Nueva versión» si no se compila antes (hueco
fundacional del retorno de mejora); decisiones huérfanas si nadie recoge;
doble fuente de verdad (BD del artefacto vs checkpoint) con su cruce
obligatorio antes de reportar conteos. Es el mismo patrón que en My
Channels se declaró **compensatorio y caducado**: la siembra nació
porque la superficie no podía leer la realidad; hoy sí puede.

## 2. Qué ya está listo en el repo de datos (mapa campo a campo)

El contrato de entrada de la vitrina se alimenta, campo a campo, de
fuentes que **ya viven versionadas** en `ChrisBP-Dev/my-pod-datos`
(verificado hoy: `registro-listings.json` y `config.json` de la tienda
29222324 idénticos entre la copia local y el repo de datos, mismo hash):

| Campo de la vitrina | Fuente en el repo de datos | Estado |
|---|---|---|
| `titulo`, `tema`, `producto_destino` (`tipo`/`track`), `fecha` de lote | `data/tiendas/<id>/registro-listings.json` → entrada del diseño | ✅ versionado |
| Porqué en secciones (tema/ángulo, frase, iconografía, qué mirar) | `porque` de la entrada (marcadores ya canónicos; el partirlo es derivación del servidor, como hoy lo hace el generador) | ✅ versionado |
| `puerta` | `nota_puerta` de la entrada | ✅ versionado |
| `personalizable`, `simulacion`, `ficha_razon` | Entrada del registro (contrato ya cerrado en `puerta-arte-propuesta` v0.8.6) | ✅ versionado |
| Tienda (id, nombre) y declaración de la instancia | `data/tiendas/<id>/config.json` (bloque `vitrina`) | ✅ versionado |
| Etiquetas y frase corta | Derivación determinista del porqué/tema (misma lógica del generador, movida al servidor de la instancia) | ✅ derivable |

**Conclusión parcial:** el lado de texto está listo. Un artefacto con el
conector de GitHub declarado (lectura) puede servir hoy mismo todo el
contenido editorial de la vitrina desde el repo de datos, como el Centro
lee `my-channels-datos` (contrato `CENTRO-GESTION-VIVO.md`: HEAD fijado
por apertura con `list_commits`, sello «Leído en vivo», lista blanca de
campos, ≈1,6 s por llamada medidos en su R0).

## 3. Los tres huecos que bloquean la lectura en vivo (y su corrección de flujo)

Un hueco es un defecto del flujo, no del caso: cada corrección de abajo
recalibra el flujo que produce la fuente **y** produce el faltante del
caso vivo, en el mismo cierre.

### H1 — El estado de la bandeja no vive en el repo de datos

`estado-propuestas.json` — el checkpoint que dice qué está entregado,
pendiente, aprobado, en mejora y recogido — está **ignorado por git en
ambos repos** (línea expresa en los dos `.gitignore`): existe solo como
archivo local. Sin él en el repo, ninguna superficie puede derivar la
bandeja en vivo. Su exclusión es una decisión compensatoria de cuando
los «estados» se trataban como estado local de corrida (como
`estado-pinterest.json`); el estado de propuestas no es eso: es el
registro del que dependen la bandeja, la Fase B y los conteos.

**Corrección:** `estado-propuestas.json` pasa a versionarse en el repo
de datos (`data/tiendas/<id>/`), sale de ambos `.gitignore` para esa
ruta, y se commitea el archivo vivo actual (lote 2026-10-19 cerrado:
10 aprobados, 10 producidos, mejoras cumplidas — entra ya en su estado
real). Los otros estados (`pinterest`, `publicacion`) no se tocan: no
son fuente de esta superficie.

### H2 — Las previas no viven en ningún repo

La política de medios manda que los binarios nunca se versionen, y el
arte de producción (PNG 300 dpi) cumple esa política: vive local. Pero
la **previa de revisión** no es el medio de producción: es un entregable
de la puerta, ligero y determinista (medido hoy: 160–290 KB por JPG a
1.100 px, muy por debajo del umbral de ~1 MB del contrato en vivo).
Hoy ese entregable se hornea en el código del artefacto — el peor de
los hogares: invisible al sistema, exige editar la superficie por lote.

**Corrección:** el paso de **entrega** del flujo (en
`puerta-arte-propuesta`, donde hoy se genera el paquete) pasa a
**producir las previas como entregable en el repo de datos**, en hogar
declarado: `data/tiendas/<id>/propuestas/<slug>/previa-oscura.jpg` y
`previa-clara.jpg` (y las de simulación en personalizables, mismo
hogar). Requiere una **excepción acotada** en el `.gitignore` del repo
de datos para ese hogar (solo `propuestas/**/previa-*.jpg` y
`simulacion-*.jpg`); el PNG de producción sigue sin versionarse y la
política de medios queda intacta para todo lo demás. La puerta
mecánica del generador **sobrevive mudada**: la entrega valida antes
de commitear: un personalizable sin simulación o sin ficha completa
**falla la entrega** y nunca llega a la bandeja disfrazado de normal.
...[truncated 10964 chars]
### H3 — Las decisiones viven solo en la base de datos del artefacto

Hoy decidir = escribir en la BD de la instancia; el sistema se entera
recién en la recogida. Es el eslabón que hace posible todo lo demás:
sin decisiones en el sistema no hay bandeja derivable, y con recogida
manual hay ventana de pérdida y doble verdad.

**Corrección — se adopta la ruta C del Centro, ya probada:** la
vitrina declara el conector de GitHub también con escritura, acotado
al repo de datos, y su **única escritura** es un registro append-only
por tienda: `data/tiendas/<id>/vitrina/decisiones.json` (lista de
`{id, fecha, slug, accion, nota, estado}`, con `estado` en
`sin-marcar | lista | aplicada | devuelta` y `commit_aplicacion`
cuando el skill la aplica). La interfaz jamás escribe otro archivo:
ni el registro, ni el config, ni el estado — esos los mueve el flujo,
con sus validaciones, en la recogida-aplicación.

## 4. El modelo nuevo (contrato, en breve)

- **Lectura (una acción, `getboard`):** fija el HEAD del repo de
  datos, lee `config.json` + `registro-listings.json` +
  `estado-propuestas.json` + `vitrina/decisiones.json` de la tienda,
  deriva la bandeja (pendientes / aprobadas / rechazadas / por
  mejorar / esperando regeneración) en el servidor con lista blanca
  de campos, y sirve las previas desde su hogar en el repo (caché de
  bytes por SHA de blob, como manda el contrato en vivo del Centro:
  los datos derivados se leen en vivo en cada apertura; solo los
  bytes inmutables se cachean). Responde con el sello «Leído en vivo
  · commit `<sha-corto>`».
- **Decidir:** cada toque escribe **al instante** en
  `decisiones.json` con un solo commit (fusión por `id`; conflicto de
  SHA: relee, refusiona y reintenta **una** vez; segundo choque: la
  decisión **no queda en pie** y la vista lo muestra fallido con su
  causa — nunca como guardado). Ritmo medido del patrón en el Centro:
  ~13 s por escritura; la vista muestra el estado de escritura sobre
  la tarjeta, sin bandeja de guardado ni botón global.
- **Marcar listas:** un commit que pasa las decisiones del dueño a
  `lista`. El recibo y el mensaje copiable se conservan tal cual:
  siguen siendo la señal que dispara la recogida.
- **Recogida-aplicación (en el skill, no en la superficie):**
  `puerta-arte-propuesta` lee las decisiones `lista` **directo del
  repo** (ya no invoca acciones del artefacto), las aplica con las
  validaciones e idempotencia vigentes hoy, actualiza
  `estado-propuestas.json` y el registro, y marca cada decisión
  `aplicada`/`devuelta` + `commit_aplicacion` en el mismo commit.
  Aprobados y rechazados salen de la bandeja **por derivación** (su
  estado en el repo ya no es «entregado»): no hay
  `confirmarrecogida`, ni purga en una BD ajena, ni resurrección
  posible — el vacío se deriva, no se administra.
- **Multitienda:** el mecanismo es el mismo para toda tienda; cada
  instancia declara en su `config.json` (bloque `vitrina`) repo +
  tienda. La instalación de una tienda nueva incluye declarar el
  conector sobre el repo de datos y el hogar de previas (esto cierra
  además el hueco ya registrado en `INVENTARIO-VALORES-FICHA.md`: el
  alta de la vitrina no era paso explícito del onboarding).

## 5. Qué NO cambia (piso de la fase)

- Los 9 principios de UX y toda la presentación de la plantilla v2.3:
  vistas (Pendientes inicial; aprobadas / rechazadas / por mejorar),
  tarjeta y detalle, conmutador segmentado «Fondo: Oscuro / Claro»,
  visor con zoom focal, arte completo sin recorte, progreso visible,
  variante personalizable con sus dos imágenes etiquetadas y su ficha.
  **Cambia el motor, no la forma** (regla de paridad visual del
  Centro: la referencia es la instancia vigente tal cual se ve).
- La gestión: bandeja continua, lotes aditivos, todo editable hasta
  la recogida, «Marcar listas para Jarvis» como bandera (ahora sobre
  el repo), recibo copiable, nuevas versiones con la nota anterior
  visible y distintivo «Nueva versión».
- La vitrina sigue siendo la **superficie única** de la aprobación
  creativa de la Etapa 1; el chat solo avisa, sin artes. Nada se
  produce desde la vitrina; la Fase B sigue produciendo solo lo
  aprobado y recogido.
- La política de medios para el arte de producción (PNG local, sin
  versionar) y el repo del sistema sin datos de instancia.

## 6. Fases (cada una cierra con su puerta; nada se fusiona sin su palabra)

- **F0 — Dale de este plan** (incluye la excepción acotada de previas
  en el repo de datos, §3-H2, y el ritmo de escritura al instante,
  §4).
- **F1 — El repo primero (los flujos guardan bien).** H1 + H2 +
  contrato de `decisiones.json` escritos donde viven: `.gitignore` de
  ambos repos ajustados para las rutas exactas, `estado-propuestas`
  vivo commiteado en datos, paso de entrega de `puerta-arte-propuesta`
  reescrito (produce previas al hogar declarado + valida
  personalizables + registra entregados en el estado, todo commiteado
  en la misma corrida), y `docs/VITRINA-VIVA.md` como contrato nuevo
  (los §§ de UX de la plantilla v2.3 se conservan verbatim; mueren
  los contratos de paquete/siembra). Sin tocar la instancia viva: la
  vitrina actual sigue operando con su flujo hasta el corte.
- **F2 — Construcción de la instancia viva (en ensayo).** Nueva
  instancia con la presentación v2.3 reproducida y el conector de
  GitHub (lectura + escritura, solo repo de datos): `getboard`,
  escritura instantánea de decisiones y marcar-listas. Se monta como
  instancia **de ensayo** sobre la misma tienda (la bandeja real está
  en cero: no hay decisiones que migrar).
- **F3 — Prueba de ciclo completo en ensayo.** Un diseño de ensayo
  (declarado como tal, fuera del registro de producción o marcado
  `sandbox`) recorre: entrega por el flujo nuevo → aparece solo, sin
  siembra → decisión + nota → marcar listas → recogida-aplicación
  por el skill → bandeja derivada en cero al reabrir (vacío terminal,
  sin resurrección, verificado reabriendo) → regeneración del mismo
  diseño como «Nueva versión» con previa nueva servida desde el
  repo. QA responsive (teléfono, tablet, desktop + WebKit móvil) con
  evidencia, caminando la presentación v2.3 decisión por decisión.
- **F4 — Corte.** El bloque `vitrina` del `config.json` apunta a la
  instancia nueva; la instancia sembrada se retira. Barrido de
  remanentes del flujo descartado (se eliminan, no se conservan):
  `scripts/generar-datos-vitrina.py`, las acciones de siembra/
  recogida en la documentación viva, los §§ de siembra de
  `VITRINA-REVISION.md` (pasa a historia en el CHANGELOG) y las
  previas horneadas en la instancia vieja. Skills y docs alineados en
  el mismo cierre (`puerta-arte-propuesta`, `FLUJO-PIPELINE.md`,
  `onboarding-tienda` con el alta de vitrina como paso explícito).
- **F5 — Su caminata.** Revisión del dueño en su iPhone sobre la
  instancia nueva (la técnica no sustituye su pase) y, con su dale,
  el primer lote real entra ya por el flujo nuevo.

## 7. Riesgos medidos del patrón (heredados del Centro, con su antídoto)

- **Latencia de escritura (~13 s por commit):** la vista muestra el
  estado de escritura por tarjeta; una decisión no confirmada por
  relectura no se da por guardada jamás.
- **Ráfagas al conector (429):** lecturas acotadas por apertura
  (~5 llamadas de texto + previas por SHA cacheadas) y paralelismo
  con techo, como fija el contrato en vivo del Centro.
- **Conflicto de SHA entre dos escrituras cercanas:** fusión por
  `id` + un reintento; el segundo choque se muestra fallido con
  causa, no se reenvía a ciegas.
- **Costo de construcción:** una instancia nueva por tienda (una
  sola vez); los lotes dejan de costar generación de paquete +
  edición de la instancia + siembra + recogida por artefacto.

## 8. Decisiones que quedan del dueño en F0

1. La excepción acotada de previas JPG en el repo de datos (§3-H2) —
  es la única relajación de la política de medios, y solo para el
  entregable de revisión en su hogar declarado.
2. El ritmo de escritura de decisiones **al instante** (§4), igual
  que en el Centro desde su v1.10 — frente a la alternativa de
  acumular en la página y escribir al marcar (más rápido al tocar,
  pero la decisión viviría fuera del sistema entre tanto: es el
  defecto que esta fase elimina). Recomendación de Jarvis: al
  instante.

**F3 EJECUTADA Y VERIFICADA (2026-10-26):** ciclo completo en la tienda de ensayo (entrega sin siembra → aprobado directo; mejorar → retiro → mejorar → aplicación → regeneración como nueva versión → aprobación → aplicación; bandeja en cero en dos lecturas, sin resurrección). Cazados y corregidos: derivación del retorno de mejora, dimensiones vacías y dos timeouts de escritura que sí aterrizan. Incidente mayor: el commit de investigación semanal pisó el registro de decisiones del ensayo vía el puente (causa raíz: decisiones es repo-first y la copia física era vieja); restaurado desde git. Enmienda F3 en `docs/VITRINA-VIVA.md`. Puerta dura de F4: regla repo-first en el puente antes del corte.

**F4 EJECUTADA Y VERIFICADA (2026-10-26):** puente con custodia repo-primero para `vitrina/decisiones.json` (9/9 pruebas contra la guarda; el commit real del corte pasó por el puente endurecido), generador de siembra eliminado, rama fusionada a main y borrada con su worktree. Instancia de producción `vitrina-de-revisi-n-my-pod-2` creada y verificada leyendo en vivo (HEAD del propio commit del corte, bandeja en cero); bloque `vitrina` de la tienda apuntado a ella (commit de datos `0314de2`) y la instancia sembrada `vitrina-de-revisi-n-my-pod` retirada. Queda F5: su caminata en iPhone y el primer lote real por el flujo nuevo.
