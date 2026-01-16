import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_test_sensor_data(num_sensors=5, days=7, reading_interval_mins=15):
    """
    Generate test weather sensor data
    
    Parameters:
    - num_sensors: Number of sensors to simulate
    - days: Number of days of data to generate
    - reading_interval_mins: Minutes between readings
    
    Returns:
    - Dictionary mapping sensor IDs to DataFrames containing their readings
    """
    sensor_data = {}
    base_time = datetime(2024, 1, 1)  # Start from Jan 1, 2024
    total_readings = int((days * 24 * 60) / reading_interval_mins)
    
    # Create timestamp range
    timestamps = [base_time + timedelta(minutes=i*reading_interval_mins) 
                 for i in range(total_readings)]
    
    np.random.seed(42)  # For reproducibility
    
    for sensor in range(num_sensors):
        # Generate normal temperature data with daily seasonality
        hours = np.array([t.hour for t in timestamps])
        base_temp = 20 + 5 * np.sin(2 * np.pi * (hours - 6) / 24)  # Peak at noon, low at midnight
        temp = base_temp + np.random.normal(0, 1, total_readings)
        
        # Generate humidity data correlated with temperature
        base_humidity = 50 - 0.3 * (temp - 20)  # Humidity decreases as temperature increases
        humidity = base_humidity + np.random.normal(0, 5, total_readings)
        humidity = np.clip(humidity, 0, 100)  # Ensure humidity stays between 0-100%
        
        # Add some anomalies (about 1% of readings)
        anomaly_indices = np.random.choice(total_readings, total_readings//100)
        temp[anomaly_indices] += np.random.uniform(-10, 10, len(anomaly_indices))
        humidity[anomaly_indices] += np.random.uniform(-20, 20, len(anomaly_indices))
        
        # Create DataFrame for this sensor
        df = pd.DataFrame({
            'timestamp': timestamps,
            'temperature': temp,
            'humidity': humidity,
            'sensor_id': f'SENSOR_{sensor:03d}'
        })
        
        sensor_data[f'SENSOR_{sensor:03d}'] = df
    
    return sensor_data

# Example output for a single reading
if __name__ == "__main__":
    test_data = generate_test_sensor_data(num_sensors=2, days=1)
    print("\nSample data from first sensor:")
    print(test_data['SENSOR_000'].head())