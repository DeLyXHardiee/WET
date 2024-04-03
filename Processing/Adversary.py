import numpy as np

def gaussian_white_noise_attack(watermarked_data, mean=0, std_dev=0.1):
    """
    Apply Gaussian white noise attack to watermarked data.

    Parameters:
        watermarked_data (list): List of tuples representing watermarked data.
        mean (float): Mean of the Gaussian distribution (default is 0).
        std_dev (float): Standard deviation of the Gaussian distribution (default is 0.1).

    Returns:
        list: Watermarked data after applying Gaussian white noise attack.
    """
    attacked_data = []
    for entry in watermarked_data:
        t_entry, x_entry, y_entry = entry
        # Adding Gaussian white noise to x and y coordinates
        x_entry += np.random.normal(mean, std_dev)
        y_entry += np.random.normal(mean, std_dev)
        attacked_data.append((t_entry, x_entry, y_entry))
    return attacked_data



