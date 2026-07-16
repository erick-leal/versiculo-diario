import { useState } from "react";
import { StyleSheet, Switch, View } from "react-native";
import DateTimePicker from "@react-native-community/datetimepicker";

import { useSettings, useUpdateSettings } from "../../src/api/useSettings";
import {
  cancelDailyReminder,
  requestNotificationPermission,
  scheduleDailyReminder,
} from "../../src/lib/notifications";
import { AppText } from "../../src/components/AppText";
import { Screen } from "../../src/components/Screen";
import { LoadingState, ErrorState } from "../../src/components/StateMessage";
import { useTheme } from "../../src/theme";

function timeStringToDate(time: string): Date {
  const [hour, minute] = time.split(":").map(Number);
  const date = new Date();
  date.setHours(hour, minute, 0, 0);
  return date;
}

function dateToTimeString(date: Date): string {
  const hh = String(date.getHours()).padStart(2, "0");
  const mm = String(date.getMinutes()).padStart(2, "0");
  return `${hh}:${mm}:00`;
}

export default function SettingsScreen() {
  const theme = useTheme();
  const { data, isPending, isError, error } = useSettings();
  const updateSettings = useUpdateSettings();
  const [permissionDenied, setPermissionDenied] = useState(false);

  const handleToggle = async (enabled: boolean) => {
    setPermissionDenied(false);

    if (!enabled) {
      await cancelDailyReminder();
      updateSettings.mutate({ notification_enabled: false });
      return;
    }

    const granted = await requestNotificationPermission();
    if (!granted) {
      setPermissionDenied(true);
      return;
    }

    const time = data ? timeStringToDate(data.notification_time) : new Date();
    await scheduleDailyReminder(time.getHours(), time.getMinutes());
    updateSettings.mutate({ notification_enabled: true });
  };

  const handleTimeChange = async (_event: unknown, selected?: Date) => {
    if (!selected) return;
    const timeString = dateToTimeString(selected);
    if (data?.notification_enabled) {
      await scheduleDailyReminder(selected.getHours(), selected.getMinutes());
    }
    updateSettings.mutate({ notification_time: timeString });
  };

  return (
    <Screen edges={["top"]}>
      <View style={{ padding: theme.spacing.lg }}>
        {isPending && <LoadingState />}
        {isError && <ErrorState message={error.message} />}

        {data && (
          <>
            <View style={styles.row}>
              <AppText variant="title">Recordatorio diario</AppText>
              <Switch
                value={data.notification_enabled}
                onValueChange={handleToggle}
                trackColor={{ true: theme.colors.accent }}
              />
            </View>

            {permissionDenied && (
              <AppText
                variant="caption"
                style={{ color: theme.colors.error, marginTop: theme.spacing.sm }}
              >
                Necesitas habilitar los permisos de notificación para tu app en la
                configuración del sistema.
              </AppText>
            )}

            {data.notification_enabled && (
              <View style={{ marginTop: theme.spacing.lg }}>
                <AppText variant="label" style={{ marginBottom: theme.spacing.sm }}>
                  Hora
                </AppText>
                <DateTimePicker
                  value={timeStringToDate(data.notification_time)}
                  mode="time"
                  display="spinner"
                  onChange={handleTimeChange}
                />
              </View>
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
  },
});
