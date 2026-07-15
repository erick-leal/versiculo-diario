from fastapi import FastAPI

from app.routers import daily_verse

app = FastAPI(title="Versiculo Diario API")
app.include_router(daily_verse.router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
