import numpy as np
import matplotlib.pyplot as plt
import random
import Filtering.CSVUtility as csvu
import Analyze as an
import Adversary as ad
import Filtering.IVT as ivt
import Filtering.EyeLink as el


def get_complex_transformation(data):
    complex_numbers = []
    for tuple in data:
        complex_numbers.append(tuple[1] + 1j*tuple[2])
    return complex_numbers

def generate_watermark(length, strength_range):
    watermark = []
    number_of_zeroes = 0
    max_zero = int(length * 0.375)
    while len(watermark) < length:
        randomnr = random.uniform(-strength_range, strength_range)
        if randomnr != 0:
            watermark.append(randomnr)
        else:
            if number_of_zeroes < max_zero:
                watermark.append(randomnr)
                number_of_zeroes = number_of_zeroes + 1
    watermark = np.array(watermark)  # Convert to NumPy array
    return watermark

def write_array_to_file(array, filename):
    with open(filename, 'w') as file:
        for i, value in enumerate(array):
            file.write(str(value))
            if (i + 1) % 16 == 0:  # Check if it's the 16th element
                file.write('\n')    # Insert newline after every 16th element
            else:
                file.write(' ')     # Otherwise, insert space



def get_FFT(complex_transformation):
    fft_result = np.fft.fft(complex_transformation)
    return fft_result

def embed_watermark(fft,watermark):
    amplitudes = np.real(fft)
    modified_amplitudes = np.add(watermark, amplitudes)
    return np.add(modified_amplitudes, np.multiply(1j, np.imag(fft)))

def extract_watermark(original_fft, watermark_fft):
    original_amplitudes = np.real(original_fft)
    watermark_amplitudes = np.real(watermark_fft)
    return np.subtract(watermark_amplitudes, original_amplitudes)

def get_IFFT(fft):
    return np.fft.ifft(fft)

def revert_from_complex_numbers(ifft,data):
    points = []
    for i in range(0,len(data)):
        points.append((data[i][0], ifft[i].real, ifft[i].imag, data[i][3]))
    return points

def plot_data(watermarked_data, data):
    x_w = []
    y_w = []
    x = []
    y = []
    # Unpack data
    print("plotting")
    for entry in watermarked_data:
        t_entry,x_entry,y_entry = entry
        x_w.append(x_entry)
        y_w.append(y_entry)
    plt.scatter(x_w, y_w, color='blue', label='Watermarked Data', s=1)

    # Unpack and plot original data
    for i in range(0,len(data[0])):
        x_entry = data[1][i]
        y_entry = data[2][i]
        x.append(x_entry)
        y.append(y_entry)
    plt.scatter(x, y, color='red', label='Original Data', s=1)

    # Customize the plot
    plt.title('Watermarked Data vs Original Data')
    plt.xlabel('X-values')
    plt.ylabel('Y-values')
    plt.legend()

    # Show the plot
    plt.show()

def filter_data(data):
    filtered_data = []
    for i in range(len(data)):
        if np.isnan(data[i][1]) or np.isnan(data[i][2]):
            continue
        filtered_data.append(data[i])
    return filtered_data

def run_watermark(data, strength_range):
    complex_transformation = get_complex_transformation(data)
    watermark = generate_watermark(len(complex_transformation), strength_range)
    fft = get_FFT(complex_transformation)
    embedded_data = embed_watermark(fft,watermark)
    ifft = get_IFFT(embedded_data)
    reverted_ifft = revert_from_complex_numbers(ifft, data)
    return reverted_ifft, watermark

def unrun_watermark(watermarked_data, original_data, strength):
    if len(watermarked_data) != len(original_data):
        print(len(watermarked_data))
        print(len(original_data))
        raise ValueError("Length of true data and predicted data must be the same")
    complex_transformation_original = get_complex_transformation(original_data)
    complex_transformation_watermark = get_complex_transformation(watermarked_data)
    original_fft = get_FFT(complex_transformation_original)
    watermark_fft = get_FFT(complex_transformation_watermark)
    extracted_watermark = extract_watermark(original_fft, watermark_fft)
    return extracted_watermark

def watermark_embedding_and_extraction_test(data, strength):
    print(len(data))
    filtered_data = filter_data(data)
    watermarked_data, watermark = run_watermark(filtered_data, strength)
    extracted_watermark = unrun_watermark(watermarked_data, filtered_data, strength)
    count = 0
    for i in range(len(watermark)):
        if watermark[i] == round(extracted_watermark[i]):
            count = count + 1
    print(len(watermark))
    print(count)

