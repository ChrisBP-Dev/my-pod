# Estrategia de Reviews — MyNightShiftShop

**Fecha:** 2026-10-16 · **Estado:** INVESTIGACIÓN — hallazgos para
decisión del dueño. Sin tácticas activadas hasta su dale.
**Contexto:** 0 reviews = freno #1 de conversión. El dueño pidió
investigar primero (programas de Etsy, fechas límite, opciones éticas)
y ver hallazgos antes de cualquier propuesta.

Fuentes: help.etsy.com y etsy.com/legal (verificadas 2026-10-16).
Cada hallazgo indica su nivel de verificación.

---

## 1. Targeted Offers — cupones automáticos nativos [VERIFICADO oficial]

Gratis. 3 tipos automáticos por email (solo a compradores que optaron
por recibir promos):
- **Thank You coupon** — después de la compra (recompra). Expira 1 año.
- **Abandoned Cart coupon** — carrito abandonado >24h. Expira 60 días.
- **Favorited Item coupon** — favorito sin compra (~48h). Expira 60 días.

Config: Shop Manager → Marketing → Sales and discounts → "Automatically
send offers to interested shoppers". Single-use, un cupón de cada tipo
por comprador a la vez; se apaga cuando se quiera.

**Límite clave:** NO pueden dirigirse a "quienes dejen review" ni
condicionarse a una review — eso es extorsión (§3). Efecto en reviews:
indirecto (más pedidos = más oportunidades).

## 2. Solicitud de reviews [VERIFICADO]

- Etsy envía emails automáticos pidiendo review tras la compra.
- Ventana: abre en la fecha estimada de entrega; el comprador tiene
  **100 días** para dejarla. Solo quien compró; 1 review por orden.
- **No se encontró** botón/herramienta nativa del vendedor para pedir
  reviews desde Shop Manager [no verificado que exista].
- El vendedor puede responder públicamente a las reviews.

## 3. Prohibiciones explícitas [VERIFICADO oficial]

- **Extorsión:** ofrecer bienes/servicios/compensación "a cambio de
  una review positiva" = extorsión (reviews removidas, acción vs tienda).
- **Prohibido:** descuento/cupón/regalo condicionado a review (aunque
  no se pidan estrellas — el condicionamiento es el problema); comprar
  reviews; pedir a familiares/amigos que compren para dejar reviews
  (riesgo de remoción); spam por Etsy Messages.
- **Permitido:** pedir review sin incentivo; tarjeta de agradecimiento
  neutra; Thank You coupon NO condicionado; responder reviews.

## 4. Cyber Specials 2026 [VERIFICADO oficial]

- Evento: **23 nov – 1 dic 2026**. Opt-in **antes del 27-oct-2026**,
  **mínimo 25% off** en los listings participantes. Gratis participar;
  Etsy puede incluir la tienda en su marketing del evento.
- Ya existe el cron `cyber-specials-decision-2026-10-26` (avisa el 26-oct).
- **Margen con −25% (aritmética verificada contra
  analisis-rentabilidad-2026-10-15):**
  - Playera $24.99 → $18.74: costos $15.28 + fees ~$2.03 = **+$1.43**
    (fino pero positivo).
  - Sudadera $34.99 → $26.24: costos $25.86 + fees ~$2.74 = **−$2.36
    PÉRDIDA por unidad**.
  - Conclusión: a precios actuales, el evento solo es viable en
    playeras (o eligiendo qué listings participan).

## 5. Star Seller [VERIFICADO oficial]

Requisitos (revisión día 1 de cada mes, ventana rolling 3 meses):
1. Responder 95%+ de primeros mensajes en 24h (auto-replies cuentan).
2. 95%+ pedidos a tiempo con tracking.
3. Rating **4.8+ estrellas**. 4. Elegible desde **90 días de la primera
   venta** + mínimo **5 pedidos y $300** en 3 meses.
El badge no mueve el ranking de búsqueda; sí es señal de confianza.
Hoy no calificable (faltan ventas/antigüedad). Cada review temprana
pesa mucho en el 4.8.

## 6. Tarjeta en el paquete [PARCIAL]

Printify **no tiene** vía nativa para inserts/tarjetas (solo branding
sets: logo en etiqueta de envío, neck labels). El proveedor empaca
estándar. **Bloqueado por el proveedor, no por Etsy.** Etsy no prohíbe
la tarjeta neutra de agradecimiento (sin condicionar, sin redirigir
fuera de Etsy).

## 7. Follow-up post-entrega por mensaje [VERIFICADO-terceros]

Un mensaje sobrio tras la entrega (plantilla guardada): agradecer,
ofrecer ayuda, pedir review honesta **sin incentivo**. $0. Es la
palanca #1 disponible hoy. Límite: 1 mensaje por pedido, sin insistir.

## 8. Cupones financiados por Etsy [VERIFICADO que existen]

Etsy financia cupones a compradores (ej. 15% hasta $20); el vendedor
cobra completo. El targeting lo decide Etsy. $0 para el vendedor.
Efecto: más ventas → más oportunidades de review. Sin control.

---

## Opciones para decisión del dueño

| # | Opción | Costo | Efecto en reviews | Fecha límite |
|---|--------|-------|-------------------|--------------|
| A | Thank You coupon automático | $0 + % descuento a definir | Indirecto (recompra) | — |
| B | Favorited/Abandoned coupons | $0 + % descuento a definir | Indirecto (conversión) | — |
| C | Follow-up post-entrega pidiendo review | $0 | **Directo** | Desde el 1er pedido |
| D | Cyber Specials (−25%, opt-in) | Margen (solo viable en playeras) | Indirecto (volumen) | **27-oct-2026** |
| E | Meta Star Seller | $0 | Las reviews alimentan el 4.8 | ~90 días post 1ª venta |
| F | Tarjeta de agradecimiento en paquete | $0 | Directo potencial | Bloqueada por Printify |
| G | Cupón/regalo A CAMBIO de review | — | — | **PROHIBIDO** |
| H | Reviews de familiares/amigos | — | — | Riesgo de remoción |

## Decisiones pendientes del dueño

1. **Cupones A/B:** ¿activar? ¿qué % de descuento? (propuesta operativa:
   Thank You 10% recompra; Favorited/Abandoned 10-15% conversión —
   el % lo define él).
2. **Follow-up C:** ¿dale para mensajear a cada comprador tras la
   entrega? Plantilla propuesta (requiere su aprobación antes de usarse):
   > "¡Gracias por tu compra! Esperamos que te encante. Si algo no está
   > perfecto, escríbenos y lo resolvemos. Y si te gustó, una review
   > honesta nos ayuda muchísimo. — Tú Dale POD"
3. **Cyber Specials D:** ¿opt-in? Solo playeras (margen verificado), o
   no participar. El cron avisa el 26-oct.
4. **Star Seller E:** objetivo declarado a 3 meses (sin acción hoy salvo
   configurar auto-reply para proteger la métrica de respuesta).

## Reglas permanentes

- Nada condicionado a review. Nunca. (Extorsión = riesgo de tienda.)
- El follow-up es servicio post-venta, no spam: 1 mensaje, sobrio,
  sin incentivo.
- Las reviews alimentan el ledger (`data/ledger-ventas.json` vía el
  endpoint de reviews de la API — M2) para que la estratega las use.
