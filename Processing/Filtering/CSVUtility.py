import pandas as pd

def extract_original_data(csv_file_path):
    # Read the Excel file into a pandas DataFrame
    df = pd.read_csv(csv_file_path, header=None, skiprows=1)
    # Assume all the data is stored in Column A
    timestamps = df[0]
    #print(timestamps)
    x_values = df[1]
    #print(x_values)
    y_values = df[2]
    #print(y_values)
    labels = df[5]
    #print(labels)

    # Create a new DataFrame with the extracted values
    extracted_data = pd.DataFrame({
        'n': timestamps,
        'x': x_values,
        'y': y_values,
        'lab': labels
    })
    return extracted_data.apply(lambda row: (row['n'], row['x'], row['y'], row['lab']), axis=1)

def extract_data(csv_file_path):
    # Read the Excel file into a pandas DataFrame
    df = pd.read_csv(csv_file_path, header=None, skiprows=1)
    # Assume all the data is stored in Column A
    timestamps = df[0]
    #print(timestamps)
    x_values = df[1]
    #print(x_values)
    y_values = df[2]
    #print(y_values)
    labels = df[3]
    #print(labels)

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