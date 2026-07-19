import { useEffect, useState } from "react";
import { Pressable, StyleSheet, View } from "react-native";
import { Feather } from "@expo/vector-icons";
import type { AppSettingsOut } from "@versiculo-diario/shared";

import { useActivateReminders } from "../hooks/useActivateReminders";
import { getSessionCountAndRecordOpen, hasSeenReminderPrompt, markReminderPromptSeen } from "../lib/reminderPrompt";
import { useTheme } from "../theme";
import { AppText } from "./AppText";

interface ReminderBannerProps {
  settings: AppSettingsOut | undefined;
}

export function ReminderBanner({ settings }: ReminderBannerProps) {
  const theme = useTheme();
  const activateReminders = useActivateReminders();
  const [priorSessions, setPriorSessions] = useState<number | null>(null);
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    getSessionCountAndRecordOpen().then(setPriorSessions);
  }, []);

  useEffect(() => {
    if (!settings || priorSessions === null) return;
    if (settings.morning_reminder_enabled || settings.night_reminder_enabled) return;
    if (priorSessions < 1) return;

    let cancelled = false;
    hasSeenReminderPrompt().then((seen) => {
      if (!seen && !cancelled) setVisible(true);
    });

    return () => {
      cancelled = true;
    };
  }, [settings, priorSessions]);

  async function handleDismiss() {
    setVisible(false);
    await markReminderPromptSeen();
  }

  async function handleAccept() {
    setVisible(false);
    await markReminderPromptSeen();
    await activateReminders();
  }

  if (!visible) return null;

  return (
    <View
      style={[
        styles.card,
        { backgroundColor: theme.colors.surface, borderColor: theme.colors.border, marginTop: theme.spacing.xl },
      ]}
    >
      <View style={styles.row}>
        <Feather name="bell" size={18} color={theme.colors.accent} />
        <AppText variant="body" style={{ flex: 1, marginLeft: theme.spacing.sm }}>
          ¿Querés que te recordemos tu momento diario con la Palabra?
        </AppText>
        <Pressable onPress={handleDismiss} hitSlop={8} accessibilityRole="button" accessibilityLabel="Cerrar">
          <Feather name="x" size={16} color={theme.colors.textSecondary} />
        </Pressable>
      </View>
      <Pressable
        onPress={handleAccept}
        style={[styles.acceptButton, { backgroundColor: theme.colors.accent }]}
        accessibilityRole="button"
      >
        <AppText variant="label" style={{ color: "#FFFFFF" }}>
          Sí, recordame
        </AppText>
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    borderRadius: 14,
    borderWidth: 1,
    padding: 14,
  },
  row: {
    flexDirection: "row",
    alignItems: "center",
  },
  acceptButton: {
    minHeight: 40,
    borderRadius: 10,
    alignItems: "center",
    justifyContent: "center",
    marginTop: 12,
  },
});
