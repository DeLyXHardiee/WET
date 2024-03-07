import math
from ExtractDataFromCSV import extract_data

subject = (0, 0, 55)

def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def calculate_centroid_distance(points):
    if len(points) < 2:
        return 0
    x_values = [point[1] for point in points]
    y_values = [point[2] for point in points]
    mean_x = sum(x_values) / len(x_values)
    mean_y = sum(y_values) / len(y_values)
    return max(calculate_distance(mean_x, mean_y, point[1], point[2]) for point in points)

def IDT(eye_tracking_data, duration_threshold, dispersion_threshold):
    fixations = []
    duration = 0
    isFixation = False
    num_fixations = 0
    current_fixation = []
    tuple_values = eye_tracking_data.apply(lambda row: (row['n'], row['x'], row['y'], row['lab']), axis=1)
    for i in range (0,int(len(tuple_values))):
        if (math.isnan(tuple_values[i][1])) | (math.isnan(tuple_values[i][2])):
            point = tuple_values[i]
            fixations.append((point[0], point[1], point[2], 0))
            continue
        #print("tuple values: \n" + str(tuple_values[i]))
        if i > 0:
            if ((tuple_values[i-1][3] == 1) & (tuple_values[i][3] == 2)):
                num_fixations += 1
        current_fixation.append(tuple_values[i])
        duration += 1
        #print(duration)
        if duration >= duration_threshold:
            #print(calculate_centroid_distance(current_fixation))
            if calculate_centroid_distance(current_fixation) <= dispersion_threshold:
                #print(calculate_centroid_distance(current_fixation))
                #print(dispersion_threshold)
                isFixation = True
                if i == len(eye_tracking_data) - 1:
                    for point in current_fixation:
                        fixations.append((point[0], point[1], point[2], 1))
            else:
                if isFixation:
                    new_start = current_fixation.pop()
                    isFixation = False
                    for point in current_fixation:
                        fixations.append((point[0], point[1], point[2], 1))
                    current_fixation = [new_start]
                    duration = 0
                else:
                    while calculate_centroid_distance(current_fixation) > dispersion_threshold:
                        point = current_fixation.pop(0)
                        fixations.append((point[0], point[1], point[2], 2))
                        duration -= 1
    print("num_fixations: "  + str(num_fixations))
    return fixations 

'''
eye_tracking_data = [
    (0, 100, 100),  # Timestamp, x-coordinate, y-coordinate
    (100, 105, 102),
    (200, 110, 98),
    (300, 115, 95),
    (400, 117, 94),
    (500, 120, 90),
    (600, 125, 87),
    (700, 130, 85),
    (800, 135, 82),
    (900, 140, 80),
    (1000, 145, 78),
    (1100, 350, 75),
    (1200, 355, 73),
    (1300, 360, 70),
    (1400, 365, 68),
    (1500, 370, 65),
    (1600, 375, 63),
    (1700, 380, 60),
    (1800, 385, 58),
    (1900, 390, 55),
    (2000, 2500, -1500),
    (2100, 2505, -1502),
    (2200, 2510, -1504),
    (2300, 2515, -1506),
    (2400, 2520, -1508),
    (2500, 400, 100),
    (2600, 510, 115)
]
'''

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

eye_tracking_data = extract_data('S_1002_S1_RAN.csv')

screen_display = (474, 297)  # Screen display (width x height)
distance_from_screen = 550

# Long fixations and eye drifting / smooth pursuits are a major issue. They often get separated into different fixations.
duration_threshold = 30
dispersion_threshold = 0.5
hz = 1000

fixations = IDT(eye_tracking_data, duration_threshold, dispersion_threshold)

print("Fixations:")
print(len(fixations))
write_tuples_to_csv(fixations,'out2.txt')

protocol = extract_data("S_1002_S1_RAN.csv").apply(lambda row: (row['n'], row['x'], row['y'], row['lab']), axis=1)

print("Saccade accuracy: " + str(measure_saccade_accuracy(protocol, fixations)))
#for fixation in fixations:
    #print(len(fixation))