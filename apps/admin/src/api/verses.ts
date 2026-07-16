import { apiDelete, apiGet, apiPost, apiPut } from "../lib/api";

export interface AdminVerse {
  id: number;
  book: string;
  chapter: number;
  verse_start: number;
  verse_end: number | null;
  reference: string;
  text: string;
  translation: string;
  created_at: string;
}

export interface VerseInput {
  book: string;
  chapter: number;
  verse_start: number;
  verse_end: number | null;
  text: string;
  translation: string;
}

export const listVerses = () => apiGet<AdminVerse[]>("/admin/verses");
export const createVerse = (payload: VerseInput) => apiPost<AdminVerse>("/admin/verses", payload);
export const updateVerse = (id: number, payload: Partial<VerseInput>) =>
  apiPut<AdminVerse>(`/admin/verses/${id}`, payload);
export const deleteVerse = (id: number) => apiDelete(`/admin/verses/${id}`);
