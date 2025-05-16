# src/modules/config_editor/app.py

import tkinter as tk
from tkinter import filedialog, messagebox, Menu, ttk
import os
# Ensure you have PyYAML installed: pip install PyYAML
# For the yaml_io module, if it's in the same directory:
from . import yaml_io # Relative import for package structure

class ConfigEditorApp:
    def __init__(self, root_window):
        self.root = root_window
        self.root.title("Fish Eco Sim - Config Editor Alpha (a0.1.3.2)") # Updated version
        self.root.geometry("800x600")

        self.current_filepath = None
        self.config_data = None
        self._editing_item_id = None # To store the iid of the item being edited
        # self._editing_item_key = None # We'll get the key directly from item_id for flat dicts

        self.create_menu()
        self.create_widgets()

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

    def create_widgets(self):
        tree_frame = ttk.Frame(self.root, padding="3 3 3 3")
        tree_frame.pack(expand=True, fill=tk.BOTH)

        self.tree = ttk.Treeview(tree_frame, columns=("Value"), show="tree headings")
        self.tree.heading("#0", text="Key / Item", anchor=tk.W)
        self.tree.heading("Value", text="Value", anchor=tk.W)
        self.tree.column("#0", width=250, minwidth=150, stretch=tk.NO) # Key column usually less wide
        self.tree.column("Value", width=450, minwidth=200, stretch=tk.YES)

        ysb = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        xsb = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=ysb.set, xscrollcommand=xsb.set)

        self.tree.grid(row=0, column=0, sticky=tk.NSEW)
        ysb.grid(row=0, column=1, sticky=tk.NS)
        xsb.grid(row=1, column=0, sticky=tk.EW)
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        # Bind double-click event for editing
        self.tree.bind("<Double-1>", self.on_tree_double_click)
        # Allow editing on pressing Enter/Return when an item is selected
        self.tree.bind("<Return>", self.on_tree_return_key)


    def on_tree_return_key(self, event):
        """Handle Return key press on a selected tree item to start editing its value."""
        selected_item_id = self.tree.focus() # Get the iid of the focused item
        if not selected_item_id:
            return
        
        # Simulate a double click on the value cell of the selected item
        # We need to get the coordinates for the value cell of the selected_item_id
        # This is a bit of a workaround to reuse the double-click logic
        # A more direct way would be to call a refactored edit_cell(item_id) method.
        
        # For now, let's directly call the edit setup logic if we're sure it's a value cell we want to edit
        # Get the bounding box of the "Value" column for the selected item
        try:
            # Ensure the column exists before getting bbox
            # Treeview columns are #0, #1, #2, ...
            # If "Value" is the first column after the tree column, it's #1
            bbox = self.tree.bbox(selected_item_id, column="#1") # Column alias for 'Value'
            if bbox: # If bbox is valid (item and column visible)
                 self._setup_cell_editor(selected_item_id, column_id_to_edit="#1")
        except tk.TclError:
            # This can happen if the item or column is not visible or doesn't exist
            pass


    def on_tree_double_click(self, event):
        """ Handle double-click event on the Treeview. """
        region = self.tree.identify_region(event.x, event.y)
        column_id_clicked = self.tree.identify_column(event.x) # e.g., "#1" for "Value"
        item_id = self.tree.identify_row(event.y)

        if not item_id: # Clicked outside of any item
            return

        if region == "cell" and column_id_clicked == "#1": # "#1" is the "Value" column
            self._setup_cell_editor(item_id, column_id_clicked)

    def _setup_cell_editor(self, item_id, column_id_to_edit):
        """Creates and places an Entry widget for editing a cell."""
        # Prevent re-entry if an editor is already active for this item (though unlikely with current flow)
        if hasattr(self, '_active_editor') and self._active_editor and self._active_editor.winfo_exists():
            self._active_editor.destroy()

        self._editing_item_id = item_id
        # For a flat dictionary, the key is the item_id itself (as we set iid=key in display_config_data)
        # Or, if using default iids, it's self.tree.item(item_id, "text")
        # Let's assume iid IS the key for flat dicts for now.
        item_key = self.tree.item(item_id, "text") # This should be the key for flat dict

        x, y, width, height = self.tree.bbox(item_id, column=column_id_to_edit)
        
        current_values_tuple = self.tree.item(item_id, "values")
        if not current_values_tuple: return # Should have a value
        current_value_str = str(current_values_tuple[0]) # Value is the first element

        entry_var = tk.StringVar(value=current_value_str)
        self._active_editor = ttk.Entry(self.tree, textvariable=entry_var)
        self._active_editor.place(x=x, y=y, width=width, height=height, anchor=tk.NW)
        
        self._active_editor.focus_set()
        self._active_editor.selection_range(0, tk.END)

        # Pass item_key (actual dictionary key) to on_edit_confirm
        self._active_editor.bind("<Return>", lambda e, ed=self._active_editor, iid=item_id, key=item_key: self.on_edit_confirm(e, ed, iid, key))
        self._active_editor.bind("<KP_Enter>", lambda e, ed=self._active_editor, iid=item_id, key=item_key: self.on_edit_confirm(e, ed, iid, key))
        self._active_editor.bind("<FocusOut>", lambda e, ed=self._active_editor, iid=item_id, key=item_key: self.on_edit_confirm(e, ed, iid, key))
        self._active_editor.bind("<Escape>", lambda e, ed=self._active_editor: self.on_edit_cancel(ed))

    def on_edit_cancel(self, editor_widget):
        editor_widget.destroy()
        self._editing_item_id = None
        if hasattr(self, '_active_editor'):
            del self._active_editor


    def on_edit_confirm(self, event, entry_editor, item_id, dict_key):
        # Check if editor still exists (might be destroyed by a quick FocusOut then Enter)
        if not entry_editor.winfo_exists():
            return

        new_value_str = entry_editor.get()
        # It's important to destroy the editor *before* any messagebox that might steal focus
        # and trigger another FocusOut on the (now defunct) editor.
        entry_editor.destroy() 
        if hasattr(self, '_active_editor'): # Clean up reference
            del self._active_editor


        # For a0.1.3.2, we assume a flat dictionary and dict_key is the simple key.
        if isinstance(self.config_data, dict) and dict_key in self.config_data:
            original_value = self.config_data[dict_key]
            new_value = None # Initialize to avoid UnboundLocalError

            try:
                if isinstance(original_value, bool):
                    if new_value_str.lower() in ("true", "yes", "1", "on"):
                        new_value = True
                    elif new_value_str.lower() in ("false", "no", "0", "off"):
                        new_value = False
                    else:
                        raise ValueError(f"'{new_value_str}' is not a valid boolean representation.")
                elif isinstance(original_value, int):
                    new_value = int(new_value_str)
                elif isinstance(original_value, float):
                    new_value = float(new_value_str)
                else: # Assume string or other types that don't need specific casting
                    new_value = new_value_str
                
                # Update in-memory config_data
                self.config_data[dict_key] = new_value
                # Update Treeview display
                self.tree.set(item_id, column="Value", value=str(new_value))

            except ValueError as ve:
                messagebox.showerror("Edit Error", f"Invalid value for '{dict_key}': '{new_value_str}'.\nType Error: {ve}\nPlease enter a value of type: {type(original_value).__name__}")
                # To revert tree display if error:
                self.tree.set(item_id, column="Value", value=str(original_value))
                return
        
        self._editing_item_id = None


    def display_config_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        if self.config_data is None:
            return

        if isinstance(self.config_data, dict):
            for key, value in self.config_data.items():
                # Using key as item id (iid) for flat dictionaries is simple and effective here.
                # This makes it easy to get the key back when an item is selected/edited.
                self.tree.insert("", tk.END, text=str(key), values=(str(value),), iid=str(key))
        elif isinstance(self.config_data, list):
            for index, item in enumerate(self.config_data):
                # For lists, using a prefixed index as iid. Editing lists is more complex.
                list_item_id = f"__list_item_{index}__"
                self.tree.insert("", tk.END, text=f"[{index}]", values=(str(item),), iid=list_item_id)
        else: # Scalar value at root
            self.tree.insert("", tk.END, text="(root)", values=(str(self.config_data),), iid="__root_scalar__")


    def open_file(self):
        filepath = filedialog.askopenfilename(
            title="Open YAML File",
            filetypes=(("YAML files", "*.yaml *.yml"), ("All files", "*.*"))
        )
        if not filepath:
            # self.display_config_data() # Clear display if user cancelled, or do nothing
            return

        try:
            self.config_data = yaml_io.load_yaml_file(filepath)
            self.current_filepath = filepath
            if self.config_data is not None: # Could be an empty file (None) or actual data
                self.root.title(f"Fish Eco Sim - Config Editor Alpha - {os.path.basename(filepath)}")
            else: # Handles empty YAML file
                self.root.title(f"Fish Eco Sim - Config Editor Alpha - {os.path.basename(filepath)} (Empty)")
            self.display_config_data() # Display the newly loaded data or clear if empty
        except FileNotFoundError:
            messagebox.showerror("Error", f"File not found: {filepath}")
            self.current_filepath = None; self.config_data = None
            self.root.title("Fish Eco Sim - Config Editor Alpha")
            self.display_config_data() # Clear display
        except yaml_io.yaml.YAMLError as e:
            messagebox.showerror("Error", f"Error parsing YAML file: {os.path.basename(filepath)}\n\n{e}")
            self.current_filepath = None; self.config_data = None
            self.root.title("Fish Eco Sim - Config Editor Alpha")
            self.display_config_data()
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred while opening file:\n{e}")
            self.current_filepath = None; self.config_data = None
            self.root.title("Fish Eco Sim - Config Editor Alpha")
            self.display_config_data()

    def save_file(self):
        if self.current_filepath:
            try:
                yaml_io.save_yaml_file(self.config_data, self.current_filepath)
                messagebox.showinfo("File Saved", f"Successfully saved: {os.path.basename(self.current_filepath)}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {os.path.basename(self.current_filepath)}\n\n{e}")
        else:
            self.save_file_as()

    def save_file_as(self):
        filepath = filedialog.asksaveasfilename(
            title="Save YAML File As...",
            defaultextension=".yaml",
            filetypes=(("YAML files", "*.yaml *.yml"), ("All files", "*.*"))
        )
        if not filepath: return

        try:
            yaml_io.save_yaml_file(self.config_data, filepath)
            self.current_filepath = filepath
            self.root.title(f"Fish Eco Sim - Config Editor Alpha - {os.path.basename(filepath)}")
            messagebox.showinfo("File Saved", f"Successfully saved to: {os.path.basename(filepath)}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file: {os.path.basename(filepath)}\n\n{e}")

    def exit_app(self):
        self.root.quit()

if __name__ == '__main__':
    root = tk.Tk()
    app = ConfigEditorApp(root)
    root.mainloop()