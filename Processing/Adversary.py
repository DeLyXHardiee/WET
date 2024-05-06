import numpy as np
from Embed_watermark import *
import Embed_watermark as ew

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

def add_small_noise(point):
    noise_x = np.random.normal(0, 0.0001)
    noise_y = np.random.normal(0, 0.0001)
    return (point[0]-1, point[1] + noise_x, point[2] + noise_y, point[3])

#REMOVES LARGE SPIKES FROM THE DATA, POTENTIALLY DESTROYING EMBED_WATERMARK_3
def SPIKE_attack(data, spike_dva=1):
    attacked_data = []
    spike_count = 0
    attacked_data.append(add_small_noise(data[1]))
    for i in range(1, len(data)-1):
        if abs(data[i][1] - data[i-1][1]) > spike_dva:
            attacked_data.append(add_small_noise(data[i+1]))
            spike_count=spike_count + 1
        elif abs(data[i][2] - data[i-1][2]) > spike_dva:
            attacked_data.append(add_small_noise(data[i+1]))
            spike_count=spike_count + 1
        else:
            attacked_data.append(data[i])
    attacked_data.append(data[-1])
    print("SPIKE_COUNT: " + str(spike_count))
    return attacked_data

def remove_spike(point):
    return point

def DEA_attack(watermarked_data, strength):
    attacked_data,watermark = ew.run_watermark(watermarked_data, strength)
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
    attacked_data = data.copy()
    n = len(data)
    counter = 0
    for i in range(1,n):
        randomnr = random.random()
        if  randomnr < theta:
            counter += 1
            # Replace the current point with its previous point
            newtuple = (data[i][0],data[i-1][1],data[i-1][2],data[i][3])
            attacked_data[i] = newtuple
    print(counter)
    return attacked_data


#SIZE MODIFICATION ATTACKS
def LIA_attack(data, num_insertions):
    """
    Linear Interpolation Attack (LIA) inserts additional points at random positions in the trajectory by linear interpolation.

    Parameters:
        data (numpy.ndarray): Trajectory data.
        num_insertions (int): Number of additional points to insert.

    Returns:
        numpy.ndarray: Trajectory data after LIA attack.
    """
    attacked_data = data.copy()
    n = len(data)

    for _ in range(num_insertions):
        # Select a random position to insert the new point
        insert_index = random.randint(0, n - 1)

        # Linear interpolation between adjacent points for x and y coordinates separately
        new_x = (data[insert_index - 1][1] + data[insert_index][1]) / 2
        new_y = (data[insert_index - 1][2] + data[insert_index][2]) / 2
        new_point = (data[insert_index][0], new_x, new_y, data[insert_index][3])

        # Insert the new point at the selected position
        attacked_data = np.insert(attacked_data, insert_index, new_point, axis=0)
        n += 1

    return attacked_data


def CA_attack(data, num_removals):
    """
    Cropping Attack (CA) removes selected points from the trajectory, decreasing the trajectory size.

    Parameters:
        data (numpy.ndarray): Trajectory data.
        num_removals (int): Number of points to remove.

    Returns:
        numpy.ndarray: Trajectory data after CA attack.
    """
    attacked_data = data.copy()
    n = len(data)

    for _ in range(num_removals):
        # Select a random point to remove
        remove_index = random.randint(0, n - 1)

        # Remove the selected point
        attacked_data = np.delete(attacked_data, remove_index, axis=0)
        n -= 1

    return attacked_data

