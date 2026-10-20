# Fase de personalización — registro (2026-10-19/20)

**Objetivo:** pulir el flujo de personalización al 100% y escribirlo en el
sistema antes de reactivar el cron de propuestas. **Decisión del dueño
(2026-10-20): piloto AUTOMÁTICO SINGLE** (la ruta automatizada de Printify);
el esquema multi-producto manual queda como excepción consciente.

**Guarda vigente:** nada de esta fase publica listings reales; el cron
`equipo-pod-propuestas-diarias` sigue PAUSADO hasta la palabra del dueño,
post-piloto.

## Qué quedó escrito y dónde (Paso 5)

| Pieza | Dónde vive |
|---|---|
| Ruta automatizada (procedimiento P1–P7) | `skills/publicar-printify-etsy` v0.8.0, §Track Single-P |
| Criterios de arte personalizable | `skills/puerta-arte-propuesta` v0.6.0, sección propia |
| Cupo + tabla del piloto (precios con costos reales) | `data/tiendas/29222324/config-propuestas.json` → `personalizados` (cupo en flujo diario = 0 hasta el veredicto del piloto) |
| Entrega al dueño con SIMULACIÓN (alineación flujo v2, pedido del dueño 2026-10-20) | `skills/puerta-arte-propuesta` v0.6.0 (entrega, variante personalizable) + puntero en `FLUJO-PIPELINE.md` etapa 1 |
| Campo `personalizados` del contrato | `docs/CONTRATO-TIPO-PRODUCTO.md` |
| Sandbox registrado + favorito p056 | `data/tiendas/29222324/registro-listings.json` (`sandbox-personalizacion`, `p056.favorito_dueno`) |

## Verificado en vivo (sandbox, 2026-10-20)

- Campos de texto: el texto del comprador se escala a la caja (nombre
  largo se achica, no desborda). Ejemplo y colocación del dueño
  (Maria / RN - UCI en PROP-PERS-001) inspeccionados visualmente: bien.
- Capa de imagen en producto existente: SÍ (toggle "Personalizable
  image"); en Etsy el campo se ve como file upload requerido (3/5 campos).
- Relleno de imagen = **FIT**: la foto entra entera con su proporción y
  su fondo; sin recorte, sin deformación, sin herramientas de ajuste
  para el comprador.
- Live Preview en Gildan 18000: SÍ. Ventana completa ejecutada con
  precio disuasorio ($199.99) y listing desactivado y verificado
  inactivo al cerrar. Sin cobros nuevos.
- Costos reales de bordado (drafts sonda, sin publicar): sudadera
  Lane Seven 1687 = $30.43 (2XL $32.15 / 3XL $33.88); beanie Yupoong
  1691 = $15.26. Los precios estimados de la propuesta v2 quedaron
  descartados; el piloto usa $59.99 / $32.99.

## Guía v1 (2026-10-18) — clasificada

La guía de la prueba se reconcilió contra los criterios del equipo:
coherencia y campos congelados, nombres contenido+zona, ejemplo
realista Maria / RN - ICU en 3 lugares, límites 15/12, geometría
medida desde píxeles y operación "Review needed" quedaron ABSORBIDOS
en los skills de arriba. Su afirmación de "aprobación automática de
respaldo tras X horas" quedó como **NO verificada** (la doc de
revisión no la muestra) — mandó el sistema. La guía NO es canon.

## Pendientes explícitos

1. **PROP-PERS-001:** corregir límites 1024 → 15/12 **solo por el editor**
   de Printify — la API no expone la configuración de personalización
   (verificado 2026-10-20 por GET). Es draft de prueba, no listing del
   piloto; se corrige si algún día se usa.
2. **Live Preview en Bella+Canvas 3001:** sin prueba en vivo; se verifica
   con el piloto (su draft nunca se publicó).
3. **Aprobación automática de respaldo:** sigue sin confirmar en ajustes
   de tienda; la operación no depende de ella.
4. **Limpieza al cerrar la fase de pruebas:** borrar de Printify el
   producto sandbox y los drafts de prueba (PROP-PERS-001, TEST-BORDADO
   sudadera/beanie). Costo hundido total: $0.20.
5. **Piloto (Paso 6):** 4 listings con diseños NUEVOS y únicos según la
   tabla del config; regla de retiro a 30 días. Recién con su veredicto,
   palabra separada del dueño para reactivar el cron de propuestas con
   cupo de personalizados > 0.

## Cierre (2026-10-20)

Fusionado a `main` con el dale del dueño (fast-forward tras integrar
`origin/main`, que había recibido el barrido counters: la personalización
de puerta-arte se renumeró **v0.6.3** sobre su v0.6.2, sin perder
contenido de ningún lado). Verificación post-fusión en main: lint VERDE,
regresión VERDE, `rameli validar` 0/0. Rama `personalizacion-paso5`
borrada (local + remota) y worktree retirado. Siguiente paso de la fase:
**Paso 6 — piloto**; el cron de propuestas sigue pausado hasta el
veredicto del piloto y la palabra separada del dueño.
