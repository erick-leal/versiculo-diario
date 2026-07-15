"""Inserta un versiculo, una reflexion y la entrada del dia de hoy para probar el endpoint /daily-verse en desarrollo."""

import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app.database import SessionLocal
from app.models import DailyVerse, Reflection, Verse

db = SessionLocal()

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

daily_verse = DailyVerse(date=date.today(), verse_id=verse.id, reflection_id=reflection.id)
db.add(daily_verse)

db.commit()
print(f"Sembrado: {verse.reference} programado para {daily_verse.date}")
