import { useState } from "react";
import { Pressable, StyleSheet, View } from "react-native";
import { Feather } from "@expo/vector-icons";
import type { DailyVerseOut } from "@versiculo-diario/shared";

import { useTheme } from "../theme";
import { AppText } from "./AppText";
import { FavoriteButton } from "./FavoriteButton";
import { MyReflectionEditor } from "./MyReflectionEditor";
import { ShareSheet } from "./ShareSheet";

interface VerseCardProps {
  dailyVerse: DailyVerseOut;
}

export function VerseCard({ dailyVerse }: VerseCardProps) {
  const theme = useTheme();
  const [shareVisible, setShareVisible] = useState(false);

  return (
    <View>
      <View style={styles.header}>
        <AppText variant="label" style={styles.reference}>
          {dailyVerse.verse.reference}
        </AppText>
        <Pressable
          onPress={() => setShareVisible(true)}
          hitSlop={8}
          style={styles.iconButton}
          accessibilityRole="button"
          accessibilityLabel="Compartir versículo"
        >
          <Feather name="share" size={20} color={theme.colors.accent} />
        </Pressable>
        <FavoriteButton dailyVerse={dailyVerse} />
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

      <MyReflectionEditor dailyVerse={dailyVerse} />

      <ShareSheet
        dailyVerse={dailyVerse}
        visible={shareVisible}
        onClose={() => setShareVisible(false)}
      />
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
  iconButton: {
    minWidth: 44,
    minHeight: 44,
    alignItems: "center",
    justifyContent: "center",
  },
  divider: {
    height: 1,
  },
});
