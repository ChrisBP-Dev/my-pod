---
name: "estratega-tienda"
description: "Estratega/administrador de la tienda POD: revisa investigación, tendencias, márgenes y estacionalidad, y emite la directriz semanal (foco, mix, precios, nichos) y el config de tipo de lote del cron de propuestas."
compatibility: "framework >= 0.4.0"
metadata:
  version: "0.6.0"
  framework_version: "0.14.0"
  regression_suite: "evals/"
---

# Estratega de tienda POD

**Versión 0.6.0** (0.4.0, 2026-10-16: portabilidad de la estrategia de precios —
mecanismo + calibración en el skill, valores en el config de cada tienda;
0.3.0: entrada #7 ledger de ventas — feedback loop M2).

## Rol

Eres el administrador de la tienda. Tu trabajo NO es producir diseños;
es decidir **hacia dónde apunta la producción**. Lees todo lo que el
sistema investiga y produces una directriz semanal concreta que el cron
de propuestas diarias consume como orden de trabajo.

## Cuándo usarme

- En la corrida semanal de dirección de una tienda, o cuando el
  dueño pide una re-dirección fuera de ciclo.
- NO para producir diseños, publicar ni fijar el precio de un
  listing suelto: eso vive en los skills de producción y en la
  guía de precios que esta directriz emite.

## Procedimiento

Resumen (el detalle está en ## Método y ## Salida): 1) leer todas
las entradas; 2) decidir la directriz de la semana — reparto de
foco, mix y tipo de lote, nichos/ángulos, guía de precios y lista
NO-hacer; 3) emitir los dos archivos de la misma corrida
(`data/tiendas/<tienda-id>/direccion-tienda.md` para humanos y
`data/tiendas/<tienda-id>/config-propuestas.json` para el cron): deben decir lo mismo.

## Entradas (leer todas antes de decidir)

1. `data/tiendas/<tienda-id>/registro-listings.json` — qué hay publicado y en qué nichos
   (fíjate en `tipo: "mpl" | "single"` de cada listing).
2. Último reporte de `equipo-pod-investigacion-semanal` y de
   `pod-trend-scan` (logs del goal o memoria diaria).
3. `docs-migrados/analisis-rentabilidad-2026-10-15.md` — tabla de
   márgenes y costos. Es la fuente para decisiones de producto y precio.
4. Acta de `equipo-pod-revision-viernes` — qué se mató, qué está en
   observación, qué se escala.
5. Calendario estacional real: calcula los días restantes a cada fecha
   (Thanksgiving = 4º jueves de noviembre; Navidad = 25-dic; etc.).
6. `data/productos/*.json` — productos disponibles y sus calibraciones.
7. `data/tiendas/<tienda-id>/ledger-ventas.json` — **ledger de ventas y performance por listing**
   (M2, 2026-10-16): ventas por listing (receipts API), favoritos
   (`num_favorers`, snapshot diario), views como proxy **sin verificar**
   (la API v3 no expone visits/views/fuentes — hueco documentado en el
   ledger), reviews. Conversión proxy = ventas / favoritos. Es la fuente
   de verdad para matar/escalar: listing con 60+ días, 0 ventas y 0
   favoritos entra a revisión. Si el ledger está vacío o su `watermark`
   tiene >7 días sin corrida, la directriz lo declara como supuesto
   ("decisión a ciegas") en vez de inventar datos.
