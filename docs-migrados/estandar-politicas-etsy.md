> Portado de `docs/estandar-politicas-etsy.md` (workspace del goal pod-etsy-sistema-operativo-q4-2026) el 2026-10-11 — hallazgo #2 dictamen del Auditor 2026-10-11. Si el origen cambia, re-portar.

# Estándar de políticas Etsy — fuente canónica
**Ref:** 2026-10-08 · Investigación verificada en Etsy Help (reporte:
`~/workspace/research_notes/etsy-pod-shop-policies-2026-20261008-2341/report.md`).
**Alcance:** toda tienda Etsy del sistema POD y todo listing que se publique.
**Idioma de los textos:** inglés (la tienda vende en EE. UU.).
**Regla de mantenimiento:** estos textos viven AQUÍ. Si Etsy o Printify cambian
algo, se actualiza este archivo y se re-publica a la tienda; nunca se editan
copias sueltas en listings individuales.

---

## 1. Principio de dos carriles (no negociable)

1. **Firmes con cambio de opinión** — cada pieza se imprime bajo pedido y no se
   puede revender. No se aceptan devoluciones ni cambios por talla/color
   equivocados por el comprador ("no me quedó", "no me encantó").
2. **Generosos y rápidos con errores nuestros** — artículo equivocado, mal
   impreso o dañado: reemplazo gratis o reembolso completo a elección del
   comprador, con foto como prueba, sin devolver nada.

**Por qué:** Etsy PERMITE el "no acepto devoluciones" (fuera de la UE), pero su
Purchase Protection puede reembolsar al comprador igual por daño/error/no
llegada y descontarlo de la cuenta. El carril 2 no es generosidad: Etsy lo
impone de todos modos. Escribirlo nosotros primero convierte una imposición en
señal de confianza.

## 2. Configuración estructurada (Shop Manager → Settings → Policy settings)

| Pestaña | Valor |
|---|---|
| Returns & exchanges | **No acepto devoluciones / No acepto cambios** — se aplica a CADA listing físico (obligatorio por listing; sin política el listing puede perder visibilidad en búsquedas) |
| Cancellations | **ON**, ventana más corta disponible (ej. "within 1 hour of purchase") + texto libre: `before your order enters production.` |
| Privacy | Plantilla de Etsy |
| Fixed | No editable (Etsy la maneja) |

## 3. Textos listos (EN) — copiar/pegar, no reescribir por listing

### 3a. Bloque corto de descripción (OBLIGATORIO en toda descripción, justo después del hook)

```
⚠️ PLEASE READ — made to order: this sweatshirt is printed just for you after you order, so we can't accept change-of-mind returns or size exchanges. Please check the size chart (photo 2) and message us with any questions before buying. If your item arrives damaged, misprinted, or wrong, we'll replace it free or refund you in full — just send a photo within 7 days. Full details in our Shop Policies & FAQ below.
```

**Por qué corto:** el texto completo en cada descripción se desactualiza (drift) y
entierra el contenido de venta. Etsy mismo recomienda el resumen en la
descripción + reglas completas en políticas/FAQ.

### 3b. FAQ — Returns ("Can I return or exchange my sweatshirt?")

```
Every sweatshirt is printed to order just for you — it's made when you buy it, so it can't be restocked or resold. Because of this, we can't accept change-of-mind returns (wrong size ordered by mistake, color preference, or simply changing your mind).

If we made a mistake, we make it right — fast. Wrong item, misprint, or damage? Send us a photo of the issue within 7 days of delivery and we'll send a free replacement or a full refund — your choice, no need to ship anything back.

📏 Avoiding size issues: please check the size chart (in the listing photos) and measure a sweatshirt you already love before ordering. We're happy to help you pick a size — just message us first!
```

### 3c. FAQ — Exchanges (incluido en la misma entrada o como "Do you offer size exchanges?")

```
We don't offer size exchanges (each piece is printed to order, so a new size means printing a brand-new sweatshirt). Ordered the wrong size? Message us within 7 days of delivery — we'll send you a one-time 30% discount code toward a replacement in the right size. If we sent the wrong size or a defective print, that's on us: free replacement or full refund, no return needed.
```

### 3d. FAQ — Cancellations ("Can I cancel or change my order?")

```
You can cancel within 1 hour of purchase — but please message us immediately. Your sweatshirt goes to our print partner within hours of ordering, and once printing has started we can't cancel or change the order (size, color, design, or address). If production hasn't begun, we'll cancel and refund you in full right away.
```

### 3e. FAQ — Shipping ("How long will my order take?")

```
Two clocks, so you know exactly what to expect.
🖨️ Production time: 2–7 business days. Your sweatshirt is printed to order by our US print partner after you check out. During the holiday rush, production can take up to 10 business days — order early!
📦 Transit time: 3–7 business days after it ships, with tracking.
Total estimated delivery: about 5–14 business days from order date. You'll get a tracking number as soon as your order ships. Shipping carriers (not us) control transit — we can't guarantee carrier dates, but if your order is running very late, message us and we'll trace it with you.
```

