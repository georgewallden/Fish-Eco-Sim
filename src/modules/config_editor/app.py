# src/modules/config_editor/app.py

import tkinter as tk
from tkinter import filedialog, messagebox, Menu
import os

# Import our YAML I/O functions
# Assuming app.py is in the same directory as yaml_io.py or yaml_io is accessible via the package
from . import yaml_io  # Relative import for modules within the same package

class ConfigEditorApp:
    def __init__(self, root_window):
        self.root = root_window
        self.root.title("Fish Eco Sim - Config Editor Alpha (a0.1.1.3)")
        
        # Set initial window size (optional, but good for consistency)
        self.root.geometry("800x600") 

        self.current_filepath = None
        self.config_data = None # This will hold the loaded YAML data as a Python dict/list

        self.create_menu()

    def create_menu(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)

        file_menu.add_command(label="Open...", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As...", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_app)

    def open_file(self):
        filepath = filedialog.askopenfilename(
            title="Open YAML File",
            filetypes=(("YAML files", "*.yaml *.yml"), ("All files", "*.*"))
        )
        if not filepath: # User cancelled
            return

        try:
            self.config_data = yaml_io.load_yaml_file(filepath)
            if self.config_data is not None:
                self.current_filepath = filepath
                self.root.title(f"Fish Eco Sim - Config Editor Alpha - {os.path.basename(filepath)}")
                # In a0.1.3.Z we will display this data. For now, just acknowledge.
                messagebox.showinfo("File Opened", f"Successfully loaded: {os.path.basename(filepath)}\n(Content display not yet implemented)")
            else:
                # load_yaml_file returns None for empty files, which is valid.
                # Or it might return None if we change its error handling (currently raises exceptions).
                # For now, let's assume if no exception, None means an empty but valid YAML.
                self.current_filepath = filepath
                self.root.title(f"Fish Eco Sim - Config Editor Alpha - {os.path.basename(filepath)} (Empty)")
                messagebox.showinfo("File Opened (Empty)", f"Successfully loaded empty file: {os.path.basename(filepath)}")
        
        except FileNotFoundError:
            messagebox.showerror("Error", f"File not found: {filepath}")
            self.current_filepath = None # Reset if open failed
            self.config_data = None
        except yaml_io.yaml.YAMLError as e: # Catching the specific YAMLError from yaml_io
            messagebox.showerror("Error", f"Error parsing YAML file: {os.path.basename(filepath)}\n\n{e}")
            self.current_filepath = None # Reset if open failed
            self.config_data = None
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred while opening file:\n{e}")
            self.current_filepath = None # Reset if open failed
            self.config_data = None

    def save_file(self):
        if self.current_filepath:
            if self.config_data is None: 
                # This case might happen if an empty file was loaded, 
                # or if config_data was cleared due to an error.
                # Saving 'None' is usually desired as an empty YAML representation.
                # Or, you might want to prevent saving if data is None and not from an empty file explicitly.
                # For now, we'll allow saving None, PyYAML handles it.
                pass # Allow saving None

            try:
                yaml_io.save_yaml_file(self.config_data, self.current_filepath)
                messagebox.showinfo("File Saved", f"Successfully saved: {os.path.basename(self.current_filepath)}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {os.path.basename(self.current_filepath)}\n\n{e}")
        else:
            # If no current filepath, "Save" should act like "Save As"
            self.save_file_as()

    def save_file_as(self):
        # if self.config_data is None:
        #     messagebox.showwarning("Save As", "No data loaded to save.")
        #     return
        # Allow saving even if config_data is None (represents an empty file)

        filepath = filedialog.asksaveasfilename(
            title="Save YAML File As...",
            defaultextension=".yaml",
            filetypes=(("YAML files", "*.yaml *.yml"), ("All files", "*.*"))
        )
        if not filepath: # User cancelled
            return

        try:
            yaml_io.save_yaml_file(self.config_data, filepath)
            self.current_filepath = filepath
            self.root.title(f"Fish Eco Sim - Config Editor Alpha - {os.path.basename(filepath)}")
            messagebox.showinfo("File Saved", f"Successfully saved to: {os.path.basename(filepath)}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file: {os.path.basename(filepath)}\n\n{e}")


    def exit_app(self):
        # Could add a "are you sure if unsaved changes" check later
        self.root.quit()

if __name__ == '__main__':
    root = tk.Tk()
    app = ConfigEditorApp(root)
    root.mainloop()