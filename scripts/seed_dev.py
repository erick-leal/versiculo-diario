"""Asegura que exista una entrada de daily_verses para hoy y mañana (UTC),
para poder probar /daily-verse en desarrollo sin pisar el contenido si ya existe.
"""

import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app.database import SessionLocal
from app.models import DailyVerse, Reflection, Verse

db = SessionLocal()

verse = db.query(Verse).filter(Verse.reference == "Juan 3:16").first()
if verse is None:
    verse = Verse(
        book="Juan",
        chapter=3,
        verse_start=16,
        verse_end=None,
        reference="Juan 3:16",
        text=(
            "Porque de tal manera amo Dios al mundo, que ha dado a su Hijo unigenito, "
            "para que todo aquel que en el cree, no se pierda, mas tenga vida eterna."
        ),
        translation="RVA1909",
    )
    db.add(verse)
    db.flush()

reflection = db.query(Reflection).filter(Reflection.verse_id == verse.id).first()
if reflection is None:
    reflection = Reflection(
        verse_id=verse.id,
        title="Un amor que no se mide en merecimientos",
        body=(
            "Este versiculo no describe una transaccion, describe una decision. "
            "Dios no amo al mundo porque el mundo lo mereciera, lo amo porque asi es Su naturaleza. "
            "Hoy, si sientes que no has hecho lo suficiente para merecer nada, recuerda que ese "
            "amor nunca dependio de eso."
        ),
        status="published",
        source="human",
        author_name="Equipo Versiculo Diario",
    )
    db.add(reflection)
    db.flush()

today = datetime.now(timezone.utc).date()
for offset in (0, 1):
    target_date = today + timedelta(days=offset)
    exists = db.query(DailyVerse).filter(DailyVerse.date == target_date).first()
    if exists:
        print(f"Ya existe entrada para {target_date}, no se toca.")
        continue
    db.add(DailyVerse(date=target_date, verse_id=verse.id, reflection_id=reflection.id))
    print(f"Sembrado: {verse.reference} programado para {target_date} (UTC)")

db.commit()
