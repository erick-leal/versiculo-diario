import { useMemo, useState } from "react";
import { FlatList, Pressable, StyleSheet } from "react-native";
import { router } from "expo-router";
import type { PersonalReflectionOut } from "@versiculo-diario/shared";

import { usePersonalReflections } from "../../src/api/usePersonalReflections";
import { AppText } from "../../src/components/AppText";
import { Screen } from "../../src/components/Screen";
import { SearchInput } from "../../src/components/SearchInput";
import { LoadingState, ErrorState } from "../../src/components/StateMessage";
import { normalizeForSearch } from "../../src/lib/normalizeForSearch";
import { useTheme } from "../../src/theme";

function formatDate(iso: string) {
  return new Date(`${iso}T00:00:00Z`).toLocaleDateString("es", {
    day: "numeric",
    month: "long",
    timeZone: "UTC",
  });
}

function JournalEntryItem({ entry }: { entry: PersonalReflectionOut }) {
  const theme = useTheme();

  return (
    <Pressable
      onPress={() => router.push(`/day/${entry.daily_verse.id}`)}
      style={[
        styles.item,
        { borderBottomColor: theme.colors.border, paddingVertical: theme.spacing.md },
      ]}
      accessibilityRole="button"
    >
      <AppText variant="caption">{formatDate(entry.daily_verse.date)}</AppText>
      <AppText variant="label" style={{ marginTop: theme.spacing.xs }}>
        {entry.daily_verse.verse.reference}
      </AppText>
      <AppText variant="body" numberOfLines={2} style={{ marginTop: theme.spacing.xs }}>
        {entry.body}
      </AppText>
    </Pressable>
  );
}

export default function JournalScreen() {
  const { data, isPending, isError, error } = usePersonalReflections();
  const theme = useTheme();
  const [query, setQuery] = useState("");

  const filtered = useMemo(() => {
    if (!data) return data;
    const normalizedQuery = normalizeForSearch(query.trim());
    if (!normalizedQuery) return data;
    return data.filter(
      (item) =>
        normalizeForSearch(item.daily_verse.verse.reference).includes(normalizedQuery) ||
        normalizeForSearch(item.body).includes(normalizedQuery)
    );
  }, [data, query]);

  return (
    <Screen edges={["top"]}>
      {isPending && <LoadingState />}
      {isError && <ErrorState message={error.message} />}
      {data && data.length === 0 && (
        <AppText
          variant="body"
          style={{
            textAlign: "center",
            marginTop: theme.spacing.xxl,
            paddingHorizontal: theme.spacing.lg,
            color: theme.colors.textSecondary,
          }}
        >
          Aún no has escrito ninguna reflexión personal. Cuando escribas una desde el
          versículo del día, aparecerá aquí.
        </AppText>
      )}
      {data && data.length > 0 && (
        <FlatList
          data={filtered}
          keyExtractor={(item) => String(item.id)}
          contentContainerStyle={{ padding: theme.spacing.lg }}
          keyboardShouldPersistTaps="handled"
          ListHeaderComponent={
            <SearchInput
              value={query}
              onChangeText={setQuery}
              placeholder="Buscar por referencia o texto..."
            />
          }
          ListHeaderComponentStyle={{ marginBottom: theme.spacing.md }}
          renderItem={({ item }) => <JournalEntryItem entry={item} />}
        />
      )}
    </Screen>
  );
}

const styles = StyleSheet.create({
  item: {
    borderBottomWidth: 1,
  },
});
