import { Pressable, ScrollView, StyleSheet } from "react-native";
import { Feather } from "@expo/vector-icons";
import { router } from "expo-router";

import { AppText } from "../../src/components/AppText";
import { Screen } from "../../src/components/Screen";
import { MOOD_TAGS, MOOD_TAG_LABELS } from "../../src/lib/moodTags";
import { useTheme } from "../../src/theme";

export default function MoodPickerScreen() {
  const theme = useTheme();

  return (
    <Screen>
      <Pressable
        onPress={() => router.back()}
        hitSlop={8}
        style={[styles.backButton, { marginLeft: theme.spacing.lg, marginTop: theme.spacing.sm }]}
        accessibilityRole="button"
        accessibilityLabel="Volver"
      >
        <Feather name="arrow-left" size={22} color={theme.colors.textPrimary} />
      </Pressable>
      <ScrollView contentContainerStyle={{ padding: theme.spacing.lg }}>
        <AppText variant="title" style={{ marginBottom: theme.spacing.md }}>
          ¿Cómo te sentís hoy?
        </AppText>
        {MOOD_TAGS.map((tag) => (
          <Pressable
            key={tag}
            onPress={() => router.push(`/mood/${tag}`)}
            style={[styles.tagRow, { borderColor: theme.colors.border }]}
            accessibilityRole="button"
          >
            <AppText variant="body" style={{ color: theme.colors.textPrimary }}>
              {MOOD_TAG_LABELS[tag]}
            </AppText>
            <Feather name="chevron-right" size={18} color={theme.colors.textSecondary} />
          </Pressable>
        ))}
      </ScrollView>
    </Screen>
  );
}

const styles = StyleSheet.create({
  backButton: {
    width: 44,
    height: 44,
    alignItems: "center",
    justifyContent: "center",
  },
  tagRow: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    minHeight: 44,
    paddingVertical: 12,
    borderBottomWidth: 1,
  },
});
