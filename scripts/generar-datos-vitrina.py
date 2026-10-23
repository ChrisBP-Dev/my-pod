#!/usr/bin/env python3
"""Generar los datos de una Vitrina de revisión de propuestas (My POD).

Parte del sistema (plantilla replicable): convierte el registro de una
tienda (`data/tiendas/<tienda-id>/registro-listings.json`) y el checkpoint
de propuestas de la tienda (`data/tiendas/<tienda-id>/estado-propuestas.json`)
en el paquete de datos que
alimenta una vitrina: `datos-vitrina.json` + vistas previas ligeras de
cada arte (sobre fondo oscuro y sobre fondo claro).

La vitrina es la superficie de la puerta creativa de la Etapa 1 del
flujo v2 (ver `docs/VITRINA-REVISION.md`): el dueño decide ahí
(aprobado / rechazado / mejorar + nota) y sus decisiones quedan
guardadas como datos que Jarvis lee y vuelca al checkpoint del sistema.

Uso:
    python3 scripts/generar-datos-vitrina.py \
        --tienda 29222324 --tienda-nombre MyNightShiftShop \
        --repo ~/workspace/my-pod \
        --salida ~/workspace/vitrina-piloto \
        [--slugs p058,p059] [--ancho-previa 1100]

Sin `--slugs`, toma el lote actual de `data/tiendas/<tienda-id>/estado-propuestas.json`.
Las previas se componen determinísticamente desde el PNG de impresión
(el de producción): fondo oscuro #17181c y fondo claro #f4f1ea, para que
el dueño juzgue el arte como se verá sobre prenda oscura o clara.

Personalizables (cierre del hueco, 2026-10-22): si la entrada del
registro trae `personalizable: true`, el paquete incluye la previa de
la SIMULACIÓN (el compuesto sobre el arte real declarado en
`simulacion` del registro) en ambos fondos y la `ficha_razon`
estructurada. Sin simulación o sin ficha completa, el generador
FALLA: un personalizable sin simulación no se puede juzgar en la
vitrina (puerta-arte-propuesta, variante personalizable) y sembrarlo
disfrazado de normal era el hueco.
"""
import argparse
import json
import re
import sys
from pathlib import Path

from PIL import Image

FONDO_OSCURO = (23, 24, 28)
FONDO_CLARO = (244, 241, 234)

# Especialidades detectables en el porqué (etiqueta visible en la tarjeta)
ESPECIALIDADES = [
    (r"\bER\b|emergencias", "ER"),
    (r"\bICU\b|cuidados intensivos", "ICU"),
    (r"\bNICU\b", "NICU"),
    (r"\bPACU\b|recuperación", "PACU"),
]


def partir_porque(porque: str) -> dict:
    """Parte el porqué canónico en sus secciones de entrega.

    El porqué se guarda como un solo texto con marcadores
    («Tema y ángulo:», «Frase:», «Iconografía:», «Qué mirar:»).
    Si un marcador no aparece, su sección queda vacía y el texto
    completo va en `tema_angulo` (la vitrina nunca inventa secciones).
    """
    secciones = {"tema_angulo": "", "frase_texto": "", "iconografia": "", "que_mirar": ""}
    marcadores = [
        ("Tema y ángulo:", "tema_angulo"),
        ("Frase:", "frase_texto"),
        ("Iconografía:", "iconografia"),
        ("Qué mirar:", "que_mirar"),
    ]
    cortes = []
    for marcador, clave in marcadores:
        idx = porque.find(marcador)
        if idx >= 0:
            cortes.append((idx, marcador, clave))
    if not cortes:
        secciones["tema_angulo"] = porque.strip()
        return secciones
    cortes.sort()
    for i, (idx, marcador, clave) in enumerate(cortes):
        fin = cortes[i + 1][0] if i + 1 < len(cortes) else len(porque)
        secciones[clave] = porque[idx + len(marcador):fin].strip()
    return secciones


def frase_corta(secciones: dict) -> str:
    m = re.search(r"«([^»]+)»", secciones.get("frase_texto", ""))
    return m.group(1) if m else ""


