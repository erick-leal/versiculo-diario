import { FlatList } from "react-native";

import { useHistory } from "../../src/api/useHistory";
import { Screen } from "../../src/components/Screen";
import { VerseListItem } from "../../src/components/VerseListItem";
import { LoadingState, ErrorState } from "../../src/components/StateMessage";
import { useTheme } from "../../src/theme";

export default function HistoryScreen() {
  const { data, isPending, isError, error } = useHistory();
  const theme = useTheme();

  return (
    <Screen edges={["top"]}>
      {isPending && <LoadingState />}
      {isError && <ErrorState message={error.message} />}
      {data && (
        <FlatList
          data={data}
          keyExtractor={(item) => String(item.id)}
          contentContainerStyle={{ paddingHorizontal: theme.spacing.lg }}
          renderItem={({ item }) => <VerseListItem dailyVerse={item} />}
        />
      )}
    </Screen>
  );
}
