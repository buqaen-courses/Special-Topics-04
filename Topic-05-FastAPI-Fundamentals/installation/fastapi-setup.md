# FastAPI Development Environment Setup

## Overview
This guide covers setting up a Python development environment for FastAPI development, including virtual environments, dependencies, and essential tools.

## Prerequisites
- Python 3.8+ installed
- Basic command line knowledge
- Text editor or IDE (VS Code recommended)

---

## Python Installation Verification

### Check Python Version
```bash
python --version
# or
python3 --version
```

**Required**: Python 3.8 or higher

### Update Python (if needed)
**Windows (using python.org installer):**
- Download latest Python from https://python.org
- Run installer, check "Add Python to PATH"
- Restart terminal

**macOS:**
```bash
# Using Homebrew
brew install python

# Or update existing
brew upgrade python
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-uv
```

---

## Virtual Environment Setup

### Why Virtual Environments?
- Isolate project dependencies
- Avoid version conflicts
- Keep system Python clean
- Reproducible environments

### Initialize UV Project
```bash
# Navigate to project directory
cd your-project-directory

# Initialize UV project (creates pyproject.toml)
uv init

# Create virtual environment
uv venv
```

### Verify Activation
```bash
# Check which Python is being used
which python

# Should show path to .venv/bin/python or .venv\Scripts\python.exe

# Check pip location
which pip
```

### Deactivate Environment
```bash
deactivate
```

---

## FastAPI Installation

### Basic Installation
```bash
# Install FastAPI and server
uv add --index-url https://mirror2.chabokan.net/pypi/simple/ fastapi uvicorn

# Install additional dependencies
uv add --index-url https://mirror2.chabokan.net/pypi/simple/ pydantic requests httpx
```

### Development Dependencies
```bash
# Install development tools
uv add --index-url https://mirror2.chabokan.net/pypi/simple/ --upgrade pip

# Code formatting and linting
uv add --index-url https://mirror2.chabokan.net/pypi/simple/ black flake8 isort

# Testing
uv add --index-url https://mirror2.chabokan.net/pypi/simple/ pytest pytest-asyncio httpx

# Documentation
uv add --index-url https://mirror2.chabokan.net/pypi/simple/ mkdocs mkdocs-material
```

---

## Project Structure Setup

### Create Project Directory
```bash
mkdir fastapi-project
cd fastapi-project
uv venv
source .venv/bin/activate  # Linux/macOS
# or .venv\Scripts\activate  # Windows
```

### Basic Project Structure
```
fastapi-project/
├── .venv/                    # Virtual environment
├── app/
│   ├── __init__.py
│   ├── main.py             # FastAPI application
│   ├── models.py           # Pydantic models
│   ├── routes.py           # API routes
│   └── dependencies.py     # Dependencies
├── tests/
│   ├── __init__.py
│   ├── test_main.py
│   └── test_routes.py
├── requirements.txt         # Dependencies
├── .gitignore              # Git ignore file
└── README.md               # Documentation
```

### Create Files
```bash
# Create directories
mkdir -p app tests

# Create Python files
New-Item app/__init__.py, app/main.py, app/models.py app/routes.py, app/dependencies.py
New-Item tests/__init__.py, tests/test_main.py, tests/test_routes.py

# Create other files
touch requirements.txt .gitignore README.md
```

---

## Essential Configuration Files

### requirements.txt
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2
black==23.11.0
flake8==6.1.0
isort==5.12.0
```

### .gitignore
```
# Virtual environment
uv/
env/
ENV/
.venv/
venv/


# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

### Basic FastAPI Application (main.py)
```python
from fastapi import FastAPI

app = FastAPI(
    title="FastAPI Project",
    description="A sample FastAPI application",
    version="1.0.0"
)

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

---

## Development Tools Setup

### VS Code Configuration
Create `.vscode/settings.json`:
```json
{
    "python.defaultInterpreterPath": "./.venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    }
}
```

### Code Formatting Setup
```bash
# Install pre-commit hooks (optional)
uv add pre-commit

# Create .pre-commit-config.yaml
cat > .pre-commit-config.yaml << EOF
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  - repo: https://github.com/psf/black
    rev: 23.11.0
    hooks:
      - id: black

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
EOF

# Install hooks
pre-commit install
```

---

## Running FastAPI Application

### Development Server
```bash
# Run with uvicorn (uv handles the virtual environment)
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Access Application
- **API Documentation**: http://localhost:8000/docs (Swagger UI)
- **Alternative Docs**: http://localhost:8000/redoc
- **API Root**: http://localhost:8000/

### Test Endpoints
```bash
# Test root endpoint
curl http://localhost:8000/

# Test health endpoint
curl http://localhost:8000/health

# View API documentation in browser
open http://localhost:8000/docs
```

---

## Testing Setup

### Run Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_main.py

# Run tests in verbose mode
pytest -v
```

### Sample Test File (test_main.py)
```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
```

---

## Code Quality Tools

### Linting
```bash
# Run flake8
flake8 app/ tests/

# Run black (auto-format)
black app/ tests/

# Run isort (sort imports)
isort app/ tests/
```

### Pre-commit Hooks
```bash
# Run all hooks manually
pre-commit run --all-files

# Run specific hook
pre-commit run black --all-files
```

---

## Environment Management

### Environment Variables
Create `.env` file:
```
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///./test.db
```

Install python-dotenv:
```bash
uv add python-dotenv
```

Use in application:
```python
from dotenv import load_dotenv
import os

load_dotenv()

DEBUG = os.getenv("DEBUG", "False").lower() == "true"
SECRET_KEY = os.getenv("SECRET_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
```

---

## Troubleshooting

### Common Issues

**Module not found errors:**
```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Reinstall dependencies
uv add -r requirements.txt
```

**Port already in use:**
```bash
# Kill process using port 8000
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn app.main:app --reload --port 8001
```

**Import errors:**
- Check file structure matches imports
- Ensure `__init__.py` files exist
- Verify virtual environment activation

**Database connection issues:**
- Check DATABASE_URL in .env
- Ensure database file exists
- Check database permissions

---

## Development Workflow

### Daily Development
```bash
# Activate environment
source .venv/bin/activate

# Run linter and formatter
black . && isort . && flake8 .

# Run tests
pytest

# Start development server
uvicorn app.main:app --reload
```

### Before Committing
```bash
# Run all checks
black . && isort . && flake8 .
pytest --cov=app --cov-report=term-missing

# Check git status
git status
git add .
git commit -m "Your commit message"
```

---

## Next Steps

1. [Learn FastAPI basics](../tutorials/01-fastapi-introduction.md)
2. [Create your first API endpoints](../workshops/workshop-01-basic-api.md)
3. [Work with Pydantic models](../tutorials/02-pydantic-models.md)
4. [Add request validation](../workshops/workshop-02-request-validation.md)

---

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://pydantic-docs.helpmanual.io/)
- [Uvicorn Documentation](https://www.uvicorn.org/)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/uv.html)
- [VS Code Python Tutorial](https://code.visualstudio.com/docs/python/python-tutorial)
