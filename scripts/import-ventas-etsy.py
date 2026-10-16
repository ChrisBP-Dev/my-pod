#!/usr/bin/env python3
"""
import-ventas-etsy.py — Feedback loop de ventas para My POD (M2).

Vía A (principal): Etsy Open API v3 → data/ledger-ventas.json
Vía B (conciliación manual): CSV "Order Items" de Etsy Stats → data/ventas-csv/

HALLAZGO DE INVESTIGACIÓN (2026-10-16): la API v3 NO tiene endpoint de
tráfico (visits/views/fuentes/conversión real). El ledger usa lo que la API
sí da: ventas por listing (receipts), favoritos (num_favorers, snapshot
diario), views del recurso listing (PROXY SIN VERIFICAR — marcado con
caveat), y reviews. Conversión proxy = ventas / favoritos.

Credenciales: NUNCA en el repo. Se leen de env (ETSY_KEYSTRING,
ETSY_SHARED_SECRET) o de ~/.config/my-pod/etsy-api.json (modo 0600),
que crea el modo --auth. El refresh_token vive ahí mismo.

Modos:
  --init        Crea data/ledger-ventas.json semilla desde
                data/registro-listings.json (25 listings, ceros).
  --auth        Flujo OAuth manual: imprime la URL de autorización, el dueño
                pega el código, el script intercambia por tokens y los guarda.
  --pull        Corrida incremental: receipts nuevos (watermark) + snapshot
                diario de listings + reviews → actualiza el ledger.
  --csv FILE    Concilia un CSV "Order Items" descargado a mano contra el
                ledger; guarda diffs en conciliacion_csv.

Uso típico (cron diario): python3 scripts/import-ventas-etsy.py --pull
"""

import argparse
import base64
import csv
import hashlib
import json
import os
import secrets
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone

APP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER_PATH = os.path.join(APP_ROOT, "data", "ledger-ventas.json")
REGISTRO_PATH = os.path.join(APP_ROOT, "data", "registro-listings.json")
CSV_DIR = os.path.join(APP_ROOT, "data", "ventas-csv")
SECRETS_PATH = os.path.expanduser("~/.config/my-pod/etsy-api.json")


def resolve_secrets_path():
    """La ruta del archivo de secretos sale del config de la tienda
    (data/tiendas/<id>/config.json -> etsy_api.secrets_file); si no
    existe, se usa el default. Ver skill conectar-etsy-api."""
    cfg = os.path.expanduser(
        os.environ.get("MY_POD_TIENDA_CONFIG",
                       "~/workspace/my-pod/data/tiendas/29222324/config.json"))
    try:
        c = json.load(open(cfg))
        p = (c.get("etsy_api") or {}).get("secrets_file")
        if p:
            return os.path.expanduser(p)
    except Exception:
        pass
    return SECRETS_PATH

API_BASE = "https://openapi.etsy.com/v3/application"
OAUTH_AUTHORIZE = "https://www.etsy.com/oauth/connect"
OAUTH_TOKEN = "https://api.etsy.com/v3/public/oauth/token"
SCOPES = "email_r shops_r listings_r transactions_r"
SHOP_ID = "68433437"  # MyNightShiftShop (Etsy). OJO: 29222324 es el ID de Printify, no de Etsy.

# ---------------------------------------------------------------- utilidades

def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load_secrets():
    sec = {}
    sp = resolve_secrets_path()
    if os.path.exists(sp):
        with open(sp) as f:
            sec = json.load(f)
    sec.setdefault("keystring", os.environ.get("ETSY_KEYSTRING", ""))
    sec.setdefault("shared_secret", os.environ.get("ETSY_SHARED_SECRET", ""))
    return sec


def save_secrets(sec):
    sp = resolve_secrets_path()
    os.makedirs(os.path.dirname(sp), exist_ok=True)
    with open(sp, "w") as f:
        json.dump(sec, f, indent=2)
    os.chmod(sp, 0o600)


