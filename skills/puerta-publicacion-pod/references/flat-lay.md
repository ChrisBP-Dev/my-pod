# Flat-lay aprobado — fuente geométrica

El primer flat-lay aprobado es la fuente de la geometría de publicación.
Todo lo demás (otros estilos, Printify) deriva de él; nada se inventa.

- **Archivo:** `flatlay-prop2-white-v1-2000.jpg` (golden set, dale 2026-10-08)
- **Medición determinista** (`scripts/verificar-publicacion.py`, arte
  canónico `vitals-stable-final.png`, SIFT + RANSAC semilla fija):
  - bbox ≈ (714, 570), ancho ≈ 526 px, centro ≈ (977, 837)
  - misma geometría medida en white, sand y sportgrey (invariante al color)
- **Regla de producción** (2026-10-12): en Printify se coloca desde este
  flat-lay — tamaño relativo, alineación, distancia al cuello — y se
  compara el preview real contra este archivo.

## Discrepancia abierta (no tocar sin su veredicto)

El doc `criterio-tamano-real-vitals-stable.md` atribuye al flat-lay
gap/ancho-cuello ≈0.41 y ancho de diseño 431 px (1.486 × cuello), pero la
medición sobre el asset aprobado da ≈0.25 y ≈526 px. La puerta calibra
contra **el asset**, no contra el número del documento, hasta que él
decida (pendiente desde 2026-10-11).
