import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import type {
  DailyVerseOut,
  PersonalReflectionOut,
  PersonalReflectionUpsert,
} from "@versiculo-diario/shared";

import { apiDelete, apiGet, apiPut } from "./client";

const PERSONAL_REFLECTIONS_KEY = ["personal-reflections"];

export function usePersonalReflections() {
  return useQuery({
    queryKey: PERSONAL_REFLECTIONS_KEY,
    queryFn: () => apiGet<PersonalReflectionOut[]>("/personal-reflections", true),
  });
}

function useSavePersonalReflection() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload: PersonalReflectionUpsert & { dailyVerse: DailyVerseOut }) =>
      apiPut<PersonalReflectionOut>("/personal-reflections", {
        daily_verse_id: payload.daily_verse_id,
        body: payload.body,
      }),
    onMutate: async (payload) => {
      await queryClient.cancelQueries({ queryKey: PERSONAL_REFLECTIONS_KEY });
      const previous = queryClient.getQueryData<PersonalReflectionOut[]>(PERSONAL_REFLECTIONS_KEY);
      const now = new Date().toISOString();
      if (previous) {
        const existing = previous.find((r) => r.daily_verse_id === payload.daily_verse_id);
        const optimisticEntry: PersonalReflectionOut = existing
          ? { ...existing, body: payload.body, updated_at: now }
          : {
              id: -Date.now(),
              daily_verse_id: payload.daily_verse_id,
              body: payload.body,
              created_at: now,
              updated_at: now,
              daily_verse: payload.dailyVerse,
            };
        const next = existing
          ? previous.map((r) => (r.daily_verse_id === payload.daily_verse_id ? optimisticEntry : r))
          : [optimisticEntry, ...previous];
        queryClient.setQueryData(PERSONAL_REFLECTIONS_KEY, next);
      }
      return { previous };
    },
    onError: (_err, _payload, context) => {
      if (context?.previous) {
        queryClient.setQueryData(PERSONAL_REFLECTIONS_KEY, context.previous);
      }
    },
    onSuccess: (data) => {
      const previous = queryClient.getQueryData<PersonalReflectionOut[]>(PERSONAL_REFLECTIONS_KEY);
      if (previous) {
        const next = previous.some((r) => r.daily_verse_id === data.daily_verse_id)
          ? previous.map((r) => (r.daily_verse_id === data.daily_verse_id ? data : r))
          : [data, ...previous];
        queryClient.setQueryData(PERSONAL_REFLECTIONS_KEY, next);
      }
    },
  });
}

function useDeletePersonalReflection() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => apiDelete(`/personal-reflections/${id}`),
    onMutate: async (id) => {
      await queryClient.cancelQueries({ queryKey: PERSONAL_REFLECTIONS_KEY });
      const previous = queryClient.getQueryData<PersonalReflectionOut[]>(PERSONAL_REFLECTIONS_KEY);
      if (previous) {
        queryClient.setQueryData(
          PERSONAL_REFLECTIONS_KEY,
          previous.filter((r) => r.id !== id)
        );
      }
      return { previous };
    },
    onError: (_err, _id, context) => {
      if (context?.previous) {
        queryClient.setQueryData(PERSONAL_REFLECTIONS_KEY, context.previous);
      }
    },
  });
}

export function usePersonalReflectionForDay(dailyVerse: DailyVerseOut) {
  const { data: reflections, isLoading } = usePersonalReflections();
  const save = useSavePersonalReflection();
  const remove = useDeletePersonalReflection();

  const entry = reflections?.find((r) => r.daily_verse_id === dailyVerse.id);

  return {
    entry,
    isLoading,
    save: (body: string, options?: { onSuccess?: () => void; onError?: (error: Error) => void }) =>
      save.mutate({ daily_verse_id: dailyVerse.id, body, dailyVerse }, options),
    remove: (options?: { onSuccess?: () => void; onError?: (error: Error) => void }) => {
      if (entry) remove.mutate(entry.id, options);
    },
    isSaving: save.isPending,
    isRemoving: remove.isPending,
  };
}
