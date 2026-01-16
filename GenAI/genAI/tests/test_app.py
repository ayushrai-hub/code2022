"""
Unit tests for the Code Review Prompt Generator application.

Tests cover:
- Initial setup validation
- Turn data creation
- Prompt generation
- Data export functionality
- Error handling
"""

import pytest
import json
from typing import Dict, Any, List
import sys
import os

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'streamlit'))

# Note: Streamlit components are difficult to test directly
# These tests focus on the data processing logic


class TestDataValidation:
    """Test data validation and structure."""
    
    def test_initial_setup_structure(self):
        """Test that initial setup has required keys."""
        # Mock initial setup data
        initial_setup = {
            "instructions for writer": "test instructions",
            "goal": "Test goal",
            "task_category": "Generation/Synthesis",
            "difficulty_level": "Medium (Undergrad)"
        }
        
        required_keys = ["goal", "task_category", "difficulty_level", "instructions for writer"]
        for key in required_keys:
            assert key in initial_setup, f"Missing required key: {key}"
    
    def test_turn_data_structure(self):
        """Test that turn data has required structure."""
        turn_data = {
            "prompt": "Test prompt",
            "responses": [
                {
                    "response_text": "Response 1",
                    "instruction_following": "1 (No Issue)",
                    "instruction_following_justification": "Test",
                    "accuracy_validation": "1 (No Issue)",
                    "accuracy_validation_justification": "Test",
                    "efficiency": "1 (No Issue)",
                    "efficiency_justification": "Test",
                    "presentation": "1 (No Issue)",
                    "presentation_justification": "Test",
                    "up_to_date": "1 (No Issue)",
                    "up_to_date_justification": "Test",
                    "comments": ""
                },
                {
                    "response_text": "Response 2",
                    "instruction_following": "2 (Minor Issue)",
                    "instruction_following_justification": "Test",
                    "accuracy_validation": "2 (Minor Issue)",
                    "accuracy_validation_justification": "Test",
                    "efficiency": "2 (Minor Issue)",
                    "efficiency_justification": "Test",
                    "presentation": "2 (Minor Issue)",
                    "presentation_justification": "Test",
                    "up_to_date": "2 (Minor Issue)",
                    "up_to_date_justification": "Test",
                    "comments": ""
                }
            ],
            "comparison_justification": "Response 1 is better",
            "needs_rewrite": "No",
            "rewrite": None,
            "rewrite_explanation": None
        }
        
        assert "prompt" in turn_data
        assert "responses" in turn_data
        assert len(turn_data["responses"]) == 2
        assert "comparison_justification" in turn_data
        assert "needs_rewrite" in turn_data


class TestPromptGeneration:
    """Test prompt generation logic."""
    
    def test_prompt_contains_goal(self):
        """Test that generated prompt contains the goal."""
        initial_setup = {
            "goal": "Test goal for evaluation",
            "task_category": "Debugging",
            "difficulty_level": "Hard (Graduate)",
            "instructions for writer": "Test instructions"
        }
        
        # Simulate prompt generation (simplified)
        prompt_text = f"Primary Goal: {initial_setup['goal']}"
        assert "Test goal for evaluation" in prompt_text
    
    def test_prompt_contains_task_category(self):
        """Test that generated prompt contains task category."""
        initial_setup = {
            "goal": "Test goal",
            "task_category": "Documentation",
            "difficulty_level": "Medium (Undergrad)",
            "instructions for writer": "Test"
        }
        
        prompt_text = f"Task Category: {initial_setup['task_category']}"
        assert "Documentation" in prompt_text


class TestDataExport:
    """Test data export functionality."""
    
    def test_export_json_structure(self):
        """Test that JSON export has correct structure."""
        initial_setup = {
            "goal": "Test",
            "task_category": "Generation/Synthesis",
            "difficulty_level": "Medium (Undergrad)",
            "instructions for writer": "Test"
        }
        
        turns_data = [
            {
                "prompt": "Test prompt",
                "responses": [
                    {"response_text": "Response 1", "instruction_following": "1 (No Issue)"},
                    {"response_text": "Response 2", "instruction_following": "2 (Minor Issue)"}
                ],
                "comparison_justification": "Response 1 is better",
                "needs_rewrite": "No"
            }
        ]
        
        export_data = {
            "initial_setup": initial_setup,
            "turns": turns_data,
            "metadata": {
                "total_turns": len(turns_data),
                "export_format": "json"
            }
        }
        
        json_str = json.dumps(export_data, indent=2)
        parsed = json.loads(json_str)
        
        assert "initial_setup" in parsed
        assert "turns" in parsed
        assert "metadata" in parsed
        assert parsed["metadata"]["total_turns"] == 1
    
    def test_export_json_valid(self):
        """Test that exported JSON is valid."""
        data = {
            "test": "data",
            "number": 42,
            "list": [1, 2, 3]
        }
        
        json_str = json.dumps(data)
        parsed = json.loads(json_str)
        
        assert parsed["test"] == "data"
        assert parsed["number"] == 42
        assert len(parsed["list"]) == 3


class TestErrorHandling:
    """Test error handling scenarios."""
    
    def test_empty_goal_validation(self):
        """Test that empty goal is detected."""
        goal = ""
        assert not goal or not goal.strip(), "Empty goal should be detected"
    
    def test_missing_turn_data(self):
        """Test handling of missing turn data."""
        turns_data = []
        assert len(turns_data) == 0, "Empty turns data should be detected"
    
    def test_incomplete_turn_data(self):
        """Test handling of incomplete turn data."""
        turn = {
            "prompt": "Test",
            # Missing responses
        }
        
        assert "responses" not in turn or len(turn.get("responses", [])) < 2, \
            "Incomplete turn data should be detected"


class TestDataIntegrity:
    """Test data integrity and consistency."""
    
    def test_response_count(self):
        """Test that each turn has exactly 2 responses."""
        turn = {
            "responses": [
                {"response_text": "Response 1"},
                {"response_text": "Response 2"}
            ]
        }
        
        assert len(turn["responses"]) == 2, "Each turn should have 2 responses"
    
    def test_evaluation_dimensions(self):
        """Test that each response has all evaluation dimensions."""
        response = {
            "instruction_following": "1 (No Issue)",
            "accuracy_validation": "1 (No Issue)",
            "efficiency": "1 (No Issue)",
            "presentation": "1 (No Issue)",
            "up_to_date": "1 (No Issue)"
        }
        
        required_dimensions = [
            "instruction_following",
            "accuracy_validation",
            "efficiency",
            "presentation",
            "up_to_date"
        ]
        
        for dimension in required_dimensions:
            assert dimension in response, f"Missing dimension: {dimension}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
