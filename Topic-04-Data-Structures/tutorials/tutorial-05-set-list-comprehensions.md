# Tutorial 5: List and Set Comprehensions

**Section**: 10 - List and Set Comprehensions (25 min)
**Level**: Beginner
**Prerequisites**: Tutorial 2 (Lists and Sets)

---

## 📋 Learning Objectives

By the end of this tutorial, you will be able to:

1. **Create lists using comprehensions** (shorter way to build lists)
2. **Create sets using comprehensions** (shorter way to build sets)
3. **Transform data simply** using basic comprehensions

---

## 📚 Table of Contents

1. [What are Comprehensions?](#what-are-comprehensions)
2. [List Comprehensions](#list-comprehensions)
3. [Set Comprehensions](#set-comprehensions)
4. [Simple Transformations](#simple-transformations)

---

## 🔸 What are Comprehensions?

Comprehensions are a short way to create lists or sets in Python. They replace longer loops with simple expressions.

### Without Comprehension (Long Way)

```python
# Create list of squares - long way
numbers = [1, 2, 3, 4, 5]
squares = []
for num in numbers:
    squares.append(num * num)
print(squares)  # [1, 4, 9, 16, 25]
```

### With Comprehension (Short Way)

```python
# Create list of squares - short way
numbers = [1, 2, 3, 4, 5]
squares = [num * num for num in numbers]
print(squares)  # [1, 4, 9, 16, 25]
```

---

## 🔸 List Comprehensions

### Basic List Comprehension

```python
# Pattern: [expression for item in list]

# Double each number
numbers = [1, 2, 3, 4]
doubled = [num * 2 for num in numbers]
print(doubled)  # [2, 4, 6, 8]

# Convert to strings
numbers = [1, 2, 3]
strings = [str(num) for num in numbers]
print(strings)  # ['1', '2', '3']

# Get string lengths
words = ["cat", "dog", "bird"]
lengths = [len(word) for word in words]
print(lengths)  # [3, 3, 4]
```

### Simple Filtering

```python
# Pattern: [expression for item in list if condition]

# Get even numbers only
numbers = [1, 2, 3, 4, 5, 6]
evens = [num for num in numbers if num % 2 == 0]
print(evens)  # [2, 4, 6]

# Get words longer than 3 letters
words = ["cat", "dog", "elephant", "bird"]
long_words = [word for word in words if len(word) > 3]
print(long_words)  # ['elephant', 'bird']
```

---

## 🔸 Set Comprehensions

### Basic Set Comprehension

```python
# Pattern: {expression for item in iterable}

# Create set of squares
numbers = [1, 2, 2, 3, 3, 3]
squares = {num * num for num in numbers}
print(squares)  # {1, 4, 9} (no duplicates!)

# Convert to uppercase
words = ["hello", "world", "hello"]
uppercase = {word.upper() for word in words}
print(uppercase)  # {'HELLO', 'WORLD'}
```

### Set Comprehension with Filtering

```python
# Pattern: {expression for item in iterable if condition}

# Get lengths of unique words
words = ["cat", "dog", "cat", "bird", "dog"]
word_lengths = {len(word) for word in words}
print(word_lengths)  # {3, 4}

# Get even numbers from mixed list
numbers = [1, 2, 3, 4, 5, 6, 7, 8]
even_set = {num for num in numbers if num % 2 == 0}
print(even_set)  # {2, 4, 6, 8}
```

---

## 🔸 Simple Transformations

### List Comprehension Examples

```python
# Add 10 to each number
numbers = [1, 2, 3]
plus_ten = [num + 10 for num in numbers]
print(plus_ten)  # [11, 12, 13]

# Get first letter of each word
words = ["Python", "Java", "C++"]
first_letters = [word[0] for word in words]
print(first_letters)  # ['P', 'J', 'C']

# Check if numbers are positive
numbers = [-1, 0, 1, 2, -3]
is_positive = [num > 0 for num in numbers]
print(is_positive)  # [False, False, True, True, False]
```

### Set Comprehension Examples

```python
# Get unique first letters
words = ["apple", "banana", "cherry", "date"]
first_letters = {word[0] for word in words}
print(first_letters)  # {'a', 'b', 'c', 'd'}

# Get unique word lengths
words = ["a", "bb", "ccc", "dddd", "eee"]
lengths = {len(word) for word in words}
print(lengths)  # {1, 2, 3, 4}
```

### Comparing Methods

```python
# Traditional way vs comprehension
numbers = [1, 2, 3, 4, 5]

# Traditional approach
squares_traditional = []
for num in numbers:
    squares_traditional.append(num ** 2)

# Comprehension approach
squares_comprehension = [num ** 2 for num in numbers]

print("Traditional:", squares_traditional)
print("Comprehension:", squares_comprehension)
# Both give: [1, 4, 9, 16, 25]
```

---

## 🎯 Practice Exercises

### Exercise 1: List Comprehension Basics
Create a list comprehension that doubles each number in [1, 2, 3, 4].

### Exercise 2: Set Comprehension Basics
Create a set comprehension that gets the first letter of each word in ["apple", "banana", "cherry"].

### Exercise 3: Simple Filtering
Use list comprehension to get numbers greater than 5 from [3, 7, 1, 9, 4, 6].

### Exercise 4: String Processing
Use list comprehension to get the length of each word in ["cat", "elephant", "dog"].

### Exercise 5: Set Uniqueness
Use set comprehension to get unique lengths from ["a", "bb", "ccc", "dd", "eee"].

---

## 🎯 Key Takeaways

1. **Comprehensions** create lists/sets in one line instead of loops
2. **List comprehensions** use `[expression for item in list]`
3. **Set comprehensions** use `{expression for item in iterable}`
4. **Add `if condition`** to filter items
5. **Sets automatically remove duplicates**

---

## 🔗 Next Steps

After this tutorial, you'll be ready to:
- Write shorter, cleaner code
- Process data more efficiently
- Use comprehensions in your programs

---

**Tutorial Version**: 1.0 - Basic Comprehensions
**Last Updated**: February 2026
**Estimated Reading Time**: 15 minutes