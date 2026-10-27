# Flujo Pipeline POD — Printify-First + MPL (2026-10-15)

**Estado: actualizado 2026-10-15 con las decisiones del dueño (flujo MPL
nativo + flujo bifurcado por personalización). Reemplaza el flujo single
del 2026-10-14 como default. Alineación 2026-10-22 (orden del dueño):
ruta MPL única — borrador base → conversión → items creados dentro
del MPL — y aprobación creativa SOLO en la vitrina antes de producir
(etapa 1); lo de Printify es producción (etapa 2) y revisión de
ubicación + colores (etapa 3, alcance de colores desde 2026-10-23),
nunca propuesta creativa.**

## Principio
Printify es la fuente de verdad para cómo se ve el producto.
No predecimos con mockups propios; usamos los de Printify directamente.
Toda mejora de este flujo se declara cerrada solo tras pasar `docs/PUERTA-CIERRE.md`.

## Flujo bifurcado (orden del dueño 2026-10-15)
- **Diseño personalizable** (nombre/texto del comprador) → **track single**
  (el MPL nativo NO soporta personalización). Producto individual.
- **Diseño NO personalizable** → **track MPL**: sudadera Gildan 18000 +
  playera Bella+Canvas 3001 en un solo listing (composición default;
  la estratega puede definir otra en `data/tiendas/<tienda-id>/config-propuestas.json`).
- Detalle operativo: `skills/publicar-printify-etsy/SKILL.md`.
- Contrato estratega → propuestas → publicación:
  `docs/CONTRATO-TIPO-PRODUCTO.md`.

## Etapas

### 1. Arte + aprobación del dueño (Fase A — flujo v2, 2026-10-19)
- Generar arte en alta calidad: PNG sin fondo, 300 DPI, recortado exacto.
- Puerta mecánica COMPLETA: `puerta-arte-propuesta` v0.5.0+ (composición
  sobre el crudo, limpieza, autotrim seguro, fidelidad contra el crudo).
- **Entrega para aprobación:** cada arte que pasa la puerta se
  entrega al dueño **en la vitrina de revisión de la tienda**,
  con su **porqué** (tema y ángulo de la directriz, frase,
  iconografía y su motivo, y qué mirar al revisar — p. ej. los
  counters, que la puerta declara pendientes del ojo humano).
  El porqué se guarda en el registro (`porque` por diseño) y lo
  hereda el paquete comercial.
- **Puerta del dueño, por diseño — superficie ÚNICA: la vitrina**
  (canonizada el 2026-10-22; el mismo día el dueño retiró el
  chat como superficie de esta fase): el dueño aprueba, rechaza
  o pide ajuste ANTES de que se produzca nada, **en la vitrina
  de revisión** de la tienda (contrato en `docs/VITRINA-VIVA.md`;
  la vitrina lee en vivo el repo de datos desde 2026-10-26, sin
  siembra): la entrega produce las previas del lote en su hogar
  del repo con `scripts/producir-previas-vitrina.py`, registra
  los entregados en el estado de la tienda y commitea todo en
  la misma corrida — con ese commit el lote ya está en la
  bandeja (continua, una instancia sola por tienda, declarada
  en `vitrina` de su `config.json`). **El chat
  solo avisa:** un aviso breve en el chat de entrega (qué lote,
  cuántos diseños, el acceso a la vitrina), sin artes adjuntos.
  El dueño decide en la vitrina (sus decisiones se escriben al
  instante en el repo), marca las decisiones con
  «Marcar listas para Jarvis» y avisa en un chat, y la
  recogida-aplicación al checkpoint sigue el procedimiento
  «Recogida-aplicación de decisiones (vitrina en vivo)» de
  `puerta-arte-propuesta`. Ninguna aprobación vale
  hasta estar registrada en el checkpoint
  (`data/tiendas/<tienda-id>/estado-propuestas.json`, registro
  versionado de la tienda). Lo
  aprobado se enlista (la cola persiste entre días; no caduca).
  Lo rechazado no consume producción. Lo ajustado (mejorar)
  vuelve solo a esta etapa.
  (Flujo v2, idea del dueño 2026-10-19: el dale creativo se mueve al
  punto más barato — antes el arte se revisaba recién en Printify,
  con el trabajo de drafts ya gastado.)
