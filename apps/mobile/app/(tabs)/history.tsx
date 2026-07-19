import { useCallback, useMemo, useState } from "react";
import { Pressable, ScrollView, StyleSheet, View } from "react-native";
import { Feather } from "@expo/vector-icons";
import { router, useFocusEffect } from "expo-router";

import { useHistory } from "../../src/api/useHistory";
import { AppText } from "../../src/components/AppText";
import { HistoryCalendar } from "../../src/components/HistoryCalendar";
import { Screen } from "../../src/components/Screen";
import { SearchInput } from "../../src/components/SearchInput";
import { LoadingState, ErrorState } from "../../src/components/StateMessage";
import { normalizeForSearch } from "../../src/lib/normalizeForSearch";
import { getViewedToday, type ViewedEntry } from "../../src/lib/recentlyViewed";
import { useTheme } from "../../src/theme";

type HistoryView = "calendar" | "viewed";

export default function HistoryScreen() {
  const { data, isPending, isError, error } = useHistory();
  const theme = useTheme();
  const [view, setView] = useState<HistoryView>("calendar");
  const [viewedToday, setViewedToday] = useState<ViewedEntry[]>([]);
  const [query, setQuery] = useState("");

  useFocusEffect(
    useCallback(() => {
      getViewedToday().then(setViewedToday);
    }, [])
  );

  const filteredViewed = useMemo(() => {
    const normalizedQuery = normalizeForSearch(query.trim());
    if (!normalizedQuery) return viewedToday;
    return viewedToday.filter((entry) => normalizeForSearch(entry.reference).includes(normalizedQuery));
  }, [viewedToday, query]);

  return (
    <Screen edges={["top"]}>
      <View style={[styles.segmentRow, { paddingHorizontal: theme.spacing.lg, marginTop: theme.spacing.lg }]}>
        <Pressable
          onPress={() => setView("viewed")}
          style={[
            styles.segmentButton,
            {
              borderColor: theme.colors.border,
              backgroundColor: view === "viewed" ? theme.colors.accent : "transparent",
            },
          ]}
          accessibilityRole="button"
        >
          <AppText
            variant="label"
            style={{ color: view === "viewed" ? theme.colors.background : theme.colors.textPrimary }}
          >
            Explorados hoy
          </AppText>
        </Pressable>
        <Pressable
          onPress={() => setView("calendar")}
          style={[
            styles.segmentButton,
            {
              borderColor: theme.colors.border,
              backgroundColor: view === "calendar" ? theme.colors.accent : "transparent",
              marginLeft: theme.spacing.sm,
            },
          ]}
          accessibilityRole="button"
        >
          <AppText
            variant="label"
            style={{ color: view === "calendar" ? theme.colors.background : theme.colors.textPrimary }}
          >
            Versículo diario
          </AppText>
        </Pressable>
      </View>

      {isPending && (
        <View style={[styles.centerFill, { paddingHorizontal: theme.spacing.lg, paddingTop: theme.spacing.md }]}>
          <LoadingState />
        </View>
      )}
      {isError && <ErrorState message={error.message} />}

      {view === "viewed" && (
        <ScrollView
          keyboardShouldPersistTaps="handled"
          contentContainerStyle={{ paddingHorizontal: theme.spacing.lg, paddingTop: theme.spacing.md }}
        >
          {viewedToday.length > 0 && (
            <SearchInput value={query} onChangeText={setQuery} placeholder="Buscar por referencia..." />
          )}
          {viewedToday.length === 0 && (
            <AppText
              variant="body"
              style={{ textAlign: "center", marginTop: theme.spacing.xxl, color: theme.colors.textSecondary }}
            >
              Todavía no exploraste ningún versículo hoy. Probá "Buscar por estado de ánimo" desde Inicio.
            </AppText>
          )}
          {filteredViewed.map((entry) => (
            <Pressable
              key={entry.id}
              onPress={() => router.push(`/day/${entry.id}`)}
              style={[styles.viewedRow, { borderColor: theme.colors.border, marginTop: theme.spacing.md }]}
              accessibilityRole="button"
            >
              <AppText variant="body" style={{ color: theme.colors.textPrimary }}>
                {entry.reference}
              </AppText>
              <Feather name="chevron-right" size={18} color={theme.colors.textSecondary} />
            </Pressable>
          ))}
        </ScrollView>
      )}

      {view === "calendar" && data && (
        <ScrollView contentContainerStyle={{ paddingHorizontal: theme.spacing.lg, paddingTop: theme.spacing.md }}>
          <HistoryCalendar data={data} />
        </ScrollView>
      )}
    </Screen>
  );
}

const styles = StyleSheet.create({
  segmentRow: {
    flexDirection: "row",
  },
  centerFill: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
  },
  segmentButton: {
    flex: 1,
    minHeight: 44,
    alignItems: "center",
    justifyContent: "center",
    borderWidth: 1,
    borderRadius: 8,
  },
  viewedRow: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    minHeight: 44,
    paddingVertical: 12,
    borderBottomWidth: 1,
  },
});
