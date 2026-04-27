# Tutorial 3: Dictionaries and JSON in Python

```bash
Section: Topic-04-Data-Structures — Section 3 (Dictionaries and JSON)
Level: Beginner
Estimated Time: ~40–45 minutes
Prerequisites: Basic Python, Lists, Tuples, Sets
```
---

# Learning Objectives

By the end of this tutorial you will be able to:

- Understand how dictionaries store data using hash tables
- Create, access, modify, and delete dictionary entries
- Loop through dictionaries using keys, values, and items
- Nest dictionaries and lists inside dictionaries
- Understand what JSON is and how it relates to Python dictionaries
- Convert between Python dictionaries and JSON strings
- Read and write JSON files

---

# Table of Contents

1. What Are Dictionaries?
2. Creating Dictionaries
3. Accessing Values
4. Modifying Dictionaries
5. Removing Elements
6. Looping Through Dictionaries
7. Nested Dictionaries
8. Useful Dictionary Methods
9. What Is JSON?
10. Converting Between Dictionary and JSON
11. Reading and Writing JSON Files
12. Functions That Work with Dictionaries and JSON
13. Common Beginner Mistakes
14. Practice Exercises
15. Key Takeaways
16. List vs Tuple vs Set vs Dict — Quick Comparison
17. Real-World Examples

---

# 1. What Are Dictionaries?

A dictionary stores data as **key-value pairs**.

Instead of accessing values by position (index), you access them by a meaningful key.

```python
person = {"name": "Alice", "age": 25}
```

Visual layout:
```bash
Key       Value
──────────────────
"name"  → "Alice"
"age"   → 25
```

Internally, Python implements dictionaries using a hash table — the same mechanism as sets. Each key is hashed to find its storage slot.

Hash Table (simplified):

Slot 0: empty
Slot 1: "name" → "Alice"
Slot 2: empty
Slot 3: "age"  → 25
...


This means:

- key lookup is $O(1)$ on average
- keys must be hashable (strings, numbers, tuples — not lists)
- keys are unique; assigning the same key twice overwrites the value
- as of Python 3.7+, dictionaries preserve insertion order

Dictionaries are commonly used for:

- representing real-world objects (a person, a product, a config)
- counting frequencies
- grouping related data
- working with JSON data from APIs

---

### Mini Exercise

Create a dictionary representing a book with keys `"title"` and `"pages"`.

---

# 2. Creating Dictionaries

### Basic Dictionary

```python
person = {"name": "Alice", "age": 25, "city": "New York"}
```

### Empty Dictionary

```python
data = {}
data = dict()   # equivalent
```

### Using dict()

```python
colors = dict(red="#FF0000", green="#00FF00", blue="#0000FF")
```

### Dictionary with Mixed Value Types

Keys are typically strings. Values can be any type.

```python
student = {
    "name":   "Bob",
    "grades": [85, 90, 88],
    "active": True
}
```

### Counting Elements

```python
person = {"name": "Alice", "age": 25, "city": "Cairo"}
print(len(person))   # 3
```

---

### Mini Exercise

Create a dictionary for a car with keys `"brand"`, `"year"`, and `"color"`. Print its length.

---

# 3. Accessing Values

### By Key

```python
person = {"name": "Alice", "age": 25}

print(person["name"])   # Alice
print(person["age"])    # 25
```

If the key does not exist, Python raises a `KeyError`:

KeyError: 'email'


### Using get()

`get()` returns `None` (or a default you provide) instead of raising an error.

```python
print(person.get("email"))           # None
print(person.get("email", "N/A"))    # N/A
```

Use `get()` when you are not sure if a key exists.

### Checking if a Key Exists

```python
print("age" in person)     # True
print("email" in person)   # False
```

---

### Mini Exercise

Given:

```python
student = {"name": "Sara", "grade": "A"}
```

Print the grade. Then try to access a key `"score"` safely using `get()`.

---

# 4. Modifying Dictionaries

### Adding a New Key

```python
person = {"name": "Alice", "age": 25}

person["city"] = "New York"

print(person)
# {"name": "Alice", "age": 25, "city": "New York"}
```

### Updating an Existing Key

Assigning to an existing key overwrites its value.

```python
person["age"] = 26
print(person)
# {"name": "Alice", "age": 26, "city": "New York"}
```

### update()

Merges another dictionary (or key-value pairs) into the current one.

```python
person.update({"email": "alice@example.com", "city": "London"})
```

If a key already exists, its value is overwritten. New keys are added.

---

