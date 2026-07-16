import { createContext, useContext, type ReactNode } from "react";
import { useColorScheme } from "react-native";

import { useSettings } from "../api/useSettings";
import { darkColors, lightColors, type ColorScheme } from "./colors";
import { radii, spacing } from "./spacing";
import { fontFamilies, typeScale } from "./typography";

const theme = {
  colors: lightColors,
  spacing,
  radii,
  fonts: fontFamilies,
  type: typeScale,
};

export type Theme = typeof theme;

const ThemeContext = createContext<Theme | null>(null);

export function ThemeProvider({ children }: { children: ReactNode }) {
  const systemScheme = useColorScheme();
  // Mientras las settings cargan (o si falla la red), seguimos al sistema -
  // nunca bloqueamos el render de toda la app por esto.
  const { data: settings } = useSettings();
  const preference = settings?.dark_mode ?? "system";
  const effectiveScheme = preference === "system" ? systemScheme : preference;

  const colors: ColorScheme = effectiveScheme === "dark" ? darkColors : lightColors;

  const value: Theme = { colors, spacing, radii, fonts: fontFamilies, type: typeScale };

  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
}

export function useTheme(): Theme {
  const ctx = useContext(ThemeContext);
  if (!ctx) {
    throw new Error("useTheme debe usarse dentro de ThemeProvider");
  }
  return ctx;
}
