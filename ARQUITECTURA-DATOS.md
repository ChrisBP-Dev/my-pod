# Arquitectura de Datos — Pod Limpio

## Principio

Los datos se separan en **compartidos** (iguales para todos) y **por tienda**
(cada tienda gestiona lo suyo).

## Estructura

```
data/
  # COMPARTIDO — catálogo del sistema, igual para todos los usuarios
  productos/          # Fichas de producto (Gildan 18000...): área de impresión,
                      #   regla de colocación. Viene de Printify, no cambia por tienda.
  artes-print/        # Diseños del usuario (sus creaciones, reutilizables
                      #   en cualquier tienda).
  banco-keywords/     # Keywords (compartido).
  direccion-tienda.md # Directriz semanal de la estratega (humano): reparto,
                      #   mix, precios, NO-hacer. Vigencia 7 días.
  config-propuestas.json  # Directriz semanal MÁQUINA (contrato
                      #   docs/CONTRATO-TIPO-PRODUCTO.md v1.0): tipo_lote
                      #   (mpl/single/mixto), componentes, temas, precios.
                      #   Lo escribe la estratega; lo lee el cron diario.

  # POR TIENDA — cada tienda tiene su propia presentación
  tiendas/
    <tienda-id>/        # Ej: 29222324 (Tú Dale POD - Store)
      config.json        # Nombre, IDs de Printify/Etsy, etc.
      modelos/           # Modelos de ESTA tienda (5 canónicos)
        <modelo-id>/      # latina-30, afroamericana-38, latino-24, rubia-22, pelirroja-24
          referencia.webp  # Cara canónica
          ficha.json       # Descripción, edad aparente
      backgrounds/       # Backgrounds por TEMPORADA para ESTA tienda
        <temporada>-<año>.json  # Ej: navidad-2026.json
                        # Define ambiente, elementos, iluminación, qué transmite
      mockups/           # Mockups generados para ESTA tienda
        flatlays/
        dobladas/
        zooms/
        onmodel/
```

## Por qué así

- **Productos y bases**: son datos del catálogo (Printify). El Gildan 18000
  es el mismo para ti, para tu familiar, para cualquiera. No se duplican.
- **Artes**: son tus creaciones. Las puedes usar en varias tiendas.
- **Modelos**: son una decisión de PRESENTACIÓN de cada tienda. Tu tienda
  puede usar un modelo; la de tu familiar, otro. O pueden compartir — pero
  la gestión es por tienda.
- **Backgrounds**: igual que modelos, es presentación. Cada tienda define
  los suyos.
- **Mockups**: los genera Printify (flujo Printify-first, 2026-10-14);
  qué mockups se usan lo declara el esquema de la config de cada
  tienda. La app no genera mockups propios.

## Multi-usuario

Si le pasas el sistema a un familiar:
1. Se crea `data/tiendas/<nueva-tienda>/`.
2. Esa tienda tiene sus propios modelos y backgrounds.
3. Reutiliza el catálogo compartido (productos, artes del dueño).
4. Puede reutilizar tus artes o crear los suyos.

No hay "memoria local" misteriosa: todo está en `data/`, versionado y
accesible por la app.

## Alcance: qué es global y qué es por tienda

- **Global (catálogo del dueño):** `artes-print/` y `productos/`.
  Un diseño es creación del dueño, no de una tienda: la misma pieza
  puede venderse en varias tiendas SIN duplicar el binario (duplicar
  crearía dos "versiones finales" que divergen). La física del
  producto (área de impresión, proveedor) tampoco depende de la
  tienda. Por eso su ruta NO lleva tienda, deliberadamente.
- **Por tienda** (`data/tiendas/<id>/`): config/ficha (precios,
  esquema de mockups, calendario), estrategia y registro de flujo.
- **Hueco conocido (2026-10-19):** `registro-listings.json` y los
  `estado-*.json` viven HOY en la raíz de `data/` — alcance global
  de facto con una sola tienda. Al abrir la segunda tienda se
  escopan a `data/tiendas/<id>/` en ese mismo cambio; hasta
  entonces se declaran aquí para que ningún lector los crea
  compartidos por diseño.

## Ciclo de vida de los activos (2026-10-19, criterio del dueño)

1. **Un hogar canónico y un estado.** Todo activo vive en el hogar
   que esta arquitectura declara y tiene estado: *candidato*,
   *aprobado*, *en producción* o *descartado*. Un activo sin hogar
   o sin estado es un hallazgo, no un archivo más.
2. **El candidato vive en zona de descarte** (`candidatos-<id>/` o
   `tmp/`), identificable como tal. Al aprobarse, el ganador se
   MUEVE a su hogar canónico y los perdedores se borran en el mismo
   cierre.
3. **Descartado = borrado.** No se archiva "por si acaso": queda la
   huella en el registro (qué fue, quién lo descartó, cuándo) sin
   conservar el binario. Si se reintenta, se parte de cero.
4. **Lo en producción se referencia desde el registro** y se
   commitea: un binario canónico que solo existe en el disco local
   está en riesgo de pérdida, no "guardado". En la pasada de
   remanentes, todo binario sin referencia y sin estado se evalúa
   y se resuelve (mover, registrar o borrar), nunca se deja.
5. **El checkpoint muere con su flujo.** Al cerrar el flujo, su
   `estado-*.json` se resume en el registro o doc correspondiente
   y se borra; un checkpoint de un flujo cerrado es estado muerto
   que finge ser reanudable.
