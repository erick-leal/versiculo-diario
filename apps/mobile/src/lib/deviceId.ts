import AsyncStorage from "@react-native-async-storage/async-storage";
import { randomUUID } from "expo-crypto";

const STORAGE_KEY = "device-id";

let cached: string | null = null;

export async function getDeviceId(): Promise<string> {
  if (cached) return cached;

  const stored = await AsyncStorage.getItem(STORAGE_KEY);
  if (stored) {
    cached = stored;
    return stored;
  }

  const id = randomUUID();
  await AsyncStorage.setItem(STORAGE_KEY, id);
  cached = id;
  return id;
}
