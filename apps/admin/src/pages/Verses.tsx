import { useEffect, useState, type FormEvent } from "react";

import {
  createVerse,
  deleteVerse,
  listVerses,
  updateVerse,
  type AdminVerse,
  type VerseInput,
} from "../api/verses";

const EMPTY_FORM: VerseInput = {
  book: "",
  chapter: 1,
  verse_start: 1,
  verse_end: null,
  text: "",
  translation: "RVA1909",
};

export function Verses() {
  const [verses, setVerses] = useState<AdminVerse[]>([]);
  const [loading, setLoading] = useState(true);
  const [form, setForm] = useState<VerseInput>(EMPTY_FORM);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const load = () => {
    setLoading(true);
    listVerses()
      .then(setVerses)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  };

  useEffect(load, []);

  const startEdit = (verse: AdminVerse) => {
    setEditingId(verse.id);
    setForm({
      book: verse.book,
      chapter: verse.chapter,
      verse_start: verse.verse_start,
      verse_end: verse.verse_end,
      text: verse.text,
      translation: verse.translation,
    });
  };

  const cancelEdit = () => {
    setEditingId(null);
    setForm(EMPTY_FORM);
  };

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      if (editingId) {
        await updateVerse(editingId, form);
      } else {
        await createVerse(form);
      }
      cancelEdit();
      load();
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err));
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm("¿Borrar este versículo?")) return;
    setError(null);
    try {
      await deleteVerse(id);
      load();
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err));
    }
  };

  return (
    <div className="verses-page">
      <h1>Versículos</h1>

      <form className="verse-form" onSubmit={handleSubmit}>
        <div className="verse-form-row">
          <label>
            Libro
            <input
              value={form.book}
              onChange={(e) => setForm({ ...form, book: e.target.value })}
              required
            />
          </label>
          <label className="verse-form-narrow">
            Capítulo
            <input
              type="number"
              min={1}
              value={form.chapter}
              onChange={(e) => setForm({ ...form, chapter: Number(e.target.value) })}
              required
            />
          </label>
          <label className="verse-form-narrow">
            Versículo desde
            <input
              type="number"
              min={1}
              value={form.verse_start}
              onChange={(e) => setForm({ ...form, verse_start: Number(e.target.value) })}
              required
            />
          </label>
          <label className="verse-form-narrow">
            Versículo hasta (opcional)
            <input
              type="number"
              min={1}
              value={form.verse_end ?? ""}
              onChange={(e) =>
                setForm({ ...form, verse_end: e.target.value ? Number(e.target.value) : null })
              }
            />
          </label>
          <label className="verse-form-narrow">
            Traducción
            <input
              value={form.translation}
              onChange={(e) => setForm({ ...form, translation: e.target.value })}
              required
            />
          </label>
        </div>

        <label>
          Texto
          <textarea
            rows={3}
            value={form.text}
            onChange={(e) => setForm({ ...form, text: e.target.value })}
            required
          />
        </label>

        {error && <p className="verse-form-error">{error}</p>}

        <div className="verse-form-actions">
          <button type="submit" disabled={submitting}>
            {editingId ? "Guardar cambios" : "Crear versículo"}
          </button>
          {editingId && (
            <button type="button" className="verse-form-cancel" onClick={cancelEdit}>
              Cancelar
            </button>
          )}
        </div>
      </form>

      {loading && <p>Cargando...</p>}

      {!loading && (
        <ul className="verse-list">
          {verses.map((verse) => (
            <li key={verse.id} className="verse-item">
              <div>
                <strong>{verse.reference}</strong>{" "}
                <span className="verse-translation">({verse.translation})</span>
                <p className="verse-text">{verse.text}</p>
              </div>
              <div className="verse-item-actions">
                <button onClick={() => startEdit(verse)}>Editar</button>
                <button onClick={() => handleDelete(verse.id)}>Eliminar</button>
              </div>
            </li>
          ))}
          {verses.length === 0 && <p>No hay versículos todavía.</p>}
        </ul>
      )}
    </div>
  );
}
