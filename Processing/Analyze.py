import numpy as np
from memory_profiler import profile

eyes = np.array([0.0,3.6,55.0])

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
                fixation_result = calculate_rms(current_fixation)
                fixation_rms_results.append(fixation_result)
                current_fixation = []
    if current_fixation:
        fixation_result = calculate_rms(current_fixation)
        fixation_rms_results.append(fixation_result)

    average_rms = sum(fixation_rms_results) / len(fixation_rms_results) if fixation_rms_results else 0
    return average_rms

def calculate_rms(fixation):
    x_values = np.array([point[1] for point in fixation])
    y_values = np.array([point[2] for point in fixation])
    
    x_mean = np.mean(x_values)
    x_values = np.subtract(x_values, x_mean)
    y_mean = np.mean(y_values)
    y_values = np.subtract(y_values, y_mean)

    rms_x = np.sqrt(np.mean(np.array(x_values) ** 2))
    rms_y = np.sqrt(np.mean(np.array(y_values) ** 2))
    
    return np.sqrt(rms_x ** 2 + rms_y ** 2) / 1000

#go through points in dataset before modifictaion and after and measure the degree of change in the two datapoints
def measure_degrees_of_visual_angle(modifiedData, unmodifiedData):
    acc = 0
    for i in range(len(unmodifiedData)):
        #print(unmodifiedData[i])
        a = np.array([unmodifiedData[i][1],unmodifiedData[i][2],0.0])
        #print(a)
        b = np.array([modifiedData[i][1],modifiedData[i][2],0.0])
        acc += angle_between_points(a,eyes,b)
    return acc/len(unmodifiedData)

def angle_between_points(A, B, C):
    # Calculate vectors AB and BC
    BA = A - B
    BC = C - B 
    cosine_angle = np.dot(BA, BC) / (np.linalg.norm(BA) * np.linalg.norm(BC))
    angle = np.arccos(cosine_angle)
    return np.degrees(angle)

def normalized_cross_correlation(signal1, signal2):
    # Convert signals to numpy arrays
    signal1 = np.array(signal1)
    signal2 = np.array(signal2)
    print("NCC")

    return np.corrcoef(signal1, signal2)[0, 1]
