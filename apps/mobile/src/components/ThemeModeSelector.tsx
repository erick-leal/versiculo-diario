import { Pressable, StyleProp, StyleSheet, View, ViewStyle } from "react-native";

import { useTheme } from "../theme";
import { AppText } from "./AppText";

type LightOrDark = "light" | "dark";

const OPTIONS: { value: LightOrDark; label: string }[] = [
  { value: "light", label: "Claro" },
  { value: "dark", label: "Oscuro" },
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
