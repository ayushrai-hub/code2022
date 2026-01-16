"""
Integration tests for GenAI Code Review Prompt Generator.

Tests the actual functions from app.py to ensure they work correctly.
"""

import sys
import os
import json
from typing import Dict, Any, List

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'streamlit'))

# Import actual functions from app
try:
    from app import generate_llm_prompt, export_data
    IMPORTS_AVAILABLE = True
except ImportError as e:
    IMPORTS_AVAILABLE = False
    IMPORT_ERROR = str(e)

import pytest


@pytest.mark.skipif(not IMPORTS_AVAILABLE, reason=f"Imports not available: {IMPORT_ERROR if not IMPORTS_AVAILABLE else ''}")
class TestAppIntegration:
    """Integration tests for actual app functions."""
    
    def test_generate_llm_prompt_integration(self):
        """Test that generate_llm_prompt works with real data."""
        initial_setup = {
            "instructions for writer": "Test instructions",
            "goal": "Test goal for evaluation",
            "task_category": "Debugging",
            "difficulty_level": "Hard (Graduate)"
        }
        
        turns_data = [
            {
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
                "comparison_justification": "Response 1 is better\n\nJustification: Test",
                "needs_rewrite": "No",
                "rewrite": None,
                "rewrite_explanation": None
            }
        ]
        
        prompt = generate_llm_prompt(initial_setup, turns_data)
        
        # Verify prompt contains key elements
        assert "Test goal for evaluation" in prompt
        assert "Debugging" in prompt
        assert "Hard (Graduate)" in prompt
        assert "Test prompt" in prompt
        assert "Response 1" in prompt
        assert "Response 2" in prompt
    
    def test_generate_llm_prompt_validation(self):
        """Test that generate_llm_prompt validates inputs."""
        initial_setup = {
            "goal": "Test",
            "task_category": "Debugging",
            "difficulty_level": "Medium",
            "instructions for writer": "Test"
        }
        
        # Test with empty turns_data
        with pytest.raises(ValueError, match="turns_data cannot be empty"):
            generate_llm_prompt(initial_setup, [])
        
        # Test with missing key
        incomplete_setup = {
            "goal": "Test",
            "task_category": "Debugging"
            # Missing difficulty_level and instructions
        }
        
        with pytest.raises(ValueError):
            generate_llm_prompt(incomplete_setup, [{"prompt": "test"}])
    
    def test_export_data_json(self):
        """Test export_data function with JSON format."""
        initial_setup = {
            "goal": "Test goal",
            "task_category": "Generation/Synthesis",
            "difficulty_level": "Medium (Undergrad)",
            "instructions for writer": "Test instructions"
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
        
        export_json = export_data(initial_setup, turns_data, "json")
        
        # Verify it's valid JSON
        parsed = json.loads(export_json)
        
        assert "initial_setup" in parsed
        assert "turns" in parsed
        assert "metadata" in parsed
        assert parsed["metadata"]["total_turns"] == 1
        assert parsed["initial_setup"]["goal"] == "Test goal"
    
    def test_export_data_txt(self):
        """Test export_data function with text format."""
        initial_setup = {
            "goal": "Test goal",
            "task_category": "Debugging",
            "difficulty_level": "Hard (Graduate)",
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
        
        export_txt = export_data(initial_setup, turns_data, "txt")
        
        # Verify text format
        assert "Test goal" in export_txt
        assert "Debugging" in export_txt
        assert "Total Turns: 1" in export_txt
        assert "Test prompt" in export_txt


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
