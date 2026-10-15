# CHANGELOG — publicar-printify-etsy

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
