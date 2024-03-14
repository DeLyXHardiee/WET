import numpy as np
import numpy as np
import Analysis.Analyze as an

import math

def check_for_nan(number):
    if math.isnan(number):
        return True
    else:
        return False

def calculate_label_accuracy(true_labels, predicted_labels):
    if len(true_labels) != len(predicted_labels):
        print("Length of true data: " + str(len(true_labels)))
        print("Length of predicted data: " + str(len(predicted_labels)))
        raise ValueError("Length of true labels and predicted labels must be the same")

    total_points = len(true_labels)
    correct_predictions = sum(1 for true, pred in zip(true_labels, predicted_labels) if true == pred)

    accuracy = correct_predictions / total_points
    return accuracy

def calculate_velocity(point1, point2):
    """Calculate velocity between two points."""
    dx = point2[1] - point1[1]
    dy = point2[2] - point1[2]
    dt = point2[0] - point1[0]
    velocity = np.sqrt(dx**2 + dy**2) / dt
    return velocity

"""I-VT algorithm without fixation groups"""
def IVT(protocol, velocity_threshold=0):
    if velocity_threshold == 0:
        velocity_threshold = find_best_threshold(protocol)
    fixations = []
    for i in range(len(protocol)):
        point = protocol[i]
        if len(fixations) == 0:
            fixations.append(point)
        else:
            velocity = calculate_velocity(fixations[-1], point)
            if check_for_nan(velocity):
                fixations.append(point)
                continue
            if velocity < velocity_threshold:
                fixations.append((point[0], point[1], point[2], 1))
            else:
                fixations.append((point[0], point[1], point[2], 2))
    return fixations

def find_best_threshold(protocol):
    # Define a range of possible velocity thresholds
    threshold_range = [0.04, 0.05, 0.06, 0.07, 0.08]

    best_threshold = 0.0
    best_f1_score = 0.0
    fixations = []

    for threshold in threshold_range:
        # Apply I-VT algorithm with current threshold to segment dataset
        # ivt_output = apply_ivt_algorithm(dataset, threshold)

        # Calculate F1 score using ground truth labels and ivt_output
        fixations = IVT(protocol, threshold)
        f1_score = an.measure_saccade_accuracy(protocol, fixations)

        # Update best threshold if F1 score is higher
        if f1_score > best_f1_score:
            best_threshold = threshold
            best_f1_score = f1_score

    return best_threshold
