---
name: "publicar-printify-etsy"
description: "Publica un diseño aprobado en Printify y Etsy (Printify-first): track MPL nativo (sudadera + playera en un listing) o single-product. Drafts, revisión del dueño, mockups, videos, publicación y verificación en Etsy."
compatibility: "framework >= 0.4.0"
metadata:
  version: "0.9.0"
  framework_version: "0.18.0"
  regression_suite: "evals/"
---

# Publicar en Printify + Etsy (Printify-First + MPL)

**Versión 0.9.0** (2026-10-22: alineación ordenada por el dueño —
ruta MPL ÚNICA: borrador base → conversión → items creados dentro
del MPL desde el catálogo; la ruta vieja de crear todos los
componentes y ensamblar los existentes queda solo como rescate.
Y la aprobación creativa vive en la vitrina ANTES de producir:
nada llega a Printify como propuesta.)
**Versión 0.8.2** (2026-10-20: M7 idempotencia de publicación —
verificar antes de reintentar, el clic de Publish es acción con
costo; M6 corrección en la fuente — prohibido manipular un video
reprobado para pasar la puerta. Incidentes p052 y p046.)
**Versión 0.8.1** — Ruta AUTOMATIZADA de personalización (§Track Single-P):
los campos se montan en Printify y se sincronizan a Etsy con Live Preview;
verificada en vivo en el sandbox (2026-10-20). La caja nativa de Etsy +
fulfillment manual queda como excepción consciente (§P8).
**Versión 0.7.3** (0.7.0 — Estándar API-vs-navegador (canon central en docs/, este skill apunta); tablas de precios por talla leídas del config de tienda (doctrina precio con colchón 2026-10-16))
**Versión 0.6.1** — Esquema de mockups/videos movido al config de tienda
(organización a nivel tienda, 2026-10-15). Printify es la fuente de verdad;
no generamos mockups propios.

## Cuándo usarme / cuándo NO

**Úsame** cuando el diseño tiene: arte aprobado (300 DPI, sin fondo),
paquete de listing aprobado (dale del dueño), y el track decidido
(§0: bifurcado).

**No me uses** si: falta el dale del dueño en el arte o el paquete,
o el diseño es personalizable y se pretende meterlo en un MPL
(el MPL nativo NO soporta personalización).

## Estándar: API de Etsy vs navegador (2026-10-16)

**Principio: API-first.** Todo lo que el API de Etsy cubre se hace por
API (determinista, rápido, verificable por máquina); el navegador es
solo para lo que el API no expone.

**Canon:** `docs/ESTANDAR-ETSY-API-VS-NAVEGADOR.md` — tabla completa de
enrutamiento (qué va por API con qué scope, qué va por navegador),
conexión por tienda y reglas de uso. Este skill lo referencia; no
duplica sus reglas.

**Resumen operativo:** precios/inventario por variación, títulos, tags,
descripciones e imágenes → por API (scope `listings_w`). Sales events,
cupones, estadísticas de visitas y mensajes → por navegador (el API no
los expone). La conexión es por tienda: `data/tiendas/<id>/config.json
→ etsy_api` (skill `conectar-etsy-api`).

## 0. Decisión de track — FLUJO BIFURCADO (orden del dueño 2026-10-15)

**¿El diseño es personalizable (lleva nombre/texto del comprador)?**

- **SÍ → Track SINGLE con ruta AUTOMATIZADA** (este skill, §Track
  Single-P). El MPL nativo de Printify NO soporta personalización — ni
  manual ni automática (verificado en help.printify.com 2026-10-15).
  Los diseños personalizables viven como producto individual, siempre,
  y nacen como diseños NUEVOS y únicos: reutilizar un diseño que ya
  vive en un MPL (aunque la copia sea la personalizable) es duplicado
  penalizado por Etsy (regla verificada 2026-10-16, corrección del
  dueño 2026-10-19).
- **NO → Track MPL** (este skill, §Track MPL). El listing es un
  Multi-Product Listing nativo de Printify: varios productos, un solo
  listing en Etsy.

