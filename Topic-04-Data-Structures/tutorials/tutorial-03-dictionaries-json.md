# Tutorial 3: Dictionaries and JSON

**Section**: 8 - Dictionaries and JSON (30 min)
**Level**: Beginner
**Prerequisites**: Tutorial 2 (Lists and Sets)

---

## 📋 Learning Objectives

By the end of this tutorial, you will be able to:

1. **Create and use dictionaries** (key-value pairs)
2. **Work with JSON data** (simple conversion)
3. **Access dictionary data** by keys

---

## 📚 Table of Contents

1. [What are Dictionaries?](#what-are-dictionaries)
2. [Creating Dictionaries](#creating-dictionaries)
3. [Using Dictionaries](#using-dictionaries)
4. [What is JSON?](#what-is-json)
5. [Working with JSON](#working-with-json)

---

## 🔸 What are Dictionaries?

Dictionaries are collections that store data as key-value pairs. Each value has a unique key that you use to access it.

### Creating Dictionaries

```python
# Empty dictionary
empty = {}

# Dictionary with data
person = {
    "name": "Alice",
    "age": 25,
    "city": "New York"
}
```

### Using Dictionaries

```python
# Print the dictionary
print(person)
# {'name': 'Alice', 'age': 25, 'city': 'New York'}

# Count items in dictionary
print(len(person))  # 3
```

---

## 🔸 Creating Dictionaries

### Different Ways to Create Dictionaries

```python
# Using dict() function
colors = dict(red="#FF0000", green="#00FF00", blue="#0000FF")

# Dictionary with mixed data types
student = {
    "name": "Bob",
    "grades": [85, 90, 88],
    "active": True
}
```

---

## 🔸 Using Dictionaries

### Accessing Dictionary Values

```python
person = {
    "name": "Alice",
    "age": 25,
    "city": "New York"
}

# Get value by key
name = person["name"]  # "Alice"
age = person["age"]    # 25

# Check if key exists
print("age" in person)  # True
print("email" in person)  # False
```

### Adding and Changing Values

```python
person = {
    "name": "Alice",
    "age": 25
}

# Add new key-value pair
person["city"] = "New York"
print(person)
# {'name': 'Alice', 'age': 25, 'city': 'New York'}

# Change existing value
person["age"] = 26
print(person)
# {'name': 'Alice', 'age': 26, 'city': 'New York'}
```

### Dictionary Keys and Values

```python
data = {
    "name": "Charlie",
    "age": 30,
    "city": "Boston"
}

# Get all keys
keys = list(data.keys())
print(keys)  # ['name', 'age', 'city']

# Get all values
values = list(data.values())
print(values)  # ['Charlie', 30, 'Boston']
```

---

## 🔸 What is JSON?

JSON (JavaScript Object Notation) is a format for storing and sharing data. It looks similar to Python dictionaries.

### JSON Examples

```python
# JSON string
json_data = '{"name": "David", "age": 35, "city": "Chicago"}'

# This looks like a Python dictionary
python_dict = {"name": "David", "age": 35, "city": "Chicago"}
```

---

## 🔸 Working with JSON

### Converting Between JSON and Dictionaries

```python
import json

# Python dictionary
person = {
    "name": "Emma",
    "age": 28,
    "city": "Seattle"
}

# Convert dictionary to JSON string
json_string = json.dumps(person)
print(json_string)
# '{"name": "Emma", "age": 28, "city": "Seattle"}'

# Convert JSON string back to dictionary
back_to_dict = json.loads(json_string)
print(back_to_dict)
# {'name': 'Emma', 'age': 28, 'city': 'Seattle'}
```

### Working with JSON Files

```python
import json

# Save dictionary to JSON file
data = {"name": "Frank", "age": 32}
with open("person.json", "w") as file:
    json.dump(data, file)

# Load dictionary from JSON file
with open("person.json", "r") as file:
    loaded_data = json.load(file)

print(loaded_data)  # {'name': 'Frank', 'age': 32}
```

### Functions with Type Hints

```python
import json
from typing import Dict, Optional

# Function that works with dictionaries
def get_user_info(user_id: int) -> Optional[Dict[str, str]]:
    """Get user info by ID, returns None if not found."""
    users = {
        1: {"name": "Alice", "city": "New York"},
        2: {"name": "Bob", "city": "Boston"}
    }
    return users.get(user_id)

# Function that works with JSON
def save_user_to_json(user_data: Dict[str, str], filename: str) -> None:
    """Save user dictionary to JSON file."""
    with open(filename, "w") as file:
        json.dump(user_data, file)

def load_user_from_json(filename: str) -> Optional[Dict[str, str]]:
    """Load user dictionary from JSON file."""
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return None

# Usage
user = get_user_info(1)
if user:
    print(f"User: {user}")  # User: {'name': 'Alice', 'city': 'New York'}

save_user_to_json({"name": "Charlie", "city": "Chicago"}, "user.json")
loaded_user = load_user_from_json("user.json")
print(f"Loaded: {loaded_user}")  # Loaded: {'name': 'Charlie', 'city': 'Chicago'}
```

---

## 🎯 Practice Exercises

### Exercise 1: Dictionary Basics
Create a dictionary with your name, age, and city. Print each value.

### Exercise 2: Dictionary Operations
Start with an empty dictionary, add 3 key-value pairs, then change one value.

### Exercise 3: JSON Conversion
Create a dictionary, convert it to JSON, then convert it back to a dictionary.

### Exercise 4: Keys and Values
Create a dictionary and print all the keys, then all the values.

---

## 🎯 Key Takeaways

1. **Dictionaries** store data as key-value pairs
2. **Keys** are unique and used to access values
3. **JSON** is a data format similar to dictionaries
4. Use **json.dumps()** to convert dictionary to JSON
5. Use **json.loads()** to convert JSON to dictionary

---

**Tutorial Version**: 3.0 - Simplified
**Last Updated**: February 2026
**Estimated Reading Time**: 15 minutes