def etiquetas_de(entrada: dict, secciones: dict) -> list:
    texto = entrada.get("porque", "")
    etiquetas = []
    tema = entrada.get("tema", "")
    if tema.startswith("navidad"):
        etiquetas.append("Navidad")
    elif tema.startswith("evergreen"):
        etiquetas.append("Evergreen")
    for patron, nombre in ESPECIALIDADES:
        if re.search(patron, texto):
            etiquetas.append(nombre)
            break
    if "turno nocturno" in texto:
        etiquetas.append("Turno nocturno")
    if entrada.get("track") == "mpl":
        etiquetas.append("MPL")
    return etiquetas


def producto_destino(entrada: dict) -> str:
    if entrada.get("track") == "mpl":
        return "MPL — sudadera + playera (un solo listing)"
    if entrada.get("track") == "single":
        ficha = entrada.get("ficha_razon") or {}
        if entrada.get("personalizable") and ficha.get("producto_destino"):
            return ficha["producto_destino"]
        return "Single — un producto"
    return entrada.get("track", "")


# Campos obligatorios de la ficha de razón de un personalizable
# (puerta-arte-propuesta, «La ficha de razón»). Sin ficha completa
# no hay entrega: el generador es la puerta mecánica de ese criterio.
FICHA_CAMPOS = [
    "razon",
    "prueba_borrado",
    "campos",
    "comprador_destinatario_ocasion",
    "clase_encaje",
    "ejemplo_simulacion",
    "peor_caso",
    "producto_destino",
    "plan_zonas",
]


def validar_personalizable(slug: str, entrada: dict, repo: Path) -> dict:
    """Devuelve {simulacion_path, ficha} o termina con error claro."""
    sim_rel = entrada.get("simulacion", "")
    sim_path = repo / sim_rel if sim_rel else None
    if not sim_path or not sim_path.exists():
        print(f"ERROR: {slug} es personalizable pero no tiene simulación "
              f"válida en el registro (`simulacion`: {sim_rel!r}). "
              "Sin simulación no hay entrega (puerta-arte-propuesta).",
              file=sys.stderr)
        raise SystemExit(1)
    ficha = entrada.get("ficha_razon")
    if not isinstance(ficha, dict):
        print(f"ERROR: {slug} es personalizable y no trae `ficha_razon`. "
              "Sin ficha completa no hay entrega.", file=sys.stderr)
        raise SystemExit(1)
    faltan = [c for c in FICHA_CAMPOS if not ficha.get(c)]
    if faltan:
        print(f"ERROR: {slug}: ficha_razon incompleta, faltan: "
              f"{', '.join(faltan)}.", file=sys.stderr)
        raise SystemExit(1)
    for campo in ficha["campos"]:
        if not campo.get("nombre") or not campo.get("tipo"):
            print(f"ERROR: {slug}: cada campo de la ficha trae `nombre` "
                  "y `tipo` (texto/dropdown/imagen).", file=sys.stderr)
            raise SystemExit(1)
        if campo["tipo"] == "texto" and not campo.get("limite"):
            print(f"ERROR: {slug}: el campo {campo['nombre']!r} es de "
                  "texto y no declara `limite` de caracteres.",
                  file=sys.stderr)
            raise SystemExit(1)
        if campo["tipo"] == "dropdown" and not campo.get("opciones"):
            print(f"ERROR: {slug}: el campo {campo['nombre']!r} es "
                  "dropdown y no declara `opciones` (vocabulario cerrado).",
                  file=sys.stderr)
            raise SystemExit(1)
    return {"simulacion_path": sim_path, "ficha": ficha}


def dimensiones_de(arte_path: Path) -> dict:
    with Image.open(arte_path) as im:
        return {"ancho_px": im.width, "alto_px": im.height}


