import { StyleSheet, View } from "react-native";
import type { DailyVerseOut } from "@versiculo-diario/shared";

import { useTheme } from "../theme";
import { AppText } from "./AppText";
import { FavoriteButton } from "./FavoriteButton";

function formatDate(iso: string) {
  return new Date(`${iso}T00:00:00Z`).toLocaleDateString("es", {
    day: "numeric",
    month: "long",
    timeZone: "UTC",
  });
}

export function VerseListItem({ dailyVerse }: { dailyVerse: DailyVerseOut }) {
  const theme = useTheme();

  return (
    <View
      style={[
        styles.container,
        { borderBottomColor: theme.colors.border, paddingVertical: theme.spacing.md },
      ]}
    >
      <View style={styles.textColumn}>
        <AppText variant="caption">{formatDate(dailyVerse.date)}</AppText>
        <AppText variant="label" style={{ marginTop: theme.spacing.xs }}>
          {dailyVerse.verse.reference}
        </AppText>
        <AppText variant="body" numberOfLines={2} style={{ marginTop: theme.spacing.xs }}>
          {dailyVerse.verse.text}
        </AppText>
      </View>
      <FavoriteButton dailyVerseId={dailyVerse.id} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: "row",
    alignItems: "center",
    borderBottomWidth: 1,
  },
  textColumn: {
    flex: 1,
  },
});