def api_get(path, sec, params=None):
    url = API_BASE + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={
        "x-api-key": f"{sec['keystring']}:{sec['shared_secret']}",
        "Authorization": f"Bearer {sec['access_token']}",
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def slug_map():
    """listing_id (str) -> slug, desde el registro."""
    with open(REGISTRO_PATH) as f:
        reg = json.load(f)
    return {str(v.get("id_etsy")): k for k, v in reg.items() if v.get("id_etsy")}


def empty_ledger():
    return {
        "meta": {
            "fuente": "etsy-open-api-v3",
            "shop_id": int(SHOP_ID),
            "creado": now_iso(),
            "watermark": {"min_created": 0, "last_run": None},
            "seen_receipt_ids": [],
            # HUECO DOCUMENTADO: la API v3 no expone visits/views/fuentes.
            # El campo `views` del recurso listing se reporta como proxy
            # provisional SIN VERIFICAR hasta observar valores no-cero
            # con tráfico real. Conversión proxy = ventas / favoritos.
            "views_listing_no_verificado": True,
            "notas": "Conversión proxy = ventas / favoritos. "
                     "Visits/views/fuentes solo en el dashboard de Etsy Stats.",
        },
        "ventas": [],
        "snapshots_diarios": [],
        "reviews": [],
        "conciliacion_csv": {"ultimo_csv": None, "diffs": []},
    }


# ---------------------------------------------------------------- modos

def cmd_init():
    if os.path.exists(LEDGER_PATH):
        print(f"Ya existe {LEDGER_PATH}; no se toca. Bórralo a mano si quieres re-sembrar.")
        return 0
    ledger = empty_ledger()
    smap = slug_map()
    hoy = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    for lid, slug in sorted(smap.items()):
        ledger["snapshots_diarios"].append({
            "fecha": hoy, "listing_id": lid, "slug": slug,
            "num_favorers": 0, "views": 0,
            "views_caveat": "proxy sin verificar",
        })
    with open(LEDGER_PATH, "w") as f:
        json.dump(ledger, f, indent=2, ensure_ascii=False)
    print(f"Ledger semilla creado: {LEDGER_PATH} ({len(smap)} listings, ventas vacías).")
    return 0


def cmd_auth():
    sec = load_secrets()
    if not sec["keystring"] or not sec["shared_secret"]:
        print("Faltan credenciales. El dueño debe:\n"
              "  1. Crear la Seller App en https://www.etsy.com/developers/register-seller-app\n"
              "     (nombre sin la palabra 'Etsy'; aprobación reportada en minutos).\n"
              "  2. Guardar keystring + shared secret en la bóveda segura.\n"
              "Luego exporta ETSY_KEYSTRING y ETSY_SHARED_SECRET y reintenta.")
        return 2
    verifier = secrets.token_urlsafe(64)
    challenge = base64.urlsafe_b64encode(
        hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
    state = secrets.token_hex(8)
    params = {
        "response_type": "code",
        "redirect_uri": "https://localhost:8080/etsy-oauth",
        "scope": SCOPES,
        "client_id": sec["keystring"],
        "state": state,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    }
    print("1. Abre esta URL con la cuenta de la tienda y autoriza:\n")
    print("   " + OAUTH_AUTHORIZE + "?" + urllib.parse.urlencode(params) + "\n")
    print("2. Etsy redirige a https://localhost:8080/etsy-oauth?code=...&state=...")
    print("   (la página no cargará; copia el valor de 'code' de la barra de dirección).")
    code = input("3. Pega el code aquí: ").strip()
    data = urllib.parse.urlencode({
        "grant_type": "authorization_code",
        "client_id": sec["keystring"],
        "redirect_uri": "https://localhost:8080/etsy-oauth",
        "code": code,
        "code_verifier": verifier,
    }).encode()
    req = urllib.request.Request(OAUTH_TOKEN, data=data,
                                 headers={"Content-Type": "application/x-www-form-urlencoded"})
    with urllib.request.urlopen(req, timeout=30) as r:
        tok = json.load(r)
    sec["access_token"] = tok["access_token"]
    sec["refresh_token"] = tok["refresh_token"]
    sec["expires_at"] = now_iso()
    save_secrets(sec)
    print("OK: tokens guardados en ~/.config/my-pod/etsy-api.json (0600). "
          "Prueba con: python3 scripts/import-ventas-etsy.py --pull")
    return 0


def refresh_if_needed(sec):
    # Estrategia simple: refrescar siempre al inicio de --pull (barato, evita expiración).
    if not sec.get("refresh_token"):
        return sec
    data = urllib.parse.urlencode({
        "grant_type": "refresh_token",
        "client_id": sec["keystring"],
        "refresh_token": sec["refresh_token"],
    }).encode()
    req = urllib.request.Request(OAUTH_TOKEN, data=data,
                                 headers={"Content-Type": "application/x-www-form-urlencoded"})
    with urllib.request.urlopen(req, timeout=30) as r:
        tok = json.load(r)
    sec["access_token"] = tok["access_token"]
    sec["refresh_token"] = tok.get("refresh_token", sec["refresh_token"])
    sec["expires_at"] = now_iso()
    save_secrets(sec)
    return sec


def cmd_pull():
    sec = load_secrets()
    if not sec.get("access_token") or not sec.get("refresh_token"):
        print("Sin tokens OAuth. Corre primero: python3 scripts/import-ventas-etsy.py --auth")
        return 2
    if not os.path.exists(LEDGER_PATH):
        print("No hay ledger. Corre primero --init.")
        return 2
    sec = refresh_if_needed(sec)
    with open(LEDGER_PATH) as f:
        ledger = json.load(f)
    smap = slug_map()
    seen = set(ledger["meta"]["watermark"].get("seen_receipt_ids", []))
    min_created = ledger["meta"]["watermark"].get("min_created", 0)
    hoy = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # 1) Receipts incrementales
    nuevas = 0
    offset = 0
    max_created = min_created
    while True:
        res = api_get(f"/shops/{SHOP_ID}/receipts", sec, {
            "min_created": min_created, "limit": 100, "offset": offset,
            "sort_on": "created", "sort_order": "asc",
        })
        receipts = res.get("results", [])
        if not receipts:
            break
        for rc in receipts:
            rid = rc["receipt_id"]
            max_created = max(max_created, rc.get("created_timestamp", 0))
            if rid in seen:
                continue
            tx = api_get(f"/shops/{SHOP_ID}/receipts/{rid}/transactions", sec)
            for t in tx.get("results", []):
                lid = str(t.get("listing_id"))
                ledger["ventas"].append({
                    "receipt_id": rid,
                    "fecha": datetime.fromtimestamp(
                        rc.get("created_timestamp", 0), tz=timezone.utc
                    ).strftime("%Y-%m-%d"),
                    "listing_id": lid,
                    "slug": smap.get(lid, "desconocido"),
                    "qty": t.get("quantity", 1),
                    "precio_usd": float(t.get("price", {}).get("amount", 0)) / 100.0
                    if isinstance(t.get("price"), dict) else 0.0,
                })
                nuevas += 1
            seen.add(rid)
        if len(receipts) < 100:
            break
        offset += 100

    # 2) Snapshot diario de listings (favoritos + views proxy)
    offset = 0
    while True:
        res = api_get(f"/shops/{SHOP_ID}/listings", sec,
                      {"state": "active", "limit": 100, "offset": offset})
        listings = res.get("results", [])
        if not listings:
            break
        for li in listings:
            lid = str(li["listing_id"])
            ledger["snapshots_diarios"].append({
                "fecha": hoy,
                "listing_id": lid,
                "slug": smap.get(lid, "desconocido"),
                "num_favorers": li.get("num_favorers", 0),
                "views": li.get("views", 0),
                "views_caveat": "proxy sin verificar",
            })
        if len(listings) < 100:
            break
        offset += 100

    # 3) Reviews (para M3)
    try:
        res = api_get(f"/shops/{SHOP_ID}/reviews", sec, {"limit": 100})
        vistos = {(r.get("listing_id"), r.get("created_timestamp"))
                  for r in ledger["reviews"]}
        for rv in res.get("results", []):
            key = (rv.get("listing_id"), rv.get("created_timestamp"))
            if key not in vistos:
                ledger["reviews"].append({
                    "listing_id": str(rv.get("listing_id")),
                    "rating": rv.get("rating"),
                    "fecha": datetime.fromtimestamp(
                        rv.get("created_timestamp", 0), tz=timezone.utc
                    ).strftime("%Y-%m-%d"),
                    "texto": (rv.get("review") or "")[:500],
                })
    except Exception as e:  # reviews es bonus; no bloquea el pull
        print(f"WARN: no se pudieron leer reviews: {e}")

    ledger["meta"]["watermark"]["min_created"] = max_created
    ledger["meta"]["watermark"]["last_run"] = now_iso()
    ledger["meta"]["watermark"]["seen_receipt_ids"] = sorted(seen)
    with open(LEDGER_PATH, "w") as f:
        json.dump(ledger, f, indent=2, ensure_ascii=False)
    print(f"Pull OK: {nuevas} líneas de venta nuevas, "
          f"{len(ledger['ventas'])} total, watermark={max_created}.")
    return 0


def cmd_csv(path):
    if not os.path.exists(LEDGER_PATH):
        print("No hay ledger. Corre primero --init.")
        return 2
    with open(LEDGER_PATH) as f:
        ledger = json.load(f)
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    cols = {c.lower().strip(): c for c in rows[0].keys()} if rows else {}
    lid_col = cols.get("listing id") or cols.get("listing_id")
    qty_col = cols.get("quantity") or cols.get("qty")
    if not lid_col:
        print(f"CSV sin columna 'Listing ID'. Columnas: {list(cols.values())[:10]}")
        return 2
    por_listing = {}
    for r in rows:
        lid = str(r[lid_col]).strip()
        por_listing[lid] = por_listing.get(lid, 0) + int(float(r.get(qty_col, 1) or 1))
    ledger_qty = {}
    for v in ledger["ventas"]:
        ledger_qty[v["listing_id"]] = ledger_qty.get(v["listing_id"], 0) + v["qty"]
    diffs = []
    for lid, q in sorted(por_listing.items()):
        lq = ledger_qty.get(lid, 0)
        if q != lq:
            diffs.append({"listing_id": lid, "csv_qty": q, "ledger_qty": lq,
                          "diff": q - lq})
    ledger["conciliacion_csv"] = {
        "ultimo_csv": os.path.basename(path),
        "fecha": now_iso(),
        "diffs": diffs,
    }
    with open(LEDGER_PATH, "w") as f:
        json.dump(ledger, f, indent=2, ensure_ascii=False)
    if diffs:
        print(f"Conciliación: {len(diffs)} diferencias (ver ledger.conciliacion_csv.diffs).")
    else:
        print("Conciliación OK: CSV y ledger coinciden en cantidades por listing.")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--init", action="store_true")
    ap.add_argument("--auth", action="store_true")
    ap.add_argument("--pull", action="store_true")
    ap.add_argument("--csv", metavar="FILE")
    a = ap.parse_args()
    if a.init:
        return cmd_init()
    if a.auth:
        return cmd_auth()
    if a.pull:
        return cmd_pull()
    if a.csv:
        return cmd_csv(a.csv)
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
