# Flujo Pipeline POD — Printify-First + MPL (2026-10-15)

**Estado: actualizado 2026-10-15 con las decisiones del dueño (flujo MPL
nativo + flujo bifurcado por personalización). Reemplaza el flujo single
del 2026-10-14 como default.**

## Principio
Printify es la fuente de verdad para cómo se ve el producto.
No predecimos con mockups propios; usamos los de Printify directamente.

## Flujo bifurcado (orden del dueño 2026-10-15)
- **Diseño personalizable** (nombre/texto del comprador) → **track single**
  (el MPL nativo NO soporta personalización). Producto individual.
- **Diseño NO personalizable** → **track MPL**: sudadera Gildan 18000 +
  playera Bella+Canvas 3001 en un solo listing (composición default;
  la estratega puede definir otra en `data/tiendas/29222324/config-propuestas.json`).
- Detalle operativo: `skills/publicar-printify-etsy/SKILL.md`.
- Contrato estratega → propuestas → publicación:
  `docs/CONTRATO-TIPO-PRODUCTO.md`.

## Etapas

### 1. Arte + aprobación del dueño (Fase A — flujo v2, 2026-10-19)
- Generar arte en alta calidad: PNG sin fondo, 300 DPI, recortado exacto.
- Puerta mecánica COMPLETA: `puerta-arte-propuesta` v0.5.0+ (composición
  sobre el crudo, limpieza, autotrim seguro, fidelidad contra el crudo).
- **Entrega para aprobación:** cada arte que pasa la puerta se entrega
  en un chat nuevo con su **porqué** (tema y ángulo de la directriz,
  frase, iconografía y su motivo, y qué mirar al revisar — p. ej. los
  counters, que la puerta declara pendientes del ojo humano). El
  porqué se guarda en el registro (`porque` por diseño) y lo hereda
  el paquete comercial.
- **Puerta del dueño, por diseño, en el chat:** aprueba, rechaza o
  pide ajuste ANTES de que se produzca nada. Lo aprobado se enlista
  (la cola persiste entre días; no caduca). Lo rechazado no consume
  producción. Lo ajustado vuelve solo a esta etapa.
- **Superficie alternativa de la misma puerta — Vitrina de revisión
  (piloto 2026-10-22):** la entrega puede presentarse en la vitrina
  (plantilla en `docs/VITRINA-REVISION.md`): el dueño decide ahí, las
  marca listas y avisa en un chat; Jarvis las recoge y las vuelca a
  este mismo checkpoint. La puerta no cambia — cambian el canal y el
  registro; la aprobación válida es la decisión guardada en la
  vitrina y recogida en el checkpoint.
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

### 2. Propuesta (drafts en Printify) — Fase B: solo aprobados
- **Track MPL:** un draft por producto de la composición (default:
  sudadera + playera), cada uno con el arte colocado. Los drafts quedan
  "unpublished" = propuesta pendiente. Los componentes NUNCA se publican
  por separado.
- **Track single:** un draft del producto indicado.
- **Track single personalizable:** un draft del producto indicado con
  los campos de personalización montados en Printify (ruta
  automatizada, `publicar-printify-etsy` §Track Single-P). El diseño
  es siempre nuevo y único; nunca se convierte un diseño del MPL.
- El tipo de lote (mpl/single/mixto) lo define la estratega en
  `data/tiendas/29222324/config-propuestas.json` (dinámico por semana).
- Posición inicial: centrada, 78% ancho, ~14% desde arriba (ajustable).
- Detección de drafts: agrupar por diseño (título real); no duplicar
  diseños que ya tienen sus componentes pendientes (ver contrato §E).

### 3. Revisión del dueño (ubicación, en Printify)
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

