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

def save_yaml_file(data, filepath: str):
    """
    Saves Python data (dictionary or list) to a specified YAML file.
    The output will be in block style for better readability.
    This function will overwrite the file if it already exists.

    Args:
        data: The Python dictionary or list to save.
        filepath (str): The path to the YAML file where data will be saved.

    Raises:
        IOError: If the file cannot be written (e.g., permission issues, invalid path parts).
        yaml.YAMLError: If an error occurs during YAML serialization (less common for standard Python types).
        Exception: For other unexpected errors.
    """
    try:
        # Create parent directories if they don't exist.
        # This is a good practice for a save function.
        # For example, if filepath is "configs/new_set/sim.yaml" and "configs/new_set/" doesn't exist.
        dir_name = os.path.dirname(filepath)
        if dir_name: # Ensure dirname is not empty (e.g. if filepath is just 'file.yaml')
            os.makedirs(dir_name, exist_ok=True)

        with open(filepath, 'w') as file:
            # default_flow_style=False ensures block style (more readable for configs)
            # sort_keys=False preserves the order of keys in dictionaries (Python 3.7+ dicts are ordered)
            # allow_unicode=True is good for handling various text characters
            yaml.dump(data, file, default_flow_style=False, sort_keys=False, allow_unicode=True)
    except IOError as e: # Covers issues like permission denied, disk full, etc.
        # print(f"IOError: Could not write to YAML file at {filepath}. Error: {e}") # Optional logging
        raise
    except yaml.YAMLError as e: # Errors during the dumping process itself
        # print(f"YAMLError: Could not dump data to YAML for {filepath}. Error: {e}") # Optional logging
        raise
    except Exception as e:
        # print(f"An unexpected error occurred while saving {filepath}: {e}") # Optional logging
        raise