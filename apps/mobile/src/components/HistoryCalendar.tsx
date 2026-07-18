import { useMemo, useState } from "react";
import { Pressable, StyleSheet, View } from "react-native";
import { Feather } from "@expo/vector-icons";
import { router } from "expo-router";
import type { DailyVerseOut } from "@versiculo-diario/shared";

import { useTheme } from "../theme";
import { AppText } from "./AppText";

const WEEKDAY_LABELS = ["D", "L", "M", "M", "J", "V", "S"];

function toDateKey(date: Date): string {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

function monthLabel(date: Date): string {
  const label = date.toLocaleDateString("es", { month: "long", year: "numeric" });
  return label.charAt(0).toUpperCase() + label.slice(1);
}

export function HistoryCalendar({ data }: { data: DailyVerseOut[] }) {
  const theme = useTheme();
  const [monthCursor, setMonthCursor] = useState(() => {
    const now = new Date();
    return new Date(now.getFullYear(), now.getMonth(), 1);
  });

  const byDate = useMemo(() => {
    const map = new Map<string, DailyVerseOut>();
    for (const item of data) {
      map.set(item.date, item);
    }
    return map;
  }, [data]);

  const weeks = useMemo(() => {
    const year = monthCursor.getFullYear();
    const month = monthCursor.getMonth();
    const firstDay = new Date(year, month, 1);
    const daysInMonth = new Date(year, month + 1, 0).getDate();

    const cells: (Date | null)[] = [];
    for (let i = 0; i < firstDay.getDay(); i++) {
      cells.push(null);
    }
    for (let day = 1; day <= daysInMonth; day++) {
      cells.push(new Date(year, month, day));
    }
    while (cells.length % 7 !== 0) {
      cells.push(null);
    }

    const result: (Date | null)[][] = [];
    for (let i = 0; i < cells.length; i += 7) {
      result.push(cells.slice(i, i + 7));
    }
    return result;
  }, [monthCursor]);

  function goToPreviousMonth() {
    setMonthCursor((prev) => new Date(prev.getFullYear(), prev.getMonth() - 1, 1));
  }

  function goToNextMonth() {
    setMonthCursor((prev) => new Date(prev.getFullYear(), prev.getMonth() + 1, 1));
  }

  return (
    <View>
      <View style={styles.header}>
        <Pressable
          onPress={goToPreviousMonth}
          hitSlop={8}
          style={styles.navButton}
          accessibilityRole="button"
          accessibilityLabel="Mes anterior"
        >
          <Feather name="chevron-left" size={22} color={theme.colors.textPrimary} />
        </Pressable>
        <AppText variant="label">{monthLabel(monthCursor)}</AppText>
        <Pressable
          onPress={goToNextMonth}
          hitSlop={8}
          style={styles.navButton}
          accessibilityRole="button"
          accessibilityLabel="Mes siguiente"
        >
          <Feather name="chevron-right" size={22} color={theme.colors.textPrimary} />
        </Pressable>
      </View>

      <View style={styles.weekRow}>
        {WEEKDAY_LABELS.map((label, index) => (
          <View key={index} style={styles.cell}>
            <AppText variant="caption" style={{ textAlign: "center" }}>
              {label}
            </AppText>
          </View>
        ))}
      </View>

      {weeks.map((week, weekIndex) => (
        <View key={weekIndex} style={styles.weekRow}>
          {week.map((date, dayIndex) => {
            if (!date) {
              return <View key={dayIndex} style={styles.cell} />;
            }
            const entry = byDate.get(toDateKey(date));
            return (
              <View key={dayIndex} style={styles.cell}>
                <Pressable
                  disabled={!entry}
                  onPress={() => entry && router.push(`/day/${entry.id}`)}
                  style={[
                    styles.dayButton,
                    entry && { backgroundColor: theme.colors.accent },
                  ]}
                  accessibilityRole={entry ? "button" : undefined}
                  accessibilityLabel={entry ? `Ver versículo del ${date.getDate()}` : undefined}
                >
                  <AppText
                    variant="body"
                    style={{
                      color: entry ? theme.colors.background : theme.colors.textSecondary,
                    }}
                  >
                    {date.getDate()}
                  </AppText>
                </Pressable>
              </View>
            );
          })}
        </View>
      ))}
    </View>
  );
}

const styles = StyleSheet.create({
  header: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    paddingVertical: 12,
  },
  navButton: {
    width: 44,
    height: 44,
    alignItems: "center",
    justifyContent: "center",
  },
  weekRow: {
    flexDirection: "row",
  },
  cell: {
    flex: 1,
    aspectRatio: 1,
    alignItems: "center",
    justifyContent: "center",
  },
  dayButton: {
    width: 36,
    height: 36,
    borderRadius: 18,
    alignItems: "center",
    justifyContent: "center",
  },
});
