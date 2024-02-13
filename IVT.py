import numpy as np


def calculate_velocity(point1, point2):
    """Calculate velocity between two points."""
    dx = point2[1] - point1[1]
    dy = point2[2] - point1[2]
    dt = point2[0] - point1[0]
    velocity = np.sqrt(dx**2 + dy**2) / dt
    return velocity


def i_vt(protocol, velocity_threshold):
    """Implement I-VT algorithm."""
    fixation_points = []
    current_group = []

    for point in protocol:
        if len(current_group) == 0:
            current_group.append(point)
        elif calculate_velocity(current_group[-1], point) < velocity_threshold:
            current_group.append(point)
        else:
            fixation_points.append(current_group)
            current_group = [point]

    # Append the last group (if any)
    if current_group:
        fixation_points.append(current_group)

    fixation_groups = []
    for group in fixation_points:
        centroid = np.mean(group, axis=0)
        fixation_groups.append(centroid)

    return fixation_groups


# Example usage:
protocol = [(0, 1, 1), (1, 2, 2), (2, 3, 3), (3, 4, 4), (4, 5, 5), (5, 6, 6)]
velocity_threshold = 1.0
fixations = i_vt(protocol, velocity_threshold)
print("Fixation points:", fixations)
