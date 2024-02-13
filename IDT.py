import math

def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def calculate_centroid_distance(points):
    x_values = [point[1] for point in points]
    y_values = [point[2] for point in points]
    mean_x = sum(x_values) / len(x_values)
    mean_y = sum(y_values) / len(y_values)
    return max(calculate_distance(mean_x, mean_y, point[1], point[2]) for point in points)


def IDT(gaze_data, dispersion_threshold, duration_threshold):
    fixations = []

    if len(gaze_data) == 0:
        return fixations

    fixation_id = 1
    isFixation = False

    current_fixation = [gaze_data[0] + (fixation_id,)]
    for i in range(1, len(gaze_data)):
        current_point = gaze_data[i] + (fixation_id,)
        duration = current_point[0] - current_fixation[0][0]
        current_fixation.append(current_point)
        distance = calculate_distance(current_point[1], current_point[2],
                                      current_fixation[0][1], current_fixation[0][2])

        if distance >= dispersion_threshold:
            if isFixation:
                current_fixation.pop()
                fixations.append(current_fixation)
                fixation_id += 1
                current_fixation = [current_point]
            else:
                current_fixation = [current_point]
            isFixation = False

        if duration >= duration_threshold:
            isFixation = True

    return fixations


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
    (2000, 2500, -1500)
]

duration_threshold = 150
dispersion_threshold = 30

fixations = IDT(eye_tracking_data, duration_threshold, dispersion_threshold)

print("Fixations:")
for fixation in fixations:
    print(fixation)
