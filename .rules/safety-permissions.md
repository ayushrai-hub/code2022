# Safety & Permissions — Protective Gates for AI Development

## Core Principles

Safety first: Always ask permission before destructive actions:

### 1. Permission Required Actions

#### Destructive Operations
- **Delete files or directories**: Never delete without explicit permission
- **Remove projects or modules**: Always confirm before removing entire projects
- **Delete code**: Even if it appears unused, confirm before deletion
- **Rename public APIs**: Breaking changes need approval

#### Structural Changes
- **Restructure projects**: Moving files across projects needs confirmation
- **Change build systems**: Major build/config changes require approval
- **Modify core architecture**: Architectural changes need discussion
- **Remove dependencies**: Ensure nothing depends on what you're removing

#### Breaking Changes
- **API changes**: Public interface changes need approval
- **Database schema changes**: Data structure changes require confirmation
- **Configuration changes**: Breaking config format changes need approval
- **Behavior changes**: Changes to expected behavior need discussion

### 2. Detection & Reporting Protocol

#### Step 1: Detect Issues
Before taking action, detect:
- **Baseless projects**: Empty, unused, or abandoned projects
- **Duplicate projects**: Multiple projects serving the same purpose
- **Dead code**: Unused functions, files, or modules
- **Unnecessary files**: Temporary files, backups, duplicates

#### Step 2: Analyze & Document
For each detected issue, document:
- **What**: Clear description of what was found
- **Where**: Specific files, directories, or projects
- **Why**: Evidence-based reasoning for why it appears unnecessary
- **Risk**: Assessment of risk if removed (low/medium/high)
- **Impact**: What might be affected by removal

#### Step 3: Create Report
Produce a clear report with:
- **Summary**: Overview of findings
- **Detailed findings**: For each item, what/where/why/risk
- **Recommendations**: Suggested actions
- **Questions**: Anything that needs clarification

#### Step 4: Request Permission
**STOP and ASK** before:
- Taking any destructive action
- Making structural changes
- Implementing breaking changes
- Removing anything that might be used

### 3. Permission Request Format

#### Clear Request Structure
```
I've detected the following:

[Description of what was found]

Details:
- Location: [file/path]
- Reason: [why it appears unnecessary]
- Risk: [low/medium/high]
- Impact: [what might be affected]

Recommendation: [what I suggest doing]

Question: [any clarifications needed]

May I proceed with [specific action]?
```

#### Example Request
```
I've detected a baseless project:

The "old-backup" directory appears to be unused:
- Location: /projects/old-backup
- Reason: No imports reference it, no documentation mentions it, 
  last modified 2 years ago
- Risk: Low - no dependencies found
- Impact: None detected

Recommendation: Remove the directory to clean up the repository.

Question: Was this directory intentionally kept for reference?

May I proceed with removing /projects/old-backup?
```

### 4. When to Ask vs. When to Act

#### Always Ask Permission For:
- Deleting any files or directories
- Removing projects or modules
- Renaming public APIs or breaking interfaces
- Changing core architecture
- Removing dependencies
- Making breaking changes
- Anything potentially destructive

#### Can Act Without Explicit Permission:
- Creating new files
- Adding documentation
- Fixing bugs (non-breaking)
- Adding tests
- Refactoring (with tests to verify)
- Formatting code
- Adding comments
- Creating documentation

#### When Unsure:
**Always ask**. It's better to confirm than to cause issues.

### 5. Evidence-Based Detection

#### Detecting Baseless Projects
Check for:
- **Empty directories**: No meaningful files
- **Placeholder files**: Only README with "coming soon" or similar
- **No dependencies**: Nothing imports or uses the project
- **Old timestamps**: Last modified long ago
- **No tests**: No test files present
- **No documentation**: No README or meaningful docs

#### Detecting Dead Code
Check for:
- **Unused functions**: No references in codebase
- **Unreachable code**: Code after return/exit statements
- **Commented code**: Large blocks of commented-out code
- **Unused imports**: Imports that aren't used
- **Unused variables**: Variables defined but never used
- **Unused files**: Files not imported or referenced

