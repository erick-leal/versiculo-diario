"""Llena automaticamente los proximos dias sin DailyVerse tomando reflexiones
en status="reviewed" (ya aprobadas por Erick en el admin, pendientes de
fecha). Pensado para correr a diario desde un Railway Cron Job — reemplaza
la asignacion manual de fecha por fecha en el calendario del admin.

Idempotente: si un dia del rango ya tiene DailyVerse, se salta. Evita repetir
una reflexion que ya se uso en los ultimos REPEAT_COOLDOWN_DAYS dias.

Orden de preferencia al elegir la reflexion de un dia:
  1. Una "reviewed" nueva (nunca programada).
  2. Si no quedan: reutilizar una "published" (ya revisada por un humano,
     asi que no rompe la regla de revision obligatoria) que no se haya usado
     en los ultimos REPEAT_COOLDOWN_DAYS dias, priorizando la que se uso
     hace mas tiempo.
  3. Si todas se usaron dentro del cooldown: la "published" usada hace mas
     tiempo, aunque sea reciente. Mejor repetir que dejar /daily-verse en 404.
Nunca toma contenido "draft" ni "ai_generated".

Termina con exit code 1 si algun dia queda sin contenido, para que Railway
marque la ejecucion como fallida (antes salia con 0 y el cron aparecia como
"succeeded" mientras la app devolvia 404 — paso del 12 al 23 de nov 2026).

Se ejecuta como modulo (python -m scripts.auto_schedule_verse) con cwd=backend/,
igual que el resto de comandos de este servicio (uvicorn, alembic).
"""

import sys
from datetime import timedelta

from sqlalchemy import func

from app.core.dates import today
from app.database import SessionLocal
from app.models import DailyVerse, Reflection

BUFFER_DAYS = 3
REPEAT_COOLDOWN_DAYS = 90
LOW_POOL_WARNING = 7


def pick_reflection(db, already_picked_ids: set[int]) -> tuple[Reflection | None, str]:
    cutoff = today() - timedelta(days=REPEAT_COOLDOWN_DAYS)
    recently_used_ids = {
        row[0]
        for row in db.query(DailyVerse.reflection_id).filter(DailyVerse.date >= cutoff)
    }
    excluded = recently_used_ids | already_picked_ids

    # 1. Contenido nuevo, revisado y nunca programado.
    candidate = (
        db.query(Reflection)
        .filter(Reflection.status == "reviewed", ~Reflection.id.in_(excluded))
        .order_by(func.random())
        .first()
    )
    if candidate is not None:
        return candidate, "nueva"

    # 2/3. Reutilizar publicadas, empezando por la que se uso hace mas tiempo.
    # Las "published" sin DailyVerse (publicadas a mano sin fecha) quedan
    # primero por nulls_first: nunca se mostraron como versiculo del dia.
    last_used = func.max(DailyVerse.date)
    rows = (
        db.query(Reflection, last_used)
        .outerjoin(DailyVerse, DailyVerse.reflection_id == Reflection.id)
        .filter(Reflection.status == "published", ~Reflection.id.in_(already_picked_ids))
        .group_by(Reflection.id)
        .order_by(last_used.asc().nulls_first(), func.random())
        .all()
    )
    for reflection, _ in rows:
        if reflection.id not in recently_used_ids:
            return reflection, "reutilizada"
    if rows:
        return rows[0][0], "reutilizada (dentro del cooldown, pool chico)"
    return None, ""


def main() -> int:
    db = SessionLocal()
    try:
        start = today()
        dates_needed = [start + timedelta(days=offset) for offset in range(BUFFER_DAYS)]

        existing_dates = {
            row[0]
            for row in db.query(DailyVerse.date).filter(DailyVerse.date.in_(dates_needed))
        }
        missing_dates = [d for d in dates_needed if d not in existing_dates]

        failed = False
        picked_ids: set[int] = set()
        for target_date in missing_dates:
            reflection, source = pick_reflection(db, picked_ids)
            if reflection is None:
                print(
                    f"❌ No hay reflexiones 'reviewed' ni 'published' para asignar a {target_date}. "
                    "Revisa y aprueba contenido en el admin (/reflections)."
                )
                failed = True
                break

            picked_ids.add(reflection.id)
            db.add(DailyVerse(date=target_date, verse_id=reflection.verse_id, reflection_id=reflection.id))
            reflection.status = "published"
            print(f"{target_date}: reflexión #{reflection.id} (verso #{reflection.verse_id}) [{source}]")

        db.commit()

        if not missing_dates:
            print("Nada que hacer: el colchón de días ya está completo.")

        remaining = db.query(Reflection).filter(Reflection.status == "reviewed").count()
        if remaining < LOW_POOL_WARNING:
            print(
                f"⚠️ Quedan {remaining} reflexiones 'reviewed' sin usar. Se están reutilizando "
                "reflexiones ya publicadas — revisa más contenido nuevo en el admin."
            )

        return 1 if failed else 0
    finally:
        db.close()


if __name__ == "__main__":
    sys.exit(main())