La estratega puede proponer mover un diseño entre tracks, pero el cambio
requiere dale del dueño: pasar de single a MPL (o nacer MPL) exige
**re-optimización SEO COMPLETA** (título, descripción, 13 tags) para
TODOS los productos del listing + mockups y videos nuevos (regla suya
2026-10-15).

## Composición estándar del MPL (regla de tienda 2026-10-15)

Default (la estratega puede definir otra composición en
`data/tiendas/<tienda-id>/config-propuestas.json` — ver `docs/CONTRATO-TIPO-PRODUCTO.md`):

- **Sudadera:** Gildan 18000, Printify Choice (blueprint 49, provider 99).
- **Playera:** Bella+Canvas 3001, Printify Choice.

**Criterio playera** (orden del dueño, regla de tienda hasta que la
estratega defina mejor): colores White + Athletic Heather + Natural,
TODAS las tallas que el proveedor ofrezca por color. Si un color trae
tallas limitadas (ej. Natural solo XL/2XL), se acepta como viene.
**NO sustituir colores ni detenerse por esto.**

**Criterio color-diseño** (regla suya 2026-10-15): los colores ofrecidos
por diseño se validan contra el diseño (contraste/legibilidad). No se
abarcan colores sin verificación visual. La paleta se elige desde el
inicio y el diseño debe verse bien en cada color. Va en la checklist.

## Precios escalonados por talla (estándar 2026-10-15, orden del dueño)

**Mecanismo (universal):** el precio NUNCA es plano por talla. Toda talla
cuyo costo base supere al de S–XL lleva recargo:
`recargo = redondeo_a_dólar((costo_talla − costo_base_SXL) × 1.15)`
El ×1.15 cubre el fee de Etsy sobre el incremento (~9.5%) y preserva el
margen en dólares de la talla base.

**Tablas vigentes:** la tabla de cada tienda vive en
`data/tiendas/<id>/config.json → estrategia_precios` (precio base S–XL
por producto; los recargos por talla se calculan con la fórmula de
arriba). Ejemplo tienda 29222324 (doctrina "precio con colchón",
2026-10-16):

| Producto | S–XL | 2XL | 3XL |
|---|---|---|---|
| Sudadera Gildan 18000 | $40.99 | $44.99 (+$4) | $46.99 (+$6) |
| Playera Bella+Canvas 3001 | $25.99 | $28.99 (+$3) | $32.99 (+$7) |

**Aplicación:**
- En Printify: el precio retail de CADA variante lleva su recargo ANTES
  de publicar (el precio sincroniza a Etsy). Nota MPL: "Changes you make
  here will also update the Single Listing pricing" — el pricing se edita
  en cada producto single, no en el contenedor MPL.
- En Etsy (verificación Fase C): cada variación con su precio correcto.
- Producto nuevo: consultar costos por talla en la API, calcular recargos
  con la fórmula, registrar la tabla en `data/productos/<producto>.json`.
- El precio base S–XL lo define la directriz vigente de la estratega
  (`data/tiendas/<tienda-id>/direccion-tienda.md` / `data/tiendas/<tienda-id>/config-propuestas.json`).

**Regla anti-desincronización (2026-10-15, orden del dueño):** el precio se
fija UNA sola vez, en el draft de Printify, ANTES de publicar. NUNCA se
editan precios por separado en Etsy y en Printify sobre un listing ya
publicado: eso deja el producto en "cambios no publicados" en Printify
(verificado 2026-10-15) y rompe el filtro publicado = en vivo. Si un
listing vivo necesita cambio de precio: se edita en UN solo lado y se
sincroniza deliberadamente al otro, nunca en los dos por separado.

**Ownership:** la tabla de precios por talla es parte del paquete de
listing — la calcula el agente de publicación con la fórmula de arriba y
los costos por talla de la API (registrada en
`data/productos/<producto>.json`); el precio BASE S–XL lo define la
estratega; el paquete de listing (título/descripción/tags) la referencia
pero no la redefine.

---

## Track MPL — procedimiento

