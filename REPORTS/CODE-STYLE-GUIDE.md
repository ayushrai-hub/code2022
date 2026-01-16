# Code Style & Quality Guide

This repository uses automated code formatting, linting, and CI/CD to maintain consistent code quality across all projects.

## 📋 Quick Start

### Code Formatting

#### Python Projects
```bash
# Format code with Black
black GenAI/genAI OutLier-AI

# Check formatting without making changes
black --check GenAI/genAI OutLier-AI
```

#### JavaScript/TypeScript Projects
```bash
# Format code with Prettier
prettier --write "portfolio/**/*.{js,jsx,ts,tsx,json}"
prettier --write "iha-by-himani/**/*.{js,jsx,ts,tsx,json}"

# Check formatting without making changes
prettier --check "portfolio/**/*.{js,jsx,ts,tsx,json}"
```

### Linting

#### Python Projects
```bash
# Run Ruff linter
ruff check GenAI/genAI OutLier-AI

# Run Pylint
pylint GenAI/genAI OutLier-AI --rcfile=.pylintrc
```

#### JavaScript/TypeScript Projects
```bash
# Run ESLint
eslint "portfolio/**/*.{js,jsx,ts,tsx}" --ext .js,.jsx,.ts,.tsx
```

## 🔧 Configuration Files

### `.editorconfig`
Universal formatting rules for all file types. Most modern editors support this automatically.

### `.prettierrc.json` & `.prettierignore`
Prettier configuration for JavaScript, TypeScript, and JSON files.

### `pyproject.toml`
Python formatting and linting configuration:
- **Black**: Code formatter
- **Ruff**: Fast Python linter
- **isort**: Import sorting

### `.pylintrc`
Additional Python linting rules with Pylint.

### `.eslintrc.json` & `.eslintignore`
ESLint configuration for JavaScript and TypeScript projects.

## 🚀 CI/CD

GitHub Actions workflows automatically run on every push and pull request:

1. **`.github/workflows/ci.yml`**: Main CI pipeline
   - Python linting and formatting checks
   - Python tests
   - JavaScript/TypeScript linting and formatting checks
   - JavaScript/TypeScript tests

2. **`.github/workflows/code-quality.yml`**: Code quality checks
   - Formatting verification
   - Linting verification

## 📝 Editor Setup

### VS Code
Install these extensions:
- **EditorConfig for VS Code**
- **Prettier - Code formatter**
- **ESLint**
- **Python** (with Black formatter)

Add to `.vscode/settings.json`:
```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter",
    "editor.formatOnSave": true
  },
  "[javascript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  }
}
```

### PyCharm
- Enable EditorConfig plugin
- Configure Black as formatter: Settings → Tools → Black
- Enable ESLint for JS/TS files

## 🎯 Best Practices

1. **Before committing:**
   - Run formatters: `black .` and `prettier --write .`
   - Run linters: `ruff check .` and `eslint .`
   - Fix any issues before pushing

2. **CI/CD will catch:**
   - Formatting inconsistencies
 - Linting errors
   - Test failures

3. **Project-specific:**
   - Each project can override root configs if needed
   - Place project-specific configs in project directories

## 📚 Additional Resources

- [EditorConfig](https://editorconfig.org/)
- [Prettier](https://prettier.io/)
- [Black](https://black.readthedocs.io/)
- [Ruff](https://docs.astral.sh/ruff/)
- [ESLint](https://eslint.org/)
- [Pylint](https://pylint.readthedocs.io/)
