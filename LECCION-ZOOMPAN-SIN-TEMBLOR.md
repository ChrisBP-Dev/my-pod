# Lección: temblor en zoompan de FFmpeg (2026-10-14)

## El error
Los videos generados con `zoompan` temblaban/vibraban visiblemente.
El usuario lo detectó: "parece que estuviese temblando todo".

## La causa
El filtro `zoompan` de FFmpeg **trunca la posición a píxeles enteros** en cada frame.
Con movimientos lentos (fracción de píxel por frame), el recorte cae en el mismo
píxel entero durante varios frames y luego salta un píxel completo.
El ojo lo lee como temblor o vibración.

Si la expresión es acumulativa (`z='min(zoom+0.002,1.2)'`), el error de
truncamiento **se acumula** frame tras frame, empeorando el temblor.

## La solución
1. **Posición absoluta por frame, no acumulativa:**
   - Mal: `z='min(zoom+0.002,1.2)'` (suma al frame anterior, acumula error)
   - Bien: `z='1+0.25*on/105'` (calcula desde el número de frame, exacto)
2. **Trabajar al doble de resolución:** escalar a 2160×2160 primero,
   luego zoompan baja a 1080. Reduce el salto visible a medio píxel.

## Referencias
- https://github.com/jham2081-blip/glide-ffmpeg (explica el truncamiento)
- https://github.com/kingithegreat/sadie/commit/69395c7150689ba028b8daab07766db340c445d8
  (2x + posición absoluta: judder 0.361 → 0.004)

## Regla
Todo zoom con `zoompan` en nuestros scripts DEBE usar posición absoluta (`on`)
y trabajar a 2x. Nunca usar `zoom+step` acumulativo.
