# Workshop 3: Dictionaries and JSON
```bash
Section: Topic-04-Data-Structures - Workshop 3
Level: Beginner
Estimated Time: ~50 minutes
Prerequisites: Tutorial 3 (Dictionaries and JSON)
```
---

# Workshop Objectives

By the end of this workshop you will be able to:

- Create, access, modify, and delete dictionary entries confidently
- Loop through dictionaries using keys, values, and items
- Work with nested dictionaries and lists of dictionaries
- Convert between Python dictionaries and JSON strings
- Read and write JSON files
- Write type-hinted functions that work with dictionaries and JSON

---

# Workshop Structure

1. Warm-Up - Reading Code
2. Exercise 1: Dictionary Basics
3. Exercise 2: Modifying and Removing
4. Exercise 3: Looping Through Dictionaries
5. Exercise 4: Nested Dictionaries
6. Exercise 5: JSON Conversion
7. Exercise 6: JSON Files
8. Challenge Exercise

---

# Setup

Create a new file called `workshop_dicts_json.py`. Add `import json` at the top. Run it after each task to check your output.

---

# 1. Warm-Up - Reading Code

Read the code below and answer the questions before running it.

```python
import json

person = {"name": "Alice", "age": 25, "city": "Cairo"}

print(person["name"])
print(person.get("email", "N/A"))
print(len(person))
print("age" in person)

for key, value in person.items():
    print(key, "->", value)

json_str = json.dumps(person)
print(type(json_str))

back = json.loads(json_str)
print(back["city"])
```

Questions - write your answers as comments first:

- What does `person["name"]` print?
- What does `person.get("email", "N/A")` print, and why?
- What does `len(person)` print?
- What does `"age" in person` print?
- What does the loop print?
- What type is `json_str`?
- What does `back["city"]` print?

Run the code and check your predictions.

---

# 2. Exercise 1: Dictionary Basics

### Task 1.1 - Create and Access

Create a dictionary called `book` with keys `"title"`, `"author"`, and `"pages"`. Print each value using its key.

```python
# TODO: Create book dictionary
# TODO: Print title, author, pages
```

Expected output:
The Alchemist
Paulo Coelho
208


---

### Task 1.2 - Safe Access with get()

Given:

```python
student = {"name": "Sara", "grade": "A"}
```

Print the grade. Then try to access `"score"` and `"email"` safely. Provide a default of `"not found"` for missing keys.

```python
# TODO: Print grade
# TODO: Print score safely
# TODO: Print email safely
```

Expected output:
```bash
A
not found
not found
```

---

### Task 1.3 - Membership Testing

Given:

```python
config = {"host": "localhost", "port": 8080, "debug": True}
```

Check whether each key below exists and print a message:

```python
keys_to_check = ["host", "username", "port", "password"]

# TODO: Loop and print "host: found" or "host: not found"
```

Expected output:
```bash
host: found
username: not found
port: found
password: not found
```

---

### Task 1.4 - Frequency Counting

Count how many times each character appears in `"mississippi"`. Print the result sorted by character.

```python
text = "mississippi"

# TODO: Build a frequency dictionary using get()
# TODO: Print sorted by character
```

Expected output:
```bash
i: 4
m: 1
p: 2
s: 4
```

---

### Task 1.5 - dict() Constructor

Create the same dictionary two ways and confirm they are equal:

```python
# Way 1: using {}
colors_a = {"red": "#FF0000", "green": "#00FF00", "blue": "#0000FF"}

# Way 2: using dict()
# TODO: Create colors_b using dict()

print(colors_a == colors_b)   # True
```

---

# 3. Exercise 2: Modifying and Removing

### Task 2.1 - Build a Dictionary Step by Step

Start with an empty dictionary and follow the steps:

```python
item = {}

# Step 1: add "product" with value "pen"
# Step 2: add "price" with value 1.5
# Step 3: add "stock" with value 100
# Step 4: update price to 2.0
# Step 5: use update() to add "color": "blue" and "brand": "Pilot"

# TODO: Print after each step
```

Expected output after each step:
```json
{'product': 'pen'}
{'product': 'pen', 'price': 1.5}
{'product': 'pen', 'price': 1.5, 'stock': 100}
{'product': 'pen', 'price': 2.0, 'stock': 100}
{'product': 'pen', 'price': 2.0, 'stock': 100, 'color': 'blue', 'brand': 'Pilot'}
```

---

### Task 2.2 - Removing Elements

Given:

```python
data = {"name": "John", "age": 30, "city": "Paris", "email": "john@example.com"}
```

Perform each removal and print after each step:

```python
# Step 1: delete "city" using del
# Step 2: pop "age" and print the returned value
# Step 3: safely pop "phone" with a default of None and print the result
# Step 4: print the final dictionary
```

Expected output:
```json
{'name': 'John', 'age': 30, 'email': 'john@example.com'}
30
None
{'name': 'John', 'email': 'john@example.com'}
```

---

### Task 2.3 - setdefault()

Predict what each line prints, then run to verify:

```python
person = {"name": "Alice"}

person.setdefault("age", 0)
print(person)

person.setdefault("name", "Unknown")
print(person)
```

