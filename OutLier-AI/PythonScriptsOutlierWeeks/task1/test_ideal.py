import unittest
from ideal_completion import calculate_final_grade, calculate_gpa, generate_transcript, process_transcripts

class TestTranscriptSystem(unittest.TestCase):
    def setUp(self):
        # Valid test data
        self.valid_performance = {
            "assignments": 85,
            "exams": 90,
            "attendance": 95
        }
        
        self.valid_subject = {
            "name": "Math",
            "credits": 3,
            "performance": self.valid_performance
        }
        
        self.valid_student = {
            "id": "S001",
            "name": "Alice",
            "semesters": [{
                "term": "Fall 2023",
                "subjects": [self.valid_subject]
            }]
        }

    def test_calculate_final_grade_valid(self):
        """Test calculation of final grade with valid inputs"""
        grade = calculate_final_grade(self.valid_performance)
        self.assertGreaterEqual(grade, 0)
        self.assertLessEqual(grade, 100)
        # Expected grade: (85 * 0.3) + (90 * 0.5) + (95 * 0.2) = 89.5
        self.assertAlmostEqual(grade, 89.5)

    def test_calculate_final_grade_missing_metrics(self):
        """Test handling of missing performance metrics"""
        invalid_performance = {
            "assignments": 85,
            "exams": 90
            # Missing attendance
        }
        with self.assertRaises(ValueError) as context:
            calculate_final_grade(invalid_performance)
        self.assertIn("Missing attendance", str(context.exception))

    def test_calculate_final_grade_out_of_range(self):
        """Test handling of out-of-range scores"""
        invalid_performances = [
            {"assignments": -1, "exams": 90, "attendance": 95},
            {"assignments": 85, "exams": 101, "attendance": 95},
            {"assignments": 85, "exams": 90, "attendance": 150}
        ]
        for perf in invalid_performances:
            with self.assertRaises(ValueError):
                calculate_final_grade(perf)

    def test_calculate_gpa_valid(self):
        """Test GPA calculation with valid inputs"""
        subjects = [
            {
                "name": "Math",
                "credits": 3,
                "performance": {"assignments": 100, "exams": 100, "attendance": 100}
            }
        ]
        gpa, credits = calculate_gpa(subjects)
        self.assertEqual(credits, 3)
        self.assertEqual(gpa, 4.0)  # Perfect scores should give 4.0 GPA

    def test_calculate_gpa_zero_credits(self):
        """Test GPA calculation with zero credit courses"""
        subjects = [
            {
                "name": "Math",
                "credits": 0,  # Invalid credits
                "performance": self.valid_performance
            }
        ]
        with self.assertRaises(ZeroDivisionError):
            calculate_gpa(subjects)

    def test_generate_transcript_honors(self):
        """Test transcript generation with honors-worthy GPA"""
        student = {
            "id": "S001",
            "name": "Alice",
            "semesters": [{
                "term": "Fall 2023",
                "subjects": [{
                    "name": "Math",
                    "credits": 3,
                    "performance": {"assignments": 100, "exams": 100, "attendance": 100}
                }]
            }]
        }
        transcript = generate_transcript(student)
        self.assertIn("with Honors", transcript)

    def test_generate_transcript_no_honors(self):
        """Test transcript generation with below-honors GPA"""
        student = {
            "id": "S001",
            "name": "Alice",
            "semesters": [{
                "term": "Fall 2023",
                "subjects": [{
                    "name": "Math",
                    "credits": 3,
                    "performance": {"assignments": 70, "exams": 70, "attendance": 70}
                }]
            }]
        }
        transcript = generate_transcript(student)
        self.assertNotIn("with Honors", transcript)

    def test_empty_student_data(self):
        """Test handling of empty student data"""
        empty_data = {"students": []}
        # Should not raise an exception
        process_transcripts(empty_data)

    def test_missing_student_fields(self):
        """Test handling of missing required student fields"""
        invalid_student = {
            # Missing id
            "name": "Alice",
            "semesters": []
        }
        with self.assertRaises(KeyError):
            generate_transcript(invalid_student)

    def test_decimal_credits(self):
        """Test handling of decimal credit values"""
        subjects = [{
            "name": "Math",
            "credits": 3.5,
            "performance": self.valid_performance
        }]
        gpa, credits = calculate_gpa(subjects)
        self.assertEqual(credits, 3.5)

    def test_multiple_semesters_cumulative_gpa(self):
        """Test cumulative GPA calculation across multiple semesters"""
        student = {
            "id": "S001",
            "name": "Alice",
            "semesters": [
                {
                    "term": "Fall 2023",
                    "subjects": [{
                        "name": "Math",
                        "credits": 3,
                        "performance": {"assignments": 90, "exams": 90, "attendance": 90}
                    }]
                },
                {
                    "term": "Spring 2024",
                    "subjects": [{
                        "name": "Physics",
                        "credits": 3,
                        "performance": {"assignments": 90, "exams": 90, "attendance": 90}
                    }]
                }
            ]
        }
        transcript = generate_transcript(student)
        self.assertIn("Cumulative GPA", transcript)

if __name__ == '__main__':
    unittest.main(verbosity=2)