import unittest
import math
from IDT import find_tresholds, calculate_centroid_distance, calculate_distance

class TestFunctions(unittest.TestCase):

    def test_distance_calculation(self):
        self.assertAlmostEqual(calculate_distance(0, 0, 3, 4), 5.0, places=5)
    
    def test_centroid_distance_calculation(self):
        points = [(0, 0, 0), (1, 3, 4), (2, 6, 8)]
        self.assertAlmostEqual(calculate_centroid_distance(points), 5.0, places=5)

    def test_centroid_distance_empty_input(self):
        # Test for empty input
        points_empty = []
        self.assertEqual(calculate_centroid_distance(points_empty), 0)

    def test_centroid_distance_single_point_input(self):
        # Test for single point input
        points_single = [(0, 0)]
        self.assertEqual(calculate_centroid_distance(points_single), 0)
        
if __name__ == '__main__':
    unittest.main()
