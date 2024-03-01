import numpy as np
import csv
from ExtractDataFromCSV import extract_data

def calculate_velocity_threshold(screen_resolution, viewing_distance, sampling_rate, distance_threshold_pixels):
    """Calculate velocity threshold based on screen resolution, viewing distance, and sampling rate."""
    # Calculate angular size of the screen
    screen_width_pixels, screen_height_pixels = screen_resolution
    screen_width_mm = 2 * np.arctan((screen_width_pixels / 2) / viewing_distance) * (180 / np.pi)
    screen_height_mm = 2 * np.arctan((screen_height_pixels / 2) / viewing_distance) * (180 / np.pi)

    # Convert pixel displacement to angular displacement
    pixel_size_mm = screen_width_mm / screen_width_pixels
    max_displacement_mm = distance_threshold_pixels * pixel_size_mm

    # Calculate angular threshold
    angular_threshold = np.arctan(max_displacement_mm / viewing_distance)

    # Calculate velocity threshold
    return angular_threshold * sampling_rate


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

    """fixation_groups = []
    for group in fixation_points:
        centroid = np.mean(group, axis=0)
        fixation_groups.append(centroid)
        """

    return fixation_points

def write_tuples_to_csv(tuples, filename):
    """Write tuples to a CSV file with row numbers."""
    with open(filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        for i, tpl in enumerate(tuples, start=1):
            row = [i] + list(tpl)  # Add row number to the beginning of the tuple
            csv_writer.writerow(row)


screen_resolution = (1680, 1050)  # Screen resolution in pixels (width x height)
viewing_distance = 550  # Viewing distance in millimeters
sampling_rate = 1000  # Sampling rate in Hz
distance_threshold_pixels = 10  # Distance threshold in pixels
velocity_threshold = calculate_velocity_threshold(screen_resolution, viewing_distance, sampling_rate, distance_threshold_pixels)


# Example usage:
protocol = extract_data("S_9016_S1_RAN.csv")
fixations = i_vt(protocol, velocity_threshold)
write_tuples_to_csv(fixations)