- **Diseño personalizable:** la entrega trae el arte real (zonas
  vacías) **más la simulación** del resultado esperado (compuesta
  sobre el arte real con el ejemplo derivado del concepto en las
  zonas medidas), y su **ficha de razón completa** (razón, prueba de
  borrado, campos, ocasión, encaje, peor caso) con producto destino
  y plan de zonas — detalle en `puerta-arte-propuesta` (criterios de
  personalizables + entrega, variante personalizable). Sin ficha no
  hay entrega. Su aprobación cubre diseño + producto + zonas.

### 2. Producción (borradores en Printify) — Fase B: solo aprobados
- **Solo `aprobados` registrados** en el checkpoint
  (`estado-propuestas.json`) vía la recogida de la vitrina.
  Nada se produce desde la vitrina ni desde una decisión no
  registrada. **Nada llega a Printify como propuesta:** la
  aprobación creativa ya ocurrió en la etapa 1 (la vitrina).
- **Track MPL — ruta ÚNICA (alineación 2026-10-22):** se crea SOLO
  el borrador del producto base (el primero de la composición),
  se convierte a MPL («Convert to Multi-Product Listing») y los
  demás productos se CREAN dentro del MPL desde el catálogo con
  el mismo diseño (Printify no crea un MPL vacío desde cero: la
  conversión del base es la entrada). Resultado: **un borrador MPL
  por diseño**, "unpublished", pendiente de la revisión de
  UBICACIÓN + COLORES (etapa 3). Crear los componentes como borradores
  sueltos y ensamblarlos después es la ruta VIEJA, descartada —
  solo vive como rescate de componentes ya creados por lotes
  anteriores, anotado en el registro (detalle: `publicar-printify-etsy`
  §M1/§M4). Los componentes NUNCA se publican por separado.
- **Track single:** un borrador del producto indicado.
- **Track single personalizable:** un borrador del producto indicado con
  los campos de personalización montados en Printify (ruta
  automatizada, `publicar-printify-etsy` §Track Single-P). El diseño
  es siempre nuevo y único; nunca se convierte un diseño del MPL.
- El tipo de lote (mpl/single/mixto) lo define la estratega en
  `data/tiendas/<tienda-id>/config-propuestas.json` (dinámico por semana).
- Posición inicial (RECALIBRADA 2026-10-17): escala = min(92% del
  ancho del área, 95% del alto), centrada horizontal, borde
  superior al 8–12% del alto del área (sesgo arriba). El 78%/14%
  anterior quedó descartado (se veía chico y bajo).
- **Selección de colores del diseño (criterio del dueño,
  consolidado 2026-10-23):** al crear cada item, con el arte ya
  colocado, producción elige sus colores **juzgando ESTE arte**
  (tonos dominantes → fondos que contrasten; verificación
  visual del arte sobre cada candidata antes de decidir;
  procedimiento completo en el skill) — **guía de 3–4 por
  prenda, sin techo** (extensión a 5–6 permitida si el arte lo
  justifica, con nota; el dueño en la etapa 3 cambia colores
  sin límite del sistema) —
  y deja solo los elegidos habilitados (desmarcar el resto es
  parte de crear el item). **Repetir el trío histórico
  (White/Sand/Sport Grey · White/Athletic Heather/Natural)
  sin ese juicio es incumplimiento**: fue el hábito que el
  dueño corrigió (Fase B: 9/10 con el mismo trío; el distinto
  lo cambió él a mano). **No hay paleta canónica** en ninguna parte: la
  selección vive solo en el borrador. Antes de entregar a la
  etapa 3 se corre la puerta de conteo
  (`publicar-printify-etsy/scripts/verificar-variantes.py
  --shop <shop_id de la tienda activa>`, sin default).
  Detalle y glosario: skill `publicar-printify-etsy`
  §Selección de colores del diseño.
