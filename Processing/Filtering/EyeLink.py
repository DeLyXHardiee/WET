import numpy as np
import sys
import os

parent_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(parent_dir)
import CSVUtility as csvu
import Analyze as an

# Constants as defined in the paper
SAMPLING_RATE = 1000  # Hz
#VELOCITY_THRESHOLD_BASE = 30  # Base velocity threshold for saccade onset in degrees/second
#ACCELERATION_THRESHOLD = 30  # Acceleration threshold for saccade onset in degrees/second^2
SACCADE_ONSET_DELAY_MS = 4  # Verification delay for saccade onset in milliseconds
SACCADE_OFFSET_DELAY_MS = 20  # Verification delay for saccade offset in milliseconds

def calculate_velocity(x, y):
    # Compute velocities using central finite difference
    vel_x = (x[2:] - x[:-2]) / 6
    vel_y = (y[2:] - y[:-2]) / 6
    return vel_x, vel_y

def adjust_velocity_threshold(velocities, window_size, VELOCITY_THRESHOLD_BASE):
    # Calculate the average velocity over the specified window size to adjust the velocity threshold
    moving_average_velocity = np.convolve(velocities, np.ones(window_size)/window_size, mode='same')
    adjusted_velocity_threshold = VELOCITY_THRESHOLD_BASE + moving_average_velocity
    return adjusted_velocity_threshold

def IVT(data, vel):
    VELOCITY_THRESHOLD_BASE = vel
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
    adjusted_velocity_threshold = adjust_velocity_threshold(radial_velocity, window_size, VELOCITY_THRESHOLD_BASE)

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
        adjusted_threshold = adjusted_velocity_threshold[i-1]
        if adjusted_threshold > 60:
            adjusted_threshold = 60
        if radial_velocity[i] > adjusted_threshold:
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
    return result

def find_best_threshold(protocol):
    # Define a range of possible velocity thresholds
    velocity_range = [20, 30, 40, 50, 60, 70, 80]

    best_vel = 0.0
    best_f1_score = 0.0
    final_data = []
    fixations = []

    for vel in velocity_range:
            fixations = IVT(protocol, vel)
            f1_score = an.measure_saccade_accuracy(protocol, fixations)

        # Update best threshold if F1 score is higher
            if f1_score > best_f1_score:
                final_data = fixations
                best_vel = vel
                best_f1_score = f1_score
    print("BEST F1 SCORE: " + str(best_f1_score))
    print("BEST VEL SCORE: " + str(best_vel))
    return best_vel


