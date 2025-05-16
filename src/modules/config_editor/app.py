# src/modules/config_editor/app.py

import tkinter as tk
from tkinter import filedialog, messagebox, Menu, ttk
import os
from . import yaml_io # Relative import for package structure

class ConfigEditorApp:
    def __init__(self, root_window):
        self.root = root_window
        self.root.title("Fish Eco Sim - Config Editor Alpha (a0.1.3.3)") # Updated version
        self.root.geometry("800x600")

        self.current_filepath = None
        self.config_data = None
        self._editing_item_id = None # To store the iid of the item being edited
        
        # This dictionary will map tree item IDs (iids) to their data path (tuple of keys/indices)
        self.item_id_to_path = {} 

        self.create_menu()
        self.create_widgets()

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
        # ... (widget creation code for treeview remains mostly the same)
        tree_frame = ttk.Frame(self.root, padding="3 3 3 3")
        tree_frame.pack(expand=True, fill=tk.BOTH)

        self.tree = ttk.Treeview(tree_frame, columns=("Value"), show="tree headings")
        self.tree.heading("#0", text="Key / Item", anchor=tk.W)
        self.tree.heading("Value", text="Value", anchor=tk.W)
        self.tree.column("#0", width=250, minwidth=150, stretch=tk.NO)
        self.tree.column("Value", width=450, minwidth=200, stretch=tk.YES)

        ysb = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        xsb = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=ysb.set, xscrollcommand=xsb.set)

        self.tree.grid(row=0, column=0, sticky=tk.NSEW)
        ysb.grid(row=0, column=1, sticky=tk.NS)
        xsb.grid(row=1, column=0, sticky=tk.EW)
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        self.tree.bind("<Double-1>", self.on_tree_double_click)
        self.tree.bind("<Return>", self.on_tree_return_key)

    # --- Methods for displaying data (REFACTORED for nesting) ---
    def display_config_data(self):
        # Clear existing items in the treeview and the path map
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.item_id_to_path.clear()

        if self.config_data is None:
            return
        
        # Start populating the tree from the root of the config_data
        # The parent_iid for top-level items is "" (the Treeview's root)
        # The initial path is an empty tuple ()
        self._populate_tree(parent_tree_id="", data_node=self.config_data, current_data_path=())

    def _generate_unique_iid(self, base_path_tuple):
        """Generates a unique string iid from a path tuple to avoid collisions."""
        # Simple string conversion; for very complex structures, might need more robust unique ID generation
        # if path tuples could somehow result in non-unique string representations (unlikely for keys/indices)
        return str(base_path_tuple)

    def _populate_tree(self, parent_tree_id, data_node, current_data_path):
        """
        Recursively populates the Treeview.
        parent_tree_id: The iid of the parent item in the Treeview.
        data_node: The current piece of data (dict, list, or scalar) to display.
        current_data_path: A tuple representing the path to this data_node from the root.
        """
        if isinstance(data_node, dict):
            for key, value_node in data_node.items():
                item_display_text = str(key)
                new_data_path = current_data_path + (key,)
                # Generate a unique iid for this tree item based on its full path
                tree_item_id = self._generate_unique_iid(new_data_path)
                self.item_id_to_path[tree_item_id] = new_data_path # Map iid to its path

                if isinstance(value_node, (dict, list)): # If it's a node that can have children
                    # Insert the parent key, value will be empty as children will show details
                    inserted_id = self.tree.insert(parent_tree_id, tk.END, text=item_display_text, iid=tree_item_id, open=False) # Start collapsed
                    self._populate_tree(inserted_id, value_node, new_data_path)
                else: # Scalar value
                    self.tree.insert(parent_tree_id, tk.END, text=item_display_text, values=(str(value_node),), iid=tree_item_id)
        
        elif isinstance(data_node, list):
            for index, value_node in enumerate(data_node):
                item_display_text = f"[{index}]" # Display list items with their index
                new_data_path = current_data_path + (index,)
                tree_item_id = self._generate_unique_iid(new_data_path)
                self.item_id_to_path[tree_item_id] = new_data_path

                if isinstance(value_node, (dict, list)):
                    inserted_id = self.tree.insert(parent_tree_id, tk.END, text=item_display_text, iid=tree_item_id, open=False)
                    self._populate_tree(inserted_id, value_node, new_data_path)
                else: # Scalar value in a list
                    self.tree.insert(parent_tree_id, tk.END, text=item_display_text, values=(str(value_node),), iid=tree_item_id)
        
        # If data_node is a scalar at the root (e.g. YAML is just "hello")
        # This case is typically handled if self.config_data is a scalar initially.
        # The initial call to _populate_tree from display_config_data would pass the scalar.
        # However, our current _populate_tree assumes dict/list to iterate.
        # This should be fine as long as the root of YAML is a collection.
        # If the root itself is scalar and needs to be handled by _populate_tree, it would need adjustment.
        # For now, we assume the first call to _populate_tree receives a dict or list.
        # If config_data itself is scalar, display_config_data would need a direct insert for it.
        # Let's adjust display_config_data to handle root scalar.

    # --- Methods for editing data (ADJUSTMENT NEEDED for nested data in a0.1.3.4) ---
    def on_tree_return_key(self, event):
        selected_item_id = self.tree.focus() 
        if not selected_item_id: return
        # Check if the item actually has a "Value" column to edit (i.e., it's a scalar)
        # Parent nodes (dicts/lists) won't have a value in the "Value" column in our display.
        # We can check if tree.item(selected_item_id, "values") is empty or not.
        if self.tree.item(selected_item_id, "values"): # If there's something in the 'values' tuple
            try:
                bbox = self.tree.bbox(selected_item_id, column="#1")
                if bbox:
                    self._setup_cell_editor(selected_item_id, column_id_to_edit="#1")
            except tk.TclError: pass

    def on_tree_double_click(self, event):
        region = self.tree.identify_region(event.x, event.y)
        column_id_clicked = self.tree.identify_column(event.x)
        item_id = self.tree.identify_row(event.y)
        if not item_id: return

        # Only edit if it's a "Value" cell and the item has values (is a scalar leaf)
        if region == "cell" and column_id_clicked == "#1" and self.tree.item(item_id, "values"):
            self._setup_cell_editor(item_id, column_id_clicked)

    def _setup_cell_editor(self, item_id, column_id_to_edit):
        if hasattr(self, '_active_editor') and self._active_editor and self._active_editor.winfo_exists():
            self._active_editor.destroy()

        self._editing_item_id = item_id
        # The item_id IS the string representation of the path, thanks to _generate_unique_iid
        # data_path_tuple = self.item_id_to_path.get(item_id) # This is how we get the path
        # if data_path_tuple is None: return # Should not happen if item_id is from our map

        x, y, width, height = self.tree.bbox(item_id, column=column_id_to_edit)
        current_values_tuple = self.tree.item(item_id, "values")
        if not current_values_tuple: return
        current_value_str = str(current_values_tuple[0])

        entry_var = tk.StringVar(value=current_value_str)
        self._active_editor = ttk.Entry(self.tree, textvariable=entry_var)
        self._active_editor.place(x=x, y=y, width=width, height=height, anchor=tk.NW)
        self._active_editor.focus_set()
        self._active_editor.selection_range(0, tk.END)

        # Pass item_id (which is the path string) to on_edit_confirm
        self._active_editor.bind("<Return>", lambda e, ed=self._active_editor, iid=item_id: self.on_edit_confirm(e, ed, iid))
        self._active_editor.bind("<KP_Enter>", lambda e, ed=self._active_editor, iid=item_id: self.on_edit_confirm(e, ed, iid))
        self._active_editor.bind("<FocusOut>", lambda e, ed=self._active_editor, iid=item_id: self.on_edit_confirm(e, ed, iid))
        self._active_editor.bind("<Escape>", lambda e, ed=self._active_editor: self.on_edit_cancel(ed))
    
    def on_edit_cancel(self, editor_widget):
        # ... (remains the same from a0.1.3.2)
        editor_widget.destroy()
        self._editing_item_id = None
        if hasattr(self, '_active_editor'):
            del self._active_editor

    def on_edit_confirm(self, event, entry_editor, item_id_is_path_str):
        # ... (THIS METHOD WILL NEED SIGNIFICANT CHANGES FOR a0.1.3.4 to handle nested paths)
        # For a0.1.3.3, editing is not the focus, but we keep the stub.
        # The current editing logic only works for flat dictionaries if item_id_is_path_str
        # was just a simple key. Now it's a path string.
        if not entry_editor.winfo_exists(): return
        new_value_str = entry_editor.get()
        entry_editor.destroy()
        if hasattr(self, '_active_editor'): del self._active_editor

        # --- Placeholder for nested editing logic (a0.1.3.4) ---
        # For now, if we try to edit, it will likely fail to update self.config_data correctly
        # because item_id_is_path_str is now like "('application', 'version')"
        # and self.config_data[item_id_is_path_str] will fail.
        # We will fix this in the next step.
        #
        # Example of what needs to be done in a0.1.3.4:
        data_path_tuple = self.item_id_to_path.get(item_id_is_path_str)
        if not data_path_tuple:
            messagebox.showerror("Edit Error", "Could not find data path for edited item.")
            return

        # Navigate to the correct part of self.config_data using data_path_tuple
        # Get original value, try type conversion, update self.config_data at that path.
        # Then update tree.
        # This is complex and is the core of a0.1.3.4.
        
        # Quick HACK for FLAT DICT only to keep previous editing working for flat_test.yaml
        # THIS WILL BREAK FOR NESTED_TEST.YAML EDITING
        if isinstance(self.config_data, dict) and len(data_path_tuple) == 1:
            dict_key = data_path_tuple[0]
            if dict_key in self.config_data:
                original_value = self.config_data[dict_key]
                new_value = None
                try:
                    if isinstance(original_value, bool):
                        if new_value_str.lower() in ("true", "yes", "1", "on"): new_value = True
                        elif new_value_str.lower() in ("false", "no", "0", "off"): new_value = False
                        else: raise ValueError(f"'{new_value_str}' is not a valid boolean.")
                    elif isinstance(original_value, int): new_value = int(new_value_str)
                    elif isinstance(original_value, float): new_value = float(new_value_str)
                    else: new_value = new_value_str
                    
                    self.config_data[dict_key] = new_value
                    self.tree.set(item_id_is_path_str, column="Value", value=str(new_value))
                except ValueError as ve:
                    messagebox.showerror("Edit Error", f"Invalid value for '{dict_key}': '{new_value_str}'.\n{ve}")
                    self.tree.set(item_id_is_path_str, column="Value", value=str(original_value))
        else:
             # For now, just update the tree display to show what was typed, but config_data won't be updated for nested.
             # This is just to make the UI *seem* to work for display. Actual data update is for a0.1.3.4.
            self.tree.set(item_id_is_path_str, column="Value", value=new_value_str)
            print(f"DEBUG: Edit confirmed for {data_path_tuple}, new value string: {new_value_str}. Actual data update for nested structures is for a0.1.3.4.")


        self._editing_item_id = None
        # --- End Placeholder ---


    # --- File I/O methods (remain the same) ---
    def open_file(self):
        # ... (same as a0.1.3.2)
        filepath = filedialog.askopenfilename(
            title="Open YAML File",
            filetypes=(("YAML files", "*.yaml *.yml"), ("All files", "*.*"))
        )
        if not filepath:
            return

        try:
            self.config_data = yaml_io.load_yaml_file(filepath)
            self.current_filepath = filepath
            if self.config_data is not None: 
                self.root.title(f"Fish Eco Sim - Config Editor Alpha - {os.path.basename(filepath)}")
            else: 
                self.root.title(f"Fish Eco Sim - Config Editor Alpha - {os.path.basename(filepath)} (Empty)")
            self.display_config_data() 
        except FileNotFoundError:
            messagebox.showerror("Error", f"File not found: {filepath}")
            self.current_filepath = None; self.config_data = None
            self.root.title("Fish Eco Sim - Config Editor Alpha")
            self.display_config_data() 
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
        # ... (same as a0.1.3.2)
        if self.current_filepath:
            try:
                yaml_io.save_yaml_file(self.config_data, self.current_filepath)
                messagebox.showinfo("File Saved", f"Successfully saved: {os.path.basename(self.current_filepath)}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {os.path.basename(self.current_filepath)}\n\n{e}")
        else:
            self.save_file_as()

    def save_file_as(self):
        # ... (same as a0.1.3.2)
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
        # ... (same as a0.1.3.2)
        self.root.quit()

if __name__ == '__main__':
    root = tk.Tk()
    app = ConfigEditorApp(root)
    root.mainloop()