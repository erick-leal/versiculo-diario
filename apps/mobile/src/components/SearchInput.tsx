import { StyleSheet, TextInput, View } from "react-native";
import { Feather } from "@expo/vector-icons";

import { useTheme } from "../theme";

interface SearchInputProps {
  value: string;
  onChangeText: (text: string) => void;
  placeholder?: string;
}

export function SearchInput({ value, onChangeText, placeholder = "Buscar..." }: SearchInputProps) {
  const theme = useTheme();

  return (
    <View
      style={[
        styles.container,
        { backgroundColor: theme.colors.surface, borderColor: theme.colors.border },
      ]}
    >
      <Feather name="search" size={16} color={theme.colors.textSecondary} />
      <TextInput
        value={value}
        onChangeText={onChangeText}
        placeholder={placeholder}
        placeholderTextColor={theme.colors.textSecondary}
        style={[
          styles.input,
          { color: theme.colors.textPrimary, fontFamily: theme.fonts.body, marginLeft: theme.spacing.sm },
        ]}
        autoCapitalize="none"
        autoCorrect={false}
        returnKeyType="search"
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: "row",
    alignItems: "center",
    minHeight: 44,
    paddingHorizontal: 12,
    borderWidth: 1,
    borderRadius: 8,
  },
  input: {
    flex: 1,
    fontSize: 16,
  },
});