### Mini Exercise

Start with:

```python
item = {"product": "pen", "price": 1.5}
```

Add a key `"stock"` with value `100`. Then update the price to `2.0`.

---

# 5. Removing Elements

Method           Behavior
──────────────────────────────────────────────────────────
del dict[key]    removes key; raises KeyError if not found
pop(key)         removes key and returns its value
pop(key, def)    removes key; returns def if not found
popitem()        removes and returns the last inserted pair
clear()          removes all elements


```python
person = {"name": "Alice", "age": 25, "city": "Cairo"}

del person["city"]
print(person)   # {"name": "Alice", "age": 25}

age = person.pop("age")
print(age)      # 25
print(person)   # {"name": "Alice"}
```

Use `pop(key, default)` when the key may not exist:

```python
val = person.pop("email", None)   # no error
```

---

### Mini Exercise

Remove the key `"age"` from:

```python
data = {"name": "John", "age": 30, "city": "Paris"}
```

---

# 6. Looping Through Dictionaries

### Loop Over Keys (default)

```python
person = {"name": "Alice", "age": 25, "city": "New York"}

for key in person:
    print(key)
```

Output:

name
age
city


### Loop Over Values

```python
for value in person.values():
    print(value)
```

Output:

Alice
25
New York


### Loop Over Key-Value Pairs

```python
for key, value in person.items():
    print(key, value)
```

Output:

name Alice
age 25
city New York


`.items()` is the most common approach when you need both key and value.

---

### Mini Exercise

Loop through the dictionary below and print each key and value:

```python
scores = {"math": 90, "english": 85, "science": 92}
```

---

# 7. Nested Dictionaries

A dictionary value can itself be a dictionary or a list.

### Nested Dictionary

```python
user = {
    "name": "Alice",
    "age": 25,
    "address": {
        "city": "New York",
        "zip": "10001"
    }
}

print(user["address"]["city"])   # New York
```

Visual layout:
```bash
user
├── "name"    → "Alice"
├── "age"     → 25
└── "address"
      ├── "city" → "New York"
      └── "zip"  → "10001"
```

You access nested values step by step:

user["address"]["city"]


### Nested Dictionary with Lists

```python
student = {
    "name": "Bob",
    "grades": {
        "math":    [90, 85, 88],
        "science": [92, 87, 91]
    }
}

print(student["grades"]["math"])      # [90, 85, 88]
print(student["grades"]["math"][0])   # 90
```

### List of Dictionaries

A common pattern for representing a collection of records:

```python
products = [
    {"id": 1, "name": "pen",      "price": 1.5},
    {"id": 2, "name": "notebook", "price": 3.0},
]

for product in products:
    print(product["name"], product["price"])
```

Output:
```bash
pen 1.5
notebook 3.0
```

---

### Mini Exercise

Create a dictionary for a book:

title
author
publisher:
    name
    year


Print the publisher's name.

---

# 8. Useful Dictionary Methods
```bash
Method                   Description
──────────────────────────────────────────────────────────────
dict.keys()              returns all keys
dict.values()            returns all values
dict.items()             returns all key-value pairs
dict.get(k, def)         safe access with optional default
dict.update(other)       merge another dict in
dict.pop(k, def)         remove and return value
dict.setdefault(k, def)  insert key with default if not present
dict.copy()              shallow copy
```

### setdefault()

Inserts a key with a default value only if the key does not already exist.

```python
person = {"name": "Alice"}

person.setdefault("age", 0)
print(person)   # {"name": "Alice", "age": 0}

person.setdefault("name", "Unknown")   # key exists, no change
print(person)   # {"name": "Alice", "age": 0}
```

### Frequency Counting Pattern

```python
words = ["apple", "banana", "apple", "orange", "banana", "apple"]

counts = {}

for word in words:
    counts[word] = counts.get(word, 0) + 1

print(counts)
# {"apple": 3, "banana": 2, "orange": 1}
```

---

### Mini Exercise

Count how many times each number appears in:

```python
numbers = [1, 2, 2, 3, 1, 1, 4]
```

---

# 9. What Is JSON?

JSON (JavaScript Object Notation) is a text format for storing and exchanging data.

It looks almost identical to a Python dictionary:

```json
{
    "name": "Alice",
    "age": 25,
    "active": true
}
```

JSON is used everywhere:

- APIs send and receive data as JSON
- configuration files (like `settings.json`)
- storing structured data in files

### Python vs JSON — Type Mapping
```bash
Python          JSON
──────────────────────
dict            object  { }
list            array   [ ]
str             string  " "
int / float     number
True            true
False           false
None            null
```

