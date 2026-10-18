---
name: "puerta-publicacion-pod"
description: "Puerta de publicación POD: valida que un mockup esté listo — dimensiones, DPI del arte y placement del diseño contra la referencia aprobada, todo medido por código."
compatibility: "framework >= 0.4.0"
metadata:
  version: "0.2.2"
  framework_version: "0.9.0"
  regression_suite: "evals/"
---

# Puerta de Publicación POD

**Versión: v0.2.1** · Skill de referencia del framework Rameli: la primera
prueba de que el formato nuevo expresa una puerta real con gates en código.

Ningún mockup se publica si rompe la regresión.

## Cuándo usarme / cuándo NO

**Úsame** antes de publicar cualquier mockup (Etsy, Printify, catálogo):
el mockup candidato se mide contra la referencia aprobada de su estilo y
color. Si una puerta falla, se corrige y se vuelve a medir; no se publica
"porque se ve bien".

**No me uses** para: aprobar el diseño artístico en sí (eso es veredicto
del dueño); mockups de un estilo sin referencia aprobada.

## Procedimiento

1. **Identificar** estilo y color del candidato (flatlay, doblada,
   closecrop, onmodel × white, sand, sportgrey).
2. **Correr** `scripts/verificar-publicacion.py` con `--referencia` =
   el flat-lay aprobado DE ESE DISEÑO (criterio canónico 2026-10-13).
   Sin `--referencia` usa el golden set por estilo/color (solo válido
   para diseños del propio kit vitals-stable).
3. **Leer el veredicto JSON.** `PASS` = publicable. `FAIL` = bloqueado,
   con el criterio violado nombrado.
4. **Puerta Printify** (procedimental, no automatizable): con el mockup
   en verde, colocar el arte en Printify desde el flat-lay aprobado
   (tamaño relativo, alineación, distancia al cuello), comparar el preview
   real de Printify contra el mockup aprobado y revisar DPI ≥ 300 antes de
   guardar. Ver `docs/publicacion/playbook-navegador.md`.
5. **Toda corrección nombra el criterio violado.** Si no lo nombra, no
   existió — y entra a regresión sin ancla.

## Puertas mecánicas (las corre el código)

`scripts/verificar-publicacion.py` emite JSON con una puerta por criterio:

- **dimensiones**: el mockup mide 2000×2000 px (estándar del kit).
- **dpi_arte**: el archivo de arte final rinde ≥ 300 DPI al ancho físico
  declarado (10.5"). Medido, no declarado.
- **placement**: el diseño se localiza en el candidato por SIFT+RANSAC
  contra el arte canónico; su centro debe caer dentro del ±3% de la
  referencia y su ancho dentro del ±5%. La referencia es el flat-lay
  aprobado DE ESE DISEÑO (`--referencia`) — cada diseño replica la
  matemática de su propio flat-lay; ningún número vale en general.
  Comparación determinista, no "se ve bien".

Tolerancias calibradas sobre el golden set y fixtures con desviación
conocida (ver `evals/casos.md`). Un mockup que el código no puede ubicar
con confianza **falla** — no se aprueba a ojo.

## Calibraciones (mecanismo vs aplicación)

- `MECANISMO:` SIFT + RANSAC con semilla fija para localizar el diseño;
  comparación determinista contra referencia — universal.
- `MECANISMO:` el arte se acota a 1600px para SIFT (SIFT_ARTE_MAX) — el
  matching es invariante a escala; sin cota, un arte de 4500px revienta
  memoria (OOM 2026-10-13). La geometría medida no cambia.
- `MECANISMO:` la referencia es el flat-lay aprobado del diseño
  (criterio canónico 2026-10-13) — no un número, no otro diseño.
- `CALIBRACIÓN:` CONF_MIN 0.35, MATCHES_MIN 30, centro ±3%, tamaño ±5% —
  calibrados en el golden set (12 mockups vitals-stable), 2026-10-12/13.
  Revalidar si cambia el tipo de arte (línea fina, monocromo extremo).
- `CALIBRACIÓN (retirada):` gap/ancho-cuello 0.41 como número universal —
  era una medición puntual fosilizada. Sustituida por referencia
  per-diseño en v0.2.0.

## Reglas con motivo

- (2026-10-12, crisis de mockups) Worker QA reportaba números limpios
  sobre mockups visiblemente rotos → las puertas miden, no opinan.
- (2026-10-12, regla suya) La puerta sistemática: colocar desde el primer
  flat-lay aprobado, comparar preview Printify contra el mockup, DPI ≥ 300.
- (2026-10-08, dale suyo) El golden set
  (`vitals-stable-kit/`, 12 mockups) es la referencia aprobada y congelada.
- (2026-10-13, criterio canónico suyo) La discrepancia 0.41 vs 0.25
  quedó disuelta: ningún número vale en general — cada diseño se mide
  contra SU flat-lay aprobado. El error era universalizar una medición
  puntual.

## Referencia

- `references/flat-lay.md` — spec del flat-lay aprobado (fuente geométrica).
- `references/golden-set.md` — los 12 archivos de referencia.
- `evals/` — casos de regresión + fixtures (los rotos deben fallar).
