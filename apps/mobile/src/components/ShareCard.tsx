import { forwardRef } from "react";
import { ImageBackground, StyleSheet, View } from "react-native";
import type { DailyVerseOut } from "@versiculo-diario/shared";

import { AppText } from "./AppText";

export const SHARE_BACKGROUNDS = {
  cream: require("../../assets/share-backgrounds/cream.jpg"),
  charcoal: require("../../assets/share-backgrounds/charcoal.jpg"),
  gold: require("../../assets/share-backgrounds/gold.jpg"),
};

export type ShareBackgroundKey = keyof typeof SHARE_BACKGROUNDS;

const TEXT_COLOR: Record<ShareBackgroundKey, string> = {
  cream: "#1F1B16",
  charcoal: "#F5F1E8",
  gold: "#F5F1E8",
};

interface ShareCardProps {
  dailyVerse: DailyVerseOut;
  background: ShareBackgroundKey;
}

export const ShareCard = forwardRef<View, ShareCardProps>(({ dailyVerse, background }, ref) => {
  const textColor = TEXT_COLOR[background];

  return (
    <View ref={ref} collapsable={false} style={styles.container}>
      <ImageBackground source={SHARE_BACKGROUNDS[background]} style={styles.background}>
        <View style={styles.content}>
          <AppText variant="label" style={[styles.reference, { color: textColor }]}>
            {dailyVerse.verse.reference}
          </AppText>
          <AppText variant="verse" style={[styles.verseText, { color: textColor }]}>
            {dailyVerse.verse.text}
          </AppText>
        </View>
        <AppText variant="caption" style={[styles.wordmark, { color: textColor }]}>
          Versículo Diario
        </AppText>
      </ImageBackground>
    </View>
  );
});

const styles = StyleSheet.create({
  container: {
    width: 300,
    aspectRatio: 9 / 16,
    borderRadius: 20,
    overflow: "hidden",
  },
  background: {
    flex: 1,
    justifyContent: "center",
    padding: 28,
  },
  content: {
    gap: 16,
  },
  reference: {
    textAlign: "center",
    opacity: 0.85,
  },
  verseText: {
    textAlign: "center",
    fontSize: 22,
    lineHeight: 32,
  },
  wordmark: {
    position: "absolute",
    bottom: 20,
    left: 0,
    right: 0,
    textAlign: "center",
    opacity: 0.7,
  },
});