> Note: JSON keys must always be strings. Python dict keys can be any hashable type, but when converting to JSON, non-string keys are converted to strings automatically.

---

# 10. Converting Between Dictionary and JSON

Python's built-in `json` module handles all conversions.

```python
import json
```

### dict → JSON string: json.dumps()

```python
person = {"name": "Alice", "age": 25}

json_string = json.dumps(person)
print(json_string)
print(type(json_string))
```

Output:

{"name": "Alice", "age": 25}
<class 'str'>


### Pretty Printing

```python
print(json.dumps(person, indent=4))
```

Output:

```json
{
    "name": "Alice",
    "age": 25
}
```

### JSON string → dict: json.loads()

```python
json_string = '{"name": "Alice", "age": 25}'

person = json.loads(json_string)
print(person["name"])    # Alice
print(type(person))      # <class 'dict'>
```


### Nested JSON

JSON often contains nested structures. After parsing, they become nested Python dictionaries.

```python
import json

json_data = '''
{
    "name": "Alice",
    "age": 25,
    "address": {
        "city": "New York",
        "zip": "10001"
    }
}
'''

data = json.loads(json_data)
print(data["address"]["city"])   # New York
```

---

### Mini Exercise

Convert this dictionary to a JSON string and print it:

```python
car = {"brand": "Toyota", "year": 2022}
```

Then convert it back to a dictionary.

---

# 11. Reading and Writing JSON Files

### Writing a JSON File: json.dump()

```python
import json

data = {
    "name": "Alice",
    "scores": [90, 85, 92]
}

with open("data.json", "w") as f:
    json.dump(data, f, indent=4)
```

This creates `data.json`:

```json
{
    "name": "Alice",
    "scores": [90, 85, 92]
}
```

### Reading a JSON File: json.load()

```python
with open("data.json", "r") as f:
    loaded = json.load(f)

print(loaded["name"])      # Alice
print(loaded["scores"])    # [90, 85, 92]
```

### The Four JSON Functions

Function        Direction                  Works with
──────────────────────────────────────────────────────────
json.dumps()    dict  →  JSON string       string in memory
json.loads()    JSON string  →  dict       string in memory
json.dump()     dict  →  JSON file         file object
json.load()     JSON file  →  dict         file object


Memory trick: the `s` in `dumps` / `loads` stands for **string**.

---

### Mini Exercise

Write the following dictionary to a file called `student.json`, then read it back and print the name:

```python
student = {"name": "Sara", "grade": "A"}
```

---

# 12. Functions That Work with Dictionaries and JSON

Type hints make it clear what a function expects and returns.

```python
import json
from typing import Dict, Optional

def get_user_info(user_id: int) -> Optional[Dict[str, str]]:
    """Return user info by ID, or None if not found."""
    users = {
        1: {"name": "Alice", "city": "New York"},
        2: {"name": "Bob",   "city": "Boston"}
    }
    return users.get(user_id)

def save_user_to_json(user_data: Dict[str, str], filename: str) -> None:
    """Save a user dictionary to a JSON file."""
    with open(filename, "w") as f:
        json.dump(user_data, f, indent=4)

def load_user_from_json(filename: str) -> Optional[Dict[str, str]]:
    """Load a user dictionary from a JSON file. Returns None if file not found."""
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None
```

Usage:

```python
user = get_user_info(1)
if user:
    print(user)   # {"name": "Alice", "city": "New York"}

save_user_to_json({"name": "Charlie", "city": "Chicago"}, "user.json")

loaded = load_user_from_json("user.json")
print(loaded)   # {"name": "Charlie", "city": "Chicago"}

missing = load_user_from_json("nonexistent.json")
print(missing)  # None
```

> Note: `Optional[Dict[str, str]]` means the function can return either a dictionary or `None`. This is useful when a result may not exist.

---

### Mini Exercise

Write a function `find_by_name(users, name)` that takes a list of user dictionaries and returns the first one where `"name"` matches, or `None` if not found.

---

# 13. Common Beginner Mistakes

### Mistake 1 — KeyError when accessing a missing key

```python
person = {"name": "Alice"}
print(person["email"])   # KeyError
```

Fix: use `get()`.

```python
print(person.get("email", "not found"))
```

### Mistake 2 — Using `{}` and expecting a set

```python
s = {}        # dict, not set
s = set()     # correct empty set
```

### Mistake 3 — Using a list as a dictionary key

