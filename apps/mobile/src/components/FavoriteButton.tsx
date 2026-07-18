import { Pressable, StyleSheet } from "react-native";
import { Ionicons } from "@expo/vector-icons";
import type { DailyVerseOut } from "@versiculo-diario/shared";

import { useFavoriteStatus } from "../api/useFavoriteStatus";
import { useTheme } from "../theme";

// Ionicons en vez de Feather (el set base del sistema de diseno) solo aca:
// es el unico de los dos que trae par relleno/contorno ("heart"/"heart-outline"),
// necesario para que el estado de favorito se lea de un vistazo.
export function FavoriteButton({ dailyVerse }: { dailyVerse: DailyVerseOut }) {
  const theme = useTheme();
  const { isFavorite, toggle, isPending } = useFavoriteStatus(dailyVerse);

  return (
    <Pressable
      onPress={toggle}
      disabled={isPending}
      hitSlop={8}
      style={styles.button}
      accessibilityRole="button"
      accessibilityLabel={isFavorite ? "Quitar de favoritos" : "Guardar en favoritos"}
    >
      <Ionicons
        name={isFavorite ? "heart" : "heart-outline"}
        size={22}
        color={theme.colors.accent}
      />
    </Pressable>
  );
}

const styles = StyleSheet.create({
  button: {
    minWidth: 44,
    minHeight: 44,
    alignItems: "center",
    justifyContent: "center",
  },
});
