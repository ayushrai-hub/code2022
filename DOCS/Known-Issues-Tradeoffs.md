# Known Issues & Tradeoffs

## Current Limitations

### Repository Structure

#### Issue: Inconsistent Directory Structure
**Description:** Some projects have nested directories (e.g., `Shiksha-Mitra/Shiksha-Mitra/`), while others are flat.

**Impact:** 
- Confusing navigation
- Inconsistent developer experience
- May indicate projects were moved/cloned from other locations

**Workaround:** Document structure in README files

**Status:** Known issue, low priority

---

#### Issue: Empty/Unnecessary Directories
**Description:** 
- `TDS/` directory is empty
- `DSA/` only contains .venv (no source code)
- `IHA/` and `ayush-work/` only show node_modules (source code may be deeper)

**Impact:**
- Repository clutter
- Confusion about which directories are active projects

**Workaround:** Document which directories are active

**Status:** Needs user confirmation before cleanup

---

### Documentation

#### Issue: Missing Project READMEs
**Description:** Most projects lack comprehensive README files with setup instructions, usage examples, and API documentation.

**Impact:**
- Difficult for new developers to get started
- Unclear how to run and test projects
- Missing documentation of project purposes

**Workaround:** Created root README, but per-project READMEs needed

**Status:** Being addressed in current audit

---

#### Issue: Incomplete Documentation
**Description:** Some projects (like Shiksha-Mitra) have extensive documentation in MarkdownDocsa, but it's not organized as standard README.

**Impact:**
- Documentation exists but is hard to find
- Not following standard project structure

**Workaround:** Link to documentation from README

**Status:** Can be improved

---

### Testing

#### Issue: Missing or Incomplete Tests
**Description:** Most projects lack comprehensive test coverage.

**Impact:**
- Risk of regressions
- Difficult to refactor safely
- No confidence in code changes

**Workaround:** Manual testing (not scalable)

**Status:** Critical issue, needs addressing

---

#### Issue: No Unified Test Runner
**Description:** Each project has its own test setup, no way to run all tests from root.

**Impact:**
- Can't easily verify entire repository
- No unified test reporting

**Workaround:** Run tests per project

**Status:** Low priority, nice to have

---

### Build & Deployment

#### Issue: No CI/CD Configuration
**Description:** No GitHub Actions, GitLab CI, or other CI/CD pipelines configured.

**Impact:**
- No automated testing on commits
- No automated deployment
- Manual quality checks

**Workaround:** Manual testing and deployment

**Status:** Should be added for production projects

---

#### Issue: No Build Scripts at Root
**Description:** No unified way to build/run all projects from root level.

**Impact:**
- Each project must be built/run individually
- No unified development workflow

**Workaround:** Document per-project commands

**Status:** Low priority (projects are independent)

---

### Dependencies

#### Issue: Virtual Environments and node_modules in Repository
**Description:** Some virtual environments (.venv, myenv) and node_modules may be tracked in git (though .gitignore should prevent this).

**Impact:**
- Large repository size
- Platform-specific files
- Unnecessary version control

**Workaround:** .gitignore should exclude these (created in audit)

**Status:** Should be verified

---

#### Issue: External Toolchain in Repository
**Description:** `mingw/` directory contains external C/C++ toolchain.

**Impact:**
- Very large directory
- Should not be in repository
- Platform-specific

**Workaround:** Should be in .gitignore or removed

**Status:** Needs user confirmation

---

### Code Quality

#### Issue: Inconsistent Code Style
**Description:** No unified code formatting or linting configuration across projects.

**Impact:**
- Inconsistent code style
- Harder code reviews
- Different standards per project

**Workaround:** Each project may have its own config

**Status:** Acceptable for independent projects

---

#### Issue: Missing Type Definitions
**Description:** Some TypeScript projects may have incomplete type definitions.

**Impact:**
- Type safety issues
- Potential runtime errors

**Workaround:** Use `any` types (not ideal)

**Status:** Should be addressed per project

---

### Security

#### Issue: Potential Secrets in Code
**Description:** Need to verify no API keys, passwords, or secrets are committed.

