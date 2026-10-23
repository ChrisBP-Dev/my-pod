# Checklist de Publicación (2026-10-15, v0.6.0 — flujo MPL; 2026-10-20 — track single alineado a la ruta automatizada de personalización, §Track Single-P; 2026-10-22 — alineación ruta única MPL, skill v0.9.0)

**Regla: ningún listing se declara "publicado" hasta que TODO lo de su
track esté verificado contra el listing vivo. No hay publicación parcial.
No se pregunta al dueño "¿quieres que complete?" — el flujo completo ya
está autorizado. El ojo del dueño es la puerta visual final.**

**Track:** ☐ MPL (diseño NO personalizable) · ☐ SINGLE (personalizable)

---

## Track MPL — Fase A: en Printify (antes de publicar)

### Borrador BASE (un solo producto — ruta única, 2026-10-22)
- [ ] SOLO el borrador base creado (primer producto de la composición,
  ej. sudadera Gildan 18000): arte colocado según §M1 (min(92% ancho,
  95% alto), centrado horizontal, sesgo arriba 8–12%, sin desborde)
- [ ] Ningún otro componente creado como borrador suelto (la ruta vieja
  de crear todos y ensamblar está descartada; solo rescate anotado)
- [ ] Colores del base = selección de colores del diseño (elegidos por
  contraste con el arte colocado, guía 3–4 por prenda; extensión a
  5–6 permitida si el arte lo justifica, con nota; el resto del
  catálogo desmarcado — sin paleta canónica, ver skill §Selección
  de colores)
- [ ] Puerta de conteo corrida (`scripts/verificar-variantes.py`):
  detiene SOLO si el MPL pasa el límite técnico (>400 variantes o
  >70 opciones); un item con >6 colores = aviso informativo en el
  reporte, sin detener
- [ ] Precios escalonados APLICADOS en el borrador base ANTES de publicar:
  - [ ] Precios según `estrategia_precios` del config de la tienda
    (ej. 29222324: sudadera S–XL $40.99 · 2XL $44.99 · 3XL $46.99;
    playera S–XL $25.99 · 2XL $28.99 · 3XL $32.99)
- [ ] Título = título REAL del diseño en el borrador (no genérico del blueprint)
- [ ] Regla: el base NO se publica single por separado

### Conversión a MPL (en la producción, tras el base)
- [ ] "Convert to Multi-Product Listing" ejecutado en el borrador base
- [ ] "Add item": cada producto restante CREADO dentro del MPL desde el
  catálogo con el mismo diseño (nunca agregado desde un borrador suelto,
  salvo rescate anotado en el registro)
- [ ] Placement, colores/tallas y precios verificados POR ITEM dentro
  del editor del MPL (colores = selección del diseño según la guía
  del skill — 3–4, o 5–6 con nota si el arte lo justifica —, todas
  las tallas que el proveedor ofrezca por color elegido; el dueño
  puede cambiar los colores en su revisión sin límite del sistema)
- [ ] Nombres de variación: "Sweatshirt" / "T-Shirt" (campo "Variation name for Etsy listing")
- [ ] Shipping profile único asignado al MPL
- [ ] Borrador MPL guardado SIN publicar; revisión de UBICACIÓN del dueño
  dentro del editor del MPL (la aprobación creativa ya fue en la vitrina)

### SEO del MPL (re-optimización COMPLETA — regla suya)
- [ ] Título ≤140 car., incluye AMBOS productos
- [ ] Descripción completa con sección "CHOOSE YOUR STYLE" + disclosure IA + políticas
- [ ] 13 tags (≤20 car. c/u) cubriendo ambos productos y el nicho
- [ ] Puerta `verificar-paquete.py` = PASS

### Mockups — esquema vigente (de `data/tiendas/29222324/config.json` → `mpl.esquema_mockups`; si la composición cambia, el esquema cambia ahí)
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
  - [ ] Precios por variación según `estrategia_precios` del config
    de la tienda (ej. 29222324: sudadera $40.99/$44.99/$46.99;
    playera $25.99/$28.99/$32.99)
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
- [ ] IDs de Printify y Etsy en `data/tiendas/<tienda-id>/registro-listings.json`, `tipo: "mpl"`, componentes listados
- [ ] Estado = "publicado_completo"
- [ ] Calendario de descuentos: si `data/tiendas/<id>/config.json → calendario_descuentos` tiene ventanas vigentes que apliquen a este listing, agregarlo (navegador: Marketing → Sales and discounts → editar la oferta/evento → incluir el listing). Nota: las ofertas con 'All listings' incluyen futuros listings automáticamente; los sales events pueden requerir alta manual

---

## Track SINGLE — checklist (diseños personalizables)

### En Printify (antes de publicar)
- [ ] Draft con arte colocado (centrado, sin desborde), título real
- [ ] Placement revisado por el dueño en Printify
- [ ] Colores/tallas según directriz; precios escalonados aplicados en el draft
- [ ] SEO: título ≤140, descripción con disclosure IA, 13 tags (puerta PASS)
- [ ] Mockups esquema single: 9 (flat ×3 + folded decorado ×3 + 3 lifestyles diferentes, hero = lifestyle)
- [ ] Rotación de héroes vs el lote (no repetir modelo/color del anterior)
- [ ] **Personalización (§Track Single-P):** producto y diseño NUEVOS; capas personalizables con nombre contenido+zona, instrucciones con ejemplo [Maria], límites por diseño (nombre 15 / credencial 12 — nunca 1024), ejemplo estándar puesto en la capa, dropdowns en decisiones cerradas; conteo de campos ≤5
- [ ] Inspección visual de las capturas del editor con el ejemplo (puerta-arte v0.6.0)

### Publicar + Etsy
- [ ] Publicar en Printify (personalización marcada en "Details to publish") → estado "Published"
- [ ] Videos subidos en Etsy (V1 on-model/lifestyle, V2 flat/folded), puerta PASS
- [ ] Título, descripción, 13 tags, categoría, atributos verificados
- [ ] Production partner = Printify; perfil de envío; políticas
- [ ] **Campos de personalización verificados en la página pública** = nombres/instrucciones/límites aprobados (llegan de Printify; JAMÁS se editan en Etsy)
- [ ] Primera imagen muestra el ejemplo realista puesto; Live Preview (DTG) probado con nombre corto y largo sin desborde
- [ ] Precio final verificado por variación en el listing vivo (tabla de personalizados, no la estándar)
- [ ] Registro en `data/tiendas/<tienda-id>/registro-listings.json`, `tipo: "single"`, estado "publicado_completo"
- [ ] Calendario de descuentos: si `data/tiendas/<id>/config.json → calendario_descuentos` tiene ventanas vigentes que apliquen a este listing, agregarlo (navegador: Marketing → Sales and discounts → editar la oferta/evento → incluir el listing). Nota: las ofertas con 'All listings' incluyen futuros listings automáticamente; los sales events pueden requerir alta manual

---

## Puerta

La publicación NO está completa hasta que un agente verifique CADA item
de esta checklist contra el listing vivo en Etsy. Si algo falta, no es
"publicado con pendientes" — es "no publicado".
