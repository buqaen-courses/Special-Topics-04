# Tutorial 0: Python Type Hints Basics

## 🎯 Learning Objectives

By the end of this tutorial, you will:

1. **Understand Type Hints**: Learn why and how to use Python's type annotations
2. **Use Basic Types**: Work with simple type hints for variables and functions
3. **Use Advanced Types**: Learn Union, Dict, and Optional type hints
4. **Write Clear Code**: Make your code easier to understand and debug

---

## 📋 Prerequisites

- Python 3.8+ installed
- Basic Python knowledge (variables, functions, lists)

---

## 🔍 Why Use Type Hints?

### The Problem: Unclear Code

```python
# Without type hints - what should we pass?
def calculate_average(numbers):
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)

# What if someone passes wrong data?
result = calculate_average([10, 20, 30])  # Works
result = calculate_average("hello")       # Fails!
```

### The Solution: Clear Expectations

```python
# With type hints - everyone knows what to expect
def calculate_average(numbers) -> float:
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)

# Now it's clear: get back a float
result = calculate_average([10, 20, 30])  # ✅ Clear intent
```

---

## 🏗️ Basic Type Hints

### 1. Simple Variable Types

**Type hints tell others what type of data a variable should hold.**

```python
# Basic type hints
name: str = "Alice"
age: int = 25
height: float = 5.7
is_student: bool = True
```

**Example with type hints:**
```python
student_name: str = "Bob"
student_age: int = 20
student_gpa: float = 3.5
is_graduated: bool = False
```

### 2. Function Type Hints

**Type hints on functions show what goes in and what comes out.**

```python
def greet(name: str) -> str:
    return f"Hello, {name}!"

def add_numbers(a: int, b: int) -> int:
    return a + b
```

**Example with type hints:**
```python
def calculate_area(length: float, width: float) -> float:
    return length * width
```

### 3. None Return Type

**Use None when a function doesn't return anything.**

```python
def print_message(message: str) -> None:
    print(f"Message: {message}")

def save_data(data: str) -> None:
    # Code to save data
    pass
```

---

## 🧪 When to Use Type Hints?

### Good Examples

```python
# ✅ Clear function purpose
def calculate_tax(price: float, rate: float) -> float:
    return price * rate

# ✅ Clear variable types
user_name: str = "Alice"
user_age: int = 25
is_active: bool = True

# ✅ Clear return type
def get_user_name() -> str:
    return "Alice"
```

### When Type Hints Help

- **Team Projects**: Other developers understand your code
- **Large Codebases**: Easier to maintain and debug
- **API Development**: Clear contracts for functions
- **Self-Documentation**: Code explains itself

---

## ⚠️ Important Notes

### Type Hints are Optional

```python
# Both are valid Python code
def greet(name):           # Without hints
    return f"Hello, {name}"

def greet(name: str) -> str:  # With hints
    return f"Hello, {name}"
```

### Type Hints Don't Change Runtime

```python
# Type hints are ignored at runtime
def add(a: int, b: int) -> int:
    return a + b

result = add("hello", "world")  # Still runs, returns "helloworld"
```

### Tools Can Check Types

```python
# Some tools can check if your code matches the hints
def divide(a: float, b: float) -> float:
    return a / b

# Tool might warn if you pass wrong types
result = divide(10, 0)  # Type hint satisfied, but logic error
```

---

## 📚 Additional Type Hints

### Union: Multiple Possible Types

**Union allows a variable or parameter to accept different types.**

```python
from typing import Union

# Parameter can be string or integer
def get_length(text: Union[str, int]) -> int:
    if isinstance(text, str):
        return len(text)
    else:
        return text  # If it's already a number

# Usage
result1 = get_length("hello")  # 5
result2 = get_length(42)       # 42
```

### Dict: Dictionary Types

**Dict shows the types of keys and values in a dictionary.**

```python
from typing import Dict

# Dictionary with string keys and integer values
def count_words(text: str) -> Dict[str, int]:
    words = text.split()
    result = {}
    for word in words:
        result[word] = result.get(word, 0) + 1
    return result

# Usage
word_count = count_words("hello world hello")
print(word_count)  # {'hello': 2, 'world': 1}
```

### Optional: Value Can Be None

**Optional shows that a value might be None.**

```python
from typing import Optional

# Function that might return None
def find_user(user_id: int) -> Optional[str]:
    users = {1: "Alice", 2: "Bob"}
    return users.get(user_id)  # Returns None if not found

# Usage
user1 = find_user(1)  # "Alice"
user3 = find_user(3)  # None
```

---

## 🎯 Key Takeaways

1. **Type hints** make code clearer and easier to understand
2. **Basic types**: `str`, `int`, `float`, `bool` for variables
3. **Function hints**: `-> type` shows return type, `param: type` shows parameters
4. **Union**: Allows multiple possible types for a value
5. **Dict**: Shows types for dictionary keys and values
6. **Optional**: Shows a value might be None
7. **Optional**: Type hints don't change how code runs
8. **Helpful**: Better for teams and large projects

---

## 🔗 Next Steps

After this tutorial, you'll be ready to:
- Write clearer functions with type hints
- Understand code written by others
- Use type hints in your projects

---

**Tutorial Version**: 2.0 - Simplified
**Last Updated**: February 2026
**Estimated Reading Time**: 15 minutes