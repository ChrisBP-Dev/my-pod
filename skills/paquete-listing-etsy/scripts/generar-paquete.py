#!/usr/bin/env python3
"""Genera el paquete de listing Etsy para un diseño.

Lee el banco de keywords del nicho y genera título, descripción,
13 tags y copy siguiendo la metodología del SKILL.md.

Uso:
    generar-paquete.py --diseno p002 --nicho enfermeria \\
        --descripcion "texto que describe el diseño" \\
        --colores White Sand "Sport Grey" --tallas S-3XL \\
        --precio 34.99 --salida /tmp/paquete-p002.md
"""
import argparse
import os
import re


DISCLOSURE_IA = ("Designed with the assistance of generative AI imagery; "
                 "composition, typography, and final artwork directed, edited, "
                 "and finalized by the seller.")

BLOQUE_MADE_TO_ORDER = """⚠️ PLEASE READ — made to order: this sweatshirt is printed just for you after you order, so we can't accept change-of-mind returns or size exchanges. Please check the size chart and message us with any questions before buying. If your item arrives damaged, misprinted, or wrong, we'll replace it free or refund you in full — just send a photo within 7 days. Full details in our Shop Policies & FAQ below."""


def leer_banco(nicho):
    path = f"data/banco-keywords/{nicho}.md"
    if not os.path.isfile(path):
        raise SystemExit(f"no existe banco de keywords: {path}")
    with open(path) as f:
        return f.read()


def generar_titulo(descripcion_corta, keyword_principal, producto="Sweatshirt"):
    # Fórmula: [keyword] [producto], [variante] | [ocasión]
    # Se refina manualmente; esto es un borrador base
    titulo = f"{keyword_principal} {producto}, {descripcion_corta}"
    # Truncar a 140 sin cortar palabra
    if len(titulo) > 140:
        titulo = titulo[:137].rsplit(" ", 1)[0] + "..."
    return titulo


def generar_descripcion(hook, descripcion_larga, colores, tallas, producto_detalle):
    colores_str = ", ".join(colores)
    return f"""{hook}

{DISCLOSURE_IA}

{BLOQUE_MADE_TO_ORDER}

{descripcion_larga}

✨ DETAILS
• {producto_detalle}
• Bold full-color print — crisp lines, vibrant color
• Relaxed unisex fit, ribbed collar, cuffs and hem
• Colors: {colores_str} · Sizes {tallas}

📏 FIT & CARE
• True-to-size unisex fit; size up for an oversized cozy look
• Machine wash cold inside-out, tumble dry low

🎁 MADE TO ORDER
• Printed just for you after you order — please allow production + shipping time.

Thanks for supporting our small shop! ✦"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--diseno", required=True)
    ap.add_argument("--nicho", required=True)
    ap.add_argument("--descripcion", required=True,
                    help="Descripción corta del diseño para el título")
    ap.add_argument("--hook", required=True,
                    help="Hook de 1-2 líneas para la descripción")
    ap.add_argument("--descripcion-larga", required=True,
                    help="Párrafo descriptivo del diseño")
    ap.add_argument("--colores", nargs="+", required=True)
    ap.add_argument("--tallas", required=True)
    ap.add_argument("--precio", required=True)
    ap.add_argument("--keyword", required=True,
                    help="Keyword principal del banco")
    ap.add_argument("--producto-detalle", default="Gildan 18000 Heavy Blend™ crewneck (50% cotton / 50% polyester)")
    ap.add_argument("--tags", nargs=13, required=True,
                    help="13 tags (se validan, no se generan automáticamente)")
    ap.add_argument("--salida", required=True)
    a = ap.parse_args()

    banco = leer_banco(a.nicho)
    titulo = generar_titulo(a.descripcion, a.keyword)

    descripcion = generar_descripcion(
        a.hook, a.descripcion_larga, a.colores, a.tallas, a.producto_detalle)

    copy = f"""{a.hook}
The sweatshirt your unit will ask about.
Cozy Gildan heavyweight crewneck — {', '.join(a.colores)}.
👉 [link del listing]"""

    with open(a.salida, "w") as f:
        f.write(f"# Paquete Etsy — {a.diseno}\n\n")
        f.write(f"**Nicho:** {a.nicho} · **Colores:** {', '.join(a.colores)} · ")
        f.write(f"**Tallas:** {a.tallas} · **Precio:** ${a.precio}\n\n")
        f.write(f"## Título ({len(titulo)} caracteres)\n```\n{titulo}\n```\n\n")
        f.write(f"## Descripción\n```\n{descripcion}\n```\n\n")
        f.write("## 13 tags\n```\n")
        f.write(" | ".join(a.tags))
        f.write("\n```\n\n")
        f.write(f"## Copy de anuncio\n```\n{copy}\n```\n")
        f.write("\n## Notas\n")
        f.write("- Production partner: Printify (declaración obligatoria en Etsy).\n")
        f.write("- Revisar título y tags con el dueño antes de publicar.\n")

    print(f"paquete generado: {a.salida}")
    print(f"NOTA: título y tags son borrador — requieren refinamiento del dueño.")


if __name__ == "__main__":
    main()
