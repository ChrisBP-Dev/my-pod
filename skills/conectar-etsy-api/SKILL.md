---
name: "conectar-etsy-api"
description: "Conecta la API de Etsy (v3, OAuth 2.0 + PKCE) para UNA tienda: crea la Seller App, guía el grant del dueño, canjea tokens, verifica la conexión y la registra en el config de la tienda. Flujo por tienda, portable."
compatibility: "framework >= 0.4.0"
metadata:
  version: "0.1.1"
  framework_version: "0.11.0"
---

# Conectar API de Etsy por tienda

**Versión 0.1.0** (2026-10-16: extraído del montaje manual de
MyNightShiftShop — primera conexión real verificada).

## Principio

La conexión API es **por tienda**: cada tienda tiene su Seller App, sus
tokens y su `shop_id`. Este skill es el **mecanismo** (pasos); los
valores (shop, scopes, archivos) son la **calibración** de cada tienda
y viven en `data/tiendas/<id>/config.json`.

**Por qué no es un conector formal del sistema:** el API de Etsy exige
en cada llamada el header compuesto `x-api-key: keystring:shared_secret`
ADEMÁS del bearer token OAuth — un esquema de doble secreto que el
sistema de conectores no modela limpiamente. Por eso las credenciales
viven en `~/.config/my-pod/etsy-api-<shop>.json` (0600, nunca en
repo/chat/logs) y los scripts las leen directo. Si el sistema de
conectores soporta el esquema en el futuro, migrar.

## Cuándo usarme

- Cuando una tienda de la app se conecta al API de Etsy por primera
  vez, o hay que re-conectar: tokens revocados, scopes nuevos,
  Seller App nueva.
- NO para el día a día de una tienda ya conectada: eso va por los
  scripts y skills que consumen la conexión ya registrada.

## Procedimiento

Resumen (el detalle paso a paso está en ## Flujo): 1) crear la
Seller App en la cuenta del dueño; 2) OAuth con PKCE, con el clic
del dueño; 3) verificación con una llamada real — sin esto no está
"conectado"; 4) registro de la conexión en el config de la tienda.
Es interactivo: el paso 2 exige la presencia del dueño.

## Flujo

### 1. Seller App (navegador, cuenta del dueño)
1. `https://www.etsy.com/developers/your-apps` → "Create a New App".
2. Nombre: `My POD - <shop-name>`. Registrar callback URLs:
   `http://localhost:8080/etsy-oauth` y
   `https://localhost:8080/etsy-oauth`.
3. Anotar `keystring` y `shared_secret` (botón Show) → guardar en el
   archivo de secretos (abajo). La app se aprueba sola (rate limit
   estándar 10 QPS / 10K QPD).

### 2. OAuth con PKCE (script + clic del dueño)
1. Generar `code_verifier` (43–128 chars), `code_challenge = S256`,
   `state` aleatorio. Guardar verifier+state en el archivo de secretos.
2. Construir la authorize URL:
   `https://www.etsy.com/oauth/connect?response_type=code`
   `&redirect_uri=http://localhost:8080/etsy-oauth`
   `&scope=<scopes separados por espacio>`
   `&client_id=<keystring>&state=<state>`
   `&code_challenge=<challenge>&code_challenge_method=S256`
3. **El dueño** abre la URL en su dispositivo, da "Grant access"; la
   página falla (esperado — nada escucha en localhost). Pega en el
   chat el valor de `code` de la barra de direcciones.
   - LECCIÓN 2026-10-16: el navegador automatizado NO puede leer el
     `code` del redirect a localhost (el harness no expone el query
     string de navegaciones fallidas ni observa páginas localhost).
     No montar listeners locales: el navegador no comparte el
     loopback de la VM. El code lo pega el dueño, siempre.
   - Los codes expiran en minutos: canjear en cuanto llegue.
4. `POST https://api.etsy.com/v3/public/oauth/token`
   (form-urlencoded): `grant_type=authorization_code`,
   `client_id`, `redirect_uri` (idéntico al del paso 2), `code`,
   `code_verifier`. Guardar `access_token` + `refresh_token`;
   borrar verifier y state del archivo.

### 3. Verificación (gate — sin esto no está "conectado")
1. `GET /users/me` → 200 con el `user_id` del dueño.
2. `GET /users/<user_id>/shops` → confirmar `shop_id` y `shop_name`.
   **OJO:** el `shop_id` de Etsy NO es el ID de Printify (lección
   2026-10-16: 29222324 era Printify; el real era 68433437).
3. `GET /shops/<shop_id>/receipts?limit=1` → 200.
4. Header obligatorio en cada llamada:
   `x-api-key: <keystring>:<shared_secret>` + `Authorization: Bearer`.
   Si falta el secret → 403 "Shared secret is required in x-api-key
   header" (lección 2026-10-16).

### 4. Registro en el config de la tienda
En `data/tiendas/<id>/config.json`:
```json
"etsy_api": {
  "shop_id": "68433437",
  "scopes": ["email_r", "shops_r", "listings_r", "transactions_r"],
  "secrets_file": "~/.config/my-pod/etsy-api-<shop>.json",
  "conectada_el": "2026-10-16"
}
```

## Scopes

- Lectura base: `email_r shops_r listings_r transactions_r`.
- Escritura de listings: sumar `listings_w` (precios, inventario,
  título/tags/descripción, imágenes, borradores). Requiere
  re-autorización: repetir el paso 2 con el scope agregado (el dueño
  vuelve a dar grant; los tokens se reemplazan).
- **No pedir scopes de más:** el mínimo que el flujo necesite.

## Límites conocidos del API (van por navegador)

El API v3 **no expone**: sales events / Sales and discounts, cupones y
Targeted Offers, estadísticas de visitas/views/fuentes de tráfico,
mensajes con compradores. Canon de enrutamiento:
`docs/ESTANDAR-ETSY-API-VS-NAVEGADOR.md` (los skills consumidores
apuntan ahí).

## Refresh de tokens

El `access_token` expira (~1h); el `refresh_token` rota. Los scripts
refrescan solos vía `scripts/etsy_auth.py` (`get_headers()` /
`load_secrets()` renuevan el token si está por vencer y reescriben el
archivo 0600). Todo script nuevo que hable con la API de Etsy DEBE usar
ese helper, nunca un token leído a mano. Si un refresh falla con
400/401, repetir el paso 2 (re-grant del dueño).
