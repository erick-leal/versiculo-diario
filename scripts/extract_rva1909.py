"""Extrae el texto exacto de una lista de referencias desde el dump SQL de la
RVA1909 (github.com/iglesianazaret/biblia-reina-valera-1909-base-datos-sql,
dominio publico). Asi el texto biblico nunca se transcribe de memoria.

Uso:
    python scripts/extract_rva1909.py <ruta a data.sql> <refs.txt> <salida.json>

refs.txt: una referencia por linea, "<Libro> <cap>:<verso>[-<verso_fin>]",
con el nombre moderno del libro tal como aparece en la tabla books del dump.
Lineas vacias o que empiezan con # se ignoran.

Valida ademas que ninguna referencia ya exista en los lotes anteriores
(seed_content.py, seed_content_batch2.py) ni este repetida en refs.txt.
"""

import json
import re
import sys
from pathlib import Path

BOOK_ROW = re.compile(r"^\s*\((\d+), '((?:[^']|'')*)', '((?:[^']|'')*)', [01]\)")
VERSE_ROW = re.compile(r"^\s*\((\d+), (\d+), (\d+), '((?:[^']|'')*)'\)")
REF = re.compile(r"^(.+) (\d+):(\d+)(?:-(\d+))?$")
EXISTING_REF = re.compile(r'^\s+\("[^"]+", \d+, \d+, (?:\d+|None), "([^"]+)"')

SCRIPTS_DIR = Path(__file__).resolve().parent


def load_dump(path: Path) -> tuple[dict[str, int], dict[tuple[int, int, int], str]]:
    books: dict[str, int] = {}
    verses: dict[tuple[int, int, int], str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if m := VERSE_ROW.match(line):
            book_id, chapter, verse, text = m.groups()
            verses[(int(book_id), int(chapter), int(verse))] = text.replace("''", "'")
        elif m := BOOK_ROW.match(line):
            books[m.group(3).replace("''", "'")] = int(m.group(1))
    return books, verses


def existing_references() -> set[str]:
    refs: set[str] = set()
    for name in ("seed_content.py", "seed_content_batch2.py"):
        for line in (SCRIPTS_DIR / name).read_text(encoding="utf-8").splitlines():
            if m := EXISTING_REF.match(line):
                refs.add(m.group(1))
    return refs


def main(dump_path: str, refs_path: str, out_path: str) -> None:
    books, verses = load_dump(Path(dump_path))
    existing = existing_references()
    seen: set[str] = set()
    errors: list[str] = []
    out = []

    for raw in Path(refs_path).read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        m = REF.match(line)
        if not m:
            errors.append(f"Formato invalido: {line!r}")
            continue
        book, chapter, vstart, vend = m.group(1), int(m.group(2)), int(m.group(3)), m.group(4)
        vend = int(vend) if vend else None
        if line in existing:
            errors.append(f"Ya existe en un lote anterior: {line}")
        if line in seen:
            errors.append(f"Repetida en refs.txt: {line}")
        seen.add(line)
        book_id = books.get(book)
        if book_id is None:
            errors.append(f"Libro desconocido en el dump: {book!r}")
            continue
        parts = []
        for v in range(vstart, (vend or vstart) + 1):
            text = verses.get((book_id, chapter, v))
            if text is None:
                errors.append(f"No existe en el dump: {book} {chapter}:{v}")
            else:
                parts.append(text)
        out.append({
            "book": book,
            "chapter": chapter,
            "verse_start": vstart,
            "verse_end": vend,
            "reference": line,
            "text": " ".join(parts),
        })

    if errors:
        print("\n".join(errors))
        sys.exit(1)

    Path(out_path).write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"OK: {len(out)} referencias extraidas a {out_path}")


if __name__ == "__main__":
    main(*sys.argv[1:4])
