// Paleta calida y neutra ("pergamino"), con un acento dorado usado con
// moderacion (referencias, iconos activos) - nunca como color de texto de
// cuerpo, para mantener buen contraste. Ver docs/design-system.md.

export const lightColors = {
  background: "#FBFAF7",
  surface: "#F5F2EA",
  border: "#E4DFD3",
  textPrimary: "#1F1B16",
  textSecondary: "#4A443B",
  textLabel: "#6B5A3A",
  accent: "#B8860B",
  error: "#B3261E",
};

export const darkColors = {
  background: "#14120F",
  surface: "#1E1B16",
  border: "#332F27",
  textPrimary: "#F5F1E8",
  textSecondary: "#C9C0AE",
  textLabel: "#D4B45A",
  accent: "#D4AF37",
  error: "#FF6B60",
};

export type ColorScheme = typeof lightColors;
