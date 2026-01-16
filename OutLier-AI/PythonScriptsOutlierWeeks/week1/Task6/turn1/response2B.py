import pandas as pd
import random
import datetime as dt
from datetime import timedelta
import matplotlib.pyplot as plt
import pytz

def generate_sample_data():
    """Generate sample data for 10 tasks."""
    start_of_week = dt.datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
    while start_of_week.weekday() != 0:  # Ensure the date starts on Monday
        start_of_week -= timedelta(days=1)

    data = []
    for task_id in range(1, 11):
        assignment_time = start_of_week + timedelta(hours=random.randint(0, 8 * 5))  # Random start time during work hours (Monday to Friday)
        deadline = assignment_time + timedelta(hours=48)
        hours_spent = random.uniform(0, 24)  # Random hours spent in the first 24 hours
        worker_type = random.choice(["Full-time", "Part-time"])
        holidays = random.choice([[], ["2024-09-16"]])  # Randomly select a holiday (in this case, September 16th)
        timezone = random.choice(["US/Eastern", "US/Central", "US/Mountain", "US/Pacific"])
        data.append({
            "Task ID": f"Task_{task_id}",
            "Worker ID": f"Worker_{random.randint(1, 5)}",  # Random worker assignment
            "Initial Assignment": assignment_time,
            "Deadline": deadline,
            "Hours Spent (First 24h)": hours_spent,
            "Worker Type": worker_type,
            "Holidays": holidays,
            "Timezone": timezone
        })

    return pd.DataFrame(data)

def calculate_task_progress(tasks_df, task_id):
    """Calculate progress for a given Task ID."""
    task = tasks_df[tasks_df["Task ID"] == task_id]
    if task.empty:
        return "Invalid Task ID"

    task = task.iloc[0]
    now = dt.datetime.now()
    deadline = task["Deadline"]
    hours_spent = task["Hours Spent (First 24h)"]
    worker_type = task["Worker Type"]
    holidays = task["Holidays"]
    timezone = task["Timezone"]

    # Adjust hours spent based on worker type
    if worker_type == "Part-time":
        hours_spent *= 0.5

    # Adjust deadline based on holidays
    for holiday in holidays:
        holiday_date = dt.datetime.strptime(holiday, "%Y-%m-%d").date()
        if deadline.date() == holiday_date:
            deadline += timedelta(days=1)

    # Localize deadline to worker's timezone
    deadline_tz = pytz.timezone(timezone).localize(deadline)

    time_remaining = deadline_tz - now
    if time_remaining.total_seconds() < 0:
        time_remaining_str = "Deadline has passed."
    else:
        days, seconds = divmod(time_remaining.total_seconds(), 86400)
        hours, seconds = divmod(seconds, 3600)
        minutes = seconds // 60
        time_remaining_str = f"{int(days)}d {int(hours)}h {int(minutes)}m"

    percentage_completed = min((hours_spent / 24) * 100, 100)

    return {
        "Time Remaining": time_remaining_str,
        "Percentage Completed (First 24h)": f"{percentage_completed:.2f}%"
    }
