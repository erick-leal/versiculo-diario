from fastapi import FastAPI

from app.routers import daily_verse, favorites, history, settings

app = FastAPI(title="Versiculo Diario API")
app.include_router(daily_verse.router)
app.include_router(favorites.router)
app.include_router(history.router)
app.include_router(settings.router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
