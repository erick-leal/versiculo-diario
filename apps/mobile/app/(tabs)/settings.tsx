import { StyleSheet, Switch, View } from "react-native";

import { useSettings, useUpdateSettings } from "../../src/api/useSettings";
import { AppText } from "../../src/components/AppText";
import { Screen } from "../../src/components/Screen";
import { LoadingState, ErrorState } from "../../src/components/StateMessage";
import { ThemeModeSelector } from "../../src/components/ThemeModeSelector";
import { useTheme } from "../../src/theme";

export default function SettingsScreen() {
  const theme = useTheme();
  const { data, isPending, isError, error } = useSettings();
  const updateSettings = useUpdateSettings();

  return (
    <Screen edges={["top"]}>
      <View style={{ padding: theme.spacing.lg }}>
        {isPending && <LoadingState />}
        {isError && <ErrorState message={error.message} />}

        {data && (
          <>
            <AppText variant="label" style={{ marginBottom: theme.spacing.sm }}>
              Apariencia
            </AppText>

            <View style={styles.row}>
              <AppText variant="body">Usar la del sistema</AppText>
              <Switch
                value={data.dark_mode === "system"}
                onValueChange={(useSystem) =>
                  updateSettings.mutate({ dark_mode: useSystem ? "system" : "light" })
                }
                trackColor={{ true: theme.colors.accent }}
              />
            </View>

            {data.dark_mode !== "system" && (
              <ThemeModeSelector
                value={data.dark_mode === "dark" ? "dark" : "light"}
                onChange={(dark_mode) => updateSettings.mutate({ dark_mode })}
                style={{ marginTop: theme.spacing.sm }}
              />
            )}
          </>
        )}
      </View>
    </Screen>
  );
}

const styles = StyleSheet.create({
  row: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    minHeight: 44,
  },
});
