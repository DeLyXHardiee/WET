import numpy as np
import re
import matplotlib.pyplot as plt
import random

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
    for i in range (0,len(slices)):
        if len(slices[i])<1:
            continue
        watermark = generate_watermark(len(slices[i]))
        fft = get_FFT(slices[i])
        embedded_data = embed_watermark(fft,watermark,strength)
        ifft = get_IFFT(embedded_data)
        reverted_ifft = revert_from_complex_numbers(ifft,sliceSize,data,i)
        for i in reverted_ifft:
            watermarked_data.append(i)
    return watermarked_data