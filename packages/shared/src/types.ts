export interface VerseOut {
  reference: string;
  text: string;
  translation: string;
}

export interface ReflectionOut {
  title: string | null;
  body: string;
  author_name: string | null;
}

export interface DailyVerseOut {
  id: number;
  date: string;
  verse: VerseOut;
  reflection: ReflectionOut;
}

export interface FavoriteOut {
  id: number;
  created_at: string;
  daily_verse: DailyVerseOut;
}

export type DarkModePreference = "light" | "dark" | "system";

export interface AppSettingsOut {
  dark_mode: DarkModePreference;
  notification_enabled: boolean;
  notification_time: string; // "HH:MM:SS"
}

export type AppSettingsUpdate = Partial<AppSettingsOut>;
