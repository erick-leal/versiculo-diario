import { useRef, useState } from "react";
import { Modal, Pressable, StyleSheet, View } from "react-native";
import type { DailyVerseOut } from "@versiculo-diario/shared";

import { usePersonalReflectionForDay } from "../api/usePersonalReflections";
import { useTheme } from "../theme";
import { AppText } from "./AppText";
import { ShareCard, SHARE_BACKGROUNDS, type ShareBackgroundKey } from "./ShareCard";
import { shareViewAsImage } from "../lib/shareImage";

const BACKGROUND_KEYS = Object.keys(SHARE_BACKGROUNDS) as ShareBackgroundKey[];

interface ShareSheetProps {
  dailyVerse: DailyVerseOut;
  visible: boolean;
  onClose: () => void;
}

export function ShareSheet({ dailyVerse, visible, onClose }: ShareSheetProps) {
  const theme = useTheme();
  const { entry } = usePersonalReflectionForDay(dailyVerse);
  const [background, setBackground] = useState<ShareBackgroundKey>("cream");
  const [includeReflection, setIncludeReflection] = useState(false);
  const [sharing, setSharing] = useState(false);
  const cardRef = useRef<View>(null);

  const handleShare = async () => {
    setSharing(true);
    try {
      await shareViewAsImage(cardRef);
    } finally {
      setSharing(false);
    }
  };

  return (
    <Modal visible={visible} animationType="slide" transparent onRequestClose={onClose}>
      <View style={styles.backdrop}>
        <View style={[styles.sheet, { backgroundColor: theme.colors.background }]}>
          <View style={styles.header}>
            <AppText variant="title">Compartir</AppText>
            <Pressable onPress={onClose} hitSlop={12} style={styles.closeButton}>
              <AppText variant="body">Cerrar</AppText>
            </Pressable>
          </View>

          <View style={styles.preview}>
            <ShareCard
              ref={cardRef}
              dailyVerse={dailyVerse}
              background={background}
              personalReflection={includeReflection ? entry?.body : undefined}
            />
          </View>

          {entry && (
            <View style={styles.segmentRow}>
              <Pressable
                onPress={() => setIncludeReflection(false)}
                style={[
                  styles.segmentButton,
                  {
                    borderColor: theme.colors.border,
                    backgroundColor: !includeReflection ? theme.colors.accent : "transparent",
                  },
                ]}
                accessibilityRole="button"
              >
                <AppText
                  variant="label"
                  style={{ color: !includeReflection ? theme.colors.background : theme.colors.textPrimary }}
                >
                  Solo versículo
                </AppText>
              </Pressable>
              <Pressable
                onPress={() => setIncludeReflection(true)}
                style={[
                  styles.segmentButton,
                  {
                    borderColor: theme.colors.border,
                    backgroundColor: includeReflection ? theme.colors.accent : "transparent",
                    marginLeft: 10,
                  },
                ]}
                accessibilityRole="button"
              >
                <AppText
                  variant="label"
                  style={{ color: includeReflection ? theme.colors.background : theme.colors.textPrimary }}
                >
                  + Mi reflexión
                </AppText>
              </Pressable>
            </View>
          )}

          <View style={styles.swatchRow}>
            {BACKGROUND_KEYS.map((key) => (
              <Pressable
                key={key}
                onPress={() => setBackground(key)}
                style={[
                  styles.swatch,
                  { borderColor: background === key ? theme.colors.accent : "transparent" },
                ]}
              >
                <View style={[styles.swatchInner, swatchPreviewStyle(key)]} />
              </Pressable>
            ))}
          </View>

          <Pressable
            onPress={handleShare}
            disabled={sharing}
            style={[styles.shareButton, { backgroundColor: theme.colors.accent }]}
          >
            <AppText variant="title" style={{ color: "#FFFFFF" }}>
              {sharing ? "Preparando..." : "Compartir"}
            </AppText>
          </Pressable>
        </View>
      </View>
    </Modal>
  );
}

function swatchPreviewStyle(key: ShareBackgroundKey) {
  const colors: Record<ShareBackgroundKey, string> = {
    cream: "#EDE6D6",
    charcoal: "#1E1B16",
    gold: "#3A2F1D",
  };
  return { backgroundColor: colors[key] };
}

const styles = StyleSheet.create({
  backdrop: {
    flex: 1,
    backgroundColor: "rgba(0,0,0,0.4)",
    justifyContent: "flex-end",
  },
  sheet: {
    borderTopLeftRadius: 24,
    borderTopRightRadius: 24,
    paddingTop: 20,
    paddingBottom: 40,
    paddingHorizontal: 24,
    alignItems: "center",
  },
  header: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    width: "100%",
    marginBottom: 20,
  },
  closeButton: {
    minHeight: 44,
    justifyContent: "center",
  },
  preview: {
    marginBottom: 20,
  },
  segmentRow: {
    flexDirection: "row",
    width: "100%",
    marginBottom: 20,
  },
  segmentButton: {
    flex: 1,
    minHeight: 44,
    alignItems: "center",
    justifyContent: "center",
    borderWidth: 1,
    borderRadius: 8,
  },
  swatchRow: {
    flexDirection: "row",
    gap: 14,
    marginBottom: 24,
  },
  swatch: {
    width: 44,
    height: 44,
    borderRadius: 22,
    borderWidth: 2,
    alignItems: "center",
    justifyContent: "center",
  },
  swatchInner: {
    width: 32,
    height: 32,
    borderRadius: 16,
  },
  shareButton: {
    width: "100%",
    minHeight: 52,
    borderRadius: 14,
    alignItems: "center",
    justifyContent: "center",
  },
});
