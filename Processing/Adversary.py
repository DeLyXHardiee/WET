import numpy as np

def gaussian_white_noise_attack(data, mean=0, std=0.1):
    attacked_data = []
    for point in data:
        noise_real = np.random.normal(mean, std)
        noise_imag = np.random.normal(mean, std)
        attacked_point = (point[0], point[1] + noise_real, point[2] + noise_imag, point[3])
        attacked_data.append(attacked_point)
    return attacked_data

