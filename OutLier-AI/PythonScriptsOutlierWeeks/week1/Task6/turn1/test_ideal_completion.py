import unittest
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
import matplotlib.pyplot as plt
import io
import sys
from ideal_completion import (
    generate_sample_data, 
    calculate_task_progress,
    validate_timezone,
    validate_hours,
    validate_task_id,
    handle_timezone_transition,
    get_worker_tasks,
    plot_hours_spent,
    ValidationError,
    CONFIG
)

class TestTaskTracker(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Setup test data once for all tests"""
        cls.test_df = generate_sample_data()
    
    def setUp(self):
        """Reset any test-specific data before each test"""
        self.captured_output = io.StringIO()
        sys.stdout = self.captured_output

    def tearDown(self):
        """Cleanup after each test"""
        sys.stdout = sys.__stdout__
        plt.close('all')

    def test_data_generation(self):
        """Test if sample data is generated correctly"""
        df = self.test_df
        self.assertEqual(len(df), 10)
        required_columns = [
            "Task ID", "Worker ID", "Worker Type", "Timezone",
            "Initial Assignment", "Deadline", "Hours Spent (First 24h)"
        ]
        self.assertTrue(all(col in df.columns for col in required_columns))
        
        # Test data validation
        self.assertTrue(all(df["Task ID"].str.startswith("Task_")))
        self.assertTrue(all(df["Worker ID"].str.startswith("Worker_")))
        self.assertTrue(all(df["Worker Type"].isin(CONFIG['WORK_HOURS'].keys())))
        self.assertTrue(all(df["Timezone"].isin(CONFIG['VALID_TIMEZONES'])))
        self.assertTrue(all(df["Hours Spent (First 24h)"] >= 0))
        self.assertTrue(all(df["Hours Spent (First 24h)"] <= 24))

    def test_timezone_validation(self):
        """Test timezone validation"""
        # Valid timezone
        try:
            validate_timezone("UTC")
        except ValidationError:
            self.fail("validate_timezone raised ValidationError unexpectedly")
        
        # Invalid timezone
        with self.assertRaises(ValidationError):
            validate_timezone("INVALID_TZ")

    def test_hours_validation(self):
        """Test hours validation"""
        # Valid hours for full-time
        try:
            validate_hours(20, "full-time")
        except ValidationError:
            self.fail("validate_hours raised ValidationError unexpectedly")
        
        # Invalid hours (negative)
        with self.assertRaises(ValidationError):
            validate_hours(-1, "full-time")
        
        # Invalid hours (too many)
        with self.assertRaises(ValidationError):
            validate_hours(25, "part-time")

    def test_task_id_validation(self):
        """Test task ID validation"""
        # Valid task ID
        try:
            validate_task_id("Task_1")
        except ValidationError:
            self.fail("validate_task_id raised ValidationError unexpectedly")
        
        # Invalid task ID
        with self.assertRaises(ValidationError):
            validate_task_id("Invalid_1")

    def test_timezone_transition(self):
        """Test timezone transition handling"""
        test_time = datetime.now(ZoneInfo("UTC"))
        
        # Test valid timezone transition
        result = handle_timezone_transition(test_time, "US/Pacific")
        self.assertEqual(result.tzinfo.key, "US/Pacific")
        
        # Test working hours constraint
        result = handle_timezone_transition(
            test_time.replace(hour=20), 
            "UTC"
        )
        self.assertLessEqual(result.hour, CONFIG['WORK_END_HOUR'])
        
        # Test invalid timezone
        with self.assertRaises(ValidationError):
            handle_timezone_transition(test_time, "Invalid/TZ")

    def test_task_progress_calculation(self):
        """Test task progress calculation"""
        # Test valid task
        test_task_id = self.test_df.iloc[0]["Task ID"]
        result = calculate_task_progress(self.test_df, test_task_id)
        self.assertIsInstance(result, dict)
        self.assertIn("Time Remaining", result)
        self.assertIn("Percentage Completed (First 24h)", result)
        
        # Test invalid task
        result = calculate_task_progress(self.test_df, "Invalid_Task")
        self.assertEqual(result, "Invalid Task ID")

    def test_worker_tasks_retrieval(self):
        """Test worker tasks retrieval"""
        # Test valid worker
        test_worker_id = self.test_df.iloc[0]["Worker ID"]
        result = get_worker_tasks(self.test_df, test_worker_id)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertFalse(result.empty)
        
        # Test invalid worker ID
        with self.assertRaises(ValidationError):
            get_worker_tasks(self.test_df, "Invalid_Worker")

    @patch('matplotlib.pyplot.show')
    def test_plot_generation(self, mock_show):
        """Test plot generation"""
        try:
            plot_hours_spent(self.test_df)
            mock_show.assert_called_once()
        except Exception as e:
            self.fail(f"plot_hours_spent raised an exception: {e}")

def run_tests():
    """Run all tests and capture results"""
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTaskTracker)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    
    if result.wasSuccessful():
        print("\n✅ All tests passed successfully!")
    else:
        print("\n❌ Some tests failed:")
        for failure in result.failures:
            print(f"\nTest: {failure[0]}")
            print(f"Error: {failure[1]}")
        for error in result.errors:
            print(f"\nTest: {error[0]}")
            print(f"Error: {error[1]}")

if __name__ == '__main__':
    run_tests()