import os
from datetime import datetime
from tkinter import Button, IntVar, Label, Radiobutton, Text, Tk, filedialog


class ProjectOrganizer:
    def __init__(self):
        self.root = Tk()
        self.root.title("Project Organizer Tool")
        self.setup_ui()

    def setup_ui(self):
        Label(self.root, text="Select Project Folder").pack(pady=5)
        Button(self.root, text="Select Input Folder", command=self.select_input_folder).pack(pady=5)
        Button(self.root, text="Select Output Folder", command=self.select_output_folder).pack(pady=5)
        
        Label(self.root, text="Select Output Format").pack(pady=5)
        self.output_format = IntVar(value=1)
        Radiobutton(self.root, text="TXT Format", variable=self.output_format, value=1).pack()
        Radiobutton(self.root, text="MD Format", variable=self.output_format, value=2).pack()

        self.output_text = Text(self.root, height=10, width=60)
        self.output_text.pack(pady=5)
        Button(self.root, text="Generate Summary", command=self.generate_summary).pack(pady=5)

    def select_input_folder(self):
        self.input_folder_path = filedialog.askdirectory()
        if self.input_folder_path:
            self.output_text.insert("end", f"Input folder selected: {self.input_folder_path}\n")
        else:
            self.output_text.insert("end", "No valid input folder selected. Please try again!\n")

    def select_output_folder(self):
        self.output_folder_path = filedialog.askdirectory()
        if self.output_folder_path:
            self.output_text.insert("end", f"Output folder selected: {self.output_folder_path}\n")
        else:
            self.output_text.insert("end", "No valid output folder selected. Please try again!\n")

    def generate_summary(self):
        if not hasattr(self, 'input_folder_path') or not self.input_folder_path:
            self.output_text.insert("end", "Error: No input folder selected. Please use the 'Select Input Folder' button to choose a folder and try again.\n")
            return

        if not hasattr(self, 'output_folder_path') or not self.output_folder_path:
            self.output_text.insert("end", "Error: No output folder selected. Please use the 'Select Output Folder' button to choose a folder and try again.\n")
            return

        file_extension = "txt" if self.output_format.get() == 1 else "md"
        output_filename = os.path.join(self.output_folder_path, f"project_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{file_extension}")

        excluded_directories = {".git", ".svn", "__pycache__"}
        excluded_files = {".DS_Store", "Thumbs.db"}

        with open(output_filename, "w", encoding="utf-8") as output_file:
            # Write folder structure
            output_file.write("The project file structure is as follows:\n")
            for root, dirs, files in os.walk(self.input_folder_path):
                # Filter out excluded directories
                dirs[:] = [d for d in dirs if d not in excluded_directories]
                level = root.replace(self.input_folder_path, "").count(os.sep)
                indent = "  " * level
                output_file.write(f"{indent}{os.path.basename(root)}/\n")
                for file in files:
                    if file.endswith(".py") and file not in excluded_files:
                        output_file.write(f"{indent}  {file}\n")
            output_file.write("\n")

            # Write Python file content only
            output_file.write("The program code is as follows:\n")
            for root, dirs, files in os.walk(self.input_folder_path):
                # Filter out excluded directories
                dirs[:] = [d for d in dirs if d not in excluded_directories]
                for file in files:
                    if file.endswith(".py") and file not in excluded_files:
                        file_path = os.path.join(root, file)
                        output_file.write(f"\nPath: {file_path}\n")
                        output_file.write("Code:\n")
                        if file_extension == "md":
                            output_file.write("```python\n")
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as code_file:
                            output_file.write(code_file.read())
                        if file_extension == "md":
                            output_file.write("\n```")
                        output_file.write("\n")

        self.output_text.insert("end", f"Summary file generated: {output_filename}\n")

if __name__ == "__main__":
    organizer = ProjectOrganizer()
    organizer.root.mainloop()