Write your predictions as comments first.

---

### Task 2.4 - Safe Deletion Loop

You need to remove all keys from a dictionary whose value is `None`. Fix the broken code below:

```python
profile = {"name": "Bob", "email": None, "city": "Rome", "phone": None}

# This will raise RuntimeError - do NOT run it as-is
for key in profile:
    if profile[key] is None:
        del profile[key]

# TODO: Fix it so it works correctly
print(profile)   # {"name": "Bob", "city": "Rome"}
```

---

# 4. Exercise 3: Looping Through Dictionaries

### Task 3.1 - Loop Over Keys, Values, Items

Given:

```python
scores = {"math": 90, "english": 75, "science": 88, "history": 60}
```

Write three separate loops:

```python
# Loop 1: print only the keys
# Loop 2: print only the values
# Loop 3: print "math: 90" for each pair
```

---

### Task 3.2 - Filter by Value

Loop through `scores` from Task 3.1 and print only the subjects where the score is greater than 80.

```python
# TODO: Print subjects with score > 80
```

Expected output:
```bash
math: 90
science: 88
```

---

### Task 3.3 - Compute Average

Write a function that takes a dictionary of subject scores and returns the average.

```python
def average_score(scores: dict) -> float:
    """Return the average of all values in the scores dictionary."""
    # TODO: implement
    pass

print(average_score({"math": 90, "english": 75, "science": 88}))   # 84.33...
```

---

### Task 3.4 - Invert a Dictionary

Write a function that swaps keys and values. Assume all values are unique.

```python
def invert_dict(d: dict) -> dict:
    """Return a new dictionary with keys and values swapped."""
    # TODO: implement
    pass

original = {"a": 1, "b": 2, "c": 3}
print(invert_dict(original))   # {1: 'a', 2: 'b', 3: 'c'}
```

---

# 5. Exercise 4: Nested Dictionaries

### Task 4.1 - Access Nested Values

Given:

```python
user = {
    "name": "Alice",
    "age": 25,
    "address": {
        "city": "New York",
        "zip": "10001"
    }
}
```

```python
# TODO: Print the city
# TODO: Print the zip code
# TODO: Print the full address dictionary
```

Expected output:
```bash
New York
10001
{'city': 'New York', 'zip': '10001'}
```

---

### Task 4.2 - Nested Dictionary with Lists

Given:

```python
student = {
    "name": "Bob",
    "grades": {
        "math":    [90, 85, 88],
        "science": [92, 87, 91]
    }
}
```

```python
# TODO: Print the math grades list
# TODO: Print the first math grade
# TODO: Print the average science grade
```

Expected output:
```bash
[90, 85, 88]
90
90.0
```

---

### Task 4.3 - Build a Nested Dictionary

Create a dictionary for a book with the structure below, then print the publisher's name.
```bash
book
├── "title"     → "Clean Code"
├── "author"    → "Robert Martin"
└── "publisher"
      ├── "name" → "Prentice Hall"
      └── "year" → 2008
```

```python
# TODO: Create the book dictionary
# TODO: Print the publisher name
```

Expected output:
```bash
Prentice Hall
```

---

### Task 4.4 - List of Dictionaries

Given:

```python
products = [
    {"id": 1, "name": "pen",      "price": 1.5},
    {"id": 2, "name": "notebook", "price": 3.0},
    {"id": 3, "name": "ruler",    "price": 0.8},
]
```

```python
# TODO: Print each product's name and price
# TODO: Find and print the most expensive product's name
# TODO: Find and print the cheapest product's name
```

Expected output:
```bash
pen 1.5
notebook 3.0
ruler 0.8
Most expensive: notebook
Cheapest: ruler
```

---

### Task 4.5 - Update a Nested Value

Given:

```python
user = {
    "name": "Alice",
    "address": {
        "city": "New York",
        "zip": "10001"
    }
}
```

Update the city to `"Boston"` and add a new key `"country"` with value `"USA"` inside the address. Print the updated address.

```python
# TODO: Update city
# TODO: Add country
# TODO: Print address
```

Expected output:
```json
{'city': 'Boston', 'zip': '10001', 'country': 'USA'}
```

---

# 6. Exercise 5: JSON Conversion

### Task 5.1 - dict to JSON String

Convert the dictionary below to a JSON string and print it. Then print it again with `indent=4`.

```python
car = {"brand": "Toyota", "year": 2022, "electric": False}

# TODO: Convert to JSON string and print
# TODO: Print with indent=4
```

Expected output:
```json
{"brand": "Toyota", "year": 2022, "electric": false}
{
    "brand": "Toyota",
    "year": 2022,
    "electric": false
}
```

Notice that Python's `False` becomes `false` in JSON.

---

### Task 5.2 - JSON String to dict

Parse the JSON string below and print the host and port.

```python
json_str = '{"host": "localhost", "port": 8080, "debug": true}'

# TODO: Parse to dictionary
# TODO: Print host and port
# TODO: Print the type of the result
```

Expected output:
```bash
localhost
8080
<class 'dict'>
```