- Detección de borradores: agrupar por diseño (título real); no
  duplicar diseños que ya tienen su MPL producido (ver contrato §E).

### 3. Revisión del dueño (ubicación + colores, en Printify)
- **Ubicación y colores, dentro del editor del MPL** (por item):
  es la segunda validación del dueño; la creativa fue la etapa 1
  en la vitrina. No hay revisión por borrador componente suelto.
  En colores: ve la selección que producción eligió por diseño
  (guía 3–4 por prenda, o 5–6 con nota) y la ajusta si quiere,
  **sin límite del sistema** — desmarcar/marcar
  es reversible y no toca arte, ubicación ni precios. Su aviso
  de «listos» aprueba **ubicación y colores**, y lo que deja en
  el borrador es lo que se publica: las etapas siguientes leen
  los colores **del borrador**, nunca de una lista guardada.
- **Piloto flujo nocturno (desde lun 2026-10-19, decisión del dueño
  2026-10-18, piloto de 1 semana; orden actualizado por el flujo v2
  del 2026-10-19):** la corrida de las 18:00 entrega las artes para
  su aprobación (etapa 1) y produce los diseños ya aprobados
  (etapa 2); el dueño entra a Printify EN LA NOCHE, antes de dormir,
  y revisa la UBICACIÓN en los drafts de lo producido. La producción
  posterior (mockups → videos → paquete → publicación) corre de
  noche tras sus dales; Pinterest corre a las 08:50 de la mañana
  siguiente sobre lo ya publicado y el watchdog a las 07:50. Si una
  noche no puede revisar, el lote espera y lo aprueba cuando pueda —
  el flujo no se rompe.
- Corrige ubicación directamente en el editor si hace falta.
- Elimina los rechazados. Los que quedan = aprobados para continuar.
- Avisa cuáles están listos.

### 3.1 Normalización post-revisión — precios + tallas (del agente, sin consulta)
Paso obligatorio al cerrar la etapa 3, ejecutado por el agente
SIEMPRE y sin pedir aprobación (regla del dueño 2026-10-26:
los precios correctos son parte del flujo, no una consulta por
lote). Habilitar un color en el editor lo deja con el **precio
default de Printify** y con la **gama de tallas parcial**; la
normalización (detalle y mecanismo: skill
`publicar-printify-etsy` §M2.1) fija por API el precio de tabla
con colchón en toda variante habilitada y completa la gama
S–3XL de cada color elegido, con verificación por API al final.
**Puerta de entrada a la etapa 4:** normalización verificada
en el registro del listing. La misma normalización corre si un
color se agrega o se quita en cualquier momento posterior.

### 4. Mockups (desde Printify — selección del worker por algoritmo; desde 2026-10-26, modelo v2 de pool primario rotativo, §M5 v0.14.0)
La lista fija de imágenes se retiró. La selección la hace el
**worker** (el dueño nunca elige mockups; su revisión de la
etapa 3 es solo ubicación + colores y va ANTES de esta etapa,
así que los colores que él agregue los absorbe esta selección):
- El worker genera el **manifiesto de selección** con
  `publicar-printify-etsy/scripts/generar-manifiesto-mockups.py`
  desde los colores FINALES del borrador (post-etapa 3), el
  **catálogo canónico de tomas de cada producto**
  (`data/productos/<producto>.json` → `tomas_preferidas`) y el
  **presupuesto de la composición** (`config.json` →
  `mpl.esquema_mockups`): **20 imágenes = el techo REAL de
  plataforma** (Etsy admite 20 fotos desde ago-2025 y Printify
  permite seleccionar 20; el total de 10 anterior era un
  esquema propio heredado de la lista fija, retirado por el
  dueño el 2026-10-26). El reparto es por COBERTURA: las
  tablas de tallas (1 por producto) siempre entran; cada color
  vendido parte con 1 espacio y los extras alternan entre
  items desde el principal — el objetivo es mostrar TODAS las
  variantes hasta donde el límite real alcance; si un color
  queda fuera es por el techo real y se declara. Algoritmo:
  skill `publicar-printify-etsy` §M5.
