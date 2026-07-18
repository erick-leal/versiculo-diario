import { Pressable, ScrollView, StyleSheet } from "react-native";
import { Feather } from "@expo/vector-icons";
import { router, useLocalSearchParams } from "expo-router";

import { useDailyVerseById } from "../../src/api/useDailyVerseById";
import { Screen } from "../../src/components/Screen";
import { VerseCard } from "../../src/components/VerseCard";
import { LoadingState, ErrorState } from "../../src/components/StateMessage";
import { useTheme } from "../../src/theme";

export default function DayScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const dailyVerseId = Number(id);
  const { data, isPending, isError, error } = useDailyVerseById(dailyVerseId);
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
      <ScrollView
        keyboardShouldPersistTaps="handled"
        contentContainerStyle={{ padding: theme.spacing.lg }}
      >
        {isPending && <LoadingState />}
        {isError && <ErrorState message={error.message} />}
        {data && <VerseCard dailyVerse={data} />}
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
});
