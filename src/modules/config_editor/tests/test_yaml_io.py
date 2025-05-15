# src/modules/config_editor/tests/test_yaml_io.py

import unittest
import os
import tempfile
import yaml # For yaml.YAMLError

# Assuming 'src' is in PYTHONPATH or tests are run correctly:
from modules.config_editor import yaml_io

class TestYamlLoading(unittest.TestCase):

    def setUp(self):
        self.temp_files = []

    def tearDown(self):
        for temp_file_path in self.temp_files:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

    def _create_temp_yaml_file(self, content):
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".yaml", prefix="test_")
        temp_file.write(content)
        temp_file.close()
        self.temp_files.append(temp_file.name)
        return temp_file.name

    # Test a0.1.1.1t: Valid YAML loading
    def test_load_valid_yaml_dict(self):
        """Test loading a valid YAML file representing a dictionary."""
        content = """
        name: Test Project
        version: 1.0
        settings:
          debug: true
          port: 8080
        """
        filepath = self._create_temp_yaml_file(content)
        
        data = yaml_io.load_yaml_file(filepath) 
        self.assertIsNotNone(data)
        self.assertEqual(data['name'], "Test Project")
        self.assertEqual(data['version'], 1.0) # PyYAML typically converts "1.0" to float
        self.assertTrue(data['settings']['debug'])
        self.assertEqual(data['settings']['port'], 8080)

    def test_load_valid_yaml_list(self):
        """Test loading a valid YAML file representing a list."""
        content = """
        - item1
        - item2
        - name: item3
          value: 100
        """
        filepath = self._create_temp_yaml_file(content)
        data = yaml_io.load_yaml_file(filepath)
        self.assertIsNotNone(data)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 3)
        self.assertEqual(data[0], "item1")
        self.assertEqual(data[2]['name'], "item3")

    # Test a0.1.1.1t: Empty file handling
    def test_load_empty_yaml_file(self):
        """Test loading an empty YAML file."""
        filepath = self._create_temp_yaml_file("")
        data = yaml_io.load_yaml_file(filepath)
        # PyYAML's safe_load returns None for an empty file.
        self.assertIsNone(data)

    # Test a0.1.1.1t: Basic error conditions - File Not Found
    def test_load_non_existent_file(self):
        """Test loading a non-existent YAML file."""
        # Assuming yaml_io.load_yaml_file will raise FileNotFoundError
        # if it attempts to open a non-existent file before PyYAML parsing.
        with self.assertRaises(FileNotFoundError):
            yaml_io.load_yaml_file("non_existent_dummy_file_for_test.yaml") # Made filename more specific

    # Test a0.1.1.1t: Basic error conditions - Malformed YAML
    def test_load_malformed_yaml_file(self):
        """Test loading a YAML file with incorrect syntax."""
        # Malformed YAML: e.g., inconsistent indentation or invalid characters
        content = "name: Test\n  version: 1.0" # Bad indentation
        filepath = self._create_temp_yaml_file(content)
        
        # Assuming yaml_io.load_yaml_file will let yaml.YAMLError propagate
        with self.assertRaises(yaml.YAMLError):
            yaml_io.load_yaml_file(filepath)

    def test_load_yaml_with_various_scalar_types(self):
        """Test loading YAML with various scalar types (int, float, bool, string)."""
        content = """
        integer_val: 123
        float_val: 45.67
        bool_true_val: true
        bool_false_val: false
        string_val: "hello world"
        null_val: null # or ~
        """
        filepath = self._create_temp_yaml_file(content)
        data = yaml_io.load_yaml_file(filepath)
        self.assertIsNotNone(data)
        self.assertEqual(data['integer_val'], 123)
        self.assertIsInstance(data['integer_val'], int)
        self.assertEqual(data['float_val'], 45.67)
        self.assertIsInstance(data['float_val'], float)
        self.assertTrue(data['bool_true_val'])
        self.assertIsInstance(data['bool_true_val'], bool)
        self.assertFalse(data['bool_false_val'])
        self.assertIsInstance(data['bool_false_val'], bool)
        self.assertEqual(data['string_val'], "hello world")
        self.assertIsInstance(data['string_val'], str)
        self.assertIsNone(data['null_val']) # PyYAML 'null' becomes None