- Puerta: `verificar-mockups.py` en PASS (imagen principal =
  pool rotado, garantías por producto, sin par (toma, color)
  repetido, sin tomas a evitar). Sin PASS no se publica. Los colores
  vendidos sin espacio quedan **declarados en el manifiesto**
  (la regla «todos representados» era imposible y se retiró).
- Rotación de héroes entre productos (modelo y color no se repiten en
  consecutivos).
- Descargar los mockups seleccionados (los del manifiesto).
- ⚠️ 2026-10-15 (lección): en Printify, **mockups SELECCIONADOS ≠ vistas
  descargables**. Solo los mockups con checkbox marcado se sincronizan a Etsy.
  Hay que marcar ANTES de publicar exactamente las vistas del
  manifiesto (o republicar solo-mockups después). Verificar el conteo "N/20
  selected" **contra el manifiesto**. Los que Printify deje
  marcados por defecto NO son una selección válida.
- **Requisito del marcado: catálogo de tomas CALIBRADO**
  (canonizado 2026-10-26, evidencia F8 del piloto p058 — skill
  §M5): el marcado compara el manifiesto contra el campo
  `etiqueta_printify` de cada toma (la etiqueta exacta del pool
  real de Printify) y exige `tomas_preferidas.estado` =
  `configurado_con_pase_del_dueno`. Con el catálogo provisional
  la etapa se detiene POR DISEÑO tras el manifiesto y el flujo
  presenta la **sesión de calibración de tomas** como el paso
  requerido: sesión única por producto en la que el dueño,
  viendo las vistas reales con su etiqueta, elige qué etiqueta
  llena cada rol; las decisiones se escriben al instante en la
  ficha del producto. Sin calibración no hay marcado, ni
  descargas, ni videos (etapa 5), ni publicación (etapa 7).

### 5. Videos
- Generar videos con `scripts/generar-video-listing.py` SOLO
  desde las tomas del **manifiesto de mockups** de la etapa 4,
  con los **escenarios A–D** del skill `publicar-printify-etsy`
  §M6 (A: MPL de 2 productos · B: producto con 1–2 colores
  cubiertos · C: single · D: composición futura según su peso
  y su catálogo). Escenario vigente por tienda:
  `config.json` → `mpl.esquema_videos`.
- Formato técnico (única fuente: §M6 del skill): 1080×1080,
  30 fps, 9.5s, H.264 yuv420p rango limitado, zoom sin
  temblor, fade 0.5s.
- Puerta: `scripts/verificar-video.py`.

### 5.1 Staging de video — ciclo de vida (2026-10-21)

Regla de la app, alineada con el estándar de datos de
instancia del framework (`rameli/docs/DATOS-INSTANCIA.md`):

- Toda zona de staging — la carpeta temporal donde un
  flujo deposita frames, tomas intermedias, manifiestos de
  generación o cualquier material de trabajo — **nace
  declarada**: antes de crearla, o en el mismo acto, se
  anota en `datos.zonas_staging` de `rameli.json` con su
  flujo dueño y su condición de cierre. Una zona de
  staging no declarada es un remanente en formación.
- Al **cierre verificado** del flujo (salidas publicadas o
  promovidas a su hogar canónico y registro completo), el
  staging **se purga como parte del cierre**: sale del
  tracking, del historial si llegó a versionarse, y del
  disco. El cierre no está completo mientras el staging
  siga vivo.
- Un staging **solo sobrevive** con un consumidor vivo
  declarado en su misma declaración (quién lo lee y para
  qué) **y fecha de revisión**; vencida la fecha sin
  consumidor, se purga en la corrida que lo detecte.
