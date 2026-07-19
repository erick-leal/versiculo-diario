import { Alert, Platform, Pressable, StyleSheet, Switch, useColorScheme, View } from "react-native";
import { DateTimePickerAndroid } from "@react-native-community/datetimepicker";
import { Feather } from "@expo/vector-icons";

import { useSettings, useUpdateSettings } from "../../src/api/useSettings";
import { AppText } from "../../src/components/AppText";
import { ReminderPrompt } from "../../src/components/ReminderPrompt";
import { Screen } from "../../src/components/Screen";
import { LoadingState, ErrorState } from "../../src/components/StateMessage";
import { ThemeModeSelector } from "../../src/components/ThemeModeSelector";
import {
  cancelMorningReminder,
  cancelNightReminder,
  requestNotificationPermission,
  scheduleMorningReminder,
  scheduleNightReminder,
} from "../../src/lib/notifications";
import { useTheme } from "../../src/theme";

type ReminderKind = "morning" | "night";

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

interface ReminderSectionProps {
  label: string;
  enabled: boolean;
  time: string;
  onToggle: (enabled: boolean) => void;
  onPressTime: () => void;
}

function ReminderSection({ label, enabled, time, onToggle, onPressTime }: ReminderSectionProps) {
  const theme = useTheme();

  return (
    <View style={{ marginTop: theme.spacing.xl }}>
      <AppText variant="label" style={{ marginBottom: theme.spacing.sm }}>
        {label}
      </AppText>
      <View style={styles.row}>
        <AppText variant="body">Recibir recordatorio</AppText>
        <Switch value={enabled} onValueChange={onToggle} trackColor={{ true: theme.colors.accent }} />
      </View>
      {enabled && (
        <Pressable onPress={onPressTime} style={styles.row} accessibilityRole="button">
          <AppText variant="body">Hora</AppText>
          <View style={styles.timeValue}>
            <AppText variant="body" style={{ color: theme.colors.accent }}>
              {formatTime(time)}
            </AppText>
            <Feather name="chevron-right" size={18} color={theme.colors.textSecondary} />
          </View>
        </Pressable>
      )}
    </View>
  );
}

export default function SettingsScreen() {
  const theme = useTheme();
  const systemScheme = useColorScheme();
  const { data, isPending, isError, error } = useSettings();
  const updateSettings = useUpdateSettings();

  async function handleToggleReminder(kind: ReminderKind, enabled: boolean) {
    if (!data) return;

    if (!enabled) {
      if (kind === "morning") {
        await cancelMorningReminder();
        updateSettings.mutate({ morning_reminder_enabled: false });
      } else {
        await cancelNightReminder();
        updateSettings.mutate({ night_reminder_enabled: false });
      }
      return;
    }

    const granted = await requestNotificationPermission();
    if (!granted) {
      Alert.alert(
        "Permiso de notificaciones",
        "Para recibir el recordatorio, habilita las notificaciones de Versículo Diario desde los ajustes del sistema."
      );
      return;
    }

    if (kind === "morning") {
      const { hour, minute } = parseTime(data.morning_reminder_time);
      await scheduleMorningReminder(hour, minute);
      updateSettings.mutate({ morning_reminder_enabled: true });
    } else {
      const { hour, minute } = parseTime(data.night_reminder_time);
      await scheduleNightReminder(hour, minute);
      updateSettings.mutate({ night_reminder_enabled: true });
    }
  }

  function handleOpenTimePicker(kind: ReminderKind) {
    // La API declarativa (<DateTimePicker> montado) deja el dialogo de
    // Android "pegado" - la API imperativa se autogestiona (abre y cierra
    // sola), evitando ese bug.
    if (!data || Platform.OS !== "android") return;

    const { hour, minute } = parseTime(
      kind === "morning" ? data.morning_reminder_time : data.night_reminder_time
    );
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
        const timeString = `${String(newHour).padStart(2, "0")}:${String(newMinute).padStart(2, "0")}:00`;

        if (kind === "morning") {
          scheduleMorningReminder(newHour, newMinute);
          updateSettings.mutate({ morning_reminder_time: timeString });
        } else {
          scheduleNightReminder(newHour, newMinute);
          updateSettings.mutate({ night_reminder_time: timeString });
        }
      },
    });
  }

  return (
    <Screen edges={["top"]}>
      <ReminderPrompt settings={data} />
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

            <ReminderSection
              label="Recordatorio de la mañana"
              enabled={data.morning_reminder_enabled}
              time={data.morning_reminder_time}
              onToggle={(enabled) => handleToggleReminder("morning", enabled)}
              onPressTime={() => handleOpenTimePicker("morning")}
            />

            <ReminderSection
              label="Recordatorio de la noche"
              enabled={data.night_reminder_enabled}
              time={data.night_reminder_time}
              onToggle={(enabled) => handleToggleReminder("night", enabled)}
              onPressTime={() => handleOpenTimePicker("night")}
            />
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