class TestYamlSaving(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for saving files
        self.test_dir = tempfile.TemporaryDirectory()
        self.temp_files_to_remove_on_cleanup = [] # For files not in TemporaryDirectory

    def tearDown(self):
        # Clean up the temporary directory and its contents
        self.test_dir.cleanup()
        for f_path in self.temp_files_to_remove_on_cleanup:
            if os.path.exists(f_path):
                os.remove(f_path)

    # Test a0.1.1.2t: Basic saving of a dictionary
    def test_save_basic_dictionary(self):
        """Test saving a simple Python dictionary to a YAML file."""
        data_to_save = {
            "project": "Fish Eco Sim",
            "version": "a0.1.1.2",
            "active": True,
            "max_agents": 100,
            "depth": 25.5
        }
        filepath = os.path.join(self.test_dir.name, "basic_dict.yaml")

        # --- This is where yaml_io.save_yaml_file would be called ---
        yaml_io.save_yaml_file(data_to_save, filepath)

        # --- Verification: Load the file back and check its content ---
        self.assertTrue(os.path.exists(filepath))
        with open(filepath, 'r') as f:
            loaded_data = yaml.safe_load(f)
        
        self.assertEqual(loaded_data["project"], "Fish Eco Sim")
        self.assertEqual(loaded_data["version"], "a0.1.1.2")
        self.assertTrue(loaded_data["active"])
        self.assertEqual(loaded_data["max_agents"], 100)
        self.assertEqual(loaded_data["depth"], 25.5)

    # Test a0.1.1.2t: Basic saving of a list
    def test_save_basic_list(self):
        """Test saving a simple Python list to a YAML file."""
        data_to_save = ["apple", "banana", {"type": "citrus", "name": "orange"}, 123]
        filepath = os.path.join(self.test_dir.name, "basic_list.yaml")

        yaml_io.save_yaml_file(data_to_save, filepath)
        
        self.assertTrue(os.path.exists(filepath))
        with open(filepath, 'r') as f:
            loaded_data = yaml.safe_load(f)
        
        self.assertIsInstance(loaded_data, list)
        self.assertEqual(len(loaded_data), 4)
        self.assertEqual(loaded_data[0], "apple")
        self.assertEqual(loaded_data[2]["name"], "orange")
        self.assertEqual(loaded_data[3], 123)

    # Test a0.1.1.2t: Saving nested structures
    def test_save_nested_structure(self):
        """Test saving a Python dictionary with nested lists and dictionaries."""
        data_to_save = {
            "simulation": {
                "grid": {"width": 100, "height": 100},
                "agents": [
                    {"id": 1, "type": "fish_a", "energy": 100},
                    {"id": 2, "type": "fish_b", "energy": 150}
                ]
            },
            "logging_level": "INFO"
        }
        filepath = os.path.join(self.test_dir.name, "nested_structure.yaml")
        yaml_io.save_yaml_file(data_to_save, filepath)

        self.assertTrue(os.path.exists(filepath))
        with open(filepath, 'r') as f:
            loaded_data = yaml.safe_load(f)
        
        self.assertEqual(loaded_data["simulation"]["grid"]["width"], 100)
        self.assertEqual(len(loaded_data["simulation"]["agents"]), 2)
        self.assertEqual(loaded_data["simulation"]["agents"][1]["type"], "fish_b")
        self.assertEqual(loaded_data["logging_level"], "INFO")

    # Test a0.1.1.2t: Ensure correct YAML output format (block style, not flow style)
    def test_save_output_format_block_style(self):
        """Test that the YAML output is in block style by default."""
        data_to_save = {"key1": "value1", "key2": {"sub_key": "sub_value"}}
        filepath = os.path.join(self.test_dir.name, "block_style.yaml")

        yaml_io.save_yaml_file(data_to_save, filepath)

        self.assertTrue(os.path.exists(filepath))
        with open(filepath, 'r') as f:
            content = f.read()
            # A simple check: flow style would likely have { } or [ ] on the same line for dicts/lists
            # Block style has indentation.
            self.assertNotIn("{", content) # This might be too strict if strings contain '{'
            self.assertNotIn("}", content)
            # A better check might be to look for newlines after keys
            self.assertIn("key1: value1\n", content.replace('\r\n', '\n'))
            self.assertIn("key2:\n", content.replace('\r\n', '\n'))
            self.assertIn("  sub_key: sub_value\n", content.replace('\r\n', '\n'))


    # Test a0.1.1.2t: Handling of None values (should be saved as null or similar)
    def test_save_with_none_value(self):
        """Test saving data containing None values."""
        data_to_save = {"key_with_none": None, "another_key": "value"}
        filepath = os.path.join(self.test_dir.name, "none_value.yaml")

        yaml_io.save_yaml_file(data_to_save, filepath)

        self.assertTrue(os.path.exists(filepath))
        with open(filepath, 'r') as f:
            loaded_data = yaml.safe_load(f)
        self.assertIsNone(loaded_data["key_with_none"])
        self.assertEqual(loaded_data["another_key"], "value")

        # Additionally, check the raw output for 'null' (or empty if PyYAML does that for None)
        with open(filepath, 'r') as f:
           content = f.read()
           self.assertIn("key_with_none: null\n", content.replace('\r\n', '\n')) # or check for empty if that's the style

    # Test a0.1.1.2t: Overwriting an existing file
    def test_save_overwrites_existing_file(self):
        """Test that saving to an existing filepath overwrites it."""
        filepath = os.path.join(self.test_dir.name, "overwrite_me.yaml")
        
        initial_data = {"message": "original content"}
        # Create the file initially
        with open(filepath, 'w') as f:
           yaml.dump(initial_data, f)

        new_data = {"message": "new content", "extra": True}
        yaml_io.save_yaml_file(new_data, filepath)
        
        self.assertTrue(os.path.exists(filepath))
        with open(filepath, 'r') as f:
            loaded_data = yaml.safe_load(f)
        
        self.assertEqual(loaded_data["message"], "new content")
        self.assertTrue(loaded_data["extra"])
        self.assertNotIn("original content", str(loaded_data)) # Ensure old content is gone

if __name__ == '__main__':
    unittest.main()