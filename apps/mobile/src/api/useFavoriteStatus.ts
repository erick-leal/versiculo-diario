import { useAddFavorite, useFavorites, useRemoveFavorite } from "./useFavorites";

export function useFavoriteStatus(dailyVerseId: number) {
  const { data: favorites } = useFavorites();
  const addFavorite = useAddFavorite();
  const removeFavorite = useRemoveFavorite();

  const favorite = favorites?.find((f) => f.daily_verse.id === dailyVerseId);

  const toggle = () => {
    if (favorite) {
      removeFavorite.mutate(favorite.id);
    } else {
      addFavorite.mutate(dailyVerseId);
    }
  };

  return {
    isFavorite: Boolean(favorite),
    toggle,
    isPending: addFavorite.isPending || removeFavorite.isPending,
  };
}
