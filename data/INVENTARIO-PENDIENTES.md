# Inventario de propuestas pendientes — verificado 2026-10-14 ~23:10 EDT

Total: **18 propuestas** en espera (p002 publicado hoy, p001 rechazada — no cuentan).

## Listas para oficializar como draft en Printify (arte print verificado)
| ID | Diseño | Estado | Arte print |
|----|--------|--------|------------|
| p004 | Real Night Owl | Arte aprobado + paquete comercial aprobado + video2 aprobado | `data/artes-print/p004-print-300dpi.png` — puerta PASS (436 DPI, RGBA) |
| p005 | Med Pass Marathon | Arte aprobado + paquete comercial aprobado + video2 aprobado | `data/artes-print/p005-print-300dpi.png` — puerta PASS (529 DPI, RGBA) |

## Pendientes con arte NO recuperable (sistema viejo eliminado 2026-10-14)
El arte print vivía en `~/workspace/especialistas-pod/` y `~/workspace/pod-etsy/`,
eliminados por orden del dueño tras confirmar el flujo Printify-first.
Verificado por búsqueda exhaustiva en `~/workspace` y `/tmp`: los archivos no existen.
Solo sobreviven las imágenes presentadas en los chats.

| ID | Diseño | Veredicto del dueño |
|----|--------|---------------------|
| p003 | Caffeine Compassion | Aprobado (chat_produccion). NOTA: su arte ni siquiera era PNG transparente (fallaba puerta RGBA) — requiere regenerar arte de todos modos |
| p006 | Dilaudid the Halls | Arte aprobado 2026-10-12 (chat_produccion abierto) |
| p007 | North Pole Night Shift | Arte aprobado 2026-10-12 |
| p008 | Night Shift Before Christmas | Arte aprobado 2026-10-12 |
| p009 | Nice List Sleepers | Arte aprobado 2026-10-12 |
| p010 | Mrs Claus RN | Arte aprobado 2026-10-12 |
| p011 | Night Shift Elves | Aprueba (2026-10-13) |
| p012 | Twelve Shifts of Christmas | Aprueba — "el más fuerte, primero en cola" (2026-10-13) |
| p013 | Silent Night Unit | Aprueba (2026-10-13) |
| p014 | NPO After Midnight | Aprueba (2026-10-13) |
| p015 | Charting Loud | FIX: fondo gris (2026-10-13) |
| p016 | PRN Peppermint & Nog | Sin veredicto |
| p017 | Night Shift Prayer | Sin veredicto |
| p018 | On Call Christmas | Sin veredicto |
| p019 | Coffee IV Drip | Sin veredicto |
| p020 | Code Gingerbread | Sin veredicto |

## Camino acordado para el lote sin arte
No se oficializa "tal cual" (no hay archivo print con calidad suficiente).
El dueño revisa desde las imágenes del chat (punto de rechazo barato, regla suya),
da veredictos, y por cada aprobado se genera arte fresco con `puerta-arte-propuesta`
(PNG 300 DPI, fondo transparente) → draft en Printify → revisión matutina de ubicación.

## Cron propuestas diarias — listo para mañana
- `equipo-pod-propuestas-diarias`: enabled, última corrida exitosa hoy 07:11 EDT,
  próxima **jue 2026-10-15 07:00 EDT**. Cuerpo migrado a flujo Printify-first
  (genera arte con puerta → crea drafts en Printify por navegador → entrega en
  📌 POD — Equipo y fábrica).
- RIESGO a vigilar: mañana es la primera corrida real del flujo nuevo por cron
  (la de hoy 07:11 aún corrió el flujo viejo). La creación de drafts por navegador
  depende de la sesión de Google en Printify — si se pierde, el dueño la re-inicia.
