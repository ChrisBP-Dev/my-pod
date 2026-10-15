# Casos de regresión — puerta-publicacion-pod

Cada fallo real entra aquí como prueba permanente: la puerta debe
rechazarlo para siempre.

## Deben PASAR (golden set)

| # | Candidato | Puerta |
|---|-----------|--------|
| G1 | los 12 del golden set (`references/golden-set.md`) | `mockup --estilo <e> --color <c>` → PASS |
| G2 | `vitals-stable-print-300dpi.png` (arte final, 3168 px) | `arte --ancho-pulgadas 10.5` → PASS (301.7 DPI) |

## Deben FALLAR (criterio violado nombrado)

| # | Fixture | Desviación conocida | Debe violar |
|---|---------|---------------------|-------------|
| F1 | `fixtures/flatlay-v7-historico.webp` (copia) | versión histórica superada, 1600 px (no 2000×2000) | dimensiones |
| F2 | `fixtures/desplazado-dx120.jpg` | diseño movido +120 px en X (inpaint + re-pegado) | placement (delta centro) |
| F3 | `fixtures/encogido-85.jpg` | diseño al 85% del tamaño aprobado | placement (delta tamaño) |

**Procedencia:** F1 es archivo histórico real (versión anterior al dale).
F2 y F3 son sintéticos con desviación conocida, generados del flat-lay
aprobado para calibrar la sensibilidad de la puerta (ver
`fixtures/README.md`). Si un fixture pasa, la puerta perdió sensibilidad:
se recalibra la puerta, no se relaja el caso.
