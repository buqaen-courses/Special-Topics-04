# Workshop 5: List and Set Comprehensions

**Section**: 10 - List and Set Comprehensions (30 min)
**Level**: Beginner
**Prerequisites**: Tutorial 5 (List and Set Comprehensions)

---

## 🎯 Workshop Objectives

By the end of this workshop, you will:

1. **Create lists using comprehensions** (shorter way to build lists)
2. **Create sets using comprehensions** (shorter way to build sets)
3. **Transform data simply** using basic comprehensions

---

## 📋 Workshop Structure

1. [Setup](#setup)
2. [Exercise 1: List Comprehensions](#exercise-1-list-comprehensions)
3. [Exercise 2: Set Comprehensions](#exercise-2-set-comprehensions)
4. [Exercise 3: Simple Transformations](#exercise-3-simple-transformations)

---

## 🛠️ Setup

Create a new Python file called `workshop_comprehensions.py` for your exercises.

---

## 🏃 Exercise 1: List Comprehensions

### Task 1.1: Basic List Comprehension
Create a list comprehension that squares each number in [1, 2, 3, 4].

```python
# TODO: Create [1, 4, 9, 16]
numbers = [1, 2, 3, 4]
squares = [num ** 2 for num in numbers]
print(squares)
```

### Task 1.2: String List Comprehension
Create a list comprehension that gets the first letter of each word in ["hello", "world", "python"].

```python
# TODO: Create ['h', 'w', 'p']
words = ["hello", "world", "python"]
first_letters = [word[0] for word in words]
print(first_letters)
```

### Task 1.3: Filtering List Comprehension
Create a list comprehension that gets even numbers from [1, 2, 3, 4, 5, 6].

```python
# TODO: Create [2, 4, 6]
numbers = [1, 2, 3, 4, 5, 6]
evens = [num for num in numbers if num % 2 == 0]
print(evens)
```

---

## 🏃 Exercise 2: Set Comprehensions

### Task 2.1: Basic Set Comprehension
Create a set comprehension that gets squares from [1, 2, 2, 3, 3, 3].

```python
# TODO: Create {1, 4, 9}
numbers = [1, 2, 2, 3, 3, 3]
squares = {num ** 2 for num in numbers}
print(squares)
```

### Task 2.2: Uppercase Set Comprehension
Create a set comprehension that converts ["a", "b", "a", "c"] to uppercase.

```python
# TODO: Create {'A', 'B', 'C'}
letters = ["a", "b", "a", "c"]
uppercase = {letter.upper() for letter in letters}
print(uppercase)
```

### Task 2.3: Length Set Comprehension
Create a set comprehension that gets unique lengths from ["a", "bb", "ccc", "dd"].

```python
# TODO: Create {1, 2, 3}
words = ["a", "bb", "ccc", "dd"]
lengths = {len(word) for word in words}
print(lengths)
```

---

## 🏃 Exercise 3: Simple Transformations

### Task 3.1: Number Transformation
Create a list comprehension that adds 100 to each number in [1, 2, 3].

```python
# TODO: Create [101, 102, 103]
numbers = [1, 2, 3]
plus_hundred = [num + 100 for num in numbers]
print(plus_hundred)
```

### Task 3.2: Word Length Filter
Create a list comprehension that gets words longer than 3 letters from ["cat", "elephant", "dog", "hippopotamus"].

```python
# TODO: Create ['elephant', 'hippopotamus']
words = ["cat", "elephant", "dog", "hippopotamus"]
long_words = [word for word in words if len(word) > 3]
print(long_words)
```

### Task 3.3: Mixed Operations
Create both a list and set comprehension from [1, 2, 3, 2, 1] that doubles each number.

```python
# TODO: List should be [2, 4, 6, 4, 2], set should be {2, 4, 6}
numbers = [1, 2, 3, 2, 1]
doubled_list = [num * 2 for num in numbers]
doubled_set = {num * 2 for num in numbers}
print("List:", doubled_list)
print("Set:", doubled_set)
```

---

**Workshop Version**: 1.0 - Basic Comprehensions
**Last Updated**: February 2026
**Estimated Time**: 30 minutes