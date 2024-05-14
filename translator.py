import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import re
from PIL import Image, ImageTk
import wikipedia
import csv
import spacy

# Load English tokenizer, tagger, parser, and NER (Named Entity Recognition) model
nlp = spacy.load("en_core_web_sm")

def generate_algorithm_from_code(code):
    # Check if the code contains addition operation
    if "a + b" in code:
        algorithm = """
        Algorithm for Addition:

        1. Start
        2. Input two numbers: a and b
        3. Compute the sum of a and b
        4. Display the result
        5. Stop
        """
    else:
        algorithm = "No addition operation detected in the provided code."

    return algorithm

class CodeTranslatorApp:
    def __init__(self, master):
        self.master = master
        master.title("Legacy Code Converter")

        # Styling
        self.master.configure(bg="#ADD8E6")  # Light blue background
        self.style = ttk.Style()
        self.style.configure('TLabel', background="#ADD8E6", font=('Helvetica', 12))  # Adjusted font size and background color for labels
        self.style.configure('TButton', background="#4CAF50", font=('Helvetica', 12))  # Adjusted font size and colors for buttons

        # Heading
        self.heading_label = ttk.Label(master, text="Legacy Code Converter", font=('Helvetica', 16, 'bold'), background="#ADD8E6")  # Centered heading
        self.heading_label.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        # Label and Text area for input
        self.input_label = ttk.Label(master, text="Enter Legacy Code:", background="#ADD8E6")
        self.input_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.input_text = tk.Text(master, height=20, width=80, font=('Helvetica', 12))  # Bigger font size for input text
        self.input_text.grid(row=2, column=0, columnspan=4, padx=10, pady=5, sticky="nsew")

        # Label and Text area for output
        self.output_label = ttk.Label(master, text="Translated Code:", background="#ADD8E6")
        self.output_label.grid(row=1, column=4, padx=10, pady=5, sticky="w")
        self.output_text = tk.Text(master, height=20, width=80, font=('Helvetica', 12))  # Bigger font size for output text
        self.output_text.grid(row=2, column=4, columnspan=4, padx=10, pady=5, sticky="nsew")

        # Dropdown menu for selecting target language
        self.target_language_label = ttk.Label(master, text="Select Target Language:", background="#ADD8E6")
        self.target_language_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.target_language_var = tk.StringVar(master)
        self.target_language_dropdown = ttk.OptionMenu(master, self.target_language_var, "C#", "C#", "Java", "Python")
        self.target_language_dropdown.grid(row=4, column=0, padx=10, pady=5, sticky="w")

        # Translate button
        self.translate_button = ttk.Button(master, text="Translate", command=self.translate_code)
        self.translate_button.grid(row=5, column=0, padx=10, pady=5, sticky="w")

        # Documentation button
        self.documentation_button = ttk.Button(master, text="Documentation", command=self.show_documentation)
        self.documentation_button.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        # Algorithm button
        self.algorithm_button = ttk.Button(master, text="Algorithm", command=self.show_algorithm)
        self.algorithm_button.grid(row=5, column=2, padx=10, pady=5, sticky="w")

        # NLP button
        self.nlp_button = ttk.Button(master, text="Analyze with NLP", command=self.analyze_with_nlp)
        self.nlp_button.grid(row=5, column=3, padx=10, pady=5, sticky="w")

    def load_translation_mappings(self, csv_file):
        translation_mappings = {}
        try:
            with open(csv_file, "r", newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    pattern = row["pattern"]  # Use lowercase column name
                    replacement = row["replacement"]  # Use lowercase column name
                    language = row["target_language"]  # Use target_language column for language
                    if language not in translation_mappings:
                        translation_mappings[language] = {}
                    translation_mappings[language][pattern] = replacement
        except FileNotFoundError:
            messagebox.showerror("Error", "Translation CSV file not found.")
        return translation_mappings

    def translate_code(self):
        # Get input code and target language
        input_code = self.input_text.get("1.0", "end-1c")
        target_language = self.target_language_var.get()

        # Load translation mappings from CSV file
        self.translation_mappings = self.load_translation_mappings("translations.csv")

        # Translate code based on target language
        if target_language in self.translation_mappings:
            translation_mapping = self.translation_mappings[target_language]
            translated_code = input_code
            for pattern, replacement in translation_mapping.items():
                translated_code = re.sub(pattern, replacement, translated_code)
        else:
            translated_code = "Selected target language is not supported."

        # Update output text area with translated code
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", translated_code)

    def show_documentation(self):
        documentation = """
        Addition Program Documentation:
        
        Overview:
        This program allows users to perform addition of two numbers. It provides a user-friendly interface to input numbers, compute their sum, and view the result. Additionally, it supports speech recognition for number input and displays the algorithm used for addition.
        
        Functionality:
        1. Input Numbers: Users can input two numbers either manually in the input text area or through speech recognition using the microphone icon.
        2. Perform Addition: Clicking the 'Add' button computes the sum of the two numbers entered.
        3. View Result: The result of the addition operation is displayed in the output text area.
        4. Speech Recognition: Users can utilize speech recognition by clicking the microphone icon and speaking the numbers they want to add.
        5. Generate Algorithm: The 'Algorithm' button generates and displays the algorithm used for addition in a separate window.
        6. Save Documentation: Users have the option to view this documentation or save it to a file for future reference.
        
        Instructions:
        1. Enter Numbers: Input the first number followed by the second number in the input text area.
        2. Add Numbers: Click the 'Add' button to calculate the sum of the entered numbers.
        3. View Result: The result of the addition will be displayed in the output text area.
        4. Speech Input: To use speech recognition, click the microphone icon and speak clearly to provide numbers for addition.
        5. View Algorithm: Click the 'Algorithm' button to see the detailed algorithm for addition.
        6. Save Documentation: To save this documentation, click the 'Save to File' button and choose a location on your device.
        
        Note: This program is specifically designed for addition of two numbers and does not support other arithmetic operations. It aims to provide a simple and intuitive interface for performing addition tasks.
        """
        # Display documentation in a new window
        doc_window = tk.Toplevel(self.master)
        doc_window.title("Addition Program Documentation")
        
        # Create a text widget to display documentation
        doc_text = tk.Text(doc_window, height=20, width=100, font=('Helvetica', 12))
        doc_text.pack(padx=10, pady=10)
        
        # Insert documentation text into the text widget
        doc_text.insert(tk.END, documentation)
        doc_text.configure(state='disabled')  # Make the text widget read-only
        
        # Add a button to save documentation to a file
        save_button = ttk.Button(doc_window, text="Save to File", command=lambda: self.save_documentation_to_file(documentation))
        save_button.pack(pady=10)

    def show_algorithm(self):
        code = self.input_text.get("1.0", tk.END)  # Get code from input text area

        # Placeholder for algorithm generation based on code
        algorithm = generate_algorithm_from_code(code)

        # Display algorithm in a new window
        algorithm_window = tk.Toplevel(self.master)
        algorithm_window.title("Algorithm")
        
        # Create a text widget to display algorithm
        algorithm_text = tk.Text(algorithm_window, height=20, width=80, font=('Helvetica', 12))
        algorithm_text.pack(padx=10, pady=10)
        
        # Insert algorithm text into the text widget
        algorithm_text.insert(tk.END, algorithm)
        algorithm_text.configure(state='disabled')  # Make the text widget read-only

    def analyze_with_nlp(self):
        code = self.input_text.get("1.0", tk.END)  # Get code from input text area
        
        # Process the code with spaCy NLP pipeline
        doc = nlp(code)
        
        # Extract entities from the code
        entities = [ent.text for ent in doc.ents]
        
        # Extract verbs from the code
        verbs = [token.lemma_ for token in doc if token.pos_ == "VERB"]
        
        # Display NLP analysis in a messagebox
        messagebox.showinfo("NLP Analysis", f"Entities: {', '.join(entities)}\nVerbs: {', '.join(verbs)}")

def main():
    root = tk.Tk()
    app = CodeTranslatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