**Impact:**
- Security risk
- Credential exposure

**Workaround:** .env files and .gitignore

**Status:** Should be audited

---

#### Issue: No Security Scanning
**Description:** No automated dependency vulnerability scanning.

**Impact:**
- Potential security vulnerabilities in dependencies
- No awareness of outdated packages

**Workaround:** Manual checking

**Status:** Should add automated scanning

---

## Technical Debt

### High Priority

1. **Add comprehensive tests** to all projects
2. **Create per-project READMEs** with setup instructions
3. **Verify .gitignore** is working correctly
4. **Remove unnecessary directories** (with user confirmation)
5. **Add CI/CD** for production projects

### Medium Priority

1. **Standardize project structure** (if possible)
2. **Add unified test runner** script
3. **Improve documentation organization**
4. **Add code formatting/linting** configuration
5. **Security audit** for secrets and vulnerabilities

### Low Priority

1. **Unified build scripts** (if needed)
2. **Shared utilities** (if patterns emerge)
3. **Performance optimization** (as needed)
4. **Visual regression testing** (for UI projects)

---

## Tradeoffs

### Independent Projects vs. Monorepo

**Tradeoff:** Keeping projects independent vs. creating a true monorepo.

**Chosen:** Independent projects

**Benefits:**
- Simpler per-project management
- Independent versioning
- No dependency conflicts
- Easier for different teams

**Costs:**
- No shared code
- No unified tooling
- More duplication
- Inconsistent structure

**Status:** Acceptable tradeoff for current needs

---

### Documentation Location

**Tradeoff:** Centralized docs vs. per-project docs.

**Chosen:** Both (DOCS directory + per-project READMEs)

**Benefits:**
- Cross-project documentation in one place
- Project-specific docs where needed
- Clear organization

**Costs:**
- Some duplication possible
- Need to maintain both

**Status:** Good balance

---

### Testing Approach

**Tradeoff:** Unified testing framework vs. per-project frameworks.

**Chosen:** Per-project frameworks (pytest for Python, Jest/Vitest for JS/TS)

**Benefits:**
- Best tool for each language
- No unnecessary abstraction
- Language-native tools

**Costs:**
- No unified test runner
- Different standards
- Can't run all tests easily

**Status:** Correct choice for different languages

---

### Git Structure

**Tradeoff:** Single repo vs. multiple repos vs. submodules.

**Current:** Mixed (some projects have own .git)

**Benefits:**
- Preserves project histories
- Independent development

**Costs:**
- Complex git operations
- Inconsistent structure

**Status:** Acceptable, but could be improved

---

## Performance Considerations

### Repository Size
- **Issue:** Large repository due to node_modules, .venv, mingw
- **Impact:** Slow clones, large disk usage
- **Mitigation:** .gitignore should exclude these

### Build Times
- **Issue:** No unified build, each project builds separately
- **Impact:** Slower overall development workflow
- **Mitigation:** Acceptable for independent projects

### Test Execution
- **Issue:** Tests run per-project, no parallel execution across projects
- **Impact:** Slower full repository testing
- **Mitigation:** Could add unified test runner script

---

## Security Considerations

### Dependency Vulnerabilities
- **Risk:** Outdated dependencies may have security vulnerabilities
- **Mitigation:** Regular dependency updates, automated scanning

### Secrets Management
- **Risk:** Secrets may be committed accidentally
- **Mitigation:** .env files, .gitignore, pre-commit hooks

### Authentication
- **Risk:** Projects with authentication need secure implementation
- **Mitigation:** Follow best practices (JWT, OAuth, secure password hashing)

---

## Future Considerations

### Scalability
- Current structure works for small to medium projects
- May need reorganization if projects grow significantly
- Consider monorepo if projects start sharing code

### Maintenance
- Need regular dependency updates
- Need to keep documentation updated
- Need to maintain test coverage

### Team Collaboration
- Current structure works for independent development
- May need more coordination if projects become interdependent
- Documentation is key for collaboration

---

**Last Updated:** 2025-01-16
