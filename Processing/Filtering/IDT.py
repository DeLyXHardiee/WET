import math
import CSVUtility
from Processing.Embed_watermark import run

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

def find_tresholds(eye_tracking_data):
    min_duration = 10000
    max_dispersion = 0
    current_fixation = []
    tuple_values = eye_tracking_data.apply(lambda row: (row['n'], row['x'], row['y'], row['lab']), axis=1)
    for i in range (0,int(len(tuple_values))):
        if tuple_values[i][3] == 1:
            current_fixation.append(tuple_values[i])
        if (tuple_values[i][3] == 2) & (len(current_fixation) > 0):
            if (len(current_fixation)) < min_duration:
                min_duration = len(current_fixation)
            if calculate_centroid_distance(current_fixation) > max_dispersion:
                max_dispersion = calculate_centroid_distance(current_fixation)
            current_fixation = []
    print("min duration : " + str(min_duration))
    print("max dispersion : " + str(max_dispersion))

def IDT(eye_tracking_data, duration_threshold, dispersion_threshold):
    fixations = []
    duration = 0
    isFixation = False
    num_fixations = 0
    current_fixation = []
    tuple_values = eye_tracking_data#.apply(lambda row: (row['n'], row['x'], row['y'], row['lab']), axis=1)
    for i in range (0,int(len(tuple_values))):
        if (math.isnan(tuple_values[i][1])) | (math.isnan(tuple_values[i][2])):
            point = tuple_values[i]
            fixations.append((point[0], point[1], point[2], 0))
            continue
        #print("tuple values: \n" + str(tuple_values[i]))
        #if i > 0:
        #    if ((tuple_values[i-1][3] == 1) & (tuple_values[i][3] == 2)):
        #        num_fixations += 1
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

def write_tuples_to_txt(tuples,filename):
    with open(filename,'w') as file:
        for data in tuples:
            if (math.isnan(data[1])):
                continue
            file.write(str(data[0:4]))
            file.write('\n')

def read_tuples_from_txt(filename):
    result = []
    with open(filename, 'r') as file:
        for line in file:
            current_tuple = eval(line.strip())
            result.append(current_tuple)
    return result

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
    #true_positives = sum(1 for point in predicted_saccades if point in true_saccades)

    # Calculate precision and recall
    precision = true_positives / len(predicted_saccades) if predicted_saccades else 0
    recall = true_positives / len(true_saccades) if true_saccades else 0

    # Calculate accuracy as the harmonic mean of precision and recall (F1 score)
    accuracy = 2 * (precision * recall) / (precision + recall) if precision + recall > 0 else 0

    return accuracy

def run_IDT_original_data(filepath, duration_threshold=30, dispersion_threshold=0.5):
    eye_tracking_data = CSVUtility.extract_original_data(filepath)
    return IDT(eye_tracking_data, duration_threshold, dispersion_threshold)

def run_IDT(filepath, duration_threshold=30, dispersion_threshold=0.5):
    eye_tracking_data = CSVUtility.extract_original_data(filepath)
    return IDT(eye_tracking_data, duration_threshold, dispersion_threshold)

filepath = '../Datasets/Reading/S_1004_S2_TEX.csv'
eye_tracking_data = read_tuples_from_txt('../IDT_watermarked_S_1004_S2_TEX.txt')#extract_data(filepath)
#eye_tracking_data = extract_data(filepath)

screen_display = (474, 297)  # Screen display (width x height)
distance_from_screen = 550

# Long fixations and eye drifting / smooth pursuits are a major issue. They often get separated into different fixations.
duration_threshold = 30
dispersion_threshold = 0.5
hz = 1000

fixations = IDT(eye_tracking_data, duration_threshold, dispersion_threshold)

print("Fixations:")
print(len(fixations))
write_tuples_to_txt(fixations,'../IDT_out_watermarked_S_1004_S2_TEX.txt')

protocol = read_tuples_from_txt('../IDT_out_S_1004_S2_TEX.txt')
#protocol = extract_data(filepath)#.apply(lambda row: (row['n'], row['x'], row['y'], row['lab']), axis=1)
print("Saccade accuracy: " + str(measure_saccade_accuracy(protocol, fixations)))