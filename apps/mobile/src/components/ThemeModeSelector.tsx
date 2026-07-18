import { Pressable, StyleProp, StyleSheet, View, ViewStyle } from "react-native";
import { Feather } from "@expo/vector-icons";
import type { DarkModePreference } from "@versiculo-diario/shared";

import { useTheme } from "../theme";
import { AppText } from "./AppText";

type LightOrDark = Exclude<DarkModePreference, "system">;

const OPTIONS: { value: LightOrDark; label: string; icon: keyof typeof Feather.glyphMap }[] = [
  { value: "light", label: "Claro", icon: "sun" },
  { value: "dark", label: "Oscuro", icon: "moon" },
];

interface ThemeModeSelectorProps {
  value: LightOrDark;
  onChange: (value: LightOrDark) => void;
  style?: StyleProp<ViewStyle>;
}

export function ThemeModeSelector({ value, onChange, style }: ThemeModeSelectorProps) {
  const theme = useTheme();

  return (
    <View style={[styles.row, { borderColor: theme.colors.border }, style]}>
      {OPTIONS.map((option) => {
        const active = option.value === value;
        const color = active ? "#FFFFFF" : theme.colors.textSecondary;
        return (
          <Pressable
            key={option.value}
            onPress={() => onChange(option.value)}
            style={[styles.option, active && { backgroundColor: theme.colors.accent }]}
            accessibilityRole="button"
            accessibilityState={{ selected: active }}
          >
            <Feather name={option.icon} size={16} color={color} />
            <AppText variant="caption" style={{ color }}>
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
    minHeight: 56,
    borderRadius: 9,
    alignItems: "center",
    justifyContent: "center",
    gap: 4,
  },
});
