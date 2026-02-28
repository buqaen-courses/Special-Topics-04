# Tutorial 2: Lists and Sets

**Section**: 7 - Lists and Sets (30 min)
**Level**: Beginner
**Prerequisites**: Tutorial 1 (Arrays and Matrices)

---

## 📋 Learning Objectives

By the end of this tutorial, you will be able to:

1. **Create and use lists** (ordered collections)
2. **Create and use tuples** (immutable sequences)
3. **Create and use sets** (unique collections)
4. **Perform basic operations** on lists, tuples, and sets

---

## 📚 Table of Contents

1. [What are Lists?](#what-are-lists)
2. [Using Lists](#using-lists)
3. [What are Tuples?](#what-are-tuples)
4. [Using Tuples](#using-tuples)
5. [What are Sets?](#what-are-sets)
6. [Using Sets](#using-sets)

---

## 🔸 What are Lists?

Lists are ordered collections that can hold multiple items. Lists can contain different types of data.

### Creating Lists

```python
# Empty list
empty = []

# List with numbers
numbers = [1, 2, 3, 4, 5]

# List with text
fruits = ["apple", "banana", "orange"]
```

### Using Lists

```python
# Print the list
print(numbers)  # [1, 2, 3, 4, 5]

# Count items in list
print(len(numbers))  # 5
```

---

## 🔸 Using Lists

### Accessing List Elements

```python
numbers = [10, 20, 30, 40, 50]

# Get first element
first = numbers[0]  # 10

# Get last element
last = numbers[4]  # 50

# Get second element
second = numbers[1]  # 20
```

### Adding to Lists

```python
numbers = [1, 2, 3]

# Add to end
numbers.append(4)
print(numbers)  # [1, 2, 3, 4]

# Add at specific position
numbers.insert(1, 10)
print(numbers)  # [1, 10, 2, 3, 4]
```

### Changing List Elements

```python
numbers = [1, 2, 3, 4, 5]

# Change first element
numbers[0] = 100
print(numbers)  # [100, 2, 3, 4, 5]
```

---

## 🔸 What are Tuples?

Tuples are ordered, immutable sequences. Once created, tuple items cannot be changed.

### Creating Tuples

```python
# Empty tuple
empty = ()

# Tuple with elements
numbers = (1, 2, 3, 4, 5)

# Tuple with different data types
person = ("Alice", 25, "New York")
```

### Using Tuples

```python
# Print the tuple
print(numbers)  # (1, 2, 3, 4, 5)

# Count items in tuple
print(len(numbers))  # 5
```

---

## 🔸 Using Tuples

### Accessing Tuple Elements

```python
numbers = (10, 20, 30, 40, 50)

# Get first element
first = numbers[0]  # 10

# Get last element
last = numbers[-1]  # 50

# Get second element
second = numbers[1]  # 20
```

### Tuple Operations

```python
# Check if item exists
numbers = (1, 2, 3, 4, 5)
print(3 in numbers)  # True

# Count occurrences
print(numbers.count(2))  # 1

# Find index
print(numbers.index(4))  # 3
```

### Tuple Unpacking

```python
# Unpack tuple into variables
person = ("Alice", 25, "New York")
name, age, city = person

print(name)  # Alice
print(age)   # 25
print(city)  # New York
```

---

## 🔸 What are Sets?

Sets are collections that contain unique items. Sets do not allow duplicates and are unordered.

### Creating Sets

```python
# Empty set
empty = set()

# Set with elements
numbers = {1, 2, 3, 4, 5}

# Set with text
colors = {"red", "green", "blue"}
```

### Using Sets

```python
# Print the set
print(numbers)  # {1, 2, 3, 4, 5}

# Count items in set
print(len(numbers))  # 5

# Check if item is in set
print(3 in numbers)  # True
print(10 in numbers)  # False
```

### Adding to Sets

```python
colors = {"red", "green", "blue"}

# Add one item
colors.add("yellow")
print(colors)  # {'red', 'green', 'blue', 'yellow'}

# Add multiple items
colors.update(["purple", "orange"])
print(colors)  # {'red', 'green', 'blue', 'yellow', 'purple', 'orange'}
```

### Functions with Type Hints

```python
# Function that works with lists
def add_to_list(items: list, new_item: str) -> list:
    """Add new item to list and return updated list."""
    items.append(new_item)
    return items

# Function that works with sets
def check_in_set(items: set, value: str) -> bool:
    """Check if value exists in set."""
    return value in items

# Function that works with tuples
def get_tuple_info(data: tuple) -> tuple:
    """Return (length, first_item) of tuple."""
    return (len(data), data[0] if data else None)

# Usage
fruits = ["apple", "banana"]
fruits = add_to_list(fruits, "orange")
print(fruits)  # ['apple', 'banana', 'orange']

colors = {"red", "blue", "green"}
has_red = check_in_set(colors, "red")
print(has_red)  # True

person = ("Alice", 25, "Engineer")
info = get_tuple_info(person)
print(info)  # (3, 'Alice')
```

---

## 🎯 Practice Exercises

### Exercise 1: List Basics
Create a list with numbers 1-5 and print the third element.

### Exercise 2: List Modification
Start with list `[1, 2, 3]`, add 4 to the end, then change the second element to 10.

### Exercise 3: Set Basics
Create a set with colors "red", "blue", "green" and check if "yellow" is in the set.

### Exercise 4: Set Operations
Create a set with numbers 1, 2, 3, then add 4 and 5 to it.

---

## 🎯 Key Takeaways

1. **Lists** are ordered, mutable collections that can have duplicates
2. **Tuples** are ordered, immutable sequences that cannot be changed
3. **Sets** are unordered collections with unique items only
4. Use **lists** when you need to modify data
5. Use **tuples** for fixed data that shouldn't change
6. Use **sets** when you need unique items and fast checking

---

**Tutorial Version**: 2.0 - Simplified
**Last Updated**: February 2026
**Estimated Reading Time**: 15 minutes