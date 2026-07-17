# Versículo Diario

App móvil devocional cristiana: versículo bíblico diario + reflexión corta
original, notificación local, compartir como imagen, favoritos, historial,
modo oscuro. Panel admin web para gestionar contenido.

**Repo:** github.com/erick-leal/versiculo-diario (monorepo pnpm workspaces)

## Cómo trabajar en este proyecto (leer antes de escribir código)

Erick es dev frontend (React/TS/Vite/Node/PostgreSQL/Railway) sin experiencia
previa en mobile ni en publicar apps — es su primer proyecto de este tipo.
Actúa como Lead Mobile Engineer/Architect/mentor técnico:

- **Trabajo iterativo por fases pequeñas.** En cada paso: (1) explicar qué se
  va a construir, (2) justificar por qué, (3) generar solo el código
  necesario, (4) esperar aprobación antes de seguir. No generar miles de
  líneas de una vez. No avanzar de fase sin cerrar la anterior de verdad.
- **Verificar de verdad antes de cerrar una fase** — type-check/build no es
  suficiente, probar que funciona en runtime (export con source-maps, probar
  el endpoint real, etc.). Ya hubo casos donde "compila" no significaba
  "funciona" (ver gotchas de Metro abajo).
- **Decisiones de arquitectura importantes → presentar alternativas + una
  recomendación justificada**, usar preguntas explícitas cuando la decisión
  es genuinamente de producto/negocio (traducción bíblica, enfoque editorial,
  dónde hostear, etc.). Decisiones técnicas triviales/reversibles: explicar
  brevemente y proceder sin bloquear.
- Explicar el "por qué" de lo mobile-específico (Expo Go vs dev builds, SDK
  versioning, EAS Build, etc.) con más detalle del que se le daría a alguien
  con experiencia mobile previa — todo eso es territorio nuevo para él.

## Stack

- **Mobile** (`apps/mobile`): React Native + Expo SDK 54 + TypeScript, Expo
  Router, TanStack Query, StyleSheet (no NativeWind/Tailwind).
- **Admin** (`apps/admin`): React + Vite + TypeScript, Firebase Auth
  (Email/Password, un solo usuario: eleal.escobar@gmail.com).
- **Backend** (`backend/`): FastAPI + SQLAlchemy 2.0 + Alembic + PostgreSQL.
- **Compartido** (`packages/shared`): tipos TS compartidos entre mobile/admin.
- **Infra:** Railway (backend + Postgres + admin, 3 servicios en el proyecto
  `diligent-reflection`), Firebase (solo Auth del admin, Storage NO se usa —
  exige plan pago Blaze).

## Decisiones de producto clave (con el porqué)

- **Traducción bíblica: RVA1909** (dominio público), no RVR1960/NVI — evita
  negociar licencia comercial antes de lanzar. Extraída del dump SQL en
  github.com/iglesianazaret/biblia-reina-valera-1909-base-datos-sql, nunca
  transcrita de memoria (exactitud del texto sagrado).
- **Enfoque editorial: interdenominacional general** por defecto (máximo
  alcance, mínima fricción doctrinal).
- **Diferenciador del producto: la reflexión, no solo el versículo** —
  propuesta original de Erick. Reflexiones con voz editorial propia,
  eventualmente borradores con IA + revisión humana **obligatoria** (nunca
  auto-publicado). Por esto `Reflections.status` tiene
  `draft/ai_generated/reviewed/published`, y `/daily-verse` + `/history`
  filtran por `status == "published"` — si esto no aparece en el código,
  es un bug de seguridad de contenido, no una feature faltante.
- **Identidad anónima desde el día 1** (`Users.is_anonymous`, UUID generado
  en el dispositivo, header `X-Device-Id`) en vez de auth real para usuarios
  finales. Permite favoritos/settings sin cuenta.
- Se descartó pivotar a "motivación genérica" por miedo a licencias de texto
  bíblico — resuelto con la traducción de dominio público, no abandonando
  el nicho (más defendible que el mercado saturado de frases motivacionales).

## Infraestructura

- Backend: `https://versiculo-diario-production.up.railway.app`, proyecto
  Railway `diligent-reflection`, servicios `versiculo-diario` + `Postgres`.
  Deploy automático por `git push` (Root Directory = `backend` en el
  dashboard). Ver gotchas de deploy abajo antes de desplegar manualmente.
