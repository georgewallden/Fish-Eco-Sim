# src/modules/config_editor/app.py

import tkinter as tk
from tkinter import filedialog, messagebox, Menu, ttk # Added ttk
import os
from . import yaml_io

class ConfigEditorApp:
    def __init__(self, root_window):
        self.root = root_window
        self.root.title("Fish Eco Sim - Config Editor Alpha (a0.1.3.1)")
        self.root.geometry("800x600")

        self.current_filepath = None
        self.config_data = None
        self._editing_item_id = None 
        self._editing_item_key = None 

        self.create_menu()
        self.create_widgets() # New method to create main UI widgets

    def create_menu(self):
        # ... (menu creation code remains the same)
        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)

        file_menu.add_command(label="Open...", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As...", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_app)


    def create_widgets(self):
        # Frame for Treeview and scrollbars
        tree_frame = ttk.Frame(self.root, padding="3 3 3 3")
        tree_frame.pack(expand=True, fill=tk.BOTH)

        # Treeview widget to display YAML data
        self.tree = ttk.Treeview(tree_frame, columns=("Value"), show="tree headings") # show="tree headings" to see column titles
        
        # Define column headings
        self.tree.heading("#0", text="Key / Item", anchor=tk.W) # "#0" is the special tree column
        self.tree.heading("Value", text="Value", anchor=tk.W)

        # Define column widths (optional, but can improve layout)
        self.tree.column("#0", width=300, minwidth=150, stretch=tk.YES)
        self.tree.column("Value", width=400, minwidth=200, stretch=tk.YES)

        # Add scrollbars
        ysb = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        xsb = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=ysb.set, xscrollcommand=xsb.set)

        # Grid layout for tree and scrollbars within the frame
        self.tree.grid(row=0, column=0, sticky=tk.NSEW)
        ysb.grid(row=0, column=1, sticky=tk.NS)
        xsb.grid(row=1, column=0, sticky=tk.EW)

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Placeholder for where data will be displayed.
        # For now, we'll populate it in open_file upon loading.

    def on_tree_double_click(self, event):
        """ Handle double-click event on the Treeview. """
        region = self.tree.identify_region(event.x, event.y)
        
        # We only want to edit if the "Value" column is clicked.
        # identify_column returns '#0', '#1', etc. '#1' is our "Value" column.
        column_id = self.tree.identify_column(event.x)

        if region == "cell" and column_id == "#1": # "#1" corresponds to the "Value" column
            item_id = self.tree.identify_row(event.y) # Get the iid of the clicked row
            if not item_id:
                return

            self._editing_item_id = item_id
            # For a0.1.3.2 (flat dictionary), the key is the text of the item in the tree column
            self._editing_item_key = self.tree.item(item_id, "text") 

            # Get cell bounding box for placing the Entry widget
            x, y, width, height = self.tree.bbox(item_id, column="Value")

            # Get current value
            current_values = self.tree.item(item_id, "values")
            if not current_values: # Should not happen if column exists
                return 
            current_value_str = str(current_values[0]) # Value is the first (and only) in 'values' tuple

            # Create and place the Entry widget
            entry_var = tk.StringVar(value=current_value_str)
            entry_editor = ttk.Entry(self.tree, textvariable=entry_var) # Place it on the tree itself
            entry_editor.place(x=x, y=y, width=width, height=height, anchor=tk.NW)
            
            entry_editor.focus_set()
            entry_editor.selection_range(0, tk.END)

            # Bind events to the Entry widget
            entry_editor.bind("<Return>", lambda e, ed=entry_editor, iid=item_id, key=self._editing_item_key: self.on_edit_confirm(e, ed, iid, key))
            entry_editor.bind("<KP_Enter>", lambda e, ed=entry_editor, iid=item_id, key=self._editing_item_key: self.on_edit_confirm(e, ed, iid, key)) # Numpad Enter
            entry_editor.bind("<FocusOut>", lambda e, ed=entry_editor, iid=item_id, key=self._editing_item_key: self.on_edit_confirm(e, ed, iid, key))
            entry_editor.bind("<Escape>", lambda e, ed=entry_editor: ed.destroy())

    def on_edit_confirm(self, event, entry_editor, item_id, item_key_or_path):
        new_value_str = entry_editor.get()
        entry_editor.destroy() # Destroy editor first

        # For a0.1.3.2, we assume a flat dictionary and item_key_or_path is the simple key.
        # Later, for nested structures, item_key_or_path will be more complex (e.g., a tuple path).
        
        if isinstance(self.config_data, dict) and item_key_or_path in self.config_data:
            original_value = self.config_data[item_key_or_path]
            
            # Attempt to cast to original type (very basic validation for now)
            # More robust validation comes in a0.1.3.5
            try:
                if isinstance(original_value, bool):
                    # Handle common string representations of booleans
                    if new_value_str.lower() in ("true", "yes", "1"):
                        new_value = True
                    elif new_value_str.lower() in ("false", "no", "0"):
                        new_value = False
                    else:
                        # If not a recognized boolean string, keep as string or raise error
                        # For now, let's try to keep it as bool if original was bool
                        # This part is tricky without full schema validation
                        raise ValueError("Invalid boolean string") 
                elif isinstance(original_value, int):
                    new_value = int(new_value_str)
                elif isinstance(original_value, float):
                    new_value = float(new_value_str)
                else: # Assume string or other types that don't need specific casting
                    new_value = new_value_str
            except ValueError:
                messagebox.showerror("Edit Error", f"Invalid value '{new_value_str}' for key '{item_key_or_path}'.\nCould not convert to original type: {type(original_value).__name__}")
                # Re-display original value in tree (or do nothing if value wasn't changed yet)
                # For simplicity now, the tree won't update on error here.
                # self.tree.set(item_id, column="Value", value=str(original_value))
                return

            # Update in-memory config_data
            self.config_data[item_key_or_path] = new_value
            # Update Treeview display
            self.tree.set(item_id, column="Value", value=str(new_value)) 
        
        # Clear editing state
        self._editing_item_id = None
        self._editing_item_key = None

    def display_config_data(self):
        # Clear existing items in the treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        if self.config_data is None:
            return # Nothing to display

        # For a0.1.3.1, we assume self.config_data is a flat dictionary
        if isinstance(self.config_data, dict):
            for key, value in self.config_data.items():
                # Insert item into the tree:
                # parent='', index='end', iid=None (auto-generated), text=key, values=(value,)
                # For a flat structure, parent is always '' (the root)
                self.tree.insert("", tk.END, text=str(key), values=(str(value),)) 
        elif isinstance(self.config_data, list):
            # Rudimentary list display for flat lists (though flat_test.yaml is a dict)
            for index, item in enumerate(self.config_data):
                self.tree.insert("", tk.END, text=f"[{index}]", values=(str(item),))
        else:
            # Handle cases where config_data might be a single scalar (e.g. just a number or string from YAML)
            self.tree.insert("", tk.END, text="(root)", values=(str(self.config_data),))


    def open_file(self):
        filepath = filedialog.askopenfilename(
            title="Open YAML File",
            filetypes=(("YAML files", "*.yaml *.yml"), ("All files", "*.*"))
        )
        if not filepath:
            self.display_config_data() # Clear display if user cancelled
            return

        try:
            self.config_data = yaml_io.load_yaml_file(filepath)
            self.current_filepath = filepath # Set current_filepath only on successful load
            if self.config_data is not None:
                self.root.title(f"Fish Eco Sim - Config Editor Alpha - {os.path.basename(filepath)}")
            else: # Handles empty YAML file which results in self.config_data being None
                self.root.title(f"Fish Eco Sim - Config Editor Alpha - {os.path.basename(filepath)} (Empty)")
            
            self.display_config_data() # Display the newly loaded data

            # No need for messagebox here anymore as data will be displayed (or lack thereof)
            # messagebox.showinfo("File Opened", f"Successfully loaded: {os.path.basename(filepath)}")

        except FileNotFoundError:
            messagebox.showerror("Error", f"File not found: {filepath}")
            self.current_filepath = None
            self.config_data = None
            self.root.title("Fish Eco Sim - Config Editor Alpha") # Reset title
            self.display_config_data() # Clear display
        except yaml_io.yaml.YAMLError as e:
            messagebox.showerror("Error", f"Error parsing YAML file: {os.path.basename(filepath)}\n\n{e}")
            self.current_filepath = None
            self.config_data = None
            self.root.title("Fish Eco Sim - Config Editor Alpha") # Reset title
            self.display_config_data() # Clear display
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred while opening file:\n{e}")
            self.current_filepath = None
            self.config_data = None
            self.root.title("Fish Eco Sim - Config Editor Alpha") # Reset title
            self.display_config_data() # Clear display

    def save_file(self):
        # ... (save_file code remains the same)
        if self.current_filepath:
            if self.config_data is None:
                pass 

            try:
                yaml_io.save_yaml_file(self.config_data, self.current_filepath)
                messagebox.showinfo("File Saved", f"Successfully saved: {os.path.basename(self.current_filepath)}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {os.path.basename(self.current_filepath)}\n\n{e}")
        else:
            self.save_file_as()

    def save_file_as(self):
        # ... (save_file_as code remains the same)
        filepath = filedialog.asksaveasfilename(
            title="Save YAML File As...",
            defaultextension=".yaml",
            filetypes=(("YAML files", "*.yaml *.yml"), ("All files", "*.*"))
        )
        if not filepath: 
            return

        try:
            yaml_io.save_yaml_file(self.config_data, filepath)
            self.current_filepath = filepath
            self.root.title(f"Fish Eco Sim - Config Editor Alpha - {os.path.basename(filepath)}")
            messagebox.showinfo("File Saved", f"Successfully saved to: {os.path.basename(filepath)}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file: {os.path.basename(filepath)}\n\n{e}")


    def exit_app(self):
        # ... (exit_app code remains the same)
        self.root.quit()

if __name__ == '__main__':
    root = tk.Tk()
    app = ConfigEditorApp(root)
    root.mainloop()