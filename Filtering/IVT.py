import numpy as np
import csv
from ExtractDataFromCSV import extract_data
import numpy as np

import math

def check_for_nan(number):
    if math.isnan(number):
        return True
    else:
        return False


def measure_saccade_accuracy(true_data, predicted_data):
    if len(true_data) != len(predicted_data):
        print("Length of true data: " + str(len(true_data)))
        print("Length of predicted data: " + str(len(predicted_data)))
        raise ValueError("Length of true data and predicted data must be the same")

    # Extract saccade labels from true and predicted data
    true_saccades = [point for point in true_data if point[3] == 2]
    predicted_saccades = [point for point in predicted_data if point[3] == 2]

    # Calculate intersection of true and predicted saccades
    true_positives = sum(1 for point in predicted_saccades if point in true_saccades)

    # Calculate precision and recall
    precision = true_positives / len(predicted_saccades) if predicted_saccades else 0
    recall = true_positives / len(true_saccades) if true_saccades else 0

    # Calculate accuracy as the harmonic mean of precision and recall (F1 score)
    accuracy = 2 * (precision * recall) / (precision + recall) if precision + recall > 0 else 0

    return accuracy

def calculate_accuracy(true_labels, predicted_labels):
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

""" Calculate the average velocity when a fixation goes to a saccade or the oppossite"""
def average_velocity(points):
    """Find the average velocity between consecutive points."""
    if len(points) < 2:
        return None  # Not enough points to calculate velocity

    total_velocity = 0.0
    count = 0

    for i in range(len(points) - 1):
        if (points[i][3] == 1 and points[i+1][3] == 2 or points[i+1][3] == 1 and points[i][3] == 2):
            velocity = calculate_velocity(points[i], points[i+1])
            if velocity == 0.0 or check_for_nan(velocity):
                continue
            total_velocity += velocity
            count += 1

    if count == 0:
        return 0.0  # No valid pairs of consecutive points

    return total_velocity / count

"""I-VT algorithm with fixation groups"""
def i_vt(protocol, velocity_threshold):

    fixation_points = []
    current_group = []

    for i in range(len(protocol)):
        point = protocol[i]
        if len(current_group) == 0:
            current_group.append(point)
        else:
            velocity = calculate_velocity(current_group[-1], point)
            if velocity < velocity_threshold:
                current_group.append(point)
            else:
                fixation_points.append(current_group)
                point = (point[0], point[1], point[2], 2)
                current_group = [point]

    # Append the last group (if any)
    if current_group:
        fixation_points.append(current_group)

    return fixation_points

"""I-VT algorithm with recalculation of velocity threshold during analysis"""
def i_vt_2(protocol, velocity_threshold, recalculate):

    fixations = []
    velocities = []
    velocity_sum = 0
    counter = 0
    for i in range(len(protocol)):
        point = protocol[i]
        if len(fixations) == 0:
            fixations.append(point)
            velocities.append(0)
            counter += 1
        else:
            velocity = calculate_velocity(fixations[-1], point)
            if (check_for_nan(velocity)):
                fixations.append(point)
                continue
            if (counter < recalculate):
                velocities.append(velocity)
                counter += 1
            elif (counter == recalculate):
                velocities.append(velocity)
                velocity_sum = sum(velocities)
                velocity_threshold = velocity_sum / recalculate
                counter += 1
            elif (counter > recalculate):
                velocity_sum = velocity_sum - velocities[counter % recalculate]
                velocity_sum = velocity_sum + velocity
                velocities[i % recalculate] = velocity
                velocity_threshold = velocity_sum / recalculate
                counter += 1
            if velocity < velocity_threshold:
                fixations.append((point[0], point[1], point[2], 1))
            else:
                fixations.append((point[0], point[1], point[2], 2))
    return fixations

"""I-VT algorithm without fixation groups"""
def i_vt_3(protocol, velocity_threshold):
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

def calculate_acceleration(point1, point2):
    """Calculate acceleration between two points."""
    dx1 = point2[1] - point1[1]
    dy1 = point2[2] - point1[2]
    dt1 = point2[0] - point1[0]
    velocity1 = np.sqrt(dx1 ** 2 + dy1 ** 2) / dt1

    dx2 = point2[1] - point1[1]
    dy2 = point2[2] - point1[2]
    dt2 = point2[0] - point1[0]
    velocity2 = np.sqrt(dx2 ** 2 + dy2 ** 2) / dt2

    acceleration = (velocity2 - velocity1) / dt2
    return acceleration

def find_best_threshold(protocol):
    # Define a range of possible velocity thresholds
    threshold_range = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10]

    best_threshold = 0.0
    best_f1_score = 0.0
    fixations = []
    best_fixations = []

    for threshold in threshold_range:
        # Apply I-VT algorithm with current threshold to segment dataset
        # ivt_output = apply_ivt_algorithm(dataset, threshold)

        # Calculate F1 score using ground truth labels and ivt_output
        fixations = i_vt_3(protocol, threshold)
        f1_score = measure_saccade_accuracy(protocol, fixations)

        # Update best threshold if F1 score is higher
        if f1_score > best_f1_score:
            best_threshold = threshold
            best_f1_score = f1_score
            best_fixations = fixations

    return best_threshold, best_f1_score, calculate_accuracy(protocol, best_fixations)

def write_tuples_to_csv(tuples, filename):
    #print(len(tuples))
    """Write tuples to a CSV file with row numbers."""
    with open(filename, 'w') as file:
        counter = 0
        for fixation in tuples:
            counter +=1
            #if len(fixation) < 2:
                #continue
            #print(counter)
            file.write("\n")
            file.write("counter: " + str(counter))
            file.write("\n")
            for data in fixation:
                # Access depth value at this point
                file.write(str(data))
                file.write("\n")


# Example usage:
#protocol = extract_data("S_9016_S1_RAN.csv").apply(lambda row: (row['n'], row['x'], row['y'], row['lab']), axis=1)
#protocol = extract_data("S_1002_S1_RAN.csv").apply(lambda row: (row['n'], row['x'], row['y'], row['lab']), axis=1)
protocol = extract_data("../Datasets/RandomSaccades/S_9016_S1_RAN.csv").apply(lambda row: (row['n'], row['x'], row['y'], row['lab']), axis=1)

threshold, f1, total_accuracy = find_best_threshold(protocol)
#write_tuples_to_csv(fixations,'out.txt')

print("Best threshold: " + str(threshold))
print("Saccade accuracy: " + str(f1))
print("Total accuracy: " + str(total_accuracy))



