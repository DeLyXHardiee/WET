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

def generate_watermark(length, strength_range, wm_length):
    number_of_zeroes = 0
    max_zero = int(wm_length * 0.375)
    watermark = []
    while len(watermark) < wm_length:
        randomnr = random.uniform(-strength_range, strength_range)
        if randomnr != 0:
            watermark.append(randomnr)
        else:
            if number_of_zeroes < max_zero:
                watermark.append(randomnr)
                number_of_zeroes = number_of_zeroes + 1
    repetitions = length // wm_length  # Calculate the number of repetitions needed
    remainder = length % wm_length  # Calculate the remaining length after repetitions
    if repetitions > 0:
        watermark *= repetitions  # Repeat the watermark
    if remainder > 0:
        watermark += watermark[:remainder]  # Add the remaining part of the watermark
    watermark = np.array(watermark)
    return watermark

def get_FFT(complex_transformation):
    fft_result = np.fft.fft(complex_transformation)
    return fft_result

def embed_watermark(fft, watermark):
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

def run_watermark(data, strength_range, wm_size=16):
    new_data = []
    watermark = generate_watermark(len(data), strength_range, wm_size)
    for idx in range(0, len(data), wm_size):
        end_idx = min(idx + wm_size, len(data))
        # Extract a slice from the complex transformation
        complex_slice = get_complex_transformation(data[idx:end_idx])
        # Get the FFT of the slice
        fft_slice = get_FFT(complex_slice)
        # Embed a slice of the watermark in the slice
        embedded_slice = embed_watermark(fft_slice, watermark[idx:end_idx])
        # Get the IFFT of the slice
        ifft_slice = get_IFFT(embedded_slice)
        new_data.extend(revert_from_complex_numbers(ifft_slice, data[idx:end_idx]))
    return new_data, watermark

def unrun_watermark(watermarked_data, original_data, strength_range, wm_size=16):
    watermark = []
    if len(watermarked_data) != len(original_data):
        raise ValueError("Length of true data and predicted data must be the same")
    for idx in range(0, len(original_data), wm_size):
        end_idx = min(idx + wm_size, len(original_data))
        complex_slice_original = get_complex_transformation(original_data[idx:end_idx])
        complex_slice_wm = get_complex_transformation(watermarked_data[idx:end_idx])
        fft_slice_original = get_FFT(complex_slice_original)
        fft_slice_wm = get_FFT(complex_slice_wm)
        extracted_watermark_slice = extract_watermark(fft_slice_original, fft_slice_wm)
        watermark.extend(extracted_watermark_slice)
    return watermark