import { useQuery } from "@tanstack/react-query";
import type { DailyVerseOut } from "@versiculo-diario/shared";

import { apiGet } from "./client";

export function useDailyVerseById(id: number) {
  return useQuery({
    queryKey: ["daily-verse", id],
    queryFn: () => apiGet<DailyVerseOut>(`/daily-verse/${id}`),
  });
}
