import { useEffect, useState } from "react";
import { Pressable, ScrollView, StyleSheet } from "react-native";
import { Feather } from "@expo/vector-icons";
import { router, useLocalSearchParams } from "expo-router";

import { useReflectionByMood } from "../../src/api/useReflectionByMood";
import { AppText } from "../../src/components/AppText";
import { Screen } from "../../src/components/Screen";
import { ErrorState, LoadingState } from "../../src/components/StateMessage";
import { VerseCard } from "../../src/components/VerseCard";
import { MOOD_TAG_LABELS, type MoodTag } from "../../src/lib/moodTags";
import { recordViewed } from "../../src/lib/recentlyViewed";
import { useTheme } from "../../src/theme";

export default function MoodResultScreen() {
  const { tag } = useLocalSearchParams<{ tag: MoodTag }>();
  const [excludeId, setExcludeId] = useState<number | undefined>(undefined);
  const theme = useTheme();
  const { data, isPending, isError, error, isFetching } = useReflectionByMood(tag, excludeId);

  useEffect(() => {
    if (!data) return;
    recordViewed({ id: data.id, reference: data.verse.reference, date: data.date });
  }, [data]);

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
      <ScrollView
        keyboardShouldPersistTaps="handled"
        contentContainerStyle={{ padding: theme.spacing.lg }}
      >
        <AppText variant="label" style={{ marginBottom: theme.spacing.md }}>
          {MOOD_TAG_LABELS[tag]}
        </AppText>

        {isPending && <LoadingState />}
        {isError && <ErrorState message={error.message} />}
        {data && (
          <>
            <VerseCard dailyVerse={data} />
            <Pressable
              onPress={() => setExcludeId(data.id)}
              disabled={isFetching}
              style={[styles.anotherButton, { borderColor: theme.colors.accent, marginTop: theme.spacing.xl }]}
              accessibilityRole="button"
            >
              <Feather name="refresh-cw" size={16} color={theme.colors.accent} />
              <AppText variant="label" style={{ color: theme.colors.accent, marginLeft: theme.spacing.sm }}>
                Otra reflexión
              </AppText>
            </Pressable>
          </>
        )}
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
  anotherButton: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    minHeight: 44,
    borderWidth: 1,
    borderRadius: 8,
  },
});
