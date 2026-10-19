# Fase de mejora post-migración v0.11.0 — PROPUESTA (2026-10-19)

Abierta automáticamente al cerrar la migración a Rameli v0.11.0, como
manda `rameli/MIGRACIONES.md`: la migración cerró con alcance del
delta (merge `3c3c882`, rama borrada, verificación idéntica) y esta
fase inventaría las brechas contra la versión adoptada. **Este
documento es la propuesta: nada de lo siguiente se ejecuta sin el
dale del dueño, y con dale corre como fase propia (rama y puertas
propias), no como apéndice de la migración.** Si se difiere o se
rechaza, queda registrada aquí y reaparece en la siguiente migración.

Inventario verificado en vivo el 2026-10-19 (lint y regresión
corridos antes/después de la migración y otra vez sobre main ya
fusionada: resultados idénticos en las tres corridas comparables).

## P1 — Lint a cero: 17 fallos en 7 skills

Qué cambia, por tipo de fallo:
- **5 descripciones sobre el máximo de 220 caracteres**
  (estratega-pinterest 225, publicar-printify-etsy 313,
  estratega-tienda 335, publicador-lote 358, onboarding-tienda 385):
  reescribirlas quirúrgicas conservando los disparadores de
  invocación.
- **5 skills sin sección "Cuando usarme" y sin "Puertas mecánicas"
  ni "## Procedimiento"** (conectar-etsy-api, estratega-pinterest,
  estratega-tienda, onboarding-tienda, publicador-lote): agregar la
  sección que corresponda a su naturaleza, con contenido real.
- **estratega-pinterest sin CHANGELOG.md**: crearlo.
- **paquete-listing-etsy sin línea de versión** en el cuerpo:
  agregarla.

Impacto: lint 17 → 0; los skills quedan completos para una IA fría
(portabilidad: hoy una IA que solo lee el skill no sabe cuándo
usar 5 de los 10). Riesgo: **bajo** en la parte aditiva (secciones,
CHANGELOG, línea de versión = 11 de los 17 fallos, no toca
comportamiento); **medio-bajo** en las descripciones, porque son la
cara de invocación de cada skill — mitigación: el dueño revisa las
5 descripciones antes de cerrar, y lint + regresión corren después.

## P2 — Regresión de puerta-publicacion-pod: 6 casos G1 en rojo

Qué cambia: primero el **diagnóstico** (no está hecho): los 6 casos
G1 (mockup doblada y en modelo × white/sand/sportgrey) esperan PASS
y dan FAIL desde antes de la migración a v0.9.0 — ya estaban en el
inventario de esa migración y nadie los ha diagnosticado. La fase
determina si es el gate, los fixtures o los assets, y corrige en
esa capa; si el veredicto correcto fuera FAIL, se recalibra la
suite documentando el caso real, nunca se baja la puerta para que
pase.

Impacto: la puerta que protege la publicación queda con su
regresión en verde por la razón correcta. Riesgo: **medio** — es la
puerta principal de publicación; mitigación: calibración contra
casos reales conocidos-buenos/malos antes de tocar nada.

## P3 — Portabilidad del registro de listings (causa YA diagnosticada)

Qué cambia: `data/registro-listings.json` guarda las rutas de los
assets finales como **rutas absolutas del árbol principal**
(`/home/hatch/workspace/my-pod/data/mockups/...`) y
`verificar-pin.py` verifica la membresía por igualdad de string.
La suite construye las rutas desde el árbol donde corre: en
cualquier otro árbol (worktree, clon, otra máquina) 4 casos de
puerta-pinterest-pin fallan con "asset no registrado como FINAL"
(p030 ×2, p032, p034) aunque el registro sea byte-idéntico —
verificado hoy (md5 del registro en main = md5 en HEAD; la
explicación tentativa del registro v0.11.0 queda corregida aquí).
El arreglo candidato: guardar rutas relativas a la raíz de la app
y normalizar al comparar. Toca el registro (todas las rutas), el
gate — **hay dos copias byte-idénticas de `verificar-pin.py`** y
la suite exige que sigan iguales — y todo consumidor que lea
`assets_finales` (grep previo obligatorio).

Impacto: la suite y el gate funcionan en cualquier árbol; la app
deja de depender de vivir en una ruta exacta — es la diferencia
entre "funciona aquí" y "el sistema es portable". Riesgo:
**medio-alto** — el registro lo consultan en producción la puerta
de Pinterest y el flujo de publicación; mitigación: ventana sin
publicación en curso, respaldo del registro, y cierre verificado
con la suite en verde en un worktree Y en el árbol vivo.

## P4 — Adopciones pendientes del modelo de workers (v0.10.0)

Qué cambia (registro completo en `docs/MIGRACION-RAMELI-V0110.md`):
- (a) Decidir si los flujos continuos (propuestas, Pinterest)
  adoptan la plantilla `templates/registro-flujo.md` del framework
  o si checkpoint local + reportes + dirección ya cumplen — un
  "no adoptar" con motivo también cierra este punto.
- (b) Watchdog explícito en `publicador-lote`: su skill no lo
  declara; hoy el cierre de un lote depende de que el orquestador
  vuelva a mirar.
- (c) Umbral de relevo del orquestador: cuándo rota el hub entre
  fases (hoy el principio está adoptado, el umbral no).

Impacto: un chat frío puede reconstruir cualquier flujo continuo
sin depender del hub. Riesgo: **bajo** (operativo/documental); el
costo real es ceremonia, por eso (a) admite no-adopción razonada.

## P5 — Huecos del framework (NO se ejecutan desde esta app)

Reportados en el registro de la migración: el documento
`EJECUCION-POR-WORKERS.md` de Rameli vigente aún se encabeza
"PROPUESTA v2" en una rama ya borrada, y `bin/rameli` está
versionado sin bit de ejecución (100644). Su arreglo va por
contribución al framework según `rameli/docs/CONTRIBUCIONES.md`,
con su propio dale — esta fase solo lo deja inventariado.

## Orden sugerido

1. **P1 aditivo** (secciones, CHANGELOG, línea de versión):
   11 fallos menos, riesgo casi cero, sin tocar comportamiento.
2. **P3 portabilidad del registro**: diagnóstico ya cerrado y
   desbloquea verificar todo lo demás fuera del árbol principal.
3. **P2 diagnóstico G1** de puerta-publicacion-pod.
4. **P1 descripciones** (las 5 restantes), con revisión del dueño.
5. **P4 adopciones** de workers pendientes.
6. **P5** contribución al framework, en su carril.

Cada punto, si se aprueba, corre con rama propia y puertas
antes/después; el avance y los veredictos se anotan en este
documento.
