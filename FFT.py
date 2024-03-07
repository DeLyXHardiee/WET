import numpy as np
import re
import matplotlib.pyplot as plt

lines = []
with open('out.txt', 'r') as file:
    lines = file.readlines()

# Extract time, x, y from the loaded data
data = []
for line in lines:
    match = re.findall(r'\(([^,]+),([^,]+),([^,]+)\)', line)
    if match:
        data.append(tuple(map(float, match[0])))

data = np.array(data, dtype=[('timestamp', float), ('x', float), ('y', float)])
time = data['timestamp']
x = data['x']
y = data['y']

signal_to_analyze = x + 1j * y

# Compute FFT
fft_result = np.fft.fft(signal_to_analyze)

# Compute the frequencies corresponding to the FFT result
freq = np.fft.fftfreq(len(time), d=(time[1] - time[0]))

# Plot the results
plt.figure(figsize=(10, 6))
# Plot the real part of the FFT result
plt.subplot(2, 1, 1)
plt.plot(freq, np.real(fft_result))
plt.title('Real Part of FFT')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')

# Plot the imaginary part of the FFT result
plt.subplot(2, 1, 2)
plt.plot(freq, np.imag(fft_result))
plt.title('Imaginary Part of FFT')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')

plt.tight_layout()
plt.show()