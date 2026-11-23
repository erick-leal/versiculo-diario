"""Tercer lote de contenido: 245 versiculos (RVA1909, dominio publico) +
reflexiones nuevas. Sumado a los 120 de los lotes 1 y 2 da 365 versiculos
distintos: un ano completo sin repetir.

Igual que seed_content_batch2.py, NO programa fechas: siembra Verse +
Reflection en status="ai_generated". Quedan pendientes de revision humana
en el admin (/reflections) -- al pasarlas a "reviewed", el cron
auto_schedule_verse las programa solo.

Los datos viven en scripts/content_batch3/:
  - refs.txt: las referencias elegidas.
  - verses.json: texto exacto de cada referencia, extraido del dump SQL de la
    RVA1909 con scripts/extract_rva1909.py (nunca transcrito de memoria).
  - reflections_1..5.py: los borradores de reflexion.

Uso (cwd = raiz del repo):
    backend/.venv/Scripts/python scripts/seed_content_batch3.py --check   # solo valida, no toca la DB
    backend/.venv/Scripts/python scripts/seed_content_batch3.py           # siembra
"""

import importlib.util
import json
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
DATA_DIR = SCRIPTS_DIR / "content_batch3"
sys.path.insert(0, str(SCRIPTS_DIR.parent / "backend"))

from app.constants import MOOD_TAGS  # noqa: E402


def load_reflections() -> dict[str, tuple[str, str, list[str]]]:
    merged: dict[str, tuple[str, str, list[str]]] = {}
    for i in range(1, 6):
        path = DATA_DIR / f"reflections_{i}.py"
        spec = importlib.util.spec_from_file_location(f"reflections_{i}", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for ref in module.REFLECTIONS:
            if ref in merged:
                raise SystemExit(f"Reflexión duplicada entre archivos: {ref}")
        merged.update(module.REFLECTIONS)
    return merged


def validate(verses: list[dict], reflections: dict) -> None:
    errors: list[str] = []
    verse_refs = [v["reference"] for v in verses]
    if len(verse_refs) != len(set(verse_refs)):
        errors.append("verses.json tiene referencias repetidas")
    missing = set(verse_refs) - reflections.keys()
    extra = reflections.keys() - set(verse_refs)
    errors += [f"Falta reflexión para {r}" for r in sorted(missing)]
    errors += [f"Reflexión sin versículo en verses.json: {r}" for r in sorted(extra)]
    titles: set[str] = set()
    for ref, (title, body, tags) in reflections.items():
        if not title.strip() or not body.strip():
            errors.append(f"{ref}: título o cuerpo vacío")
        if title in titles:
            errors.append(f"{ref}: título repetido «{title}»")
        titles.add(title)
        if not tags or any(t not in MOOD_TAGS for t in tags):
            errors.append(f"{ref}: mood_tags inválidos {tags}")
        if len(tags) != len(set(tags)):
            errors.append(f"{ref}: mood_tags repetidos {tags}")
    for v in verses:
        if not v["text"].strip():
            errors.append(f"{v['reference']}: texto vacío")
    if errors:
        print("\n".join(errors))
        raise SystemExit(1)


def main() -> None:
    verses = json.loads((DATA_DIR / "verses.json").read_text(encoding="utf-8"))
    reflections = load_reflections()
    validate(verses, reflections)
    print(f"Validación OK: {len(verses)} versículos con su reflexión.")

    if "--check" in sys.argv:
        return

    from app.database import SessionLocal
    from app.models import Reflection, Verse

    db = SessionLocal()
    created_verses = skipped_verses = created_reflections = skipped_reflections = 0
    try:
        verse_by_reference: dict[str, Verse] = {}
        for v in verses:
            verse = db.query(Verse).filter(Verse.reference == v["reference"]).first()
            if verse is None:
                verse = Verse(
                    book=v["book"],
                    chapter=v["chapter"],
                    verse_start=v["verse_start"],
                    verse_end=v["verse_end"],
                    reference=v["reference"],
                    text=v["text"],
                    translation="RVA1909",
                )
                db.add(verse)
                db.flush()
                created_verses += 1
            else:
                skipped_verses += 1
            verse_by_reference[v["reference"]] = verse

        for reference, verse in verse_by_reference.items():
            if db.query(Reflection).filter(Reflection.verse_id == verse.id).first():
                skipped_reflections += 1
                continue
            title, body, mood_tags = reflections[reference]
            db.add(Reflection(
                verse_id=verse.id,
                title=title,
                body=body,
                status="ai_generated",
                source="ai_assisted",
                mood_tags=mood_tags,
            ))
            created_reflections += 1

        db.commit()
    finally:
        db.close()

    print(
        f"Versículos nuevos: {created_verses} (ya existían: {skipped_verses}). "
        f"Reflexiones nuevas: {created_reflections} (ya existían: {skipped_reflections})."
    )
    print(
        "Quedaron en status='ai_generated' -- revísalas y pásalas a 'reviewed' en "
        "el admin (/reflections). El cron las programa solo."
    )


if __name__ == "__main__":
    main()
