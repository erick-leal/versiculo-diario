import { useEffect, useState, type FormEvent } from "react";

import {
  createQuoteImage,
  deleteQuoteImage,
  listQuoteImages,
  setQuoteImageActive,
  type AdminQuoteImage,
} from "../api/quoteImages";

export function Media() {
  const [images, setImages] = useState<AdminQuoteImage[]>([]);
  const [loading, setLoading] = useState(true);
  const [urlInput, setUrlInput] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const load = () => {
    setLoading(true);
    listQuoteImages()
      .then(setImages)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  };

  useEffect(load, []);

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      await createQuoteImage(urlInput);
      setUrlInput("");
      load();
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err));
    } finally {
      setSubmitting(false);
    }
  };

  const toggleActive = async (image: AdminQuoteImage) => {
    setError(null);
    try {
      await setQuoteImageActive(image.id, !image.is_active);
      load();
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err));
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm("¿Borrar este fondo?")) return;
    setError(null);
    try {
      await deleteQuoteImage(id);
      load();
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err));
    }
  };

  return (
    <div className="verses-page">
      <h1>Fondos para compartir</h1>
      <p className="verse-translation">
        Todavía no hay subida de archivos (ver nota en el commit) — pegá la URL de una imagen ya
        alojada en otro lado.
      </p>

      <form className="verse-form" onSubmit={handleSubmit}>
        <label>
          URL de la imagen
          <input
            type="url"
            value={urlInput}
            onChange={(e) => setUrlInput(e.target.value)}
            placeholder="https://..."
            required
          />
        </label>
        {error && <p className="verse-form-error">{error}</p>}
        <div className="verse-form-actions">
          <button type="submit" disabled={submitting}>
            Agregar fondo
          </button>
        </div>
      </form>

      {loading && <p>Cargando...</p>}

      {!loading && (
        <div className="media-grid">
          {images.map((image) => (
            <div key={image.id} className="media-card">
              <img src={image.image_url} alt="" className="media-thumb" />
              <div className="media-card-actions">
                <label className="media-active-toggle">
                  <input
                    type="checkbox"
                    checked={image.is_active}
                    onChange={() => toggleActive(image)}
                  />
                  Activo
                </label>
                <button onClick={() => handleDelete(image.id)}>Eliminar</button>
              </div>
            </div>
          ))}
          {images.length === 0 && <p>No hay fondos todavía.</p>}
        </div>
      )}
    </div>
  );
}
