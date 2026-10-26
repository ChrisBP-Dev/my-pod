# Changelog — puerta-arte-propuesta

## v0.12.0 (2026-10-26) — presentación sin acabado fingido; estilo por diseño; tipografía declarada

Tres correcciones del dueño sobre el piloto p068–p071, con su dale a recalibrar el canon y regenerar con worker frío:

- **`resultado_esperado` RETIRADO del flujo:** la vista «cómo se vería» con acabado bordado no se quiere — confundía el juicio y fingía un acabado. La propuesta de todo método lleva UN arte (la fuente) y la simulación compuesta sobre la fuente misma. La puerta mecánica de entrega ahora FALLA si una entrada declara `resultado_esperado`, y ya no lo exige en bordado. (La separación fuente/resultado de v0.11.0 queda como historia: la fuente plana sigue siendo la regla; lo que muere es la vista texturizada.)
- **Estilo declarado e independiente del método:** la ficha gana el campo `estilo` (obligatorio en la puerta mecánica). Un dtg nace como gráfico de impresión, nunca con look bordado/parche salvo concepto declarado; el sesgo del lote no contagia estéticas.
- **Tipografía declarada por campo:** cada campo de la ficha declara `fuente` y `color` (obligatorio en la puerta mecánica); canon de fuentes con archivos en `assets/fuentes/` (Dancing Script, Oswald, Montserrat). Las simulaciones renderizan los ejemplos con la fuente y el color declarados, y el ejemplo lleva el carácter del concepto — un texto básico de relleno es defecto de la entrega. Aclarado en el canon: el dueño aprueba la ficha una vez; el sistema compone el texto del comprador desde ella, pedido a pedido, sin que el dueño coloque textos.

## v0.11.1 (2026-10-26) — contornos lisos: la fuente plana nace plana

- **Corrección del dueño sobre la corrección v0.11.0:** las fuentes planas de p070/p071, producidas aplanando el arte texturizado, heredaban su silueta — un tembloreo sutil de hilo en todos los contornos: «no parece un diseño normal». Regla nueva en la puerta: la fuente plana exige **contornos lisos tipo vector**; aplanar/posterizar un texturizado NO es una fuente válida. Si el concepto nació texturizado, la fuente se regenera como ilustración plana de contornos lisos (misma composición) y se cuantiza a colores exactos. Caso vivo cerrado el mismo día: p070 regenerado (5 colores exactos, PASS) y p071 regenerado (4 colores exactos, PASS), previas regeneradas en la vitrina.

## v0.11.0 (2026-10-26) — bordado: fuente plana ≠ resultado esperado; método declarado

- **Estándar de fuente para bordado (duda del dueño, resuelta contra la guía oficial de Printify):** el archivo que entra a Printify para bordar es PLANO — colores sólidos (máx. 6 de hilo), formas gruesas, sin degradados, sombras ni textura de puntadas; la textura nace al digitalizar y coser. Un arte «que ya se ve bordado» es FAIL como fuente: la digitalización simplifica o altera sus partes finas y el resultado difiere de la previa.
- **Dos archivos con roles y nombres distintos en bordado:** `arte` = fuente plana de producción; `resultado_esperado` = referencia con textura de cómo se verá cosido (nunca entra a Printify). La simulación del personalizable bordado se compone sobre el resultado esperado; la previa del arte muestra la fuente plana.
- **`metodo` declarado en toda propuesta** (`dtg` | `bordado`) en la entrada del registro; la vitrina lo muestra como etiqueta visible junto a «Personalizable» y rotula fuente/resultado en bordados (contrato `docs/VITRINA-VIVA.md`, Enmienda Bordado). Caso vivo que lo destapó: p070/p071 del piloto U3 llegaron con la textura dentro de la fuente y sin etiqueta de método — corregidos en plano el mismo día.

## v0.10.0 (2026-10-26) — recogida sin marca (U1 del brief de alineación)

