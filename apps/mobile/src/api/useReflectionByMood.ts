import { useQuery } from "@tanstack/react-query";
import type { DailyVerseOut } from "@versiculo-diario/shared";

import { apiGet } from "./client";

export function useReflectionByMood(mood: string, excludeId?: number) {
  return useQuery({
    queryKey: ["reflection-by-mood", mood, excludeId],
    queryFn: () => {
      const params = new URLSearchParams({ mood });
      if (excludeId !== undefined) params.set("exclude_id", String(excludeId));
      return apiGet<DailyVerseOut>(`/reflections/by-mood?${params.toString()}`);
    },
  });
}
