# Testing Strategy

## Overview

This document outlines the testing strategy for all projects in this repository. Since projects use different technologies, each has its own testing approach, but we follow common principles.

## Core Testing Principles

### 1. Test Coverage Goals
- **Critical paths:** 100% coverage
- **Business logic:** 80%+ coverage
- **Overall:** 80%+ coverage target
- **Coverage quality over quantity:** Meaningful tests are more important than high coverage numbers

### 2. Test Types

#### Unit Tests
- **Purpose:** Test individual functions/methods in isolation
- **Speed:** Fast (milliseconds per test)
- **Scope:** Single function, class, or module
- **Dependencies:** Mock external dependencies
- **When:** Test business logic, algorithms, data transformations

#### Integration Tests
- **Purpose:** Test how components work together
- **Speed:** Moderate (seconds per test)
- **Scope:** Multiple modules or components
- **Dependencies:** Use real or mocked external services
- **When:** Test API endpoints, database operations, service interactions

#### End-to-End Tests
- **Purpose:** Test complete user journeys
- **Speed:** Slow (seconds to minutes per test)
- **Scope:** Entire application flow
- **Dependencies:** Real or test environments
- **When:** Critical user workflows, happy paths

## Per-Project Testing Approaches

### GenAI (Python/Streamlit)

**Framework:** pytest

**Test Structure:**
```
GenAI/genAI/
├── tests/
│   ├── unit/
│   │   ├── test_instructions.py
│   │   └── test_data_processing.py
│   ├── integration/
│   │   └── test_streamlit_app.py
│   └── fixtures/
│       └── sample_data.py
```

**Testing Strategy:**
- Unit tests for data processing functions
- Integration tests for Streamlit components (using streamlit testing utilities)
- Mock user inputs for form testing
- Test JSON export functionality

**Coverage Goals:**
- Core logic: 80%+
- UI components: 60%+ (Streamlit testing is limited)

**Commands:**
```bash
cd GenAI/genAI
pytest tests/ -v --cov=. --cov-report=html
```

### Shiksha-Mitra (TypeScript/Next.js)

**Framework:** Jest + React Testing Library + Playwright (for E2E)

**Test Structure:**
```
Shiksha-Mitra/Shiksha-Mitra/
├── __tests__/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── src/
│   └── __tests__/
│       └── components/
```

**Testing Strategy:**
- Unit tests for utilities, hooks, and business logic
- Component tests with React Testing Library
- Integration tests for API routes
- E2E tests for critical user flows (login, course enrollment, etc.)

**Coverage Goals:**
- Components: 80%+
- API routes: 90%+
- Utilities: 100%
- E2E: Critical paths only

**Commands:**
```bash
cd Shiksha-Mitra/Shiksha-Mitra
npm test                    # Unit and integration
npm run test:e2e            # E2E tests
npm run test:coverage       # Coverage report
```

### OutLier-AI (Python)

**Framework:** pytest

**Test Structure:**
```
OutLier-AI/
├── tests/
│   ├── week1/
│   ├── week2/
│   └── ...
```

**Testing Strategy:**
- Unit tests for each script's functionality
- Test edge cases and error handling
- Test data processing and ML model outputs

**Coverage Goals:**
- Core scripts: 70%+ (learning project, lower priority)
- Critical algorithms: 90%+

**Commands:**
```bash
cd OutLier-AI
pytest tests/ -v
```

### MogoDb & new/mongodb-node-app (Node.js/MongoDB)

**Framework:** Jest + Supertest

**Test Structure:**
```
MogoDb/MogoDb/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
```

**Testing Strategy:**
- Unit tests for database operations (mocked)
- Integration tests with test MongoDB instance
- API endpoint tests
- Database connection and error handling tests

**Coverage Goals:**
- API endpoints: 80%+
- Database operations: 90%+
- Error handling: 100%

**Commands:**
```bash
cd MogoDb/MogoDb
npm test
npm run test:integration    # With test DB
```

### portfolio/ayush.me (React/Vite)

**Framework:** Vitest + React Testing Library

