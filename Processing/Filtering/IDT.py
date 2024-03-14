import math

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
    return fixations 

""" screen_display = (474, 297)  # Screen display (width x height)
distance_from_screen = 550

# Long fixations and eye drifting / smooth pursuits are a major issue. They often get separated into different fixations.
duration_threshold = 30
dispersion_threshold = 0.5
hz = 1000
 """