**Criterio de números (decisión 2026-10-08, delegada a Jarvis):**
- La API de Printify declara `handling_time` = 10 días para Gildan 18000 vía
  Printify Choice (proveedor 99 — el producto vivo usa Printify Choice, NO
  SwiftPOD como decían los docs del kit).
- La guía oficial de Printify dice: producción típica **2–7 business days**;
  si un pedido no sale en 7 días, se escala a soporte (o sea, 7 es su propio
  umbral de servicio). El 10 de la API es el techo contractual, no el caso típico.
- Decisión: prometer el rango típico documentado (2–7) + disclose honesto del
  pico navideño (hasta 10). Prometer el techo (10) de plano hunde conversión y
  ningún vendedor POD serio lo hace; prometer 2–5 mentiría contra los datos del
  proveedor. El perfil de envío de Etsy ("processing time") debe cubrir 7 días
  hábiles — es la promesa que Etsy fiscaliza (Star Seller, casos).
- **Los números se VERIFICAN contra Printify por producto/proveedor antes de
  publicar — nunca se inventan ni se copian de otro producto.** Si el proveedor
  o el producto cambian, este criterio se re-ejecuta.

### 3f. FAQ — Print colors ("Will the print colors match what I see on my screen?")

```
We use direct-to-garment (DTG) printing for a soft, durable print. Colors can look slightly different on different screens — the photos show the design accurately, but expect small variations. The print may feel slightly stiff on first wear and softens after the first wash.
```

### 3g. FAQ — Care ("How should I wash my sweatshirt?")

```
Machine wash cold, inside-out, with like colors. Tumble dry low or hang dry. Do not bleach or iron directly on the print.
```

### 3h. FAQ — Origin ("Where is my order printed and shipped from?")

```
Designed by us in Naples, Florida; printed and shipped by our US production partner Printify.
```

### 3i. Messages to Buyers (página de recibo + email de compra)

```
Thanks for your order! A quick reminder: your sweatshirt is printed to order just for you, so we can't accept change-of-mind returns — please double-check your size against the size chart (photo 2 of your listing) while your order is in production. If anything arrives damaged, misprinted, or wrong, send us a photo and we'll make it right.
```

## 4. Plantilla de descripción — orden de secciones (estándar)

1. **Hook** (2–3 líneas, keywords al frente)
2. **⚠️ Bloque de política** (§3a) — siempre aquí, nunca al final
3. Detalles de la prenda (blank, tela, fit)
4. Guía de tallas + tabla de medidas (texto + foto)
5. Notas de color
6. Cuidado
7. Producción y envío (ventanas verificadas)
8. Nota de regalo (opcional)
9. About de la tienda (1–2 líneas)

## 5. Socio de producción (declaración obligatoria, no opcional)

- Shop Manager → Settings → Partners you work with → agregar **Printify**
  (ubicación = la que Printify declara en su propia página; título público
  "Apparel printer"; nombre visible a compradores: ON).
- Adjuntar a **cada listing** (Listing details → Production partners).
- Actualizar **delivery locations** a la ubicación del socio.
- **No declararlo = riesgo de remoción de listings / suspensión de la tienda.**

## 6. Regla anti-incompleto (puerta del sistema)

**Ninguna tienda se considera ABIERTA** hasta completar el checklist de 15 ítems
(ver §7): políticas en los 4 tabs, socio de producción declarado, icon/banner,
About, anuncio, 4 destacados, secciones, FAQ, Messages to Buyers, perfiles de
envío con ventanas reales, materiales/origen, 10 fotos por listing con tabla de
tallas.

**Ningún listing se PUBLICA** sin el trío verificado:
1. ✅ Política de devolución/cambio adjunta al listing
2. ✅ Socio de producción adjunto al listing
3. ✅ Bloque ⚠️ de política en la descripción (después del hook)

Si un listing ya está vivo sin el trío, se audita y se corrige antes de seguir
publicando (retrofit, misma regla que el checklist de cumplimiento).

## 7. Checklist de completitud de tienda (15 ítems)

1. Returns & exchanges: política en CADA listing físico
2. Cancellations: shop-wide, ON, ventana corta + "before production"
3. Privacy: plantilla de Etsy
4. Production partner declarado + adjunto a cada listing + delivery locations
5. Icono 500×500 + banner 1200×300 (o 1200×400) con marca
6. About completo (historia + proceso + mención del socio)
7. Shop announcement (qué vendemos + tiempos actuales)
8. 4 featured listings
9. Shop sections (≤20, nombres con keywords)
10. FAQ (las 6 entradas del §3)
11. Messages to Buyers (§3i)
12. Shipping profiles: processing time = ventana real de producción; orígenes correctos
13. Materiales y origen en los atributos del listing
14. Social links (solo si están activos)
15. Fotos del listing: mockups + slide de tabla de tallas + slide de política

## 8. Lo que NO se puede verificar sin entrar a Etsy/Printify

- Valores exactos de los dropdowns de Policy settings (detrás del login).
- Ventanas de producción actuales de Printify por blueprint/proveedor
  (verificar en el catálogo de Printify antes de cada publicación).
- Alcance UE/Reino Unido (si se vende ahí: 14 días de desistimiento mínimo).
