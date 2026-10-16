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
  bases/              # Fotos base de prenda sin arte (por producto/color).
                      #   La prenda física es la misma para todos.
  bases-doblada/      # Calibraciones de doblada por producto/color.
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
- **Mockups**: se generan por tienda porque combinan arte (global) +
  modelo/background (por tienda).

## Multi-usuario

Si le pasas el sistema a un familiar:
1. Se crea `data/tiendas/<nueva-tienda>/`.
2. Esa tienda tiene sus propios modelos y backgrounds.
3. Reutiliza el catálogo compartido (productos, bases).
4. Puede reutilizar tus artes o crear los suyos.

No hay "memoria local" misteriosa: todo está en `data/`, versionado y
accesible por la app.

## Migración pendiente

Los mockups actuales están en `data/flatlays/`, `data/zooms/`, etc. (raíz).
Deben moverse a `data/tiendas/29222324/mockups/` cuando se confirme que
la estructura es la correcta.
