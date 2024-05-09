import numpy
import numpy as np
import CSVUtility as csvu

import numpy as np

# Constants as defined in the paper
SAMPLING_RATE = 1000  # Hz
VELOCITY_THRESHOLD_BASE = 30  # Base velocity threshold for saccade onset in degrees/second
ACCELERATION_THRESHOLD = 30  # Acceleration threshold for saccade onset in degrees/second^2
SACCADE_ONSET_DELAY_MS = 4  # Verification delay for saccade onset in milliseconds
SACCADE_OFFSET_DELAY_MS = 20  # Verification delay for saccade offset in milliseconds

def calculate_velocity(x, y):
    # Compute velocities using central finite difference
    vel_x = (x[2:] - x[:-2]) / 6
    vel_y = (y[2:] - y[:-2]) / 6
    return vel_x, vel_y

def adjust_velocity_threshold(velocities, window_size):
    # Calculate the average velocity over the specified window size to adjust the velocity threshold
    moving_average_velocity = np.convolve(velocities, np.ones(window_size)/window_size, mode='same')
    adjusted_velocity_threshold = VELOCITY_THRESHOLD_BASE + moving_average_velocity
    return adjusted_velocity_threshold

def classify_eye_movements(data):
    timestamps, x_positions, y_positions, _ = zip(*data)
    x_positions = np.array(x_positions)
    y_positions = np.array(y_positions)

    # Calculate velocity
    dt = np.diff(timestamps)
    dx = np.diff(x_positions)
    dy = np.diff(y_positions)
    radial_velocity = 1000*np.sqrt((dx / dt)**2 + (dy / dt)**2)
    acceleration = np.diff(radial_velocity)

    # Adjust the velocity threshold based on the average velocity from the preceding 40 ms
    window_size = 40  # 40 ms window size
    adjusted_velocity_threshold = adjust_velocity_threshold(radial_velocity, window_size)

    # Initialize all labels to fixations (1)
    labels = [1] * len(timestamps)
    previous_event = 1
    current_saccade = []
    current_fixation = []
    result = []
    result.extend(np.array(data[0:2]))
    for i in range(2, len(data)):
        if i < window_size or i >= len(radial_velocity) - window_size:
            result.append(data[i])
            continue
        if (len(result) + len(current_fixation) + len(current_saccade)) != i:
            print(i)
        if radial_velocity[i] > adjusted_velocity_threshold[i-1] or acceleration[i-2] > ACCELERATION_THRESHOLD:
            if 0 < len(current_fixation) < 20:
                current_saccade.extend([(t[0], t[1], t[2], 2) for t in current_fixation])
                current_saccade.append((data[i][0], data[i][1], data[i][2], 2))
                current_fixation = []
            elif len(current_fixation) >= 20:
                current_saccade.append((data[i][0], data[i][1], data[i][2], 2))
                result.extend(current_fixation)
                current_fixation = []
            else:
                current_saccade.append((data[i][0], data[i][1], data[i][2], 2))
        # Add verification delay for saccade onset
        else:
            if 4 > len(current_saccade) > 0:
                current_fixation.extend([(t[0], t[1], t[2], 1) for t in current_saccade])
                current_fixation.append((data[i][0], data[i][1], data[i][2], 1))
                current_saccade = []
            elif len(current_saccade) >= 4:
                current_fixation.append((data[i][0], data[i][1], data[i][2], 1))
                result.extend(current_saccade)
                current_saccade = []
            else:
                current_fixation.append((data[i][0], data[i][1], data[i][2], 1))
    if (len(current_saccade) > 0):
        result.extend(current_saccade)
    if (len(current_fixation) > 0):
        result.extend(current_fixation)


    # Pack the data with new labels into the output list
    return sorted(result, key=lambda x: x[0])


