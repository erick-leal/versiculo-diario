export const MOOD_TAGS = [
  "ansiedad",
  "tristeza",
  "duelo",
  "gratitud",
  "esperanza",
  "duda",
  "fortaleza",
  "paz",
  "gozo",
  "agotamiento",
] as const;

export type MoodTag = (typeof MOOD_TAGS)[number];

export const MOOD_TAG_LABELS: Record<MoodTag, string> = {
  ansiedad: "Ansiedad",
  tristeza: "Tristeza",
  duelo: "Duelo",
  gratitud: "Gratitud",
  esperanza: "Esperanza",
  duda: "Duda",
  fortaleza: "Fortaleza",
  paz: "Paz",
  gozo: "Gozo",
  agotamiento: "Agotamiento",
};