```python
d = {[1, 2]: "value"}   # TypeError: unhashable type: 'list'
d = {(1, 2): "value"}   # OK — tuple is hashable
```

### Mistake 4 — Confusing json.dump and json.dumps

```python
json.dumps(data)          # returns a string
json.dump(data, file)     # writes to a file
```

### Mistake 5 — Forgetting to import json

```python
json.dumps(data)   # NameError: name 'json' is not defined
```

Fix:

```python
import json
```

### Mistake 6 — Modifying a dictionary while looping over it

```python
for key in person:
    del person[key]   # RuntimeError
```

Fix: loop over a copy of the keys.

```python
for key in list(person.keys()):
    del person[key]
```

---

# 14. Practice Exercises

### Exercise 1

Create a dictionary with your name, age, and city. Print each value using a loop.

### Exercise 2

Start with an empty dictionary. Add 3 key-value pairs, then change one value and print the result.

### Exercise 3

Create a dictionary for a student with keys `"name"`, `"age"`, and `"grades"` (a list of numbers). Print the average grade.

### Exercise 4

Loop through the dictionary below and print only the keys where the value is greater than 80:

```python
scores = {"math": 90, "english": 75, "science": 88, "history": 60}
```

### Exercise 5

Count the frequency of each character in the string `"mississippi"`.

### Exercise 6

Convert the dictionary below to a JSON string with indentation, then parse it back and print the host:

```python
config = {"host": "localhost", "port": 8080, "debug": True}
```

### Exercise 7

Write a list of dictionaries to a JSON file and read it back:

```python
users = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"}
]
```

---

# 15. Key Takeaways

- Dictionaries store data as key-value pairs using a hash table
- Key lookup is $O(1)$ on average
- Keys must be hashable; values can be any type
- Use `get()` for safe access without risking `KeyError`
- `.keys()`, `.values()`, `.items()` are the standard ways to iterate
- Dictionaries preserve insertion order (Python 3.7+)
- JSON is a text format that maps directly to Python dictionaries
- `json.dumps()` / `json.loads()` convert between dict and string
- `json.dump()` / `json.load()` convert between dict and file
- The `s` in `dumps` / `loads` stands for string

---

# 16. List vs Tuple vs Set vs Dict — Quick Comparison

| Feature | List | Tuple | Set | Dict |
|---|---|---|---|---|
| Syntax | `[1, 2]` | `(1, 2)` | `{1, 2}` | `{"k": v}` |
| Ordered | Yes | Yes | No | Yes (3.7+) |
| Mutable | Yes | No | Yes | Yes |
| Duplicates | Yes | Yes | No | Keys: No |
| Indexed access | Yes | Yes | No | By key |
| Hashable (as key) | No | Yes | No | No |
| Membership $O(n)$ / $O(1)$ | $O(n)$ | $O(n)$ | $O(1)$ avg | $O(1)$ avg |
| Use case | Ordered data | Fixed data | Unique items | Key-value pairs |

Decision guide:

- ordered sequence that can change → list
- fixed data or dict key → tuple
- unique items or fast membership testing → set
- labeled data or structured records → dict

---

# 17. Real-World Examples

### Dictionary — User Profile

```python
user = {
    "id":     1001,
    "name":   "Alice",
    "email":  "alice@example.com",
    "active": True,
    "scores": [88, 92, 79]
}

print(user["name"])
print(sum(user["scores"]) / len(user["scores"]))   # average
```

### Dictionary — Config File in Memory

```python
config = {
    "host":  "localhost",
    "port":  5432,
    "debug": False
}

if config["debug"]:
    print("Debug mode on")
```

### JSON — Reading Data from an API Response

In real applications, API responses arrive as JSON strings. You parse them with `json.loads()`:

```python
import json

api_response = '{"status": "ok", "temperature": 22.5, "city": "Cairo"}'

data = json.loads(api_response)
print(data["city"])           # Cairo
print(data["temperature"])    # 22.5
```

### JSON — Saving Application Settings

```python
import json

settings = {
    "theme":     "dark",
    "language":  "en",
    "font_size": 14
}

with open("settings.json", "w") as f:
    json.dump(settings, f, indent=4)

with open("settings.json", "r") as f:
    settings = json.load(f)

print(settings["theme"])   # dark
```

---

### Mini Exercise

```python
products = [
    {"name": "pen",      "price": 1.5},
    {"name": "notebook", "price": 3.0},
    {"name": "ruler",    "price": 0.8}
]
```

Find the most expensive product by looping through the list.

---