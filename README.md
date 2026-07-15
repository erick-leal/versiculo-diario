# Versículo Diario

App móvil para acercar a personas cristianas a la Biblia cada día: un versículo, una reflexión breve, y la posibilidad de guardarlo, compartirlo y recibir un recordatorio diario.

## Stack

- **Mobile:** React Native + Expo + TypeScript
- **Admin (panel de contenido):** React + Vite + TypeScript
- **Backend:** FastAPI (Python)
- **Base de datos:** PostgreSQL (Railway)
- **Notificaciones:** Expo Notifications

## Estructura

```
apps/
  mobile/     App de React Native (Expo) — la app que instalan los usuarios
  admin/      Panel web para gestionar versículos y reflexiones
packages/
  shared/     Tipos y utilidades TypeScript compartidos entre mobile y admin
backend/      API en FastAPI + modelos de datos (SQLAlchemy) + migraciones (Alembic)
database/     Diagrama ER, decisiones de esquema, seed de contenido
docs/         Decisiones de arquitectura (ADRs) y notas de diseño
scripts/      Scripts puntuales de mantenimiento/importación
```

## Desarrollo local

**Mobile:**
```
pnpm install
pnpm mobile
```
Escanea el QR con la app Expo Go en tu celular.

**Admin:**
```
pnpm admin
```

**Backend:**
```
cd backend
.venv/Scripts/activate   # Windows
uvicorn app.main:app --reload
```
