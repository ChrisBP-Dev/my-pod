#!/usr/bin/env python3
"""Puerta de completitud de la ficha visual de la tienda
(publicar-printify-etsy v0.13.0, Programa Estándar My POD F3).

Antes de seleccionar mockups (§M5), esta puerta verifica que la
estrategia visual que el algoritmo va a consumir EXISTA como
decisión de la tienda — no como valor sembrado ni como silencio:

  - config de la tienda → `mpl.esquema_mockups.estado`
  - ficha de cada producto del listing →
    `tomas_preferidas.estado`

Estados y veredicto:
  - `configurado` (en todos los campos revisados) →
    OPERACIÓN NORMAL (exit 0).
  - `provisional...` (alguno provisional, ninguno sin
    configurar) → PILOTO DECLARADO (exit 0, con el aviso en
    grande): el flujo puede correr SOLO como piloto declarado;
    queda anotado en el registro del listing y en el reporte
    de la corrida. Nunca es operación normal.
  - `sin_configurar` o campo ausente (en cualquiera) →
    DETENER (exit 2): la puerta nombra EXACTAMENTE qué falta
    y en qué paso se llena: «Calibración visual de la tienda»
    de `onboarding-tienda` (descubrimiento visual en Fase 1;
    catálogo por producto en Fase 4). No se inventan valores
    y no se usan defaults en silencio.

Uso (modo fixture y en vivo leen los mismos JSON):
    verificar-ficha-visual.py --config <config-tienda.json> \
        --producto <ficha-producto.json> [--producto ...]
"""
import argparse
import json
import sys

PASO = ("«Calibración visual de la tienda» de onboarding-tienda "
        "(presupuesto/reparto: descubrimiento visual, Fase 1; "
        "catálogo por producto: calibración por producto, Fase 4)")


def estado_de(valor):
    """Normaliza el campo estado de una ficha."""
    if valor is None:
        return "sin_configurar"
    v = str(valor).strip().lower()
    if v.startswith("configurado"):
        return "configurado"
    if v.startswith("provisional"):
        return "provisional"
    if v.startswith("sin_configurar") or v.startswith("sin configurar"):
        return "sin_configurar"
    return "sin_configurar"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True,
                    help="config.json de la tienda activa")
    ap.add_argument("--producto", action="append", default=[],
                    help="ficha de producto (data/productos/"
                         "<producto>.json); repetir por producto "
                         "del listing")
    args = ap.parse_args()

    faltantes = []
    provisionales = []
    confirmados = []

    with open(args.config) as f:
        cfg = json.load(f)
    nombre_tienda = cfg.get("nombre") or cfg.get("tienda_id") or args.config
    em = ((cfg.get("mpl") or {}).get("esquema_mockups") or {})
    est = estado_de(em.get("estado"))
    campo = "config → mpl.esquema_mockups.estado (presupuesto de " \
            "fotos, pesos y reparto de la tienda)"
    if est == "sin_configurar":
        faltantes.append(f"{campo}: SIN CONFIGURAR")
    elif est == "provisional":
        provisionales.append(f"{campo}: provisional")
    else:
        confirmados.append(f"{campo}: configurado")

    for ruta in args.producto:
        with open(ruta) as f:
            ficha = json.load(f)
        slug = ficha.get("slug") or ficha.get("producto") or ruta
        tp = ficha.get("tomas_preferidas") or {}
        est = estado_de(tp.get("estado"))
        campo = f"ficha {slug} → tomas_preferidas.estado " \
                f"(catálogo de tomas del producto)"
        if not tp:
            faltantes.append(f"{campo}: SIN CONFIGURAR "
                             f"(la ficha no trae tomas_preferidas)")
        elif est == "sin_configurar":
            faltantes.append(f"{campo}: SIN CONFIGURAR")
        elif est == "provisional":
            provisionales.append(f"{campo}: provisional")
        else:
            confirmados.append(f"{campo}: configurado")

    print(f"Ficha visual — tienda: {nombre_tienda}")
    for c in confirmados:
        print(f"  ✓ {c}")
    for p in provisionales:
        print(f"  ~ {p}")
    for f_ in faltantes:
        print(f"  ✗ {f_}")

    if faltantes:
        print("RESULTADO: DETENIDO — ficha visual incompleta. "
              "Falta, y se llena en el paso " + PASO + ":")
        for f_ in faltantes:
            print(f"  - {f_}")
        print("No se seleccionan mockups: ningún valor se "
              "inventa ni se asume en silencio.")
        return 2
    if provisionales:
        print("RESULTADO: PILOTO DECLARADO — la ficha visual "
              "tiene valores provisionales sin pase del dueño; "
              "el flujo corre SOLO como piloto declarado "
              "(anotarlo en el registro del listing y en el "
              "reporte de la corrida). La calibración se cobra "
              "en el paso " + PASO + ".")
        return 0
    print("RESULTADO: OK — ficha visual configurada; operación "
          "normal.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
