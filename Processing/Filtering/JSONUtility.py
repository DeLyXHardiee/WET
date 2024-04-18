import json
import os

def file_exists(directory, filename):
    """ Check if a file exists in a directory using os.path. """
    # Build the full file path
    file_path = os.path.join(directory, filename)
    # Check if the file exists
    return os.path.exists(file_path)

def extract_context(json_file_path):
    """
    Reads a JSON file and extracts velocities into a dictionary.

    Args:
    json_file_path (str): The path to the JSON file.

    Returns:
    dict: A dictionary where 'file' is the key and 'v' is the value.
    """
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    return data

def create_empty_json(folder_path, file_name):
    """
    Creates an empty JSON file in a specified folder.

    Args:
    folder_path (str): The path to the folder where the JSON file should be created.
    file_name (str): The name of the JSON file to create.
    """
    # Ensure the folder exists, if not, create it
    os.makedirs(folder_path, exist_ok=True)

    # Full path for the new JSON file
    file_path = os.path.join(folder_path, file_name)

    # Create an empty JSON file with an empty dictionary or specific structure
    with open(file_path, 'w') as json_file:
        json.dump({}, json_file, indent=4)

    print(f"Empty JSON file created at {file_path}")

def write_context_to_json(file_v_map, file_path):
    """
    Writes a dictionary to a JSON file.

    Args:
    file_v_map (dict): Dictionary where keys are 'file' and values are 'v'.
    file_path (str): Path to the JSON file to be written.
    """
    with open(file_path, 'w') as json_file:
        json.dump(file_v_map, json_file, indent=4)

    print(f"Data written to {file_path} successfully.")

def create_strength_json(folder_path, file_name, strength):
    """
    Creates an empty JSON file with a 'strength' key set to a default value (e.g., null) in the specified folder.

    Args:
    folder_path (str): The path to the folder where the JSON file should be created.
    file_name (str): The name of the JSON file to create.
    """
    # Ensure the folder exists, if not, create it
    os.makedirs(folder_path, exist_ok=True)

    # Full path for the new JSON file
    file_path = os.path.join(folder_path, file_name)

    # Data structure with 'strength' initialized to None or a default value
    data = {"strength": None}

    # Writing the data structure to a JSON file
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print(f"JSON file created at {file_path} with 'strength' initialized to {strength}.")


def update_strength_in_json(file_path, new_strength):
    """
    Updates the 'strength' value in a specified JSON file.

    Args:
    file_path (str): The path to the JSON file.
    new_strength (int or float): The new value to update the 'strength' to.
    """
    # Read the existing data from the JSON file
    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        print(f"No file found at {file_path}. Please check the file path.")
        return
    except json.JSONDecodeError:
        print(f"File at {file_path} is not a valid JSON file.")
        return

    # Update the 'strength' value
    data['strength'] = new_strength

    # Write the updated data back to the JSON file
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print(f"'Strength' updated to {new_strength} in {file_path}")


def update_wm_context(directory, file, context):
    return None