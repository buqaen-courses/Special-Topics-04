# Homework 5: List and Set Comprehensions

**Section**: 10 - List and Set Comprehensions (25 min)
**Level**: Beginner
**Prerequisites**: Tutorial 5 (List and Set Comprehensions)

---

## 🎯 Assignment Objectives

By completing this homework, you will:

1. **Create lists using comprehensions** (shorter way to build lists)
2. **Create sets using comprehensions** (shorter way to build sets)
3. **Transform data simply** using basic comprehensions

---

## 📋 Assignment Structure

Complete 4 simple tasks:

1. [Task 1: List Comprehensions](#task-1-list-comprehensions)
2. [Task 2: Set Comprehensions](#task-2-set-comprehensions)
3. [Task 3: Filtering](#task-3-filtering)
4. [Task 4: Mixed Operations](#task-4-mixed-operations)

---

## 🏃 Task 1: List Comprehensions

**Objective:** Practice basic list comprehensions.

Create a Python file `homework_05_comprehensions.py` with the following functions:

### Function 1: Double Numbers
Write a function that doubles each number in a list using list comprehension.

```python
def double_numbers(nums: list) -> list:
    # TODO: Return list with each number doubled
    pass

# Test your function
result = double_numbers([1, 2, 3])
print(result)  # Should print [2, 4, 6]
```

### Function 2: String Lengths
Write a function that gets the length of each string in a list.

```python
def string_lengths(words: list) -> list:
    # TODO: Return list of lengths for each word
    pass

# Test your function
result = string_lengths(["cat", "elephant", "dog"])
print(result)  # Should print [3, 8, 3]
```

### Function 3: Convert to Uppercase
Write a function that converts each string to uppercase.

```python
def to_uppercase(words: list) -> list:
    # TODO: Return list with all strings uppercase
    pass

# Test your function
result = to_uppercase(["hello", "world"])
print(result)  # Should print ['HELLO', 'WORLD']
```

---

## 🏃 Task 2: Set Comprehensions

**Objective:** Practice basic set comprehensions.

### Function 4: Unique Squares
Write a function that returns unique squares from a list of numbers.

```python
def unique_squares(nums: list) -> set:
    # TODO: Return set of unique squares
    pass

# Test your function
result = unique_squares([1, 2, 2, 3, 3, 3])
print(result)  # Should print {1, 4, 9}
```

### Function 5: Unique First Letters
Write a function that returns unique first letters from a list of words.

```python
def unique_first_letters(words: list) -> set:
    # TODO: Return set of unique first letters
    pass

# Test your function
result = unique_first_letters(["apple", "banana", "cherry", "date"])
print(result)  # Should print {'a', 'b', 'c', 'd'}
```

---

## 🏃 Task 3: Filtering

**Objective:** Practice comprehensions with filtering.

### Function 6: Even Numbers Only
Write a function that returns only even numbers from a list.

```python
def get_even_numbers(nums: list) -> list:
    # TODO: Return list of even numbers only
    pass

# Test your function
result = get_even_numbers([1, 2, 3, 4, 5, 6])
print(result)  # Should print [2, 4, 6]
```

### Function 7: Long Words Only
Write a function that returns words longer than 4 letters.

```python
def get_long_words(words: list) -> list:
    # TODO: Return words longer than 4 letters
    pass

# Test your function
result = get_long_words(["cat", "elephant", "dog", "hippopotamus"])
print(result)  # Should print ['elephant', 'hippopotamus']
```

---

## 🏃 Task 4: Mixed Operations

**Objective:** Combine different comprehension techniques.

### Function 8: Numbers Greater Than Average
Write a function that returns numbers greater than the average.

```python
def above_average(nums: list) -> list:
    # TODO: Return numbers above the list's average
    pass

# Test your function
result = above_average([1, 3, 5, 7, 9])
print(result)  # Should print [7, 9]
```

### Function 9: Unique Word Lengths
Write a function that returns unique lengths of words starting with a vowel.

```python
def vowel_word_lengths(words: list) -> set:
    # TODO: Return unique lengths of words starting with A, E, I, O, U
    pass

# Test your function
result = vowel_word_lengths(["apple", "cat", "elephant", "dog", "owl"])
print(result)  # Should print {3, 5} (apple=5, elephant=8, owl=3)
```

---

## 📝 Submission Instructions

1. Create `homework_05_comprehensions.py` with all 9 functions
2. Test each function with the provided examples
3. Submit your Python file

---

## ✅ Grading Criteria

- **Function 1-3:** List comprehensions (30 points)
- **Function 4-5:** Set comprehensions (20 points)
- **Function 6-7:** Filtering comprehensions (25 points)
- **Function 8-9:** Mixed operations (20 points)
- **Code quality:** Clear, readable code (5 points)

**Total: 100 points**

---

**Homework Version**: 1.0 - Basic Comprehensions
**Last Updated**: February 2026