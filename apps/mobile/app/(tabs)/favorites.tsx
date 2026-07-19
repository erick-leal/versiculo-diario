import { useMemo, useState } from "react";
import { FlatList } from "react-native";

import { useFavorites } from "../../src/api/useFavorites";
import { Screen } from "../../src/components/Screen";
import { SearchInput } from "../../src/components/SearchInput";
import { VerseListItem } from "../../src/components/VerseListItem";
import { LoadingState, ErrorState } from "../../src/components/StateMessage";
import { AppText } from "../../src/components/AppText";
import { normalizeForSearch } from "../../src/lib/normalizeForSearch";
import { useTheme } from "../../src/theme";

export default function FavoritesScreen() {
  const { data, isPending, isError, error } = useFavorites();
  const theme = useTheme();
  const [query, setQuery] = useState("");

  const filtered = useMemo(() => {
    if (!data) return data;
    const normalizedQuery = normalizeForSearch(query.trim());
    if (!normalizedQuery) return data;
    return data.filter((item) =>
      normalizeForSearch(item.daily_verse.verse.reference).includes(normalizedQuery)
    );
  }, [data, query]);

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
          data={filtered}
          keyExtractor={(item) => String(item.id)}
          contentContainerStyle={{ padding: theme.spacing.lg }}
          keyboardShouldPersistTaps="handled"
          ListHeaderComponent={
            <SearchInput value={query} onChangeText={setQuery} placeholder="Buscar por referencia..." />
          }
          ListHeaderComponentStyle={{ marginBottom: theme.spacing.md }}
          renderItem={({ item }) => <VerseListItem dailyVerse={item.daily_verse} />}
        />
      )}
    </Screen>
  );
}
