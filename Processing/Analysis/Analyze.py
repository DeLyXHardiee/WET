def measure_saccade_accuracy(true_data, predicted_data):
    if len(true_data) != len(predicted_data):
        raise ValueError("Length of true data and predicted data must be the same")

    # Extract saccade labels from true and predicted data
    true_saccades = [point for point in true_data if point[3] == 2]
    predicted_saccades = [point for point in predicted_data if point[3] == 2]

    # Calculate intersection of true and predicted saccades
    true_positives = 0
    for point in predicted_saccades:
        for true_point in true_saccades:
            if (point[0] == true_point[0]) & (point[3] == true_point[3]):
                true_positives += 1
                continue
    
    # Calculate precision and recall
    precision = true_positives / len(predicted_saccades) if predicted_saccades else 0
    recall = true_positives / len(true_saccades) if true_saccades else 0

    # Calculate accuracy as the harmonic mean of precision and recall (F1 score)
    accuracy = 2 * (precision * recall) / (precision + recall) if precision + recall > 0 else 0

    return accuracy