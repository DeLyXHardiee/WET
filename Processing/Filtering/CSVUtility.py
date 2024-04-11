from csv import writer
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

def extract_data(csv_file_path):
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
    print(str(csv_filename) + str(len(data)))
    df = pd.DataFrame(data, columns=['n', 'x', 'y', 'lab'])
    df.to_csv(csv_filename, index=False)

def append_result(csv_filename, values):
    print(csv_filename)
    with open(csv_filename, 'a',newline='') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(values)
        f_object.close()