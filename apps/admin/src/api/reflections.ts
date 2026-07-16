import { apiDelete, apiGet, apiPost, apiPut } from "../lib/api";
import type { AdminVerse } from "./verses";

export type ReflectionStatus = "draft" | "ai_generated" | "reviewed" | "published";
export type ReflectionSource = "human" | "ai_assisted";

export interface AdminReflection {
  id: number;
  verse_id: number;
  verse: AdminVerse;
  title: string | null;
  body: string;
  status: ReflectionStatus;
  source: ReflectionSource;
  author_name: string | null;
  reviewed_by: string | null;
  created_at: string;
  updated_at: string;
}

export interface ReflectionInput {
  verse_id: number;
  title: string | null;
  body: string;
  status: ReflectionStatus;
  source: ReflectionSource;
  author_name: string | null;
}

export const listReflections = () => apiGet<AdminReflection[]>("/admin/reflections");
export const createReflection = (payload: ReflectionInput) =>
  apiPost<AdminReflection>("/admin/reflections", payload);
export const updateReflection = (id: number, payload: Partial<ReflectionInput>) =>
  apiPut<AdminReflection>(`/admin/reflections/${id}`, payload);
export const deleteReflection = (id: number) => apiDelete(`/admin/reflections/${id}`);
