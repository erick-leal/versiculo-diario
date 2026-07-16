import { ActivityIndicator, ScrollView, StyleSheet, Text, View } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

import { useDailyVerse } from "../src/api/useDailyVerse";

export default function HomeScreen() {
  const { data, isPending, isError, error } = useDailyVerse();

  return (
    <SafeAreaView style={styles.container} edges={["top", "bottom"]}>
      <ScrollView contentContainerStyle={styles.content}>
        {isPending && <ActivityIndicator size="large" />}

        {isError && <Text style={styles.errorText}>{error.message}</Text>}

        {data && (
          <View>
            <Text style={styles.reference}>{data.verse.reference}</Text>
            <Text style={styles.verseText}>{data.verse.text}</Text>

            <View style={styles.divider} />

            {data.reflection.title && (
              <Text style={styles.reflectionTitle}>{data.reflection.title}</Text>
            )}
            <Text style={styles.reflectionBody}>{data.reflection.body}</Text>
          </View>
        )}
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#FBFAF7",
  },
  content: {
    flexGrow: 1,
    justifyContent: "center",
    padding: 28,
  },
  reference: {
    fontSize: 15,
    fontWeight: "600",
    color: "#8A7B5C",
    marginBottom: 12,
    textTransform: "uppercase",
    letterSpacing: 0.5,
  },
  verseText: {
    fontSize: 22,
    lineHeight: 32,
    color: "#1F1B16",
    fontWeight: "500",
  },
  divider: {
    height: 1,
    backgroundColor: "#E4DFD3",
    marginVertical: 28,
  },
  reflectionTitle: {
    fontSize: 17,
    fontWeight: "600",
    color: "#1F1B16",
    marginBottom: 8,
  },
  reflectionBody: {
    fontSize: 16,
    lineHeight: 24,
    color: "#4A443B",
  },
  errorText: {
    fontSize: 15,
    color: "#B3261E",
    textAlign: "center",
  },
});
