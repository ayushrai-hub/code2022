"""
Code Review Prompt Generator - Main Application

This Streamlit application generates comprehensive LLM prompts for code review evaluation.
It collects multi-turn conversation data and evaluation metrics to create detailed review prompts.
"""

import streamlit as st
import json
from typing import Dict, List, Any, Optional
from instructions import writer_instructions


def create_initial_setup() -> Dict[str, Any]:
    """
    Create the initial setup form for the code review evaluation.
    
    Collects:
    - Goal: The primary objective of the coding task
    - Task Category: Type of coding task
    - Difficulty Level: Complexity level of the task
    
    Returns:
        Dictionary containing initial setup data including writer instructions,
        goal, task category, and difficulty level.
    
    Raises:
        ValueError: If required fields are empty (validation handled by UI)
    """
    goal = st.text_area(
        "Goal Setting: Record the goal for this conversation",
        placeholder="Enter the goal of the conversation here...",
        help="Describe the primary objective or goal for this coding task evaluation."
    )
    
    # Validate goal is not empty
    if not goal or not goal.strip():
        st.warning("⚠️ Please enter a goal for the conversation.")
    
    task_category = st.selectbox(
        "Task Category",
        ["Generation/Synthesis", "Editing/Rewriting", "Debugging", "Documentation", "Review/Critique", "Code Ecosystem"],
        help="Select the category that best describes the coding task type."
    )
    
    difficulty_level = st.selectbox(
        "Difficulty Level",
        ["Medium (Undergrad)", "Hard (Graduate)", "Challenger (SME)"],
        help="Select the difficulty level appropriate for the task complexity."
    )
    
    return {
        "instructions for writer": writer_instructions,
        "goal": goal.strip() if goal else "",
        "task_category": task_category,
        "difficulty_level": difficulty_level
    }


def create_turn_section(turn_num: int) -> Dict[str, Any]:
    """
    Create a turn section for collecting conversation data and evaluations.
    
    Each turn collects:
    - A prompt/question
    - Two AI model responses
    - Multi-dimensional evaluations for each response
    - Comparison between responses
    - Optional rewrite if needed
    
    Args:
        turn_num: The turn number (1-indexed)
    
    Returns:
        Dictionary containing all turn data including prompt, responses,
        evaluations, comparison, and rewrite information.
    """
    st.subheader(f"Turn {turn_num}")
    
    # Prompt for this turn
    prompt = st.text_area(
        f"Prompt for Turn {turn_num}",
        key=f"prompt_{turn_num}",
        help="Enter the prompt or question for this turn of the conversation.",
        placeholder="Enter the prompt here..."
    )
    
    # Validate prompt is not empty
    if not prompt or not prompt.strip():
        st.warning(f"⚠️ Please enter a prompt for Turn {turn_num}.")
    
    # Response sections - collect two responses for comparison
    responses: List[Dict[str, Any]] = []
    for response_num in [1, 2]:
        st.write(f"### Response {response_num}")
        
        # Model response
        response_text = st.text_area(
            f"Model Response {response_num} for Turn {turn_num}",
            key=f"response_{turn_num}_{response_num}"
        )
        
        # Response evaluation
        st.write(f"#### Evaluation for Response {response_num}")
        
        # Rating dimensions with justifications
        dimensions = {
            "instruction_following": "Instruction Following",
            "accuracy_validation": "Accuracy and Input Validation",
            "efficiency": "Optimality and Efficiency",
            "presentation": "Presentation",
            "up_to_date": "Up-to-Date"
        }
        
        ratings = {}
        justifications = {}
        
        for key, label in dimensions.items():
            col1, col2 = st.columns([1, 2])
            with col1:
                ratings[key] = st.radio(
                    label,
                    ["1 (No Issue)", "2 (Minor Issue)", "3 (Major Issue)"],
                    key=f"{key}_{turn_num}_{response_num}"
                )
            with col2:
                justifications[key] = st.text_area(
                    f"Justify your {label} rating",
                    key=f"{key}_justification_{turn_num}_{response_num}",
                    height=100
                )
        
        comments = st.text_area(
            "Additional Comments",
            key=f"comments_{turn_num}_{response_num}",
            help="Please provide any additional comments or explanations for your ratings."
        )
        
        responses.append({
            "response_text": response_text,
            "instruction_following": ratings["instruction_following"],
            "instruction_following_justification": justifications["instruction_following"],
            "accuracy_validation": ratings["accuracy_validation"],
            "accuracy_validation_justification": justifications["accuracy_validation"],
            "efficiency": ratings["efficiency"],
            "efficiency_justification": justifications["efficiency"],
            "presentation": ratings["presentation"],
            "presentation_justification": justifications["presentation"],
            "up_to_date": ratings["up_to_date"],
            "up_to_date_justification": justifications["up_to_date"],
            "comments": comments
        })
    
    # Comparison section
    st.write("### Response Comparison")
    comparison_justification = st.radio(
        "Which response is better?",
        [
            "1 - Response 1 is much better",
            "2 - Response 1 is better",
            "3 - Response 1 is slightly better",
            "4 - Response 1 is negligibly better",
            "5 - Response 2 is negligibly better",
            "6 - Response 2 is slightly better",
            "7 - Response 2 is better",
            "8 - Response 2 is much better"
        ],
        key=f"response_comparison_{turn_num}"
    )
    
    comparison_explanation = st.text_area(
        "Explain your comparison",
        key=f"comparison_explanation_{turn_num}",
        help="Please provide detailed reasoning for your comparison choice."
    )
    
    # Rewrite section
    st.write("### Rewrite Section")
    needs_rewrite = st.radio(
        "Does this turn need a rewrite?",
        ["No", "Yes"],
        key=f"needs_rewrite_{turn_num}"
    )
    
    rewrite = None
    rewrite_explanation = None
    if needs_rewrite == "Yes":
        rewrite = st.text_area(
            "Provide the rewrite",
            key=f"rewrite_{turn_num}"
        )
        rewrite_explanation = st.text_area(
            "Explain your rewrite",
            key=f"rewrite_explanation_{turn_num}",
            help="Please explain why this rewrite was necessary and how it improves upon the original responses."
        )
    
    return {
        "prompt": prompt,
        "responses": responses,
        "comparison_justification": f"{comparison_justification}\n\nJustification: {comparison_explanation}",
        "needs_rewrite": needs_rewrite,
        "rewrite": rewrite,
        "rewrite_explanation": rewrite_explanation if needs_rewrite == "Yes" else None
    }


