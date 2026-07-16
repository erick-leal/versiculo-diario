import { ScrollView } from "react-native";

import { useDailyVerse } from "../src/api/useDailyVerse";
import { Screen } from "../src/components/Screen";
import { VerseCard } from "../src/components/VerseCard";
import { LoadingState, ErrorState } from "../src/components/StateMessage";
import { useTheme } from "../src/theme";

export default function HomeScreen() {
  const { data, isPending, isError, error } = useDailyVerse();
  const theme = useTheme();

  return (
    <Screen>
      <ScrollView
        contentContainerStyle={{
          flexGrow: 1,
          justifyContent: "center",
          padding: theme.spacing.lg,
        }}
      >
        {isPending && <LoadingState />}
        {isError && <ErrorState message={error.message} />}
        {data && <VerseCard dailyVerse={data} />}
      </ScrollView>
    </Screen>
  );
}
