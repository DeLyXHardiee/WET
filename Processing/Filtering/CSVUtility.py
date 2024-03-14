import pandas as pd
import csv

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
    return extracted_data.apply(lambda row: (row['n'], row['x'], row['y'], row['lab']), axis=1)

def write_data(csv_filename, data):
    df = pd.DataFrame(data, columns=['n', 'x', 'y', 'lab'])
    df.to_csv(csv_filename, index=False)