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
    onMutate: async (payload) => {
      await queryClient.cancelQueries({ queryKey: SETTINGS_KEY });
      const previous = queryClient.getQueryData<AppSettingsOut>(SETTINGS_KEY);
      if (previous) {
        queryClient.setQueryData(SETTINGS_KEY, { ...previous, ...payload });
      }
      return { previous };
    },
    onError: (_err, _payload, context) => {
      if (context?.previous) {
        queryClient.setQueryData(SETTINGS_KEY, context.previous);
      }
    },
    onSuccess: (data) => {
      queryClient.setQueryData(SETTINGS_KEY, data);
    },
  });
}
