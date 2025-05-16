# src/modules/config_editor/app.py

import tkinter as tk
from tkinter import filedialog, messagebox, Menu, ttk
import os
from . import yaml_io 

class ConfigEditorApp:
    def __init__(self, root_window):
        self.root = root_window
        self.root.title("Fish Eco Sim - Config Editor Alpha (a0.1.3.4)") # Updated version
        self.root.geometry("800x600")

        self.current_filepath = None
        self.config_data = None
        self._editing_item_id = None
        self.item_id_to_path = {} 

        self.create_menu()
        self.create_widgets()

    # --- Helper functions for nested data access ---
    def _get_value_from_path(self, data_path_tuple):
        """Gets a value from self.config_data using a path tuple."""
        current_level = self.config_data
        try:
            for key_or_index in data_path_tuple:
                current_level = current_level[key_or_index]
            return current_level
        except (KeyError, IndexError, TypeError):
            # TypeError can happen if trying to index a non-collection (e.g. scalar)
            # This indicates an issue with the path or data structure
            messagebox.showerror("Internal Error", f"Could not retrieve data at path: {data_path_tuple}")
            return None # Or raise an exception

    def _set_value_at_path(self, data_path_tuple, new_value):
        """Sets a value in self.config_data using a path tuple."""
        current_level = self.config_data
        try:
            # Navigate to the parent of the target
            for key_or_index in data_path_tuple[:-1]: # All but the last element of the path
                current_level = current_level[key_or_index]
            
            # Set the value on the final key/index
            last_key_or_index = data_path_tuple[-1]
            current_level[last_key_or_index] = new_value
            return True
        except (KeyError, IndexError, TypeError):
            messagebox.showerror("Internal Error", f"Could not set data at path: {data_path_tuple}")
            return False


    # --- UI Creation methods (mostly unchanged from a0.1.3.3) ---
    def create_menu(self):
        # ... (same)
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
        # ... (same)
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

    # --- Display methods (unchanged from a0.1.3.3) ---
    def display_config_data(self):
        # ... (same)
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.item_id_to_path.clear()
        if self.config_data is None: return
        self._populate_tree(parent_tree_id="", data_node=self.config_data, current_data_path=())

    def _generate_unique_iid(self, base_path_tuple):
        # ... (same)
        return str(base_path_tuple)

    def _populate_tree(self, parent_tree_id, data_node, current_data_path):
        # ... (same as a0.1.3.3)
        if isinstance(data_node, dict):
            for key, value_node in data_node.items():
                item_display_text = str(key)
                new_data_path = current_data_path + (key,)
                tree_item_id = self._generate_unique_iid(new_data_path)
                self.item_id_to_path[tree_item_id] = new_data_path 

                if isinstance(value_node, (dict, list)): 
                    inserted_id = self.tree.insert(parent_tree_id, tk.END, text=item_display_text, iid=tree_item_id, open=False)
                    self._populate_tree(inserted_id, value_node, new_data_path)
                else: 
                    self.tree.insert(parent_tree_id, tk.END, text=item_display_text, values=(str(value_node),), iid=tree_item_id)
        elif isinstance(data_node, list):
            for index, value_node in enumerate(data_node):
                item_display_text = f"[{index}]" 
                new_data_path = current_data_path + (index,)
                tree_item_id = self._generate_unique_iid(new_data_path)
                self.item_id_to_path[tree_item_id] = new_data_path

                if isinstance(value_node, (dict, list)):
                    inserted_id = self.tree.insert(parent_tree_id, tk.END, text=item_display_text, iid=tree_item_id, open=False)
                    self._populate_tree(inserted_id, value_node, new_data_path)
                else: 
                    self.tree.insert(parent_tree_id, tk.END, text=item_display_text, values=(str(value_node),), iid=tree_item_id)

    # --- Editing methods (on_edit_confirm is REVISED) ---
    def on_tree_return_key(self, event):
        # ... (same as a0.1.3.3)
        selected_item_id = self.tree.focus() 
        if not selected_item_id: return
        if self.tree.item(selected_item_id, "values"): 
            try:
                bbox = self.tree.bbox(selected_item_id, column="#1")
                if bbox:
                    self._setup_cell_editor(selected_item_id, column_id_to_edit="#1")
            except tk.TclError: pass

    def on_tree_double_click(self, event):
        # ... (same as a0.1.3.3)
        region = self.tree.identify_region(event.x, event.y)
        column_id_clicked = self.tree.identify_column(event.x)
        item_id = self.tree.identify_row(event.y)
        if not item_id: return
        if region == "cell" and column_id_clicked == "#1" and self.tree.item(item_id, "values"):
            self._setup_cell_editor(item_id, column_id_clicked)

    def _setup_cell_editor(self, item_id, column_id_to_edit):
        # ... (same as a0.1.3.3)
        if hasattr(self, '_active_editor') and self._active_editor and self._active_editor.winfo_exists():
            self._active_editor.destroy()
        self._editing_item_id = item_id
        x, y, width, height = self.tree.bbox(item_id, column=column_id_to_edit)
        current_values_tuple = self.tree.item(item_id, "values")
        if not current_values_tuple: return
        current_value_str = str(current_values_tuple[0])
        entry_var = tk.StringVar(value=current_value_str)
        self._active_editor = ttk.Entry(self.tree, textvariable=entry_var)
        self._active_editor.place(x=x, y=y, width=width, height=height, anchor=tk.NW)
        self._active_editor.focus_set()
        self._active_editor.selection_range(0, tk.END)
        self._active_editor.bind("<Return>", lambda e, ed=self._active_editor, iid=item_id: self.on_edit_confirm(e, ed, iid))
        self._active_editor.bind("<KP_Enter>", lambda e, ed=self._active_editor, iid=item_id: self.on_edit_confirm(e, ed, iid))
        self._active_editor.bind("<FocusOut>", lambda e, ed=self._active_editor, iid=item_id: self.on_edit_confirm(e, ed, iid))
        self._active_editor.bind("<Escape>", lambda e, ed=self._active_editor: self.on_edit_cancel(ed))
    
    def on_edit_cancel(self, editor_widget):
        # ... (same as a0.1.3.3)
        editor_widget.destroy()
        self._editing_item_id = None
        if hasattr(self, '_active_editor'):
            del self._active_editor

    def on_edit_confirm(self, event, entry_editor, item_id_is_path_str): # item_id_is_path_str is the Treeview iid
        if not entry_editor.winfo_exists(): return
        new_value_str = entry_editor.get()
        entry_editor.destroy()
        if hasattr(self, '_active_editor'): del self._active_editor

        data_path_tuple = self.item_id_to_path.get(item_id_is_path_str)
        if data_path_tuple is None:
            messagebox.showerror("Internal Error", "Could not find data path for edited tree item.")
            # Attempt to re-display original value if possible, though this state is problematic
            # For now, do nothing to the tree, as we don't know original value without path
            return

        original_value = self._get_value_from_path(data_path_tuple)
        if original_value is None and data_path_tuple: # _get_value_from_path might show its own error
            # If original_value is legitimately None (e.g. null in YAML), this is fine.
            # If _get_value_from_path failed and returned None, an error was already shown.
            pass


        # Attempt type conversion based on original value's type
        try:
            if isinstance(original_value, bool) or original_value is None and new_value_str.lower() in ("true", "false", "yes", "no", "on", "off", "1", "0"): # try to infer bool if original was None
                if new_value_str.lower() in ("true", "yes", "1", "on"): new_value = True
                elif new_value_str.lower() in ("false", "no", "0", "off"): new_value = False
                else: raise ValueError(f"'{new_value_str}' is not a valid boolean representation.")
            elif isinstance(original_value, int) or original_value is None and new_value_str.lstrip('-').isdigit(): # try to infer int
                 new_value = int(new_value_str)
            elif isinstance(original_value, float) or original_value is None and ('.' in new_value_str and new_value_str.replace('.', '', 1).lstrip('-').isdigit()): # try to infer float
                new_value = float(new_value_str)
            elif original_value is None and new_value_str.lower() in ('null', 'none', '~', ''): # If original was None, allow setting back to None
                new_value = None
            else: # Assume string, or if original_value was None and new_value_str doesn't match above types, treat as string
                new_value = new_value_str
            
            # Update the in-memory self.config_data
            if self._set_value_at_path(data_path_tuple, new_value):
                # Update Treeview display
                self.tree.set(item_id_is_path_str, column="Value", value=str(new_value))
            else:
                # _set_value_at_path showed an error, revert Treeview if possible
                # (though this state implies a deeper issue if path was valid for get but not set)
                self.tree.set(item_id_is_path_str, column="Value", value=str(original_value if original_value is not None else ''))


        except ValueError as ve:
            display_key = data_path_tuple[-1] if data_path_tuple else "value"
            messagebox.showerror("Edit Error", f"Invalid value for '{display_key}': '{new_value_str}'.\n{ve}")
            # Revert Treeview display to original value
            self.tree.set(item_id_is_path_str, column="Value", value=str(original_value if original_value is not None else ''))
        
        self._editing_item_id = None


    # --- File I/O methods (unchanged from a0.1.3.3) ---
    def open_file(self): # ... same
        filepath = filedialog.askopenfilename(
            title="Open YAML File",
            filetypes=(("YAML files", "*.yaml *.yml"), ("All files", "*.*"))
        )
        if not filepath: return
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

    def save_file(self): # ... same
        if self.current_filepath:
            try:
                yaml_io.save_yaml_file(self.config_data, self.current_filepath)
                messagebox.showinfo("File Saved", f"Successfully saved: {os.path.basename(self.current_filepath)}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {os.path.basename(self.current_filepath)}\n\n{e}")
        else:
            self.save_file_as()

    def save_file_as(self): # ... same
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

    def exit_app(self): # ... same
        self.root.quit()

if __name__ == '__main__':
    root = tk.Tk()
    app = ConfigEditorApp(root)
    root.mainloop()