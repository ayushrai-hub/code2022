"""
Acoustic Beamforming System Implementation
Enhanced version with proper class structure, type hints, and comprehensive error handling.

Author: Claude
Date: December 2024

This module implements an acoustic beamforming system with the following key features:
- Signal validation and preprocessing
- Direction of Arrival (DOA) estimation
- Delay-and-sum beamforming
- Embedded system optimization
"""

import numpy as np
from typing import List, Optional
from dataclasses import dataclass
from enum import Enum
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BeamformingError(Exception):
    """Base exception class for beamforming-related errors."""
    pass

class SignalValidationError(BeamformingError):
    """Exception raised for signal validation errors."""
    pass

class DOAEstimationError(BeamformingError):
    """Exception raised for DOA estimation errors."""
    pass

@dataclass(frozen=True)
class SystemParameters:
    """Immutable system parameters configuration."""
    SAMPLE_RATE: int = 16000      # Sampling rate in Hz
    SOUND_SPEED: float = 343.0    # Sound speed in m/s
    MIC_DISTANCE: float = 0.05    # Distance between microphones in meters
    NUM_MICS: int = 4            # Total microphones in the array
    FRAME_SIZE: int = 512        # Processing frame size for embedded systems
    MAX_INT24: int = 8388607     # Maximum value for 24-bit integer
    MIN_ANGLE: float = -90.0     # Minimum valid angle in degrees
    MAX_ANGLE: float = 90.0      # Maximum valid angle in degrees

class SignalType(Enum):
    """Enumeration for different types of signals."""
    TARGET = "target"
    NOISE = "noise"
    COMBINED = "combined"

class SignalProcessor:
    """Handles signal processing operations with input validation."""
    
    def __init__(self, params: SystemParameters = SystemParameters()):
        """Initialize with system parameters."""
        self.params = params
        
    def normalize_to_int24(self, signal: np.ndarray) -> np.ndarray:
        """
        Normalize floating point signal to 24-bit integer range.
        
        Args:
            signal: Input signal array
            
        Returns:
            Normalized signal within int24 range
            
        Raises:
            SignalValidationError: If signal is invalid
        """
        if not isinstance(signal, np.ndarray):
            raise SignalValidationError("Signal must be a numpy array")
            
        max_val = np.max(np.abs(signal))
        if max_val == 0:
            return np.zeros_like(signal, dtype=np.int32)
            
        normalized = (signal / max_val) * self.params.MAX_INT24
        return np.clip(normalized, -self.params.MAX_INT24, 
                      self.params.MAX_INT24).astype(np.int32)

class SignalValidator:
    """Validates input signals and parameters."""
    
    def __init__(self, params: SystemParameters = SystemParameters()):
        """Initialize with system parameters."""
        self.params = params
    
    def validate_signals(self, signals: np.ndarray, required_mics: Optional[int] = None) -> None:
        """
        Validate microphone array signals.
        
        Args:
            signals: Input signals array
            required_mics: Number of required microphones (defaults to system setting)
            
        Raises:
            SignalValidationError: If validation fails
        """
        if required_mics is None:
            required_mics = self.params.NUM_MICS
            
        if not isinstance(signals, np.ndarray):
            raise SignalValidationError("Signals must be a numpy array")
            
        if len(signals.shape) != 2:
            raise SignalValidationError("Signals must be a 2D array")
            
        if signals.shape[0] != required_mics:
            raise SignalValidationError(
                f"Expected {required_mics} microphones, got {signals.shape[0]}")
            
        if signals.size == 0:
            raise SignalValidationError("Signals cannot be empty")
            
        if not np.all(np.isfinite(signals)):
            raise SignalValidationError("Signals contain invalid values (inf or nan)")
    
    def validate_angle(self, angle: float) -> None:
        """
        Validate DOA angle.
        
        Args:
            angle: Direction of arrival angle in degrees
            
        Raises:
            SignalValidationError: If angle is invalid
        """
        if not isinstance(angle, (int, float, np.number)):
            raise SignalValidationError("Angle must be a number")
            
        if not self.params.MIN_ANGLE <= angle <= self.params.MAX_ANGLE:
            raise SignalValidationError(
                f"Angle must be between {self.params.MIN_ANGLE} and {self.params.MAX_ANGLE} degrees")

