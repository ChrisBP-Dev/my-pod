# Migración a Rameli v0.9.0 — registro de ejecución (2026-10-18)

Dale del dueño 2026-10-18 ("actualizamos My POD primero, tal cual lo
pide el framework, sin dejar remanentes"). Ejecutada en la rama
`migracion-rameli-v090` según `rameli/MIGRACIONES.md` y el CHANGELOG
v0.8.0 → v0.9.0 del framework (cambio terminológico + criterio de
colocación + contribuciones; sin cambios de datos ni de comportamiento).

## Alcance aplicado

- `rameli.json`: pin 0.8.0 → 0.9.0 + nota de adopción (patrón My Channels).
- `README.md`: pin, nota de migración, frase con término retirado
  reemplazada, celda de versión de `puerta-pinterest-pin` corregida a
  v0.4.0 (verificada en su SKILL.md; estaba desactualizada en la tabla).
- Los 10 skills: `framework_version: "0.9.0"` en su frontmatter.
- Secciones renombradas: "Calibraciones (mecanismo vs instancia)" →
  "(mecanismo vs aplicación)" (5 skills) y "(mecanismo vs instancia vs
  tienda)" → "(mecanismo vs aplicación vs tienda)"
  (publicar-printify-etsy). "(instancia: nicho…)" → "(aplicación:
  nicho…)" en paquete-listing-etsy.
- Dos CHANGELOG de skill cuya primera línea es una declaración viva de
  pin ("Pineado a Rameli v0.8.0") actualizados a v0.9.0.
- `docs/REGLA-DELIVERY-CHATS.md`: apéndice 2026-10-18 con el nombre
  vigente del hub (🎯 My POD — Centro de mando); las entradas viejas
  quedan como historia.
- Scripts: barrido sin hits (ningún término retirado ni pin viejo).
- El gemelo máquina de la ficha de la tienda (`config.json`) NO cambió
  de nombre ni formato. Ningún dato se tocó.

## Verificación (antes vs después, mismo árbol de comparación)

- Barrido final de términos retirados: solo quedan en documentos
  históricos (CHANGELOGs con entradas fechadas, INVENTARIO-PENDIENTES
  del 2026-10-15) — como manda la guía.
- `rameli lint` sobre los 10 skills: resultado IDÉNTICO antes y
  después (3 VERDE: las tres puertas; 17 fallos repartidos en los
  otros 7 skills). La migración introduce cero fallos nuevos.
- Regresión (`rameli test`): puerta-arte-propuesta 8/8 en ambos;
  puerta-publicacion-pod 12 ok / 6 fallas en ambos (preexistente);
  puerta-pinterest-pin 15/15 sobre main con los datos vivos — en el
  worktree aislado marca 4 fallas "asset no registrado como FINAL"
  porque lee el registro commiteado, no el estado vivo: diferencia de
  datos entre árboles, no de la migración.

## Deuda preexistente que la migración NO toca (fase siguiente)

El lint del framework marca 17 fallos de formato en 7 skills
(descripciones sobre el máximo de 220 caracteres, secciones "Cuando
usarme" / "Puertas mecánicas" ausentes en skills escritos antes de
que el lint existiera) y la regresión de puerta-publicacion-pod trae
6 casos en rojo idénticos en main. Son deuda anterior a v0.9.0,
inventariada aquí para corregirla como fase propia con los criterios
nuevos — no se metió en la migración para no repetir el error de
agregar trabajo a mitad de un flujo.
