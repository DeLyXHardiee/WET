import numpy as np
import re
import matplotlib.pyplot as plt
import random
import Filtering.CSVUtility as csvu

# Extract time, x, y from the loaded data
def read_tuples_from_txt(filename):
    result = []
    with open(filename, 'r') as file:
        for line in file:
            current_tuple = eval(line.strip())
            result.append(current_tuple)
    return result

def get_complex_transformation(data):
    complex_numbers = []
    for tuple in data:
        complex_numbers.append(tuple[1] + 1j*tuple[2])
    return complex_numbers

def get_slices(complex_transformation,slicesize):
    slices = []
    for i in range(0,len(complex_transformation),slicesize):
        slices.append(complex_transformation[i:i+slicesize])
    return slices

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
    amplitudes = np.abs(fft)
    modified_amplitudes = np.add((watermark*strength),amplitudes)
    return modified_amplitudes * np.exp(1j * np.angle(fft))

def extract_watermark(original_fft, watermark_fft, strenght):
    original_amplitudes = np.abs(original_fft)
    watermark_amplitudes = np.abs(watermark_fft)
    return (watermark_amplitudes - original_amplitudes)/strenght

def get_IFFT(fft):
    return np.fft.ifft(fft)

def write_tuples_to_txt(tuples,filename):
    with open(filename,'w') as file:
        for data in tuples:
            file.write(str(data[0:3]))
            file.write('\n')

def revert_from_complex_numbers(slice,slicesize,data,i):
    points = []
    for j in range(0,len(slice)):
            #print(i*slicesize+j)
            points.append((data[i*slicesize+j][0],slice[j].real,slice[j].imag, int(data[i*slicesize+j][3])))
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


def run_watermark(data):
    sliceSize = 16
    strength = 0.0003
    complex_transformation = get_complex_transformation(data)
    slices = get_slices(complex_transformation,sliceSize)
    watermarked_data = []
    watermark = []
    for i in range (0,len(slices)):
        if len(slices[i])<1:
            continue
        watermark_slice = generate_watermark(len(slices[i]))
        watermark.append(watermark_slice)
        fft = get_FFT(slices[i])
        embedded_data = embed_watermark(fft,watermark,strength)
        ifft = get_IFFT(embedded_data)
        reverted_ifft = revert_from_complex_numbers(ifft,sliceSize,data,i)
        for i in reverted_ifft:
            watermarked_data.append(i)
    return watermarked_data, watermark

def unrun_watermark(watermarked_data, original_data, sliceSize, strength):
    if len(watermarked_data) != len(original_data):
        raise ValueError("Length of true data and predicted data must be the same")
    complex_transformation_original = get_complex_transformation(original_data)
    complex_transformation_watermark = get_complex_transformation(watermarked_data)
    original_slices = get_slices(complex_transformation_original, sliceSize)
    watermark_slices = get_slices(complex_transformation_watermark, sliceSize)
    extracted_watermark = []
    for i in range (0,len(original_slices)):
        if len(original_slices[i])<1:
            continue
        original_fft = get_FFT(original_slices[i])
        watermark_fft = get_FFT(watermark_slices[i])
        watermark = extract_watermark(original_fft, watermark_fft, strength)
        extracted_watermark.append(watermark)
    return extracted_watermark

def watermark_embedding_and_extraction_test(data, slicesize, strength):
    watermarked_data, watermark = run_watermark(data)
    extracted_watermark = unrun_watermark(watermarked_data, data, slicesize, strength)
    for i in range(len(watermarked_data)-1):
        for j in range(slicesize-1):
            if (watermark[i][j] != extracted_watermark[i][j]):
                raise ValueError("Original watermark and extracted watermark is not the same")
    print("WEEEEEEEEE")

data = csvu.extract_data("../Datasets/Reading/S_1004_S2_TEX.csv")
watermark_embedding_and_extraction_test(data, 16, 0.0003)

