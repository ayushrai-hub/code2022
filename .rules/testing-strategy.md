# Testing Strategy — Comprehensive Testing Discipline

## Core Principles

Testing is not optional — it's a fundamental part of software development:

### 1. Test-First Mindset
- **Write tests before or alongside code**: Don't leave testing until the end
- **Tests define behavior**: Use tests to specify expected behavior
- **Tests as documentation**: Good tests document how code should be used
- **Red-Green-Refactor**: Write failing test → make it pass → improve code

### 2. Test Coverage Philosophy
- **Aim for high coverage**: Target 80%+ for critical paths, 100% for business logic
- **Coverage isn't everything**: 100% coverage of meaningless tests is worthless
- **Test meaningful behavior**: Focus on what the code does, not implementation details
- **Critical paths first**: Ensure business-critical logic is thoroughly tested

### 3. Test Types & When to Use

#### Unit Tests
- **Purpose**: Test individual functions/methods in isolation
- **Speed**: Fast (milliseconds per test)
- **Scope**: Single function, class, or module
- **Dependencies**: Mock external dependencies
- **Use when**: Testing business logic, algorithms, data transformations

#### Integration Tests
- **Purpose**: Test how components work together
- **Speed**: Moderate (seconds per test)
- **Scope**: Multiple modules or components
- **Dependencies**: Use real or mocked external services
- **Use when**: Testing API endpoints, database operations, service interactions

#### End-to-End Tests
- **Purpose**: Test complete user journeys
- **Speed**: Slow (seconds to minutes per test)
- **Scope**: Entire application flow
- **Dependencies**: Real or test environments
- **Use when**: Critical user workflows, happy paths

### 4. Test Quality Standards

#### Test Naming
- **Descriptive names**: `test_user_login_with_invalid_password` not `test_login`
- **Follow conventions**: Use consistent naming patterns (test_<scenario>_<expected_result>)
- **Express intent**: Name should describe what is being tested and expected outcome

#### Test Structure
- **Arrange-Act-Assert (AAA)**: Clear separation of setup, execution, verification
- **Single assertion per test**: One concept per test (but multiple assertions OK for related checks)
- **Test one thing**: Each test should verify one behavior or scenario

#### Test Independence
- **No test dependencies**: Tests shouldn't depend on each other or execution order
- **No shared state**: Each test should set up its own state
- **Isolated**: Tests should be able to run in any order or in parallel

### 5. What to Test

#### Happy Paths
- Normal, expected usage scenarios
- Valid inputs producing correct outputs
- Standard workflows from start to finish

#### Edge Cases
- Boundary conditions (empty strings, zero, max values)
- Null/undefined handling
- Empty collections or arrays
- Maximum/minimum inputs

#### Error Cases
- Invalid inputs producing appropriate errors
- Missing required parameters
- Authentication/authorization failures
- Network or external service failures

#### Business Logic
- Complex calculations and transformations
- Conditional logic and branching
- State transitions
- Business rules and validations

### 6. What NOT to Test

#### Implementation Details
- Don't test private methods directly (test public interface)
- Don't assert on internal state unless necessary
- Don't test framework/library code (test your code)

#### Trivial Code
- Simple getters/setters (unless they contain logic)
- Pure pass-through functions
- Obvious, self-evident code

#### External Dependencies
- Don't test third-party libraries
- Mock external APIs and services
- Test your code's interaction with dependencies, not the dependencies themselves

### 7. Test Data Management

#### Test Fixtures
- **Reusable fixtures**: Create fixtures for common test data
- **Factories**: Use factories for generating test objects
- **Realistic data**: Test data should resemble real-world data

#### Test Isolation
- **Clean state**: Each test should start with a clean state
- **Tear down**: Clean up resources after tests (files, database records, etc.)
- **No side effects**: Tests shouldn't leave permanent changes

### 8. Mocking & Stubbing

#### When to Mock
- **External services**: APIs, databases, file systems
- **Slow operations**: Network calls, complex computations
- **Non-deterministic**: Random values, timestamps (unless testing them)
- **Hard to set up**: Complex dependencies or environments

#### How to Mock
- **Mock external dependencies**: Not your own code (unless testing integration)
- **Verify interactions**: Ensure mocked dependencies are called correctly
- **Return realistic values**: Mocked responses should be believable
- **Test error scenarios**: Mock failures to test error handling

### 9. Test Maintenance

#### Keep Tests Updated
- **Update when code changes**: Tests must reflect current behavior
- **Refactor tests**: Keep tests readable and maintainable
- **Remove obsolete tests**: Delete tests for removed functionality

#### Test Performance
- **Fast execution**: Unit tests should run in milliseconds
- **Parallel execution**: Tests should be able to run concurrently
- **Avoid flakiness**: Tests should be deterministic and reliable

### 10. Testing Anti-Patterns to Avoid

- **Testing implementation details**: Tests break on refactoring
- **Over-mocking**: Mocking everything makes tests meaningless
- **Flaky tests**: Non-deterministic tests that sometimes fail
- **Slow tests**: Tests that take too long discourage running them
- **Test duplication**: Copy-paste test code without adaptation
- **Ignoring failures**: Never skip or ignore failing tests
- **Silent failures**: Tests that pass when they should fail

## Testing Workflow

### Step 1: Write Test
- Write a test that describes desired behavior
- Test should fail initially (Red in TDD)

### Step 2: Make Test Pass
- Write minimal code to make test pass
- Don't over-engineer (Green in TDD)

### Step 3: Refactor
- Improve code while keeping tests green
- Refactor tests if needed (Refactor in TDD)

### Step 4: Repeat
- Continue for each feature or bug fix
- Maintain test coverage as you go

## Test Execution

### Before Committing
- Run all tests locally
- Ensure all tests pass
- Fix any failing tests before committing

### In CI/CD
- Run full test suite on every commit
- Run faster tests first (unit before integration)
- Fail build if any tests fail

### Test Reports
- Generate test coverage reports
- Review coverage gaps regularly
- Use coverage to identify untested code

## Testing Checklist

Before considering code complete:
- [ ] Unit tests written for new functionality
- [ ] Edge cases tested (null, empty, boundaries)
- [ ] Error cases tested (invalid inputs, failures)
- [ ] Integration tests for component interactions
- [ ] All tests pass locally
- [ ] Tests are readable and maintainable
- [ ] Test names clearly describe what they test
- [ ] No flaky or non-deterministic tests
- [ ] Test coverage meets project standards
- [ ] Tests run in CI/CD pipeline
