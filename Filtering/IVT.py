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
    print(len(true_data))
    print(len(predicted_data))
    if len(true_data) != len(predicted_data):
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
        raise ValueError("Length of true labels and predicted labels must be the same")

    total_points = len(true_labels)
    correct_predictions = sum(1 for true, pred in zip(true_labels, predicted_labels) if true == pred)

    accuracy = correct_predictions / total_points
    return accuracy

def transform_tuples(list_of_lists):
    transformed_list = []
    for nested_list in list_of_lists:
        if len(nested_list) == 1:
                # If nested list has size 1, set fourth element of tuple to 2
                transformed_tuples = [(t[0], t[1], t[2], 2) for t in nested_list]
        else:
            # If nested list has size > 1, set fourth element of all tuples to 1
            transformed_tuples = [(t[0], t[1], t[2], 1) for t in nested_list]
        transformed_list.append(transformed_tuples)
    return transformed_list

def flatten_nested_list(nested_list):
    flattened_list = []
    for sublist in nested_list:
        for item in sublist:
            flattened_list.append(item)
    return flattened_list


def calculate_velocity(point1, point2):
    """Calculate velocity between two points."""
    dx = point2[1] - point1[1]
    dy = point2[2] - point1[2]
    dt = point2[0] - point1[0]
    velocity = np.sqrt(dx**2 + dy**2) / dt
    return velocity


def average_velocity(points):
    """Find the average velocity between consecutive points."""
    if len(points) < 2:
        return None  # Not enough points to calculate velocity

    total_velocity = 0.0
    count = 0

    for i in range(len(points) - 1):
        if (points[i][3] == 1 and points[i+1][3] == 2 or points[i+1][3] == 1 and points[i][3] == 2):
            velocity = calculate_velocity(points[i], points[i+1])
            if velocity == 0.0:
                continue
            total_velocity += velocity
            count += 1

    if count == 0:
        return 0.0  # No valid pairs of consecutive points

    return total_velocity / count


def i_vt(protocol, velocity_threshold):
    """Implement I-VT algorithm with velocity and acceleration thresholds."""
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

def i_vt_2(protocol, velocity_threshold, acceleration_threshold):
    """Implement I-VT algorithm with velocity and acceleration thresholds."""
    fixations = []
    velocities = []
    velocity_sum = 0
    for i in range(len(protocol)):
        point = protocol[i]
        if (point[3] == -1):
            print("Iteration: " + str(i))
            print("velocity sum: " + str(velocity_sum))
            fixations.append((point[0], point[1], point[2], 1, 0))
            velocities.append(0)
            continue
        if len(fixations) == 0:
            fixations.append((point[0], point[1], point[2], 1, 0))
            velocities.append(0)
        else:
            velocity = calculate_velocity(fixations[-1], point)
            acceleration = calculate_acceleration(fixations[-1], point)
            if (i < 39):
                velocities.append(velocity)
            elif (i == 39):
                velocities.append(velocity)
                velocity_sum = sum(velocities)
                velocity_threshold = velocity_sum / 40
            elif (i > 39):
                velocity_sum = velocity_sum - velocities[i % 40]
                velocity_sum = velocity_sum + velocity
                velocities[i % 40] = velocity
                velocity_threshold = velocity_sum / 40
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

def i_vt_acceleration(protocol, velocities, acceleration_threshold):
    """Implement I-VT algorithm with velocity and acceleration thresholds."""
    fixations = []
    for i in range(len(protocol)):
        point = protocol[i]
        if len(fixations) == 0:
            fixations.append((point[0], point[1], point[2], point[3], point[4]))
        else:
            acceleration = calculate_acceleration(velocities[i-1], velocities[i], 0.001)
            if acceleration > acceleration_threshold:
                fixations.append((point[0], point[1], point[2], 2))
            else:
                fixations.append(point)
    return fixations

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
protocol = extract_data("S_1003_S1_RAN.csv").apply(lambda row: (row['n'], row['x'], row['y'], row['lab']), axis=1)
#print("Smallest velocity: " + str(smallest_velocity(protocol)))
average = average_velocity(protocol)
print("Average velocity: " + str(average))
fixations = i_vt_2(protocol, average, 0)

#fixations = i_vt(protocol, average)
#fixations_vel = i_vt_acceleration(fixations, velocities, 20)
#fixations = transform_tuples(fixations)
write_tuples_to_csv(fixations,'out.txt')
#flattened_fixation = flatten_nested_list(fixations)
print("Total data accuracy: " + str(calculate_accuracy(protocol, fixations)))
print("Saccade accuracy: " + str(measure_saccade_accuracy(protocol, fixations)))



