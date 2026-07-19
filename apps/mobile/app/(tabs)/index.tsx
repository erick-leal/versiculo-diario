import { Pressable, ScrollView, StyleSheet } from "react-native";
import { Feather } from "@expo/vector-icons";
import { router } from "expo-router";

import { useDailyVerse } from "../../src/api/useDailyVerse";
import { useSettings } from "../../src/api/useSettings";
import { AppText } from "../../src/components/AppText";
import { ReminderBanner } from "../../src/components/ReminderBanner";
import { Screen } from "../../src/components/Screen";
import { VerseCard } from "../../src/components/VerseCard";
import { LoadingState, ErrorState } from "../../src/components/StateMessage";
import { useTheme } from "../../src/theme";

export default function HomeScreen() {
  const { data, isPending, isError, error } = useDailyVerse();
  const { data: settings } = useSettings();
  const theme = useTheme();

  return (
    <Screen>
      <ScrollView
        keyboardShouldPersistTaps="handled"
        contentContainerStyle={{
          flexGrow: 1,
          justifyContent: "center",
          padding: theme.spacing.lg,
        }}
      >
        {isPending && <LoadingState />}
        {isError && <ErrorState message={error.message} />}
        {data && <VerseCard dailyVerse={data} />}

        <Pressable
          onPress={() => router.push("/mood")}
          style={[styles.moodButton, { borderColor: theme.colors.border, marginTop: theme.spacing.xl }]}
          accessibilityRole="button"
        >
          <Feather name="compass" size={16} color={theme.colors.accent} />
          <AppText variant="label" style={{ color: theme.colors.accent, marginLeft: theme.spacing.sm }}>
            Buscar por estado de ánimo
          </AppText>
        </Pressable>

        <ReminderBanner settings={settings} />
      </ScrollView>
    </Screen>
  );
}

const styles = StyleSheet.create({
  moodButton: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    minHeight: 44,
    borderWidth: 1,
    borderRadius: 8,
  },
});
