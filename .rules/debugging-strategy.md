# Debugging Strategy — Systematic Problem-Solving Rules

## Core Principles

When debugging issues, follow this systematic approach:

### 1. Understand the Problem
- **Reproduce consistently**: Can you reproduce the issue reliably? If not, gather more information
- **Understand expected behavior**: What should happen vs. what actually happens?
- **Gather context**: When does it occur? Under what conditions? What changed recently?
- **Check error messages**: Read error messages, stack traces, and logs carefully

### 2. Isolate the Issue
- **Minimize scope**: Identify the smallest unit that exhibits the problem
- **Remove variables**: Eliminate unnecessary complexity to isolate the root cause
- **Use bisection**: If a large change introduced the issue, use binary search to find the commit
- **Check dependencies**: Verify if the issue is in your code or in dependencies

### 3. Hypothesis Formation
- **Form specific hypotheses**: "X is causing Y" rather than "something is wrong"
- **Start with likely causes**: Common issues first (typos, null checks, off-by-one errors)
- **Consider recent changes**: What changed recently that could have caused this?
- **Think systematically**: Check inputs → processing → outputs

### 4. Evidence Gathering
- **Add logging**: Strategic logging at key points (inputs, outputs, decision points)
- **Use debuggers**: Step through code to observe actual behavior
- **Inspect state**: Check variable values, object properties, database state
- **Compare with working code**: If similar code works, compare implementations

### 5. Test Hypotheses
- **Create minimal test cases**: Reproduce the issue with the simplest possible input
- **Modify and observe**: Make one change at a time, observe the result
- **Use assertions**: Add assertions to verify your assumptions about state
- **Check edge cases**: Does the issue occur with edge cases or only specific inputs?

### 6. Root Cause Analysis
- **Find the root cause**: Fix the underlying issue, not just symptoms
- **Understand why it happened**: Was it a logic error, timing issue, configuration problem?
- **Consider design issues**: Is the bug a symptom of poor design that needs refactoring?
- **Document findings**: Record what the bug was and why it occurred

### 7. Fix Strategy
- **Fix correctly**: Ensure the fix addresses the root cause
- **Test the fix**: Verify the issue is resolved and no regressions introduced
- **Test edge cases**: Ensure the fix doesn't break other scenarios
- **Review the fix**: Is it the right solution, or a workaround?

### 8. Prevention
- **Add tests**: Write tests that would have caught this bug
- **Improve error handling**: If the bug was an unhandled case, improve error handling
- **Add validation**: Add input validation or preconditions if appropriate
- **Document gotchas**: If it's a subtle issue, document it for future reference

## Debugging Techniques by Type

### Logic Errors
1. **Trace execution**: Follow the code path step by step
2. **Check conditions**: Verify boolean expressions and comparisons
3. **Inspect variables**: Ensure variables have expected values
4. **Check operator precedence**: Verify operations execute in expected order

### Runtime Errors
1. **Read stack traces**: They show where the error occurred and the call chain
2. **Check null/undefined**: Common cause of runtime errors
3. **Verify types**: Ensure data types match expectations
4. **Check bounds**: Array/list access within valid ranges

### Performance Issues
1. **Profile the code**: Use profiling tools to find bottlenecks
2. **Measure, don't guess**: Time operations to identify slow parts
3. **Check algorithms**: Ensure appropriate algorithms for the problem size
4. **Inspect resource usage**: Memory, CPU, I/O operations

### Race Conditions / Timing Issues
1. **Identify shared state**: What data is accessed concurrently?
2. **Check synchronization**: Ensure proper locking/mutexes where needed
3. **Review async/await**: Verify async code handles timing correctly
4. **Test under load**: Some timing issues only appear under stress

### Integration Issues
1. **Verify APIs**: Ensure API calls match expected contracts
2. **Check data formats**: Verify request/response formats match expectations
3. **Test connectivity**: Can services reach each other?
4. **Review configuration**: Are endpoints, credentials, settings correct?

## Debugging Workflow

### Step 1: Reproduce
- Can you reproduce the issue consistently?
- What steps trigger the problem?
- What are the preconditions?

### Step 2: Gather Information
- Check error messages and logs
- Review recent changes (git history)
- Inspect current state (variables, database, files)

### Step 3: Form Hypothesis
- What could cause this behavior?
- What changed recently?
- What assumptions might be wrong?

### Step 4: Test Hypothesis
- Add logging or breakpoints
- Create a minimal test case
- Modify code to test assumptions

### Step 5: Identify Root Cause
- Is the fix addressing the symptom or the cause?
- Why did this bug occur?
- Is there a design issue that enabled it?

### Step 6: Fix
- Implement the correct fix
- Test that the issue is resolved
- Verify no regressions

### Step 7: Prevent Recurrence
- Add tests to catch this bug
- Improve error handling or validation
- Document the issue if it's subtle

## Debugging Tools & Techniques

### Logging
- Use appropriate log levels (debug, info, warn, error)
- Include context in log messages (inputs, state, IDs)
- Log at key decision points and state changes
- Remove or disable verbose logging in production

### Debuggers
- Learn to use your language's debugger effectively
- Set breakpoints at suspected problem areas
- Step through code to observe execution
- Inspect variable values and call stacks

### Unit Tests as Debugging Tools
- Write failing tests that reproduce the bug
- Use tests to isolate the issue
- Fix the code until tests pass
- Keep the test as regression prevention

### Code Review
- Sometimes a fresh pair of eyes sees the issue
- Explain the problem out loud (rubber duck debugging)
- Review code systematically (top to bottom, or by data flow)

## Common Pitfalls to Avoid

- **Fixing symptoms instead of causes**: Don't patch around the issue
- **Changing multiple things at once**: Makes it hard to identify what fixed it
- **Assuming without verifying**: Test your assumptions
- **Ignoring error messages**: They usually point to the problem
- **Not checking recent changes**: Bugs often introduced by recent modifications
- **Rushing to fix**: Take time to understand the problem first

## Debugging Checklist

Before considering a bug fixed:
- [ ] Issue is consistently reproducible (or root cause identified if intermittent)
- [ ] Root cause is identified, not just symptoms
- [ ] Fix addresses the root cause correctly
- [ ] Issue is resolved (tested in the scenario where it occurred)
- [ ] No regressions introduced (existing tests still pass)
- [ ] Edge cases handled (tested related scenarios)
- [ ] Tests added to prevent recurrence
- [ ] Fix is documented if the issue was subtle
- [ ] Code review completed if it's a significant change
