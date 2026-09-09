import os

import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import (
    admin,
    admin_daily_verses,
    admin_quote_images,
    admin_reflections,
    admin_verses,
    daily_verse,
    favorites,
    history,
    personal_reflections,
    privacy,
    settings,
)

# Error tracking: solo se activa si SENTRY_DSN esta seteada (Railway en
# produccion). En dev local, sin la variable, no manda nada. send_default_pii
# se deja en False (default) porque la app es anonima por diseno y la
# politica de privacidad promete "sin rastreo" - no mandamos IP/headers del
# usuario, solo el stack trace y la request (metodo, path, sin body).
if sentry_dsn := os.getenv("SENTRY_DSN"):
    sentry_sdk.init(dsn=sentry_dsn)

app = FastAPI(title="Versiculo Diario API")

# El panel admin corre en el navegador (a diferencia de la app movil, que no
# aplica CORS). Restringido a origenes conocidos, no wildcard.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://passionate-determination-production.up.railway.app",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(daily_verse.router)
app.include_router(favorites.router)
app.include_router(history.router)
app.include_router(settings.router)
app.include_router(personal_reflections.router)
app.include_router(admin.router)
app.include_router(admin_verses.router)
app.include_router(admin_reflections.router)
app.include_router(admin_daily_verses.router)
app.include_router(admin_quote_images.router)
app.include_router(privacy.router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