- Los medios de staging no se versionan como si fueran
  datos. Si un intermedio merece conservarse, se
  **promueve** a su hogar canónico (`data/videos/` para
  los videos finales) con su registro; lo demás es
  desechable por diseño.
- **Caso fundacional:** `tmp/videos-pendientes/`, staging
  de la sesión de videos del 2026-10-16. El flujo cerró y
  publicó ese mismo día, pero la carpeta sobrevivió 5
  días sin consumidor ni declaración hasta que un censo la
  cazó. Eliminada el 2026-10-21 por decisión del dueño
  (evidencia en `docs/FASE-MEJORA-V0160-PROPUESTA.md`,
  propuesta P2, y en `docs/MIGRACION-RAMELI-V0160.md`).
  Hoy la app no reconoce ninguna zona de staging viva:
  `datos.zonas_staging` va vacío, y la regla queda escrita
  igual.

### 6. Paquete de listing
- Skill `paquete-listing-etsy`: título, descripción, 13 tags, copy.
- **Track MPL:** re-optimización COMPLETA para TODOS los productos:
  título con ambos productos (≤140), descripción con sección
  "CHOOSE YOUR STYLE", 13 tags ≤20 car.
- Puerta: `verificar-paquete.py`.
- Dale del dueño (confía en puerta para SEO).

### 7. Publicación
- Skill `publicar-printify-etsy` (track MPL o single según §Flujo bifurcado).
- **Track MPL:** el MPL YA viene ensamblado de la etapa 2 (borrador
  base convertido + items creados dentro; nombres de variación
  "Sweatshirt"/"T-Shirt") — en esta etapa NO se convierte nada: se
  publica el MPL tal cual, con verificación exhaustiva en Etsy
  (Fase C: variaciones, precios, SKUs, orden de imágenes, videos
  intactos, atributos, políticas, envío).
- **Chequeo previo (2026-10-26):** antes de publicar, verificar
  por API que los componentes del MPL tengan nombres internos
  DISTINTOS (la playera = diseño + " - T-Shirt"). Con nombres
  duplicados Printify bloquea guardar y publicar sin decir la
  causa en el error (solo en el aviso del botón) — detalle y
  arreglo en el skill, §M7. Producción ya lo verifica al
  cerrar (etapa 2); esto es la segunda red, en el punto de uso.
- **Track single:** publicar el draft → sincroniza a Etsy → completar
  (videos, caja de personalización si aplica).
- Subir videos directo en Etsy.
- Verificar título, descripción, tags.
- Registrar IDs en `data/tiendas/<tienda-id>/registro-listings.json` (con `tipo: "mpl"|"single"`).

### 8. Publicidad (Pinterest)
- Skill `puerta-pinterest-pin`: valida pins antes de publicar.
- Crear pins con mockups finales.

## Lo que YA NO se hace
- ❌ Generar mockups propios (flat-lay, doblada, zoom, on-model)
  → Eliminados 2026-10-14 (flujo probado en producción con p002)
- ❌ Traducir colocación nuestra → Printify
  → La colocación se hace directo en Printify
- ❌ Predecir cómo se verá → Se ve directo en Printify

## Tienda activa (declaración de instancia)

Este documento es MECANISMO: nombra `data/tiendas/<tienda-id>/`
en todas sus rutas (des-hardcodeado el 2026-10-27, recalibración
de alineación). La tienda activa de esta instancia es
**29222324 (MyNightShiftShop)**, la única bajo `data/tiendas/`;
`<tienda-id>` se resuelve a ella. Si abre una segunda tienda, la
resolución pasa a ser explícita por flujo (cada agenda y cada
corrida nombra su tienda) y esta declaración se actualiza en la
misma corrida — ninguna ruta vuelve a llevar un id en duro.

## Inventario de agendas de la app (2026-10-27)

