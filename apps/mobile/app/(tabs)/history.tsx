import { ScrollView } from "react-native";

import { useHistory } from "../../src/api/useHistory";
import { HistoryCalendar } from "../../src/components/HistoryCalendar";
import { Screen } from "../../src/components/Screen";
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
        <ScrollView contentContainerStyle={{ paddingHorizontal: theme.spacing.lg }}>
          <HistoryCalendar data={data} />
        </ScrollView>
      )}
    </Screen>
  );
}
