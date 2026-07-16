import { useEffect, useState, type FormEvent } from "react";

import {
  createReflection,
  deleteReflection,
  listReflections,
  updateReflection,
  type AdminReflection,
  type ReflectionInput,
  type ReflectionSource,
  type ReflectionStatus,
} from "../api/reflections";
import { listVerses, type AdminVerse } from "../api/verses";

const STATUS_LABELS: Record<ReflectionStatus, string> = {
  draft: "Borrador",
  ai_generated: "Generado con IA",
  reviewed: "Revisado",
  published: "Publicado",
};

const SOURCE_LABELS: Record<ReflectionSource, string> = {
  human: "Humano",
  ai_assisted: "Asistido por IA",
};

function emptyForm(defaultVerseId: number): ReflectionInput {
  return {
    verse_id: defaultVerseId,
    title: "",
    body: "",
    status: "draft",
    source: "human",
    author_name: "",
  };
}

export function Reflections() {
  const [reflections, setReflections] = useState<AdminReflection[]>([]);
  const [verses, setVerses] = useState<AdminVerse[]>([]);
  const [loading, setLoading] = useState(true);
  const [form, setForm] = useState<ReflectionInput>(emptyForm(0));
  const [editingId, setEditingId] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const load = () => {
    setLoading(true);
    Promise.all([listReflections(), listVerses()])
      .then(([reflectionsData, versesData]) => {
        setReflections(reflectionsData);
        setVerses(versesData);
        if (!editingId && versesData.length > 0) {
          setForm((f) => (f.verse_id ? f : { ...f, verse_id: versesData[0].id }));
        }
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  };

  useEffect(load, []);

  const startEdit = (reflection: AdminReflection) => {
    setEditingId(reflection.id);
    setForm({
      verse_id: reflection.verse_id,
      title: reflection.title ?? "",
      body: reflection.body,
      status: reflection.status,
      source: reflection.source,
      author_name: reflection.author_name ?? "",
    });
  };

  const cancelEdit = () => {
    setEditingId(null);
    setForm(emptyForm(verses[0]?.id ?? 0));
  };

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    setError(null);
    setSubmitting(true);
    const payload: ReflectionInput = {
      ...form,
      title: form.title || null,
      author_name: form.author_name || null,
    };
    try {
      if (editingId) {
        await updateReflection(editingId, payload);
      } else {
        await createReflection(payload);
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
    if (!confirm("¿Borrar esta reflexión?")) return;
    setError(null);
    try {
      await deleteReflection(id);
      load();
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err));
    }
  };

  return (
    <div className="verses-page">
      <h1>Reflexiones</h1>

      <form className="verse-form" onSubmit={handleSubmit}>
        <div className="verse-form-row">
          <label>
            Versículo
            <select
              value={form.verse_id}
              onChange={(e) => setForm({ ...form, verse_id: Number(e.target.value) })}
              required
            >
              {verses.map((v) => (
                <option key={v.id} value={v.id}>
                  {v.reference}
                </option>
              ))}
            </select>
          </label>
          <label>
            Título (opcional)
            <input
              value={form.title ?? ""}
              onChange={(e) => setForm({ ...form, title: e.target.value })}
            />
          </label>
        </div>

        <label>
          Texto
          <textarea
            rows={4}
            value={form.body}
            onChange={(e) => setForm({ ...form, body: e.target.value })}
            required
          />
        </label>

        <div className="verse-form-row">
          <label className="verse-form-narrow">
            Estado
            <select
              value={form.status}
              onChange={(e) => setForm({ ...form, status: e.target.value as ReflectionStatus })}
            >
              {Object.entries(STATUS_LABELS).map(([value, label]) => (
                <option key={value} value={value}>
                  {label}
                </option>
              ))}
            </select>
          </label>
          <label className="verse-form-narrow">
            Origen
            <select
              value={form.source}
              onChange={(e) => setForm({ ...form, source: e.target.value as ReflectionSource })}
            >
              {Object.entries(SOURCE_LABELS).map(([value, label]) => (
                <option key={value} value={value}>
                  {label}
                </option>
              ))}
            </select>
          </label>
          <label>
            Autor (opcional)
            <input
              value={form.author_name ?? ""}
              onChange={(e) => setForm({ ...form, author_name: e.target.value })}
            />
          </label>
        </div>

        {error && <p className="verse-form-error">{error}</p>}

        <div className="verse-form-actions">
          <button type="submit" disabled={submitting || verses.length === 0}>
            {editingId ? "Guardar cambios" : "Crear reflexión"}
          </button>
          {editingId && (
            <button type="button" className="verse-form-cancel" onClick={cancelEdit}>
              Cancelar
            </button>
          )}
        </div>
        {verses.length === 0 && <p>Creá al menos un versículo primero.</p>}
      </form>

      {loading && <p>Cargando...</p>}

      {!loading && (
        <ul className="verse-list">
          {reflections.map((reflection) => (
            <li key={reflection.id} className="verse-item">
              <div>
                <strong>{reflection.verse.reference}</strong>{" "}
                <span className="verse-translation">
                  {STATUS_LABELS[reflection.status]} · {SOURCE_LABELS[reflection.source]}
                  {reflection.reviewed_by ? ` · revisado por ${reflection.reviewed_by}` : ""}
                </span>
                {reflection.title && <p className="verse-text"><strong>{reflection.title}</strong></p>}
                <p className="verse-text">{reflection.body}</p>
              </div>
              <div className="verse-item-actions">
                <button onClick={() => startEdit(reflection)}>Editar</button>
                <button onClick={() => handleDelete(reflection.id)}>Eliminar</button>
              </div>
            </li>
          ))}
          {reflections.length === 0 && <p>No hay reflexiones todavía.</p>}
        </ul>
      )}
    </div>
  );
}
