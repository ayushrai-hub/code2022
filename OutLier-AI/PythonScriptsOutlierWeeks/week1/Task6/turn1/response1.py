import pandas as pd
import random
import datetime as dt
import matplotlib.pyplot as plt
from dateutil.relativedelta import relativedelta
import pytz

# Define a function to generate sample data
def generate_sample_data():
    """Generate sample data for 10 tasks."""
    start_of_week = dt.datetime.now(pytz.utc).replace(hour=9, minute=0, second=0, microsecond=0)
    while start_of_week.weekday() != 0:  # Ensure the date starts on Monday
        start_of_week -= dt.timedelta(days=1)

    data = []
    for task_id in range(1, 11):
        # Randomly assign a worker to a task with varying work hours and time zones
        worker_timezones = ['US/Pacific', 'US/Eastern', 'Europe/London', 'Australia/Sydney']
        worker_tz = random.choice(worker_timezones)
        worker_hours = random.choice([4, 6, 8])  # Part-time workers with different hours

        # Random start time during work hours (Monday to Friday)
        assignment_time = start_of_week + dt.timedelta(hours=random.randint(0, 8 * 5))
        deadline = assignment_time + dt.timedelta(hours=48)

        # Calculate hours spent based on worker's work hours
        hours_spent = random.uniform(0, worker_hours)

        data.append({
            "Task ID": f"Task_{task_id}",
            "Worker ID": f"Worker_{task_id}",
            "Worker Timezone": worker_tz,
            "Worker Hours": worker_hours,
            "Initial Assignment": assignment_time,
            "Deadline": deadline,
            "Hours Spent (First 24h)": hours_spent
        })

    return pd.DataFrame(data)

# Define a function to calculate task progress
def calculate_task_progress(tasks_df, task_id):
    """Calculate progress for a given Task ID."""
    task = tasks_df[tasks_df["Task ID"] == task_id].iloc[0]
    now = dt.datetime.now(pytz.utc)
    deadline = task["Deadline"]
    hours_spent = task["Hours Spent (First 24h)"]
    worker_hours = task["Worker Hours"]

    time_remaining = deadline - now
    if time_remaining.total_seconds() < 0:
        time_remaining_str = "Deadline has passed."
    else:
        days, seconds = divmod(time_remaining.total_seconds(), 86400)
        hours, seconds = divmod(seconds, 3600)
        minutes = seconds // 60
        time_remaining_str = f"{int(days)}d {int(hours)}h {int(minutes)}m"

    # Calculate percentage completed based on worker's work hours
    percentage_completed = min((hours_spent / worker_hours) * 100, 100)

    return {
        "Time Remaining": time_remaining_str,
        "Percentage Completed (First 24h)": f"{percentage_completed:.2f}%"
    }

# Define a function to plot hours spent
def plot_hours_spent(dataframe):
    """Plot hours spent in the first 24 hours for all tasks."""
    plt.figure(figsize=(10, 6))
    plt.bar(dataframe["Task ID"], dataframe["Hours Spent (First 24h)"], color="skyblue")
    plt.xlabel("Task ID")
    plt.ylabel("Hours Spent (First 24 Hours)")
    plt.title("Hours Spent by Workers in the First 24 Hours")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Plot a pie chart of hours spent by each worker
    plt.figure(figsize=(10, 6))
    plt.pie(dataframe["Hours Spent (First 24h)"], labels=dataframe["Worker ID"], autopct='%1.1f%%')
    plt.title("Hours Spent by Each Worker")
    plt.show()

def main():
    # Generate sample data
    tasks_df = generate_sample_data()
    print("Sample Data:")
    print(tasks_df)

    # Plot hours spent
    plot_hours_spent(tasks_df)

    while True:
        task_id = input("Enter Task ID to check progress (or 'exit' to quit): ")
        if task_id.lower() == 'exit':
            break
        progress = calculate_task_progress(tasks_df, task_id)
        if isinstance(progress, str):
            print(progress)  # Display error message for invalid Task ID
        else:
            print(f"Progress for {task_id}:")
            print(f"  Time Remaining: {progress['Time Remaining']}")
            print(f"  Percentage Completed (First 24h): {progress['Percentage Completed (First 24h)']}\n")

if __name__ == "__main__":
    main()