# Tutorial 1: Arrays and Matrices in Python

**Section**: 6 - Arrays and Matrices (30 min)
**Level**: Beginner
**Prerequisites**: Basic Python knowledge (variables, loops, functions)

---

## 📋 Learning Objectives

By the end of this tutorial, you will be able to:

1. **Create and use arrays** (lists in Python)
2. **Access array elements** by position
3. **Create and use matrices** (2D arrays)
4. **Perform basic array and matrix operations**

---

## 📚 Table of Contents

1. [What are Arrays?](#what-are-arrays)
2. [Creating Arrays](#creating-arrays)
3. [Using Arrays](#using-arrays)
4. [What are Matrices?](#what-are-matrices)
5. [Creating Matrices](#creating-matrices)
6. [Using Matrices](#using-matrices)

---

## 🔸 What are Arrays?

Arrays are containers that hold multiple values. In Python, we use **lists** as arrays. Arrays help us work with collections of data.

### Creating Arrays

```python
# Empty array
empty = []

# Array with numbers
numbers = [1, 2, 3, 4, 5]

# Array with text
fruits = ["apple", "banana", "orange"]
```

### Using Arrays

```python
# Print the array
print(numbers)  # [1, 2, 3, 4, 5]

# Count items in array
print(len(numbers))  # 5
```

---

---

## 🔸 Using Arrays

### Accessing Array Elements

```python
numbers = [10, 20, 30, 40, 50]

# Get first element (position 0)
first = numbers[0]  # 10

# Get second element (position 1)
second = numbers[1]  # 20

# Get last element using positive index
last = numbers[4]  # 50

# Get last element using negative index
last_negative = numbers[-1]  # 50 (easier way!)
```

### Array Slicing

```python
numbers = [10, 20, 30, 40, 50]

# Get first 3 elements [start:end]
first_three = numbers[0:3]  # [10, 20, 30]

# Get elements from index 2 to end
from_index_2 = numbers[2:]  # [30, 40, 50]

# Get last 2 elements
last_two = numbers[-2:]  # [40, 50]

# Get every other element [start:end:step]
every_other = numbers[::2]  # [10, 30, 50]
print(numbers[1:4])  # [20, 30, 40]

print(numbers[:3])  # [10, 20, 30]

print(numbers[2:])  # [30, 40, 50]

print(numbers[-3:])  # [30, 40, 50]

print(numbers[:-2])  # [10, 20, 30]

print(numbers[::2])  # [10, 30, 50]

print(numbers[1::2])  # [20, 40]

print(numbers[::-1])  # [50, 40, 30, 20, 10]

print(numbers[:])  # [10, 20, 30, 40, 50] (copy of the entire list)



numbers.append(60)  # Add 60 to the end of the list
print(numbers)  # Output: [10, 20, 30, 40, 50, 60]

numbers.insert(2, 25)  # Insert 25 at index 2   
print(numbers)  # Output: [10, 20, 25, 30, 40, 50, 60]  

numbers.remove(40)  # Remove the first occurrence of 40
print(numbers)  # Output: [10, 20, 25, 30, 50, 60]

k=numbers.pop()  # Remove the last element (60)
print(numbers)  # Output: [10, 20, 25, 30, 50]
print(k)  # Output: 60

numbers.clear()  # Remove all elements from the list
numbers=[]  # Another way to clear the list

numbers = [10, 20, 30]
numbers.extend([40, 50])  # Add multiple elements to the end of the list
print(numbers)  # Output: [10, 20, 30, 40, 50]

```

### Changing Array Elements

```python
numbers = [10, 20, 30, 40, 50]

# Change first element
numbers[0] = 100

print(numbers)  # [100, 20, 30, 40, 50]
```

### Adding Elements to Arrays

```python
numbers = [10, 20, 30]

# Add to end
numbers.append(40)
print(numbers)  # [10, 20, 30, 40]

# Add at specific position
numbers.insert(1, 15)
print(numbers)  # [10, 15, 20, 30, 40]
```

---

## 🔸 What are Matrices?

Matrices are tables of numbers arranged in rows and columns. Think of them as arrays of arrays. We use matrices for grids, tables, and 2D data.

### Creating Matrices

```python
# Simple 2x2 matrix
matrix = [
    [1, 2],
    [3, 4]
]

# 3x3 matrix
grid = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
```

---

## 🔸 Creating Matrices

### Creating Different Types of Matrices

```python
# Zero matrix (all zeros)
zeros = [
    [0, 0, 0],
    [0, 0, 0]
]

# Identity matrix (1s on diagonal)
identity = [
    [1, 0],
    [0, 1]
]
```

### Matrix Dimensions

```python
matrix = [
    [1, 2, 3],
    [4, 5, 6]
]

# Count rows
rows = len(matrix)  # 2

# Count columns
cols = len(matrix[0])  # 3

print(f"Matrix has {rows} rows and {cols} columns")
```

### Array Processing with Loops

```python
numbers = [10, 20, 30, 40, 50]

# Method 1: Iterate through each element
print("Iterating through elements:")
for num in numbers:
    print(num)

print()

# Method 2: Iterate using index
print("Iterating with index:")
for i in range(len(numbers)):
    print(f"Index {i}: {numbers[i]}")

print()

# Finding the maximum value
max_value = numbers[0]  # Start with first element
for num in numbers:
    if num > max_value:
        max_value = num
print(f"Maximum value: {max_value}")

print()

# Finding the sum of all elements
total = 0
for num in numbers:
    total += num
print(f"Sum of all elements: {total}")

print()

# Counting elements greater than a value
count = 0
threshold = 25
for num in numbers:
    if num > threshold:
        count += 1
print(f"Elements greater than {threshold}: {count}")

print()

# Creating a new array with doubled values
doubled = []
for num in numbers:
    doubled.append(num * 2)
print(f"Original: {numbers}")
print(f"Doubled: {doubled}")
```

---

## 🔸 Using Matrices

### Accessing Matrix Elements

```python
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

# Get element at row 0, column 1
element = matrix[0][1]  # 2

# Get element at row 2, column 2
corner = matrix[2][2]  # 9

# Get entire row
first_row = matrix[0]  # [1, 2, 3]
```

### Changing Matrix Elements

```python
matrix = [
    [1, 2, 3],
    [4, 5, 6]
]

# Change element at row 0, column 0
matrix[0][0] = 10

print(matrix)
# [[10, 2, 3], [4, 5, 6]]
```

### Matrix Rows and Columns

```python
matrix = [
    [1, 2, 3],
    [4, 5, 6]
]

# Get all rows
for row in matrix:
    print(row)
# [1, 2, 3]
# [4, 5, 6]

# Get first column
first_column = []
for row in matrix:
    first_column.append(row[0])

print(first_column)  # [1, 4]
```

### Functions with Type Hints

```python
# Function that works with arrays
def sum_array(numbers: list) -> int:
    """Calculate sum of numbers in array."""
    total = 0
    for num in numbers:
        total += num
    return total

# Function that works with matrices
def get_matrix_size(matrix: list) -> tuple:
    """Return (rows, columns) of matrix."""
    if not matrix:
        return (0, 0)
    return (len(matrix), len(matrix[0]))

# Usage
numbers = [1, 2, 3, 4, 5]
result = sum_array(numbers)
print(f"Sum: {result}")  # Sum: 15

grid = [[1, 2], [3, 4]]
size = get_matrix_size(grid)
print(f"Size: {size}")  # Size: (2, 2)
```

---

## 🎯 Practice Exercises

### Exercise 1: Array Basics
Create an array with numbers 1-5 and print each element.

### Exercise 2: Matrix Basics
Create a 2x2 matrix and print all elements.

### Exercise 3: Array Modification
Start with array `[1, 2, 3]`, add 4 to the end, then change the first element to 10.

### Exercise 4: Matrix Access
Create a 3x3 matrix and print the element at row 1, column 2.

---

## 🎯 Key Takeaways

1. **Arrays store multiple values** in a list
2. **Access elements by position** (starting from 0)
3. **Matrices are arrays of arrays** (rows and columns)
4. **Use simple operations** to work with data

---

**Tutorial Version**: 2.0 - Simplified
**Last Updated**: February 2026
**Estimated Reading Time**: 15 minutes