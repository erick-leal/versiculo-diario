import * as Notifications from "expo-notifications";
import * as Device from "expo-device";
import { Platform } from "react-native";

const MORNING_NOTIFICATION_ID = "morning-verse-reminder";
const NIGHT_NOTIFICATION_ID = "night-verse-reminder";

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

async function ensureReminderChannel(): Promise<void> {
  if (Platform.OS === "android") {
    await Notifications.setNotificationChannelAsync("daily-reminder", {
      name: "Recordatorio diario",
      importance: Notifications.AndroidImportance.DEFAULT,
    });
  }
}

export async function scheduleMorningReminder(hour: number, minute: number): Promise<void> {
  await Notifications.cancelScheduledNotificationAsync(MORNING_NOTIFICATION_ID).catch(() => {});
  await ensureReminderChannel();

  await Notifications.scheduleNotificationAsync({
    identifier: MORNING_NOTIFICATION_ID,
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

export async function cancelMorningReminder(): Promise<void> {
  await Notifications.cancelScheduledNotificationAsync(MORNING_NOTIFICATION_ID).catch(() => {});
}

export async function scheduleNightReminder(hour: number, minute: number): Promise<void> {
  await Notifications.cancelScheduledNotificationAsync(NIGHT_NOTIFICATION_ID).catch(() => {});
  await ensureReminderChannel();

  await Notifications.scheduleNotificationAsync({
    identifier: NIGHT_NOTIFICATION_ID,
    content: {
      title: "Versículo Diario",
      body: "Antes de descansar, un momento con la Palabra de hoy.",
    },
    trigger: {
      type: Notifications.SchedulableTriggerInputTypes.DAILY,
      hour,
      minute,
    },
  });
}

export async function cancelNightReminder(): Promise<void> {
  await Notifications.cancelScheduledNotificationAsync(NIGHT_NOTIFICATION_ID).catch(() => {});
}
