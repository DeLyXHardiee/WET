import numpy as np
from memory_profiler import profile

def measure_saccade_accuracy(true_data, predicted_data):
    if len(true_data) != len(predicted_data):
        raise ValueError("Length of true data and predicted data must be the same")

    # Extract saccade labels from true and predicted data
    true_saccades = [point for point in true_data if point[3] == 2]
    predicted_saccades = [point for point in predicted_data if point[3] == 2]

    # Calculate intersection of true and predicted saccades
    true_positives = 0
    for point in predicted_saccades:
        for true_point in true_saccades:
            if (point[0] == true_point[0]) & (point[3] == true_point[3]):
                true_positives += 1
                continue
    
    # Calculate precision and recall
    precision = true_positives / len(predicted_saccades) if predicted_saccades else 0
    recall = true_positives / len(true_saccades) if true_saccades else 0

    # Calculate accuracy as the harmonic mean of precision and recall (F1 score)
    accuracy = 2 * (precision * recall) / (precision + recall) if precision + recall > 0 else 0
    return accuracy

def measure_rms_precision(data):
    current_fixation = []
    fixation_rms_results = []

    for point in data:
        if point[3] == 1: 
            current_fixation.append(point)
        else: 
            if current_fixation: 
                fixation_result = calculate_fixation_rms(current_fixation)
                fixation_rms_results.append(fixation_result)
                current_fixation = []

    if current_fixation:
        fixation_result = calculate_fixation_rms(current_fixation)
        fixation_rms_results.append(fixation_result)

    average_rms = sum(fixation_rms_results) / len(fixation_rms_results) if fixation_rms_results else 0

    return average_rms

def calculate_fixation_rms(fixation):
    return

def distance_between_points(point1, point2):
    return np.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

def calculate_rms(values):
    return np.sqrt(np.mean(values**2))

def normalized_cross_correlation(signal1, signal2):
    # Convert signals to numpy arrays
    signal1 = np.array(signal1)
    signal2 = np.array(signal2)
    print("NCC")

    return np.corrcoef(signal1, signal2)[0, 1]
