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

export interface PersonalReflectionOut {
  id: number;
  daily_verse_id: number;
  body: string;
  created_at: string;
  updated_at: string;
  daily_verse: DailyVerseOut;
}

export interface PersonalReflectionUpsert {
  daily_verse_id: number;
  body: string;
}

export type DarkModePreference = "light" | "dark" | "system";

export interface AppSettingsOut {
  dark_mode: DarkModePreference;
  morning_reminder_enabled: boolean;
  morning_reminder_time: string; // "HH:MM:SS"
  night_reminder_enabled: boolean;
  night_reminder_time: string; // "HH:MM:SS"
}

export type AppSettingsUpdate = Partial<AppSettingsOut>;
