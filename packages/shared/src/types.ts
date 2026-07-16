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
  date: string;
  verse: VerseOut;
  reflection: ReflectionOut;
}
