import { useEffect, useState } from "react";
import { Modal, Pressable, StyleSheet, View } from "react-native";
import type { AppSettingsOut } from "@versiculo-diario/shared";

import { useActivateReminders } from "../hooks/useActivateReminders";
import { hasSeenReminderPrompt, markReminderPromptSeen } from "../lib/reminderPrompt";
import { useTheme } from "../theme";
import { AppText } from "./AppText";

interface ReminderPromptProps {
  settings: AppSettingsOut | undefined;
}

export function ReminderPrompt({ settings }: ReminderPromptProps) {
  const theme = useTheme();
  const activateReminders = useActivateReminders();
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    if (!settings) return;
    if (settings.morning_reminder_enabled || settings.night_reminder_enabled) return;

    let cancelled = false;
    hasSeenReminderPrompt().then((seen) => {
      if (!seen && !cancelled) setVisible(true);
    });

    return () => {
      cancelled = true;
    };
  }, [settings]);

  async function handleDismiss() {
    setVisible(false);
    await markReminderPromptSeen();
  }

  async function handleAccept() {
    setVisible(false);
    await markReminderPromptSeen();
    await activateReminders();
  }

  return (
    <Modal visible={visible} transparent animationType="fade" onRequestClose={handleDismiss}>
      <View style={styles.backdrop}>
        <View style={[styles.card, { backgroundColor: theme.colors.background }]}>
          <AppText variant="title" style={{ marginBottom: theme.spacing.sm }}>
            No te pierdas tu versículo
          </AppText>
          <AppText variant="body" style={{ marginBottom: theme.spacing.lg }}>
            Te avisamos en la mañana y en la noche para que no olvides tu momento diario con la Palabra.
          </AppText>

          <Pressable
            onPress={handleAccept}
            style={[styles.primaryButton, { backgroundColor: theme.colors.accent }]}
          >
            <AppText variant="title" style={{ color: "#FFFFFF" }}>
              Sí, recordame
            </AppText>
          </Pressable>

          <Pressable onPress={handleDismiss} style={styles.secondaryButton} accessibilityRole="button">
            <AppText variant="body" style={{ color: theme.colors.textSecondary }}>
              Ahora no
            </AppText>
          </Pressable>
        </View>
      </View>
    </Modal>
  );
}

const styles = StyleSheet.create({
  backdrop: {
    flex: 1,
    backgroundColor: "rgba(0,0,0,0.4)",
    justifyContent: "center",
    alignItems: "center",
    padding: 24,
  },
  card: {
    width: "100%",
    borderRadius: 20,
    padding: 24,
  },
  primaryButton: {
    minHeight: 52,
    borderRadius: 14,
    alignItems: "center",
    justifyContent: "center",
  },
  secondaryButton: {
    minHeight: 44,
    alignItems: "center",
    justifyContent: "center",
    marginTop: 4,
  },
});
