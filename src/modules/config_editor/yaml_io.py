# src/modules/config_editor/yaml_io.py

import yaml
import os # For checking file existence if we want to be more explicit before open, though open() handles it.

def load_yaml_file(filepath: str):
    """
    Loads data from a specified YAML file into a Python dictionary/list structure.

    Args:
        filepath (str): The path to the YAML file.

    Returns:
        dict or list or None: The loaded data if successful, 
                              None if the file is empty or cannot be parsed,
                              or if the file is not found.
                              (Consider raising specific exceptions for better error handling by callers)
    
    Raises:
        FileNotFoundError: If the specified filepath does not exist.
        yaml.YAMLError: If the file content is not valid YAML.
                        (Or a custom wrapper exception if preferred)
    """
    try:
        with open(filepath, 'r') as file:
            # Using yaml.safe_load() is crucial for security, 
            # as it prevents arbitrary code execution from untrusted YAML files.
            data = yaml.safe_load(file)
            return data
    except FileNotFoundError:
        # Re-raise the exception to be handled by the caller,
        # as per our test case test_load_non_existent_file.
        # The caller (e.g., UI) can then decide how to inform the user.
        # print(f"Error: File not found at path: {filepath}") # Optional logging
        raise
    except yaml.YAMLError as e:
        # Re-raise the YAML parsing error.
        # The caller can catch this specific error type.
        # print(f"Error: Could not parse YAML file at {filepath}. Error: {e}") # Optional logging
        raise
    except Exception as e:
        # Catch any other unexpected errors during file operations or loading
        # print(f"An unexpected error occurred while loading {filepath}: {e}") # Optional logging
        # It might be better to re-raise a generic custom error or the original error here
        # depending on how much detail the caller needs. For now, re-raise.
        raise

# Placeholder for the save function, which will be implemented in a0.1.1.2
def save_yaml_file(data, filepath):
    """
    Saves Python data to a specified YAML file.
    (Implementation to be added in a0.1.1.2)
    """
    pass