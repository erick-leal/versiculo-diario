import { StyleSheet, View } from "react-native";
import type { DailyVerseOut } from "@versiculo-diario/shared";

import { useTheme } from "../theme";
import { AppText } from "./AppText";

interface VerseCardProps {
  dailyVerse: DailyVerseOut;
}

export function VerseCard({ dailyVerse }: VerseCardProps) {
  const theme = useTheme();

  return (
    <View>
      <AppText variant="label">{dailyVerse.verse.reference}</AppText>
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
  divider: {
    height: 1,
  },
});
