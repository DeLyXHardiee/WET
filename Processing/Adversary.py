import numpy as np
from Embed_watermark import *

#NOISE ATTACKS
def gaussian_white_noise_attack(data, mean=0, std=0.1):
    attacked_data = []
    for point in data:
        noise_x = np.random.normal(mean, std)
        noise_y = np.random.normal(mean, std)
        attacked_point = (point[0], point[1] + noise_x, point[2] + noise_y, point[3])
        attacked_data.append(attacked_point)
    return attacked_data


def DEA_attack(watermarked_data, strength):
    # Generate a new watermark for the DEA attack
    new_watermark = generate_watermark(len(watermarked_data))

    # Embed the new watermark with the same strength as the original watermark
    attacked_data = embed_watermark(watermarked_data, new_watermark, strength)

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
    for i in range(n):
        if random.random() < theta:
            # Replace the current point with its previous point
            attacked_data[i] = data[i - 1]
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

