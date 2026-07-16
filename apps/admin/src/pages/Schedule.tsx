import { useEffect, useMemo, useState, type FormEvent } from "react";

import {
  createDailyVerse,
  deleteDailyVerse,
  listDailyVerses,
  updateDailyVerse,
  type AdminDailyVerse,
  type DailyVerseInput,
} from "../api/dailyVerses";
import { listReflections, type AdminReflection } from "../api/reflections";
import { listVerses, type AdminVerse } from "../api/verses";

function todayIso(): string {
  return new Date().toISOString().slice(0, 10);
}

function emptyForm(defaultVerseId: number, defaultReflectionId: number): DailyVerseInput {
  return { date: todayIso(), verse_id: defaultVerseId, reflection_id: defaultReflectionId };
}

export function Schedule() {
  const [entries, setEntries] = useState<AdminDailyVerse[]>([]);
  const [verses, setVerses] = useState<AdminVerse[]>([]);
  const [reflections, setReflections] = useState<AdminReflection[]>([]);
  const [loading, setLoading] = useState(true);
  const [form, setForm] = useState<DailyVerseInput>(emptyForm(0, 0));
  const [editingId, setEditingId] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const load = () => {
    setLoading(true);
    Promise.all([listDailyVerses(), listVerses(), listReflections()])
      .then(([entriesData, versesData, reflectionsData]) => {
        setEntries(entriesData);
        setVerses(versesData);
        setReflections(reflectionsData);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  };

  useEffect(load, []);

  const reflectionsForVerse = useMemo(
    () => reflections.filter((r) => r.verse_id === form.verse_id),
    [reflections, form.verse_id]
  );

  const setVerseId = (verseId: number) => {
    const firstReflection = reflections.find((r) => r.verse_id === verseId);
    setForm((f) => ({ ...f, verse_id: verseId, reflection_id: firstReflection?.id ?? 0 }));
  };

  const startEdit = (entry: AdminDailyVerse) => {
    setEditingId(entry.id);
    setForm({ date: entry.date, verse_id: entry.verse_id, reflection_id: entry.reflection_id });
  };

  const cancelEdit = () => {
    setEditingId(null);
    const firstVerse = verses[0];
    const firstReflection = reflections.find((r) => r.verse_id === firstVerse?.id);
    setForm(emptyForm(firstVerse?.id ?? 0, firstReflection?.id ?? 0));
  };

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      if (editingId) {
        await updateDailyVerse(editingId, form);
      } else {
        await createDailyVerse(form);
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
    if (!confirm("¿Quitar este versículo del calendario?")) return;
    setError(null);
    try {
      await deleteDailyVerse(id);
      load();
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err));
    }
  };

  const noReflectionsForVerse = form.verse_id !== 0 && reflectionsForVerse.length === 0;

  return (
    <div className="verses-page">
      <h1>Calendario</h1>

      <form className="verse-form" onSubmit={handleSubmit}>
        <div className="verse-form-row">
          <label className="verse-form-narrow">
            Fecha
            <input
              type="date"
              value={form.date}
              onChange={(e) => setForm({ ...form, date: e.target.value })}
              required
            />
          </label>
          <label>
            Versículo
            <select
              value={form.verse_id}
              onChange={(e) => setVerseId(Number(e.target.value))}
              required
            >
              <option value={0} disabled>
                Elegí un versículo
              </option>
              {verses.map((v) => (
                <option key={v.id} value={v.id}>
                  {v.reference}
                </option>
              ))}
            </select>
          </label>
          <label>
            Reflexión
            <select
              value={form.reflection_id}
              onChange={(e) => setForm({ ...form, reflection_id: Number(e.target.value) })}
              required
              disabled={noReflectionsForVerse}
            >
              <option value={0} disabled>
                {noReflectionsForVerse ? "Sin reflexiones para este versículo" : "Elegí una reflexión"}
              </option>
              {reflectionsForVerse.map((r) => (
                <option key={r.id} value={r.id}>
                  {r.title || `#${r.id}`} ({r.status})
                </option>
              ))}
            </select>
          </label>
        </div>

        {error && <p className="verse-form-error">{error}</p>}

        <div className="verse-form-actions">
          <button type="submit" disabled={submitting || !form.verse_id || !form.reflection_id}>
            {editingId ? "Guardar cambios" : "Programar"}
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
          {entries.map((entry) => (
            <li key={entry.id} className="verse-item">
              <div>
                <strong>{entry.date}</strong> — {entry.verse.reference}
                <p className="verse-text">{entry.reflection.title || "(sin título)"}</p>
              </div>
              <div className="verse-item-actions">
                <button onClick={() => startEdit(entry)}>Editar</button>
                <button onClick={() => handleDelete(entry.id)}>Quitar</button>
              </div>
            </li>
          ))}
          {entries.length === 0 && <p>No hay nada programado todavía.</p>}
        </ul>
      )}
    </div>
  );
}
