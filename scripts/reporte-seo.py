#!/usr/bin/env python3
"""
reporte-seo.py — M4: cruza banco-keywords × ledger de ventas.

Lee:
  data/banco-keywords/*.md        frases semilla por nicho (Etsy y Pinterest)
  data/paquetes-listing/*         título, descripción y tags reales por listing
  data/registro-listings.json     nicho + id_etsy por slug
  data/ledger-ventas.json         ventas y favoritos por listing (si hay datos)

Reporta por nicho:
  - cobertura: qué keywords del banco usa cada listing (título/desc/tags)
  - keywords del banco que NADIE usa (huecos)
  - listings sin ninguna keyword del banco (riesgo SEO)
  - cuando el ledger tiene datos: ventas/favoritos atribuidos por keyword

Uso: python3 scripts/reporte-seo.py [--nicho enfermeria]
Sin datos de ventas aún, el reporte muestra cobertura y lo dice explícito.
"""

import argparse
import glob
import json
import os
import re
import sys
from collections import defaultdict

APP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BANKS_DIR = os.path.join(APP_ROOT, "data", "banco-keywords")
PAQUETES_DIR = os.path.join(APP_ROOT, "data", "paquetes-listing")
REGISTRO_PATH = os.path.join(APP_ROOT, "data", "registro-listings.json")
LEDGER_PATH = os.path.join(APP_ROOT, "data", "ledger-ventas.json")


def extract_keywords(bank_path):
    phrases = []
    with open(bank_path, encoding="utf-8") as f:
        for line in f:
            m = re.match(r"^\s*\d+\.\s+(.+?)\s*$", line)
            if m:
                phrases.append(m.group(1).strip())
                continue
            m = re.match(r"^\s*\|\s*\d+\s*\|\s*([^|]+?)\s*\|", line)
            if m:
                phrases.append(m.group(1).strip())
    seen, out = set(), []
    for p in phrases:
        p = p.strip().lower()
        if " " in p and p not in seen:
            seen.add(p)
            out.append(p)
    return out


def parse_paquete(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    def block(header):
        m = re.search(re.escape(header) + r".*?```\n(.*?)```", text, re.S)
        return m.group(1).strip() if m else ""
    titulo = block("## Título")
    descripcion = block("## Descripción")
    tags_raw = block("## 13 tags")
    tags = [t.strip().lower() for t in tags_raw.split("|") if t.strip()]
    slug = os.path.basename(path).replace("-paquete.md", "")
    return slug, {"titulo": titulo, "descripcion": descripcion, "tags": tags,
                  "texto": (titulo + "\n" + descripcion + "\n" + " ".join(tags)).lower()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nicho", default=None)
    args = ap.parse_args()

    reg = json.load(open(REGISTRO_PATH, encoding="utf-8"))
    slug2niche = {k: v.get("nicho", "?") for k, v in reg.items()}
    slug2lid = {k: str(v.get("id_etsy")) for k, v in reg.items() if v.get("id_etsy")}
    lid2slug = {v: k for k, v in slug2lid.items()}

    paquetes = {}
    for p in glob.glob(os.path.join(PAQUETES_DIR, "*-paquete.md")):
        slug, data = parse_paquete(p)
        paquetes[slug] = data

    # ledger (tolerante a vacío/ausente)
    ventas_por_slug = defaultdict(int)
    favs_por_slug = defaultdict(int)
    hay_datos = False
    if os.path.exists(LEDGER_PATH):
        ledger = json.load(open(LEDGER_PATH, encoding="utf-8"))
        for v in ledger.get("ventas", []):
            slug = lid2slug.get(str(v["listing_id"]), v.get("slug"))
            if slug:
                ventas_por_slug[slug] += v.get("qty", 0)
        vistos = set()
        for s in sorted(ledger.get("snapshots_diarios", []),
                        key=lambda x: x["fecha"], reverse=True):
            slug = lid2slug.get(str(s["listing_id"]), s.get("slug"))
            if slug and slug not in vistos:
                vistos.add(slug)
                favs_por_slug[slug] = s.get("num_favorers", 0)
        hay_datos = bool(ledger.get("ventas"))

    # bancos por nicho y canal
    bancos = defaultdict(dict)  # nicho -> {"etsy": [...], "pinterest": [...]}
    for b in glob.glob(os.path.join(BANKS_DIR, "*.md")):
        name = os.path.basename(b)[:-3]
        canal = "pinterest" if name.startswith("pinterest-") else "etsy"
        nicho = name.replace("pinterest-", "")
        bancos[nicho][canal] = extract_keywords(b)

    nichos = sorted(bancos) if not args.nicho else [args.nicho]
    print(f"# Reporte SEO — cruce banco-keywords × ledger ({len(paquetes)} paquetes)")
    if not hay_datos:
        print("SIN DATOS DE VENTAS AÚN: el ledger está vacío; "
              "el reporte muestra cobertura de keywords.\n")

    for nicho in nichos:
        if nicho not in bancos:
            print(f"## {nicho}: sin banco de keywords\n")
            continue
        slugs = sorted(s for s, n in slug2niche.items()
                       if n == nicho and s in paquetes)
        print(f"## Nicho: {nicho} ({len(slugs)} listings con paquete)")
        for canal in ("etsy", "pinterest"):
            kws = bancos[nicho].get(canal, [])
            if not kws:
                continue
            print(f"\n### Banco {canal} ({len(kws)} frases)")
            cobertura = {kw: [] for kw in kws}
            for slug in slugs:
                texto = paquetes[slug]["texto"]
                for kw in kws:
                    if kw in texto:
                        cobertura[kw].append(slug)
            sin_uso = [kw for kw, ss in cobertura.items() if not ss]
            print(f"Cubiertas: {len(kws) - len(sin_uso)}/{len(kws)}")
            for kw in sorted(kws, key=lambda k: -len(cobertura[k])):
                ss = cobertura[kw]
                extra = ""
                if hay_datos:
                    v = sum(ventas_por_slug[s] for s in ss)
                    f = sum(favs_por_slug[s] for s in ss)
                    extra = f" | ventas={v} favs={f}"
                print(f"  - {kw}: {len(ss)} listings{extra}")
            if sin_uso:
                print(f"HUECOS (nadie las usa): {', '.join(sin_uso)}")
        # listings sin ninguna keyword del banco
        todas = [kw for c in bancos[nicho].values() for kw in c]
        huerfanos = [s for s in slugs
                     if not any(kw in paquetes[s]["texto"] for kw in todas)]
        if huerfanos:
            print(f"\nRIESGO SEO (0 keywords del banco): {', '.join(huerfanos)}")
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
