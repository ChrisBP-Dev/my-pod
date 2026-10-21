name: "paquete-listing-etsy"
description: "Genera el paquete completo de listing para Etsy: título SEO, descripción estructurada, 13 tags y copy de anuncio, siguiendo la metodología validada en listings publicados."
compatibility: "framework >= 0.4.0"
metadata:
  version: "0.2.0"
  framework_version: "0.17.0"
  regression_suite: "evals/"
---

# Paquete de Listing Etsy

**Versión: v0.2.0**

Genera el paquete comercial completo para publicar un diseño en Etsy:
título, descripción, 13 tags y copy de anuncio.

## Cuándo usarme / cuándo NO

**Úsame** cuando el diseño tiene todos sus mockups aprobados y el dueño dio
el dale para preparar la publicación. Necesito: descripción del diseño,
nicho, colores y tallas.

**No me uses** para: diseñar el arte (eso es otro flujo); mockups
(no están listos = no hay paquete).

## Metodología (de listings publicados)

### Título
- **Fórmula:** `[keyword] [material/trait] | [occasion/recipient]`
- **Límite:** 140 caracteres (Etsy), objetivo 100-130
- **Keyword principal** en los primeros ~40 caracteres
- **6-14 palabras**, ninguna palabra más de 2x
- **Sin adjetivos subjetivos** (hermoso, increíble, perfecto)
- Fuente de keywords: `data/banco-keywords/<nicho>.md`

### Descripción
Estructura fija (precedente listings #1, #2, #3):
1. **Hook** (1-2 líneas, emoji, tono del diseño)
2. **Disclosure IA** (obligatorio): "Designed with the assistance of generative AI imagery; composition, typography, and final artwork directed, edited, and finalized by the seller."
3. **Bloque ⚠️ PLEASE READ** (made-to-order, no returns por cambio de opinión, reemplazo por daño)
4. **Párrafo descriptivo** (el diseño, para quién es)
5. **✨ DETAILS** (producto, material, print, fit, colores, tallas)
6. **📏 FIT & CARE** (talla, lavado)
7. **🎁 MADE TO ORDER** (tiempo de producción)
8. **Cierre** (gracias por apoyar la tienda)

### 13 tags
- **Máximo 20 caracteres** por tag (verificado por código)
- **2-3 palabras** por tag
- **Sin repetir** keywords del título (complementan, no duplican)
- **Ángulos:** descriptivo, ocasión, destinatario, producto, lugar
- Ninguna palabra líder en más de 5 tags

### Copy de anuncio
- 3-4 líneas para Etsy Ads / redes
- Hook + producto + colores + CTA

## Procedimiento

1. **Leer** `data/banco-keywords/<nicho>.md` para keywords y fórmula.
2. **Recibir** del dueño o del registro: descripción del diseño, colores, tallas, precio.
   **REGLA DE COHERENCIA (2026-10-14, lección cara):** antes de generar, ABRIR el
   arte print aprobado y verificar que el concepto/hook/descripción hablen del
   diseño REAL (sujeto, temporada, elementos). Los conceptos heredados del sistema
   viejo pueden estar desactualizados respecto al arte final (caso real: p005
   figuraba "ICU Halloween" cuando el arte ya era un carrito navideño; p004
   describía "enfermera" cuando el arte era un búho). La puerta mecánica NO detecta
   esto (solo valida formato) — la coherencia se verifica contra el arte, siempre.
3. **Generar** el paquete con `scripts/generar-paquete.py`.
4. **Validar** con `scripts/verificar-paquete.py` (puerta mecánica).
5. **Presentar** al dueño para aprobación. Sin su dale, no se publica.

## Puertas mecánicas

`scripts/verificar-paquete.py` valida:
- **título**: ≤140 caracteres, keyword al inicio, sin palabra >2x
- **tags**: exactamente 13, cada uno ≤20 caracteres, sin duplicados
- **descripción**: contiene disclosure IA, bloque made-to-order, secciones DETAILS/FIT
- **completitud**: todos los campos presentes

## Calibraciones (mecanismo vs aplicación)

- **MECANISMO** (universal): estructura de descripción, fórmula de título,
  reglas de tags. Vienen de principios SEO públicos de Etsy.
- **CALIBRACIÓN** (aplicación: nicho enfermería, 2026-10-08): banco de keywords
  específico, frases semilla long-tail. Ver `data/banco-keywords/enfermeria.md`.

## Actualización continua (proactividad)

El banco de keywords NO es estático. La investigación pasada se vuelve
obsoleta — los trends cambian, nuevos términos emergen, otros mueren.

**Ciclo de refresh (cada 90 días o cuando un listing del nicho despegue/muera):**
1. Revisar autosuggest de Etsy para las frases semilla (observar, no scrapear agresivo).
2. Revisar performance de listings activos del nicho (qué tags/títulos convierten).
3. Actualizar `data/banco-keywords/<nicho>.md` con fecha de revisión.
4. Si cambian keywords principales, regenerar paquetes afectados (con dale del dueño).

**Disparadores de revisión anticipada:**
- Un listing del nicho despega (analizar qué keywords funcionaron)
- Un listing muere (analizar qué falló)
- Cambio de temporada (ej: Navidad → San Valentín → graduación)
- Etsy anuncia cambios en SEO/búsqueda

Este ciclo es responsabilidad del sistema, no del dueño. El dueño solo
aprueba los cambios resultantes.
