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

class Beamformer:
    def __init__(self):
        pass
    
    def validate_signals(self, signals, required_mics=NUM_MICS):
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
            
    def validate_angle(self, angle):
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
        
    def validate_inputs(self, target_signal: np.ndarray, noise_signal: np.ndarray, doa_angles: List[float]) -> None:
        """
        Validate input parameters and signals.
        
        Args:
            target_signal: Target audio signal
            noise_signal: Noise signal
            doa_angles: Direction of arrival angles
        Raises:
            ValueError: If inputs are invalid
            
        """
        if not isinstance(target_signal, np.ndarray):
            raise TypeError("Target signal must be a numpy array")
        if len(doa_angles) != NUM_MICS:
            raise ValueError(f"Number of DOA angles ({len(doa_angles)}) must match number of microphones ({NUM_MICS})")
            
        if len(target_signal) != len(noise_signal):
            raise ValueError("Target and noise signals must have the same length")
            
        if not all(-90 <= angle <= 90 for angle in doa_angles):
            raise ValueError("DOA angles must be between -90 and 90 degrees")
            
        if not isinstance(target_signal, np.ndarray) or not isinstance(noise_signal, np.ndarray):
            raise TypeError("Signals must be numpy arrays")
            
    def simulate_microphone_signals(self, target_signal: np.ndarray, 
                                  noise_signal: np.ndarray, 
                                  doa_angles: List[float]) -> np.ndarray:
        """
        Generate microphone signals with embedded system constraints.
        
        Args:
            target_signal: Target audio signal
            noise_signal: Noise signal
            doa_angles: Direction of arrival angles for each microphone
        Returns:
            Array of simulated microphone signals
        """
        # Single validation call that covers all our requirements
        self.validate_inputs(target_signal, noise_signal, doa_angles)
        
        # Initialize with proper shape and int24 precision
        mic_signals = np.zeros((NUM_MICS, len(target_signal)), dtype=np.int32)
        
        try:
            for i in range(NUM_MICS):
                # Calculate delay with bounds checking
                delay = (MIC_DISTANCE * i * np.cos(np.deg2rad(doa_angles[i]))) / SOUND_SPEED
                delay_samples = int(np.clip(delay * SAMPLE_RATE, 0, len(target_signal)-1))
                
                # Process in frames for embedded efficiency
                for frame_start in range(0, len(target_signal), FRAME_SIZE):
                    frame_end = min(frame_start + FRAME_SIZE, len(target_signal))
                    
                    frame_signal = np.roll(target_signal[frame_start:frame_end], delay_samples)
                    frame_noise = noise_signal[frame_start:frame_end]
                    
                    # Convert to int24 precision
                    combined_frame = self.normalize_to_int24(frame_signal + frame_noise)
                    mic_signals[i, frame_start:frame_end] = combined_frame
                    
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
        # Input validation
        self.validate_signals(signals)
        
        sig1 = signals[0]
        sig2 = signals[1]
        n = len(sig1)
        if signals.shape[0] < 2:
            raise ValueError("At least two microphone signals required for DOA estimation")
            
        try:
            # Process in frames for embedded efficiency
            sig1 = signals[0]
            sig2 = signals[1]
            n = len(sig1)
            
            # Convert back to float for FFT processing
            sig1_float = sig1.astype(np.float32) / MAX_INT24
            sig2_float = sig2.astype(np.float32) / MAX_INT24
            
            SIG1 = np.fft.fft(sig1_float)
            SIG2 = np.fft.fft(sig2_float)
            R = SIG1 * np.conj(SIG2)
            
            # Avoid division by zero
            denominator = np.abs(R)
            denominator[denominator < 1e-10] = 1e-10
            
            cross_corr = np.fft.ifft(R / denominator)
            max_delay_idx = np.argmax(np.abs(cross_corr))
            
            # Convert delay to angle with bounds checking
            max_delay = max_delay_idx if max_delay_idx < n // 2 else max_delay_idx - n
            time_delay = max_delay / SAMPLE_RATE
            
            # Check if time delay is within physical limits
            max_possible_delay = MIC_DISTANCE / SOUND_SPEED
            if abs(time_delay) > max_possible_delay:
                warnings.warn("Calculated time delay exceeds physical limits")
                time_delay = np.clip(time_delay, -max_possible_delay, max_possible_delay)
                
            doa_angle = np.arcsin(time_delay * SOUND_SPEED / MIC_DISTANCE) * (180 / np.pi)
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
            for frame_start in range(0, num_samples, FRAME_SIZE):
                frame_end = min(frame_start + FRAME_SIZE, num_samples)
                frame_sum = np.zeros(frame_end - frame_start, dtype=np.int32)
                
                for mic_idx in range(NUM_MICS):
                    delay = (MIC_DISTANCE * mic_idx * np.cos(np.deg2rad(doa_angle))) / SOUND_SPEED
                    delay_samples = int(np.clip(delay * SAMPLE_RATE, 0, num_samples-1))
                    
                    frame = signals[mic_idx, frame_start:frame_end]
                    delayed_frame = np.roll(frame, delay_samples)
                    frame_sum += delayed_frame
                    
                frame_sum = (frame_sum + (NUM_MICS // 2)) // NUM_MICS
                beamformed_signal[frame_start:frame_end] = np.clip(frame_sum, -MAX_INT24, MAX_INT24)
                
            return beamformed_signal
            
        except Exception as e:
            raise RuntimeError(f"Error in beamforming: {str(e)}")

if __name__ == "__main__":
    try:
        beamformer = Beamformer()
        
        # Simulate a target signal (speech) and noise
        t = np.linspace(0, 1, SAMPLE_RATE, endpoint=False)
        target_signal = np.sin(2 * np.pi * 440 * t)  # Simulated speech at 440Hz
        noise_signal = np.random.normal(0, 0.1, len(t))  # Simulated noise
        
        # Convert to int24 precision
        target_signal = beamformer.normalize_to_int24(target_signal)
        noise_signal = beamformer.normalize_to_int24(noise_signal)
        
        # Simulate microphone signals with different DOA angles
        doa_angles = [0, 30, 60, 90]  # DOA angles in degrees for each mic
        mic_signals = beamformer.simulate_microphone_signals(target_signal, noise_signal, doa_angles)
        
        # Estimate DOA
        estimated_doa = beamformer.estimate_doa(mic_signals)
        print(f"Estimated DOA: {estimated_doa:.2f} degrees")
        
        # Perform delay-and-sum beamforming
        beamformed_signal = beamformer.delay_and_sum(mic_signals, estimated_doa)
        
        print("Processing completed successfully")
        print(f"Output signal peak value: {np.max(np.abs(beamformed_signal))}")
        print(f"Output signal dtype: {beamformed_signal.dtype}")
        
        # Optional: Save or play the output
        # import sounddevice as sd
        # sd.play((beamformed_signal / MAX_INT24).astype(np.float32), SAMPLE_RATE)
        
    except Exception as e:
        print(f"Error in main execution: {str(e)}")