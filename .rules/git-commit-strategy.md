# Git Commit Strategy — Version Control Best Practices

## Core Principles

Good commit practices make project history clear and maintainable:

### 1. Atomic Commits
- **One logical change per commit**: Each commit should represent one complete thought or change
- **Related changes together**: Don't split related changes across multiple commits
- **Unrelated changes separate**: Don't mix unrelated changes in one commit
- **Complete and working**: Each commit should leave the codebase in a working state

### 2. Clear Commit Messages
- **Descriptive subject line**: Summarize what changed in 50-72 characters
- **Imperative mood**: "Add feature" not "Added feature" or "Adds feature"
- **Body explains why**: When needed, explain why the change was made
- **Reference issues**: Link to issues, tickets, or discussions when relevant

### 3. Commit Message Format

#### Standard Format
```
Short summary (50 chars or less)

More detailed explanation, if needed. Wrap at 72 characters.
Explain what and why, not how.

- Bullet points are OK
- For multiple related changes
- Use present tense

Fixes #123
```

#### Examples of Good Commits
```
Add user authentication endpoint

Implements POST /api/auth/login endpoint with JWT token generation.
Includes validation for email/password format and rate limiting.

- Validates credentials against database
- Returns JWT token on success
- Returns 401 on invalid credentials
- Rate limits to 5 requests per minute

Fixes #45
```

```
Fix memory leak in image processing

The image resize function was not releasing memory after processing.
This caused memory usage to grow continuously during batch operations.

The fix ensures proper cleanup of temporary buffers after each image.

Fixes #78
```

### 4. What Makes a Good Commit

#### Good Commits:
- **Focused**: One clear purpose or change
- **Working**: Code compiles and tests pass
- **Self-contained**: Commit makes sense on its own
- **Well-described**: Message explains what and why

#### Bad Commits:
- **Too large**: "Refactor entire authentication system" (should be split)
- **Too vague**: "Fix stuff" or "Update code"
- **Broken**: Commit that doesn't compile or breaks tests
- **Mixed concerns**: "Add feature X and fix bug Y and update docs"

### 5. Commit Frequency

#### When to Commit
- **After completing a logical unit of work**: Feature, bug fix, refactoring
- **Before leaving work**: Save progress at end of day
- **After passing tests**: Only commit working code
- **Before major refactoring**: Commit stable state before risky changes

#### When NOT to Commit
- **Work in progress**: Don't commit broken or incomplete code
- **Every single line change**: Group related changes together
- **With failing tests**: Fix tests before committing
- **Mixed concerns**: Separate different types of changes

### 6. Commit Size Guidelines

#### Small Commits (Preferred)
- Single bug fix
- One feature addition
- One refactoring step
- Documentation update
- **Benefits**: Easy to review, easy to revert, clear history

#### Medium Commits (Acceptable)
- Related feature additions
- Complete refactoring of one module
- **When appropriate**: When changes are logically related

#### Large Commits (Avoid)
- Multiple unrelated features
- Entire system refactoring
- **Problems**: Hard to review, hard to revert, unclear history

### 7. Commit Best Practices

#### Before Committing
- **Review your changes**: Use `git diff` to see what you're committing
- **Run tests**: Ensure all tests pass
- **Check formatting**: Apply consistent formatting
- **Remove debug code**: Don't commit `console.log`, `debugger`, temporary files

#### During Commit
- **Stage related changes**: Use `git add -p` to selectively stage changes
- **Write clear message**: Take time to write a good commit message
- **Verify commit**: Review what will be committed

#### After Committing
- **Verify commit looks good**: `git show` to review the commit
- **Push when ready**: Push after completing a logical set of changes

### 8. Branching Strategy

#### Feature Branches
- **One feature per branch**: Keep branches focused
- **Descriptive names**: `feature/user-authentication`, `bugfix/memory-leak`
- **Keep branches short-lived**: Merge promptly after feature is complete

#### Commit on Branch
- **Commit to feature branch**: Don't commit directly to main/master
- **Regular commits**: Commit often on your feature branch
- **Squash before merge**: Consider squashing commits before merging

### 9. Commit History Maintenance

#### Clean History
- **Logical progression**: History tells a story of development
- **Easy to review**: Others can understand what changed and why
- **Easy to revert**: Can revert specific changes without side effects
- **Useful for debugging**: `git blame` and `git bisect` are more effective

#### Interactive Rebase (Advanced)
- **Clean up before pushing**: Use `git rebase -i` to clean up commits
- **Squash related commits**: Combine small related commits
- **Reword messages**: Fix typos or improve clarity
- **Reorder commits**: Put commits in logical order

### 10. Commit Message Guidelines

#### Subject Line Rules
- **50 characters or less**: Short and focused
- **Capitalize first letter**: "Add feature" not "add feature"
- **No period at end**: "Fix bug" not "Fix bug."
- **Imperative mood**: "Add" not "Added" or "Adds"

#### Body Rules (When Needed)
- **Separate from subject**: Blank line between subject and body
- **Wrap at 72 characters**: Easier to read in terminals
- **Explain why**: Focus on motivation, not implementation details
- **Use present tense**: "This change adds..." not "This change added..."

#### Common Prefixes
- `Add`: New feature
- `Fix`: Bug fix
- `Update`: Change to existing feature
- `Remove`: Delete feature or code
- `Refactor`: Code improvement without behavior change
- `Docs`: Documentation changes
- `Test`: Test additions or changes
- `Style`: Code style/formatting changes
- `Chore`: Maintenance tasks

### 11. Commit Message Anti-Patterns

#### Avoid These:
- **"WIP"**: Work in progress shouldn't be committed
- **"Fix typo"**: Too vague — what typo?
- **"Update"**: Update what?
- **"Misc changes"**: Be specific
- **Emoji-only**: Use words, emoji can be supplementary
- **All caps**: "FIX BUG" is harder to read
- **No message**: Always write a message

### 12. Commit Checklist

Before committing:
- [ ] Changes are complete and working
- [ ] Tests pass
- [ ] Code is formatted consistently
- [ ] Debug code removed
- [ ] Changes reviewed with `git diff`
- [ ] Commit message is clear and descriptive
- [ ] Commit is atomic (one logical change)
- [ ] Related files staged together

After committing:
- [ ] Commit looks good (`git show`)
- [ ] Ready to push or continue working
- [ ] Commit message follows conventions

## Git Workflow Example

### Typical Workflow
```bash
# Start working on a feature
git checkout -b feature/new-feature

# Make changes, test, commit incrementally
git add file1.py
git commit -m "Add helper function for data validation"

git add file2.py
git commit -m "Implement feature X using helper function"

git add tests/test_feature.py
git commit -m "Add tests for feature X"

# Review and clean up before pushing
git log --oneline  # Review commits
git rebase -i HEAD~3  # Optionally squash/reword

# Push when feature is complete
git push origin feature/new-feature
```

### Cleanup Before Merge
```bash
# Review commits
git log --oneline

# Interactive rebase to clean up
git rebase -i main

# Squash related commits, reword messages
# Push cleaned history
git push --force-with-lease origin feature/new-feature
```

## Final Guidelines

- **Commit often**: Small, frequent commits are better than large, infrequent ones
- **Write good messages**: Future you (and others) will thank you
- **Keep history clean**: Makes debugging and code review easier
- **Review before committing**: Check what you're committing
- **Test before committing**: Don't commit broken code
