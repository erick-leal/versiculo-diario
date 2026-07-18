import { FlatList, Pressable, StyleSheet, View } from "react-native";
import { router } from "expo-router";
import type { PersonalReflectionOut } from "@versiculo-diario/shared";

import { usePersonalReflections } from "../../src/api/usePersonalReflections";
import { AppText } from "../../src/components/AppText";
import { Screen } from "../../src/components/Screen";
import { LoadingState, ErrorState } from "../../src/components/StateMessage";
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

  return (
    <Screen edges={["top"]}>
      {isPending && <LoadingState />}
      {isError && <ErrorState message={error.message} />}
      {data && data.length === 0 && (
        <View style={{ padding: theme.spacing.lg }}>
          <AppText variant="body" style={{ color: theme.colors.textSecondary }}>
            Aún no has escrito ninguna reflexión personal. Cuando escribas una desde el
            versículo del día, aparecerá aquí.
          </AppText>
        </View>
      )}
      {data && data.length > 0 && (
        <FlatList
          data={data}
          keyExtractor={(item) => String(item.id)}
          contentContainerStyle={{ paddingHorizontal: theme.spacing.lg }}
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
