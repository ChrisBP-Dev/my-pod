# Fixtures — procedencia

- `flatlay-v7-historico.webp`: copia del flat-lay prop2 white v7
  (versión histórica anterior al dale del golden set). 1600 px, no
  2000×2000 → la puerta lo rechaza en `dimensiones`.
- `desplazado-dx120.jpg`: flat-lay aprobado con el diseño movido +120 px
  en X (inpaint del hueco + re-pegado del recorte). Desviación conocida →
  la puerta lo rechaza en `placement` (delta centro).
- `encogido-85.jpg`: flat-lay aprobado con el diseño al 85% de su tamaño,
  centrado en el centro original. Desviación conocida → la puerta lo
  rechaza en `placement` (delta tamaño).

Los sintéticos calibran la sensibilidad de la puerta; no pretenden ser
fotorrealistas. Se regeneran bit-idénticos con `generar-fixtures.py`
(determinista: inpaint TELEA + LANCZOS, sin azar). Si un fixture pasa,
se recalibra la puerta.
