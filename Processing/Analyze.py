import numpy as np
import math
from memory_profiler import profile

eyes = np.array([0.0,3.6,55.0])

def measure_saccade_accuracy(true_data, predicted_data):
    if len(true_data) != len(predicted_data):
        print("Truth: " + str(len(true_data)))
        print("Predicted: " + str(len(predicted_data)))
        raise ValueError("Length of true data and predicted data must be the same")

    # Extract saccade labels from true and predicted data
    true_saccades = [point for point in true_data if point[3] == 2]
    predicted_saccades = [point for point in predicted_data if point[3] == 2]
    print("Truth: " + str(len(true_saccades)))
    print("Predicted: " + str(len(predicted_saccades)))

    # Calculate intersection of true and predicted saccades
    true_positives = 0
    for point in predicted_saccades:
        for true_point in true_saccades:
            if (point[0] == true_point[0]) & (point[3] == true_point[3]):
                true_positives += 1
                break
    print("True positives: " + str(true_positives))
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
                fixation_result = calculate_inter_sample_angular_distance(current_fixation)
                fixation_rms_results.append(fixation_result)
                current_fixation = []
    if current_fixation:
        fixation_result = calculate_inter_sample_angular_distance(current_fixation)
        fixation_rms_results.append(fixation_result)

    average_rms = sum(fixation_rms_results) / len(fixation_rms_results) if fixation_rms_results else 0
    return average_rms

def calculate_inter_sample_angular_distance(fixation):
    if len(fixation) < 2:
        return 0
    distances = []
    for i in range(1, len(fixation)):
        # Calculate angular distance between consecutive points
        angular_dist = angular_distance(fixation[i-1], fixation[i])
        distances.append(angular_dist)

    # Calculate RMS of inter-sample angular distances
    rms = np.sqrt(np.mean(np.array(distances) ** 2))

    return rms

def angular_distance(point1, point2):
    # Convert points to numpy arrays
    p1 = np.array([point1[1], point1[2]])
    p2 = np.array([point2[1], point2[2]])

    # Calculate difference between coordinates
    diff = p2 - p1

    # Calculate angular distance using Pythagorean theorem
    angular_dist = np.sqrt(np.sum(diff ** 2))

    return angular_dist

#go through points in dataset before modifictaion and after and measure the degree of change in the two datapoints
def measure_degrees_of_visual_angle(modifiedData, unmodifiedData):
    acc = 0
    nanCounter = 0
    max = 0
    for i in range(len(unmodifiedData)):
        if np.isnan(unmodifiedData[i][1]):
            nanCounter += 1
            continue
        #print(unmodifiedData[i])
        p1 = [unmodifiedData[i][1],unmodifiedData[i][2]]
        #print(a)
        p2 = [modifiedData[i][1],modifiedData[i][2]]
        dist = math.dist(p1,p2)
        acc += dist
        if dist > max:
            max = dist
    print("max: " + str(max))
    return acc/(len(unmodifiedData)-nanCounter)

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
