import unittest
from IVT import check_for_nan, calculate_label_accuracy, calculate_velocity, IVT, find_best_threshold

class TestFunctions(unittest.TestCase):

    def test_calculate_label_accuracy(self):
        true_labels = [1, 1, 2, 2, 1]
        predicted_labels = [1, 1, 1, 2, 1]
        self.assertAlmostEqual(calculate_label_accuracy(true_labels, predicted_labels), 0.8, delta=0.01)

    def test_calculate_velocity(self):
        point1 = (0, 0, 0)
        point2 = (1, 3, 4)
        self.assertAlmostEqual(calculate_velocity(point1, point2), 5.0, delta=0.01)

if __name__ == '__main__':
    unittest.main()
