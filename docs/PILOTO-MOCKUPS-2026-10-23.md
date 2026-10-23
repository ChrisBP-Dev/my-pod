# Piloto seco — colores sin techo + manifiesto de mockups (2026-10-23)

**Qué es:** la prueba en seco (SIN tocar nada en vivo) de la
consolidación v0.11.0 de `publicar-printify-etsy` sobre un MPL
real. No se editó ningún borrador, no se seleccionó ningún
mockup en Printify, no se publicó nada: la única operación
externa fue **lectura** (`printify request` GET) y todo lo
demás corrió en modo fixture sobre esa lectura.

## El MPL usado

**p058 «Quiet ER Christmas Wish»** (registro de la tienda
29222324, Fase B del 2026-10-23, pendiente de revisión del
dueño — es el diseño cuyos colores oscuros eligió el dueño a
mano):

- Sudadera (base): `6adae647f5d2645eb60d70b3` — blueprint 49 / provider 99
- Playera: `6adae80640382312f90a1e1e` — blueprint 12 / provider 99
- MPL draft: `96855940-ccf7-42a1-99a8-4c2979742c06`

## Paso 1 — puerta de conteo nueva sobre los datos reales

`verificar-variantes.py --desde-json <ambos items>` (cuerpos
del GET, contando solo variantes `is_enabled`):

```
Quiet ER Christmas Wish: 3 colores habilitados ['Forest Green', 'Maroon', 'Navy'] · 13 variantes · 8 opciones
Quiet ER Christmas Wish: 3 colores habilitados ['Dark Grey Heather', 'Maroon', 'Navy'] · 13 variantes · 8 opciones
TOTAL conjunto: 26 variantes habilitadas (límite técnico MPL: 400) · 16 opciones (límite técnico MPL: 70)
RESULTADO: OK — dentro de los límites técnicos (los colores no tienen techo)   [exit 0]
```

## Paso 2 — manifiesto generado con el algoritmo nuevo

Entrada (modo fixture): colores reales leídos arriba +
catálogos reales `tomas_preferidas` de ambos productos +
pesos vigentes (principal 5 / secundario 3 / 1 tabla por
producto / total 10). Dos datos de juicio se fijaron como
entrada explícita del piloto (en producción los decide el
worker con el editor abierto): `color_prioritario = Navy` en
ambos items, y el tono de Dark Grey Heather clasificado
«oscuro» (gris heather oscuro frente al arte de letras crema
de p058).

`generar-manifiesto-mockups.py` → 10 espacios, 0 sustituciones:

| Pos | Producto | Rol | Toma | Color |
|---|---|---|---|---|
| 1 | gildan-18000 | principal | lifestyle-2 | Navy |
| 2 | gildan-18000 | secundaria | lifestyle-1 | Forest Green |
| 3 | gildan-18000 | plana | front-flat | Navy |
| 4 | gildan-18000 | plana | front-flat | Maroon |
| 5 | gildan-18000 | doblada-decorada | folded-decorado | Navy |
| 6 | bella-canvas-3001 | principal | modelo-playera-1 | Navy |
| 7 | bella-canvas-3001 | secundaria | modelo-playera-2 | Dark Grey Heather |
| 8 | bella-canvas-3001 | plana | tee-flat | Navy |
| 9 | gildan-18000 | tabla_tallas | tabla-tallas | — |
| 10 | bella-canvas-3001 | tabla_tallas | tabla-tallas | — |

Color sin representación, **declarado** en el manifiesto:
playera **Maroon** — «sin espacios tras garantías mínimas y
cobertura por turnos (espacios_visuales=3)».

## Paso 3 — puerta de cobertura sobre el manifiesto

```
verificar-mockups.py → RESULTADO: PASS — 8 espacios visuales, 2 tablas,
1 colores sin representación declarados; imagen principal correcta   [exit 0]
```

## Lo que se aprendió

1. **Los sets reales de p058 son 3 colores oscuros por prenda**
   (la corrección a mano del dueño): la garantía claro/oscuro
   queda vacua (no hay claros que mostrar) y el algoritmo no
   fuerza ninguno — correcto por diseño.
2. **Tensión real garantía-vs-cobertura en la playera:** con
   3 espacios y 3 colores, las garantías (2 tomas con modelo
   + plana del prioritario) dejan 1 color sin representar y
   el manifiesto lo declara. Si en el piloto EN VIVO se
   prefiere que la plana cubra el tercer color en vez de
   repetir el prioritario, la garantía se ajusta en el
   sistema con esa evidencia — no se decidió en este piloto
   seco porque la propuesta §4 manda garantías primero.
3. **La disponibilidad de cada toma por color en Printify
   NO se puede verificar en modo fixture** (los
   `camera_label` exactos de la mayoría de las tomas del
   catálogo tampoco constan en el historial: solo
   `lifestyle` está verificado). Eso es exactamente lo que
   el piloto de publicación en vivo — cuando el dueño
   termine su revisión de colores de los MPL — debe
   confirmar o corregir en el catálogo, con evidencia, antes
   de dar la mejora por cerrada del todo.
4. **Conteo de opciones:** el universo de opciones del
   blueprint es grande (46 valores en la sudadera, 135 en la
   playera), pero las opciones **en variantes habilitadas**
   son 8 por item; la puerta cuenta solo las habilitadas
   (definición documentada en su docstring). La lectura del
   límite de 70 opciones del MPL conviene confirmarla contra
   la validación del propio Printify en el piloto en vivo.
5. **Colocación (D1):** `data/**` no se versiona en este
   repo desde 2026-10-21: los catálogos de producto y el
   config de tienda de esta consolidación se commitearon en
   el repo de datos `my-pod-datos` (commits del 2026-10-23),
   no en esta rama. Quien busque `tomas_preferidas` en el
   historial de `my-pod` no lo encontrará: vive en el repo
   de datos, como manda `ARQUITECTURA-DATOS.md`.

**Veredicto del piloto seco:** el mecanismo nuevo corre de
punta a punta sobre datos reales (lectura → conteo →
manifiesto → puerta) sin tocar nada en vivo. Pendiente
declarado: el piloto de publicación EN VIVO con los MPL que
el dueño está revisando, que es donde se verifican la
disponibilidad real de tomas por color y los `camera_label`
provisionales del catálogo.

---

## Corrección posterior (2026-10-23, v0.11.1) — la plana ya no desperdicia un espacio

Al explicar este piloto, el dueño preguntó si el criterio había quedado
bien pulido o a qué se refería el «color que quedó fuera». Revisión
honesta: era un **defecto del algoritmo**, no un límite — la garantía
«plana en el color prioritario» corría antes que la cobertura y, en la
playera de 3 espacios, repetía Navy y dejaba fuera a Maroon pudiendo
entrar. **Corregido en la fuente el mismo día** (skill v0.11.1): la
plana garantizada cubre primero el color sin representar. Re-piloto
sobre la misma entrada de p058: **los 6 colores de ambos productos
quedan representados**, 0 declarados sin representación, puerta PASS;
suite de regresión 12 ok / 0 fallas (F12 nueva cubre este caso).

Lo que sigue siendo límite real (físico, no defecto): 10 imágenes por
anuncio, 2 son tablas de tallas → 8 fotos, y cada foto muestra un solo
color de un solo producto. Si una prenda vende más colores que sus
espacios visuales, los colores restantes no tendrán foto propia: se
ordenan por prioridad y los no cubiertos quedan declarados en el
manifiesto.
