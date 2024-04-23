import numpy as np
from memory_profiler import profile

eyes = (0,0,55)

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

#go through points in dataset before modifictaion and after and measure the degree of change in the two datapoints
def measure_degrees_of_visual_angle(modifiedData, unmodifiedData):
    acc = 0
    for i in range(len(unmodifiedData)):
        a = (unmodifiedData[i][1][0],unmodifiedData[i][1][1],0)
        b = (modifiedData[i][2][0],modifiedData[i][2][1],0)
        acc += angle_between_points(a,b,eyes)
    return acc/len(unmodifiedData)

def angle_between_points(A, B, C):
    # Calculate vectors AB and BC
    AB = np.array(B) - np.array(A)
    BC = np.array(C) - np.array(B)
    
    # Calculate dot product
    dot_product = np.dot(AB, BC)
    
    # Calculate magnitudes of vectors
    magnitude_AB = np.linalg.norm(AB)
    magnitude_BC = np.linalg.norm(BC)
    
    # Calculate cosine of the angle
    cos_angle = dot_product / (magnitude_AB * magnitude_BC)
    
    # Convert cosine to angle in degrees
    angle = np.arccos(cos_angle)
    angle_degrees = np.degrees(angle)
    
    return angle_degrees

def normalized_cross_correlation(signal1, signal2):
    # Convert signals to numpy arrays
    signal1 = np.array(signal1)
    signal2 = np.array(signal2)
    print("NCC")

    return np.corrcoef(signal1, signal2)[0, 1]