### M0. Inicio de sesión (protocolo Google-first, 2026-10-15)
Antes de pedirle al dueño que inicie sesión manualmente:
1. Ir a printify.com → "Log in" → "Continue with Google".
2. La sesión de Google YA está guardada en el navegador: en el selector
   de cuentas elegir la de la tienda (tudale.pod / Tú Dale POD).
3. Esto inicia sesión en Printify sin intervención del dueño.
Solo si Google no ofrece cuenta guardada o el login falla, se le pide a
él que lo haga manual en el navegador. Mismo protocolo vale para Etsy.

### M1. Crear el borrador BASE (un solo producto — ruta única, 2026-10-22)

**Orden real de ejecución del track: M1 → M4 → M2 → M3 → M5 → M6 →
M7 → M8 → M9 → M10** (la numeración es histórica; la conversión
§M4 ocurre dentro de la producción, antes de la revisión del dueño).

**La ruta normal crea UN solo borrador suelto: el del primer
producto de la composición (default: sudadera Gildan 18000).** Los
demás productos NO se crean como borradores separados: nacen
dentro del MPL en §M4, creados desde el catálogo con el mismo
diseño. Crear todos los componentes por separado y ensamblarlos
después es la ruta VIEJA, descartada por el dueño el 2026-10-22 —
duplicaba trabajo y dejaba componentes sueltos que se confundían
con propuestas; su único uso vivo es el rescate (§M4, excepción).
- Subir el arte a Printify (navegador, el CLI está roto).
- Crear el borrador base con el blueprint/provider del primer
  producto de la composición.
- Colocación inicial (RECALIBRADA por el dueño, 2026-10-17 — reemplaza
  el 78%/centrado anterior): escala = min(92% del ancho del área,
  95% del alto del área) — el diseño se ve GRANDE y COMPLETO, NUNCA se
  desborda del área (2026-10-15: colocar solo por ancho cortó los
  diseños altos). **Centrado HORIZONTAL siempre. Vertical NO centrado:**
  el borde superior del diseño queda al 8–12% del alto del área desde
  el tope (sesgo arriba) — el centro vertical deja aire arriba/abajo y
  el diseño se ve chico y bajo; el dueño lo corrige a mano en cada
  revisión, así que nace corregido. El ajuste fino por diseño sigue
  siendo de su revisión, pero la base ya sale en su criterio.
- Aplicar la paleta validada contra el diseño (criterio color-diseño) y
  los precios escalonados de la tabla vigente (la paleta y los precios
  de cada item agregado se aplican al crearlo dentro del MPL, §M4).
- En el borrador, poner el **título real del diseño** (nunca el nombre
  genérico del blueprint) — regla 2026-10-15.
- El borrador base queda "unpublished" y pasa de inmediato a la
  conversión (§M4). **No es una propuesta:** la aprobación creativa
  ya ocurrió en la vitrina (Fase A, flujo v2); este borrador es
  PRODUCCIÓN de un diseño aprobado (Fase B), pendiente solo de la
  revisión de ubicación del dueño (§M2).
- **REGLA: no publicar el base ni ningún componente single por
  separado.** Los componentes de un MPL se publican SOLO como parte
  del MPL. Publicar un componente solo crea un listing single
  huérfano que compite con el MPL y rompe el flujo.

### M2. Revisión del dueño — placement DENTRO del editor del MPL
- Esta es la SEGUNDA validación del dueño. La primera (la creativa)
  ocurrió en la vitrina ANTES de producir: **nada llega a Printify
  como propuesta creativa** (flujo v2, superficie única vitrina).
- Lo producido en Fase B llega a esta revisión como **un borrador
  MPL por diseño** (base convertido + items creados dentro,
  §M1 → §M4), nunca como componentes sueltos. El dueño abre cada
  borrador MPL y verifica el placement **por item dentro del
  editor del MPL** (grande según §M1, centrado horizontal, sesgo
  arriba, dentro del área de impresión, sin desbordamiento — cada
  blueprint tiene su área). **No existe variante de revisión por
  borrador componente suelto:** era la forma vieja, eliminada en
  la alineación del 2026-10-22.
  Rechazado = elimina el borrador MPL completo. Aprobado = sigue a M3.
- Corrige la ubicación directamente en el editor si hace falta.
- Elimina los rechazados. Avisa cuáles están listos.