def hacer_previa(arte_path: Path, destino: Path, fondo, ancho: int) -> None:
    arte = Image.open(arte_path).convert("RGBA")
    if arte.width > ancho:
        alto = round(arte.height * ancho / arte.width)
        arte = arte.resize((ancho, alto), Image.LANCZOS)
    lienzo = Image.new("RGBA", arte.size, fondo + (255,))
    lienzo.alpha_composite(arte)
    destino.parent.mkdir(parents=True, exist_ok=True)
    lienzo.convert("RGB").save(destino, "JPEG", quality=88, optimize=True)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tienda", required=True, help="id de tienda (carpeta en data/tiendas/)")
    ap.add_argument("--tienda-nombre", default="", help="nombre visible de la tienda")
    ap.add_argument("--repo", default=".", help="raíz del repo/datos de la app (donde vive data/)")
    ap.add_argument("--salida", required=True, help="carpeta de salida del paquete de la vitrina")
    ap.add_argument("--slugs", default="", help="lista separada por comas; default: lote actual del checkpoint")
    ap.add_argument("--ancho-previa", type=int, default=1100)
    args = ap.parse_args()

    repo = Path(args.repo).expanduser()
    salida = Path(args.salida).expanduser()
    registro_path = repo / "data" / "tiendas" / args.tienda / "registro-listings.json"
    estado_path = repo / "data" / "tiendas" / args.tienda / "estado-propuestas.json"
    if not registro_path.exists():
        print(f"ERROR: no existe el registro: {registro_path}", file=sys.stderr)
        return 1
    registro = json.loads(registro_path.read_text(encoding="utf-8"))

    if args.slugs:
        slugs = [s.strip() for s in args.slugs.split(",") if s.strip()]
        lote_fecha = ""
    else:
        if not estado_path.exists():
            print(f"ERROR: no existe el checkpoint: {estado_path}", file=sys.stderr)
            return 1
        estado = json.loads(estado_path.read_text(encoding="utf-8"))
        lote = estado.get("lote_actual", {})
        slugs = lote.get("disenos", [])
        lote_fecha = lote.get("fecha", "")
    if not slugs:
        print("ERROR: lote vacío (sin slugs).", file=sys.stderr)
        return 1

    disenos = []
    for slug in slugs:
        entrada = registro.get(slug)
        if entrada is None:
            print(f"ERROR: {slug} no está en el registro de la tienda.", file=sys.stderr)
            return 1
        arte_rel = entrada.get("arte", "")
        arte_path = repo / arte_rel
        if not arte_path.exists():
            print(f"ERROR: no existe el arte de {slug}: {arte_path}", file=sys.stderr)
            return 1
        secciones = partir_porque(entrada.get("porque", ""))
        previa_oscura = salida / "previas" / f"{slug}-oscura.jpg"
        previa_clara = salida / "previas" / f"{slug}-clara.jpg"
        hacer_previa(arte_path, previa_oscura, FONDO_OSCURO, args.ancho_previa)
        hacer_previa(arte_path, previa_clara, FONDO_CLARO, args.ancho_previa)
        personalizable = entrada.get("personalizable") is True
        sim_oscura = sim_clara = None
        ficha = None
        etiquetas = etiquetas_de(entrada, secciones)
        if personalizable:
            valido = validar_personalizable(slug, entrada, repo)
            ficha = valido["ficha"]
            sim_oscura_path = salida / "previas" / f"{slug}-sim-oscura.jpg"
            sim_clara_path = salida / "previas" / f"{slug}-sim-clara.jpg"
            hacer_previa(valido["simulacion_path"], sim_oscura_path,
                         FONDO_OSCURO, args.ancho_previa)
            hacer_previa(valido["simulacion_path"], sim_clara_path,
                         FONDO_CLARO, args.ancho_previa)
            sim_oscura = f"previas/{slug}-sim-oscura.jpg"
            sim_clara = f"previas/{slug}-sim-clara.jpg"
            etiquetas.append("Personalizable")
        disenos.append({
            "slug": slug,
            "titulo": entrada.get("titulo", slug),
            "tema": entrada.get("tema", ""),
            "etiquetas": etiquetas,
            "frase": frase_corta(secciones),
            "tema_angulo": secciones["tema_angulo"],
            "frase_texto": secciones["frase_texto"],
            "iconografia": secciones["iconografia"],
            "que_mirar": secciones["que_mirar"],
            "puerta": entrada.get("nota_puerta", ""),
            "producto_destino": producto_destino(entrada),
            "personalizable": personalizable,
            "simulacion": sim_oscura,
            "simulacion_clara": sim_clara,
            "ficha_razon": ficha,
            "arte_ref": arte_rel,
            "dimensiones_px": dimensiones_de(arte_path),
            "previa_oscura": f"previas/{slug}-oscura.jpg",
            "previa_clara": f"previas/{slug}-clara.jpg",
        })

    paquete = {
        "version_contrato": 1,
        "tienda": {"id": args.tienda, "nombre": args.tienda_nombre},
        "lote": {"fecha": lote_fecha, "slugs": slugs},
        "disenos": disenos,
    }
    salida.mkdir(parents=True, exist_ok=True)
    (salida / "datos-vitrina.json").write_text(
        json.dumps(paquete, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK: {len(disenos)} diseños → {salida / 'datos-vitrina.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
