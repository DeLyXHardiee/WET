import unittest
import numpy as np
from Embed_watermark import *

class TestWatermarkFunctions(unittest.TestCase):

    def test_get_complex_transformation(self):
        # Test data with known x and y values
        test_data = [(0, 1, 2), (1, 3, 4), (2, 5, 6)]
        # Call the function to get complex transformation
        result = get_complex_transformation(test_data)
        # Expected complex transformation
        expected_result = [1 + 2j, 3 + 4j, 5 + 6j]
        # Check if the result matches the expected complex transformation
        self.assertEqual(result, expected_result)

    def test_generate_watermark(self):
        # Generate a watermark of known length
        watermark_length = 10
        watermark = generate_watermark(watermark_length)
        # Check if the length of the watermark matches the expected length
        self.assertEqual(len(watermark), watermark_length)
        # Check if the watermark contains only integers between -1, 0, and 1
        self.assertTrue(all(x in [-1, 0, 1] for x in watermark))

    def test_embed_watermark(self):
        # Test input data
        fft = np.array([1 + 2j, 3 + 4j, 5 + 6j])
        watermark = np.array([0, 1, -1])
        strength = 0.5
        # Call the function to embed watermark
        result = embed_watermark(fft, watermark, strength)
        # Expected result after embedding watermark
        expected_result = np.array([1.0 + 2.0j, 3.5 + 4.0j, 4.5 + 6.0j])
        # Check if the result matches the expected result
        np.testing.assert_array_equal(result, expected_result)

    def test_extract_watermark(self):
        # Test input data
        original_fft = np.array([1 + 2j, 2.5 + 4j, 5 + 6j])
        watermark_fft = np.array([0.5 + 2j, 3 + 4j, 5 + 6j])
        strength = 0.5
        # Call the function to extract watermark
        result = extract_watermark(original_fft, watermark_fft, strength)
        # Expected result after extracting watermark
        expected_result = np.array([-1, 1, 0])
        # Check if the result matches the expected result
        np.testing.assert_array_equal(result, expected_result)

    def test_revert_from_complex_numbers(self):
        # Test input data
        ifft = np.array([1 + 2j, 3 + 4j, 5 + 6j])
        data = [(1, 0, 0, 1), (2, 0, 0, 2), (3, 0, 0, 3)]
        # Call the function to revert from complex numbers
        result = revert_from_complex_numbers(ifft, data)
        # Expected result after reverting from complex numbers
        expected_result = [(1, 1.0, 2.0, 1), (2, 3.0, 4.0, 2), (3, 5.0, 6.0, 3)]
        # Check if the result matches the expected result
        self.assertEqual(result, expected_result)

    def test_watermark_extraction(self):
        # Generate test data
        data = [(1, 1.54245245, 2.245245245, 1), (2, 3.24524524, 4.24524524, 2), (3, 5.245245245, 6.245245245, 3)]
        strength = 1000  # Some arbitrary strength value
        # Run watermark embedding and extraction
        watermarked_data, original_watermark = run_watermark(data, strength)
        extracted_watermark = unrun_watermark(watermarked_data, data, strength)
        # Check if extracted watermark matches original watermark
        self.assertTrue(np.array_equal(original_watermark, np.round(extracted_watermark)))

    def test_watermark_difference(self):
        # Generate test data
        data = [(1, 1.54245245, 2.245245245, 1), (2, 3.24524524, 4.24524524, 2), (3, 5.245245245, 6.245245245, 3)]
        strength = 1000  # Some arbitrary strength value
        # Run watermark embedding
        watermarked_data, _ = run_watermark(data, strength)
        # Check if watermarked data is different from original data
        self.assertNotEqual(data, watermarked_data)

    def test_get_FFT(self):
        # Generate a complex transformation array
        complex_transformation = [1 + 2j, 3 + 4j, 5 + 6j]
        # Calculate the FFT
        fft_result = get_FFT(complex_transformation)
        # Check if the length of the result matches the input array
        self.assertEqual(len(fft_result), len(complex_transformation))

    # You can add similar test methods for other functions

    # Make sure to clean up any temporary files or resources after testing

if __name__ == '__main__':
    unittest.main()