def generate_llm_prompt(initial_setup: Dict[str, Any], turns_data: List[Dict[str, Any]]) -> str:
    """
    Generate a comprehensive LLM prompt for code review evaluation.
    
    This function constructs a detailed prompt that includes:
    - Task context (goal, category, difficulty)
    - Evaluation criteria
    - Complete conversation history with evaluations
    - Instructions for comprehensive review
    
    Args:
        initial_setup: Dictionary containing goal, task category, difficulty level, and instructions
        turns_data: List of dictionaries, each containing a turn's data (prompt, responses, evaluations)
    
    Returns:
        A formatted string containing the complete LLM prompt for code review.
    
    Raises:
        ValueError: If initial_setup is missing required keys or turns_data is empty
    """
    # Validate inputs
    required_keys = ["goal", "task_category", "difficulty_level", "instructions for writer"]
    for key in required_keys:
        if key not in initial_setup:
            raise ValueError(f"Missing required key in initial_setup: {key}")
    
    if not turns_data:
        raise ValueError("turns_data cannot be empty")
    
    # Validate each turn has required data
    for i, turn in enumerate(turns_data, 1):
        if not turn.get("prompt"):
            raise ValueError(f"Turn {i} is missing a prompt")
        if not turn.get("responses") or len(turn["responses"]) < 2:
            raise ValueError(f"Turn {i} must have at least 2 responses")
    
    prompt = f"""You are an expert code reviewer tasked with providing detailed, actionable feedback. Please analyze the following coding task, conversation, and evaluation process:

Task Context:
- Primary Goal: {initial_setup['goal']}
- Task Category: {initial_setup['task_category']}
- Difficulty Level: {initial_setup['difficulty_level']}
- Writer Instructions: {initial_setup['instructions for writer']}

Evaluation Criteria:
1. Code Quality and Correctness:
   - Implementation accuracy
   - Input validation and error handling
   - Security considerations
   - Edge case handling
   - Error recovery mechanisms
   - Data validation
   - Exception management
   - Boundary conditions

2. Performance and Efficiency:
   - Algorithm complexity
   - Resource utilization
   - Memory management
   - Scalability characteristics
   - Bottleneck identification
   - Optimization opportunities
   - Cache considerations
   - I/O efficiency

3. Code Organization and Style:
   - Structure and modularity
   - Naming conventions
   - Documentation quality
   - Code formatting
   - Component separation
   - Interface design
   - Dependency management
   - Pattern usage

4. Best Practices and Standards:
   - Modern design patterns
   - Industry standards
   - Security practices
   - Testing approach
   - Error handling patterns
   - Logging strategies
   - Configuration management
   - Deployment considerations

Task History and Solutions:
"""
    
    for i, turn in enumerate(turns_data, 1):
        prompt += f"\n=== Turn {i} ===\n"
        prompt += f"Writer's Task/Question:\n{turn['prompt']}\n"
        
        prompt += "\nInitial Solution Attempts:\n"
        for j, response in enumerate(turn['responses'], 1):
            prompt += f"\nResponse {j}:\n{response['response_text']}\n"
            prompt += f"Evaluation of Response {j}:\n"
            prompt += f"1. Instruction Following: {response['instruction_following']}\n"
            prompt += f"   Justification: {response['instruction_following_justification']}\n"
            prompt += f"2. Accuracy and Input Validation: {response['accuracy_validation']}\n"
            prompt += f"   Justification: {response['accuracy_validation_justification']}\n"
            prompt += f"3. Code Efficiency: {response['efficiency']}\n"
            prompt += f"   Justification: {response['efficiency_justification']}\n"
            prompt += f"4. Code Presentation: {response['presentation']}\n"
            prompt += f"   Justification: {response['presentation_justification']}\n"
            prompt += f"5. Modern Practices: {response['up_to_date']}\n"
            prompt += f"   Justification: {response['up_to_date_justification']}\n"
            if response['comments']:
                prompt += f"Additional Notes: {response['comments']}\n"
        
        prompt += f"\nComparison of Initial Solutions: {turn['comparison_justification']}\n"
        
        prompt += "\nFinal Solution:"
        if turn.get('needs_rewrite') == "Yes":
            prompt += " (Rewritten due to issues in initial solutions)\n"
            prompt += f"{turn['rewrite']}\n"
            prompt += f"Rewrite Rationale: {turn['rewrite_explanation']}\n"
        else:
            better_response = 1
            if any(turn['comparison_justification'].lower().find(x) != -1 for x in 
                  ["response 2 is better", "response 2 is much better", "response 2 is slightly better"]):
                better_response = 2
            prompt += f" (Original Response {better_response} was optimal)\n"
            prompt += f"{turn['responses'][better_response - 1]['response_text']}\n"

    prompt += """
Please provide a comprehensive review addressing:

1. Solution Quality Assessment:
   - Effectiveness in solving the original task
   - Technical implementation quality
   - Input validation and error handling
   - Security measures
   - Achievement of stated goals

2. Technical Analysis:
   - Implementation strengths/weaknesses
   - Algorithm efficiency
   - Resource utilization
   - Error handling completeness
   - Input validation coverage
   - Edge case handling
   - Security considerations
   - Performance characteristics
   - Testing coverage

3. Best Practices Evaluation:
   - Code organization
   - Documentation quality
   - Error handling patterns
   - Input validation approach
   - Security practices
   - Maintainability
   - Reusability
   - Modern pattern usage

4. Improvement Recommendations:
   - Specific enhancement suggestions
   - Alternative approaches
   - Optimization opportunities
   - Security improvements
   - Input validation enhancements
   - Error handling refinements
   - Future-proofing considerations

5. Evaluation Process Assessment:
   For each turn, please assess:
   
   a) Rating Accuracy and Justifications:
      For each dimension (Instruction Following, Accuracy/Validation, Efficiency, Presentation, Up-to-Date):
      - Is the rating (1-3) appropriate given the response?
      - Is the justification specific and well-reasoned?
      - Are concrete examples provided?
      - Is the impact properly assessed?
      - Are standards referenced where relevant?
      - Are improvement suggestions included?
      - Are there any inconsistencies?
   
   b) Comparison Assessment:
      - Is the comparison detailed and dimension-specific?
      - Is the reasoning clear and well-supported?
      - Are differences properly analyzed?
      - Are trade-offs considered?
      - Was the better response correctly identified?
      - Are future implications considered?
   
   c) Rewrite Analysis:
      - Was a rewrite needed based on mandatory conditions?
      - Were ALL identified issues addressed?
      - Is the rewrite explanation comprehensive?
      - Are design decisions justified?
      - Were improvements properly verified?
      - Is proper input validation added?
      - Is error handling complete?
      - Are there any remaining issues?

6. Overall Evaluation Quality:
   - Rating consistency across responses
   - Justification completeness and specificity
   - Comparative analysis depth
   - Rewrite decision appropriateness
   - Issue coverage completeness
   - Improvement verification thoroughness
   - Future consideration inclusion

Please structure your review with clear sections and provide specific examples where applicable. For each issue identified, explain:
1. What the issue is
2. Why it's an issue
3. How it could be improved
4. Impact of the issue
5. Verification of the fix

Focus on providing actionable feedback that will help improve both:
- Just feedback is required no need to correct anything
- The rewrite does not need to be anything extra from the promp (exactly should be what is asked with proper error handeling and edge case)
- The implementation quality
- The evaluation process accuracy
- The justification clarity and completeness
- The input validation coverage
- The error handling robustness"""

    return prompt


