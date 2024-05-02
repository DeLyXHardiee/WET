from csv import writer
import os
import pandas as pd
import numpy as np
import csv

def file_exists(directory, filename):
    """ Check if a file exists in a directory using os.path. """
    # Build the full file path
    file_path = os.path.join(directory, filename)
    # Check if the file exists
    return os.path.exists(file_path)

def list_csv_files_in_directory(directory):
    """ List all CSV files in a given directory using the os module. """
    # Get all entries in the directory specified
    all_entries = os.listdir(directory)
    # Filter out directories and only keep files with a .csv extension
    csv_files = [entry for entry in all_entries if os.path.isfile(os.path.join(directory, entry)) and entry.endswith('.csv')]
    return csv_files

def extract_velocities(csv_file_path):
    # Read the CSV file using pandas
    df = pd.read_csv(csv_file_path)

    # Assuming the columns are named 'file' and 'v'
    file_column = df['file']
    v_column = df['v']

    # Create a dictionary where 'file' is the key and 'v' is the value
    file_to_v_map = dict(zip(file_column, v_column))

    return file_to_v_map

def create_empty_velocity_csv(folder_path, file_name):
    """
    Creates an empty CSV file with specified headers in a given folder.

    Args:
    folder_path (str): The path to the folder where the CSV should be created.
    file_name (str): The name of the CSV file to create.
    """
    # Ensure the folder exists, if not, create it
    os.makedirs(folder_path, exist_ok=True)

    # Full path for the new CSV file
    file_path = os.path.join(folder_path, file_name)

    # Open the file in write mode and create it with headers
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Example headers - modify as needed
        headers = ["file", "v"]
        writer.writerow(headers)

    print(f"Empty CSV file created at {file_path}")

def write_velocities_to_csv(file_v_map, file_path):
    """
    Writes a dictionary to a CSV file with columns 'file' and 'v'.

    Args:
    file_v_map (dict): Dictionary where keys are 'file' and values are 'v'.
    file_path (str): Path to the CSV file to be written.
    """
    # Create a DataFrame from the dictionary
    df = pd.DataFrame(list(file_v_map.items()), columns=['file', 'v'])

    # Write the DataFrame to a CSV file
    df.to_csv(file_path, index=False)

    print(f"Data written to {file_path} successfully.")

def extract_data(csv_file_path):
    # Read the Excel file into a pandas DataFrame
    df = pd.read_csv(csv_file_path)
    timestamps = df["n"]
    x_values = df["x"]
    y_values = df["y"]
    labels = df["lab"]

    # Create a new DataFrame with the extracted values
    extracted_data = pd.DataFrame({
        'n': timestamps,
        'x': x_values,
        'y': y_values,
        'lab': labels
    })
    return filter_data(extracted_data.apply(lambda row: (row['n'], row['x'], row['y'], row['lab']), axis=1))

def extract_data_with_true_point(csv_file_path):
    # Read the Excel file into a pandas DataFrame
    df = pd.read_csv(csv_file_path)
    timestamps = df["n"]
    x_values = df["x"]
    y_values = df["y"]
    x_true = df["xT"]
    y_true = df["yT"]
    labels = df["lab"]

    # Create a new DataFrame with the extracted values
    extracted_data = pd.DataFrame({
        'n': timestamps,
        'x': x_values,
        'y': y_values,
        'lab': labels,
        'xT' : x_true,
        'yT': y_true
    })
    return filter_data(extracted_data.apply(lambda row: (row['n'], row['x'], row['y'],row['xT'],row['yT'], row['lab']), axis=1))

def extract_results2(csv_file_path):
    df = pd.read_csv(csv_file_path)
    strengths = df['S']
    saccadeAccuracies = df['SA']
    visualDegrees = df['VD']
    rms = df['RMS']
    extracted_data = pd.DataFrame({
            'S': strengths,
            'SA': saccadeAccuracies,
            'VD': visualDegrees,
            'RMS': rms,
            })
    return extracted_data.apply(lambda row: (row['S'], row['SA'], row['VD'], row['RMS']), axis=1)

def extract_results(csv_file_path):
    print(csv_file_path)
    # Read the Excel file into a pandas DataFrame
    df = pd.read_csv(csv_file_path)
    strengths = df["S"]
    standard_deviations = df["SD"]
    results = df["NCC"]

    # Create a new DataFrame with the extracted values
    if "IDT" in csv_file_path:
        duration_thresholds = df["DUT"]
        dispersion_thresholds = df["DIT"]
        extracted_data = pd.DataFrame({
            'DUT': duration_thresholds,
            'DIT': dispersion_thresholds,
            'S': strengths,
            'SD': standard_deviations,
            'NCC': results
        })
        return filter_data(extracted_data.apply(lambda row: (row['DUT'], row['DIT'], row['S'], row['SD'], row['NCC']), axis=1))

    elif "IVT" in csv_file_path:
        velocity_thresholds = df["VT"]
        extracted_data = pd.DataFrame({
            'VT': velocity_thresholds,
            'S': strengths,
            'SD': standard_deviations,
            'NCC': results
        })
        return filter_data(extracted_data.apply(lambda row: (row['VT'], row['S'], row['SD'], row['NCC']), axis=1))

def filter_data(data):
    filtered_data = []
    for i in range(len(data)):
        if np.isnan(data[i][1]) or np.isnan(data[i][2]):
            continue
        filtered_data.append(data[i])
    return filtered_data

def write_data(csv_filename, data):
    print(str(csv_filename))
    df = pd.DataFrame(data, columns=['n', 'x', 'y', 'lab'])
    df.to_csv(csv_filename, index=False)

def append_result(csv_filename, values):
    print(csv_filename)
    with open(csv_filename, 'a',newline='') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(values)
        f_object.close()

def get_reader(file):
    return csv.reader(file)