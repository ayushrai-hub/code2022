# Architecture Documentation

## System Overview

This repository contains multiple independent projects, each serving different purposes and built with different technology stacks. The repository follows a **polyrepo-style collection** rather than a true monorepo, as each project is independent with its own dependencies and build processes.

## Architecture Principles

### 1. Project Independence
- Each project is self-contained with its own dependencies
- Projects do not share code or dependencies
- Each project can be developed, tested, and deployed independently

### 2. Technology Diversity
- **Python Projects:** GenAI, OutLier-AI
- **TypeScript/JavaScript Projects:** Shiksha-Mitra, MogoDb, new/mongodb-node-app, portfolio, iha-by-himani
- **Mixed:** Some projects use multiple technologies

### 3. No Shared Infrastructure
- No shared build system
- No shared CI/CD configuration
- No shared dependency management

## Project Architectures

### GenAI - Streamlit Application

**Architecture Pattern:** Single-page Streamlit application

```
GenAI/
└── genAI/
    └── streamlit/
        ├── app.py              # Main application entry point
        └── instructions.py     # Instruction definitions
```

**Technology Stack:**
- Python 3.x
- Streamlit (web framework)
- JSON (data storage)

**Data Flow:**
1. User inputs goal, task category, difficulty level
2. User creates turns with prompts and responses
3. User evaluates responses across multiple dimensions
4. Data is collected and can be exported as JSON

**Key Components:**
- Initial setup form
- Turn-based conversation interface
- Multi-dimensional evaluation system
- JSON export functionality

### Shiksha-Mitra - Educational Platform

**Architecture Pattern:** Next.js application (planned/partial implementation)

**Planned Architecture:**
```
Shiksha-Mitra/
└── Shiksha-Mitra/
    ├── apps/
    │   ├── web/              # Next.js frontend
    │   ├── api/              # Express backend (if separate)
    │   └── mobile/           # React Native (future)
    ├── packages/
    │   ├── ui/               # Shared UI components
    │   ├── database/         # Prisma schema
    │   ├── config/           # Shared configs
    │   ├── utils/            # Utility functions
    │   └── types/            # TypeScript definitions
    └── docs/                 # Documentation
```

**Technology Stack:**
- **Frontend:** Next.js 14+, TypeScript, TailwindCSS, Shadcn/UI
- **Backend:** Node.js + Express OR Next.js API routes
- **Database:** PostgreSQL (primary), Redis (caching)
- **ORM:** Prisma
- **Authentication:** JWT + NextAuth.js
- **Real-time:** Socket.io
- **AI/ML:** OpenAI GPT-4, Anthropic Claude, TensorFlow.js

**Current Status:** Documentation exists, implementation status unclear

### OutLier-AI - Python ML Scripts

**Architecture Pattern:** Collection of independent Python scripts

```
OutLier-AI/
└── PythonScriptsOutlierWeeks/
    ├── week1/
    ├── week2/
    └── ...
```

**Technology Stack:**
- Python 3.x
- Various ML libraries (as needed per script)

**Structure:** Organized by weeks, each containing learning/exercise scripts

### MogoDb - MongoDB Application

**Architecture Pattern:** Node.js application with MongoDB

**Technology Stack:**
- Node.js
- MongoDB
- Express.js (likely)

**Current Status:** Only node_modules visible, source code structure unclear

### new/mongodb-node-app - MongoDB TypeScript Application

**Architecture Pattern:** TypeScript Node.js application

**Technology Stack:**
- TypeScript
- Node.js
- MongoDB

**Current Status:** Source code structure needs investigation

### portfolio/ayush.me - Portfolio Website

**Architecture Pattern:** React SPA with Vite

**Technology Stack:**
- React
- TypeScript
- Vite (build tool)
- Various UI libraries

**Current Status:** Active project, structure needs documentation

### iha-by-himani/IHA-art-studio - Art Studio Application

**Architecture Pattern:** React application

**Technology Stack:**
- React
- TypeScript
- Build tool (likely Vite or similar)

**Current Status:** Active project, structure needs documentation

## Data Flow Patterns

### GenAI
- **Input:** User form inputs (goal, category, difficulty)
- **Processing:** Turn-based conversation collection
- **Output:** JSON export of evaluation data

### Shiksha-Mitra (Planned)
- **Frontend → Backend:** API calls for data operations
- **Backend → Database:** Prisma ORM queries
- **Real-time:** WebSocket connections for chat/video
- **AI Integration:** API calls to OpenAI/Anthropic

## Integration Points

### External Services
- **Shiksha-Mitra:** OpenAI, Anthropic, Cloudinary, payment gateways
- **Other projects:** MongoDB connections, various APIs

### Internal Dependencies
- None (projects are independent)

## Deployment Architecture

### Current State
- No unified deployment strategy
- Each project would deploy independently

### Recommended Approach
- **GenAI:** Deploy to Streamlit Cloud or similar
- **Shiksha-Mitra:** Vercel (frontend), Railway/Supabase (backend)
- **Portfolio:** Vercel or Netlify
- **Other projects:** Deploy based on individual requirements

## Security Considerations

1. **Environment Variables:** Each project should manage its own .env files
2. **API Keys:** Should never be committed to repository
3. **Authentication:** Shiksha-Mitra implements JWT + OAuth
4. **Database:** Connection strings should be secured

## Scalability Considerations

- **GenAI:** Single-user application, minimal scaling needs
- **Shiksha-Mitra:** Designed for multi-user, requires horizontal scaling
- **Other projects:** Scale based on individual requirements

## Technology Decisions

### Why Multiple Projects?
- Different purposes and requirements
- Independent development and deployment
- Different technology stacks suited to each purpose

### Why Not a Monorepo?
- Projects are unrelated
- Different teams/developers may work on different projects
- Simpler dependency management per project

## Future Architecture Considerations

1. **Shared Utilities:** If common patterns emerge, consider extracting to shared packages
2. **CI/CD:** Consider unified CI/CD if projects grow
3. **Documentation:** Centralized documentation (this DOCS directory)
4. **Testing:** Standardized testing approach across projects

---

**Last Updated:** 2025-01-16
