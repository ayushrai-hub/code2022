# 🤖 AI_Code.md — AI-Assisted Development Standards for Shiksha-Mitra

This document defines **best practices, workflows, and guardrails** for using **AI-assisted coding tools** (Windsurf, Copilot, Cursor, Codeium, etc.) in the **Shiksha-Mitra project**.  
It ensures that AI-generated contributions are **reliable, testable, maintainable, and aligned with project goals**.

---

## 1. 🎯 Purpose

- Accelerate development with **AI pair-programming**.  
- Avoid pitfalls of **hallucinated code, fake APIs, and poor practices**.  
- Ensure all AI-generated code meets **team standards** before merging.

---

## 2. 🏗️ Project Context

Shiksha-Mitra is a **React 18 + TypeScript + Vite + Tailwind** application.  
AI contributions must align with the following stack & practices:

- **Frontend:** React, TailwindCSS, React Router DOM, Lucide React  
- **Testing:** Vitest + React Testing Library  
- **Quality:** ESLint + TypeScript ESLint  
- **Design System:** Utility-first, consistent color palette, accessibility first  
- **Deployment:** Vite build → Netlify / Vercel / GitHub Pages  

---

## 3. ✅ AI Code Contribution Checklist

Before committing AI-generated code:

- [ ] Runs successfully with `npm run dev`  
- [ ] Passes linting (`npm run lint`)  
- [ ] Includes **proper TypeScript typings**  
- [ ] Unit tests added (Vitest + RTL)  
- [ ] **No hallucinated imports** (verify with official docs)  
- [ ] Follows **Shiksha-Mitra coding standards**:
  - Functional components only  
  - Props typed via interfaces  
  - Tailwind utility classes (no inline styles)  
  - Accessibility checks (ARIA labels, semantic HTML)  

---

## 4. 🔄 Workflow for AI-Generated Code

### 4.1 Requesting Code
- Use AI tools to **prototype** functions, components, or utilities.
- Prefer **small, isolated tasks** (e.g., "Generate a JournalCard component") instead of entire pages.

### 4.2 Reviewing Code
- Validate imports and dependencies.  
- Ensure no unnecessary packages are added.  
- Run `npm run test` to confirm correctness.  

### 4.3 Submitting Code
- Commit to a **feature branch** (`feature/ai-component-X`).  
- Open a **Pull Request** with a clear label:
