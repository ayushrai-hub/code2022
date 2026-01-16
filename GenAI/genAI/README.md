# GenAI - Code Review Prompt Generator

A Streamlit web application for generating comprehensive LLM prompts for code review evaluation with multi-dimensional analysis.

## Overview

This tool helps evaluate AI model responses to coding tasks by:
- Collecting structured conversation data across multiple turns
- Evaluating responses across 5 dimensions (Instruction Following, Accuracy/Validation, Efficiency, Presentation, Up-to-Date)
- Comparing multiple responses
- Generating detailed LLM prompts for comprehensive code review

## Features

- **Multi-turn Evaluation**: Evaluate conversations across multiple turns
- **5-Dimensional Analysis**: Comprehensive evaluation across instruction following, accuracy, efficiency, presentation, and modern practices
- **Response Comparison**: Compare two AI responses per turn
- **Rewrite Support**: Mark turns that need rewriting with explanations
- **Prompt Generation**: Generate detailed LLM prompts for code review
- **Data Export**: Export evaluation data as JSON or text

## Technology Stack

- **Python 3.8+**
- **Streamlit** - Web framework
- **JSON** - Data serialization

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Navigate to the project directory:
```bash
cd GenAI/genAI
```

2. Create a virtual environment (recommended):
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Application

```bash
streamlit run streamlit/app.py
```

The application will open in your default web browser at `http://localhost:8501`

### Using the Application

1. **Initial Setup**:
   - Enter the goal for the conversation
   - Select task category (Generation/Synthesis, Editing/Rewriting, Debugging, etc.)
   - Choose difficulty level (Medium, Hard, Challenger)

2. **Create Turns**:
   - Set the number of turns (1-10)
   - For each turn:
     - Enter the prompt/question
     - Provide two AI model responses
     - Evaluate each response across 5 dimensions
     - Compare the responses
     - Optionally provide a rewrite if needed

3. **Generate Prompt**:
   - Click "Generate Review Prompt" to create the LLM prompt
   - Download the prompt as a text file

4. **Export Data**:
   - Export evaluation data as JSON for further analysis
   - Clear all data to start fresh

## Project Structure

```
GenAI/genAI/
├── streamlit/
│   ├── app.py              # Main application
│   └── instructions.py     # Evaluation framework instructions
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── tests/                 # Test files (to be added)
```

## Development

### Adding Features

When adding new features:
1. Follow the existing code structure
2. Add type hints to all functions
3. Include error handling
4. Add input validation
5. Update this README
6. Write tests for new functionality

### Code Style

- Use type hints for all functions
- Follow PEP 8 style guide
- Add docstrings to all functions
- Use meaningful variable names

## Testing

Tests are located in the `tests/` directory. Run tests with:

```bash
pytest tests/ -v
```

For coverage report:
```bash
pytest tests/ -v --cov=. --cov-report=html
```

## Troubleshooting

### Application won't start
- Ensure Python 3.8+ is installed
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check that Streamlit is properly installed: `streamlit --version`

### Data lost on refresh
- This is expected behavior - use the export functionality to save data
- Future versions may include persistent storage

### Errors in prompt generation
- Ensure all required fields are filled
- Check that at least one turn is completed
- Verify goal is not empty

## Future Improvements

- [ ] Persistent data storage (database or file-based)
- [ ] Import functionality for previous evaluations
- [ ] Enhanced validation and error messages
- [ ] More export formats (CSV, PDF)
- [ ] Template system for common evaluation scenarios
- [ ] Analytics dashboard for evaluation trends

## License

[Add license information]

## Contributing

[Add contribution guidelines]

---

**Last Updated:** 2025-01-16