- **«Marcar listas» deja de ser puerta:** la decisión del dueño es vigente desde que la vitrina la escribe al instante en `vitrina/decisiones.json`; no hay botón, ni recibo copiable, ni estado `lista` como requisito. La recogida-aplicación (§ homónima) opera sobre las **decisiones vigentes** del repo: última entrada por slug, no `aplicada`/`devuelta`, `accion` ≠ `retirar` (una última entrada `retirar` = sin decisión vigente).
- **Compatibilidad hacia atrás:** entradas históricas con `estado` `sin-marcar` o `lista` se leen como `vigente`; `fecha_lista` pasa a dato histórico ignorado. Las fechas de aprobación/decisión de la recogida salen ahora de `fecha` (el instante de la decisión), y `fecha_envio_dueno` del bloque `recogida_vitrina` conserva su nombre histórico con ese mismo valor.
- **Disparador sin cambios de fondo:** cualquier aviso del dueño en un chat (regla libre de v0.8.4); sin aviso no hay aplicación. Motivo de U1: la marca era compensatoria de la vitrina sembrada — con lectura en vivo y escritura al instante, su contexto murió (decisión cerrada del dueño, 2026-10-26). Contrato alineado: `docs/VITRINA-VIVA.md` (Enmienda U1, §Acciones: `getboard`/`sello`/`guardardecision`, `marcarlistas` retirada).

## v0.9.0 (2026-10-26) — la entrega y la recogida se mudan a la vitrina en vivo (sin siembra)

- **Entrega reescrita:** mueren el paquete (`datos-vitrina.json`) y la siembra. La entrega ahora es: porqué completo en el registro → previas producidas como entregable en su hogar del repo de datos con `scripts/producir-previas-vitrina.py` (que hereda la puerta mecánica de personalizables: sin simulación o sin ficha, falla) y declaradas en la entrada (`dimensiones_px` + bloque `vitrina`) → entregados registrados en `estado-propuestas.json` → un solo commit del puente. Con ese commit el diseño ya está en la vitrina: la instancia lo deriva del repo al abrir.
- **Recogida → recogida-aplicación:** la fuente deja de ser la instancia (acciones `leerdecisiones`/`confirmarrecogida`, retiradas) y pasa a ser el registro de decisiones de la tienda en el repo (`vitrina/decisiones.json`, append-only, escrito al instante por la vitrina — ruta C del Centro de My Channels). Se conservan disparador, cruce obligatorio, validaciones, idempotencia con su excepción de nueva versión y las escrituras exactas por resultado; se suma la marca `aplicada`/`devuelta` + `commit_aplicacion` sobre cada decisión y la verificación por relectura como paso de cierre.
- **`estado-propuestas.json` cambia de clase:** de checkpoint local no versionado a registro versionado de la tienda (decisión del dueño 2026-10-26; el puente `registros-datos.py` y los `.gitignore` lo declaran igual).
- **Retorno de una mejora:** el requisito «previa compilada en la instancia antes de sembrar» se reemplaza por producir las previas del arte nuevo en su hogar y verificar por relectura tras el commit — mostrar el arte viejo como nueva versión es imposible por construcción (la previa servida es la del `arte_ref` vigente).
- Contratos nuevos en `docs/VITRINA-VIVA.md`; la plantilla sembrada v2.3 queda como historia. Decisión y plan: `docs/PROPUESTA-VITRINA-LECTURA-EN-VIVO.md`.

## v0.8.8 (2026-10-23) — el formato profesional sale del skill: es calibración de nicho (Programa Estándar My POD, F4)
- La sección «Formato profesional real (enfermería)» (firma ANCC, vocabulario cerrado de unidades, instrucción al comprador) se **mueve sin cambios** a la referencia de nicho de la tienda que la usa: `data/tiendas/<tienda>/investigaciones/formato-profesional-enfermeria.md` en el repo de datos, declarada desde su ficha (`config.json → nicho.referencia_formato_profesional`).
- En el skill queda el **mecanismo**: si la ficha declara un nicho con formato profesional documentado, la puerta carga esa referencia antes de juzgar personalizables; si no la declara, juzga con los criterios generales y declara la ausencia. Ninguna tienda hereda el formato de otro nicho.

