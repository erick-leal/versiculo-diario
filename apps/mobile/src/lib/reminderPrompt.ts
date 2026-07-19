import AsyncStorage from "@react-native-async-storage/async-storage";

const SEEN_KEY = "reminder-prompt-dismissed";
const SESSION_KEY = "reminder-prompt-session-count";

// Flag compartido: si el usuario acepta o descarta el modal (Ajustes) o el
// banner (Inicio), no se le vuelve a mostrar ninguno de los dos.
export async function hasSeenReminderPrompt(): Promise<boolean> {
  const value = await AsyncStorage.getItem(SEEN_KEY);
  return value === "true";
}

export async function markReminderPromptSeen(): Promise<void> {
  await AsyncStorage.setItem(SEEN_KEY, "true");
}

// Lee cuantas veces se abrio la app ANTES de esta vez, y registra esta
// apertura para la proxima. Se llama una vez por lanzamiento (Inicio monta
// una sola vez por sesion), asi que no hay condicion de carrera entre
// lectura y escritura.
export async function getSessionCountAndRecordOpen(): Promise<number> {
  const raw = await AsyncStorage.getItem(SESSION_KEY);
  const priorSessions = raw ? parseInt(raw, 10) : 0;
  await AsyncStorage.setItem(SESSION_KEY, String(priorSessions + 1));
  return priorSessions;
}