- Admin: `https://passionate-determination-production.up.railway.app`,
  mismo proyecto Railway, servicio propio. Root Directory = raíz del repo
  (NO `apps/admin` — depende de `packages/shared` vía pnpm workspace, se
  rompe si Railway no ve el resto del monorepo). Build/Start override en
  el dashboard: `pnpm install --frozen-lockfile && pnpm --filter admin
  build` / `pnpm --filter admin exec serve -s dist -l $PORT`. Variable
  `NIXPACKS_NODE_VERSION=22.13.0` puesta a propósito — mismo motivo que el
  gotcha de EAS Build (pnpm 11 necesita Node ≥22.13, si no truena con
  `node:sqlite`). El backend tiene el dominio del admin en
  `CORSMiddleware.allow_origins` (`backend/app/main.py`) — si se regenera
  el dominio de Railway, hay que actualizar esa lista y redesplegar.
- Firebase (`versiculo-diario-1e43b`) solo Auth del admin. Verificación de
  tokens **liviana** (PyJWT + certs públicos de Google,
  `backend/app/firebase_verify.py`) — **NO usar el SDK `firebase-admin`**,
  tumbó producción en Railway (ver gotchas abajo). Config:
  `FIREBASE_PROJECT_ID` en `backend/.env` (no es secreto).
- `QuoteImages` (fondos para compartir) gestionados en el admin pegando URLs
  externas, no upload — Firebase Storage exige plan pago. Mobile usa 3 fondos
  fijos empaquetados (`apps/mobile/assets/share-backgrounds/`).

## Gotchas técnicos (no revertir estos fixes sin releer el porqué)

### pnpm + Expo/React Native monorepo

1. **Dependencias fantasma de Expo/RN** — muchos paquetes de Expo asumen
   hoisting npm/yarn clásico. Fix: `.npmrc` raíz con `shamefully-hoist=true`.
2. **Metro necesita hierarchical lookup activo con pnpm** — NO poner
   `disableHierarchicalLookup = true` en `apps/mobile/metro.config.js` (la
   guía oficial de Expo lo sugiere pero rompe con pnpm).
3. **Dos copias de React (admin 19.2.x, mobile 19.1.x)** causaban "Invalid
   hook call" en runtime. Fix real: `resolver.resolveRequest` en
   `metro.config.js` interceptando `react`/`react-native` hacia la copia
   propia de `apps/mobile/node_modules`. Verificar con `expo export
   --platform android --source-maps` — en el `.map` debe aparecer solo UNA
   ruta `node_modules/react/index.js`.
4. **Expo Go va detrás del último SDK** — proyecto fijado a SDK 54 (no 57)
   porque el build de Expo Go para SDKs nuevos tarda días/semanas en pasar
   revisión de tiendas.
5. **EAS Build necesita Node 22.13+ explícito** — pnpm 11.13.0 usa
   `node:sqlite` internamente, requiere Node ≥22.13. La imagen default de
   EAS Android trae Node 20.19.4 → falla con `ERR_UNKNOWN_BUILTIN_MODULE`.
   Fix: `"node": "22.13.0"` en cada perfil de `apps/mobile/eas.json`.
6. **"Hoy" para `/daily-verse` y `/history` se calcula en `America/Bogota`
   fijo**, no en UTC — ver `backend/app/core/dates.py` (`today()`). Antes
   usaba `datetime.now(timezone.utc).date()`, lo cual causó un 404 real en
   producción: a las 21:50 hora Colombia el servidor ya marcaba "mañana" en
   UTC, dejando sin publicar el contenido que Erick sí había revisado para
   "hoy". Decisión explícita de Erick (audiencia esperada en Latam) sobre
   usar zona fija en vez de UTC o timezone por dispositivo — no revertir a
   UTC sin volver a plantear esa decisión.
7. **Google Play Protect bloquea el APK de `eas build --profile preview`
   al instalarlo** — normal, no es un problema del build. Cualquier APK
   fuera de la Play Store sin "reputación" (paquete nunca visto antes en
   ningún dispositivo) se bloquea por defecto. Fix en el dispositivo: en la
   pantalla de bloqueo, menú "⋮" → "Instalar de todos modos"; o Play Store →
   perfil → Play Protect → ⚙️ → desactivar "Analizar apps con Play Protect"
   temporalmente. Desaparece solo cuando la app esté publicada en Play
   Store (aunque sea en pista interna).

### Deploy en Railway

1. **`railway up` siempre desde la raíz del repo, no desde `backend/`** —
   Root Directory=`backend` está configurado en el dashboard; correr desde
   `backend/` hace que Railway busque `backend/backend` y falle.