### M3. Paquete de listing — SEO completo para TODOS los productos
- Generar con el skill `paquete-listing-etsy`.
- **Regla SEO MPL (suya 2026-10-15):** re-optimización COMPLETA para
  TODOS los productos del listing:
  - **Título** (≤140 car.): incluye AMBOS productos
    (ej. "...Sweatshirt, ...T-Shirt...").
  - **Descripción:** estructurada con sección **"CHOOSE YOUR STYLE"**
    (o "ELIGE TU ESTILO") que presenta cada producto + disclosure IA +
    políticas.
  - **13 tags** (≤20 car. c/u) cubriendo ambos productos y el nicho.
- Puerta: `verificar-paquete.py`.

### M4. Convertir a MPL en Printify (dentro de la producción, tras M1)
Printify no ofrece crear un MPL vacío desde cero: la entrada es
convertir un producto existente. Por eso la ruta es base →
conversión → items creados dentro del MPL.
- En el borrador base: "Convert to Multi-Product Listing".
- "Add item": **crear nuevo con EL MISMO diseño desde el catálogo**
  (1 clic) — **ruta ÚNICA normal**. Cada item nace dentro del MPL;
  no se crea ningún borrador suelto para él.
- **Excepción de rescate (no es una ruta):** "agregar un producto
  existente" SOLO cuando un lote anterior a la alineación del
  2026-10-22 ya dejó un componente creado y verificado del mismo
  diseño; el rescate se anota en el registro del diseño. Fuera de
  ese caso, agregar existentes está prohibido: era la ruta vieja
  de ensamblado (crear todos los componentes y unirlos después).
- Por cada item: verificar placement, colores/tallas, precios.
- Al terminar: **guardar como borrador SIN publicar**. El resultado
  es UN borrador MPL por diseño, listo para la revisión de
  ubicación del dueño (§M2).
- **Nombres de variación** (campo "Variation name for Etsy listing"):
  **"Sweatshirt"** / **"T-Shirt"** — cortos, sin el nombre del blueprint.
  (Decisión 2026-10-15, verificado en p005.)
- Notas del MPL nativo (verificadas 2026-10-15):
  - Título/descripción/tags/mockups se gestionan EN EL MPL, no en los
    productos individuales; el pricing sigue en cada producto single.
  - Un solo shipping price/profile compartido para todo el MPL.
  - Límites: 20 productos, 400 variantes, 70 opciones por MPL.
  - Al publicar, Etsy conserva URL, reseñas y SEO del listing base.
  - Guardar como draft NO toca el listing vivo.
  - Revert a single disponible tras publicar.

### M5. Mockups — esquema por composición (config de tienda, no quemado)
El esquema de mockups NO está quemado en este skill: vive en
`data/tiendas/<tienda-id>/config.json` → `mpl.esquema_mockups`
(una entrada por slot: producto + tipo + nota). Si la estratega define
otra composición, define su esquema ahí; el skill lo lee.

