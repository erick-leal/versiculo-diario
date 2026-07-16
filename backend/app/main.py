from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import admin, daily_verse, favorites, history, settings

app = FastAPI(title="Versiculo Diario API")

# El panel admin corre en el navegador (a diferencia de la app movil, que no
# aplica CORS). Restringido a origenes conocidos, no wildcard - se agrega el
# dominio real cuando el admin este desplegado (Fase 11).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(daily_verse.router)
app.include_router(favorites.router)
app.include_router(history.router)
app.include_router(settings.router)
app.include_router(admin.router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