### 4. Mockups (desde Printify)
**Esquema MPL — 10 imágenes (APROBADO por el dueño 2026-10-15):**
1. Sudadera lifestyle hero (principal) · 2. Sudadera lifestyle 2 (distinto)
3. Sudadera flat-lay · 4. Sudadera flat-lay otro color
5. Sudadera folded decorado/ambientado · 6. Playera on-model
7. Playera on-model distinto · 8. Playera flat-lay
9. Tabla de tallas sudadera · 10. Tabla de tallas playera.
Reglas: nunca repetir pose/modelo en colores diferentes; todos los
productos/colores vendidos representados; hero = lifestyle.
**Track single:** esquema de 9 (flat ×3 + folded decorado ×3 + 3
lifestyles diferentes, hero = lifestyle).
- Rotación de héroes entre productos (modelo y color no se repiten en
  consecutivos).
- Descargar los mockups seleccionados.
- Puerta: el dueño los revisa en Printify.
- ⚠️ 2026-10-15 (lección): en Printify, **mockups SELECCIONADOS ≠ vistas
  descargables**. Solo los mockups con checkbox marcado se sincronizan a Etsy.
  Para 10 imágenes en Etsy hay que marcar las 10 vistas en el producto ANTES de
  publicar (o republicar solo-mockups después). Verificar el conteo "N/20
  selected" en el producto.

### 5. Videos
- Descargar mockups de Printify.
- Generar videos con `scripts/generar-video-listing.py`:
  - **Track MPL:** Video 1 = 3 lifestyles de sudadera (distintos);
    Video 2 = 3 tomas de playera (distintas).
  - **Track single:** Video 1 = on-model/lifestyle; Video 2 = flat/folded.
