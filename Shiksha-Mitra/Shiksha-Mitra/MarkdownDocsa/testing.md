# Shiksha-Mitra Frontend Testing Master Prompt (React + TypeScript, Next.js 14)

You are an expert frontend tester for a Next.js 14 (App Router) application written in React and TypeScript. Your task is to produce a complete, production-grade testing suite and documentation for the Shiksha-Mitra platform’s frontend. Follow the specifications below precisely. Generate code, configuration, and documentation as requested.

Context and stack
- Framework: Next.js 14+ (App Router: server and client components)
- Language: TypeScript (strict mode)
- UI: TailwindCSS + shadcn/ui
- State/data: React Query (TanStack Query)
- Forms: React Hook Form + Zod
- Animations: Framer Motion
- Auth: NextAuth.js + JWT
- API: Next.js Route Handlers or external API
- Realtime: Socket.io (client)
- AI integrations present but stubbed via MSW for tests

Overall goals
- Deliver a maintainable, deterministic, and fast testing setup covering unit, integration, E2E, accessibility, and visual regression for critical flows.
- Validate SSR/CSR/hydration, App Router navigation, data fetching with React Query, forms with RHF+Zod, auth-protected routes, and realtime UI behavior.
- Include proper mocking (network, auth, router, time, intersection observer, media, WebRTC), fixtures, factories, and test data isolation.
- Enforce coding standards, coverage thresholds, CI integration, and test documentation.

Deliverables
1. Tooling and configuration
   - Jest config (ts-jest or swc/jest), Testing Library, jest-dom, user-event, jest-axe, MSW, @faker-js/faker, identity-obj-proxy, next/router mocks for App Router (next/navigation), and any necessary polyfills.
   - Playwright config for E2E (headed/headless, projects for desktop/mobile, trace/video on failure, storage state for authenticated tests).
   - Storybook config (for component isolation) and Chromatic or Playwright component tests for visual regression.
   - ESLint testing rules and Prettier config updates.
   - NPM scripts to run unit, integration, E2E, a11y, visual regression, and coverage locally and in CI.

2. Test architecture and conventions
   - Test directory layout:
     - co-locate unit tests next to components: ComponentName.test.tsx
     - integration tests under tests/integration
     - E2E tests under tests/e2e with Playwright
     - shared: tests/utils (render helpers, providers), tests/mocks (MSW handlers), tests/fixtures (JSON), tests/factories
   - Utilities: a custom render wrapper that provides React Query client, ThemeProvider, NextIntl/i18n mock (if applicable), RHF context as needed, and MSW setup/teardown hooks.
   - Selectors: prefer accessible roles and labels; avoid testing implementation details; use data-testid only as a last resort.
   - Arrange-Act-Assert pattern. Avoid snapshot tests except for stable, static markup. Prefer explicit assertions.

3. Cross-cutting concerns to test and mock
   - App Router and navigation:
     - Mock next/navigation (useRouter, usePathname, redirect) with a reliable adapter.
     - Validate link navigation, intercepting routes, and dynamic segments.
     - Verify SSR/ISR/CSR and hydration mismatches for key pages.
   - Data fetching with React Query:
     - Mock network with MSW, assert cache states (loading, error, success), invalidations, background refetch, pagination, and optimistic updates.
   - Forms with React Hook Form + Zod:
     - Validate client-side schema errors, server errors via API, submit/disabled states, multi-step flows, and field arrays.
   - Auth-protected routes with NextAuth:
     - Mock session states (unauthenticated, authenticated with roles: STUDENT, TEACHER, INSTITUTION, ADMIN).
     - Guarded route redirects and conditional UI.
     - In E2E, support storageState for pre-authenticated flows and/or a Credentials provider in test env.
   - Realtime UI with Socket.io:
     - Abstract socket client; mock connect/disconnect, re-connect, incoming events, optimistic UI, and error toasts.
   - Media and browser APIs:
     - Mock IntersectionObserver, ResizeObserver, matchMedia, WebRTC getUserMedia, canvas (whiteboard), and Clipboard as needed.
   - Time and timers:
     - Use fake timers for debounced inputs, autosave, and countdowns; test DST/timezone, locale formatting.
   - Accessibility:
     - Use jest-axe on key components and pages.
     - Ensure proper roles/labels, focus management, and keyboard navigation.
   - Internationalization/localization (if used):
     - Test English + one non-English locale; RTL direction if applicable. Verify pluralization and date/number formatting.
   - Animations:
     - Disable animations in test env; assert final states and ARIA attributes rather than animation frames.
   - Analytics/events:
     - Mock analytics layer; assert event names, payload schema, and timing for critical flows.

4. Targeted feature coverage
   Provide tests for each item below, including component/unit tests, integration tests, and E2E scenarios.

   Authentication and onboarding
   - OAuth login (Google/GitHub/LinkedIn) mocked; email and phone OTP flows; email verification.
   - Role-based redirects and protected routes.
   - 2FA flow and recovery state handling.
   - E2E: full onboarding wizard per role, persistence across steps, validation, and resumability.

   User profile
   - Profile form with RHF + Zod: avatar upload (mock), bio, interests, goals, privacy controls.
   - Education/skills sub-forms; dynamic fields; autosave with optimistic updates.
   - Accessibility and responsive behavior.

   Study buddy matching
   - List/grid of matches with filters (subjects, schedule, location).
   - Empty/loading/error states; pagination/infinite scroll with virtualized lists.
   - Interaction: save/favorite, dismiss, report; optimistic updates and rollback on server failure.

   Real-time communication
   - Chat UI: message composer, uploads (mock Cloudinary), markdown/links, read receipts (mocked), presence indicators.
   - Whiteboard component (canvas mocked): add/erase/undo/redo, export.
   - Video call initialization UI (WebRTC mocked): permission prompts, device switching, screen share toggle; reconnection UX.
   - E2E: join study room, send/receive messages, disconnection and reconnection.

   AI learning assistant (frontend scaffolding)
   - Prompt input, streamed responses (mock SSE), stop/cancel, retry with context.
   - RAG result list; loading skeletons; error fallback; copy-to-clipboard.
   - Guardrails UI: content moderation messages, safe retry CTA.

   Analytics dashboard (frontend)
   - Charts rendering with sample data; loading/error states; date range filters.
   - Export actions; a11y of charts (titles/desc).

5. Performance and security checks
   - Performance budget tests:
     - Playwright + Lighthouse CI for key routes: LCP, CLS, TBT budgets; assert no blocking large scripts; image lazy loading.
   - Security-focused tests (frontend):
     - Prevent XSS via message rendering and profile fields (escape/allowlist).
     - CSRF/Clickjacking headers validated in E2E for