Las agendas (crons) viven en el sistema de scheduling del
entorno, fuera de este repo; esta tabla es su inventario
declarado en la app: qué agenda existe, qué skill invoca y su
estado. Una agenda **invoca un skill**; si su cuerpo duplica el
método de un skill, manda el skill y la diferencia se reporta
como hueco (caso B3, auditoría v0.11.0: el consumidor fuera del
repo quedó atrás). Agenda sin skill = hueco declarado, no
estilo.

| Agenda | Invoca | Estado |
|---|---|---|
| `equipo-pod-investigacion-semanal` (lun) | `skills/investigacion-tienda` (desde 2026-10-27; antes era cuerpo con método propio y nicho en duro) | activa |
| `pod-trend-scan` (lun/jue) | Sin skill propio: rastreo de tendencias de producto; su salida alimenta a `investigacion-tienda` y a la estratega vía `investigaciones/` — hueco menor declarado (candidato a skill si crece) | activa |
| `equipo-pod-estratega-semanal` (lun) | `skills/estratega-tienda` | activa |
| `equipo-pod-revision-viernes` (vie) | Ritual de revisión (ledger + Ads + acta en `revisiones/`); sin skill propio — declarado | activa |
| `pod-ritual-lunes-h04` / `pod-ritual-viernes-h12` | Rituales de la instancia (verificación de bancos/ledger); sin skill propio — declarado | activas |
| `equipo-pod-propuestas-diarias` (diario) | `skills/puerta-arte-propuesta` (Fase A) + Fase B de `publicar-printify-etsy` | **pausada por el dueño** |
| `equipo-pod-pinterest-diario` (diario) | `skills/estratega-pinterest` + `skills/puerta-pinterest-pin` | activa |
| `equipo-pod-watchdog` (30 min) | Vigilancia de la operación (cruza registro/checkpoint/decisiones) | activa |

## Ruta de lectura (adoptada 2026-10-19, fase de mejora post-migración v0.12.1)

Qué lee el orquestador (o un chat frío que retoma la app) para
cada tipo de tarea: las **lecturas mínimas gobernantes**, como
punteros puros — esta sección no copia contenido. Es **piso,
nunca techo**: un incidente o una investigación pueden exigir
leer más, y la ruta nunca lo prohíbe. Canon:
`../rameli/skills/fabrica-skills/references/ruta-de-lectura.md`.
Esta sección ES el índice de lo vivo (reemplaza a la antigua
lista "Skills activos", que cubría 4 de los 9 skills): **lo que
no está en la ruta no es flujo vivo, y retirar un flujo = retirar
su ruta en el mismo cambio.**

