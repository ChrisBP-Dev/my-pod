# Checklist de Publicación (2026-10-15, v0.6.0 — flujo MPL)

**Regla: ningún listing se declara "publicado" hasta que TODO lo de su
track esté verificado contra el listing vivo. No hay publicación parcial.
No se pregunta al dueño "¿quieres que complete?" — el flujo completo ya
está autorizado. El ojo del dueño es la puerta visual final.**

**Track:** ☐ MPL (diseño NO personalizable) · ☐ SINGLE (personalizable)

---

## Track MPL — Fase A: en Printify (antes de publicar)

### Drafts componentes (uno por producto)
- [ ] Sudadera Gildan 18000 draft: arte colocado, centrado, sin desborde
- [ ] Playera Bella+Canvas 3001 draft: arte colocado, centrado, sin desborde
- [ ] Placement verificado EN CADA producto + revisión del dueño
- [ ] Colores = paleta validada contra el diseño (criterio color-diseño)
- [ ] Playera: White + Athletic Heather + Natural, todas las tallas del proveedor
- [ ] Precios escalonados APLICADOS en cada draft ANTES de publicar:
  - [ ] Sudadera: S–XL $34.99 · 2XL $37.99 · 3XL $39.99
  - [ ] Playera: S–XL $24.99 · 2XL $27.99 · 3XL $30.99
- [ ] Título = título REAL del diseño en cada draft (no genérico del blueprint)
- [ ] Regla: componentes NO publicados single por separado

### Conversión a MPL
- [ ] "Convert to Multi-Product Listing" ejecutado en el producto base
- [ ] "Add item": segundo producto agregado (mismo diseño / existente)
- [ ] Nombres de variación: "Sweatshirt" / "T-Shirt" (campo "Variation name for Etsy listing")
- [ ] Shipping profile único asignado al MPL

### SEO del MPL (re-optimización COMPLETA — regla suya)
- [ ] Título ≤140 car., incluye AMBOS productos
- [ ] Descripción completa con sección "CHOOSE YOUR STYLE" + disclosure IA + políticas
- [ ] 13 tags (≤20 car. c/u) cubriendo ambos productos y el nicho
- [ ] Puerta `verificar-paquete.py` = PASS

### Mockups — esquema de 10 (orden exacto)
- [ ] 1. Sudadera lifestyle hero (= imagen principal del listing)
- [ ] 2. Sudadera lifestyle 2 (pose/modelo DIFERENTE)
- [ ] 3. Sudadera flat-lay
- [ ] 4. Sudadera flat-lay otro color
- [ ] 5. Sudadera folded decorado/ambientado (con fondo)
- [ ] 6. Playera on-model
- [ ] 7. Playera on-model distinto
- [ ] 8. Playera flat-lay
- [ ] 9. Tabla de tallas sudadera
- [ ] 10. Tabla de tallas playera
- [ ] Ninguna pose/modelo repetida en colores diferentes
- [ ] Todos los productos y colores vendidos están representados
- [ ] Conteo "N/20 selected" en Printify = 10 antes de publicar

### Videos
- [ ] Video 1: 3 lifestyles de sudadera (distintos)
- [ ] Video 2: 3 tomas de playera (distintas)
- [ ] 1080×1080, 30fps, H.264, 9.5s, sin audio
- [ ] Puerta `verificar-video.py` = PASS (movimiento ≥3.0) + manifiesto

---

## Track MPL — Fase B: publicar

- [ ] Publicar el MPL en Printify (no los componentes por separado)
- [ ] Estado = "Published" (no "Publishing")
- [ ] Verificar en "My Products" que el MPL aparece publicado

---

## Track MPL — Fase C: en Etsy (verificación exhaustiva, nada se da por sentado)

- [ ] Abrir el listing vivo en Etsy
- [ ] Variaciones: "Sweatshirt"/"T-Shirt" + tallas + colores correctos
- [ ] Precio por variación verificado:
  - [ ] Sudadera S–XL $34.99 · 2XL $37.99 · 3XL $39.99
  - [ ] Playera S–XL $24.99 · 2XL $27.99 · 3XL $30.99
- [ ] SKUs correctos por variación
- [ ] Orden de imágenes = esquema de 10; hero = lifestyle sudadera
- [ ] (Si el orden no se preservó del sync: reordenar en el editor de Etsy)
- [ ] Video 1 y Video 2 presentes y reproducibles (no se borraron en la conversión)
- [ ] Título, descripción completa, 13 tags
- [ ] Materiales, atributos, categoría correctos
- [ ] Production partner = Printify (declarado)
- [ ] Perfil de envío asignado; política de devoluciones
- [ ] Cantidades correctas
- [ ] Caja de personalización AUSENTE (el MPL no la soporta; si aparece = error)
- [ ] Visibilidad de variantes = "Only show in stock variants and hide out of stock"

## Registro
- [ ] IDs de Printify y Etsy en `data/registro-listings.json`, `tipo: "mpl"`, componentes listados
- [ ] Estado = "publicado_completo"

---

## Track SINGLE — checklist (diseños personalizables)

### En Printify (antes de publicar)
- [ ] Draft con arte colocado (centrado, sin desborde), título real
- [ ] Placement revisado por el dueño en Printify
- [ ] Colores/tallas según directriz; precios escalonados aplicados en el draft
- [ ] SEO: título ≤140, descripción con disclosure IA, 13 tags (puerta PASS)
- [ ] Mockups esquema single: 9 (flat ×3 + folded decorado ×3 + 3 lifestyles diferentes, hero = lifestyle)
- [ ] Rotación de héroes vs el lote (no repetir modelo/color del anterior)

### Publicar + Etsy
- [ ] Publicar en Printify → estado "Published"
- [ ] Videos subidos en Etsy (V1 on-model/lifestyle, V2 flat/folded), puerta PASS
- [ ] Título, descripción, 13 tags, categoría, atributos verificados
- [ ] Production partner = Printify; perfil de envío; políticas
- [ ] **Caja de personalización** configurada (nativa de Etsy) si el diseño la lleva
- [ ] Precio final verificado por variación en el listing vivo
- [ ] Registro en `data/registro-listings.json`, `tipo: "single"`, estado "publicado_completo"

---

## Puerta

La publicación NO está completa hasta que un agente verifique CADA item
de esta checklist contra el listing vivo en Etsy. Si algo falta, no es
"publicado con pendientes" — es "no publicado".
