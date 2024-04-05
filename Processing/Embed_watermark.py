import numpy as np
import matplotlib.pyplot as plt
import random
import Filtering.CSVUtility as csvu
import Analyze as an


def get_complex_transformation(data):
    complex_numbers = []
    for tuple in data:
        complex_numbers.append(tuple[1] + 1j*tuple[2])
    return complex_numbers

def generate_watermark(length):
    maxZeros = int(length*0.375)
    watermark = np.array([])
    while len(watermark) < length:
        randomnr = random.randint(-1,1)
        if ((length - np.count_nonzero(watermark)) == maxZeros) & (randomnr == 0):
            continue
        watermark = np.append(watermark,randomnr)
    return watermark

def get_FFT(complex_transformation):
    fft_result = np.fft.fft(complex_transformation)
    return fft_result

def embed_watermark(fft,watermark,strength):
    amplitudes = np.real(fft)
    modified_amplitudes = np.add(np.multiply(watermark, strength), amplitudes)
    return np.add(modified_amplitudes, np.multiply(1j, np.imag(fft)))

def extract_watermark(original_fft, watermark_fft, strength):
    original_amplitudes = np.real(original_fft)
    watermark_amplitudes = np.real(watermark_fft)
    return np.round(np.divide(np.subtract(watermark_amplitudes, original_amplitudes), strength))

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
    count = 0
    for i in range(len(data)):
        if np.isnan(data[i][1]) or np.isnan(data[i][2]):
            count = count + 1
            continue
        filtered_data.append(data[i])
    print(count)
    return filtered_data

def run_watermark(data, strength):
    complex_transformation = get_complex_transformation(data)
    watermark = generate_watermark(len(complex_transformation))
    fft = get_FFT(complex_transformation)
    embedded_data = embed_watermark(fft,watermark,strength)
    ifft = get_IFFT(embedded_data)
    reverted_ifft = revert_from_complex_numbers(ifft, data)
    return reverted_ifft, watermark

def unrun_watermark(watermarked_data, original_data, strength):
    if len(watermarked_data) != len(original_data):
        raise ValueError("Length of true data and predicted data must be the same")
    complex_transformation_original = get_complex_transformation(original_data)
    complex_transformation_watermark = get_complex_transformation(watermarked_data)
    original_fft = get_FFT(complex_transformation_original)
    watermark_fft = get_FFT(complex_transformation_watermark)
    extracted_watermark = extract_watermark(original_fft, watermark_fft, strength)
    return extracted_watermark

def watermark_embedding_and_extraction_test(data, strength):
    print(len(data))
    filtered_data = filter_data(data)
    watermarked_data, watermark = run_watermark(filtered_data, strength)
    extracted_watermark = unrun_watermark(watermarked_data, filtered_data, strength)
    count = 0
    for i in range(len(watermark)):
        if (np.array_equal(watermark[i],extracted_watermark[i])):
            count = count + 1
    print(len(watermark))
    print(count)
    csvu.write_data("test.csv", watermarked_data)


