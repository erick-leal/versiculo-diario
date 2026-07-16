import { Pressable, StyleSheet, View } from "react-native";
import type { DarkModePreference } from "@versiculo-diario/shared";

import { useTheme } from "../theme";
import { AppText } from "./AppText";

const OPTIONS: { value: DarkModePreference; label: string }[] = [
  { value: "light", label: "Claro" },
  { value: "dark", label: "Oscuro" },
  { value: "system", label: "Sistema" },
];

interface ThemeModeSelectorProps {
  value: DarkModePreference;
  onChange: (value: DarkModePreference) => void;
}

export function ThemeModeSelector({ value, onChange }: ThemeModeSelectorProps) {
  const theme = useTheme();

  return (
    <View style={[styles.row, { borderColor: theme.colors.border }]}>
      {OPTIONS.map((option) => {
        const active = option.value === value;
        return (
          <Pressable
            key={option.value}
            onPress={() => onChange(option.value)}
            style={[
              styles.option,
              active && { backgroundColor: theme.colors.accent },
            ]}
            accessibilityRole="button"
            accessibilityState={{ selected: active }}
          >
            <AppText
              variant="body"
              style={{ color: active ? "#FFFFFF" : theme.colors.textSecondary }}
            >
              {option.label}
            </AppText>
          </Pressable>
        );
      })}
    </View>
  );
}

const styles = StyleSheet.create({
  row: {
    flexDirection: "row",
    borderWidth: 1,
    borderRadius: 12,
    padding: 4,
    gap: 4,
  },
  option: {
    flex: 1,
    minHeight: 44,
    borderRadius: 9,
    alignItems: "center",
    justifyContent: "center",
  },
});
