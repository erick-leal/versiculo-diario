import AsyncStorage from "@react-native-async-storage/async-storage";

const MAX_ENTRIES = 20;

export interface ViewedEntry {
  id: number;
  reference: string;
  date: string;
}

function todayKey(): string {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, "0");
  const day = String(now.getDate()).padStart(2, "0");
  return `viewed-today:${year}-${month}-${day}`;
}

export async function getViewedToday(): Promise<ViewedEntry[]> {
  const raw = await AsyncStorage.getItem(todayKey());
  if (!raw) return [];
  try {
    return JSON.parse(raw) as ViewedEntry[];
  } catch {
    return [];
  }
}

export async function recordViewed(entry: ViewedEntry): Promise<void> {
  const current = await getViewedToday();
  const withoutDuplicate = current.filter((item) => item.id !== entry.id);
  const updated = [entry, ...withoutDuplicate].slice(0, MAX_ENTRIES);
  await AsyncStorage.setItem(todayKey(), JSON.stringify(updated));
}
