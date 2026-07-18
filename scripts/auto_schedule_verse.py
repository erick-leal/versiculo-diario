"""Llena automaticamente los proximos dias sin DailyVerse tomando reflexiones
en status="reviewed" (ya aprobadas por Erick en el admin, pendientes de
fecha). Pensado para correr a diario desde un Railway Cron Job — reemplaza
la asignacion manual de fecha por fecha en el calendario del admin.

Idempotente: si un dia del rango ya tiene DailyVerse, se salta. Evita repetir
una reflexion que ya se uso en los ultimos MOOD_REPEAT_COOLDOWN_DAYS dias.
"""

import sys
from datetime import timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from sqlalchemy import func

from app.core.dates import today
from app.database import SessionLocal
from app.models import DailyVerse, Reflection

BUFFER_DAYS = 3
REPEAT_COOLDOWN_DAYS = 90


def pick_reflection(db, already_picked_ids: set[int]) -> Reflection | None:
    cutoff = today() - timedelta(days=REPEAT_COOLDOWN_DAYS)
    recently_used_ids = {
        row[0]
        for row in db.query(DailyVerse.reflection_id).filter(DailyVerse.date >= cutoff)
    }
    excluded = recently_used_ids | already_picked_ids

    query = db.query(Reflection).filter(Reflection.status == "reviewed")
    candidate = query.filter(~Reflection.id.in_(excluded)).order_by(func.random()).first()
    if candidate is None:
        # Pool exhausto de reflexiones "frescas": mejor repetir una ya usada
        # que dejar un dia sin contenido (evita 404 en /daily-verse).
        candidate = query.filter(~Reflection.id.in_(already_picked_ids)).order_by(func.random()).first()
    return candidate


def main() -> None:
    db = SessionLocal()
    try:
        start = today()
        dates_needed = [start + timedelta(days=offset) for offset in range(BUFFER_DAYS)]

        existing_dates = {
            row[0]
            for row in db.query(DailyVerse.date).filter(DailyVerse.date.in_(dates_needed))
        }
        missing_dates = [d for d in dates_needed if d not in existing_dates]

        if not missing_dates:
            print("Nada que hacer: el colchón de días ya está completo.")
            return

        picked_ids: set[int] = set()
        for target_date in missing_dates:
            reflection = pick_reflection(db, picked_ids)
            if reflection is None:
                print(
                    f"⚠️ No hay reflexiones en status='reviewed' para asignar a {target_date}. "
                    "Revisa y aprueba más contenido en el admin (/reflections)."
                )
                break

            picked_ids.add(reflection.id)
            db.add(DailyVerse(date=target_date, verse_id=reflection.verse_id, reflection_id=reflection.id))
            reflection.status = "published"
            print(f"{target_date}: asignada reflexión #{reflection.id} (verso #{reflection.verse_id})")

        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    main()
