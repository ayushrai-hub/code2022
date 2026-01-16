
import pandas as pd
import random
import datetime as dt
from datetime import timedelta
import matplotlib.pyplot as plt
from zoneinfo import ZoneInfo  # For timezone handling
import holidays  # For holiday handling
from typing import Dict, List, Optional, Union
import logging
CONFIG = {
    'VALID_TIMEZONES': ["UTC", "US/Pacific", "US/Eastern", "Asia/Tokyo"],
    'WORK_HOURS': {'full-time': 8, 'part-time': 4},
    'MAX_TASKS_PER_WORKER': 3,
    'WORK_START_HOUR': 9,
    'WORK_END_HOUR': 17
}

def validate_timezone(timezone: str) -> None:
    """Validate if the given timezone is in the list of valid timezones."""
    if timezone not in CONFIG['VALID_TIMEZONES']:
        raise ValidationError(f"Invalid timezone")

def validate_hours(hours: float, worker_type: str) -> None:
    """Validate if the given hours are within the allowed range for the worker type."""
    max_hours = CONFIG['WORK_HOURS'][worker_type] * 3
    if hours < 0 or hours > max_hours:
        raise ValidationError(f"Invalid hours")

def validate_task_id(task_id: str) -> None:
    """Validate if the task ID matches the expected format."""
    if not task_id.startswith("Task_"):
        raise ValidationError("Invalid task ID format")

def generate_sample_data() -> pd.DataFrame:
    """
    Generate sample data for 10 tasks with timezone and part-time worker support.
    
    Returns:
        pd.DataFrame: DataFrame containing task assignments and tracking data
    """
    # ... (implementation details)

def handle_timezone_transition(current_time: dt.datetime, timezone: str) -> dt.datetime:
    """
    Handle timezone transitions and DST adjustments.
    
    Args:
        current_time: The datetime to convert
        timezone: Target timezone string
        
    Returns:
        dt.datetime: Adjusted datetime in target timezone
    """
    # ... (implementation details)

def calculate_task_progress(tasks_df, task_id):
    """
    Calculate task progress with timezone and work schedule considerations.
    Returns progress details including adjusted deadline and completion percentage.
    """
    # ... (implementation details)

def get_worker_tasks(tasks_df: pd.DataFrame, worker_id: str) -> pd.DataFrame:
    """Get all tasks assigned to a worker."""
    # ... (implementation details)


def plot_hours_spent(dataframe):
    """
    Create a pie chart showing hours spent distribution across tasks.
    Includes proper labeling and percentage display.
    """
    # ... (implementation details)

def print_progress(progress: Dict[str, str]) -> None:
    """
    Print task progress information in a formatted way.
    
    Args:
        progress: Dictionary containing progress information
    """
    # ... (implementation details)

def main():
    # ... (implementation details)

if __name__ == "__main__":
    main()