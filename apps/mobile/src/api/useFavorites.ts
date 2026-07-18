import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import type { DailyVerseOut, FavoriteOut } from "@versiculo-diario/shared";

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
    mutationFn: (dailyVerse: DailyVerseOut) =>
      apiPost<FavoriteOut>("/favorites", { daily_verse_id: dailyVerse.id }),
    onMutate: async (dailyVerse) => {
      await queryClient.cancelQueries({ queryKey: FAVORITES_KEY });
      const previous = queryClient.getQueryData<FavoriteOut[]>(FAVORITES_KEY);
      if (previous) {
        const optimisticEntry: FavoriteOut = {
          id: -Date.now(),
          created_at: new Date().toISOString(),
          daily_verse: dailyVerse,
        };
        queryClient.setQueryData(FAVORITES_KEY, [optimisticEntry, ...previous]);
      }
      return { previous };
    },
    onError: (_err, _dailyVerse, context) => {
      if (context?.previous) {
        queryClient.setQueryData(FAVORITES_KEY, context.previous);
      }
    },
    onSuccess: (data, dailyVerse) => {
      const previous = queryClient.getQueryData<FavoriteOut[]>(FAVORITES_KEY);
      if (previous) {
        queryClient.setQueryData(
          FAVORITES_KEY,
          previous.map((f) => (f.daily_verse.id === dailyVerse.id ? data : f))
        );
      }
    },
  });
}

export function useRemoveFavorite() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (favoriteId: number) => apiDelete(`/favorites/${favoriteId}`),
    onMutate: async (favoriteId) => {
      await queryClient.cancelQueries({ queryKey: FAVORITES_KEY });
      const previous = queryClient.getQueryData<FavoriteOut[]>(FAVORITES_KEY);
      if (previous) {
        queryClient.setQueryData(
          FAVORITES_KEY,
          previous.filter((f) => f.id !== favoriteId)
        );
      }
      return { previous };
    },
    onError: (_err, _favoriteId, context) => {
      if (context?.previous) {
        queryClient.setQueryData(FAVORITES_KEY, context.previous);
      }
    },
  });
}
