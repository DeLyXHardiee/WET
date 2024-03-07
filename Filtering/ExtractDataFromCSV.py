import pandas as pd

def extract_data(excel_file_path):
    # Read the Excel file into a pandas DataFrame
    df = pd.read_csv(excel_file_path, header=None, skiprows=1)
    # Assume all the data is stored in Column A
    timestamps = df[0]
    print(timestamps)
    x_values = df[1]
    print(x_values)
    y_values = df[2]
    print(y_values)
    labels = df[7]
    print(labels)

    # Create a new DataFrame with the extracted values
    extracted_data = pd.DataFrame({
        'n': timestamps,
        'x': x_values,
        'y': y_values,
        'lab': labels
    })
    return extracted_data

#print(extract_data('S_9016_S1_RAN.csv'))
