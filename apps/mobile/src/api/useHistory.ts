import { useQuery } from "@tanstack/react-query";
import type { DailyVerseOut } from "@versiculo-diario/shared";

import { apiGet } from "./client";

export function useHistory() {
  return useQuery({
    queryKey: ["history"],
    queryFn: () => apiGet<DailyVerseOut[]>("/history"),
  });
}
