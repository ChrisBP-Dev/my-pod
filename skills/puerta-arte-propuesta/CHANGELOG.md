# Changelog — puerta-arte-propuesta
Skill de app. Pineado a Rameli v0.8.0.
## v0.1.0 — 2026-10-13
- Creado desde la plantilla.

## v0.1.1 (2026-10-13)
- G2 dividido en `fondo_limpio` (esquinas alfa=0) y `recorte_ajustado`
  (margen ≤32px): el criterio del dueño es recorte exacto al arte, sin
  bordes vacíos — el gate anterior pedía margen mínimo, al revés.
- Nuevo `--autotrim`: recorta al bbox + 4px y re-verifica (verifier-repair).
- Suite 4/4: P1 + F1/F2/F3 (fondo, dpi, recorte).
