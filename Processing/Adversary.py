import numpy as np
from W_Trace_Watermark import *

#NOISE ATTACK
def GWN_attack(data, std=0.1):
    mean=0
    attacked_data = []
    for point in data:
        noise_x = np.random.normal(mean, std)
        noise_y = np.random.normal(mean, std)
        attacked_point = (point[0], point[1] + noise_x, point[2] + noise_y, point[3])
        attacked_data.append(attacked_point)
    return attacked_data

def decrease_time(point):
    return (point[0]-1, point[1], point[2], point[3])

def increase_time(point):
    return (point[0]+1, point[1], point[2], point[3])

#REMOVES LARGE SPIKES FROM THE DATA, POTENTIALLY DESTROYING EMBED_WATERMARK_3
def SPIKE_attack(data, spike_dva=1):
    attacked_data = []
    spike_count = 0
    attacked_data.append(decrease_time(data[1]))
    for i in range(1, len(data)-1):
        if abs(data[i][1] - data[i-1][1]) > spike_dva:
            attacked_data.append(decrease_time(data[i+1]))
            spike_count=spike_count + 1
        elif abs(data[i][2] - data[i-1][2]) > spike_dva:
            attacked_data.append(decrease_time(data[i+1]))
            spike_count=spike_count + 1
        else:
            attacked_data.append(data[i])
    attacked_data.append(data[-1])
    print("SPIKE_COUNT: " + str(spike_count))
    return attacked_data

def remove_spike(point):
    return point

def DEA_attack(watermarked_data, strength):
    # Generate a new watermark for the DEA attack

    # Embed the new watermark with the same strength as the original watermark
    attacked_data,_ = run_watermark(watermarked_data, strength)

    return attacked_data

#POINT REPLACEMENT ATTACKS
def RRP_attack(data, theta):
    """
    Replace Random Points (RRP) attack.

    Parameters:
        data (numpy.ndarray): Trajectory data.
        theta (float): Probability of selecting points for replacement.

    Returns:
        numpy.ndarray: Trajectory data after RRP attack.
    """
    count = 0
    attacked_data = data.copy()
    n = len(data)
    for i in range(n):
        if random.random() < theta:
            count = count + 1
            # Replace the current point with its previous point
            attacked_data[i] = increase_time(data[i - 1])
    print("Removed points: " + str(count))
    return attacked_data


#SIZE MODIFICATION ATTACKS
def LIA_attack(data, num_insertions):
    num_insertions = int(num_insertions)
    """
    Linear Interpolation Attack (LIA) inserts additional points at random positions in the trajectory by linear interpolation.

    Parameters:
        data (list): Trajectory data.
        num_insertions (int): Number of additional points to insert.

    Returns:
        list: Trajectory data after LIA attack.
    """
    attacked_data = data.copy()
    n = len(data)


    for _ in range(num_insertions):
        # Select a random position to insert the new point
        insert_index = random.randint(1, n-1)
        #print(insert_index)
        # Linear interpolation between adjacent points for x and y coordinates separately
        new_x = (data[insert_index - 1][1] + data[insert_index][1]) / 2
        new_y = (data[insert_index - 1][2] + data[insert_index][2]) / 2
        new_point = (data[insert_index][0], new_x, new_y, data[insert_index][3])

        # Insert the new point at the selected position
        attacked_data.insert(insert_index, new_point)
    return correct_timestamps(attacked_data)




def CA_attack(data, num_removals):
    """
    Cropping Attack (CA) removes selected points from the trajectory, decreasing the trajectory size.

    Parameters:
        data (numpy.ndarray): Trajectory data.
        num_removals (int): Number of points to remove.

    Returns:
        numpy.ndarray: Trajectory data after CA attack.
    """
    num_removals = int(num_removals)
    attacked_data = data.copy()
    n = len(data)

    for _ in range(num_removals):
        # Select a random point to remove
        remove_index = random.randint(0, n - 1)

        # Remove the selected point
        attacked_data = np.delete(attacked_data, remove_index, axis=0)
        n -= 1

    return(correct_timestamps(attacked_data))

def correct_timestamps(data):
    corrected_data = []
    for i in range(len(data)):
        n, x, y, lab = data[i]
        if i < len(data) - 1:
            next_n = data[i + 1][0]
            if next_n != n + 1:
                # If the next timestamp is not incremented by one, correct it
                corrected_data.append((n + 1, x, y, lab))
            else:
                corrected_data.append((n, x, y, lab))
        else:
            corrected_data.append((n, x, y, lab))  # Keep the last point as is
    return corrected_data