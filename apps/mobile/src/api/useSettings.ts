import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import type { AppSettingsOut, AppSettingsUpdate } from "@versiculo-diario/shared";

import { apiGet, apiPut } from "./client";

const SETTINGS_KEY = ["settings"];

export function useSettings() {
  return useQuery({
    queryKey: SETTINGS_KEY,
    queryFn: () => apiGet<AppSettingsOut>("/settings", true),
  });
}

export function useUpdateSettings() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload: AppSettingsUpdate) => apiPut<AppSettingsOut>("/settings", payload),
    onSuccess: (data) => {
      queryClient.setQueryData(SETTINGS_KEY, data);
    },
  });
}
