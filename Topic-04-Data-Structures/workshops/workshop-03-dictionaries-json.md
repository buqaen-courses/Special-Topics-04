# Workshop 3: Dictionaries and JSON

**Section**: 8 - Dictionaries and JSON (45 min)
**Level**: Beginner
**Prerequisites**: Tutorial 3 (Dictionaries and JSON)

---

## 🎯 Workshop Objectives

By the end of this workshop, you will:

1. **Create and use dictionaries** for key-value data
2. **Work with JSON data** conversion
3. **Access dictionary data** by keys

---

## 📋 Workshop Structure

1. [Setup](#setup)
2. [Exercise 1: Dictionary Basics](#exercise-1-dictionary-basics)
3. [Exercise 2: Dictionary Operations](#exercise-2-dictionary-operations)
4. [Exercise 3: JSON Practice](#exercise-3-json-practice)

---

## 🛠️ Setup

Create a new Python file called `workshop_dict_json.py` for your exercises.

---

## 🏃 Exercise 1: Dictionary Basics

### Task 1.1: Dictionary Creation
Create a dictionary with your name, age, and city. Print the dictionary.

```python
# TODO: Create and print a dictionary
```

### Task 1.2: Dictionary Access
Create a dictionary and print the value for "name" and "age" keys.

```python
# TODO: Access dictionary values
```

### Task 1.3: Dictionary Keys and Values
Create a dictionary and print all keys, then all values.

```python
# TODO: Get dictionary keys and values
```

---

## 🏃 Exercise 2: Dictionary Operations

### Task 2.1: Adding to Dictionary
Start with an empty dictionary, add 3 key-value pairs.

```python
# TODO: Add items to dictionary
```

### Task 2.2: Changing Dictionary Values
Create a dictionary with age: 20, then change it to 21.

```python
# TODO: Change dictionary value
```

### Task 2.3: Checking Dictionary Keys
Create a dictionary and check if "email" key exists.

```python
# TODO: Check if key exists in dictionary
```

---

## 🏃 Exercise 3: JSON Practice

### Task 3.1: Dictionary to JSON
Create a dictionary and convert it to a JSON string.

```python
import json

# TODO: Convert dictionary to JSON
person = {"name": "Alice", "age": 25}
json_str = json.dumps(person)
print(json_str)
```

### Task 3.2: JSON to Dictionary
Take a JSON string and convert it back to a dictionary.

```python
import json

# TODO: Convert JSON to dictionary
json_data = '{"name": "Bob", "age": 30}'
dict_data = json.loads(json_data)
print(dict_data)
```

### Task 3.3: JSON File Operations
Save a dictionary to a JSON file, then load it back.

```python
import json

# TODO: Save and load JSON file
data = {"name": "Charlie", "age": 35}

# Save to file
with open("test.json", "w") as f:
    json.dump(data, f)

# Load from file
with open("test.json", "r") as f:
    loaded_data = json.load(f)

print(loaded_data)
```

### Task 3.4: Dictionary Building
Create a function that builds a dictionary from two lists (keys and values).

```python
def build_dict(keys: list, values: list) -> dict:
    # TODO: Create dictionary from keys and values lists
    pass

# Test your function
keys = ["name", "age", "city"]
values = ["David", 28, "Boston"]
result = build_dict(keys, values)
print(result)  # Should print {'name': 'David', 'age': 28, 'city': 'Boston'}
```

---

**Workshop Version**: 3.0 - Simplified
**Last Updated**: February 2026
**Estimated Time**: 45 minutes