| Tarea / flujo | Lecturas mínimas gobernantes |
|---|---|
| **Propuestas — etapa 1: arte y aprobación** (F1 Fase A) | Este doc (§Flujo bifurcado, §Etapa 1) · `skills/puerta-arte-propuesta/SKILL.md` · `data/tiendas/<tienda-id>/direccion-tienda.md` (directriz vigente) · `data/tiendas/<tienda-id>/config-propuestas.json` (composición y tipo de lote) · `docs/CONTRATO-TIPO-PRODUCTO.md` · `data/tiendas/<tienda-id>/config.json` (ficha de la tienda) · herramientas de procesamiento declaradas en el skill: `scripts/procesar-arte-propuesta.py` (crudos con fondo blanco) y `scripts/reparar-fondo-casi-blanco.py` (fondos casi-blancos) · `docs/VITRINA-VIVA.md` (contrato de la superficie única de entrega, en vivo) + `scripts/producir-previas-vitrina.py` (previas del lote a su hogar en el repo de datos) |
| **Recogida-aplicación de decisiones de la vitrina** (el dueño avisa «recoge las decisiones de la vitrina de <tienda>») | `skills/puerta-arte-propuesta/SKILL.md` (§«Recogida-aplicación de decisiones (vitrina en vivo)»: procedimiento completo, validaciones e idempotencia) · `docs/VITRINA-VIVA.md` (contrato de decisiones) · `data/tiendas/<tienda-id>/config.json` (bloque `vitrina`: la instancia de ESA tienda) · `data/tiendas/<tienda-id>/vitrina/decisiones.json` (fuente: decisiones del dueño en el repo) · `data/tiendas/<tienda-id>/estado-propuestas.json` (destino) · `data/tiendas/<tienda-id>/registro-listings.json` (validación de slugs) |
| **Producción — etapa 2: borradores de aprobados** (F1 Fase B) | Este doc (§Etapa 2) · `skills/publicar-printify-etsy/SKILL.md` · `docs/CONTRATO-TIPO-PRODUCTO.md` · `data/tiendas/<tienda-id>/registro-listings.json` (qué diseños ya tienen su MPL producido) · `data/tiendas/<tienda-id>/estado-propuestas.json` (los `aprobados` registrados que consume esta fase) |
| **Revisión del dueño y producción** (mockups, videos) | Este doc (§§Etapa 3–5) · `skills/publicar-printify-etsy/SKILL.md` (§M5 algoritmo y manifiesto de mockups · §M6 escenarios y formato técnico de video, única fuente desde v0.11.0) |
| **Paquete comercial del listing** | `skills/paquete-listing-etsy/SKILL.md` · este doc (§Etapa 6) · el porqué guardado en `data/tiendas/<tienda-id>/registro-listings.json` (lo hereda el paquete) |
| **Publicación por lote** (F2) | `skills/publicador-lote/SKILL.md` · `skills/publicar-printify-etsy/SKILL.md` (checklist de publicación) · este doc (§Etapa 7) · `docs/ESTANDAR-ETSY-API-VS-NAVEGADOR.md` |
| **Pinterest diario** (F3) | `skills/estratega-pinterest/SKILL.md` (parrilla) · `skills/puerta-pinterest-pin/SKILL.md` (puerta del pin) · este doc (§Etapa 8) · `data/tiendas/<tienda-id>/config.json` (links rastreables Share & Save) |
| **Dirección semanal** (F4: investigación y estratega) | `skills/investigacion-tienda/SKILL.md` (produce la investigación: ficha → `investigaciones/<fecha>-investigacion.md`, con su puerta `scripts/verificar-investigacion.py`) · `skills/estratega-tienda/SKILL.md` · `docs/CONTRATO-TIPO-PRODUCTO.md` · insumos: la investigación y el trend-scan más recientes en `data/tiendas/<tienda-id>/investigaciones/` y el acta más reciente en `data/tiendas/<tienda-id>/revisiones/` · la ficha `data/tiendas/<tienda-id>/config.json` (líneas vigentes, entrada 11 de la estratega) · `scripts/reporte-seo.py` (cobertura SEO banco × ledger, entrada declarada en el skill de la estratega) · salidas que produce: `data/tiendas/<tienda-id>/direccion-tienda.md` y `data/tiendas/<tienda-id>/config-propuestas.json` (se commitean en la misma corrida, con el consumo de líneas verificado por `scripts/verificar-consumo-lineas-tienda.py`) |
| **Operación comercial** (F7: precios, ledger, ofertas) | `docs/DELIMITACIONES-ADOPCION.md` (§1: dueño y ruta completa del flujo, scripts incluidos) · `docs/ESTANDAR-ETSY-API-VS-NAVEGADOR.md` · `data/tiendas/<tienda-id>/config.json` (precios y calendario de descuentos) |
| **Conectar Etsy API de una tienda** (F6) | `skills/conectar-etsy-api/SKILL.md` · `docs/ESTANDAR-ETSY-API-VS-NAVEGADOR.md` |
| **Onboarding de tienda nueva** (F5) | `skills/onboarding-tienda/SKILL.md` · este doc (§Crear tienda desde cero) · `docs/PATRONES-RESILIENCIA.md` (cómo nacen sus crons) |
| **Trabajos largos con dependencia externa** (cualquier flujo) | `docs/PATRONES-RESILIENCIA.md` (health-check, checkpoints con resume, reintentos acotados) · `docs/REGLA-DELIVERY-CHATS.md` (cómo se entrega el resultado) |
| **Versionado de registros** (cualquier flujo que escriba bajo `data/`) | `ARQUITECTURA-DATOS.md` (mapa de repos D1: qué se commitea en cada repo) · `scripts/registros-datos.py` (el puente: `commit` sincroniza los registros físicos al repo privado `my-pod-datos`, commitea y pushea; `pull` restaura el árbol físico) |
| **Mantenimiento del sistema** (F9: migraciones, fases de mejora, contribuciones) | `rameli.json` (pin vigente) · `../rameli/MIGRACIONES.md` y `../rameli/CHANGELOG.md` (proceso y delta) · `../rameli/docs/CONTRIBUCIONES.md` (si el trabajo sube al framework) · `docs/DELIMITACIONES-ADOPCION.md` (§§2–3: orquestación y capa de juicio) · `docs/EJECUCION-Y-RELEVO.md` (registro y relevo) · `data/tiendas/<tienda-id>/registro-flujo.md` (estado de los flujos de la tienda) |

