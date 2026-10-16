# Banco de keywords — Pinterest · Enfermería

**Nicho:** enfermería · **Creado:** 2026-10-16 · **Revisión:** cada 90 días
o cuando un listing del nicho despegue.
**Distinto al banco de Etsy** (`enfermeria.md`): Pinterest es un buscador
de descubrimiento y planificación, no de transacción. El lenguaje aquí es
el de quien busca IDEAS ("nurse gift ideas"), no el de quien ya decidió
comprar ("funny nurse crewneck sweatshirt").

**Fuentes/método:** autocomplete de la barra de búsqueda de Pinterest
(la mejor fuente gratuita: es el lenguaje propio de Pinterest),
guided-search tiles (las tarjetas de colores bajo la barra = el mapa de
keywords relacionadas que Pinterest regala), Pinterest Trends
(trends.pinterest.com, vista Shopping Trends para intención de compra),
y la regla de intención futura: la usuaria de Pinterest planifica con
~2 meses de anticipación (en octubre se pinean keywords de Navidad).

## Frases semilla (descubrimiento)

1. nurse gift ideas
2. christmas gifts for nurses
3. funny nurse shirts
4. night shift nurse gifts
5. nurse appreciation gifts
6. gifts for nursing students
7. rn graduation gift ideas
8. nurse christmas shirt
9. night shift nurse essentials
10. cute nurse sweatshirt

## Fórmula de título (pin)

`[keyword Pinterest] + [ángulo ocasión/destinatario]` — directo, sin
adjetivos subjetivos, sin hashtags.

**Ejemplo 1:** `Nurse Gift Ideas: Funny Night Shift Nurse Sweatshirt for Christmas`
**Ejemplo 2:** `Christmas Gifts for Nurses | Cute RN Crewneck for Night Shift`

## Descripción (2-3 frases naturales, keywords integradas)

`Funny nurse shirts make the best christmas gifts for nurses. This cozy
night shift nurse sweatshirt is perfect for RN graduation gift ideas or
nurse appreciation gifts.`

## Tableros por intención (crear si no existen)

- `Christmas Nurse Gifts` — intención: regalo navideño
- `Funny Nurse Shirts` — intención: estilo/humor
- `Night Shift Nurse Life` — intención: identidad de turno nocturno
- `Nurse Graduation Gifts` — intención: graduación (estacional: may/jun, dic)

## Notas operativas

- Los tableros llevan keywords en el TÍTULO (no "Cute Stuff"): es
  posicionamiento, igual que el pin.
- Ventana estacional: activar keywords de Navidad desde octubre
  (planificación de ~2 meses); en diciembre la intención ya migró a
  Año Nuevo — no pineas Navidad en diciembre, pineas lo siguiente.
- Este banco alimenta `keywords_fuente` de los pin.json; la puerta
  `scripts/verificar-pin.py` exige ≥1 frase multi-palabra de aquí en
  título+descripción.
