import math

def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2-x1) ** 2 + (y2 - y1) ** 2)

def calculate_centroid_distance(points):
    x_values = [point[1] for point in points]
    y_values = [point[2] for point in points]
    mean_x = sum(x_values) / len(x_values)
    mean_y = sum(y_values) / len(y_values)
    return max(calculate_distance(mean_x, mean_y, point[1], point[2]) for point in points)
    
def IDT(gaze_data, dispersion_threshold, duration_threshold, hz):
    fixations = []
    duration = 0
    isFixation = False

    current_fixation = []
    for i in range(0, len(gaze_data)):
        current_fixation.append(gaze_data[i])
        duration += 1/hz
        print(duration)
        if duration >= duration_threshold:
            print(calculate_centroid_distance(current_fixation))
            if calculate_centroid_distance(current_fixation) < dispersion_threshold:
                isFixation = True
            else:
                if isFixation:
                    new_start = current_fixation.pop()
                    isFixation = False
                    duration = 0
                    fixations.append(current_fixation)
                    current_fixation = [new_start]
    return fixations 

eye_tracking_data = [
    (0, 100, 100),   # Timestamp, x-coordinate, y-coordinate
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
hz = 1/100

fixations = IDT(eye_tracking_data, duration_threshold, dispersion_threshold, hz)

print("Fixations:")
for fixation in fixations:
    print(fixation)