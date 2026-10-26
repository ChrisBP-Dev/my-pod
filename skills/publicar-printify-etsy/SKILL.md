---
name: "publicar-printify-etsy"
description: "Publica un diseño aprobado en Printify y Etsy (Printify-first): track MPL nativo (sudadera + playera en un listing) o single-product. Drafts, revisión del dueño, mockups, videos, publicación y verificación en Etsy."
compatibility: "framework >= 0.4.0"
metadata:
  version: "0.14.0"
  framework_version: "0.19.0"
  regression_suite: "evals/"
---

# Publicar en Printify + Etsy (Printify-First + MPL)

**Versión 0.13.0** (2026-10-23, Programa Estándar F3: puerta de completitud de la ficha visual antes de §M5 — `verificar-ficha-visual.py` — y presupuesto de fotos leído de la ficha con techo de plataforma 20. Base: **Versión 0.12.0** (2026-10-23, Programa Estándar My POD F4: la puerta de conteo `verificar-variantes.py` ya no trae default de tienda — `--shop` explícito obligatorio en modo en vivo — y los ejemplos con precios/IDs reales de una tienda pasan a ficticios etiquetados o al config de la tienda activa. Base: **Versión 0.11.1** (2026-10-23: corrección de cobertura — la plana cubre el color sin representar antes de repetir el prioritario; hallazgo del piloto seco de p058 explicado al dueño el mismo día. Base: **Versión 0.11.0** (2026-10-23: **colores sin techo + mockups y
videos con estándar** — consolidación de la propuesta aprobada
por el dueño el 2026-10-23: (1) el tope de 4 colores por prenda
de v0.10.0 queda **eliminado como techo**: 3–4 es la **guía de
producción** por juicio del arte, la extensión a 5–6 está
permitida sin bloqueo con nota operativa, y el dueño en §M2
agrega o quita colores **sin límite del sistema**; la puerta de
conteo solo detiene por el límite técnico del MPL (400
variantes / 70 opciones) y avisa sin detener desde 7 colores
por item. (2) §M5 deja de ser una lista fija de espacios: la
selección de mockups la hace el worker con un **algoritmo
determinista** sobre el **catálogo canónico de tomas por
producto** (`tomas_preferidas` en `data/productos/<producto>.json`)
y los **pesos por composición** del config de tienda, y produce
un **manifiesto de selección** que la puerta
`scripts/verificar-mockups.py` exige en PASS antes de publicar;
el dueño **nunca** elige mockups. (3) §M6: los videos se arman
solo con tomas del manifiesto, con **escenarios A–D** según la
composición; el formato técnico de video vive ahora en este
skill y `CRITERIO-VIDEO.md` (raíz) se retiró como fuente
duplicada que contradecía al esquema.)
**Versión 0.10.0** (2026-10-23: **selección de colores del
diseño** — criterio corregido por el dueño: NO existe paleta
canónica ni quemada en ninguna parte; los colores se eligen
por diseño al producir, según el contraste con el arte
colocado y la disponibilidad del producto, con tope de 4
por prenda; el dueño es el filtro final en su revisión
(§M2 = ubicación + colores) y la fuente de verdad al
publicar es el borrador tal como él lo dejó. Nace de la
auditoría del 2026-10-23: en la Fase B los items salieron
con 3 colores por item, pero por **hábito** — el mismo trío
en 9 de 10 sin juicio por arte; el distinto lo cambió el
dueño a mano. Faltaban el procedimiento de elección, el
alcance formal en la etapa 3, la puerta de conteo y que el
paquete leyera los colores del borrador.)
**Versión 0.9.1** (2026-10-23: lecciones de producción de la Fase B
del lote 2026-10-19 en §M4 — nada de producción en paralelo en la
misma cuenta; el Replace de proveedor regenera el ID y rompe la
referencia del MPL, cierre por re-agregar vía "Your products").
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

**Selección de colores del diseño** (criterio del dueño,
2026-10-15, **corregido y consolidado el 2026-10-23**):

- **No existe paleta canónica.** Ninguna lista de colores
  vive quemada en este skill, en la ficha ni en un registro
  como referencia de validación. «Paleta» como lista fija
  queda **retirada del glosario** de este tema: lo que existe
  es la **selección de colores de cada diseño**, que nace
  con el diseño y vive **solo en su borrador** de Printify.
- **Quién elige y cuándo:** producción, al producir — con el
  arte ya colocado en la prenda, viendo el contraste y la
  legibilidad reales, y según la disponibilidad del producto
  (blueprint/proveedor). El diseño debe verse bien en cada
  color elegido; no se abarcan colores sin verificación
  visual (regla suya 2026-10-15).
- **Guía de producción: 3–4 colores por prenda** (criterio
  del dueño 2026-10-23, **sin techo desde v0.11.0**): es la
  cantidad que producción elige por juicio del arte, **no un
  límite del sistema para nadie**. Si el juicio sobre ESTE
  arte lo justifica (ej.: el arte pide fondos claros **y**
  oscuros), producción puede habilitar **5–6** y el flujo
  sigue, dejando la nota operativa del paso 5 ampliada con
  el porqué de la extensión. Por color van TODAS las tallas
  que el proveedor ofrezca; si un color trae tallas
  limitadas, se acepta como viene. El único techo real es
  el técnico del MPL (400 variantes / 70 opciones), que es
  lo único que la puerta de conteo detiene (§puerta abajo).
- **El trío histórico NO es punto de partida.** Sudadera
  White/Sand/Sport Grey y playera White/Athletic
  Heather/Natural fue el **hábito heredado** de los primeros
  listings, y repetirlo sin mirar el arte es
  **incumplimiento de este criterio** — es exactamente el
  defecto que el dueño señaló el 2026-10-23: en la Fase B,
  9 de 10 diseños salieron con el mismo trío por inercia, y
  el único distinto (p058, oscuros) lo había cambiado **el
  dueño a mano**. Caso de prueba, p059: letras crema sobre
  White/Sand quedan lavadas, casi ilegibles; ese arte pide
  fondos oscuros. Si el juicio sobre ESTE arte respalda un
  color del trío, se usa como cualquier otro candidato —
  nunca por defecto.
- **Procedimiento de elección (por item, obligatorio):**
  1. **Mirar el arte ya colocado:** tonos dominantes del
     trazo y del texto (¿claro u oscuro?), el elemento más
     fino que debe leerse y sus colores de línea.
  2. **Candidatas:** colores disponibles del producto cuyo
     fondo contraste con esos tonos y mantenga legible lo
     más fino. Arte claro → fondos oscuros; arte oscuro →
     fondos claros; arte con fondo propio o bordes
     marcados → fondos que no peleen con ese borde.
  3. **Verificación visual por candidata:** ver el arte
     sobre cada color candidato (preview del editor de
     Printify o composición equivalente) ANTES de decidir.
     Sin esa vista no hay elección — elegir de memoria o
     por hábito es el incumplimiento de arriba.
  4. **Elegir según la guía (3–4; 5–6 si el juicio del
     arte lo justifica, ver arriba)** y dejar **solo esas
     habilitadas**.
  5. **Nota de producción de una línea** en el registro de
     la corrida (tonos del arte → colores elegidos y por
     qué). Es nota operativa de ESE diseño: no se guarda
     como canónica ni sirve de default para el siguiente.
- **El dueño es el filtro final** (§M2): en su revisión
  puede cambiar los colores **sin límite del sistema**
  (agrega o quita los que quiera; su juicio manda sobre la
  guía de producción); su «ya están listos» aprueba
  ubicación **y** colores. Esa elección **no se guarda como
  canónica en ningún registro**: la fuente de verdad al
  publicar es el borrador tal como él lo dejó, y el paquete
  (§M3) y la verificación (§M8) se generan y contrastan
  **leyendo ese borrador**, nunca una lista previa. Como
  §M5 corre DESPUÉS de §M2, cualquier color que el dueño
  agregue lo absorbe el worker al seleccionar los mockups
  desde los colores finales del borrador — el dueño nunca
  elige mockups (§M5).
- **Puerta mecánica (única, de conteo):** antes de mockups
  y antes de publicar, correr
  `scripts/verificar-variantes.py --shop <shop_id de la tienda
  activa>` sobre los items (el shop se pasa explícito desde la
  ficha de la tienda; la puerta no tiene default — corrección
  de colocación 2026-10-23, Programa Estándar F4): cuenta
  colores habilitados por item, variantes y opciones del
  conjunto. **Detiene SOLO por el límite técnico del MPL**
  (>400 variantes totales o >70 opciones). Si un item pasa
  de **6** colores, la puerta **avisa sin detener** (el
  aviso queda en el reporte de la corrida y el flujo
  sigue): 5–6 colores son una extensión válida, no un
  error. La puerta no compara contra ninguna lista.

## Precios escalonados por talla (estándar 2026-10-15, orden del dueño)

**Mecanismo (universal):** el precio NUNCA es plano por talla. Toda talla
cuyo costo base supere al de S–XL lleva recargo:
`recargo = redondeo_a_dólar((costo_talla − costo_base_SXL) × 1.15)`
El ×1.15 cubre el fee de Etsy sobre el incremento (~9.5%) y preserva el
margen en dólares de la talla base.

**Tablas vigentes:** la tabla de cada tienda vive en
`data/tiendas/<id>/config.json → estrategia_precios` (precio base S–XL
por producto; los recargos por talla se calculan con la fórmula de
arriba). Ejemplo FICTICIO (doctrina "precio con colchón"; cifras
inventadas solo para ilustrar la fórmula — la tabla real de cada
tienda vive en su config):

| Producto | S–XL | 2XL | 3XL |
|---|---|---|---|
| Sudadera (ejemplo) | $30.99 | $34.99 (+$4) | $36.99 (+$6) |
| Playera (ejemplo) | $20.99 | $23.99 (+$3) | $27.99 (+$7) |

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
   de cuentas elegir la de la tienda activa (la cuenta que la
   ficha de la tienda declara; nunca una cuenta personal ni la
   de otra tienda).
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
- Aplicar la **selección de colores del diseño** (ver
  «Selección de colores del diseño» arriba: elegir por
  contraste con el arte ya colocado, guía 3–4 por prenda,
  extensión 5–6 permitida con nota) y
  los precios escalonados de la tabla vigente. **Dejar solo
  los colores elegidos habilitados (desmarcar el resto del
  catálogo) es parte de crear el item, no un paso
  posterior** — y lo mismo al agregar cada item dentro del
  MPL (§M4). Ojo al verificar por API: el GET de un producto
  lista también las variantes **deshabilitadas** y el
  universo completo de opciones del blueprint — el conteo
  válido es solo sobre variantes con `is_enabled` en
  verdadero (error de lectura ya cometido una vez,
  2026-10-23: se reportó «catálogo completo habilitado»
  contando las deshabilitadas). Sin publicar nada, correr
  la puerta de conteo (`scripts/verificar-variantes.py`)
  antes de entregar a la revisión del dueño.
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

### M2. Revisión del dueño — ubicación + colores DENTRO del editor del MPL
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
- **También revisa los COLORES** (alcance ampliado por el dueño
  el 2026-10-23): ve la selección que producción eligió por
  diseño y la ajusta en el mismo editor si no le convence —
  desmarcar/marcar colores es reversible y no toca arte,
  ubicación ni precios, y **no tiene límite del sistema**
  (la guía 3–4 y su extensión 5–6 atan a producción, no a
  él). **No revisa ni elige mockups:** en este punto del
  flujo aún no existen; los selecciona el worker en §M5
  desde los colores finales que él deje aquí. Su «ya están listos» aprueba
  **ubicación y colores**; lo que él deja en el borrador es
  lo que se publica (§M3 y §M8 leen de ahí).
- Corrige la ubicación directamente en el editor si hace falta.
- Elimina los rechazados. Avisa cuáles están listos.

### M2.1 Normalización post-revisión — precios y tallas (paso del agente, SIN consulta)
Al cerrar §M2, el agente normaliza CADA borrador aprobado, siempre
y sin pedir aprobación (regla del dueño 2026-10-26: «eso ya se sabe,
es parte del flujo» — no es una decisión por lote). Hecho mecánico
detrás de esta regla: **habilitar un color en el editor de Printify
lo deja con el precio default de Printify y con la gama de tallas
parcial**, aunque el resto del borrador esté correcto; si nadie
normaliza, el listing vende bajo el piso de margen y con tallas
faltantes. La normalización, por API y por producto:
1. Fijar el precio de TODA variante habilitada según la **tabla
   con colchón** de la ficha del producto (sección «Precios
   escalonados por talla» de este skill), con el payload mínimo
   verificado (`title` REAL del GET + `description` + `tags` +
   solo variantes habilitadas; el `title` del payload es
   autoritativo: jamás uno reconstruido).
2. Completar la gama **S–3XL** de cada color elegido: habilitar
   las variantes de ese color y esa gama que existan en el
   producto y estén deshabilitadas, cada una con su precio de
   tabla. (Colores no elegidos y tallas fuera de la gama — XS,
   4XL+ — no se tocan.)
3. Verificar por API: toda variante habilitada a su precio de
   tabla y gama completa por color; el resultado queda en el
   registro del listing.
Sin esta verificación en PASS no se entra a §M5. La misma
normalización aplica cuando un color se agrega o se quita en
cualquier momento posterior (p. ej., al adoptar un external
inactivo): agregar colores sin normalizar deja el borrador en
estado no publicable.

### M3. Paquete de listing — SEO completo para TODOS los productos
- Generar con el skill `paquete-listing-etsy`.
- **Colores del paquete = los del borrador, leídos por API**
  (los que el dueño dejó aprobados en §M2). Nunca escritos a
  mano ni tomados de una lista guardada: si el borrador
  cambió, el paquete se regenera desde su lectura vigente.
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
- **Lecciones de producción (Fase B del lote 2026-10-19, ejecutada
  2026-10-23; verificadas en vivo, 10 MPLs):**
  - **NUNCA producción en paralelo en la misma cuenta:** dos
    ventanas trabajando a la vez en Printify se cruzan — el flujo
    de una tomó la playera de rescate de otro diseño, la renombró
    y le cambió el arte (p059/p062). Una unidad a la vez por cuenta.
  - **El item creado desde el catálogo nace con Printful** (el
    flujo "Add item" no deja elegir proveedor) y "Replace print
    provider" **regenera el ID del producto**: el MPL queda
    apuntando al producto viejo y puede romperse o no dejar
    guardar (pricing $0.00 en el MPL, p059; MPL que dejó de cargar,
    p063). Tras el Replace, el cierre fiable es: quitar el item
    roto del MPL y re-agregar el producto nuevo vía "Your
    products" — mismo patrón de rescate de arriba, anotado en el
    registro del diseño.
  - **La validación del MPL exige nombres de producto distintos:**
    la playera lleva el título del diseño + " - T-Shirt" como
    nombre interno (no toca el título del listing ni los nombres
    de variación "Sweatshirt"/"T-Shirt").
  - **El diálogo "Your products" puede no listar un producto
    recién creado** (índice desactualizado de Printify): si no
    aparece, se espera y se reintenta en otra corrida (patrón de
    reintentos acotados), no se crea otro duplicado.
  - **Un componente puede aparecer "Published" sin clic de
    publicación** (observado en p064: la sudadera base se sincronizó
    como single a Etsy durante la producción). Si pasa: "Hide on
    Etsy" de inmediato, verificar por la API de Etsy que el listing
    quedó `inactive`, y anotar el incidente en el registro — la
    decisión de fondo (borrar el listing o adoptarlo al publicar
    el MPL, que conserva la URL del base) es del dueño.
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

### M5. Mockups — selección del worker por algoritmo (v0.11.0)

**Quién selecciona: el worker (área de publicación), siempre.
El dueño NUNCA elige mockups** — su revisión (§M2) es solo
ubicación + colores, y ocurre ANTES de este paso: el algoritmo
lee los colores FINALES que él dejó en el borrador. **Los
mockups que Printify deje marcados por defecto NO son una
selección válida:** sin manifiesto generado y verificado, el
listing no tiene mockups.

**Puerta de completitud de la ficha visual (v0.13.0, Programa
Estándar F3 — ANTES de seleccionar nada):** correr
`scripts/verificar-ficha-visual.py --config <config de la
tienda> --producto <ficha de cada producto del listing>`. La
puerta lee el estado de la estrategia visual que este paso va
a consumir (`mpl.esquema_mockups.estado` del config y
`tomas_preferidas.estado` de cada ficha de producto):
- **`sin_configurar` o ausente → DETENER.** Se reporta qué
  campo falta y en qué paso se llena («Calibración visual de
  la tienda» de `onboarding-tienda`: presupuesto/reparto en el
  descubrimiento visual de la Fase 1; catálogo por producto
  en la Fase 4). No se inventan valores ni se usan defaults.
- **`provisional` → solo PILOTO DECLARADO:** el paso puede
  correr, y el piloto queda anotado en el registro del
  listing y en el reporte de la corrida. Nunca es operación
  normal.
- **`configurado` → operación normal.**
La misma puerta aplica al dar de alta un producto o una
composición nueva: sin su calibración visual, no entra a
producción.

**Calibración de tomas con etiquetas reales (requisito del
MARCADO, canonizado 2026-10-26 — evidencia F8 del piloto p058):**
el manifiesto se genera con el catálogo en estado provisional,
pero el **marcado en Printify y todo lo que cuelga de él
(descargas, videos §M6, publicación §M7) exigen el catálogo
CALIBRADO**: cada toma de `tomas_preferidas` con su campo
`etiqueta_printify` = la etiqueta EXACTA que la biblioteca de
mockups de Printify muestra para ese producto (p. ej.
`Lifestyle 2`, `Person 3`, `Front 2`, `Folded 2`), y
`tomas_preferidas.estado` = `configurado_con_pase_del_dueno`
(la puerta `verificar-ficha-visual.py` reconoce el estado por
el prefijo `configurado`). El pool real no usa
los ids del catálogo sembrado (evidencia: sudadera Gildan
18000 = 15 tipos de vista; playera Bella+Canvas 3001 = 33;
en `data/mockups/F8-pool-printify-2026-10-26.md`). Con el
catálogo provisional, el marcado se DETIENE por diseño tras
generar el manifiesto — no es una falla ni una improvisación:
el flujo presenta en ese momento la **sesión de calibración**
como el paso requerido. La sesión (única por producto, con el
dueño): se le muestran las vistas reales del pool, agrupadas
por producto y rol, con su etiqueta; él elige qué etiqueta
llena cada rol (principal, secundaria, plana, doblada,
detalle) y las decisiones se escriben AL INSTANTE en la ficha
del producto (`etiqueta_printify` por toma + `estado:
configurado_con_pase_del_dueno`). Con el catálogo calibrado, el marcado compara el
manifiesto contra `etiqueta_printify` — correspondencia 1:1
sin juicio del worker — y los manifiestos se regeneran si la
calibración cambió alguna toma. La tabla de tallas se marca
con la etiqueta `Size Chart` del color prioritario (la imagen
es idéntica en todos los colores; convención de mecanismo,
no decisión visual).

**Modelo de selección v2 — POOL PRIMARIO ROTATIVO
(v0.14.0, calibración del dueño 2026-10-26; reemplaza al
héroe fijo de la v1):** el catálogo de cada producto declara
su conjunto favorito como tomas de rol `principal` (el POOL,
ordenado por `prioridad`). No hay héroe fijo ni color fijo:
- El héroe de cada listing es la primera toma del pool
  ROTADO por el índice del diseño en su lote (`rotacion` de
  la entrada del generador); el color prioritario también
  rota por diseño (contraste + rotación de la entrada).
- Las demás tomas del pool se reparten entre los colores
  siguientes antes de repetir una toma en otro color
  (criterio del dueño: «si elegí cuatro favoritas y tengo
  cuatro colores, cada mockup en un color»).
- La plana solo entra si el catálogo la declara (la playera
  calibrada no usa plana: se exhibe con Lifestyle + Hanging).
- La extensión (rol `secundaria`) entra solo cuando los
  espacios/colores lo piden tras agotar pool y plana.
- Criterio de fondo del dueño (esta tienda): fondos con
  escena, evitar el blanco; las tomas no elegidas en su
  calibración quedan fuera del catálogo o en
  `tomas_a_evitar` con su motivo.
La puerta `verificar-mockups.py` verifica contra este
modelo: héroe = pool rotado, plana solo si el catálogo la
declara, sin pares (toma, color) repetidos.

**Insumos (ninguno quemado en este skill):**
- **Catálogo canónico de tomas por producto:**
  `data/productos/<producto>.json` → `tomas_preferidas` +
  `tomas_a_evitar` (cada toma con su identificador documentado,
  rol, prioridad y fuente). **Producto sin catálogo = este
  paso se detiene y reporta** (no improvisa, no usa defaults):
  el alta del catálogo es parte del alta del producto.
- **Pesos por composición:** `data/tiendas/<tienda-id>/config.json`
  → `mpl.esquema_mockups` (total de imágenes, espacios
  visuales del producto principal y del secundario, 1 tabla
  de tallas por producto). El producto principal es el
  primero de la composición. Otra composición declara SUS
  pesos y cada producto trae SU catálogo: nada se hereda en
  silencio de la composición default. **El total de imágenes
  es el presupuesto que la ficha de la tienda declara en su
  calibración visual, con techo de plataforma 20** (Etsy
  permite 20 fotos por listing desde ago-2025; el generador
  de manifiesto no tiene default y detiene si el total falta
  o supera 20). **Semántica del total (2026-10-24, hallazgo
  P3 de la prueba de frío): el total es META EXACTA derivada
  = espacios visuales de los items + tablas de tallas; si la
  ficha no cuadra, el generador se detiene temprano
  declarando la inconsistencia — no genera de menos ni deja
  que la puerta falle tarde por conteo.**

**Algoritmo (determinista — ejecutor:
`scripts/generar-manifiesto-mockups.py`):**
1. Leer los colores finales de cada item del borrador por
   API (post-§M2, tal como el dueño los dejó), con su tono
   (claro/oscuro) y el **color prioritario** por item
   (juicio de contraste del worker + rotación de héroes del
   lote, ver abajo).
2. Ordenar los colores: prioritario primero; después
   alternando un claro y un oscuro.
3. Repartir los espacios según los pesos de la composición
   y aplicar las **garantías mínimas por producto**: toma
   principal en el color prioritario; segunda pose distinta
   en el siguiente color; y una plana, cuyo color sale de la
   cobertura: si queda un color sin representar, la plana lo
   cubre; solo si todos están representados va en el
   prioritario. (Corrección 2026-10-23, hallazgo del piloto
   seco de p058: la plana en el prioritario repetía color y
   dejaba un tercer color sin foto pudiendo entrar.)
   Después, cobertura por turnos de los colores aún no
   representados y relleno sin repetir par (toma, color).
4. **Restricciones duras:** nunca repetir la misma pose o
   modelo en otro color (aplica a tomas con modelo; la
   plana sí puede repetirse en otro color — evidencia
   p046); nunca usar una toma de `tomas_a_evitar` ni fuera
   del catálogo de ese producto. Sustitución reglada: si la
   toma preferida no está disponible, se baja a la siguiente
   prioridad del mismo rol y queda registrada.
5. **La regla «todos los colores representados» queda
   RETIRADA** (era imposible: la playera tiene 3 espacios
   visuales y puede vender 4+ colores). La reemplaza la
   declaración honesta: **todo color vendido sin espacio
   queda declarado en el manifiesto con su motivo**.

**Salida obligatoria — manifiesto de selección** por diseño
(mismo patrón que los manifiestos de video): cada espacio =
{posición, producto, color, toma, etiqueta de cámara, rol} +
colores sin representación declarados + sustituciones. Los
checkboxes marcados en Printify deben coincidir
**exactamente** con el manifiesto.

**Puerta:** `scripts/verificar-mockups.py` contra el
manifiesto y los colores del borrador — imagen principal
correcta (producto principal, toma prioridad 1, color
prioritario), garantías mínimas, sin pose repetida, sin
tomas a evitar ni fuera de catálogo, sin-representación
declarados. **Sin PASS, §M7 no corre.** Si falla, el worker
re-selecciona en la fuente (regenera el manifiesto), jamás
edita el manifiesto para pasar la medición.

**Rotación de héroes entre productos** (criterio suyo 2026-10-15): en
cada lote, ROTAR el modelo lifestyle y el color del héroe. Dos
productos consecutivos NUNCA comparten modelo ni color de héroe.
Aplica igual al primer clip del video 1.

**Nota primario Printify vs Etsy** (observado 2026-10-15): Printify
marca un primario pero al sincronizar el orden puede no preservarse.
Tras el sync, VERIFICAR en Etsy que la imagen principal sea la
esperada; si no, reordenar directo en el editor de Etsy.

### M6. Videos — escenarios A–D, siempre desde el manifiesto (v0.11.0)

**Principio único:** los videos se arman SOLO con tomas del
**manifiesto de mockups de §M5** (seleccionadas por el worker),
nunca con los defaults de Printify ni con elecciones del
dueño. Qué escenario aplica lo decide la composición y la
cobertura del manifiesto, según `mpl.esquema_videos` del
config de tienda:

- **Escenario A — MPL default (2 productos):** Video 1 =
  producto principal: 3 tomas de su bloque del manifiesto —
  la imagen principal primero, otra pose distinta, una plana
  o detalle; colores distintos entre sí si el manifiesto
  cubre ≥3 colores de esa prenda. Video 2 = producto
  secundario, con la misma lógica sobre sus tomas.
- **Escenario B — un producto con solo 1–2 colores
  cubiertos:** las tomas de su video varían por **tipo**
  (modelo, plana, doblada/detalle) en vez de por color; queda
  registrado en el manifiesto de video.
- **Escenario C — single (un producto):** Video 1 = tomas
  con modelo/lifestyle del manifiesto; Video 2 = plana →
  doblada decorada → detalle, del color principal.
- **Escenario D — composición futura (otro product
  listing):** se aplica A/B con el **producto principal
  según el peso de esa composición** y el catálogo de tomas
  de ESE producto.

**Formato técnico (única fuente desde v0.11.0 — absorbido
del retirado `CRITERIO-VIDEO.md` de la raíz, cuya estructura
de videos contradecía a este esquema):**
- Resolución 1080×1080 (1:1), 30 fps, H.264 (libx264),
  duración 9.5s (3 clips de 3.5s con fades solapados de
  0.5s, offsets 3.0s y 6.0s, xfade fade — nunca corte
  directo), sin audio, ~1–3 MB.
- **Pixel format yuv420p de rango LIMITADO (tv)
  obligatorio** (verificado 2026-10-15): Etsy RECHAZA
  yuvj420p (rango completo). El flag `-pix_fmt yuv420p`
  solo NO basta — el filtro debe incluir
  `scale=out_range=limited,format=yuv420p` (ver
  `scripts/generar-video-listing.py`).
- **Movimiento sin temblor:** zoom-in 1.0 → 1.25 con
  posición absoluta por frame (`z='1+0.25*on/105'`) —
  NUNCA zoom acumulativo por pasos (trunca a píxeles
  enteros y tiembla; ver `LECCION-ZOOMPAN-SIN-TEMBLOR.md`).
  Se escala primero a 2160×2160 y zoompan baja a 1080;
  centrado `x='iw/2-(iw/zoom/2)'`, `y='ih/2-(ih/zoom/2)'`.
- Scripts: `scripts/generar-video-listing.py`; puerta:
  `scripts/verificar-video.py` (movimiento mínimo 3.0) +
  manifiesto de video (que referencia las tomas del
  manifiesto de mockups usadas).
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
- Variaciones correctas ("Sweatshirt"/"T-Shirt" + tallas +
  colores) — **contra la lectura del borrador de Printify
  tal como el dueño lo dejó** (§M2), que es la fuente de
  verdad; nunca contra una lista previa o «esperada».
- Conteo previo a publicar (puerta de §M1): la puerta solo
  detiene por el límite técnico (MPL >400 variantes o >70
  opciones); un item con >6 colores genera aviso
  informativo en el reporte, sin detener ni corregir lo que
  el dueño dejó.
- Precios por variación según la tabla vigente de la tienda
  (`estrategia_precios` en el config de la tienda activa; sin
  precios quemados en este skill).
- SKUs correctos por variación.
- Orden de imágenes = **manifiesto de mockups verificado**
  (§M5, puerta en PASS); imagen principal = posición 1 del
  manifiesto (toma principal del producto principal de la
  composición, en su color prioritario).
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
5. **Mockups:** también salen del **manifiesto** (§M5: mismo
   algoritmo, mismo catálogo `tomas_preferidas` del producto;
   el reparto de espacios del track single se declara en la
   entrada del manifiesto). Hero = toma principal del
   producto. Rotación de héroes entre productos (§M5).
6. **Videos:** **escenario C de §M6** (Video 1 = tomas con
   modelo del manifiesto; Video 2 = plana → doblada decorada
   → detalle del color principal). Formato técnico de §M6.
   Puerta `verificar-video.py`.
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
- **verificar-variantes.py**: conteo de colores/variantes —
  detiene solo por el límite técnico del MPL (400 variantes /
  70 opciones); sin techo de colores (§Selección de colores).
- **verificar-ficha-visual.py**: completitud de la ficha
  visual ANTES de §M5 (v0.13.0) — `sin_configurar` detiene
  nombrando el paso de onboarding que lo llena; `provisional`
  solo permite piloto declarado; `configurado` = operación
  normal.
- **verificar-mockups.py**: el manifiesto de selección de
  mockups cumple el algoritmo de §M5 (principal correcta,
  garantías mínimas, sin pose repetida, sin tomas a evitar,
  sin-representación declarados). Sin su PASS no se publica.
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
  la composición del MPL, los precios base, los pesos de mockups y los
  escenarios de video los define la tienda (vía la estratega), NO este skill.
  Agregar un producto nuevo = ficha en `data/productos/` **con su
  catálogo `tomas_preferidas` sembrado** (§M5: sin catálogo no hay
  producción) + pesos en el config si entra en una composición;
  el skill no se reescribe.
- **CALIBRACIÓN** (Gildan 18000): posición inicial min(92% ancho,
  95% alto), centrada horizontal, 8–12% desde arriba (corrección del
  dueño 2026-10-17; antes 78% ancho centrado — se veía chico con aire
  en todos lados y él lo agrandaba/subía a mano en cada revisión,
  perdiendo DPI en el zoom). El dueño ajusta por diseño en el editor.
- **CALIBRACIÓN** (Bella+Canvas 3001): blueprint 12, provider 99
  (Printify Choice), verificado vía API 2026-10-15. Placement verificado
  visual en p005 (centrado, aprox 10.5"×11.93"); la puerta numérica de
  placement queda pendiente para este producto.
