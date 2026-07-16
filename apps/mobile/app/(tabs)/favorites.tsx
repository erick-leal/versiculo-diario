import { FlatList } from "react-native";

import { useFavorites } from "../../src/api/useFavorites";
import { Screen } from "../../src/components/Screen";
import { VerseListItem } from "../../src/components/VerseListItem";
import { LoadingState, ErrorState } from "../../src/components/StateMessage";
import { AppText } from "../../src/components/AppText";
import { useTheme } from "../../src/theme";

export default function FavoritesScreen() {
  const { data, isPending, isError, error } = useFavorites();
  const theme = useTheme();

  return (
    <Screen edges={["top"]}>
      {isPending && <LoadingState />}
      {isError && <ErrorState message={error.message} />}
      {data && data.length === 0 && (
        <AppText
          variant="body"
          style={{ textAlign: "center", marginTop: theme.spacing.xxl, paddingHorizontal: theme.spacing.lg }}
        >
          Todavía no guardaste ningún versículo. Toca el corazón en el de hoy para empezar.
        </AppText>
      )}
      {data && data.length > 0 && (
        <FlatList
          data={data}
          keyExtractor={(item) => String(item.id)}
          contentContainerStyle={{ paddingHorizontal: theme.spacing.lg }}
          renderItem={({ item }) => <VerseListItem dailyVerse={item.daily_verse} />}
        />
      )}
    </Screen>
  );
}
