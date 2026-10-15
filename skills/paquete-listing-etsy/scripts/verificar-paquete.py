#!/usr/bin/env python3
"""Puerta del paquete de listing Etsy.

Valida que el paquete cumpla los criterios mecánicos:
- Título: ≤140 caracteres, sin palabra >2x
- Tags: exactamente 13, cada uno ≤20 caracteres, sin duplicados
- Descripción: contiene disclosure IA, bloque made-to-order, secciones

Uso:
    verificar-paquete.py --paquete ruta.md
"""
import argparse
import re
import sys


def extraer_bloque(texto, inicio, fin="##"):
    """Extrae el contenido entre ## inicio y el siguiente ##."""
    pattern = rf"## {inicio}\n```\n(.*?)\n```"
    m = re.search(pattern, texto, re.DOTALL)
    return m.group(1).strip() if m else ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--paquete", required=True)
    a = ap.parse_args()

    with open(a.paquete) as f:
        texto = f.read()

    errors = []

    # Título
    titulo = extraer_bloque(texto, "Título")
    # El título está en la primera línea del bloque (antes de los ```)
    # Buscarlo directamente
    m = re.search(r"## Título \(\d+ caracteres\)\n```\n(.*?)\n```", texto, re.DOTALL)
    if m:
        titulo = m.group(1).strip()
        if len(titulo) > 140:
            errors.append(f"título {len(titulo)} caracteres > 140")
        palabras = re.findall(r"\b\w+\b", titulo.lower())
        from collections import Counter
        repetidas = [p for p, c in Counter(palabras).items() if c > 2 and len(p) > 2]
        if repetidas:
            errors.append(f"palabras repetidas >2x en título: {repetidas}")
    else:
        errors.append("no se encontró el título")

    # Tags
    m = re.search(r"## 13 tags\n```\n(.*?)\n```", texto, re.DOTALL)
    if m:
        tags_str = m.group(1).strip()
        tags = [t.strip() for t in tags_str.split("|")]
        if len(tags) != 13:
            errors.append(f"tags: {len(tags)} en vez de 13")
        for t in tags:
            if len(t) > 20:
                errors.append(f"tag '{t}' tiene {len(t)} caracteres > 20")
        if len(set(tags)) != len(tags):
            errors.append("tags duplicados")
    else:
        errors.append("no se encontraron los tags")

    # Descripción
    m = re.search(r"## Descripción\n```\n(.*?)\n```", texto, re.DOTALL)
    if m:
        desc = m.group(1)
        if "generative AI" not in desc:
            errors.append("descripción sin disclosure de IA")
        if "made to order" not in desc.lower():
            errors.append("descripción sin bloque made-to-order")
        if "✨ DETAILS" not in desc:
            errors.append("descripción sin sección DETAILS")
        if "📏 FIT" not in desc:
            errors.append("descripción sin sección FIT & CARE")
    else:
        errors.append("no se encontró la descripción")

    if errors:
        print("FAIL:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    print("PASS: paquete válido")
    sys.exit(0)


if __name__ == "__main__":
    main()
