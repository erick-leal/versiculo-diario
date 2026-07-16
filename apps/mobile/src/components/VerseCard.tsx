import { StyleSheet, View } from "react-native";
import type { DailyVerseOut } from "@versiculo-diario/shared";

import { useTheme } from "../theme";
import { AppText } from "./AppText";
import { FavoriteButton } from "./FavoriteButton";

interface VerseCardProps {
  dailyVerse: DailyVerseOut;
}

export function VerseCard({ dailyVerse }: VerseCardProps) {
  const theme = useTheme();

  return (
    <View>
      <View style={styles.header}>
        <AppText variant="label" style={styles.reference}>
          {dailyVerse.verse.reference}
        </AppText>
        <FavoriteButton dailyVerseId={dailyVerse.id} />
      </View>
      <AppText variant="verse" style={{ marginTop: theme.spacing.sm }}>
        {dailyVerse.verse.text}
      </AppText>

      <View
        style={[
          styles.divider,
          { backgroundColor: theme.colors.border, marginVertical: theme.spacing.xl },
        ]}
      />

      {dailyVerse.reflection.title && (
        <AppText variant="title" style={{ marginBottom: theme.spacing.sm }}>
          {dailyVerse.reflection.title}
        </AppText>
      )}
      <AppText variant="body">{dailyVerse.reflection.body}</AppText>
    </View>
  );
}

const styles = StyleSheet.create({
  header: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
  },
  reference: {
    flex: 1,
  },
  divider: {
    height: 1,
  },
});
