import { getDeviceId } from "../lib/deviceId";

const API_URL = process.env.EXPO_PUBLIC_API_URL;

if (!API_URL) {
  throw new Error("Falta EXPO_PUBLIC_API_URL. Definila en apps/mobile/.env");
}

async function request<T>(
  path: string,
  options: { method?: string; body?: unknown; withDeviceId?: boolean } = {}
): Promise<T> {
  const { method = "GET", body, withDeviceId = false } = options;

  const headers: Record<string, string> = {};
  if (body !== undefined) headers["Content-Type"] = "application/json";
  if (withDeviceId) headers["X-Device-Id"] = await getDeviceId();

  const response = await fetch(`${API_URL}${path}`, {
    method,
    headers,
    body: body !== undefined ? JSON.stringify(body) : undefined,
  });

  if (!response.ok) {
    throw new Error(`${path} respondio ${response.status}`);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return response.json() as Promise<T>;
}

export const apiGet = <T>(path: string, withDeviceId = false) =>
  request<T>(path, { withDeviceId });

export const apiPost = <T>(path: string, body: unknown) =>
  request<T>(path, { method: "POST", body, withDeviceId: true });

export const apiPut = <T>(path: string, body: unknown) =>
  request<T>(path, { method: "PUT", body, withDeviceId: true });

export const apiDelete = (path: string) => request<void>(path, { method: "DELETE", withDeviceId: true });
