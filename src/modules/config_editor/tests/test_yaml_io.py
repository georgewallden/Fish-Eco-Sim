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

if __name__ == '__main__':
    unittest.main()