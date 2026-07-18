import { Alert, Platform, Pressable, StyleSheet, Switch, useColorScheme, View } from "react-native";
import { DateTimePickerAndroid } from "@react-native-community/datetimepicker";
import { Feather } from "@expo/vector-icons";

import { useSettings, useUpdateSettings } from "../../src/api/useSettings";
import { AppText } from "../../src/components/AppText";
import { Screen } from "../../src/components/Screen";
import { LoadingState, ErrorState } from "../../src/components/StateMessage";
import { ThemeModeSelector } from "../../src/components/ThemeModeSelector";
import {
  cancelDailyReminder,
  requestNotificationPermission,
  scheduleDailyReminder,
} from "../../src/lib/notifications";
import { useTheme } from "../../src/theme";

function parseTime(time: string): { hour: number; minute: number } {
  const [hour, minute] = time.split(":").map(Number);
  return { hour, minute };
}

function formatTime(time: string): string {
  const { hour, minute } = parseTime(time);
  const date = new Date();
  date.setHours(hour, minute, 0, 0);
  return date.toLocaleTimeString("es", { hour: "numeric", minute: "2-digit" });
}

export default function SettingsScreen() {
  const theme = useTheme();
  const systemScheme = useColorScheme();
  const { data, isPending, isError, error } = useSettings();
  const updateSettings = useUpdateSettings();

  async function handleToggleNotifications(enabled: boolean) {
    if (!data) return;

    if (!enabled) {
      await cancelDailyReminder();
      updateSettings.mutate({ notification_enabled: false });
      return;
    }

    const granted = await requestNotificationPermission();
    if (!granted) {
      Alert.alert(
        "Permiso de notificaciones",
        "Para recibir el recordatorio diario, habilita las notificaciones de Versículo Diario desde los ajustes del sistema."
      );
      return;
    }

    const { hour, minute } = parseTime(data.notification_time);
    await scheduleDailyReminder(hour, minute);
    updateSettings.mutate({ notification_enabled: true });
  }

  function handleOpenTimePicker() {
    // La API declarativa (<DateTimePicker> montado) deja el dialogo de
    // Android "pegado" - la API imperativa se autogestiona (abre y cierra
    // sola), evitando ese bug.
    if (!data || Platform.OS !== "android") return;

    const { hour, minute } = parseTime(data.notification_time);
    const value = new Date();
    value.setHours(hour, minute, 0, 0);

    DateTimePickerAndroid.open({
      value,
      mode: "time",
      is24Hour: false,
      onChange: (event, selected) => {
        if (event.type !== "set" || !selected) return;
        const newHour = selected.getHours();
        const newMinute = selected.getMinutes();
        scheduleDailyReminder(newHour, newMinute);
        updateSettings.mutate({
          notification_time: `${String(newHour).padStart(2, "0")}:${String(newMinute).padStart(2, "0")}:00`,
        });
      },
    });
  }

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
            <ThemeModeSelector
              // "system" solo es el default inicial del backend (nunca
              // seleccionable desde este selector) - se resalta el que
              // coincide con el SO hasta que el usuario elija uno explicito.
              value={data.dark_mode === "system" ? (systemScheme === "dark" ? "dark" : "light") : data.dark_mode}
              onChange={(dark_mode) => updateSettings.mutate({ dark_mode })}
            />

            <AppText
              variant="label"
              style={{ marginTop: theme.spacing.xl, marginBottom: theme.spacing.sm }}
            >
              Recordatorio diario
            </AppText>

            <View style={styles.row}>
              <AppText variant="body">Recibir recordatorio</AppText>
              <Switch
                value={data.notification_enabled}
                onValueChange={handleToggleNotifications}
                trackColor={{ true: theme.colors.accent }}
              />
            </View>

            {data.notification_enabled && (
              <Pressable onPress={handleOpenTimePicker} style={styles.row} accessibilityRole="button">
                <AppText variant="body">Hora</AppText>
                <View style={styles.timeValue}>
                  <AppText variant="body" style={{ color: theme.colors.accent }}>
                    {formatTime(data.notification_time)}
                  </AppText>
                  <Feather name="chevron-right" size={18} color={theme.colors.textSecondary} />
                </View>
              </Pressable>
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
  timeValue: {
    flexDirection: "row",
    alignItems: "center",
    gap: 4,
  },
});
