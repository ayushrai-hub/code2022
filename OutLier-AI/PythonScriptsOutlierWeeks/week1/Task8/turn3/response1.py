import numpy as np
from typing import List, Tuple, Optional
import warnings

# Constants
SAMPLE_RATE = 16000  # Sampling rate in Hz
SOUND_SPEED = 343     # Sound speed in m/s
MIC_DISTANCE = 0.05  # Distance between microphones in meters
NUM_MICS = 4            # Total microphones in the array
FRAME_SIZE = 512     # Processing frame size for embedded systems
MAX_INT24 = 8388607  # Maximum value for 24-bit integer

class AudioSignalProcessor:
    def __init__(self, sample_rate: int = SAMPLE_RATE, sound_speed: float = SOUND_SPEED, mic_distance: float = MIC_DISTANCE, num_mics: int = NUM_MICS):
        self.sample_rate = sample_rate
        self.sound_speed = sound_speed
        self.mic_distance = mic_distance
        self.num_mics = num_mics

    def validate_signals(self, signals: np.ndarray, required_mics: int = NUM_MICS) -> None:
        """Validate input signals"""
        if not isinstance(signals, np.ndarray):
            raise TypeError("Signals must be a numpy array")
        if len(signals.shape) != 2:
            raise ValueError("Signals must be a 2D array")
        if signals.shape[0] != required_mics:
            raise ValueError(f"Expected {required_mics} microphones, got {signals.shape[0]}")
        if signals.size == 0:
            raise ValueError("Signals cannot be empty")
        if not np.all(np.isfinite(signals)):
            raise ValueError("Signals contain invalid values (inf or nan)")

    def validate_angle(self, angle: float) -> None:
        """Validate DOA angle"""
        if not isinstance(angle, (int, float, np.number)):
            raise TypeError("Angle must be a number")
        if angle < -90 or angle > 90:
            raise ValueError("Angle must be between -90 and 90 degrees")

    def normalize_to_int24(self, signal: np.ndarray) -> np.ndarray:
        """
        Convert float64 signal to int24-compatible values.
        
        Args:
            signal: Input signal array
        Returns:
            Normalized signal within int24 range
        """
        max_val = np.max(np.abs(signal))
        if max_val == 0:
            return signal
        normalized = (signal / max_val) * MAX_INT24
        return np.clip(normalized, -MAX_INT24, MAX_INT24).astype(np.int32)

    def simulate_microphone_signals(self, target_signal: np.ndarray, noise_signal: np.ndarray, doa_angles: List[float]) -> np.ndarray:
        """
        Generate microphone signals with embedded system constraints.
        
        Args:
            target_signal: Target audio signal
            noise_signal: Noise signal
            doa_angles: Direction of arrival angles for each microphone
        Returns:
            Array of simulated microphone signals
        """
        self.validate_signals(np.array([target_signal, noise_signal]), required_mics=2)
        if len(doa_angles) != self.num_mics:
            raise ValueError(f"Number of DOA angles ({len(doa_angles)}) must match number of microphones ({self.num_mics})")
        
        mic_signals = np.zeros((self.num_mics, len(target_signal)), dtype=np.int32)
        
        try:
            for i in range(self.num_mics):
                delay = (self.mic_distance * i * np.cos(np.deg2rad(doa_angles[i]))) / self.sound_speed
                delay_samples = int(np.clip(delay * self.sample_rate, 0, len(target_signal)-1))
                
                frame_signal = np.roll(target_signal, delay_samples)
                frame_noise = noise_signal
                
                combined_frame = self.normalize_to_int24(frame_signal + frame_noise)
                mic_signals[i] = combined_frame
                
        except Exception as e:
            raise RuntimeError(f"Error in signal simulation: {str(e)}")
        
        return mic_signals

    def estimate_doa(self, signals: np.ndarray) -> float:
        """
        Enhanced DOA estimation with validation and error handling.
        
        Args:
            signals: Array of microphone signals
        Returns:
            Estimated direction of arrival angle
        """
        self.validate_signals(signals)
        
        sig1 = signals[0]
        sig2 = signals[1]
        n = len(sig1)
        
        try:
            SIG1 = np.fft.fft(sig1.astype(np.float32) / MAX_INT24)
            SIG2 = np.fft.fft(sig2.astype(np.float32) / MAX_INT24)
            R = SIG1 * np.conj(SIG2)
            
            denominator = np.abs(R)
            denominator[denominator < 1e-10] = 1e-10
            
            cross_corr = np.fft.ifft(R / denominator)
            max_delay_idx = np.argmax(np.abs(cross_corr))
            
            max_delay = max_delay_idx if max_delay_idx < n // 2 else max_delay_idx - n
            time_delay = max_delay / self.sample_rate
            
            max_possible_delay = self.mic_distance / self.sound_speed
            if abs(time_delay) > max_possible_delay:
                warnings.warn("Calculated time delay exceeds physical limits")
                time_delay = np.clip(time_delay, -max_possible_delay, max_possible_delay)
                
            doa_angle = np.arcsin(time_delay * self.sound_speed / self.mic_distance) * (180 / np.pi)
            return float(np.clip(doa_angle, -90, 90))
            
        except Exception as e:
            raise RuntimeError(f"Error in DOA estimation: {str(e)}")

    def delay_and_sum(self, signals: np.ndarray, doa_angle: float) -> np.ndarray:
        """Simple delay-and-sum beamformer."""
        self.validate_signals(signals)
        self.validate_angle(doa_angle)
        
        num_samples = signals.shape[1]
        beamformed_signal = np.zeros(num_samples, dtype=np.int32)
        
        try:
            for i in range(self.num_mics):
                delay = (self.mic_distance * i * np.cos(np.deg2rad(doa_angle))) / self.sound_speed
                delay_samples = int(np.clip(delay * self.sample_rate, 0, num_samples-1))
                
                delayed_signal = np.roll(signals[i], delay_samples)
                beamformed_signal += delayed_signal
                
            beamformed_signal = self.normalize_to_int24(beamformed_signal)
            
        except Exception as e:
            raise RuntimeError(f"Error in beamforming: {str(e)}")
        
        return beamformed_signal


if __name__ == "__main__":
    try:
        processor = AudioSignalProcessor()
        
        t = np.linspace(0, 1, SAMPLE_RATE, endpoint=False)
        target_signal = np.sin(2 * np.pi * 440 * t)  # Simulated speech at 440Hz
        noise_signal = np.random.normal(0, 0.1, len(t))  # Simulated noise
        
        target_signal = processor.normalize_to_int24(target_signal)
        noise_signal = processor.normalize_to_int24(noise_signal)
        
        doa_angles = [0, 30, 60, 90]  # DOA angles in degrees for each mic
        mic_signals = processor.simulate_microphone_signals(target_signal, noise_signal, doa_angles)
        
        estimated_doa = processor.estimate_doa(mic_signals)
        print(f"Estimated DOA: {estimated_doa:.2f} degrees")
        
        beamformed_signal = processor.delay_and_sum(mic_signals, estimated_doa)
        
        print("Processing completed successfully")
        print(f"Output signal peak value: {np.max(np.abs(beamformed_signal))}")
        print(f"Output signal dtype: {beamformed_signal.dtype}")
        
    except Exception as e:
        print(f"Error in main execution: {str(e)}")