**Esquema vigente para la composición default** (APROBADO por el dueño
2026-10-15) — 10 imágenes, en este orden:
1. Sudadera lifestyle hero (imagen principal del listing).
2. Sudadera lifestyle 2 — pose/modelo DIFERENTE al #1.
3. Sudadera flat-lay.
4. Sudadera flat-lay, otro color.
5. Sudadera folded decorado/ambientado (con fondo, NUNCA plano blanco).
6. Playera on-model.
7. Playera on-model distinto (pose/modelo diferente al #6).
8. Playera flat-lay.
9. Tabla de tallas sudadera.
10. Tabla de tallas playera.

**REGLAS duras** (`mpl.reglas_esquema` en el config):
- Nunca repetir la misma pose/modelo en colores diferentes.
- Todos los productos y colores vendidos deben estar representados
  visualmente (si un color se vende, aparece en alguna imagen).
- La imagen principal (#1) SIEMPRE es lifestyle de sudadera.
- Si el catálogo no ofrece los shoots necesarios, REPORTAR la
  limitación antes de continuar, no improvisar.

**Rotación de héroes entre productos** (criterio suyo 2026-10-15): en
cada lote, ROTAR el modelo lifestyle y el color del héroe. Dos
productos consecutivos NUNCA comparten modelo ni color de héroe.
Aplica igual al primer clip del video 1.

**Nota primario Printify vs Etsy** (observado 2026-10-15): Printify
marca un primario pero al sincronizar el orden puede no preservarse.
Tras el sync, VERIFICAR en Etsy que la imagen principal sea la
esperada; si no, reordenar directo en el editor de Etsy.

### M6. Videos — esquema por composición (config de tienda)
El esquema de videos vive en `data/tiendas/<tienda-id>/config.json` →
`mpl.esquema_videos`. **Esquema vigente** (APROBADO 2026-10-15):
- Formato: 1080×1080, 30fps, H.264, 9.5s, sin audio.
- **Video 1:** 3 lifestyles de SUDADERA (distintos).
- **Video 2:** 3 tomas de PLAYERA (distintas).
- Scripts: `scripts/generar-video-listing.py`; puerta:
  `scripts/verificar-video.py` (movimiento mínimo 3.0) + manifiesto.
- Criterio: `CRITERIO-VIDEO.md`.
- **Si la puerta FALLA, se corrige en la FUENTE (2026-10-20,
  incidente p046 — doctrina del dueño: «eso es hacer trampa para
  pasar»):** el video se REGENERA con el generador (otra toma del
  esquema o parámetros corregidos) hasta pasar por mérito propio.
  **PROHIBIDO** reencuadrar, recortar, acelerar o manipular el
  artefacto reprobado para inflar la métrica: eso pasa la
  medición, no la propiedad. Las decisiones de composición del
  esquema se toman ANTES de generar, nunca como reacción a un
  FAIL. Si el esquema genuinamente no puede cumplirse, se escala
  al orquestador ANTES de subir — jamás se documenta después
  como hecho consumado. (La regla de `publicador-lote` «no
  regenerar» protege videos VÁLIDOS; un video reprobado no es
  válido y se regenera.)

### M7. Publicar el MPL
- En Printify: publicar el MPL (los componentes ya están adentro).
- Se sincroniza a Etsy automáticamente (canal conectado).
- Verificar estado = "Published".

**Idempotencia y resultado incierto (2026-10-20, incidente p052
— costó $0.20 reales):** cada clic en Publish crea un listing en
Etsy y cobra su tarifa de publicación; **el clic es una acción
con costo, no un reintento gratis.** Reglas:
1. **Antes de publicar:** verificar que el MPL no tenga ya
   `external.id` ni exista un listing vivo en Etsy originado en
   él. Si ya existe, NO se publica de nuevo — se adopta el
   existente y se sigue desde ahí.
2. **Un solo clic.** Tras clic, la única verdad es la
   VERIFICACIÓN (poll a `external.id` del producto y a la API de
   Etsy), nunca el estado de la fila en la UI: está OBSERVADO
   (p052) que la fila puede volver a «Unpublished» tras una
   publicación que SÍ se creó en silencio.
3. **Resultado incierto = STOP y verificar por API.** Jamás un
   segundo clic sobre un resultado no verificado: el duplicado
   cuesta otra tarifa, contamina la tienda y su rollback
   (desactivar) NO devuelve la tarifa cobrada.
4. Si un barrido posterior detecta un duplicado: desactivarlo de
   inmediato, registrarlo en la entrada del diseño con el
   impacto en tarifa, y reportarlo como defecto del sistema, no
   como nota menor.

### M8. Verificación en Etsy — FASE C (exhaustiva, 2026-10-15)
Nada se da por sentado. Verificar contra el listing vivo:
- Variaciones correctas ("Sweatshirt"/"T-Shirt" + tallas + colores).
- Precios por variación según la tabla vigente de la tienda
  (`estrategia_precios` en su config; ej. 29222324: sudadera
  $40.99/$44.99/$46.99, playera $25.99/$28.99/$32.99).
- SKUs correctos por variación.
- Orden de imágenes = esquema de 10; hero = lifestyle sudadera.
- Videos: los 2 nuevos presentes y reproducibles (que no se hayan
  borrado en la conversión).
- Título, descripción completa (con "CHOOSE YOUR STYLE"), 13 tags.
- Materiales, atributos, políticas, perfil de envío, cantidades.
- Caja de personalización: NO debe existir en un MPL
  (el MPL no la soporta; si aparece, es error).
- Visibilidad de variantes: "Only show in stock variants and hide out
  of stock" (oculta combos que el proveedor no ofrece).

### M9. Registrar
- Guardar IDs de Printify y Etsy en `data/tiendas/<tienda-id>/registro-listings.json`
  con `tipo: "mpl"` y la lista de componentes.

### M10. Publicidad (Pinterest)
- Skill `puerta-pinterest-pin`: valida pins.
- Crear pins con los mockups de Printify.

---

## Track Single — procedimiento

El flujo single clásico (v0.5.0): pasos 1–10 para todo single.
Si el diseño es personalizable, se suma §Track Single-P (la ruta
automatizada manda sobre cualquier mención anterior a la caja
nativa de Etsy):

1. **Login** (protocolo Google-first, §M0).
2. **Draft en Printify:** subir arte, crear producto draft (producto
   según directriz), colocación según §M1 (min(92% ancho, 95% alto),
   centrada horizontal, sesgo arriba 8–12% desde el tope),
   precios escalonados, título real del diseño. El borrador es
   producción de un diseño ya aprobado en la vitrina (Fase A),
   pendiente de la revisión de ubicación del dueño — nunca una
   propuesta creativa en Printify.
3. **Revisión del dueño** en Printify (placement + mockups).
4. **Paquete de listing** (`paquete-listing-etsy`): título, descripción
   con disclosure IA, 13 tags. Puerta `verificar-paquete.py`.
5. **Mockups:** esquema single vigente = 9 (flat ×3 colores + folded
   decorado ×3 + 3 lifestyles diferentes, hero = lifestyle).
   Rotación de héroes entre productos (§M5).
6. **Videos:** Video 1 = on-model/lifestyle, Video 2 = flat/folded.
   1080×1080, 9.5s, sin audio. Puerta `verificar-video.py`.
7. **Publicar** en Printify → sincroniza a Etsy.
8. **Completar en Etsy:** videos, título, descripción, 13 tags,
   categoría, atributos, production partner = Printify, envío,
   políticas, precios por variación verificados. La personalización
   NO se completa aquí: llega sincronizada desde Printify (§Track
   Single-P) y en Etsy solo se VERIFICA.
9. **Registrar** en `data/tiendas/<tienda-id>/registro-listings.json` con `tipo: "single"`.
10. **Pinterest** (`puerta-pinterest-pin`).

---

## Track Single-P — personalización AUTOMATIZADA (default desde 2026-10-20)

La personalización se define **en Printify** (capas marcadas
personalizables) y se sincroniza a Etsy: el comprador escribe/sube en
la página del listing, ve Live Preview (DTG) y la orden llega con el
diseño aplicado. Verificado en vivo en el sandbox de la tienda
(2026-10-20, fase de personalización). Los criterios de ARTE (zonas,
geometría, contraste) viven en `puerta-arte-propuesta`; aquí vive el
procedimiento.

### P1. Producto NUEVO, diseño NUEVO
- La personalización solo se monta en productos **nuevos** de
  Printify; no se convierte un producto existente ni un componente
  de MPL.
- El diseño personalizable es un diseño nuevo y único (§0: duplicar
  un diseño del MPL = duplicado penalizado).

### P2. Campos — se montan en el editor de Printify, congelados con la aprobación
- Capas de texto y/o imagen con su opción de personalización activa
  (imagen: toggle **"Personalizable image"**).
- **Nombre de capa = contenido + zona** (`Name — red banner`,
  `Credential — below banner`, `Photo — buyer upload`): ese nombre es
  el título que el comprador ve sobre su campo en Etsy.
- **Instrucciones** con dónde va el dato y ejemplo entre corchetes:
  `Enter the name to print in gold script on the red banner [Example: Maria]`.
- **Límites por diseño, nunca el default 1024:** nombre **15**,
  credencial **12** caracteres de partida (más cortos si la zona es
  más angosta). Required ON cuando el diseño no tiene sentido sin
  el dato.
- **Ejemplo realista obligatorio** (política de Etsy: prohibido
  "Your text here" y foto principal en blanco en personalizables):
  estándar de tienda **Maria / RN - ICU**, coherente en la capa
  (mockups), las instrucciones y la primera imagen. El texto de
  ejemplo de la capa lo fija quien tenga el editor abierto — en la
  práctica el dueño en su revisión (~10 s); el paquete verifica que
  quedó puesto.
- **Decisiones cerradas = dropdown, no texto libre:** credencial
  (RN/LPN/CNA/NP…), color de hilo en bordado, etc. El vocabulario
  cerrado vigente y el formato profesional (firma ANCC) viven en
  `puerta-arte-propuesta` ("Formato profesional real"); el diseño
  llega con su ficha de razón y sus campos ya definidos (≤3 del
  comprador por criterio; el tope técnico de la plataforma es 5).
- Máximo **5 campos** por listing (texto + imagen combinados).
- Los campos quedan **congelados con la aprobación del dueño**;
  publicación solo verifica. **Jamás se editan desde Etsy** (rompe
  el mapeo y el preview). **La API de Printify NO expone la
  configuración de personalización** (verificado 2026-10-20 por GET:
  las capas no traen esos campos): corregir un campo = editor de
  Printify + push selectivo de la personalización + re-verificar.

### P3. Comportamiento verificado (sandbox, 2026-10-20)
- **Texto:** el texto del comprador se **escala a la caja** de su
  capa — un nombre largo se achica, no desborda. La caja manda.
- **Imagen:** relleno **FIT** — la foto entra ENTERA con su
  proporción original dentro de la caja (cotas máximas), sin recorte
  y sin deformación, y se imprime como parche rectangular con su
  propio fondo. El comprador **no** tiene herramientas de ajuste
  (solo subir/quitar/reemplazar). Formatos PNG/JPG <100 MB; la foto
  **HEIC de iPhone es excepción manual** (no la acepta el campo).
  El marco del arte se diseña tipo passe-partout (puerta-arte).
- **Live Preview:** disponible en DTG (verificado en Gildan 18000);
  **el bordado está EXCLUIDO** — en bordado las fotos del listing
  venden la confianza. Elegibilidad por blueprint: solo se confirma
  creando el producto y viendo si ofrece preview (sin lista pública).
- **Sandbox de pruebas** (protocolo de la fase): las pruebas sin
  Etsy se hacen en drafts ($0). Las que necesitan Etsy usan UN
  listing inactivo ya pagado como sandbox (IDs en el registro de la
  tienda): limpiar/montar → republicar → precio disuasorio alto →
  activar solo minutos → capturar renders → **desactivar y verificar
  inactivo**. Editar/reactivar antes del vencimiento no cobra fee.

### P4. Publicar y verificar (Fase C-P)
- Publicar desde Printify con la personalización marcada en
  "Details to publish" (push selectivo si el listing ya vive).
- Verificar contra el listing vivo, además de la Fase C general:
  - Los campos visibles en la página pública = nombres, instrucciones
    y límites aprobados (conteo ≤5).
  - La primera imagen muestra el ejemplo realista puesto.
  - Live Preview (DTG) responde con un nombre corto y uno largo:
    sin desborde, legible.
  - Precio = tabla de personalizados de la tienda (con colchón),
    no el precio estándar del producto.

### P5. Órdenes
- La orden llega con el diseño **ya aplicado** y marca
  **"Review needed"**: se aprueba (panel de Printify o API) y pasa
  a producción. Sin edición manual por orden.
- La aprobación automática de respaldo tras X horas **no está
  verificada** (la guía v1 la afirmaba; la doc de revisión no la
  muestra): la operación NO cuenta con ella — aprueba Jarvis.

### P6. Bordado personalizado
- Texto con **fuentes pre-digitalizadas**: se escala sin digitalizar
  por orden (máx. 6 colores de hilo, paleta de 15). La digitalización
  del diseño base es gratis (≤36 h, una vez por diseño).
- Sin Live Preview (§P3): el listing vende con fotos y el ejemplo.
- Handling de bordado ≈10 días → corte práctico de Navidad ~8–10 dic.
- Costos base reales y precios del piloto: config de tienda →
  `personalizados` (leídos de drafts reales, no estimados).

### P7. Ruta manual — excepción consciente (NO el default)
La caja nativa de Etsy + fulfillment manual por orden queda solo
para el esquema **multi-producto manual** (un listing cuyas
variaciones se conectan por SKU a productos Printify distintos),
donde la ruta automatizada no llega: ahí no hay Live Preview ni
diseño aplicado y cada orden se trabaja a mano. Requiere dale
expreso del dueño por listing, sabiendo el costo operativo.

---

## Reglas de seguridad Printify ↔ Etsy (2026-10-15)

- **Editar en Printify NO empuja solo a Etsy.** El listing de Etsy solo
  cambia cuando se publica/republica explícitamente desde Printify.
- **PELIGRO: republicar desde Printify SOBRESCRIBE el listing de Etsy**
  (título, descripción, imágenes, tags) con lo que haya en Printify.
  Por eso: una vez publicado en Etsy, NUNCA republicar completo desde
  Printify. Si hay que cambiar el diseño o variantes, usar publicación
  selectiva (solo los campos necesarios).
- **Push selectivo por categorías** (verificado en UI 2026-10-15): el
  diálogo "Sync and publish changes?" empuja lo marcado en "Details to
  publish". NO hay preview ni descarte de cambios.
- **Mejoras SEO van en Etsy**, directo en el Shop Manager. No vuelven
  a Printify.
- **Modelo de estados**: draft "unpublished" en Printify = NO está en
  Etsy. Publicado = tiene ID de Etsy (external_id) y título real.
  La fuente de verdad del estado es `data/tiendas/<tienda-id>/registro-listings.json`,
  con `tipo: "mpl" | "single"`.
- **MPL:** los componentes single NO se publican por separado una vez
  que pertenecen a un MPL (ver §M1, regla).

## Puertas mecánicas

- **verificar-paquete.py**: el paquete comercial es válido (título
  ≤140, 13 tags ≤20 car., disclosure presente; en MPL: título con
  ambos productos y sección "CHOOSE YOUR STYLE").
- **verificar-video.py**: los videos cumplen el criterio (puerta
  mínima de movimiento 3.0).
- **CHECKLIST-PUBLICACION.md**: ningún listing se declara publicado
  hasta verificar CADA item contra el listing vivo en Etsy.
- **Revisión en Printify**: el dueño valida colocación y mockups
  directamente donde se ve el resultado real. **El ojo del dueño es
  la puerta de calidad visual** — ningún gate numérico la sustituye.

## Calibraciones (mecanismo vs aplicación vs tienda)

- **MECANISMO** (este skill): el flujo es igual para cualquier producto y
  diseño. Printify-first siempre. El track (MPL/single) lo decide el flujo
  bifurcado (§0).
- **TIENDA** (`data/tiendas/<id>/config.json` + `data/tiendas/<tienda-id>/config-propuestas.json`):
  la composición del MPL, los precios base, el esquema de mockups/videos y
  el tipo de lote los define la tienda (vía la estratega), NO este skill.
  Agregar un producto nuevo = ficha en `data/productos/` + esquema en el
  config; el skill no se reescribe.
- **CALIBRACIÓN** (Gildan 18000): posición inicial min(92% ancho,
  95% alto), centrada horizontal, 8–12% desde arriba (corrección del
  dueño 2026-10-17; antes 78% ancho centrado — se veía chico con aire
  en todos lados y él lo agrandaba/subía a mano en cada revisión,
  perdiendo DPI en el zoom). El dueño ajusta por diseño en el editor.
- **CALIBRACIÓN** (Bella+Canvas 3001): blueprint 12, provider 99
  (Printify Choice), verificado vía API 2026-10-15. Placement verificado
  visual en p005 (centrado, aprox 10.5"×11.93"); la puerta numérica de
  placement queda pendiente para este producto.
