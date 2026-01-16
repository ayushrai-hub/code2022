"""
Code Review Evaluation Framework Instructions

This module contains the comprehensive evaluation framework instructions used by
the Code Review Prompt Generator. These instructions define the evaluation
criteria, dimensions, and requirements for assessing AI model responses to
coding tasks.
"""

writer_instructions = """
# Code Review Evaluation Framework

## Overview
This framework provides a structured approach for evaluating coding abilities using a goal-oriented, multi-turn methodology. It simulates real-world software development scenarios that require iterative refinement.

## I. Project Goal
To systematically evaluate LLM performance across diverse coding tasks through structured, multi-turn conversations. The process involves:
- Providing series of prompts
- Analyzing responses based on detailed rubrics
- Iteratively refining prompts and responses
- Uncovering capabilities in code generation, comprehension, and reasoning

## II. Task Specifications

### A. Goal Definition
Before starting, establish:
- Precise, achievable coding goal
- Task category (generation, debugging, optimization, etc.)
- Target programming language
- Difficulty level:
  * Medium (Undergraduate)
  * Hard (Graduate)
  * Challenger (SME)

Requirements:
- Clear articulation
- Unambiguous goals
- Testable outcomes
- Evaluator expertise matching difficulty level

### B. Evaluation Dimensions

#### 1. Instruction Following
- **No Issue (1)**: 
  * Fulfills primary request and all constraints
  * Shows deep understanding
  * Handles ambiguity well
  * Adheres to requirements without overstepping
- **Minor Issue (2)**:
  * Fulfills primary request but misses some constraints
  * Could better handle ambiguity
- **Major Issue (3)**:
  * Fails primary request or major constraints

#### 2. Accuracy and Input Validation
- **No Issue (1)**:
  * Error-free execution
  * Safe, vulnerability-free code
  * Factual accuracy
  * Coherent with context
  * Prior errors addressed
  * Comprehensive input validation
  * Proper error handling for invalid inputs
- **Minor Issue (2)**:
  * Non-failing syntax errors
  * Low-risk vulnerabilities
  * Ambiguous coherence
  * Unproven assertions
  * Basic input validation present
  * Some error handling gaps
- **Major Issue (3)**:
  * Execution failures
  * Severe vulnerabilities
  * False claims
  * Contextual inconsistency
  * Missing input validation
  * Poor error handling

#### 3. Optimality and Efficiency
- **No Issue (1)**:
  * High performance
  * Edge case optimization
  * Standard practices adherence
  * Efficient resource usage
  * Scalable design
- **Minor Issue (2)**:
  * Room for low-effort optimization
  * Scalability concerns
  * Most standards followed
  * Some resource inefficiencies
- **Major Issue (3)**:
  * Severe performance issues
  * Standard practice violations
  * Resource wastage
  * Poor scalability

#### 4. Presentation
- **No Issue (1)**:
  * Clear documentation
  * Well-structured code
  * Readable variable names
  * Proper formatting
  * Modular design
  * Consistent style
- **Minor Issue (2)**:
  * Sufficient but sparse documentation
  * Minor readability issues
  * Room for structural improvement
  * Style inconsistencies
- **Major Issue (3)**:
  * Insufficient documentation
  * Poor readability
  * Disorganized structure
  * Major style issues

#### 5. Up-to-Date Practices
- **No Issue (1)**:
  * Current APIs/libraries
  * Maintained versions
  * Modern patterns
- **Minor Issue (2)**:
  * Slightly outdated but functional
  * Legacy patterns with justification
- **Major Issue (3)**:
  * Deprecated components
  * Runtime/compile errors
  * Obsolete patterns

### C. Rewrite Requirements

1. Mandatory Rewrite Conditions:
   - Major issues in any evaluation dimension
   - Multiple minor issues across dimensions
   - Security vulnerabilities
   - Critical functionality gaps
   - Poor input validation
   - Severe performance issues

2. Rewrite Guidelines:
   - Address ALL identified issues
   - Maintain or improve existing functionality
   - Add comprehensive documentation
   - Implement proper input validation
   - Follow consistent style
   - Use modern patterns appropriately
   - Consider scalability
   - Add error handling

3. Rewrite Explanation Requirements:
   - List all issues being addressed
   - Explain approach to each fix
   - Justify new design decisions
   - Document improvements
   - Note any trade-offs
   - Verify all requirements met

### D. Justification Requirements

1. Rating Justifications:
   - Specific examples from code
   - Clear reasoning for rating
   - Impact assessment
   - Reference to standards
   - Improvement suggestions

2. Comparison Justifications:
   - Detailed dimension-by-dimension comparison
   - Clear reasoning for preference
   - Impact of differences
   - Trade-off analysis
   - Future considerations

3. Rewrite Justifications:
   - Complete issue coverage
   - Clear improvement mapping
   - Design decision explanations
   - Verification of fixes
   - Future-proofing considerations
"""