2. **Cada carpeta tiene su propio link de Railway** — antes de un primer
   `railway up` desde un directorio nuevo, correr `railway status` para
   confirmar que está linkeado al proyecto correcto. Si no, `railway link
   --project 7c87e905-cafb-4ac0-a40d-d792f5c3eb0d --environment production
   --service versiculo-diario`. Correr `railway up` sin link crea un
   proyecto duplicado en vez de fallar/preguntar.
3. **`firebase-admin` (Python) tumbó producción** (OOM silencioso, sin logs
   de crash) por sus dependencias pesadas (grpcio, google-cloud-*). No
   reinstalar — usar `backend/app/firebase_verify.py`.
4. **`railway status`/`railway logs` pueden mostrar el último deploy
   EXITOSO, no el más reciente** — para ver el estado real:
   `railway deployment list --service versiculo-diario` o
   `railway logs --latest`.

## Estado del roadmap (13 fases)

**Cerradas:** 1 (monorepo) · 2 (modelo de datos + `/daily-verse`) · 3 (app
Expo consumiendo backend real) · 4 (sistema de diseño) · 5 (favoritos +
historial + identidad anónima) · 6 (notificación local + Ajustes) · 7
(compartir como imagen) · 8 (modo oscuro) · 9 (panel admin completo) · 10
(30 días de contenido sembrado, `scripts/seed_content.py`, 2026-07-15 a
2026-08-13).

**⚠️ Pendiente recurrente de Fase 10:** las 29 reflexiones sembradas están en
`status="ai_generated"`, NO publicadas. Erick debe revisarlas y publicarlas
una por una en el admin (`/reflections`) antes de que llegue cada fecha, o
`/daily-verse` devuelve 404 ese día. Juan 3:16 (2026-07-16) ya está publicado
y tiene un favorito real de prueba apuntándole — no tocar esa fila sin
revisar que no rompa el favorito.

**En curso — Fase 11** (identidad de app + publicación):
- ✅ Nombre "Versículo Diario", ícono real, `bundleIdentifier`/`package`
  `com.erickleal.versiculodiario`, splash screen.
- ✅ Política de privacidad en `GET /privacy` (backend).
- ✅ Proyecto EAS vinculado (`projectId` en `app.json`, owner
  `ericklealescobar`), `apps/mobile/eas.json` con perfiles `preview` y
  `production`.
- ✅ Build preview (APK) exitoso — build
  `0290df30-bcd6-4115-acf4-0a0a0f4dd219` en
  expo.dev/accounts/ericklealescobar/projects/versiculo-diario/builds/0290df30-bcd6-4115-acf4-0a0a0f4dd219.
  (El primer intento, `24ad2bfe...`, compiló bien pero crasheaba al abrir:
  `EXPO_PUBLIC_API_URL` no estaba disponible en el build de EAS porque solo
  vivía en el `.env` local, que no se sube al servidor de build. Fix:
  bloque `"env"` con esa variable agregado a cada perfil de
  `apps/mobile/eas.json` — es pública, queda inline en el bundle igual, no
  hay problema de seguridad en tenerla ahí.)
  Si un build futuro falla, diagnosticar vía `eas build:view <id> --json` →
  URL firmada de GCS en `logFiles` → `curl` → puede venir comprimido en
  brotli (paquete `brotli` de Python ya instalado en `backend/.venv` si hace
  falta descomprimir manualmente).
- 🔄 Pendiente: Erick instalando el APK en su Android físico y probándolo
  como build nativo real (primera vez fuera de Expo Go) — golden path
  (versículo del día, favorito, historial, compartir imagen, modo oscuro,
  notificación) y reportar si algo se ve distinto a Expo Go.
- Pendiente después: build de producción (`--profile production`, AAB) y
  envío a Google Play Console (ficha de tienda, screenshots, cuestionario de
  clasificación de contenido, formulario de seguridad de datos — ya
  informado por la política de privacidad escrita).

**No iniciado:** publicación en App Store (iOS) — explícitamente pospuesta,
también requiere EAS Build porque Windows no puede compilar iOS localmente.

## Scripts útiles

- `scripts/seed_content.py` — siembra versículos+reflexiones (detecta y
  nunca sobrescribe fechas con favoritos reales apuntándolas).
- `scripts/generate_app_icon.py` — genera assets de ícono/splash con PIL.
- `scripts/generate_share_backgrounds.py` — genera los 3 fondos fijos de
  "compartir como imagen".
