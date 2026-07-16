import { apiDelete, apiGet, apiPost, apiPut } from "../lib/api";
import type { AdminReflection } from "./reflections";
import type { AdminVerse } from "./verses";

export interface AdminDailyVerse {
  id: number;
  date: string;
  verse_id: number;
  reflection_id: number;
  verse: AdminVerse;
  reflection: AdminReflection;
}

export interface DailyVerseInput {
  date: string;
  verse_id: number;
  reflection_id: number;
}

export const listDailyVerses = () => apiGet<AdminDailyVerse[]>("/admin/daily-verses");
export const createDailyVerse = (payload: DailyVerseInput) =>
  apiPost<AdminDailyVerse>("/admin/daily-verses", payload);
export const updateDailyVerse = (id: number, payload: Partial<DailyVerseInput>) =>
  apiPut<AdminDailyVerse>(`/admin/daily-verses/${id}`, payload);
export const deleteDailyVerse = (id: number) => apiDelete(`/admin/daily-verses/${id}`);