class BeamformingSystem:
    """Main beamforming system implementation."""
    
    def __init__(self, params: SystemParameters = SystemParameters()):
        """Initialize beamforming system components."""
        self.params = params
        self.validator = SignalValidator(params)
        self.processor = SignalProcessor(params)
        logger.info("Beamforming system initialized with %d microphones", params.NUM_MICS)
        
    def simulate_microphone_signals(self, 
                                  target_signal: np.ndarray,
                                  noise_signal: np.ndarray,
                                  doa_angles: List[float]) -> np.ndarray:
        """
        Simulate microphone array signals with target and noise components.
        
        Args:
            target_signal: Target audio signal
            noise_signal: Noise signal
            doa_angles: Direction of arrival angles for each microphone
            
        Returns:
            Array of simulated microphone signals
            
        Raises:
            BeamformingError: If simulation fails
        """
        try:
            # Validate inputs
            if len(target_signal) != len(noise_signal):
                raise SignalValidationError("Target and noise signals must have same length")
                
            if len(doa_angles) != self.params.NUM_MICS:
                raise SignalValidationError(
                    f"Number of DOA angles must match number of microphones ({self.params.NUM_MICS})")
                    
            for angle in doa_angles:
                self.validator.validate_angle(angle)
                
            # Initialize output array
            mic_signals = np.zeros((self.params.NUM_MICS, len(target_signal)), dtype=np.int32)
            
            # Process each microphone
            for i in range(self.params.NUM_MICS):
                # Calculate delay
                delay = (self.params.MIC_DISTANCE * i * 
                        np.cos(np.deg2rad(doa_angles[i]))) / self.params.SOUND_SPEED
                delay_samples = int(np.clip(delay * self.params.SAMPLE_RATE, 
                                         0, len(target_signal)-1))
                
                # Process in frames
                for frame_start in range(0, len(target_signal), self.params.FRAME_SIZE):
                    frame_end = min(frame_start + self.params.FRAME_SIZE, len(target_signal))
                    
                    # Combine delayed target with noise
                    frame_signal = np.roll(target_signal[frame_start:frame_end], delay_samples)
                    frame_noise = noise_signal[frame_start:frame_end]
                    combined = self.processor.normalize_to_int24(frame_signal + frame_noise)
                    
                    mic_signals[i, frame_start:frame_end] = combined
                    
            return mic_signals
            
        except Exception as e:
            raise BeamformingError(f"Failed to simulate microphone signals: {str(e)}")
    
    def estimate_doa(self, signals: np.ndarray) -> float:
        """
        Estimate direction of arrival using improved phase correlation.
        
        Args:
            signals: Array of microphone signals
            
        Returns:
            Estimated DOA angle in degrees
            
        Raises:
            DOAEstimationError: If estimation fails
        """
        try:
            self.validator.validate_signals(signals)
            
            if signals.shape[0] < 2:
                raise DOAEstimationError("At least two microphone signals required")
            
            # Process signals in frames for better estimation
            frame_size = self.params.FRAME_SIZE
            num_frames = signals.shape[1] // frame_size
            angle_estimates = []
            
            for frame in range(num_frames):
                start_idx = frame * frame_size
                end_idx = start_idx + frame_size
                
                # Extract reference signals for current frame
                sig1 = signals[0, start_idx:end_idx].astype(np.float32) / self.params.MAX_INT24
                sig2 = signals[1, start_idx:end_idx].astype(np.float32) / self.params.MAX_INT24
                
                # Apply Hanning window to reduce edge effects
                window = np.hanning(len(sig1))
                sig1 *= window
                sig2 *= window
                
                # Compute cross-correlation in frequency domain with improved normalization
                SIG1 = np.fft.rfft(sig1)
                SIG2 = np.fft.rfft(sig2)
                X12 = SIG1 * np.conj(SIG2)
                
                # Normalize using smoothed power spectrum
                smooth_factor = 0.1
                power_spectrum = np.abs(X12)
                smoothed_power = np.maximum(power_spectrum, 
                                         smooth_factor * np.mean(power_spectrum))
                X12_norm = X12 / smoothed_power
                
                # Get time delay from phase slope
                freqs = np.fft.rfftfreq(len(sig1), d=1/self.params.SAMPLE_RATE)
                valid_freq_mask = (freqs > 50) & (freqs < 4000)  # Focus on speech frequencies
                phases = np.angle(X12_norm[valid_freq_mask])
                freqs = freqs[valid_freq_mask]
                
                # Unwrap phases and fit line to get delay
                unwrapped_phases = np.unwrap(phases)
                coeffs = np.polyfit(freqs, unwrapped_phases, deg=1)
                time_delay = -coeffs[0] / (2 * np.pi)
                
                # Convert to angle and validate
                max_possible_delay = self.params.MIC_DISTANCE / self.params.SOUND_SPEED
                if abs(time_delay) > max_possible_delay:
                    time_delay = np.clip(time_delay, -max_possible_delay, max_possible_delay)
                
                # Calculate angle using arcsin
                angle = np.arcsin(time_delay * self.params.SOUND_SPEED / 
                                self.params.MIC_DISTANCE) * (180 / np.pi)
                angle_estimates.append(angle)
            
            # Use median for robust final estimate
            final_angle = float(np.median(angle_estimates))
            return np.clip(final_angle, self.params.MIN_ANGLE, self.params.MAX_ANGLE)
            
        except Exception as e:
            raise DOAEstimationError(f"Failed to estimate DOA: {str(e)}")
    
    def delay_and_sum(self, signals: np.ndarray, doa_angle: float) -> np.ndarray:
        """
        Implement delay-and-sum beamforming.
        
        Args:
            signals: Microphone array signals
            doa_angle: Direction of arrival angle
            
        Returns:
            Beamformed output signal
            
        Raises:
            BeamformingError: If beamforming fails
        """
        try:
            self.validator.validate_signals(signals)
            self.validator.validate_angle(doa_angle)
            
            num_samples = signals.shape[1]
            beamformed_signal = np.zeros(num_samples, dtype=np.int32)
            
            # Process in frames
            for frame_start in range(0, num_samples, self.params.FRAME_SIZE):
                frame_end = min(frame_start + self.params.FRAME_SIZE, num_samples)
                frame_sum = np.zeros(frame_end - frame_start, dtype=np.int32)
                
                # Sum delayed signals from each microphone
                for mic_idx in range(self.params.NUM_MICS):
                    delay = (self.params.MIC_DISTANCE * mic_idx * 
                            np.cos(np.deg2rad(doa_angle))) / self.params.SOUND_SPEED
                    delay_samples = int(np.clip(delay * self.params.SAMPLE_RATE, 
                                             0, num_samples-1))
                    
                    frame = signals[mic_idx, frame_start:frame_end]
                    delayed_frame = np.roll(frame, delay_samples)
                    frame_sum += delayed_frame
                
                # Average and clip to int24 range
                frame_sum = (frame_sum + (self.params.NUM_MICS // 2)) // self.params.NUM_MICS
                beamformed_signal[frame_start:frame_end] = np.clip(
                    frame_sum, -self.params.MAX_INT24, self.params.MAX_INT24)
            
            return beamformed_signal
            
        except Exception as e:
            raise BeamformingError(f"Failed to perform beamforming: {str(e)}")

def main():
    """Example usage of the beamforming system."""
    try:
        # Initialize system
        params = SystemParameters()
        system = BeamformingSystem(params)
        
        # Generate test signals
        t = np.linspace(0, 1, params.SAMPLE_RATE, endpoint=False)
        target_signal = np.sin(2 * np.pi * 440 * t)  # 440 Hz test tone
        noise_signal = np.random.normal(0, 0.1, len(t))
        
        # Normalize signals
        target_signal = system.processor.normalize_to_int24(target_signal)
        noise_signal = system.processor.normalize_to_int24(noise_signal)
        
        # Simulate microphone array
        doa_angles = [0, 30, 60, 90]
        mic_signals = system.simulate_microphone_signals(target_signal, noise_signal, doa_angles)
        
        # Estimate DOA and apply beamforming
        estimated_doa = system.estimate_doa(mic_signals)
        logger.info("Estimated DOA: %.2f degrees", estimated_doa)
        
        beamformed_signal = system.delay_and_sum(mic_signals, estimated_doa)
        logger.info("Processing completed successfully")
        logger.info("Output signal peak value: %d", np.max(np.abs(beamformed_signal)))
        logger.info("Output signal dtype: %s", beamformed_signal.dtype)
        
    except Exception as e:
        logger.error("Processing failed: %s", str(e))
        raise

if __name__ == "__main__":
    main()