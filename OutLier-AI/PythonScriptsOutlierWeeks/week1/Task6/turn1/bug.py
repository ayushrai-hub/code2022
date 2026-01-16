import pandas as pd
import random
import datetime as dt


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
            "Initial Assignment": assignment_time,
            "Deadline": deadline,
            "Hours Spent (First 24h)": hours_spent
        })

    return pd.DataFrame(data)

def calculate_task_progress(tasks_df, task_id):
    """Calculate progress for a given Task ID."""
    task = tasks_df[tasks_df["Task ID"] == task_id].iloc[0]
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

    percentage_completed = min((hours_spent / 28) * 100, 100)

    return {
        "Time Remaining": time_remaining_str,
        "Percentage Completed (First 24h)": f"{percentage_completed:.2f}%"
    }

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

def main():
    # Generate sample data
    tasks_df = generate_sample_data()
    print("Sample Data:")
    print(tasks_df)

    while True:
        task_id = input("Enter Task ID to check progress (or 'exit' to quit): ")
        progress = calculate_task_progress(tasks_df, task_id)
        if isinstance(progress, str):
            print(progress)  # Display error message for invalid Task ID
        else:
            print(f"Progress for {task_id}:")
            print(f"  Time Remaining: {progress['Time Remaining']}")
            print(f"  Percentage Completed (First 24h): {progress['Percentage Completed (First 24h)']}\n")

if __name__ == "__main__":
    main()
