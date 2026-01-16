# Design Decisions

This document records important design decisions made across the projects in this repository.

## Repository Structure

### Decision: Independent Projects vs. Monorepo

**Decision:** Keep projects as independent directories rather than a true monorepo.

**Rationale:**
- Projects serve different purposes and have different requirements
- Different technology stacks (Python vs. Node.js)
- Independent deployment cycles
- Simpler dependency management per project
- Easier for different developers/teams to work on different projects

**Alternatives Considered:**
- True monorepo with shared tooling (rejected - too complex for unrelated projects)
- Separate repositories (rejected - want to keep related work together)

**Trade-offs:**
- ✅ Simpler per-project management
- ✅ Independent versioning and releases
- ❌ No shared utilities or common code
- ❌ No unified CI/CD (currently)

**Status:** Current approach, may be reconsidered if projects grow and share more code.

---

## Technology Choices

### GenAI: Streamlit for Web Interface

**Decision:** Use Streamlit for the GenAI evaluation tool.

**Rationale:**
- Rapid prototyping and development
- Built-in form handling and state management
- Python-native (matches project language)
- Easy deployment

**Alternatives Considered:**
- Flask/FastAPI + React (rejected - more complex, slower development)
- Django (rejected - overkill for this use case)

**Trade-offs:**
- ✅ Fast development
- ✅ Simple deployment
- ❌ Less customization than custom frontend
- ❌ Performance limitations for complex UIs

---

### Shiksha-Mitra: Next.js for Full-Stack

**Decision:** Use Next.js for the Shiksha-Mitra educational platform.

**Rationale:**
- Full-stack framework (frontend + API routes)
- Server-side rendering for SEO
- TypeScript support
- Large ecosystem and community
- Good for educational/content platforms

**Alternatives Considered:**
- Separate React frontend + Express backend (rejected - more complex deployment)
- Django (rejected - team prefers TypeScript/JavaScript)

**Trade-offs:**
- ✅ Unified codebase
- ✅ Good SEO capabilities
- ✅ Modern React features
- ❌ Learning curve for Next.js App Router
- ❌ Vendor lock-in to Vercel (if using Vercel deployment)

---

## Project Organization

### Decision: Nested Directory Structure

**Decision:** Some projects have nested directories (e.g., `Shiksha-Mitra/Shiksha-Mitra/`).

**Rationale:**
- Projects may have been cloned/moved from other locations
- Maintains original project structure
- Some projects may be git submodules

**Alternatives Considered:**
- Flatten all structures (rejected - may break project-specific tooling)

**Trade-offs:**
- ✅ Preserves original project structure
- ✅ Works with existing tooling
- ❌ Inconsistent structure across projects
- ❌ Slightly confusing navigation

**Status:** Acceptable for now, could be improved in future refactoring.

---

## Documentation Strategy

### Decision: Centralized DOCS Directory + Per-Project READMEs

**Decision:** Create centralized DOCS directory for architecture-level documentation, plus per-project READMEs.

**Rationale:**
- Centralized docs for cross-project concerns
- Per-project docs for project-specific information
- Follows mega prompt requirements

**Alternatives Considered:**
- Only per-project docs (rejected - need cross-project documentation)
- Only centralized docs (rejected - projects need individual documentation)

**Trade-offs:**
- ✅ Clear separation of concerns
- ✅ Easy to find project-specific info
- ✅ Centralized architecture documentation
- ❌ Some duplication possible

---

## Testing Strategy

### Decision: Per-Project Testing (No Unified Framework)

**Decision:** Each project uses its own testing framework and approach.

**Rationale:**
- Different languages require different testing tools
- Python projects use pytest
- Node.js projects use Jest/Vitest
- No need for unified approach for independent projects

**Alternatives Considered:**
- Unified testing framework (rejected - impractical for different languages)

**Trade-offs:**
- ✅ Use best tool for each language
- ✅ No unnecessary abstraction
- ❌ No unified testing standards
- ❌ Can't run all tests from root

**Future Consideration:** Could add unified test runner script that delegates to each project.

---

## Dependency Management

### Decision: Independent Dependency Management

**Decision:** Each project manages its own dependencies independently.

**Rationale:**
- Projects are independent
- Different languages use different package managers
- No shared code means no shared dependencies

**Alternatives Considered:**
- Unified dependency management (rejected - not applicable for independent projects)

**Trade-offs:**
- ✅ Simple and clear
- ✅ No dependency conflicts between projects
- ❌ No shared dependency versioning
- ❌ More disk space (duplicate dependencies)

---

## Git Strategy

### Decision: Mixed Git Structure (Some Projects Have Own Repos)

**Decision:** Some projects (e.g., Shiksha-Mitra) have their own .git directories.

**Rationale:**
- Projects may have been developed separately
- Some may be git submodules
- Maintains project history

**Alternatives Considered:**
- Single git repository (rejected - would lose project histories)
- All as submodules (rejected - not all projects need this)

**Trade-offs:**
- ✅ Preserves project histories
- ✅ Projects can be developed independently
- ❌ More complex git operations
- ❌ Inconsistent structure

---

## Security Decisions

### Decision: Environment Variables for Secrets

**Decision:** Use environment variables for all secrets and configuration.

**Rationale:**
- Standard practice
- Prevents secrets in code
- Easy to manage per environment

**Implementation:**
- .env files (not committed)
- .env.example files (committed as templates)
- Documented in each project's README

**Alternatives Considered:**
- Secrets management service (considered for future, not needed now)
- Hardcoded configs (rejected - security risk)

---

## Code Quality

### Decision: AI-Assisted Development Rules in .rules Directory

**Decision:** Create comprehensive .rules directory with development guidelines.

**Rationale:**
- Provides consistent development practices
- Helps AI assistants understand project standards
- Documents best practices

**Content:**
- Coding strategy
- Testing strategy
- Refactoring strategy
- Debugging strategy
- Git commit strategy
- Safety & permissions

**Trade-offs:**
- ✅ Clear guidelines
- ✅ Consistent development
- ❌ Requires maintenance
- ❌ May be ignored if not enforced

---

## Future Considerations

### Potential Future Decisions

1. **CI/CD:** Should we add unified CI/CD or keep per-project?
2. **Shared Utilities:** If common patterns emerge, should we extract shared packages?
3. **Documentation:** Should we add API documentation generation?
4. **Testing:** Should we add unified test runner?
5. **Deployment:** Should we standardize deployment approach?

---

**Last Updated:** 2025-01-16
