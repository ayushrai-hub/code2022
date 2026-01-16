import pandas as pd
import random
import datetime as dt
from datetime import timedelta
import matplotlib.pyplot as plt
from zoneinfo import ZoneInfo  # For timezone handling
import holidays  # For holiday handling
from typing import Dict, List, Optional, Union
import logging
class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass
CONFIG = {
    'VALID_TIMEZONES': ["UTC", "US/Pacific", "US/Eastern", "Asia/Tokyo"],
    'WORK_HOURS': {'full-time': 8, 'part-time': 4},
    'MAX_TASKS_PER_WORKER': 3,
    'WORK_START_HOUR': 9,
    'WORK_END_HOUR': 17
}

def validate_timezone(timezone: str) -> None:
    if timezone not in CONFIG['VALID_TIMEZONES']:
        raise ValidationError(f"Invalid timezone")

def validate_hours(hours: float, worker_type: str) -> None:
    max_hours = CONFIG['WORK_HOURS'][worker_type] * 3
    if hours < 0 or hours > max_hours:
        raise ValidationError(f"Invalid hours")

def validate_task_id(task_id: str) -> None:
    if not task_id.startswith("Task_"):
        raise ValidationError("Invalid task ID format")

def generate_sample_data() -> pd.DataFrame:
    """
    Generate sample data for 10 tasks with timezone and part-time worker support.
    Returns a DataFrame with task assignments and progress tracking.
    
    Returns:
        pd.DataFrame: DataFrame containing task assignments and tracking data
    """
    # Initialize worker schedules tracking
    worker_schedules: Dict[str, List[str]] = {}
    data = []
    
    # Ensure consistent start time in UTC
    start_of_week = dt.datetime.now(ZoneInfo("UTC")).replace(
        hour=CONFIG['WORK_START_HOUR'], 
        minute=0, 
        second=0, 
        microsecond=0
    )
    while start_of_week.weekday() != 0:  # Adjust to Monday
        start_of_week -= timedelta(days=1)
        
    us_holidays = holidays.US()  # US holiday calendar

    for task_id in range(1, 11):
        # Generate worker ID and check availability
        worker_id = f"Worker_{random.randint(1, 5)}"
        if worker_id not in worker_schedules:
            worker_schedules[worker_id] = []
            
        # Skip if worker has max tasks
        if len(worker_schedules[worker_id]) >= CONFIG['MAX_TASKS_PER_WORKER']:
            continue
            
        # Randomly assign worker type and timezone
        worker_type = random.choice(list(CONFIG['WORK_HOURS'].keys()))
        worker_timezone = random.choice(CONFIG['VALID_TIMEZONES'])
        
        # Generate assignment time
        assignment_time = start_of_week + timedelta(hours=random.randint(0, 8))
        
        # Calculate deadline with holiday and weekend adjustments
        deadline = assignment_time + timedelta(hours=48)
        additional_hours = 0
        current = assignment_time
        
        while current <= deadline:
            if current.weekday() >= 5 or current.date() in us_holidays:
                additional_hours += 24
            current += timedelta(days=1)
        deadline += timedelta(hours=additional_hours)
        
        # Calculate hours spent based on worker type
        max_hours = CONFIG['WORK_HOURS'][worker_type] * 3  # 3 work periods
        hours_spent = random.uniform(0, min(24, max_hours))
        
        # Create task entry
        task_data = {
            "Task ID": f"Task_{task_id}",
            "Worker ID": worker_id,
            "Worker Type": worker_type,
            "Timezone": worker_timezone,
            "Initial Assignment": assignment_time,
            "Deadline": deadline,
            "Hours Spent (First 24h)": hours_spent,
            "Status": "not_started",
            "Expected Progress": CONFIG['WORK_HOURS'][worker_type] * 3,
            "Continuous Hours": []
        }
        
        data.append(task_data)
        worker_schedules[worker_id].append(f"Task_{task_id}")

    return pd.DataFrame(data)


def handle_timezone_transition(current_time: dt.datetime, timezone: str) -> dt.datetime:
    """
    Handle timezone transitions and DST adjustments.
    
    Args:
        current_time: The datetime to convert
        timezone: Target timezone string
        
    Returns:
        dt.datetime: Adjusted datetime in target timezone
    """
    try:
        validate_timezone(timezone)
        zone = ZoneInfo(timezone)
        local_time = current_time.astimezone(zone)
        
        # Check for DST transition
        tomorrow = local_time + timedelta(days=1)
        if local_time.dst() != tomorrow.dst():
            # Adjust if we're in DST transition period
            dst_offset = local_time.dst()
            if dst_offset:
                local_time += dst_offset
                
        # Ensure time is within working hours
        local_time = local_time.replace(
            hour=max(min(local_time.hour, CONFIG['WORK_END_HOUR']), 
                    CONFIG['WORK_START_HOUR'])
        )
        return local_time
        
    except Exception as e:
        logging.error(f"Timezone transition error: {e}")
        raise ValidationError(f"Failed to handle timezone transition: {e}")


def calculate_task_progress(tasks_df, task_id):
    """
    Calculate task progress with timezone and work schedule considerations.
    Returns progress details including adjusted deadline and completion percentage.
    """
    try:
        task = tasks_df[tasks_df["Task ID"] == task_id].iloc[0]
    except (IndexError, KeyError):
        return "Invalid Task ID"

        # Add timezone transition handling
    now = handle_timezone_transition(dt.datetime.now(), task["Timezone"])
    deadline = handle_timezone_transition(task["Deadline"], task["Timezone"])

    # Convert times to task's timezone
    now = dt.datetime.now(ZoneInfo(task["Timezone"]))
    deadline = task["Deadline"].replace(tzinfo=ZoneInfo(task["Timezone"]))
    hours_spent = task["Hours Spent (First 24h)"]
    worker_type = task["Worker Type"]

    # Calculate time remaining with holiday/weekend adjustments
    time_remaining = deadline - now
    if time_remaining.total_seconds() < 0:
        time_remaining_str = "Deadline has passed."
    else:
        # Adjust for holidays and weekends
        us_holidays = holidays.US()
        remaining_work_hours = time_remaining.total_seconds() / 3600
        current = now
        while current <= deadline:
            if current.weekday() >= 5 or current.date() in us_holidays:
                remaining_work_hours -= 24
            current += timedelta(days=1)
        
        days, hours = divmod(max(0, remaining_work_hours), 24)
        minutes = (hours % 1) * 60
        time_remaining_str = f"{int(days)}d {int(hours)}h {int(minutes)}m"

    # Adjust completion percentage based on worker type
    max_hours = 24 if worker_type == "full-time" else 12
    percentage_completed = min((hours_spent / max_hours) * 100, 100)

    return {
        "Time Remaining": time_remaining_str,
        "Percentage Completed (First 24h)": f"{percentage_completed:.2f}%"
    }

def get_worker_tasks(tasks_df: pd.DataFrame, worker_id: str) -> pd.DataFrame:
    """Get all tasks assigned to a worker."""
    if not worker_id.startswith("Worker_"):
        raise ValidationError("Invalid worker ID")
    worker_tasks = tasks_df[tasks_df["Worker ID"] == worker_id]
    if worker_tasks.empty:
        raise ValidationError(f"No tasks found for {worker_id}")
    return worker_tasks

def plot_hours_spent(dataframe):
    """
    Create a pie chart showing hours spent distribution across tasks.
    Includes proper labeling and percentage display.
    """
    plt.figure(figsize=(10, 8))
    hours = dataframe["Hours Spent (First 24h)"]
    labels = [f"{task} ({hours:.1f}h)" for task, hours in zip(dataframe["Task ID"], hours)]
    
    plt.pie(hours, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.title("Distribution of Hours Spent in First 24 Hours")
    plt.axis('equal')
    plt.show()

def print_progress(progress: Dict[str, str]) -> None:
    """
    Print task progress information in a formatted way.
    
    Args:
        progress: Dictionary containing progress information
    """
    try:
        if isinstance(progress, str):
            print(progress)  # Error message
            return
            
        print("\nTask Progress:")
        print(f"  Time Remaining: {progress['Time Remaining']}")
        print(f"  Completion: {progress['Percentage Completed (First 24h)']}")
        
        # Add status indicators
        percentage = float(progress['Percentage Completed (First 24h)'].rstrip('%'))
        if percentage >= 90:
            status = "� On Track"
        elif percentage >= 60:
            status = "� Needs Attention"
        else:
            status = "� Behind Schedule"
        print(f"  Status: {status}")
        
    except Exception as e:
        logging.error(f"Error printing progress: {e}")
        print("Error displaying progress information")

def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    try:
        tasks_df = generate_sample_data()
        print("\nSample Data:")
        print(tasks_df.to_string())
        
        while True:
            command = input("\nEnter command (task_id/worker_id/plot/exit): ")
            
            try:
                if command.startswith('Worker_'):
                    worker_tasks = get_worker_tasks(tasks_df, command)
                    print("\nTasks for", command)
                    print(worker_tasks)
                elif command == 'plot':
                    plot_hours_spent(tasks_df)
                elif command.startswith('Task_'):
                    progress = calculate_task_progress(tasks_df, command)
                    print_progress(progress)
                elif command == 'exit':
                    break
                else:
                    print("Invalid command")
            except ValidationError as e:
                print(f"Error: {e}")
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                
    except Exception as e:
        logger.error(f"Application error: {e}")

if __name__ == "__main__":
    main()