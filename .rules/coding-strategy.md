# Coding Strategy — AI-Assisted Development Rules

## Core Principles

When writing or modifying code, follow these meta-strategies:

### 1. Understand Before Writing
- **Read existing code first**: Understand patterns, conventions, and architecture before writing new code
- **Infer intent**: Don't assume what code should do — analyze existing implementations and documentation
- **Follow established patterns**: Match the style and patterns already in use, unless there's a clear reason to deviate
- **Respect boundaries**: Understand module boundaries and don't create tight coupling

### 2. Code Quality First
- **Write self-documenting code**: Use clear names that express intent
- **Keep functions focused**: Single responsibility — one function, one purpose
- **Favor composition over inheritance**: Build complex behavior from simple components
- **Avoid premature optimization**: Write clear, correct code first; optimize only when needed and measured

### 3. DRY (Don't Repeat Yourself)
- **Detect duplication**: Before writing, check if similar functionality exists
- **Extract common logic**: Create reusable functions/modules for repeated patterns
- **Consolidate carefully**: Ensure extracted code serves all use cases correctly
- **Document abstractions**: If creating shared utilities, document their purpose and usage

### 4. SOLID Principles
- **Single Responsibility**: Each class/module should have one reason to change
- **Open/Closed**: Open for extension, closed for modification
- **Liskov Substitution**: Subtypes must be substitutable for their base types
- **Interface Segregation**: Create specific interfaces, not monolithic ones
- **Dependency Inversion**: Depend on abstractions, not concretions

### 5. Error Handling
- **Fail explicitly**: Don't silently ignore errors — handle or propagate them clearly
- **Use appropriate error types**: Create specific exceptions/errors for different failure modes
- **Log errors contextually**: Include relevant context (inputs, state) in error messages
- **Validate inputs early**: Check preconditions at function entry points

### 6. Configuration & Environment
- **No hardcoded values**: Use configuration files or environment variables for environment-specific values
- **Validate configuration**: Check required config values at startup
- **Provide sensible defaults**: Where possible, allow optional configuration with sensible defaults
- **Document configuration**: Clearly document what each configuration option does

### 7. Dependencies & Imports
- **Minimize dependencies**: Only add dependencies that are truly needed
- **Pin versions**: Use lock files to ensure reproducible builds
- **Keep dependencies updated**: Regularly check for security updates, but test thoroughly
- **Organize imports**: Group imports (stdlib, third-party, local) with clear separators

### 8. Performance Considerations
- **Measure before optimizing**: Profile code to find actual bottlenecks
- **Use appropriate data structures**: Choose data structures that match access patterns
- **Avoid premature abstraction**: Simple solutions are better than complex abstractions when performance matters
- **Consider caching**: Identify expensive operations that can be cached

### 9. Code Comments & Documentation
- **Comment why, not what**: Code should explain what it does; comments explain why
- **Document complex logic**: Explain algorithms, business rules, or non-obvious decisions
- **Keep comments updated**: Outdated comments are worse than no comments
- **Use docstrings/docs**: Follow language conventions for function/module documentation

### 10. Refactoring Strategy
- **Refactor in small steps**: Make incremental changes, test after each step
- **Preserve behavior**: Refactoring should not change functionality (verified by tests)
- **Remove dead code**: Delete unused functions, variables, and imports
- **Improve structure**: Simplify complex code, extract meaningful abstractions

### 11. Version Control Practices
- **Atomic commits**: Each commit should represent one logical change
- **Clear commit messages**: Describe what changed and why (not how)
- **Small, focused PRs**: Break large changes into smaller, reviewable pieces
- **Review your own code**: Before committing, review diffs to catch mistakes

### 12. Testing Mindset
- **Write testable code**: Structure code to enable unit testing
- **Test edge cases**: Consider boundary conditions, empty inputs, null handling
- **Test error paths**: Verify error handling and failure modes
- **Keep tests simple**: Tests should be easy to understand and maintain

### 13. Security Awareness
- **No secrets in code**: Never commit credentials, API keys, or secrets
- **Validate inputs**: Sanitize user inputs to prevent injection attacks
- **Use secure defaults**: Default to secure configurations
- **Keep dependencies updated**: Regularly check for known vulnerabilities

### 14. Language-Specific Practices
- **Follow language idioms**: Write idiomatic code for the language/framework
- **Use language features appropriately**: Leverage language-specific features (generators, async/await, etc.)
- **Follow style guides**: Adhere to established style guides (PEP 8, Google Style, etc.)
- **Use type hints/annotations**: Where supported, use type annotations for clarity

### 15. Collaboration & Maintainability
- **Write for future maintainers**: Code is read more often than written
- **Consider team conventions**: Follow team or project coding standards
- **Ask questions**: If unsure about requirements or approach, clarify before implementing
- **Review and iterate**: Code review is a learning opportunity

## Implementation Checklist

Before committing code, verify:
- [ ] Code follows project patterns and conventions
- [ ] No duplication of existing functionality
- [ ] Error handling is appropriate and tested
- [ ] No hardcoded configuration values
- [ ] Imports are organized and minimal
- [ ] Comments explain why, not what
- [ ] Tests pass and cover new functionality
- [ ] No secrets or sensitive data in code
- [ ] Code is readable and maintainable
- [ ] Commit message is clear and descriptive
