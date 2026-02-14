# Python Virtual Environments (venv)

## Overview
A virtual environment is an isolated Python environment that allows you to manage dependencies for different projects separately.

## Why Use venv?

- **Dependency Isolation**: Install packages without affecting system Python
- **Project Independence**: Different projects can use different package versions
- **Clean Setup**: Easy to reproduce environments across machines

## Creating a Virtual Environment

```bash
python -m venv venv
```

## Activating the Environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

## Installing Packages

```bash
pip install package-name
```

## Deactivating the Environment

```bash
deactivate
```

## Best Practices

- Always activate before installing packages
- Use `requirements.txt` to track dependencies:
    ```bash
    pip freeze > requirements.txt
    pip install -r requirements.txt
    ```
- Add `venv/` to `.gitignore`
