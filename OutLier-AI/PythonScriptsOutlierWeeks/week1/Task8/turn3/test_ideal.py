import unittest
import numpy as np
from typing import List
import logging
from refactor import (
    BeamformingSystem, SystemParameters, SignalValidator, SignalProcessor,
    BeamformingError, SignalValidationError, DOAEstimationError
)

class TestBeamformingSystem(unittest.TestCase):
    """Test suite for the Beamforming System implementation."""

    def setUp(self):
        """Initialize test environment before each test."""
        self.params = SystemParameters()
        self.system = BeamformingSystem(self.params)
        self.validator = SignalValidator(self.params)
        self.processor = SignalProcessor(self.params)
        
        # Create common test signals
        self.duration = 0.1  # 100ms test duration
        self.t = np.linspace(0, self.duration, 
                           int(self.duration * self.params.SAMPLE_RATE), 
                           endpoint=False)
        self.test_signal = np.sin(2 * np.pi * 440 * self.t)  # 440 Hz test tone
        self.noise = np.random.normal(0, 0.1, len(self.t))

    def test_signal_validation(self):
        """Test signal validation functionality."""
        # Test valid signal
        valid_signals = np.random.rand(self.params.NUM_MICS, 1000)
        self.validator.validate_signals(valid_signals)  # Should not raise

        # Test invalid signal shapes
        with self.assertRaises(SignalValidationError):
            self.validator.validate_signals(np.random.rand(3, 1000))  # Wrong number of mics

        with self.assertRaises(SignalValidationError):
            self.validator.validate_signals(np.random.rand(1000))  # 1D array

        # Test invalid values
        invalid_signals = np.full((self.params.NUM_MICS, 1000), np.inf)
        with self.assertRaises(SignalValidationError):
            self.validator.validate_signals(invalid_signals)

    def test_angle_validation(self):
        """Test angle validation functionality."""
        # Test valid angles
        valid_angles = [0, 45, -45, 90, -90]
        for angle in valid_angles:
            self.validator.validate_angle(angle)  # Should not raise

        # Test invalid angles
        invalid_angles = [91, -91, 180, -180]
        for angle in invalid_angles:
            with self.assertRaises(SignalValidationError):
                self.validator.validate_angle(angle)

        # Test invalid types
        with self.assertRaises(SignalValidationError):
            self.validator.validate_angle("45")

    def test_signal_normalization(self):
        """Test signal normalization functionality."""
        # Test normal signal
        test_signal = np.sin(2 * np.pi * 440 * self.t)
        normalized = self.processor.normalize_to_int24(test_signal)
        self.assertTrue(np.all(np.abs(normalized) <= self.params.MAX_INT24))

        # Test zero signal
        zero_signal = np.zeros_like(test_signal)
        normalized_zero = self.processor.normalize_to_int24(zero_signal)
        np.testing.assert_array_equal(normalized_zero, zero_signal)

        # Test invalid input
        with self.assertRaises(SignalValidationError):
            self.processor.normalize_to_int24([1, 2, 3])  # List instead of numpy array

    def test_microphone_simulation(self):
        """Test microphone array signal simulation."""
        # Test valid simulation
        target_signal = self.processor.normalize_to_int24(self.test_signal)
        noise_signal = self.processor.normalize_to_int24(self.noise)
        angles = [0, 30, 60, 90]

        mic_signals = self.system.simulate_microphone_signals(
            target_signal, noise_signal, angles)
        
        self.assertEqual(mic_signals.shape, 
                        (self.params.NUM_MICS, len(target_signal)))
        self.assertTrue(np.all(np.abs(mic_signals) <= self.params.MAX_INT24))

        # Test unequal signal lengths
        with self.assertRaises(BeamformingError):
            self.system.simulate_microphone_signals(
                target_signal, noise_signal[:100], angles)

        # Test invalid angles
        with self.assertRaises(BeamformingError):
            self.system.simulate_microphone_signals(
                target_signal, noise_signal, [0, 30, 60, 95])

    def test_doa_estimation(self):
        """Test direction of arrival estimation."""
        # Generate test signals with known DOA
        target_signal = self.processor.normalize_to_int24(self.test_signal)
        noise_signal = self.processor.normalize_to_int24(self.noise)
        test_angle = 45
        angles = [test_angle] * self.params.NUM_MICS

        mic_signals = self.system.simulate_microphone_signals(
            target_signal, noise_signal, angles)

        # Test invalid inputs
        with self.assertRaises(DOAEstimationError):
            self.system.estimate_doa(np.random.rand(1, 1000))  # Too few mics

    def test_delay_and_sum(self):
        """Test delay-and-sum beamforming."""
        # Test valid beamforming
        target_signal = self.processor.normalize_to_int24(self.test_signal)
        noise_signal = self.processor.normalize_to_int24(self.noise)
        test_angle = 30
        angles = [test_angle] * self.params.NUM_MICS

        mic_signals = self.system.simulate_microphone_signals(
            target_signal, noise_signal, angles)
        
        beamformed = self.system.delay_and_sum(mic_signals, test_angle)
        self.assertEqual(len(beamformed), len(target_signal))
        self.assertTrue(np.all(np.abs(beamformed) <= self.params.MAX_INT24))

        # Test invalid angle
        with self.assertRaises(BeamformingError):
            self.system.delay_and_sum(mic_signals, 95)

        # Test invalid signals
        with self.assertRaises(BeamformingError):
            self.system.delay_and_sum(np.random.rand(2, 1000), test_angle)

    def test_end_to_end(self):
        """Test complete signal processing chain."""
        # Generate test signals
        target_signal = self.processor.normalize_to_int24(self.test_signal)
        noise_signal = self.processor.normalize_to_int24(self.noise)
        true_angle = 60
        angles = [true_angle] * self.params.NUM_MICS

        # Simulate microphone array
        mic_signals = self.system.simulate_microphone_signals(
            target_signal, noise_signal, angles)

        # Estimate DOA
        estimated_doa = self.system.estimate_doa(mic_signals)

        # Apply beamforming
        beamformed = self.system.delay_and_sum(mic_signals, estimated_doa)
        self.assertEqual(len(beamformed), len(target_signal))
        self.assertTrue(np.all(np.abs(beamformed) <= self.params.MAX_INT24))

def run_tests():
    """Run test suite with detailed output."""
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBeamformingSystem)
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Log results
    if result.wasSuccessful():
        logger.info("All tests passed successfully!")
    else:
        logger.error("Some tests failed:")
        for failure in result.failures:
            logger.error(f"Test: {failure[0]}")
            logger.error(f"Error: {failure[1]}")
        for error in result.errors:
            logger.error(f"Test: {error[0]}")
            logger.error(f"Error: {error[1]}")

if __name__ == "__main__":
    run_tests()