import numpy as np

def gaussian_white_noise_attack(data, mean=0, std=0.1):
    attacked_data = []
    for point in data:
        noise_x = np.random.normal(mean, std)
        noise_y = np.random.normal(mean, std)
        attacked_point = (point[0], point[1] + noise_x, point[2] + noise_y, point[3])
        attacked_data.append(attacked_point)
    return attacked_data

