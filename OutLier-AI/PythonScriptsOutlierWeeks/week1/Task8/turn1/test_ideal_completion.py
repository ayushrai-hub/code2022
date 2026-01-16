import unittest
import numpy as np
from numpy.testing import assert_array_almost_equal, assert_array_equal
import os
import sys

# Import the beamforming code (assuming it's in the same directory)
from new_ideal_solution import (
    simulate_microphone_signals,
    estimate_doa,
    delay_and_sum,
    SAMPLE_RATE,
    NUM_MICS
)

class TestBeamforming(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.duration = 0.1  # 100ms of audio for testing
        self.t = np.linspace(0, self.duration, int(SAMPLE_RATE * self.duration), endpoint=False)
        self.target_signal = np.sin(2 * np.pi * 440 * self.t)
        self.noise_signal = np.random.normal(0, 0.1, len(self.t))
        self.doa_angles = [0, 30, 60, 90]

    def test_simulate_microphone_signals_shape(self):
        """Test if simulate_microphone_signals produces correct output shape"""
        mic_signals = simulate_microphone_signals(self.target_signal, self.noise_signal, self.doa_angles)
        self.assertEqual(mic_signals.shape, (NUM_MICS, len(self.target_signal)))

    def test_simulate_microphone_signals_input_validation(self):
        """Test input validation for simulate_microphone_signals"""
        # Test with mismatched angles length
        wrong_angles = [0, 30, 60]  # Only 3 angles for 4 mics
        with self.assertRaises(ValueError):
            simulate_microphone_signals(self.target_signal, self.noise_signal, wrong_angles)

        # Test with invalid signal type
        with self.assertRaises(TypeError):
            simulate_microphone_signals([1, 2, 3], self.noise_signal, self.doa_angles)

    def test_estimate_doa_range(self):
        """Test if estimated DOA angle is within valid range (-90 to 90 degrees)"""
        mic_signals = simulate_microphone_signals(self.target_signal, self.noise_signal, self.doa_angles)
        doa = estimate_doa(mic_signals)
        self.assertTrue(-90 <= doa <= 90)

    def test_estimate_doa_input_validation(self):
        """Test input validation for estimate_doa"""
        # Test with invalid signal shape
        wrong_shape_signals = np.zeros((3, 100))  # Only 3 mics instead of 4
        with self.assertRaises(ValueError):
            estimate_doa(wrong_shape_signals)

        # Test with empty signals
        with self.assertRaises(ValueError):
            estimate_doa(np.array([]))

    def test_delay_and_sum_shape(self):
        """Test if delay_and_sum produces output of correct shape"""
        mic_signals = simulate_microphone_signals(self.target_signal, self.noise_signal, self.doa_angles)
        beamformed = delay_and_sum(mic_signals, 45)
        self.assertEqual(len(beamformed), len(self.target_signal))

    def test_delay_and_sum_input_validation(self):
        """Test input validation for delay_and_sum"""
        mic_signals = simulate_microphone_signals(self.target_signal, self.noise_signal, self.doa_angles)

        # Test with invalid angle (outside -90 to 90 degrees)
        with self.assertRaises(ValueError):
            delay_and_sum(mic_signals, 100)

        # Test with invalid signal shape
        wrong_shape_signals = np.zeros((3, 100))  # Only 3 mics instead of 4
        with self.assertRaises(ValueError):
            delay_and_sum(wrong_shape_signals, 45)

    def test_end_to_end(self):
        """Test complete signal processing chain"""
        # Generate test signals
        mic_signals = simulate_microphone_signals(self.target_signal, self.noise_signal, self.doa_angles)
        
        # Estimate DOA
        estimated_doa = estimate_doa(mic_signals)
        
        # Apply beamforming
        beamformed = delay_and_sum(mic_signals, estimated_doa)
        
        # Check if output maintains expected properties
        self.assertEqual(len(beamformed), len(self.target_signal))
        self.assertTrue(np.all(np.isfinite(beamformed)))  # Check for NaN or inf values
  

    def test_noise_robustness(self):
        """Test performance with different noise levels"""
        # Test with high SNR
        low_noise = np.random.normal(0, 0.01, len(self.t))
        mic_signals_low_noise = simulate_microphone_signals(self.target_signal, low_noise, self.doa_angles)
        doa_low_noise = estimate_doa(mic_signals_low_noise)

        # Test with low SNR
        high_noise = np.random.normal(0, 1.0, len(self.t))
        mic_signals_high_noise = simulate_microphone_signals(self.target_signal, high_noise, self.doa_angles)
        doa_high_noise = estimate_doa(mic_signals_high_noise)

        # Results should be different but both within valid range
        self.assertTrue(-90 <= doa_low_noise <= 90)
        self.assertTrue(-90 <= doa_high_noise <= 90)

    def test_numerical_stability(self):
        """Test numerical stability with extreme values"""
        # Test with very small signals
        tiny_signal = self.target_signal * 1e-10
        tiny_noise = self.noise_signal * 1e-10
        mic_signals_tiny = simulate_microphone_signals(tiny_signal, tiny_noise, self.doa_angles)
        doa_tiny = estimate_doa(mic_signals_tiny)
        self.assertTrue(-90 <= doa_tiny <= 90)

        # Test with very large signals
        large_signal = self.target_signal * 1e10
        large_noise = self.noise_signal * 1e10
        mic_signals_large = simulate_microphone_signals(large_signal, large_noise, self.doa_angles)
        doa_large = estimate_doa(mic_signals_large)
        self.assertTrue(-90 <= doa_large <= 90)

if __name__ == '__main__':
    unittest.main(verbosity=2)