- Criterio: `CRITERIO-VIDEO.md` (1080×1080, 9.5s, zoom sin temblor, fade 0.5s).
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
- **Track MPL:** convertir a MPL en Printify ("Convert to Multi-Product
  Listing"), nombres de variación "Sweatshirt"/"T-Shirt", publicar el MPL,
  verificación exhaustiva en Etsy (Fase C: variaciones, precios, SKUs,
  orden de imágenes, videos intactos, atributos, políticas, envío).
- **Track single:** publicar el draft → sincroniza a Etsy → completar
  (videos, caja de personalización si aplica).
- Subir videos directo en Etsy.
- Verificar título, descripción, tags.
- Registrar IDs en `data/tiendas/29222324/registro-listings.json` (con `tipo: "mpl"|"single"`).

### 8. Publicidad (Pinterest)
- Skill `puerta-pinterest-pin`: valida pins antes de publicar.
- Crear pins con mockups finales.

## Lo que YA NO se hace
- ❌ Generar mockups propios (flat-lay, doblada, zoom, on-model)
  → Eliminados 2026-10-14 (flujo probado en producción con p002)
- ❌ Traducir colocación nuestra → Printify
  → La colocación se hace directo en Printify
- ❌ Predecir cómo se verá → Se ve directo en Printify

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
| **Propuestas — etapa 1: arte y aprobación** (F1 Fase A) | Este doc (§Flujo bifurcado, §Etapa 1) · `skills/puerta-arte-propuesta/SKILL.md` · `data/tiendas/29222324/direccion-tienda.md` (directriz vigente) · `data/tiendas/29222324/config-propuestas.json` (composición y tipo de lote) · `docs/CONTRATO-TIPO-PRODUCTO.md` · `data/tiendas/29222324/config.json` (ficha de la tienda) · herramientas de procesamiento declaradas en el skill: `scripts/procesar-arte-propuesta.py` (crudos con fondo blanco) y `scripts/reparar-fondo-casi-blanco.py` (fondos casi-blancos) |
| **Propuestas — etapa 2: drafts de aprobados** (F1 Fase B) | Este doc (§Etapa 2) · `skills/publicar-printify-etsy/SKILL.md` · `docs/CONTRATO-TIPO-PRODUCTO.md` · `data/tiendas/29222324/registro-listings.json` (qué diseños ya tienen componentes) |
| **Revisión del dueño y producción** (mockups, videos) | Este doc (§§Etapa 3–5) · `skills/publicar-printify-etsy/SKILL.md` · `CRITERIO-VIDEO.md` (criterio y puerta de video) |
| **Paquete comercial del listing** | `skills/paquete-listing-etsy/SKILL.md` · este doc (§Etapa 6) · el porqué guardado en `data/tiendas/29222324/registro-listings.json` (lo hereda el paquete) |
| **Publicación por lote** (F2) | `skills/publicador-lote/SKILL.md` · `skills/publicar-printify-etsy/SKILL.md` (checklist de publicación) · este doc (§Etapa 7) · `docs/ESTANDAR-ETSY-API-VS-NAVEGADOR.md` |
| **Pinterest diario** (F3) | `skills/estratega-pinterest/SKILL.md` (parrilla) · `skills/puerta-pinterest-pin/SKILL.md` (puerta del pin) · este doc (§Etapa 8) · `data/tiendas/29222324/config.json` (links rastreables Share & Save) |
| **Dirección semanal** (F4: estratega e investigación) | `skills/estratega-tienda/SKILL.md` · `docs/CONTRATO-TIPO-PRODUCTO.md` · insumos: la investigación y el trend-scan más recientes en `data/tiendas/29222324/investigaciones/` y el acta más reciente en `data/tiendas/29222324/revisiones/` · `scripts/reporte-seo.py` (cobertura SEO banco × ledger, entrada declarada en el skill de la estratega) · salidas que produce: `data/tiendas/29222324/direccion-tienda.md` y `data/tiendas/29222324/config-propuestas.json` (se commitean en la misma corrida) |
| **Operación comercial** (F7: precios, ledger, ofertas) | `docs/DELIMITACIONES-ADOPCION.md` (§1: dueño y ruta completa del flujo, scripts incluidos) · `docs/ESTANDAR-ETSY-API-VS-NAVEGADOR.md` · `data/tiendas/29222324/config.json` (precios y calendario de descuentos) |
| **Conectar Etsy API de una tienda** (F6) | `skills/conectar-etsy-api/SKILL.md` · `docs/ESTANDAR-ETSY-API-VS-NAVEGADOR.md` |
| **Onboarding de tienda nueva** (F5) | `skills/onboarding-tienda/SKILL.md` · este doc (§Crear tienda desde cero) · `docs/PATRONES-RESILIENCIA.md` (cómo nacen sus crons) |
| **Trabajos largos con dependencia externa** (cualquier flujo) | `docs/PATRONES-RESILIENCIA.md` (health-check, checkpoints con resume, reintentos acotados) · `docs/REGLA-DELIVERY-CHATS.md` (cómo se entrega el resultado) |
| **Versionado de registros** (cualquier flujo que escriba bajo `data/`) | `ARQUITECTURA-DATOS.md` (mapa de repos D1: qué se commitea en cada repo) · `scripts/registros-datos.py` (el puente: `commit` sincroniza los registros físicos al repo privado `my-pod-datos`, commitea y pushea; `pull` restaura el árbol físico) |
| **Mantenimiento del sistema** (F9: migraciones, fases de mejora, contribuciones) | `rameli.json` (pin vigente) · `../rameli/MIGRACIONES.md` y `../rameli/CHANGELOG.md` (proceso y delta) · `../rameli/docs/CONTRIBUCIONES.md` (si el trabajo sube al framework) · `docs/DELIMITACIONES-ADOPCION.md` (§§2–3: orquestación y capa de juicio) · `docs/EJECUCION-Y-RELEVO.md` (registro y relevo) · `data/tiendas/29222324/registro-flujo.md` (estado de los flujos de la tienda) |

Cobertura verificada al adoptar (2026-10-19): los **9 skills
vivos** aparecen en al menos una ruta — puerta-arte-propuesta,
publicar-printify-etsy, paquete-listing-etsy, publicador-lote,
estratega-pinterest, puerta-pinterest-pin, estratega-tienda,
conectar-etsy-api, onboarding-tienda — y todo puntero de la
tabla resuelve a un archivo existente.


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
La estratega los decide cada semana en `data/tiendas/29222324/config-propuestas.json`
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
  dale del dueño. Ver `data/tiendas/29222324/direccion-tienda.md`.
