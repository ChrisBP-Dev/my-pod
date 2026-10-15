name: "publicar-printify-etsy"
description: "Publica un diseño aprobado en Printify y Etsy siguiendo el flujo Printify-first: el draft se crea en Printify, el dueño revisa la colocación ahí, los mockups salen de Printify, y se publica."
compatibility: "framework >= 0.4.0"
metadata:
  version: "0.4.0"
  framework_version: "0.8.0"
  regression_suite: "evals/"
---

# Publicar en Printify + Etsy (Printify-First)

**Versión 0.2.0** — Actualizado al flujo Printify-first (2026-10-14).
Printify es la fuente de verdad; no generamos mockups propios.

## Cuándo usarme / cuándo NO

**Úsame** cuando el diseño tiene: arte aprobado (300 DPI, sin fondo),
paquete de listing aprobado (dale del dueño).

**No me uses** si: falta el dale del dueño en el arte o el paquete.

## Procedimiento (Printify-First)

### 0. Inicio de sesión (protocolo Google-first, 2026-10-15)
Antes de pedirle al dueño que inicie sesión manualmente:
1. Ir a printify.com → "Log in" → "Continue with Google".
2. La sesión de Google YA está guardada en el navegador: en el selector de
   cuentas elegir la de la tienda (tudale.pod / Tú Dale POD).
3. Esto inicia sesión en Printify sin intervención del dueño.
Solo si Google no ofrece cuenta guardada o el login falla, se le pide a él
que lo haga manual en el navegador. Mismo protocolo vale para Etsy.

### 1. Crear propuesta (draft en Printify)
- Subir el arte a Printify (navegador, el CLI está roto).
- Crear producto draft: Gildan 18000, provider Printify Choice.
- Colocación inicial: centrada, 78% ancho, ~14% desde arriba.
- El draft queda "unpublished" = propuesta pendiente de revisión.

### 2. Revisión del dueño (en Printify)
- El dueño revisa el draft en Printify cada mañana.
- Corrige la ubicación directamente en el editor si hace falta.
- Elimina los rechazados. Avisa cuáles están listos.
- **La colocación se valida en Printify, no contra nuestros mockups.**

### 3. Generar mockups (en Printify)
- En el draft aprobado, generar todos los mockups del catálogo × colores.
- Descargar los mockups para usar en videos y Pinterest.
- El dueño los revisa en Printify.

### 4. Generar videos
- Con los mockups descargados de Printify:
  `scripts/generar-video-listing.py`
- Criterio: `CRITERIO-VIDEO.md`.
- Puerta: `scripts/verificar-video.py` (incluye manifiesto).

### 5. Publicar producto
- En Printify: publicar el draft (ya con colocación aprobada).
- Se sincroniza a Etsy automáticamente (canal conectado).

### 6. Completar en Etsy
- Subir los videos (no van por Printify).
- Verificar título, descripción, 13 tags del paquete.
- Publicar el listing.

### 7. Registrar
- Guardar IDs de Printify y Etsy en `data/registro-listings.json`.

### 8. Publicidad (Pinterest)
- Skill `puerta-pinterest-pin`: valida pins.
- Crear pins con los mockups de Printify.

## Puertas mecánicas

- **verificar-paquete.py**: el paquete comercial es válido.
- **verificar-video.py**: los videos cumplen el criterio.
- **Revisión en Printify**: el dueño valida colocación y mockups
  directamente donde se ve el resultado real.

## Calibraciones (mecanismo vs instancia)

- **MECANISMO**: el flujo es igual para cualquier producto y diseño.
  Printify-first siempre.
- **CALIBRACIÓN** (Gildan 18000): posición inicial 78% ancho, 14% desde
  arriba. El dueño ajusta por diseño en el editor.