---

### Task 5.3 - Round-Trip Conversion

Convert the dictionary to JSON and back, then confirm the result equals the original.

```python
config = {"host": "localhost", "port": 5432, "debug": False}

# TODO: Convert to JSON string
# TODO: Convert back to dictionary
# TODO: Print whether original == restored
```

Expected output:
`True`


---

### Task 5.4 - Nested JSON Parsing

Parse the JSON string below and print the city.

```python
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

# TODO: Parse and print the city
```

Expected output:
`New York`


---

### Task 5.5 - Simulated API Response

Parse the API response below and print a formatted summary.

```python
api_response = '{"status": "ok", "temperature": 22.5, "city": "Cairo", "humidity": 60}'

# TODO: Parse the response
# TODO: Print: "Weather in Cairo: 22.5°C, humidity 60%"
```

Expected output:
```bash
Weather in Cairo: 22.5°C, humidity 60%
```

---

# 7. Exercise 6: JSON Files

### Task 6.1 - Write and Read a JSON File

Write the dictionary below to `student.json`, then read it back and print the name and grade.

```python
student = {"name": "Sara", "grade": "A", "scores": [95, 88, 91]}

# TODO: Write to student.json with indent=4
# TODO: Read back and print name and grade
```

Expected output:
```bash
Sara
A
```

---

### Task 6.2 - Write a List of Dictionaries

Write the list below to `users.json`, then read it back and print each user's name.

```python
users = [
    {"id": 1, "name": "Alice", "city": "New York"},
    {"id": 2, "name": "Bob",   "city": "Boston"},
    {"id": 3, "name": "Carol", "city": "Chicago"},
]

# TODO: Write to users.json
# TODO: Read back and print each name
```

Expected output:
```bash
Alice
Bob
Carol
```

---

### Task 6.3 - load_user_from_json with Error Handling

Write a function that loads a dictionary from a JSON file and returns `None` if the file does not exist.

```python
import json
from typing import Optional

def load_user_from_json(filename: str) -> Optional[dict]:
    """Load a dictionary from a JSON file. Returns None if file not found."""
    # TODO: implement with try/except
    pass

result = load_user_from_json("users.json")
print(result is not None)   # True

missing = load_user_from_json("nonexistent.json")
print(missing)              # None
```

---

### Task 6.4 - Save and Load Settings

Write a function that saves a settings dictionary to a file, and another that loads it back.

```python
def save_settings(settings: dict, filename: str) -> None:
    """Save settings dictionary to a JSON file."""
    # TODO: implement
    pass

def load_settings(filename: str) -> dict:
    """Load settings from a JSON file. Return empty dict if file not found."""
    # TODO: implement
    pass

settings = {"theme": "dark", "language": "en", "font_size": 14}
save_settings(settings, "settings.json")

loaded = load_settings("settings.json")
print(loaded["theme"])      # dark
print(loaded["font_size"])  # 14

default = load_settings("missing.json")
print(default)              # {}
```

---

# 8. Challenge Exercise

### Task - Student Registry

Build a small student registry that stores data in a JSON file.

```python
import json
from typing import Optional

FILENAME = "registry.json"

def load_registry(filename: str) -> list:
    """Load the registry from a JSON file. Return empty list if not found."""
    # TODO: implement
    pass

def save_registry(registry: list, filename: str) -> None:
    """Save the registry to a JSON file."""
    # TODO: implement
    pass

def add_student(registry: list, name: str, grades: list[int]) -> None:
    """Add a new student to the registry."""
    # TODO: append a dict with "name" and "grades"
    pass

def find_student(registry: list, name: str) -> Optional[dict]:
    """Return the first student with the given name, or None."""
    # TODO: implement
    pass

def average_grade(student: dict) -> float:
    """Return the average grade for a student."""
    # TODO: implement
    pass
```

Use the functions to:

```python
registry = load_registry(FILENAME)

add_student(registry, "Alice", [90, 85, 92])
add_student(registry, "Bob",   [78, 82, 80])
add_student(registry, "Carol", [95, 91, 88])

save_registry(registry, FILENAME)

loaded = load_registry(FILENAME)

for student in loaded:
    avg = average_grade(student)
    print(f"{student['name']}: average = {avg:.1f}")

found = find_student(loaded, "Bob")
print(found)

not_found = find_student(loaded, "Dave")
print(not_found)
```

Expected output:
```bash
Alice: average = 89.0
Bob: average = 80.0
Carol: average = 91.3
{'name': 'Bob', 'grades': [78, 82, 80]}
None
```

---

# Key Takeaways

- use `get()` whenever a key might not exist - it avoids `KeyError`
- `.items()` is the standard way to loop when you need both key and value
- nested dictionaries are accessed step by step: `d["a"]["b"]`
- `json.dumps()` / `json.loads()` work with strings in memory
- `json.dump()` / `json.load()` work with files - the `s` stands for string
- Python's `True`/`False`/`None` become `true`/`false`/`null` in JSON
- always use `try/except FileNotFoundError` when reading files that may not exist
- type hints like `Optional[dict]` make function signatures self-documenting