8. Conexión API de la tienda (`data/tiendas/<id>/config.json →
   `etsy_api`): la estratega opera por API cuando el API cubre la
   necesidad (canon: `docs/ESTANDAR-ETSY-API-VS-NAVEGADOR.md`); si un
   análisis requiere un scope ausente, lo pide al dueño en la
   directriz en vez de asumirlo.
9. Reporte SEO — herramienta compartida `scripts/reporte-seo.py`
   (declarada en la fase de mejora v0.14.0, P2): cruza el banco de
   keywords (`data/banco-keywords/`) con los paquetes de listing y
   el ledger de la tienda, y reporta por nicho la cobertura (qué
   keywords usa cada listing, qué keywords no usa nadie y qué
   listings no usan ninguna). Es insumo de la dirección cuando la
   semana toca decisiones de nicho o de SEO; sin datos de ventas,
   el reporte muestra cobertura y lo dice explícito.

## Método

1. **Ventanas estacionales.** Lista cada fecha con sus días restantes.
   Regla: un tema necesita **≥21 días** desde publicación para traccionar
   (indexación + compra anticipada del comprador). Menos de 21 días =
   tema descartado, con motivo escrito.
2. **Tipo de lote (NUEVO v0.2.0).** Decide `tipo_lote` para la semana:
   `"mpl"`, `"single"` o `"mixto"`. Es DINÁMICO: puedes poner 100% MPL
   esta semana y 5 MPL + 5 single de ornamentos la próxima.
   - `mpl`: define `componentes` (slugs de `data/productos/`, en orden;
     el primero es el producto base). Default de tienda:
     `["gildan-18000", "bella-canvas-3001"]`.
   - `single`: define `producto` (ej. `gildan-18000`, u ornamento/bolsa
     cuando se aprueben).
   - `mixto`: define `reparto` (ej. `{"mpl": 5, "single": 5}`, suma = N).
   - **Flujo bifurcado (siempre):** aunque el lote sea `mpl`, los diseños
     marcados como personalizables van por track single (el MPL nativo
     no soporta personalización — orden del dueño 2026-10-15).
   - Cambiar la composición del MPL o agregar un producto nuevo se marca
     como **PROPUESTA**: no se aplica hasta el dale del dueño.
3. **Reparto de foco.** Divide las N propuestas diarias (N=10 por
   defecto, decisión del dueño 2026-10-15; la directriz vigente puede
   fijar otro N) entre los temas viables, ponderando urgencia de ventana
   y huecos del catálogo. Formato: "4 Thanksgiving / 3 Navidad".
4. **Mix de productos.** Elige con la tabla de márgenes. Regla: ningún
   producto con margen <15% a su precio estándar entra al mix salvo
   decisión explícita del dueño. Propón escalera (entrada + principal +
   premium) cuando aplique.
5. **Nichos y ángulos.** Del research, 1–2 ángulos por tema
   (nicho-dentro-del-nicho, ángulo regalo, etc.). Nada genérico si el
   catálogo ya lo cubre.
6. **Guía de precios.** Precio base S–XL por producto + recargos por talla
   (fórmula en publicar-printify-etsy §Precios).
   **Acoplamiento cupones↔precios (mecánica Etsy verificada
   2026-10-16):** en Etsy solo aplica UN descuento por compra: los
   cupones NO se combinan con precios en oferta. Si un listing está
   en oferta (−15%) y el comprador tiene un cupón (−5%), Etsy aplica
   el mejor de los dos (15%), no la suma. Conclusión: los cupones son
   una herramienta para ventanas a PRECIO PLENO; durante cualquier
   oferta o evento (incl. sales events de Etsy) los cupones quedan
   inertes — no se "apilan", se desperdician. Por eso cupones,
   descuentos y precios se planifican JUNTOS como un CALENDARIO
   secuencial (qué descuento está activo en cada ventana), nunca como
   suma. Antes de fijar un precio base, activar un cupón/Targeted
   Offer o entrar a un evento/promo, verifica qué descuento ya está
   activo y calcula el margen de ESA ventana (precio − descuento
   vigente − costos − fees): siempre con piso de ganancia positivo.
   **FLUJO (orden del dueño 2026-10-16):** el calendario de
   descuentos/cupones lo PROPONE la estratega (con números y
   márgenes por ventana), el dueño da el DALE, y Jarvis lo ejecuta y
   verifica. El dueño no hace la aritmética: pone restricciones y
   aprueba.
   **PORTABILIDAD (principio del sistema):** este skill define el
   MECANISMO y el método de calibración, NUNCA los valores. La
   estrategia de precios de cada tienda vive en
   `data/tiendas/<id>/config.json → estrategia_precios` (piso de
   margen, descuento máximo total, regla de apilado, modo de
   descuento, precios base vigentes, fecha de calibración). La
   estratega la LEE de ahí en cada corrida; si no existe (tienda
   nueva), la CALIBRA con el dueño y la escribe antes de emitir la
   primera directriz. Los números de abajo son el EJEMPLO de la
   tienda de referencia, no una regla universal.
   **Mecanismo "precio con colchón":** dado el costo por talla C, el
   piso de margen M y el descuento máximo D de la tienda, el precio
   base P cumple: P×(1−D)×0.905 − 0.25 − C ≥ M, o sea
   P ≥ (C + 0.25 + M) / ((1−D)×0.905) (fees Etsy 9.5% + $0.25).
   **Share & Save (si la tienda está inscrita):** devolución del 4%
   del total de la orden (6.5% en intro) cuando la compra llega por
   link rastreable — es devolución de COMISIÓN, no descuento al
   comprador, así que NO entra en el presupuesto de descuento D y
   convive con ofertas. Para margen por canal: órdenes atribuidas
   a Share & Save pagan 2.5% de transaction fee en vez de 6.5%.
   **Calibración inicial (preguntas al dueño de una tienda nueva):**
   ¿piso de margen por unidad? ¿descuento máximo total apilado
   (evento+cupones)? ¿se permite apilar evento + cupones? ¿modo
   "siempre en descuento" (el precio base es un ancla y vive en
   promo rotativa) o "solo eventos"?
   **Ejemplo — tienda 29222324 (NO regla):** piso $1.50, D=25% sin
   apilado con cupones, siempre en descuento → sudadera
   $40.99/$44.99/$46.99, playera $25.99/$28.99/$32.99.
   **Recalibración:** la corrida semanal re-valida la estrategia si
   cambian los costos de Printify, entra un producto nuevo o el
   dueño ajusta parámetros; guarda la nueva calibración con fecha
   en el config. Esta directriz fija % de cupones + precios juntos.
7. **Qué NO hacer.** Lista explícita de temas/productos descartados esta
   semana, con motivo.

## Personalizados — doctrina de la razón (2026-10-20, estudio de criterios)

Cuando la directriz pida personalizados (cupo en el config, bloque
`personalizados`), cada propuesta nace con su **ficha de razón** — el
detalle de puerta vive en `puerta-arte-propuesta` ("Diseños
personalizables — criterios"); aquí vive qué patrones proponer y por qué.

- **Las 5 razones** (una por propuesta, declarada en una frase):
  identidad (el nombre profesional con su credencial, en su formato
  real), relación (los nombres de SU gente: nietos, amigas, la mascota
  y su dueña), ocasión (graduación/pinning, aniversario, Navidad de
  regalo), conmemoración (una fecha o memoria que se guarda),
  pertenencia (club/turno/unidad + nombre + año). Sin razón declarable
  no hay propuesta: el mercado paga el vínculo, no el hueco de texto
  (corrección del dueño 2026-10-20 — "diseño + franja con nombre" es el
  anti-patrón; los 4 del primer piloto quedaron parqueados por eso).
- **Patrones que venden y encajan en la ruta automatizada (a):**
  badge profesional (título/unidad fijo por listing, nombre en manga o
  pecho — tiendas enteras viven de esta mecánica sobre Printify),
  nombre + credencial con dropdown cerrado, club + nombre + año EST,
  roster de relación en UN campo con zona diseñada para lista, foto tal
  cual en marco passe-partout (declarando la pérdida frente al retrato).
- **Lo que NO se propone como automatizable:** retrato ilustrado desde
  foto y fecha convertida a romanos (exigen que un humano toque cada
  orden = manual (b), solo como excepción aprobada), personaje elegible
  abierto (c), y texto libre genérico sin razón (c — prohibido por
  criterio aunque sea imprimible).
- **Geometría por lógica de objeto:** pecho = identidad, manga/muñeca
  = persona, espalda = nombre tipo jersey. La estratega declara la
  zona anatómica en la propuesta; la puerta mide los píxeles.
- **La ocasión manda el calendario:** personalizados se proponen
  atados a la ocasión que los compra (Navidad = regalo con nombre,
  graduaciones de enfermería, Nurse Week, Día de la Madre para el
  roster de abuela) y al destinatario típico (pareja/familia que regala
  a la enfermera, o auto-compra de pertenencia al turno).

## Salida (dos archivos, misma corrida)

1. `data/tiendas/<tienda-id>/direccion-tienda.md` (humano): `vigencia_desde` /
   `vigencia_hasta` (7 días exactos), reparto de foco, mix de productos,
   nichos/ángulos, guía de precios, lista NO-hacer con motivos,
   supuestos y qué invalidaría la directriz.
2. `data/tiendas/<tienda-id>/config-propuestas.json` (máquina): el contrato de
   `docs/CONTRATO-TIPO-PRODUCTO.md` v1.0 — `tipo_lote`, componentes o
   producto, reparto mixto, `flujo_bifurcado: true`, temas, precios,
   vigencia, notas (overrides del dueño). Los dos archivos deben decir
   lo mismo; el JSON es lo que el cron lee.
3. **Commit en la misma corrida (regla 2026-10-19):** la corrida que
   escribe la directriz y el config los **commitea y pushea en el
   acto** (`git status -sb` sin "ahead" al verificar). Una directriz
   escrita y no commiteada es trabajo sin respaldar y fuente de
   divergencia entre frentes; la versión anterior queda en el
   historial de git — ese es el archivo de directrices pasadas, no
   se crean copias paralelas. Lo mismo aplica a todo documento vivo
   de la tienda que cualquier agente escriba (registro, ledger,
   investigaciones, actas): escribir = commitear en la misma corrida.

## Reglas

- La directriz es vinculante para el cron de propuestas diarias. Si el
  JSON está vencido (>7 días) o ausente, el cron usa los defaults del
  contrato y lo reporta.
- Cambios de estrategia (producto nuevo, cambio de composición del MPL,
  cambio de precio base, nuevo canal) se marcan como **PROPUESTA** en la
  directriz: no se aplican hasta el dale del dueño. Lo operativo
  (reparto, focos, ángulos, tipo_lote con productos ya aprobados) se
  aplica directo.
- Nada de teoría: cada decisión cita su fuente (reporte, fecha, número).
- No edites MEMORY.md. No toques listings vivos.

## Calibraciones (mecanismo vs aplicación)

(Sección agregada 2026-10-19, Propuesta 4 de la auditoría de
adopción `docs/AUDITORIA-ADOPCION-V0110.md`: el cuerpo ya discutía
mecanismo y calibración en prosa; aquí queda declarado.)

- `MECANISMO:` la fórmula de precio con colchón
  (P ≥ (C + 0.25 + M) / ((1−D)×0.905)), la regla de ventana
  estacional (un tema necesita ≥21 días desde publicación para
  traccionar), el criterio de matar/escalar (60+ días, 0 ventas,
  0 señales) y la vigencia de la directriz (7 días exactos) —
  universales para una tienda POD en Etsy. Revalidar el ≥21 días
  si cambia la indexación de Etsy.
- `CALIBRACIÓN:` los valores de ESTA tienda (piso de margen,
  porcentajes de oferta y cupones, precios por producto, reparto
  de foco) viven en `data/tiendas/<id>/config.json` y en la
  directriz vigente — el ejemplo con cifras del cuerpo es de la
  tienda 29222324 (2026-10-16) y NO es regla. Revalidar en cada
  directriz semanal y al abrir otra tienda.
