import pandas as pd
import random
import datetime as dt
from datetime import timedelta
import matplotlib.pyplot as plt

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
        data.append({
            "Task ID": f"Task_{task_id}",
            "Worker ID": f"Worker_{random.randint(1, 5)}",  # Random worker assignment
            "Initial Assignment": assignment_time,
            "Deadline": deadline,
            "Hours Spent (First 24h)": hours_spent
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

    time_remaining = deadline - now
    if time_remaining.total_seconds() < 0:
        time_remaining_str = "Deadline has passed."
    else:
        days, seconds = divmod(time_remaining.total_seconds(), 86400)
        hours, seconds = divmod(seconds, 3600)
        minutes = seconds // 60
        time_remaining_str = f"{int(days)}d {int(hours)}h {int(minutes)}m"

    percentage_completed = min((hours_spent / 24) * 100, 100)  # Corrected the denominator

    return {
        "Time Remaining": time_remaining_str,
        "Percentage Completed (First 24h)": f"{percentage_completed:.2f}%"
    }

def plot_hours_spent(dataframe):
    """Plot hours spent in the first 24 hours for all tasks."""
    plt.figure(figsize=(10, 6))
    plt.pie(dataframe["Hours Spent (First 24h)"], labels=dataframe["Task ID"], autopct='%1.1f%%')
    plt.title("Hours Spent by Workers in the First 24 Hours")
    plt.show()

def main():
    # Generate sample data
    tasks_df = generate_sample_data()
    print("Sample Data:")
    print(tasks_df)

    while True:
        print("\\nOptions:")
        print("1. Check task progress")
        print("2. Plot hours spent")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            task_id = input("Enter Task ID to check progress: ")
            progress = calculate_task_progress(tasks_df, task_id)
            if isinstance(progress, str):
                print(progress)  # Display error message for invalid Task ID
            else:
                print(f"Progress for {task_id}:")
                print(f"  Time Remaining: {progress['Time Remaining']}")
                print(f"  Percentage Completed (First 24h): {progress['Percentage Completed (First 24h)']}\\n")
        elif choice == "2":
            plot_hours_spent(tasks_df)
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
