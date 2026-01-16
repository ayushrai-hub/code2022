# Quick Start Guide

This guide provides quick setup instructions for each project in the repository.

## Prerequisites

### For Python Projects
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### For Node.js Projects
- Node.js 16 or higher
- npm or yarn

## Project Setup Instructions

### 1. GenAI - Code Review Prompt Generator

**Technology:** Python, Streamlit

```bash
cd GenAI/genAI
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run streamlit/app.py
```

**Access:** http://localhost:8501

**Tests:**
```bash
pytest tests/ -v
```

---

### 2. Shiksha-Mitra - Educational Platform

**Technology:** TypeScript, Next.js

**Status:** Documentation only, implementation needed

**When implemented:**
```bash
cd Shiksha-Mitra/Shiksha-Mitra
npm install
npm run dev
```

**Documentation:** See `Shiksha-Mitra/Shiksha-Mitra/MarkdownDocsa/` for detailed guides

---

### 3. OutLier-AI - Python ML/AI Scripts

**Technology:** Python

```bash
cd OutLier-AI
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt  # Install dependencies as needed

# Run individual scripts
python PythonScriptsOutlierWeeks/week1/task1/script.py
```

**Note:** Most scripts use standard library only. Install additional packages only if needed.

---

### 4. MogoDb - MongoDB Application

**Technology:** Node.js, MongoDB

**Status:** Source code needed

**When source code is available:**
```bash
cd MogoDb/MogoDb
npm install
# Create .env file with MONGODB_URI
npm start
```

---

### 5. new/mongodb-node-app - MongoDB TypeScript App

**Technology:** TypeScript, Node.js, MongoDB

**Status:** Source code needed

**When source code is available:**
```bash
cd new/mongodb-node-app
npm install
# Create .env file with MONGODB_URI
npm run build
npm start
```

---

### 6. portfolio/ayush.me - Portfolio Website

**Technology:** React, TypeScript, Vite

```bash
cd portfolio/ayush.me
npm install
npm run dev
```

**Access:** http://localhost:5173 (or port assigned by Vite)

**Build:**
```bash
npm run build
```

---

### 7. iha-by-himani/IHA-art-studio - Art Studio App

**Technology:** React, TypeScript

**Status:** Source code structure needs verification

**When source code is available:**
```bash
cd iha-by-himani/IHA-art-studio
npm install
npm run dev  # or npm start
```

---

## Common Commands

### Python Projects
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v
```

### Node.js Projects
```bash
# Install dependencies
npm install

# Development mode
npm run dev  # or npm start

# Build for production
npm run build

# Run tests
npm test
```

---

## Troubleshooting

### Python Issues

**Import errors:**
- Ensure virtual environment is activated
- Install missing packages: `pip install <package-name>`
- Check Python version: `python --version` (should be 3.8+)

**Streamlit not found:**
```bash
pip install streamlit
```

### Node.js Issues

**Module not found:**
- Delete `node_modules` and `package-lock.json`
- Run `npm install` again

**Port already in use:**
- Change port in configuration
- Kill process using the port

**Build errors:**
- Check Node.js version: `node --version` (should be 16+)
- Clear cache: `npm cache clean --force`

---

## Environment Variables

Some projects may require environment variables. Create `.env` files as needed:

### MongoDB Projects
```env
MONGODB_URI=mongodb://localhost:27017/your-database
```

### API Keys (if needed)
```env
API_KEY=your-api-key
```

**Note:** Never commit `.env` files to git. Use `.env.example` as a template.

---

## Getting Help

1. Check project-specific README files
2. Review `DOCS/` directory for detailed documentation
3. Check `AUDIT_REPORT.md` for project status
4. Review `DOCS/Known-Issues-Tradeoffs.md` for common issues

---

**Last Updated:** 2025-01-16
