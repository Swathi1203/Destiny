import csv
import re

class CodeTranslator:
    def __init__(self, translation_filename):
        self.translation_mappings = self.load_translation_mappings(translation_filename)

    def load_translation_mappings(self, csv_file):
        translation_mappings = {}
        try:
            with open(csv_file, "r", newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    source_language = row["source_language"]
                    target_language = row["target_language"]
                    pattern = row["pattern"]
                    replacement = row["replacement"]
                    key = (source_language, target_language)
                    if key not in translation_mappings:
                        translation_mappings[key] = []
                    translation_mappings[key].append((pattern, replacement))
        except FileNotFoundError:
            print("Translation CSV file not found.")
        return translation_mappings

    def translate_code(self, source_language, target_language, input_code):
        key = (source_language, target_language)
        if key in self.translation_mappings:
            translation_mapping = self.translation_mappings[key]
            translated_code = input_code
            for pattern, replacement in translation_mapping:
                try:
                    # Use regex to substitute patterns with replacements
                    translated_code = re.sub(pattern, replacement, translated_code)
                except re.error as e:
                    print(f"Error in regex pattern: {e}")
                    return None
            return translated_code
        else:
            print("Translation mapping not found.")
            return None

def main():
    # Create a CodeTranslator instance
    translator = CodeTranslator("translations.csv")

    # Test translations
    delphi_code = "procedure test(a: Integer; b: Integer): Integer;\nbegin\n  Result := a + b;\nend;"
    csharp_code = translator.translate_code("Delphi", "C#", delphi_code)
    java_code = translator.translate_code("Delphi", "Java", delphi_code)
    python_code = translator.translate_code("Delphi", "Python", delphi_code)

    print("Delphi Code:")
    print(delphi_code)
    print("\nC# Code:")
    print(csharp_code)
    print("\nJava Code:")
    print(java_code)
    print("\nPython Code:")
    print(python_code)

if __name__ == "__main__":
    main()
