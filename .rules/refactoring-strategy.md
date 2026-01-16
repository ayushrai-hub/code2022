# Refactoring Strategy — Safe Code Improvement Guidelines

## Core Principles

Refactoring is improving code structure without changing behavior:

### 1. Refactoring vs. Rewriting
- **Refactoring**: Improves structure, preserves behavior — safe to do incrementally
- **Rewriting**: Changes behavior — requires careful planning and approval
- **When to refactor**: When code works but structure can be improved
- **When to rewrite**: When behavior needs to change significantly

### 2. Safety First
- **Tests are mandatory**: Never refactor without tests that verify behavior
- **Small, incremental steps**: Make one change at a time, test after each
- **Preserve behavior**: Refactoring should be behavior-preserving
- **Verify after each step**: Run tests to ensure nothing broke

### 3. When to Refactor

#### Code Smells (Signs You Should Refactor)
- **Duplication**: Same code appears in multiple places (DRY violation)
- **Long functions**: Functions longer than 20-50 lines (language dependent)
- **Large classes**: Classes with too many responsibilities
- **Deep nesting**: Too many levels of indentation (hard to follow)
- **Magic numbers**: Hardcoded values that should be named constants
- **Feature envy**: Function uses another object's data more than its own
- **Dead code**: Unused functions, variables, or imports

#### Triggers for Refactoring
- **Before adding features**: Clean code is easier to extend
- **After fixing bugs**: Improve code while you're already changing it
- **During code review**: Address review feedback through refactoring
- **Regular maintenance**: Dedicated refactoring sessions to reduce technical debt

### 4. Refactoring Techniques

#### Extract Function/Method
- **When**: A function does too much or a block of code has a clear purpose
- **How**: Move code into a new function with a descriptive name
- **Benefit**: Improves readability and reusability

#### Extract Variable
- **When**: A complex expression is hard to understand
- **How**: Store expression result in a well-named variable
- **Benefit**: Makes code self-documenting

#### Rename Variable/Function
- **When**: Name doesn't clearly express purpose
- **How**: Rename to better reflect what it does
- **Benefit**: Improves code readability

#### Eliminate Duplication
- **When**: Same code appears in multiple places
- **How**: Extract common code into shared function/module
- **Benefit**: Single source of truth, easier to maintain

#### Simplify Conditionals
- **When**: Complex if/else or nested conditionals
- **How**: Extract conditions to named functions, use early returns
- **Benefit**: Easier to understand and test

#### Break Large Classes
- **When**: Class has too many responsibilities
- **How**: Extract related functionality into separate classes
- **Benefit**: Single Responsibility Principle, easier to test

#### Move Code
- **When**: Code is in the wrong place (wrong class/module)
- **How**: Move to appropriate location where it logically belongs
- **Benefit**: Better organization and cohesion

### 5. Refactoring Workflow

#### Step 1: Understand Current Code
- Read the code carefully
- Understand what it does (behavior, not implementation)
- Identify dependencies and side effects
- Note any edge cases or special handling

#### Step 2: Write/Verify Tests
- **Critical**: Ensure existing tests cover current behavior
- If tests are missing, write them first
- Verify tests pass (this establishes baseline)
- Tests will catch regressions during refactoring

#### Step 3: Make Small Change
- Make one refactoring step at a time
- Keep changes small and focused
- Don't mix refactoring with feature changes

#### Step 4: Run Tests
- Run all tests after each change
- Fix any failures immediately
- Don't proceed if tests fail

#### Step 5: Commit (Optional)
- Commit after each successful refactoring step
- Makes it easy to revert if something goes wrong
- Clear history of improvements

#### Step 6: Repeat
- Continue with next refactoring step
- Test after each change
- Stop when code is clean enough

### 6. Refactoring Safety Practices

#### Incremental Changes
- **One change at a time**: Don't refactor multiple things simultaneously
- **Test frequently**: Run tests after every small change
- **Revert if broken**: If tests fail, revert and try a different approach

#### Preserve Behavior
- **Don't change functionality**: Refactoring is structural only
- **Verify output**: Ensure output is identical before and after
- **Check edge cases**: Verify edge cases still work correctly

#### Use Version Control
- **Commit frequently**: Small commits make it easy to revert
- **Clear commit messages**: Describe what was refactored and why
- **Review changes**: Look at diffs to catch unintended changes

### 7. Common Refactoring Patterns

#### Extract Method
```python
# Before
def process_order(order):
    total = 0
    for item in order.items:
        price = item.price * item.quantity
        if item.discount:
            price = price * (1 - item.discount)
        total += price
    # ... rest of function

# After
def calculate_item_total(item):
    price = item.price * item.quantity
    if item.discount:
        price = price * (1 - item.discount)
    return price

def process_order(order):
    total = sum(calculate_item_total(item) for item in order.items)
    # ... rest of function
```

#### Extract Variable
```javascript
// Before
if (user.age >= 18 && user.age <= 65 && user.status === 'active') {
    // ...
}

// After
const isWorkingAge = user.age >= 18 && user.age <= 65;
const isActiveUser = user.status === 'active';
if (isWorkingAge && isActiveUser) {
    // ...
}
```

#### Early Return
```python
# Before
def process_user(user):
    if user is not None:
        if user.is_active:
            if user.has_permission:
                # actual logic here

# After
def process_user(user):
    if user is None:
        return
    if not user.is_active:
        return
    if not user.has_permission:
        return
    # actual logic here
```

### 8. Refactoring Pitfalls to Avoid

- **Refactoring without tests**: Guaranteed way to introduce bugs
- **Changing behavior while refactoring**: Keep refactoring and feature changes separate
- **Too large refactoring steps**: Small steps are safer
- **Refactoring everything at once**: Focus on one area at a time
- **Ignoring test failures**: Fix failing tests immediately, don't proceed
- **No rollback plan**: Know how to revert if something goes wrong

### 9. When NOT to Refactor

- **Close to deadline**: Refactoring can introduce unexpected issues
- **No tests**: Don't refactor untested code without adding tests first
- **Unclear requirements**: Understand what code should do before changing structure
- **Large architectural changes**: That's rewriting, not refactoring

### 10. Measuring Refactoring Success

#### Before Refactoring
- Note current issues: duplication, complexity, maintainability concerns
- Measure code metrics if available: cyclomatic complexity, duplication percentage

#### After Refactoring
- **Tests still pass**: Critical — behavior is preserved
- **Code is more readable**: Easier to understand
- **Less duplication**: DRY principles followed
- **Easier to extend**: New features are easier to add
- **No regressions**: Existing functionality still works

## Refactoring Checklist

Before starting refactoring:
- [ ] Current code is understood (behavior and purpose)
- [ ] Tests exist and pass (establish baseline)
- [ ] Refactoring goal is clear (what improvement to make)
- [ ] Changes are isolated (won't affect other systems)

During refactoring:
- [ ] Making small, incremental changes
- [ ] Running tests after each change
- [ ] Tests continue to pass
- [ ] Behavior is preserved (output identical)

After refactoring:
- [ ] All tests pass
- [ ] Code is more readable/maintainable
- [ ] No duplication introduced
- [ ] Changes are committed with clear messages
- [ ] Documentation updated if necessary
