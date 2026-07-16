import type { RefObject } from "react";
import { captureRef } from "react-native-view-shot";
import * as Sharing from "expo-sharing";
import type { View } from "react-native";

export async function shareViewAsImage(viewRef: RefObject<View | null>): Promise<void> {
  if (!viewRef.current) return;

  const uri = await captureRef(viewRef, {
    format: "png",
    quality: 1,
    result: "tmpfile",
  });

  const canShare = await Sharing.isAvailableAsync();
  if (!canShare) return;

  await Sharing.shareAsync(uri, { mimeType: "image/png" });
}
