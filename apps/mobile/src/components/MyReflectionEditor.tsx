import { useEffect, useState } from "react";
import { ActivityIndicator, Alert, Pressable, StyleSheet, TextInput, View } from "react-native";
import { Feather } from "@expo/vector-icons";
import type { DailyVerseOut } from "@versiculo-diario/shared";

import { usePersonalReflectionForDay } from "../api/usePersonalReflections";
import { useTheme } from "../theme";
import { AppText } from "./AppText";

export function MyReflectionEditor({ dailyVerse }: { dailyVerse: DailyVerseOut }) {
  const theme = useTheme();
  const { entry, save, remove, isSaving, isRemoving, isLoading } = usePersonalReflectionForDay(dailyVerse);
  const [editing, setEditing] = useState(false);
  const [draft, setDraft] = useState(entry?.body ?? "");

  useEffect(() => {
    if (!editing) {
      setDraft(entry?.body ?? "");
    }
  }, [entry?.body, editing]);

  function handleSave() {
    const trimmed = draft.trim();
    if (!trimmed) return;
    setEditing(false);
    save(trimmed, {
      onError: () => {
        setEditing(true);
        Alert.alert("No se pudo guardar", "Intenta de nuevo en unos segundos.");
      },
    });
  }

  function handleCancel() {
    setDraft(entry?.body ?? "");
    setEditing(false);
  }

  return (
    <View
      style={[
        styles.container,
        {
          borderColor: theme.colors.border,
          marginTop: theme.spacing.xl,
          paddingTop: theme.spacing.md,
        },
      ]}
    >
      <View style={styles.header}>
        <AppText variant="label">Mi reflexión</AppText>
        {!editing && !isLoading && (
          <Pressable
            onPress={() => setEditing(true)}
            hitSlop={8}
            accessibilityRole="button"
            accessibilityLabel={entry ? "Editar mi reflexión" : "Escribir mi reflexión"}
          >
            <Feather
              name={entry ? "edit-2" : "plus"}
              size={18}
              color={theme.colors.accent}
            />
          </Pressable>
        )}
      </View>

      {isLoading ? (
        <View style={{ marginTop: theme.spacing.sm, alignItems: "flex-start" }}>
          <ActivityIndicator size="small" color={theme.colors.accent} />
        </View>
      ) : editing ? (
        <>
          <TextInput
            value={draft}
            onChangeText={setDraft}
            multiline
            autoFocus
            placeholder="Escribe lo que este versículo significa para ti..."
            placeholderTextColor={theme.colors.textSecondary}
            style={[
              styles.input,
              {
                color: theme.colors.textPrimary,
                fontFamily: theme.fonts.body,
                marginTop: theme.spacing.sm,
              },
            ]}
          />
          <View style={[styles.actions, { marginTop: theme.spacing.sm }]}>
            {entry && (
              <Pressable
                onPress={() => {
                  setEditing(false);
                  remove({
                    onError: () => {
                      setEditing(true);
                      Alert.alert("No se pudo eliminar", "Intenta de nuevo en unos segundos.");
                    },
                  });
                }}
                disabled={isRemoving}
                accessibilityRole="button"
                style={styles.actionButton}
              >
                <AppText variant="body" style={{ color: theme.colors.error }}>
                  Eliminar
                </AppText>
              </Pressable>
            )}
            <Pressable onPress={handleCancel} accessibilityRole="button" style={styles.actionButton}>
              <AppText variant="body">Cancelar</AppText>
            </Pressable>
            <Pressable
              onPress={handleSave}
              disabled={isSaving || !draft.trim()}
              accessibilityRole="button"
              style={styles.actionButton}
            >
              <AppText variant="body" style={{ color: theme.colors.accent }}>
                Guardar
              </AppText>
            </Pressable>
          </View>
        </>
      ) : entry ? (
        <AppText variant="body" style={{ marginTop: theme.spacing.sm }}>
          {entry.body}
        </AppText>
      ) : (
        <AppText
          variant="body"
          style={{ marginTop: theme.spacing.sm, color: theme.colors.textSecondary }}
        >
          Aún no has escrito nada sobre este versículo.
        </AppText>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    borderTopWidth: 1,
  },
  header: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
  },
  input: {
    minHeight: 80,
    maxHeight: 140,
    textAlignVertical: "top",
    fontSize: 16,
    lineHeight: 22,
  },
  actions: {
    flexDirection: "row",
    justifyContent: "flex-end",
    gap: 16,
  },
  actionButton: {
    minHeight: 44,
    justifyContent: "center",
  },
});
