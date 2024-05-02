import numpy as np
import math
from memory_profiler import profile

eyes = np.array([0.0,3.6,55.0])

def measure_saccade_accuracy(true_data, predicted_data):
    if len(true_data) != len(predicted_data):
        print("Truth: " + str(len(true_data)))
        print("Predicted: " + str(len(predicted_data)))
        #raise ValueError("Length of true data and predicted data must be the same")

    # Extract saccade labels from true and predicted data
    true_saccades = {(point[0], point[3]) for point in true_data if point[3] == 2}
    predicted_saccades = {(point[0], point[3]) for point in predicted_data if point[3] == 2}

    # Calculate intersection of true and predicted saccades
    true_positives = len(true_saccades.intersection(predicted_saccades))

    # Calculate precision and recall
    precision = true_positives / len(predicted_saccades) if predicted_saccades else 0
    recall = true_positives / len(true_saccades) if true_saccades else 0

    # Calculate accuracy as the harmonic mean of precision and recall (F1 score)
    accuracy = 2 * (precision * recall) / (precision + recall) if precision + recall > 0 else 0
    return accuracy

def denoise_saccade_onset(gaze_data, SACCADE_ONSET_DELAY_MS=4):
    denoised_data = []
    current_fixation = []
    current_saccade = []
    denoise_count = 0
    for i, (time, x, y, lab) in enumerate(gaze_data):
        if lab == 1:  # Fixation
            current_fixation.append((time, x, y, lab))

            # Check for saccade onset delay
            if current_saccade and (time - current_saccade[0][0]) < SACCADE_ONSET_DELAY_MS:
                # Transition from saccade to fixation
                # Update label of the saccade to fixation (2 to 1)
                current_saccade = [(t, xx, yy, 1) for t, xx, yy, _ in current_saccade]
                denoised_data.extend(current_saccade)
                current_saccade = []
                denoise_count = denoise_count + 1
            elif current_saccade and (time - current_saccade[0][0]) >= SACCADE_ONSET_DELAY_MS:
                denoised_data.extend(current_saccade)
                current_saccade = []

        elif lab == 2:  # Saccade
            current_saccade.append((time, x, y, lab))
            if current_fixation:
                denoised_data.extend(current_fixation)
                current_fixation = []


    # Append any remaining fixations or saccades
    denoised_data.extend(current_fixation)
    denoised_data.extend(current_saccade)
    print("Denoise count: " + str(denoise_count))
    return denoised_data

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
        fixation_result = calculate_rms(current_fixation)
        fixation_rms_results.append(fixation_result)

    average_rms = sum(fixation_rms_results) / len(fixation_rms_results) if fixation_rms_results else 0
    return average_rms

def euclidean_distance(coordinates, x_center, y_center):
    distances = [np.sqrt((point[1] - x_center)**2 + (point[2] - y_center)**2) for point in coordinates]
    return distances

def calculate_rms(fixation):
    x_values = np.array([point[1] for point in fixation])
    y_values = np.array([point[2] for point in fixation])
    
    x_mean = np.mean(x_values)
    #x_values = np.subtract(x_values, x_mean)
    y_mean = np.mean(y_values)
    #y_values = np.subtract(y_values, y_mean)

    distances = euclidean_distance(fixation, x_mean, y_mean)

    rms = np.sqrt(np.mean(np.array(distances) ** 2))
    #rms_y = np.sqrt(np.mean(np.array(y_values) ** 2))
    
    #return np.sqrt(rms_x ** 2 + rms_y ** 2)
    return rms

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
    """
    Calculate the angular distance between two points in degrees.

    Args:
    - point1 (tuple): Coordinates (x, y) of the first point in degrees.
    - point2 (tuple): Coordinates (x, y) of the second point in degrees.

    Returns:
    - angular_dist (float): Angular distance between the points in degrees.
    """
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
'''
def measure_degrees_of_visual_angle(data):
    acc = 0
    nanCounter = 0
    for i in range(len(data)):
        #print(data[i])
        p1 = [data[i][1],data[i][2]]
        #print(a)
        p2 = [data[i][4],data[i][5]]
        dist = math.dist(p1,p2)        
        acc += dist
        #if dist > 10:
        #    print(dist)
    return acc/(len(data)-nanCounter)    
'''
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
    ncc = np.corrcoef(signal1, signal2)[0, 1]
    #print("NCC: " + str(ncc))
    return ncc

#test_data = [(1, 1, 1, 1), (2, 1, 1, 1), (3, 1, 1, 2), (4, 1, 1, 2), (5, 1, 1, 2),
 #(6, 1, 1, 2), (7, 1, 1, 1), (8, 1, 1, 1), (9, 1, 1, 1), (10, 1, 1, 1),
 #(11, 12, 1, 1), (12, 1, 1, 1), (13, 1, 1, 1), (14, 1, 1, 1), (15, 1, 1, 1),
 #(16, 1, 1, 2), (17, 1, 1, 2), (18, 1, 1, 1), (19, 1, 1, 1), (20, 1, 1, 1)]

#print(denoise_saccade_onset(test_data))