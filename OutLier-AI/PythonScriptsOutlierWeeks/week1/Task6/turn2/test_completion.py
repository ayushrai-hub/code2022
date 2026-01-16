import unittest
import pandas as pd
import datetime as dt
from zoneinfo import ZoneInfo
from unittest.mock import patch
from ideal_completion import ( 
    CONFIG, ValidationError, validate_timezone, validate_hours,
    validate_task_id, generate_sample_data, handle_timezone_transition,
    calculate_task_progress, get_worker_tasks, plot_hours_spent
)

class TestTaskManager(unittest.TestCase):
    def setUp(self):
        # Setup sample data for tests
        self.sample_df = generate_sample_data()
        self.test_time = dt.datetime(2024, 1, 1, 12, 0, tzinfo=ZoneInfo("UTC"))
    
    def test_validation_functions(self):
        # Test timezone validation
        self.assertRaises(ValidationError, validate_timezone, "Invalid_TZ")
        validate_timezone("UTC")  # Should not raise error
        
        # Test hours validation
        self.assertRaises(ValidationError, validate_hours, -1, "full-time")
        self.assertRaises(ValidationError, validate_hours, 25, "full-time")
        validate_hours(8, "full-time")  # Should not raise error
        
        # Test task ID validation
        self.assertRaises(ValidationError, validate_task_id, "Invalid_ID")
        validate_task_id("Task_1")  # Should not raise error
    
    def test_timezone_transition(self):
        # Test timezone conversion
        test_time = dt.datetime.now(ZoneInfo("UTC"))
        result = handle_timezone_transition(test_time, "US/Pacific")
        self.assertEqual(result.tzinfo.key, "US/Pacific")
        
        # Test invalid timezone
        with self.assertRaises(ValidationError):
            handle_timezone_transition(test_time, "Invalid_TZ")
    
    def test_calculate_task_progress(self):
        # Test valid task calculation
        result = calculate_task_progress(self.sample_df, "Task_1")
        self.assertIn("Time Remaining", result)
        self.assertIn("Percentage Completed (First 24h)", result)
        
        # Test invalid task ID
        result = calculate_task_progress(self.sample_df, "Invalid_Task")
        self.assertEqual(result, "Invalid Task ID")
    
    def test_get_worker_tasks(self):
        # Test valid worker
        worker_id = self.sample_df["Worker ID"].iloc[0]
        result = get_worker_tasks(self.sample_df, worker_id)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertFalse(result.empty)
        
        # Test invalid worker
        with self.assertRaises(ValidationError):
            get_worker_tasks(self.sample_df, "Invalid_Worker")
        
        # Test worker with no tasks
        with self.assertRaises(ValidationError):
            get_worker_tasks(self.sample_df, "Worker_999")
    
    def test_sample_data_generation(self):
        df = generate_sample_data()
        # Test DataFrame properties
        self.assertIsInstance(df, pd.DataFrame)
        self.assertFalse(df.empty)
        self.assertLessEqual(len(df), 10)
        
        # Test required columns
        required_columns = [
            "Task ID", "Worker ID", "Worker Type", "Timezone",
            "Initial Assignment", "Deadline", "Hours Spent (First 24h)"
        ]
        for col in required_columns:
            self.assertIn(col, df.columns)

if __name__ == '__main__':
    unittest.main(verbosity=2)