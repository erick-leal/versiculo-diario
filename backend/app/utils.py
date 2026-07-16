def build_verse_reference(book: str, chapter: int, verse_start: int, verse_end: int | None) -> str:
    if verse_end and verse_end != verse_start:
        return f"{book} {chapter}:{verse_start}-{verse_end}"
    return f"{book} {chapter}:{verse_start}"