## v0.8.7 (2026-10-23) — la siembra es solo del flujo; diseños no sembrados = incidente
- El paso de siembra de la entrega declara que la acción explícita del flujo es la ÚNICA siembra existente (la instancia nunca se siembra sola; regla espejo en la plantilla `VITRINA-REVISION.md` v2.3 §«Regla de siembra», del incidente de resurrección del 2026-10-22: la instancia del piloto resembró el lote recogido al abrirse con la bandeja vacía). Si el tablero muestra diseños que la entrega vigente no sembró, es incidente de la instancia: no se pide decisión sobre ellos ni se recogen; se reporta y se corrige primero.

## v0.8.6 (2026-10-22) — dónde viven la simulación y la ficha en el registro (cierre de vitrina personalizable)
- La variante personalizable declara ahora su hogar en el sistema: la entrada del registro lleva `personalizable: true`, `simulacion` (ruta del compuesto sobre el arte real) y `ficha_razon` estructurada (razón, prueba de borrado, campos con tipo/límite/opciones y ejemplo, comprador/destinatario/ocasión, clase de encaje, ejemplo de simulación, peor caso, producto destino, plan de zonas). El generador de la vitrina valida ese paquete y falla sin él — la entrega de dos imágenes + ficha deja de depender de que alguien lo recuerde al sembrar.

## v0.8.5 (2026-10-22) — pasos 5–6 del procedimiento alineados al flujo vitrina
- El resumen del procedimiento estándar todavía decía «Draft en Printify → el dueño revisa ubicación» como paso inmediato tras el PASS de la puerta — remanente del flujo en que la propuesta llegaba a Printify. Corregido: paso 5 = entrega en la vitrina y aprobación registrada en el checkpoint; paso 6 = producción en Printify (Fase B) con revisión de ubicación. Sin cambios en la puerta ni en la entrega (ya canonizadas en v0.8.0–v0.8.4).

## v0.8.4 (2026-10-22) — el aviso no exige frase exacta y los estados se reportan cruzando la vitrina
- **Disparador de la recogida aclarado:** cualquier mensaje del dueño (texto o audio) que indique que ya decidió o marcó listas sus decisiones en la vitrina ES el aviso; el mensaje copiable del recibo es una ayuda, no una clave. Caso fundacional: aprobó la nueva versión del p063 a las 21:21 ET y avisó por audio a las 21:36 — la recogida corrió con ese aviso (p063 aprobado; la cola de aprobados del lote quedó en 10).
- **Cruce obligatorio antes de reportar estados:** el checkpoint no conoce lo decidido y enviado en la vitrina sin recoger; quien reporte conteos al dueño cruza primero la lectura de decisiones y lo reporta como «decidido en la vitrina, pendiente de recogida». El watchdog ganó la REGLA VITRINA complementaria (decisiones enviadas sin recoger por más de 24 h = alerta menor, porque viven solo en la vitrina).

## v0.8.3 (2026-10-22) — la recogida también alinea el registro (hueco detectado por el watchdog)
- La recogida (§«Recogida de decisiones (vitrina)», paso 4) ahora actualiza en el mismo acto el `estado` de cada diseño recogido en `registro-listings.json` y lo commitea al repo de datos. Causa: la recogida fundacional escribió solo el checkpoint y el watchdog de las 21:09 cruzó registro vs checkpoint y alertó «el registro no refleja la aprobación» — hueco real de la v0.8.0. Los estados del lote 2026-10-19 se alinearon a mano el mismo día (9 aprobados «pendiente Fase B», p063 «nueva versión en vitrina»).

## v0.8.2 (2026-10-22) — retorno de una mejora: el ciclo del «mejorar» queda cerrado en el sistema
- **Nueva sección «Retorno de una mejora (regeneración → nueva versión en la vitrina)»:** procedimiento completo con el caso fundacional p063 v2 — regenerar solo lo pedido, verificación del arte nuevo (con adjudicación registrada cuando el cambio mismo es un fondo de diseño), registro actualizado, **requisito duro de previa compilada por `arte_ref` ANTES de sembrar** (hueco fundacional: las previas eran estáticas por slug y la siembra habría mostrado el arte viejo como «Nueva versión»; la instancia se reparó y publicó el 2026-10-22), siembra, verificación en el tablero y aviso sin artes en el chat.
- **Contabilidad del checkpoint al cumplirse una mejora:** la entrada se mueve de `mejorar` a `mejoras_cumplidas` (con su cumplimiento), y la recogida gana la excepción explícita: la decisión sobre una nueva versión es NUEVA y se procesa, no la bloquea la idempotencia.
- Sin cambios en gates, criterios ni en la recogida base.

