# Codebase Repository

This repository contains multiple independent projects across different technologies and domains.

## 📁 Project Structure

### Active Projects

#### 1. **GenAI** - AI Conversation Evaluation Tool
- **Location:** `./GenAI/genAI/`
- **Technology:** Python, Streamlit
- **Purpose:** AI model response evaluation tool with multi-dimensional rating system
- **Entry Point:** `streamlit/app.py`
- **Run:** `streamlit run GenAI/genAI/streamlit/app.py`

#### 2. **Shiksha-Mitra** - AI-Powered Educational Platform
- **Location:** `./Shiksha-Mitra/Shiksha-Mitra/`
- **Technology:** TypeScript, Next.js, React
- **Purpose:** Educational platform connecting students, teachers, and learning resources
- **Features:** AI learning assistant, courses, doubt clearing, assessments
- **Documentation:** See `Shiksha-Mitra/Shiksha-Mitra/MarkdownDocsa/` for detailed docs

#### 3. **OutLier-AI** - Python ML/AI Scripts
- **Location:** `./OutLier-AI/`
- **Technology:** Python
- **Purpose:** Machine learning and AI scripts/exercises
- **Structure:** Organized by weeks in `PythonScriptsOutlierWeeks/`

#### 4. **MogoDb** - MongoDB Application
- **Location:** `./MogoDb/MogoDb/`
- **Technology:** Node.js, MongoDB
- **Purpose:** MongoDB database operations and connectivity

#### 5. **new/mongodb-node-app** - MongoDB Node.js Application
- **Location:** `./new/mongodb-node-app/`
- **Technology:** TypeScript, Node.js, MongoDB
- **Purpose:** MongoDB integration with Node.js/TypeScript

#### 6. **portfolio/ayush.me** - Personal Portfolio Website
- **Location:** `./portfolio/ayush.me/`
- **Technology:** React, TypeScript, Vite
- **Purpose:** Personal portfolio website showcasing projects and skills

#### 7. **iha-by-himani/IHA-art-studio** - Art Studio Application
- **Location:** `./iha-by-himani/IHA-art-studio/`
- **Technology:** React, TypeScript
- **Purpose:** Art studio application

## 🚀 Quick Start

Each project is independent and should be run from its respective directory. Refer to individual project READMEs for specific setup instructions.

### Prerequisites
- **Python 3.8+** (for Python projects)
- **Node.js 16+** (for Node.js projects)
- **npm** or **yarn** (for Node.js projects)

## 📚 Documentation

- **Main Audit Report:** See `AUDIT_REPORT.md` for comprehensive codebase analysis
- **AI Coding Rules:** See `.rules/` directory for development guidelines
- **Project-Specific Docs:** Each project may have its own documentation

## 🛠️ Development Guidelines

This repository follows strict development practices:
- See `.rules/` directory for coding, testing, refactoring, and commit strategies
- All projects should have comprehensive tests
- Documentation is mandatory for all projects
- Follow SOLID principles and DRY methodology

## 📝 Project Status

| Project | Status | Documentation | Tests |
|---------|--------|---------------|-------|
| GenAI | ✅ Active | ✅ Complete | ✅ Tests Added |
| Shiksha-Mitra | ✅ Active | ✅ Comprehensive | ⚠️ Needs tests |
| OutLier-AI | ✅ Active | ✅ Complete | ⚠️ Needs tests |
| MogoDb | ✅ Active | ✅ Complete | ⚠️ Needs source code |
| new/mongodb-node-app | ✅ Active | ✅ Complete | ⚠️ Needs source code |
| portfolio/ayush.me | ✅ Active | ✅ Complete | ⚠️ Needs tests |
| iha-by-himani/IHA-art-studio | ✅ Active | ✅ Complete | ⚠️ Needs source code |

## 🔧 Repository Management

### Directory Structure
```
.
├── .rules/              # AI-assisted coding rules
├── GenAI/               # Python/Streamlit AI evaluation tool
├── Shiksha-Mitra/       # Educational platform
├── OutLier-AI/          # Python ML scripts
├── MogoDb/              # MongoDB application
├── new/                 # MongoDB Node.js app
├── portfolio/           # Portfolio website
├── iha-by-himani/       # Art studio app
├── doc/                 # Documentation
├── AUDIT_REPORT.md      # Comprehensive audit report
└── README.md            # This file
```

### Notes
- Each project is independent with its own dependencies
- Virtual environments and node_modules are excluded via .gitignore
- Projects may have their own git repositories (e.g., Shiksha-Mitra)

## 🤝 Contributing

1. Follow the guidelines in `.rules/` directory
2. Write tests for new features
3. Update documentation
4. Follow commit message conventions (see `.rules/git-commit-strategy.md`)

## 📄 License

[Add license information if applicable]

## 🔍 Audit & Maintenance

This repository has been audited following the MEGA PROMPT methodology. See `AUDIT_REPORT.md` for detailed findings and recommendations.

---

**Last Updated:** 2025-01-16  
**Auditor:** Autonomous AI Codebase Auditor