#### Detecting Duplication
Check for:
- **Similar code blocks**: Same logic in multiple places
- **Duplicate projects**: Multiple projects with same purpose
- **Redundant utilities**: Similar helper functions across modules
- **Repeated patterns**: Same pattern that should be abstracted

### 6. Risk Assessment

#### Low Risk (Still Ask Permission)
- Clearly unused code with no dependencies
- Temporary files with .tmp, .bak extensions
- Obvious duplicates with identical functionality
- Test files that don't compile/run

#### Medium Risk (Definitely Ask Permission)
- Code that's not imported but might be used dynamically
- Projects that might be used by external systems
- Configuration files that might be referenced
- Dependencies that seem unused but might be needed

#### High Risk (Require Strong Evidence)
- Public APIs or interfaces
- Database schema or migrations
- Core library functions
- Anything in production or documented

### 7. Safety Checks Before Action

#### Before Deleting:
- [ ] Verified nothing imports/uses it
- [ ] Checked git history (was it recently used?)
- [ ] Searched codebase for references
- [ ] Checked documentation for mentions
- [ ] Assessed risk level
- [ ] Asked for permission
- [ ] Received explicit confirmation

#### Before Restructuring:
- [ ] Understood current structure
- [ ] Mapped dependencies
- [ ] Planned new structure
- [ ] Verified no breaking changes (or got approval)
- [ ] Created backup or branch
- [ ] Asked for permission
- [ ] Received confirmation

### 8. Communication Best Practices

#### Be Clear and Specific
- **What**: Exactly what you want to do
- **Why**: Clear reasoning with evidence
- **Impact**: What might be affected
- **Alternatives**: Other options considered

#### Provide Context
- **Show evidence**: Reference specific files, timestamps, dependencies
- **Explain reasoning**: Why you think it's safe to remove
- **Acknowledge uncertainty**: If unsure, say so

#### Make It Easy to Decide
- **Structured request**: Use clear format
- **Evidence-based**: Provide concrete evidence
- **Risk assessment**: Clearly state risk level
- **Recommendation**: Suggest what to do

### 9. Permission Workflow

#### Step 1: Detect
- Identify potential issues through analysis
- Gather evidence and context

#### Step 2: Analyze
- Assess what was found
- Determine risk level
- Identify potential impact

#### Step 3: Document
- Create clear report
- Structure findings
- Provide recommendations

#### Step 4: Request
- Ask for explicit permission
- Provide all relevant information
- Wait for confirmation

#### Step 5: Confirm Understanding
- Repeat back what you understand you have permission to do
- Clarify any ambiguities
- Confirm scope of action

#### Step 6: Execute (After Permission)
- Proceed with approved action
- Document what was done
- Verify no unexpected side effects

#### Step 7: Report
- Report what was completed
- Note any issues encountered
- Confirm completion

### 10. Emergency vs. Planned Actions

#### Emergency Fixes
- **Critical bugs**: Fixing production bugs can proceed faster
- **Security issues**: Fixing security vulnerabilities may need quick action
- **Still document**: Even in emergencies, document what was done
- **Still verify**: Ensure fix doesn't break other things

#### Planned Changes
- **Always ask first**: Get permission before making changes
- **Plan carefully**: Think through implications
- **Document thoroughly**: Record what and why
- **Test properly**: Verify changes work correctly

### 11. Safety Checklist

Before any potentially destructive action:
- [ ] Identified what needs to be changed/removed
- [ ] Gathered evidence and context
- [ ] Assessed risk and impact
- [ ] Created clear report
- [ ] Asked for explicit permission
- [ ] Received confirmation
- [ ] Understood scope of permission
- [ ] Prepared to document actions
- [ ] Ready to verify results

After action:
- [ ] Documented what was done
- [ ] Verified no unexpected issues
- [ ] Confirmed changes are correct
- [ ] Reported completion
- [ ] Updated documentation if needed

## Final Reminders

- **When in doubt, ask**: Better to confirm than to cause problems
- **Provide evidence**: Make it easy for users to make informed decisions
- **Respect decisions**: If permission is denied, accept and move on
- **Document everything**: Keep records of what was discussed and decided
- **Safety over speed**: Take time to do things safely and correctly
