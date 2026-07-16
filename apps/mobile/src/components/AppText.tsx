import { Text, type TextProps } from "react-native";

import { useTheme } from "../theme";

type Variant = "verse" | "title" | "body" | "label" | "caption";

const variantConfig: Record<Variant, { fontKey: "verse" | "heading" | "body" | "label"; colorKey: "textPrimary" | "textSecondary" | "textLabel" }> = {
  verse: { fontKey: "verse", colorKey: "textPrimary" },
  title: { fontKey: "heading", colorKey: "textPrimary" },
  body: { fontKey: "body", colorKey: "textSecondary" },
  label: { fontKey: "label", colorKey: "textLabel" },
  caption: { fontKey: "body", colorKey: "textSecondary" },
};

interface AppTextProps extends TextProps {
  variant?: Variant;
}

export function AppText({ variant = "body", style, ...rest }: AppTextProps) {
  const theme = useTheme();
  const { fontKey, colorKey } = variantConfig[variant];

  return (
    <Text
      style={[
        {
          fontFamily: theme.fonts[fontKey],
          color: theme.colors[colorKey],
          ...theme.type[variant],
        },
        variant === "label" && { textTransform: "uppercase" },
        style,
      ]}
      {...rest}
    />
  );
}
