> Portado el 2026-10-21 de `docs/operacion/ledger.md` (H11) y
> `docs/operacion/ads.md` (H13) del workspace del goal
> pod-etsy-sistema-operativo-q4-2026 — resolución del hallazgo #5
> del barrido de la migración a Rameli v0.18.0, por decisión del
> dueño (2026-10-21 10:33 EDT, opción A: portar H11/H13 a la app,
> re-apuntar el ritual al registro vivo y unificar la regla de
> matar en 30 días sin tracción, mandando la revisión de viernes).
> **Desde esta fecha la fuente VIVA de estas reglas es este
> documento en la app.** Los archivos del goal quedan como
> historia: no se editan ni se borran, y ya no mandan.

# Reglas de revisión de listings y Ads (H11 + H13) — fuente viva

**Vigente desde:** 2026-10-21 (reglas originales H11/H13:
2026-10-08). **Consumidores:** el ritual
`pod-ritual-viernes-h12` (reglas + Ads + fee bleed) y
`equipo-pod-revision-viernes` (misma forma unificada de las
reglas de listings). **Datos:** el registro vivo de la tienda
— `data/tiendas/29222324/registro-listings.json` (estado por
listing) y `data/tiendas/29222324/ledger-ventas.json` (ventas,
vía API Etsy v3). El antiguo `ledger-registros.md` del goal
(14 filas, congelado el 2026-10-16) ya no es fuente de nada.

Los números se toman de Etsy Stats / la API; nunca se
inventan. Dato no disponible = `n/d` con fecha.

## Alineación aplicada al portar (manda la revisión de viernes)

| Regla original H11 | Forma unificada (única vigente) |
|---|---|
| Kill: >60 días sin venta → desactivar | **Sin tracción en 30 días → matar** (§1, regla 1 — escrita una sola vez, aquí) |
| Observación: 30 días sin favoritos ni ventas → en observación | Ese estado (30 días sin favoritos ni ventas) ES «sin tracción»: cae en la regla de matar. Observación queda para **lo tibio** (§1, regla 2), como enuncia la revisión de viernes |
| Fee bleed: auto-renew OFF en observación o sin ventas en 60 días | Auto-renew OFF en observación o en desactivados por la regla de matar (§1, regla 4) — la ventana de 60 días muere con la regla que la anclaba |
| Escala: ventas + margen verificado (H02) → candidato | Sin cambio de fondo: es «escalar lo que convierte» de la revisión de viernes, con el margen verificado como condición (§1, regla 3) |
| Ads (H13) | Sin solape con la revisión de viernes: se porta tal cual (§2) |

## 1. Reglas de listings (forma unificada)

1. **Matar — sin tracción en 30 días → desactivar.** Tracción
   = ventas o favoritos registrados en el registro vivo
   dentro de la ventana de 30 días. Desactivar conserva
   historial; **borrar solo por decisión explícita del
   dueño**.
2. **En observación — lo tibio:** alguna señal (views o
   favoritos) sin ventas, o señal insuficiente para escalar,
   sin cumplir la regla de matar. Se revisa cada viernes en
   ambos flujos; al entrar en observación, auto-renew OFF.
3. **Escala — lo que convierte:** ventas/conversión con
   margen verificado (puerta de pricing H02) → **candidato
   a escalar**: más variantes del cluster, no más
   presupuesto a ciegas.
4. **Fee bleed:** auto-renew **OFF** en todo listing en
   observación o desactivado. Barrido mensual de
   renovaciones (¿qué se renovó y por qué?); el ritual del
   viernes de fin de mes calcula el fee bleed del mes.

Las decisiones que requieren la palabra del dueño
(desactivar, escalar, activar Ads) se **presentan**, no se
ejecutan — lo enuncian igual los dos flujos de viernes.

**Formato de registro por listing** (campos que las reglas
evalúan; viven en el registro vivo, no en este documento):
`slug` · `id_etsy` · `id_printify` · `fecha_publicacion` ·
`nicho` · `producto` · `precio` · `url` · `views_30d` ·
`favoritos` · `ventas_30d` · `ventas_total` ·
`ad_spend_acumulado` · `auto_renew` · `ultima_revision` ·
`estado` (activo / en observacion / desactivado) ·
`motivo_cambio_estado`. Cada listing se registra el día de
publicación; las métricas se actualizan en la revisión del
viernes, con fecha. El registro no guarda el diseño ni el
SEO (viven en su carpeta y su template) — guarda métricas y
decisiones.

## 2. Ads (H13)

**Estado:** EN ESPERA · **Revisión:** cada viernes dentro
del ritual H12.

### Condiciones de activación (TODAS, medibles en el registro vivo)

| # | Condición | Dónde se mide |
|---|---|---|
| a | Tienda con 15+ días de abierta (Etsy lo exige; mínimo $1/día) | Apertura 2026-10-06 → se cumple el 2026-10-21 |
| b | ≥3 listings con ventas orgánicas (prueba de concepto, sin Ads) | Registro vivo: ventas_total con ad_spend $0 |
| c | Listings con 30+ días publicados | Registro vivo: fecha_publicacion → el listing #1 cumple el 2026-11-05 |
| d | Q4: idealmente corriendo desde early October | Calendario — se cumplirá tarde; al activar, sin expectativa de datos ricos en Q4 |

(Estados al 2026-10-16, del documento origen: las 4
pendientes — 14 listings, 0 ventas. El ritual las re-evalúa
cada viernes contra el registro vivo.)

### Al activar

- **$1–$5/día total**, solo en listings probados (3–5).
  Primeros 30 días = recolección de datos pagada, no profit.
- No tocar la campaña las primeras 2 semanas (dejar que
  Etsy aprenda).

### Reglas de kill de Ads

- **>$30 de gasto con ROAS bajo break-even → OFF.**
  Break-even ROAS ≈ 3.4 (puerta de pricing H02).
- **>50 clics con 0 ventas → pausa.**
- Subir presupuesto solo en listings con conversión **>3%**.

### Cadencia y registro

Revisión semanal dentro del ritual del viernes (H12). El
ad spend se anota por listing en el registro vivo.

### Offsite Ads

Tienda nueva (<$10k/365d) puede hacer opt-out (Shop Manager
→ Settings → Offsite Ads). **Decisión:** opt-out hasta que
los márgenes se prueben; al cruzar $10k el 12% es
obligatorio de por vida. Documentado, no por defecto
silencioso.

### Mito corregido

Los Ads **NO** mejoran el ranking orgánico — solo compran
slots pagos.

### Tráfico orgánico paralelo

Cada producto héroe se publica en Pinterest (títulos
keyword-rich, sin hashtags) y TikTok (proceso/empaque). El
tráfico externo reporta señales de calidad al listing.

### Checklist de activación (el día que se cumplan las 4 condiciones)

1. Verificar las 4 condiciones en el registro vivo (tabla
   de arriba).
2. Elegir 3–5 listings con ventas orgánicas y conversión
   >3%.
3. Crear la campaña en Etsy Ads: presupuesto $1–$5/día
   total, solo esos listings.
4. Anotar fecha de inicio y presupuesto en el registro
   (ad_spend por listing).
5. No tocar 2 semanas. Revisar cada viernes contra las
   reglas de kill.
6. A los 30 días: decidir escalar / mantener / apagar con
   datos.

## 3. Calendario de revisión

- **Semanal (viernes):** ambos flujos aplican §1 y el
  ritual revisa §2.
- **Mensual:** barrido de fee bleed — renovaciones y
  auto-renews.
