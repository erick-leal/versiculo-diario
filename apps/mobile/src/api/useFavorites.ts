import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import type { FavoriteOut } from "@versiculo-diario/shared";

import { apiDelete, apiGet, apiPost } from "./client";

const FAVORITES_KEY = ["favorites"];

export function useFavorites() {
  return useQuery({
    queryKey: FAVORITES_KEY,
    queryFn: () => apiGet<FavoriteOut[]>("/favorites", true),
  });
}

export function useAddFavorite() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (dailyVerseId: number) =>
      apiPost<FavoriteOut>("/favorites", { daily_verse_id: dailyVerseId }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: FAVORITES_KEY });
    },
  });
}

export function useRemoveFavorite() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (favoriteId: number) => apiDelete(`/favorites/${favoriteId}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: FAVORITES_KEY });
    },
  });
}
