import os
import pandas as pd
import numpy as np

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

def filter_data(data):
    filtered_data = []
    for i in range(len(data)):
        if np.isnan(data[i][1]) or np.isnan(data[i][2]):
            continue
        filtered_data.append(data[i])
    return filtered_data

def write_data(csv_filename, data):
    print(str(csv_filename) + str(len(data)))
    df = pd.DataFrame(data, columns=['n', 'x', 'y', 'lab'])
    df.to_csv(csv_filename, index=False)

def append_result(csv_filename, parameters, result):
    print(csv_filename)
    try:
        df = pd.read_csv(csv_filename)
    except FileNotFoundError:
        print("File not found")
        return

    # Append new data
    new_row = pd.Series(parameters + [result], index=df.columns)
    df = df.append(new_row, ignore_index=True)

    # Write back to the file
    df.to_csv(csv_filename, index=False)