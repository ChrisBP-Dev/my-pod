# Criterio Video Listings Etsy (2026-10-14, corregido)

## Origen
NO inventado. Copiado del script que generó el video del último listing
aprobado (`sleighin-12-hour-shift-video1-v4.mp4`, 9.4s).
Script origen: `especialistas-pod/files/disenos/propuestas-2026-10-11/p003/scratch-build-videos.py`

## Formato técnico
- **Resolución:** 1080×1080 (1:1 cuadrado)
- **FPS:** 30
- **Codec:** H.264 (libx264), pix_fmt yuv420p, preset medium
- **Duración:** 9.5s (3 clips de 3.5s con fades de 0.5s solapados)
- **Audio:** ninguno (Etsy lo elimina al subir)
- **Tamaño:** ~1-3 MB (límite Etsy 100 MB)

## Movimiento
- **Zoom IN:** 1.0 → 1.25 (perceptible, no imperceptible)
- **Posición absoluta por frame:** `z='1+0.25*on/105'` — NUNCA `zoom+step`
  acumulativo (causa temblor por truncamiento a píxeles enteros).
  Ver `LECCION-ZOOMPAN-SIN-TEMBLOR.md`.
- **Suavidad:** se escala a 2160×2160 primero, luego zoompan baja a 1080.
- **Centrado:** x='iw/2-(iw/zoom/2)', y='ih/2-(ih/zoom/2)'

## Transición
- **xfade fade 0.5s** entre clips (NO corte directo)
- Offsets: 3.0s y 6.0s

## Estructura Video 1 — On-model
- **Contenido:** 3 fotos on-model aprobadas
- **Orden:** hero (giro) primero, luego las otras 2 variantes

## Estructura Video 2 — Mockups
- **Contenido:** 3 mockups (flat-lay, doblada, zoom) del color hero
- **Orden:** flat-lay → doblada → zoom

## Implementación
Script: `scripts/generar-video-listing.py` (réplica del script origen)
