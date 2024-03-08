import numpy as np
import re
import matplotlib.pyplot as plt
import random

# Extract time, x, y from the loaded data
def get_data_from_txt(filepath):
    lines = []
    with open(filepath, 'r') as file:
        lines = file.readlines()
        data = []
    for line in lines:
        match = re.findall(r'\(([^,]+),([^,]+),([^,]+)\)', line)
        if match:
            data.append(tuple(map(float, match[0])))

    data = np.array(data, dtype=[('timestamp', float), ('x', float), ('y', float)])
    time = data['timestamp']
    x = data['x']
    y = data['y']
    arrayLength = 3000
    return x,y,time

def get_complex_transformation(x,y):
    return x + 1j * y

def get_slices(complex_transformation,slicesize):
    slices = []
    for i in range(0,len(complex_transformation),slicesize):
        #print(complex_transformation[i:i+slicesize])
        slices.append(complex_transformation[i:i+slicesize])
        #print(len(slices))
    #print(slices[0])
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

def revert_from_complex_numbers(slice,time):
    points = []
    for i in range(0,len(slice)):
            points.append((time[i],slice[i].real,slice[i].imag))
    return points

def run():
    sliceSize = 16
    strength = 0.0003
    data = get_data_from_txt('out.txt')
    complex_transformation = get_complex_transformation(data[0],data[1])
    slices = get_slices(complex_transformation,sliceSize)
    #print(len(slices))
    watermarked_data = []
    #print(slices)
    for i in range (0,len(slices)-1):
        if len(slices[i])<1:
            continue
        watermark = generate_watermark(sliceSize)
        fft = get_FFT(slices[i])
        embedded_data = embed_watermark(fft,watermark,strength)
        ifft = get_IFFT(embedded_data)
        reverted_ifft = revert_from_complex_numbers(ifft,data[2][i*sliceSize:(i+1)*sliceSize])
        for i in reverted_ifft:
            watermarked_data.append(i)
    print(watermarked_data)



run()


# Compute FFT
'''
fft_result = np.fft.fft(get_data_from_txt)

# Compute the frequencies corresponding to the FFT result
#freq = np.fft.fftfreq(len(time), d=(time[1] - time[0]))

# Plot the results
plt.figure(figsize=(10, 6))
# Plot the real part of the FFT result
plt.subplot(2, 1, 1)
plt.plot(np.real(fft_result))
plt.title('Real Part of FFT')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')

# Plot the imaginary part of the FFT result
plt.subplot(2, 1, 2)
plt.plot(np.imag(fft_result))
plt.title('Imaginary Part of FFT')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')

plt.tight_layout()
plt.show()'''