Cobertura verificada al adoptar (2026-10-19): los **9 skills
vivos** aparecen en al menos una ruta — puerta-arte-propuesta,
publicar-printify-etsy, paquete-listing-etsy, publicador-lote,
estratega-pinterest, puerta-pinterest-pin, estratega-tienda,
conectar-etsy-api, onboarding-tienda — y todo puntero de la
tabla resuelve a un archivo existente. (2026-10-27: el skill
**investigacion-tienda** se suma en la ruta de Dirección
semanal — 10 skills vivos.)


## Crear tienda desde cero (para nuevas tiendas/nichos)

**Propósito:** la app es agnóstica — funciona sin memoria del asistente. Todo lo necesario está en skills, gates y este documento.

### Pasos
1. **Tienda en Printify:** crear shop, conectar a Etsy.
   - Registrar shop ID en `data/tiendas/<shop-id>/config.json`
2. **Nicho:** investigar y elegir nicho (banco de keywords en `data/banco-keywords/<nicho>.md`).
3. **Producto base:** elegir blueprint/provider (ej: Gildan 18000, blueprint 49, provider 99).
   - Registrar en `data/productos/<producto>.json`
4. **Criterios de tienda:** precio estándar, selección de mockups, hero — se definen por tienda en `data/tiendas/<shop-id>/config.json`, no se heredan de otra tienda.
5. **Flujo normal:** desde etapa 1 (Arte) con los criterios de esa tienda.

### Principio
Cada tienda tiene su propia configuración. Los criterios de una tienda no contaminan otra. La app no depende de la memoria del asistente.

## Selección de productos y tipo de lote (2026-10-15)

**Principio:** el producto y el tipo de lote NO están hardcodeados.
La estratega los decide cada semana en `data/tiendas/<tienda-id>/config-propuestas.json`
(contrato: `docs/CONTRATO-TIPO-PRODUCTO.md`).

### Cómo se agrega un producto
1. El cron `pod-trend-scan` (2×/semana) investiga qué prendas están en tendencia en el nicho.
2. Si un producto emerge como tendencia fuerte, se PROPONE al dueño (no se agrega solo).
3. Si el dueño aprueba, se agrega a `productos_aprobados` en `data/tiendas/<id>/config.json` + ficha en `data/productos/<slug>.json`.
4. La estratega puede incluirlo en la composición del MPL o en lotes single (PROPUESTA hasta su dale si cambia la composición).

### Personalización — DECIDIDO 2026-10-15
- Diseño personalizable → track single-product SIEMPRE (el MPL nativo no
  soporta personalización — verificado en help.printify.com).
- Etsy: caja nativa de personalización (gratis, fulfillment manual).
- Automatización sin intervención (Teeinblue/Customily/HelloCustom) y
  flujo Canva (template + API): en investigación, spikes pendientes del
  dale del dueño. Ver `data/tiendas/<tienda-id>/direccion-tienda.md`.
