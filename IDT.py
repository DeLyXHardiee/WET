import math
from ExtractDataFromCSV import extract_data

subject = (0, 0, 55)

def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def calculate_angle_between_points(point1, point3):
    # Calculate vectors AB and BC
    vector_AB = [subject[i] - point1[i] for i in range(3)]
    vector_BC = [point3[i] - subject[i] for i in range(3)]

    # Calculate dot product of AB and BC
    dot_product = sum(vector_AB[i] * vector_BC[i] for i in range(3))

    # Calculate magnitudes of AB and BC
    magnitude_AB = math.sqrt(sum(coord**2 for coord in vector_AB))
    magnitude_BC = math.sqrt(sum(coord**2 for coord in vector_BC))

    # Calculate cosine of the angle
    cosine_theta = dot_product / (magnitude_AB * magnitude_BC)

    # Calculate the angle in radians
    if cosine_theta > 1:
        cosine_theta = 1
    elif cosine_theta < -1:
        cosine_theta = -1
    angle_radians = math.acos(cosine_theta)

    return angle_radians*(180/math.pi)

def calculate_centroid_distance(points):
    if len(points) < 2:
        return 0
    x_values = [point[1] for point in points]
    y_values = [point[2] for point in points]
    mean_x = sum(x_values) / len(x_values)
    mean_y = sum(y_values) / len(y_values)
    return max(calculate_distance(mean_x, mean_y, point[1], point[2]) for point in points)
    return max(calculate_angle_between_points((mean_x, mean_y,0), (point[1], point[2],0)) for point in points)
    
def get_bounds(points):
    max_x = 0
    max_y = 0
    min_x = 0
    min_y = 0
    for point in points:
        if point[1] > max_x:
            max_x = point[1]
        if point[1] < min_x:
            min_x = point[1]
        if point[2] > max_y:
            max_y = point[2]
        if point[2] < min_y:
            min_y = point[2]
    return (max_x,max_y),(min_x,min_y)

def IDT(eye_tracking_data, duration_threshold, dispersion_threshold):
    fixations = []
    duration = 0
    isFixation = False
    num_fixations = 0
    current_fixation = []
    tuple_values = eye_tracking_data.apply(lambda row: (row['n'], row['x'], row['y'], row['lab']), axis=1)
    for i in range (0,int(len(tuple_values))):
        #print(i)
        if (tuple_values[i][3] == -1) | (tuple_values[i][3] == 0):
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
                    fixations.append(current_fixation)
            else:
                if isFixation:
                    new_start = current_fixation.pop()
                    isFixation = False
                    fixations.append(current_fixation)
                    current_fixation = [new_start]
                    duration = 0
                else:
                    current_fixation.reverse()
                    while calculate_centroid_distance(current_fixation) > dispersion_threshold:
                        current_fixation.pop()
                        duration -= 1
                    current_fixation.reverse()
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

point3 = (-14.817994,6.432674, 0)
point1 = (-17.23406,8.249892, 0)
point2 = (0, 0, 55)
#angle = 180-calculate_angle_between_points(point1, point2, point3)
#print("angle: " + str(angle))

eye_tracking_data = extract_data('S_1002_S1_RAN.csv')

screen_display = (474, 297)  # Screen display (width x height)
distance_from_screen = 550

duration_threshold = 150
dispersion_threshold = 1
hz = 1000

fixations = IDT(eye_tracking_data, duration_threshold, dispersion_threshold)

print("Fixations:")
print(len(fixations))
for fixation in fixations:
    print(len(fixation))