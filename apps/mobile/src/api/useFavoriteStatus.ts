import type { DailyVerseOut } from "@versiculo-diario/shared";

import { useAddFavorite, useFavorites, useRemoveFavorite } from "./useFavorites";

export function useFavoriteStatus(dailyVerse: DailyVerseOut) {
  const { data: favorites } = useFavorites();
  const addFavorite = useAddFavorite();
  const removeFavorite = useRemoveFavorite();

  const favorite = favorites?.find((f) => f.daily_verse.id === dailyVerse.id);

  const toggle = () => {
    if (favorite) {
      removeFavorite.mutate(favorite.id);
    } else {
      addFavorite.mutate(dailyVerse);
    }
  };

  return {
    isFavorite: Boolean(favorite),
    toggle,
    isPending: addFavorite.isPending || removeFavorite.isPending,
  };
}