**Test Structure:**
```
portfolio/ayush.me/
├── src/
│   └── __tests__/
│       └── components/
└── tests/
    └── e2e/
```

**Testing Strategy:**
- Component tests for UI components
- Snapshot tests for visual regression
- E2E tests for navigation and interactions

**Coverage Goals:**
- Components: 70%+
- Critical user flows: 100%

**Commands:**
```bash
cd portfolio/ayush.me
npm test
npm run test:e2e
```

### iha-by-himani/IHA-art-studio (React)

**Framework:** Vitest + React Testing Library

**Testing Strategy:**
- Similar to portfolio project
- Component tests
- Integration tests for art-related features

**Coverage Goals:**
- Components: 70%+
- Core features: 80%+

## Test Data Management

### Fixtures and Factories
- Create reusable test fixtures
- Use factories for generating test data
- Keep test data realistic but minimal

### Test Isolation
- Each test should be independent
- Clean up after tests (database, files, etc.)
- No shared state between tests

### Mocking Strategy

**When to Mock:**
- External APIs
- Database operations (in unit tests)
- File system operations
- Network requests
- Time-dependent functions

**When NOT to Mock:**
- Your own code (unless testing integration)
- Simple utility functions
- Pure functions

## Test Execution

### Local Development
- Run tests before committing
- Run relevant tests during development
- Run full suite before pushing

### CI/CD Integration
- Run all tests on every commit
- Run faster tests first (unit before integration)
- Fail build if any tests fail
- Generate coverage reports

### Test Performance
- Keep unit tests fast (< 100ms each)
- Integration tests should complete in < 30 seconds
- E2E tests can be slower but should be < 2 minutes each

## Test Quality Standards

### Test Naming
- Descriptive names: `test_user_login_with_invalid_password_fails`
- Follow convention: `test_<scenario>_<expected_result>`
- Express intent clearly

### Test Structure (AAA Pattern)
```python
def test_calculate_total():
    # Arrange
    items = [Item(price=10), Item(price=20)]
    
    # Act
    total = calculate_total(items)
    
    # Assert
    assert total == 30
```

### What to Test

**Must Test:**
- Happy paths
- Edge cases (empty inputs, null values, boundaries)
- Error cases (invalid inputs, failures)
- Business logic
- Critical user flows

**Don't Test:**
- Framework code
- Third-party library code
- Trivial getters/setters
- Implementation details

## Continuous Testing

### Pre-Commit Hooks
- Run linter
- Run unit tests
- Check test coverage threshold

### CI/CD Pipeline
1. Install dependencies
2. Run linter
3. Run unit tests
4. Run integration tests
5. Run E2E tests (on main branch)
6. Generate coverage report
7. Fail if coverage below threshold

## Coverage Reporting

### Tools
- **Python:** pytest-cov
- **TypeScript/JavaScript:** Jest/Vitest coverage, Istanbul

### Reports
- HTML coverage reports
- Terminal output
- CI/CD integration

### Thresholds
- Overall: 80%
- Critical paths: 100%
- New code: 90%+ (enforced in CI)

## Test Maintenance

### Keep Tests Updated
- Update tests when code changes
- Refactor tests for readability
- Remove obsolete tests

### Test Performance
- Identify and fix slow tests
- Parallelize test execution
- Use test databases for integration tests

## Testing Checklist

Before considering code complete:
- [ ] Unit tests written for new functionality
- [ ] Edge cases tested
- [ ] Error cases tested
- [ ] Integration tests for component interactions
- [ ] All tests pass locally
- [ ] Tests are readable and maintainable
- [ ] Test names clearly describe what they test
- [ ] No flaky tests
- [ ] Test coverage meets project standards
- [ ] Tests run in CI/CD pipeline

## Future Improvements

1. **Unified Test Runner:** Script to run all project tests
2. **Shared Test Utilities:** Common testing helpers
3. **Visual Regression Testing:** For UI projects
4. **Performance Testing:** Load testing for APIs
5. **Security Testing:** Automated security scans

---

**Last Updated:** 2025-01-16