## v0.8.1 (2026-10-22) — corrección del dueño: la vitrina es la superficie ÚNICA de la Fase A
- **La entrega para aprobación ya no tiene dos superficies:** la única es la **vitrina de revisión** de la tienda. El chat deja de ser superficie de aprobación en esta fase (era el flujo anterior a la vitrina; con la vitrina lista, las propuestas por chat dispersan la revisión y llenan el chat de artes — corrección del dueño del 2026-10-22, el mismo día de la canonización: la v0.8.0 había dejado el chat como vía equivalente siguiendo el encargo de canonización, que traía el modelo viejo).
- **El chat solo avisa:** aviso breve en el chat de entrega (qué lote, cuántos diseños, el acceso a la vitrina con su tarjeta), **sin adjuntar artes ni porqués** — todo eso vive dentro de la vitrina. La entrega queda escrita como procedimiento de 4 pasos (paquete → siembra → aviso → decisión y recogida).
- Sin cambios en la recogida (sección v0.8.0), los gates ni los criterios.

## v0.8.0 (2026-10-22) — vitrina de revisión canonizada: entrega dual + recogida de decisiones
- **La entrega para aprobación tiene DOS superficies equivalentes** (chat y vitrina de revisión) que alimentan el mismo checkpoint `estado-propuestas.json`; ninguna aprobación vale hasta estar registrada ahí. *(Superado el mismo día por la v0.8.1: superficie única, la vitrina.)* La superficie vitrina se sembraba desde la plantilla `docs/VITRINA-REVISION.md` (rama `vitrina-revision`, fusionada a main el 2026-10-22) sin que ningún skill la nombrara como canal de entrega.
- **Nueva sección «Recogida de decisiones (vitrina)»:** procedimiento ejecutable completo — disparador (aviso del dueño en un chat), instancia declarada en `vitrina` del `config.json` de la tienda, lectura por `leerdecisiones` solo de decisiones `enviada=true`, validaciones previas (slug en registro y checkpoint, conteos, **idempotencia** contra el checkpoint y contra `esperandoRegeneracion`), escrituras exactas por resultado (`aprobados`/`rechazados`/`mejorar` + bloque `recogida_vitrina`), confirmación con `confirmarrecogida`, reporte en el chat del aviso y modo lectura (dry-run). Vive en este skill, dueño de la puerta, y no en un skill aparte (justificación en la propia sección).
- Sin cambios en los gates mecánicos ni en los criterios de personalizables.

## v0.7.0 (2026-10-20) — criterios de personalización con RAZÓN (estudio + corrección del dueño)
- **La sección de personalizables se reescribe con la razón gobernando:** ficha de razón obligatoria en la entrega (razón en una frase — identidad/relación/ocasión/conmemoración/pertenencia —, prueba de borrado en dos estados, campos ≤3 cerrados, comprador/destinatario/ocasión, clase de encaje, peor caso renderizado). Base: el estudio de criterios de personalización del 2026-10-20 y la corrección del dueño del mismo día (los 4 diseños del piloto, "diseño + franja con texto", quedaron parqueados como prueba de flujo por no tener razón).
- **Formato profesional real:** firma ANCC (grado → licencia → designación → certificación, con comas), vocabulario cerrado de títulos/unidades para los dropdowns, patrón de instrucción al comprador de los listings top.
- **Encaje con regla de oro:** si un humano debe tocar el dato o la imagen antes de imprimir, es manual (b); la ruta automatizada solo imprime tal cual lo del comprador. Texto libre sin razón = (c) no encaja por criterio.
- **RETIRADO el comodín "Maria / RN - ICU"** como ejemplo estándar de tienda (era un ejemplo casual del dueño, aplicado sin criterio): la simulación usa el ejemplo derivado del concepto con su formato real. La geometría de zonas se reordena por lógica de objeto (pecho = identidad, manga = persona, espalda = jersey) en vez de franjas genéricas.
- **Técnica sumada de la producción del piloto:** prompt con blancos sombreados (el blanco puro de diseño se lo come limpiar-fondo: gorro de PIL-02 v1) y orden de proceso (resize con alfa premultiplicado ANTES de las limpiezas; el Lanczos directo recrea la película). Regla del motivo íntegro (estetoscopio completo y conectado — corrección del dueño).

