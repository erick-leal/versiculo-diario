import { Alert } from "react-native";

import { useUpdateSettings } from "../api/useSettings";
import { requestNotificationPermission, scheduleMorningReminder, scheduleNightReminder } from "../lib/notifications";

export function useActivateReminders() {
  const updateSettings = useUpdateSettings();

  return async function activateReminders(): Promise<void> {
    const granted = await requestNotificationPermission();
    if (!granted) {
      Alert.alert(
        "Permiso de notificaciones",
        "Para recibir el recordatorio, habilita las notificaciones de Versículo Diario desde los ajustes del sistema."
      );
      return;
    }

    await scheduleMorningReminder(7, 0);
    await scheduleNightReminder(21, 0);
    updateSettings.mutate({
      morning_reminder_enabled: true,
      night_reminder_enabled: true,
    });
  };
}
