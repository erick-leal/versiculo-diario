import { apiDelete, apiGet, apiPost, apiPut } from "../lib/api";

export interface AdminQuoteImage {
  id: number;
  image_url: string;
  is_active: boolean;
  created_at: string;
}

export const listQuoteImages = () => apiGet<AdminQuoteImage[]>("/admin/quote-images");
export const createQuoteImage = (imageUrl: string) =>
  apiPost<AdminQuoteImage>("/admin/quote-images", { image_url: imageUrl });
export const setQuoteImageActive = (id: number, isActive: boolean) =>
  apiPut<AdminQuoteImage>(`/admin/quote-images/${id}`, { is_active: isActive });
export const deleteQuoteImage = (id: number) => apiDelete(`/admin/quote-images/${id}`);
