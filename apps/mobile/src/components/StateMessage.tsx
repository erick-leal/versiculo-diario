import { ActivityIndicator, View } from "react-native";

import { useTheme } from "../theme";
import { AppText } from "./AppText";

export function LoadingState() {
  const theme = useTheme();
  return (
    <View>
      <ActivityIndicator size="large" color={theme.colors.accent} />
    </View>
  );
}

export function ErrorState({ message }: { message: string }) {
  const theme = useTheme();
  return (
    <AppText variant="body" style={{ color: theme.colors.error, textAlign: "center" }}>
      {message}
    </AppText>
  );
}