## v0.6.3 (2026-10-20) — personalización (llega sobre la v0.6.2 del barrido counters; numerada 0.6.3 para no colisionar)
- **Criterios de arte para diseños personalizables** (fase de personalización, Pasos 2+3): el diseño nace con su zona integrada y la forma sigue al diseño/mercado (caja de herramientas, no plantilla — corrección del dueño 2026-10-19); geometría medida desde los píxeles del arte final (caja del nombre ≈60–65% de la cara, una línea, margen en 4 lados; dato pegado 0.15–0.3"; contraste fuerte sobre la prenda más clara); marco de foto tipo passe-partout (relleno FIT verificado en vivo: la foto entra entera con su ratio y su fondo); bordado = texto corto bold con fuentes pre-digitalizadas; diseño personalizable siempre NUEVO y único (nunca copia de un MPL — duplicado penalizado); puerta visual con el ejemplo estándar Maria / RN - ICU antes de reportar un draft listo. La guía v1 de la prueba quedó clasificada contra estos criterios (donde conflictó, mandó el sistema; su "aprobación automática de respaldo" queda como NO verificada).
- **Entrega para aprobación con SIMULACIÓN** (pedido del dueño 2026-10-20, alineación del flujo v2): la entrega de un personalizable trae dos imágenes — el arte real (zonas vacías, el de producción) y la simulación del resultado esperado, compuesta determinísticamente sobre el arte real con el ejemplo estándar en las zonas medidas (nunca una generación paralela) — y su porqué declara producto destino + plan de zonas (dato, límites, dropdowns). Sin la simulación el dueño no puede juzgar un diseño cuyas zonas nacen vacías.

## v0.5.3 (2026-10-19)
- Fase de mejora v0.14.0: P1 — el diseño canónico de calibración de la suite vive ahora en `evals/fixtures/` (copia con origen y sha256 registrados en la suite; `K` ya no apunta fuera del repo). P2 — declaradas en el skill las herramientas compartidas `scripts/procesar-arte-propuesta.py` y `scripts/reparar-fondo-casi-blanco.py`.

## v0.5.2 (2026-10-19)
- El registro del diseño (`porque`) vive en `data/tiendas/<tienda-id>/registro-listings.json` (reorden de datos por tienda, 2026-10-19).
Skill de app. Pineado a Rameli v0.19.0.

## v0.5.1 — 2026-10-19 (flujo de propuestas v2, idea del dueño)
- Nueva sección "Entrega para aprobación del dueño": el PASS de
  la puerta se entrega por diseño en un chat nuevo, con el arte
  final y su porqué (tema/ángulo/frase/iconografía) + qué mirar
  (los pendientes del ojo humano que la puerta ya declaraba).
  Sin esa aprobación, el diseño no entra a producción: el dale
  creativo se mueve al punto más barato (antes se revisaba el
  arte recién en Printify, con los drafts ya creados). El porqué
  se guarda en el registro (`porque`) y lo hereda el paquete
  comercial. Sin cambios en los gates.

## v0.5.0 — 2026-10-18 (lote de drafts mutilados p038-p057, cazado por el dueño)
Contexto: 16 diseños llegaron CORTADOS a los drafts de Printify (palabras
rebanadas en los extremos, hojas y elementos incompletos) y ninguna
puerta lo vio — la puerta medía que no sobrara aire tras el recorte,
pero un diseño ya cortado "pasa" ese criterio. Causas medidas, no
supuestas (auditoría completa en data/registro-correccion-recortes-2026-10-19.json):
(a) lote A (p038-p045): el autotrim por bbox de MASA (0.05%) amputó los
extremos de baja masa de originales completos (7-53px por lado a escala
de generación); (b) lote B (p048-p057): un desbordamiento tipo fill
rebanó 0.4-3.7% por lado.
- Nuevo gate `composicion_completa` (`--es-original`, sobre el CRUDO
  antes de procesar): margen del bbox SEGURO por lado ≥ máx(6px, 0.4%).
  El bbox seguro = unión de componentes reales (área ≥150px,
  min(ancho,alto) ≥8px; filtra slivers/specks de borde).
- Nuevo gate `contenido_intacto` (finales): el bbox seguro no toca el
  borde del archivo (≥2px/lado).
- Nuevo gate `fidelidad_recorte` (`--original <crudo>`): desviación de
  aspecto del contenido ≤1.5% y pérdida en banda externa ≤2%/lado
  (rejilla 200×200 normalizada a bbox seguro). Si no se puede
  verificar, no pasa.
- FIX RAÍZ: `--autotrim` recorta al bbox SEGURO (antes: masa). La
  salida declara qué bbox usó (`autotrim_bbox`).
- Calibración con casos reales (no fixtures inventados): crudos del
  lote 16/16 PASS composición (mín. 0.86%/lado); prints mutilados
  16/16 FAIL composición (0px en los 4 lados) y 16/16 FAIL
  contenido_intacto; finales corregidos 16/16 PASS en todo, incluida
  fidelidad (pérdida 0.0, aspecto ≤0.5%). Fidelidad sola caza 10/16
  mutilados: las amputaciones finas/simétricas restantes no las
  separa ninguna métrica de píxeles a esa magnitud (el registro por
  template tiene piso de ruido ~0.5%/lado; medido y descartado como
  gate) — quedan cubiertas por contenido_intacto + el fix del
  mecanismo. La puerta nueva cazó además un defecto real en la
  primera reconstrucción corregida (p049 v1: pad inferior clampeado
  a 0) antes de subirla.
- Suite 8→13 casos: P3/F7 composición, P4/F8 fidelidad, F9 autotrim
  seguro (la barra fina de baja masa sobrevive: salida 1409px vs
  1384px con masa). 13/13 verde.

## v0.4.0 — 2026-10-17 (corrección del dueño revisando el lote de ayer)
- `recorte_ajustado` REPARADO: medía el margen MENOR de los 4 lados
  (min) — aire enorme en 3 lados pasaba si un lado estaba pegado. El
  canónico vitals trae máx 50px/lado (el "22px" citado era el mínimo).
  Ahora: bbox de contenido real (alfa≥128) y tope POR LADO
  máx(48px, 4% del lado). `--autotrim` usa el mismo bbox real.
- Nuevo gate `dpi_al_zoom` (flag `--exigir-margen-zoom`): el ancho del
  CONTENIDO debe rendir ≥300 DPI al ancho nominal ×1.20 — el dueño
  agranda la colocación al revisar y los artes de 3200px caían a
  250-260 DPI ("ya no lo puedo jugar").
- Procedimiento: paso 2b RECORTAR obligatorio (--autotrim) antes de la
  puerta final; antes el cron corría la puerta sin recortar nunca.
- Suite 5→8 casos: F5 aire asimétrico (caza el bug min), P2 zoom con
  margen, F6 vitals sin margen de zoom. Calibración verificada:
  conocido-bueno PASS / conocido-malo FAIL en cada criterio nuevo.
## v0.1.0 — 2026-10-13
- Creado desde la plantilla.

## v0.1.1 (2026-10-13)
- G2 dividido en `fondo_limpio` (esquinas alfa=0) y `recorte_ajustado`
  (margen ≤32px): el criterio del dueño es recorte exacto al arte, sin
  bordes vacíos — el gate anterior pedía margen mínimo, al revés.
- Nuevo `--autotrim`: recorta al bbox + 4px y re-verifica (verifier-repair).
- Suite 4/4: P1 + F1/F2/F3 (fondo, dpi, recorte).
