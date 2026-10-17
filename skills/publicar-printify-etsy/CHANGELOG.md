# CHANGELOG — publicar-printify-etsy

## v0.7.1 (2026-10-16)
- **Propuestas como MPL drafts (orden del dueño, causa raíz 2026-10-16):** M2 calibrado — las propuestas diarias llegan ensambladas como MPL draft (un draft por diseño); la revisión del dueño verifica placement por item dentro del editor del MPL. El cron de propuestas ahora incluye el ensamblaje (M1+M4 antes de la revisión).
## v0.7.0 (2026-10-16)
- **Estándar API de Etsy vs navegador** (punto del dueño): sección nueva que apunta al canon `docs/ESTANDAR-ETSY-API-VS-NAVEGADOR.md` (API-first; navegador solo para ofertas/cupones, stats de visitas, mensajes).
- **Tablas de precios**: ya no hardcodeadas; se leen de `estrategia_precios` del config de tienda (ejemplo 29222324 actualizado a doctrina precio con colchón).
- Paso de checklist: listings nuevos se agregan a eventos de ofertas vigentes (`eventos_ofertas` del config).

## v0.6.1 (2026-10-15)
- **Organización a nivel tienda** (punto del dueño): el esquema de
  mockups (`mpl.esquema_mockups`) y de videos (`mpl.esquema_videos`) se
  movió a `data/tiendas/29222324/config.json`. El skill lee el esquema
  vigente; si la estratega define otra composición, define su esquema
  en el config sin reescribir el skill. Nueva sección "Calibraciones
  (mecanismo vs instancia vs tienda)".

## v0.6.0 (2026-10-15)
- **Flujo MPL nativo** (decisión del dueño): track MPL para diseños NO
  personalizables — composición estándar Gildan 18000 + Bella+Canvas 3001
  (Printify Choice), conversión "Convert to Multi-Product Listing" en
  Printify, nombres de variación "Sweatshirt"/"T-Shirt".
- **Flujo bifurcado por personalización** (orden del dueño): diseño
  personalizable → track single-product SIEMPRE (el MPL nativo no soporta
  personalización, verificado en help.printify.com). Cambiar de track
  exige re-optimización SEO completa + mockups/videos nuevos.
- **Esquema de mockups MPL: 10 imágenes** (APROBADO por el dueño):
  2 lifestyles sudadera + 2 flat sudadera + 1 folded decorado + 2 on-model
  playera + 1 flat playera + 2 tablas de tallas. Reglas: nunca repetir
  pose/modelo, todos los colores vendidos representados, hero = lifestyle.
- **Esquema de videos MPL:** Video 1 = 3 lifestyles sudadera, Video 2 =
  3 tomas playera (1080×1080, 9.5s, sin audio).
- **SEO MPL:** título con ambos productos, descripción con sección
  "CHOOSE YOUR STYLE", 13 tags ≤20 car.
- **Precios playera:** S–XL $24.99, 2XL $27.99, 3XL $30.99 (fórmula ×1.15).
- **Placement en CADA producto del MPL** + revisión del dueño (lección
  p005: el placement heredado no pasó puerta numérica).
- **Criterio color-diseño** (regla suya): colores validados contra el
  diseño, sin abarcar sin verificación visual.
- **Regla:** componentes de un MPL no se publican single por separado.
- **Fase C:** verificación exhaustiva en Etsy tras publicar el MPL
  (variaciones, precios, SKUs, orden de imágenes, videos intactos,
  materiales, atributos, políticas, envío, personalización ausente,
  cantidades, visibilidad de variantes).
- Notas MPL verificadas 2026-10-15: título/desc/tags/mockups se gestionan
  en el MPL (pricing en cada single), un shipping profile compartido,
  límites 20 productos/400 variantes/70 opciones, push selectivo por
  categorías, revert a single disponible.

## v0.5.0 (2026-10-15)
- **Estándar de precios escalonados por talla** (orden del dueño): el precio
  nunca es plano; recargo = redondeo((costo_talla − costo_SXL) × 1.15).
  Calibración Gildan 18000: S–XL $34.99, 2XL $37.99 (+$3), 3XL $39.99 (+$5).
  Aplica en Printify antes de publicar y se verifica por variación en Etsy.
  El precio base S–XL lo define la directriz de la estratega
  (`data/direccion-tienda.md`).
- Checklist: "Precio final verificado" ahora exige cada variación con su
  precio correcto en el listing vivo.

## v0.4.0 (2026-10-14)
- **Endurecimiento:** checklist completa de publicación (CHECKLIST-PUBLICACION.md).
  Ningún listing se declara publicado hasta verificar título, descripción,
  13 tags, hero correcto, videos en Etsy, categoría, atributos, production
  partner, envío y políticas. Lección: p002 se publicó incompleto (sin tags,
  sin videos, hero incorrecto) por no tener esta validación.
- Puerta `verificar-listos-publicar.py` actualizada a Printify-first
  (ya no busca mockups propios eliminados; exige 2 videos Printify-first).

## v0.3.0 (2026-10-14)
- **Probado en producción:** p002 publicado exitosamente con este flujo.
- Selección estándar de mockups documentada: Flat + Folded 2 decorado + Lifestyle 1/2/3 (1 por color, sin repetir modelo). Hero = lifestyle (preferencia 2/3, luego 1 o Folded decorado).
- El color del hero depende del diseño (no siempre blanco).
- Eliminados remanentes del flujo anterior (scripts de mockups propios, bases, flatlays, zooms generados).

## v0.2.0 (2026-10-14)
- **Cambio mayor:** flujo Printify-first. Ya no se generan mockups propios
  ni se traduce colocación. El draft se crea en Printify, el dueño revisa
  ahí, los mockups salen de Printify.
- Procedimiento simplificado de 7 a 8 pasos (agrega Pinterest).
- La puerta de colocación ahora es revisión del dueño en Printify,
  no comparación contra mockups propios.

## v0.1.0 (2026-10-14)
- Versión inicial: flujo con mockups propios y validación de colocación
  por comparación. Reemplazado por v0.2.0.
