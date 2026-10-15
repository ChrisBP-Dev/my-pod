# Flujo Pipeline POD — Printify-First (2026-10-14)

**Estado: APROBADO por el dueño 2026-10-14. Reemplaza el flujo anterior.**

## Principio
Printify es la fuente de verdad para cómo se ve el producto.
No predecimos con mockups propios; usamos los de Printify directamente.

## Etapas

### 1. Arte
- Generar arte en alta calidad: PNG sin fondo, 300 DPI, recortado exacto.
- Puerta: `puerta-arte-propuesta` (fondo transparente, DPI, márgenes).
- Dale del dueño al arte.

### 2. Propuesta (draft en Printify)
- Crear producto draft en Printify con el arte colocado.
- Posición inicial: centrada, 78% ancho, ~14% desde arriba (ajustable).
- El draft queda como "unpublished" = propuesta pendiente.

### 3. Revisión matutina (dueño)
- El dueño entra a Printify cada mañana, revisa los drafts.
- Corrige ubicación directamente en el editor si hace falta.
- Elimina los rechazados. Los que quedan = aprobados para continuar.
- Avisa cuáles están listos.

### 4. Mockups (desde Printify)
**Selección estándar (criterio del dueño 2026-10-14):**
- Flat (default, 1 por color) — básico pero se acepta
- Folded decorado/ambientado (Folded 2, 1 por color) — NO el blanco plano
- Lifestyle 1, 2, 3 (1 por color, diferentes modelos/poses — nunca repetir la misma chica)
- **Hero:** casi siempre un lifestyle. El color depende del diseño (White, Sand o Sport Grey). Orden: Lifestyle 2 o 3 primero, última opción Lifestyle 1 o Folded decorado. En propuestas: Jarvis elige una y el dueño valida.
- Descargar los mockups seleccionados.
- Puerta: el dueño los revisa en Printify.

### 5. Videos
- Descargar mockups de Printify.
- Generar videos con `scripts/generar-video-listing.py`:
  - Video 1: on-model (si hay) o mockups lifestyle
  - Video 2: flat-lay → doblada → zoom/detalle
- Criterio: `CRITERIO-VIDEO.md` (1080×1080, 9.5s, zoom sin temblor, fade 0.5s).
- Puerta: `scripts/verificar-video.py`.

### 6. Paquete de listing
- Skill `paquete-listing-etsy`: título, descripción, 13 tags, copy.
- Puerta: `verificar-paquete.py`.
- Dale del dueño (confía en puerta para SEO).

### 7. Publicación
- Skill `publicar-printify-etsy`.
- Publicar producto en Printify → sincroniza a Etsy.
- Subir videos directo en Etsy.
- Verificar título, descripción, tags.
- Registrar IDs en `data/registro-listings.json`.

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

## Selección de productos (2026-10-14)

**Principio:** el producto NO está hardcodeado. Cada tienda tiene una lista de `productos_aprobados` en su config.

### Cómo se agrega un producto
1. El cron `pod-trend-scan` (2×/semana) investiga qué prendas están en tendencia en el nicho.
2. Si un producto emerge como tendencia fuerte, se PROPONE al dueño (no se agrega solo).
3. Si el dueño aprueba, se agrega a `productos_aprobados` en `data/tiendas/<id>/config.json`.
4. Las propuestas diarias (7am) generan drafts usando los productos aprobados (rota entre ellos para no quemar uno solo).

### Personalización (pendiente)
- Estado: pendiente de investigación.
- Objetivo: determinar si se puede automatizar personalización via Etsy/Printify/herramientas propias.
- No se implementa hasta tener investigación completa.
