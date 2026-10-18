# my-pod — aplicación POD (cuarto limpio)

App construida con Rameli **v0.9.0** (pineado en `rameli.json`).
Valida el framework en el camino más corto antes de construir My Channels.

## Migración a Rameli v0.9.0 (2026-10-18)

Adoptada por dale del dueño, siguiendo `rameli/MIGRACIONES.md`:
pin en `rameli.json` y en el frontmatter de los 10 skills, secciones
"Calibraciones (mecanismo vs aplicación)" renombradas, terminología
canónica (framework / aplicación / ficha) en los documentos vivos.
El gemelo máquina de la ficha de la tienda (`config.json`) no cambió
de nombre ni de formato: ningún dato se tocó. Los documentos
históricos conservan la terminología de su época.

## Skills

| Skill | Versión | Qué puerta |
|---|---|---|
| `conectar-etsy-api` | v0.1.1 | Conexión API Etsy por tienda: Seller App → OAuth PKCE → tokens → registro |
| `estratega-tienda` | v0.5.1 | Dirección semanal de tienda: reparto de foco, mix, guía de precios, NO-hacer |
| `estratega-pinterest` | v0.1.0 | Parrilla de Pinterest: 5 pins/día, mix por listing |
| `onboarding-tienda` | v0.1.2 | Playbook de puesta en marcha: de cero a tienda operativa |
| `paquete-listing-etsy` | v0.2.0 | Paquete comercial del listing: título, descripción, tags, keywords |
| `publicar-printify-etsy` | v0.7.2 | Drafts en Printify → ensamblaje MPL → publicación en Etsy |
| `publicador-lote` | v0.1.1 | Lote aprobado → side chat: manifiesto explícito, checkpoints por listing, reporte |
| `puerta-arte-propuesta` | v0.4.0 | Arte listo: PNG 300 DPI, fondo transparente, sin blanco puro |
| `puerta-pinterest-pin` | v0.4.0 | Pin listo: asset FINAL del listing, keywords con fuente, URL rastreable |
| `puerta-publicacion-pod` | v0.2.2 | Mockup listo: dimensiones, DPI ≥300, placement contra el flat-lay aprobado DE ESE DISEÑO |

## Principios operativos (para quien opere esta app)

Esta app es portable: quien la clone recibe skills + docs + scripts.
Estos principios rigen cómo se opera, sin depender del manual del
operador original:

- **Patrones de resiliencia** (`docs/PATRONES-RESILIENCIA.md`): todo
  trabajo largo con dependencia externa lleva health-check antes de
  trabajar, checkpoints con resume, y reintentos acotados (tope 3/día).
- **Puesta en marcha** (`skills/onboarding-tienda`): playbook de cero
  a tienda operativa; es el que aplica los patrones al crear crons.
- **Capas**: sistema portable y versionado (skills/docs/scripts) vs
  tienda (config en `data/tiendas/<id>/`). Nada de la tienda quemado
  en código.
- **API-first**: lo que cubre la API de Etsy va por API; navegador
  solo para lo no expuesto (`docs/ESTANDAR-ETSY-API-VS-NAVEGADOR.md`).

## Docs operativos

- `docs/PATRONES-RESILIENCIA.md` — patrones portables para workers con dependencias externas (health-check, checkpoints, reintentos acotados).
- `docs/CONTRATO-TIPO-PRODUCTO.md` — contrato de tipo de lote (mpl/single/mixto).
- `docs/ESTANDAR-ETSY-API-VS-NAVEGADOR.md` — API-first; navegador solo para lo no expuesto.
- `docs/REGLA-DELIVERY-CHATS.md` — reportes automáticos en chat nuevo, nunca en archivados.

## Datos

- `data/registro-listings.json` — listings + sus assets finales aprobados (4 listings, 44 assets).
- `data/banco-keywords/` — bancos de keywords por nicho.
- `data/cola-pins/` — pins que pasaron la puerta, en espera de publicación.

## Criterios canónicos

- `CRITERIO-COLOCACION.md` — la referencia es el flat-lay aprobado del diseño.
- `VISION-BIBLIOTECA-MOCKUPS-BORRADOR.md` — biblioteca de mockups por tienda.
- `CAMINO-OPTIMIZADO-BORRADOR.md` — flujo end-to-end revalidado.
