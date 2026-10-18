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
  la estratega puede definir otra en `data/config-propuestas.json`).
- Detalle operativo: `skills/publicar-printify-etsy/SKILL.md`.
- Contrato estratega → propuestas → publicación:
  `docs/CONTRATO-TIPO-PRODUCTO.md`.

## Etapas

### 1. Arte
- Generar arte en alta calidad: PNG sin fondo, 300 DPI, recortado exacto.
- Puerta: `puerta-arte-propuesta` (fondo transparente, DPI, márgenes).
- Dale del dueño al arte.

### 2. Propuesta (drafts en Printify)
- **Track MPL:** un draft por producto de la composición (default:
  sudadera + playera), cada uno con el arte colocado. Los drafts quedan
  "unpublished" = propuesta pendiente. Los componentes NUNCA se publican
  por separado.
- **Track single:** un draft del producto indicado.
- El tipo de lote (mpl/single/mixto) lo define la estratega en
  `data/config-propuestas.json` (dinámico por semana).
- Posición inicial: centrada, 78% ancho, ~14% desde arriba (ajustable).
- Detección de drafts: agrupar por diseño (título real); no duplicar
  diseños que ya tienen sus componentes pendientes (ver contrato §E).

### 3. Revisión del dueño
- **Piloto flujo nocturno (desde lun 2026-10-19, decisión del dueño
  2026-10-18, piloto de 1 semana):** las propuestas se generan a las
  18:00 y el dueño entra a Printify EN LA NOCHE, antes de dormir,
  revisa los drafts. La producción posterior (mockups → videos →
  paquete → publicación) corre de noche tras sus dales; Pinterest
  corre a las 08:50 de la mañana siguiente sobre lo ya publicado y el
  watchdog a las 07:50. Si una noche no puede revisar, el lote espera
  y lo aprueba cuando pueda — el flujo no se rompe.
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
- Registrar IDs en `data/registro-listings.json` (con `tipo: "mpl"|"single"`).

### 8. Publicidad (Pinterest)
- Skill `puerta-pinterest-pin`: valida pins antes de publicar.
- Crear pins con mockups finales.

## Lo que YA NO se hace
- ❌ Generar mockups propios (flat-lay, doblada, zoom, on-model)
  → Eliminados 2026-10-14 (flujo probado en producción con p002)
- ❌ Traducir colocación nuestra → Printify
  → La colocación se hace directo en Printify
- ❌ Predecir cómo se verá → Se ve directo en Printify

## Skills activos
- `puerta-arte-propuesta` — valida el arte
- `paquete-listing-etsy` — genera paquete comercial
- `publicar-printify-etsy` — flujo de publicación
- `puerta-pinterest-pin` — valida pins
- `puerta-publicacion-pod` — (legacy, solo para mockups propios archivados)


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
La estratega los decide cada semana en `data/config-propuestas.json`
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
  dale del dueño. Ver `data/direccion-tienda.md`.