def export_data(initial_setup: Dict[str, Any], turns_data: List[Dict[str, Any]], format: str = "json") -> str:
    """
    Export evaluation data to a specified format.
    
    Args:
        initial_setup: Initial setup data
        turns_data: List of turn data
        format: Export format ("json" or "txt")
    
    Returns:
        String representation of exported data
    """
    export_data = {
        "initial_setup": initial_setup,
        "turns": turns_data,
        "metadata": {
            "total_turns": len(turns_data),
            "export_format": format
        }
    }
    
    if format == "json":
        return json.dumps(export_data, indent=2, ensure_ascii=False)
    else:
        # Text format
        text = f"Code Review Evaluation Data\n"
        text += f"{'='*50}\n\n"
        text += f"Goal: {initial_setup['goal']}\n"
        text += f"Task Category: {initial_setup['task_category']}\n"
        text += f"Difficulty: {initial_setup['difficulty_level']}\n\n"
        text += f"Total Turns: {len(turns_data)}\n\n"
        for i, turn in enumerate(turns_data, 1):
            text += f"Turn {i}:\n"
            text += f"  Prompt: {turn.get('prompt', 'N/A')}\n"
            text += f"  Responses: {len(turn.get('responses', []))}\n\n"
        return text


def main() -> None:
    """
    Main application entry point.
    
    Sets up the Streamlit interface and handles user interactions for:
    - Initial setup configuration
    - Multi-turn conversation data collection
    - Response evaluation
    - Prompt generation
    - Data export
    """
    st.title("Code Review Prompt Generator")
    st.markdown("Generate comprehensive LLM prompts for code review evaluation with multi-dimensional analysis.")
    
    # Initial setup section
    st.header("Initial Setup")
    try:
        initial_setup = create_initial_setup()
    except Exception as e:
        st.error(f"Error in initial setup: {str(e)}")
        st.stop()
    
    # Conversation turns section
    st.header("Task Turns")
    num_turns = st.number_input(
        "Number of turns",
        min_value=1,
        max_value=10,
        value=1,
        help="Number of conversation turns to evaluate (1-10)"
    )
    
    # Store turn data in session state for persistence
    if 'turns_data' not in st.session_state:
        st.session_state.turns_data = []
    
    # Ensure we have enough turns in session state
    while len(st.session_state.turns_data) < num_turns:
        st.session_state.turns_data.append(None)
    
    # Remove excess turns if user reduced number
    if len(st.session_state.turns_data) > num_turns:
        st.session_state.turns_data = st.session_state.turns_data[:num_turns]
    
    # Create tabs for each turn
    tabs = st.tabs([f"Turn {i+1}" for i in range(num_turns)])
    
    # Collect data for each turn
    for i, tab in enumerate(tabs):
        with tab:
            try:
                turn_data = create_turn_section(i + 1)
                st.session_state.turns_data[i] = turn_data
            except Exception as e:
                st.error(f"Error in Turn {i+1}: {str(e)}")
                st.session_state.turns_data[i] = None
    
    # Generate prompt and export section
    st.header("Generated LLM Prompt")
    
    # Filter out any None values from turns_data
    valid_turns = [turn for turn in st.session_state.turns_data if turn is not None and turn.get("prompt")]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Generate Review Prompt", type="primary"):
            if not initial_setup.get("goal") or not initial_setup["goal"].strip():
                st.error("⚠️ Please enter a goal in the Initial Setup section.")
            elif not valid_turns:
                st.warning("⚠️ Please complete at least one turn with a prompt before generating.")
            else:
                try:
                    generated_prompt = generate_llm_prompt(initial_setup, valid_turns)
                    st.code(generated_prompt, language="text")
                    
                    # Add download button for prompt
                    st.download_button(
                        label="Download Prompt",
                        data=generated_prompt,
                        file_name="code_review_prompt.txt",
                        mime="text/plain"
                    )
                except ValueError as e:
                    st.error(f"Validation error: {str(e)}")
                except Exception as e:
                    st.error(f"Error generating prompt: {str(e)}")
    
    with col2:
        if st.button("Export Data (JSON)"):
            if valid_turns:
                try:
                    export_json = export_data(initial_setup, valid_turns, "json")
                    st.download_button(
                        label="Download JSON",
                        data=export_json,
                        file_name="evaluation_data.json",
                        mime="application/json"
                    )
                except Exception as e:
                    st.error(f"Error exporting data: {str(e)}")
            else:
                st.warning("No data to export. Complete at least one turn first.")
    
    with col3:
        if st.button("Clear All Data"):
            if st.session_state.get('turns_data'):
                st.session_state.turns_data = []
                st.session_state.clear()
                st.success("Data cleared! Please refresh the page.")
                st.rerun()


if __name__ == "__main__":
    main()
