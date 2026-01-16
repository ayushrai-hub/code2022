import pandas as pd
from datetime import datetime, timedelta
import random

# Generate sample data
def generate_task_data():
    monday = pd.Timestamp.now().normalize() - timedelta(days=pd.Timestamp.now().weekday())
    data = {
        'Task_ID': range(1, 11),
        'Worker_ID': [f'DEV_{i}' for i in range(100, 110)],
        'Assignment_Time': [monday + timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59)) for _ in range(10)],
    }
    
    df = pd.DataFrame(data)
    df['Deadline'] = df['Assignment_Time'] + timedelta(hours=48)
    df['Progress_24hr'] = [random.randint(0, 100) for _ in range(10)]
    return df

def calculate_remaining_time(worker_id):
    df = generate_task_data()
    current_time = datetime.now()
    
    worker_tasks = df[df['Worker_ID'] == worker_id]
    if len(worker_tasks) == 0:
        print(f"No tasks found for {worker_id}")
        return
    
    for _, task in worker_tasks.iterrows():
        time_left = task['Deadline'] - current_time
        progress = task['Progress_24hr']
        print(f"Task {task['Task_ID']}:")
        print(f"Time left: {time_left}")
        print(f"Progress: {progress}%")

def main():
    worker_id = input("Enter Worker ID (format: DEV_XXX): ")
    calculate_remaining_time(worker_id)

if __name__ == "__main__":
    main()