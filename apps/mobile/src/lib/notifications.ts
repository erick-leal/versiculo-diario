import * as Notifications from "expo-notifications";
import * as Device from "expo-device";
import { Platform } from "react-native";

const DAILY_NOTIFICATION_ID = "daily-verse-reminder";

export async function requestNotificationPermission(): Promise<boolean> {
  if (!Device.isDevice) {
    // Los simuladores/emuladores no soportan push/local notifications de forma confiable.
    return false;
  }
  const current = await Notifications.getPermissionsAsync();
  if (current.status === "granted") return true;

  const requested = await Notifications.requestPermissionsAsync();
  return requested.status === "granted";
}

export async function scheduleDailyReminder(hour: number, minute: number): Promise<void> {
  await Notifications.cancelScheduledNotificationAsync(DAILY_NOTIFICATION_ID).catch(() => {});

  if (Platform.OS === "android") {
    await Notifications.setNotificationChannelAsync("daily-reminder", {
      name: "Recordatorio diario",
      importance: Notifications.AndroidImportance.DEFAULT,
    });
  }

  await Notifications.scheduleNotificationAsync({
    identifier: DAILY_NOTIFICATION_ID,
    content: {
      title: "Versículo Diario",
      body: "Tu momento de hoy con la Palabra te espera.",
    },
    trigger: {
      type: Notifications.SchedulableTriggerInputTypes.DAILY,
      hour,
      minute,
    },
  });
}

export async function cancelDailyReminder(): Promise<void> {
  await Notifications.cancelScheduledNotificationAsync(DAILY_NOTIFICATION_ID).catch(() => {});
}
