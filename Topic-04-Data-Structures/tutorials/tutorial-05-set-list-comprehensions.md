# Tutorial 5: List and Set Comprehensions
```bash
Section: Topic-05-Data-Structures - Section 5 (Comprehensions)
Level: Beginner
Estimated Time: ~25–30 minutes
Prerequisites: Tutorial 1 (Lists), Tutorial 2 (Sets)
```
---

## Learning Objectives

By the end of this tutorial you will be able to:

- Understand what comprehensions are and why they exist
- Build lists using list comprehensions
- Build sets using set comprehensions
- Filter items using conditions inside comprehensions
- Choose between a loop and a comprehension confidently

---

## Table of Contents

1. What Are Comprehensions?
2. List Comprehensions
3. Filtering with Comprehensions
4. Set Comprehensions
5. Common Transformations
6. Loop vs Comprehension - When to Use Each
7. Common Beginner Mistakes
8. Practice Exercises
9. Key Takeaways

---

## 1. What Are Comprehensions?

A comprehension is a concise way to build a list or set from an existing sequence. Instead of writing a loop that appends items one by one, you express the whole thing in a single line.

#### Without comprehension

```python
numbers = [1, 2, 3, 4, 5]
squares = []
for num in numbers:
    squares.append(num * num)
print(squares)  ## [1, 4, 9, 16, 25]
```

#### With comprehension

```python
numbers = [1, 2, 3, 4, 5]
squares = [num * num for num in numbers]
print(squares)  ## [1, 4, 9, 16, 25]
```

Both produce the same result. The comprehension version is shorter and reads almost like plain English: "give me `num * num` for each `num` in `numbers`."

The general pattern is:
```bash
[expression   for item in iterable]
 ──────────   ────────────────────
 what to do   where to get items
```

---

#### Mini Exercise

What do you think `[num + 1 for num in [10, 20, 30]]` produces? Work it out mentally before moving on.

---

## 2. List Comprehensions

#### Basic examples

```python
## Double each number
numbers = [1, 2, 3, 4]
doubled = [num * 2 for num in numbers]
print(doubled)  ## [2, 4, 6, 8]

## Convert numbers to strings
numbers = [1, 2, 3]
as_strings = [str(num) for num in numbers]
print(as_strings)  ## ['1', '2', '3']

## Get the length of each word
words = ["cat", "dog", "bird"]
lengths = [len(word) for word in words]
print(lengths)  ## [3, 3, 4]

## Get the first letter of each word
words = ["Python", "Java", "C++"]
first_letters = [word[0] for word in words]
print(first_letters)  ## ['P', 'J', 'C']
```

#### Producing booleans

You can use any expression, including comparisons:

```python
numbers = [-1, 0, 1, 2, -3]
is_positive = [num > 0 for num in numbers]
print(is_positive)  ## [False, False, True, True, False]
```

This is useful when you want to check a condition for every item and keep the results as a list.

---

#### Mini Exercise

Write a list comprehension that adds 10 to each number in `[1, 2, 3]`.

---

## 3. Filtering with Comprehensions

You can add an `if` condition to keep only the items you want.
```bash
[expression   for item in iterable   if condition]
 ──────────   ────────────────────   ────────────
 what to do   where to get items     which to keep
```

#### Examples

```python
## Keep only even numbers
numbers = [1, 2, 3, 4, 5, 6]
evens = [num for num in numbers if num % 2 == 0]
print(evens)  ## [2, 4, 6]

## Keep only words longer than 3 letters
words = ["cat", "dog", "elephant", "bird"]
long_words = [word for word in words if len(word) > 3]
print(long_words)  ## ['elephant', 'bird']

## Keep only positive numbers
numbers = [-3, -1, 0, 2, 5]
positives = [num for num in numbers if num > 0]
print(positives)  ## [2, 5]
```

#### Combining transformation and filtering

The expression and the condition are independent - you can transform and filter at the same time:

```python
## Square only the even numbers
numbers = [1, 2, 3, 4, 5, 6]
even_squares = [num ** 2 for num in numbers if num % 2 == 0]
print(even_squares)  ## [4, 16, 36]
```

---

#### Mini Exercise

Write a list comprehension that keeps only numbers greater than 5 from `[3, 7, 1, 9, 4, 6]`.

---

## 4. Set Comprehensions

Set comprehensions work exactly like list comprehensions, but use curly braces `{}` and produce a set. Because sets do not allow duplicates, repeated values are automatically removed.

`{expression   for item in iterable}`


#### Basic examples

```python
## Squares - duplicates removed automatically
numbers = [1, 2, 2, 3, 3, 3]
squares = {num * num for num in numbers}
print(squares)  ## {1, 4, 9}

## Unique uppercase words
words = ["hello", "world", "hello"]
uppercase = {word.upper() for word in words}
print(uppercase)  ## {'HELLO', 'WORLD'}

## Unique first letters
words = ["apple", "banana", "cherry", "date"]
first_letters = {word[0] for word in words}
print(first_letters)  ## {'a', 'b', 'c', 'd'}
```

#### With filtering

```python
## Unique lengths of words
words = ["cat", "dog", "cat", "bird", "dog"]
word_lengths = {len(word) for word in words}
print(word_lengths)  ## {3, 4}

## Unique even numbers
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 2, 4]
even_set = {num for num in numbers if num % 2 == 0}
print(even_set)  ## {2, 4, 6, 8}
```

Note: sets are unordered, so the printed order may vary each time you run the code.

---

#### Mini Exercise

Write a set comprehension that gets unique lengths from `["a", "bb", "ccc", "dd", "eee"]`.

---

## 5. Common Transformations

Here are patterns you will use often:

#### String operations

```python
names = ["alice", "bob", "charlie"]

## Capitalize each name
capitalized = [name.capitalize() for name in names]
print(capitalized)  ## ['Alice', 'Bob', 'Charlie']

## Uppercase
upper = [name.upper() for name in names]
print(upper)  ## ['ALICE', 'BOB', 'CHARLIE']

## Keep only names longer than 3 characters
long_names = [name for name in names if len(name) > 3]
print(long_names)  ## ['alice', 'charlie']
```

#### Working with ranges

```python
## Squares of 1 through 5
squares = [n ** 2 for n in range(1, 6)]
print(squares)  ## [1, 4, 9, 16, 25]

## Even numbers from 0 to 9
evens = [n for n in range(10) if n % 2 == 0]
print(evens)  ## [0, 2, 4, 6, 8]

## Unique squares - same result here since range has no duplicates
unique_squares = {n ** 2 for n in range(1, 6)}
print(unique_squares)  ## {1, 4, 9, 16, 25}
```

#### Extracting data from a list of dictionaries

```python
students = [
    {"name": "Alice", "grade": 90},
    {"name": "Bob",   "grade": 75},
    {"name": "Carol", "grade": 88},
]

## Get all names
names = [s["name"] for s in students]
print(names)  ## ['Alice', 'Bob', 'Carol']

## Get names of students who passed (grade >= 80)
passed = [s["name"] for s in students if s["grade"] >= 80]
print(passed)  ## ['Alice', 'Carol']
```

---

## 6. Loop vs Comprehension - When to Use Each
```bash
Situation                                    Prefer
──────────────────────────────────────────────────────────────
Simple transformation or filtering           comprehension
Result fits on one readable line             comprehension
You need side effects (print, write file)    for loop
Logic is complex or multi-step               for loop
You need to break or continue early          for loop
Building something other than a list/set     for loop
```

#### Example - when a loop is clearer

```python
## This is getting hard to read as a comprehension
result = [process(item) for item in data if validate(item) and item is not None]

## A loop is more readable here
result = []
for item in data:
    if item is not None and validate(item):
        result.append(process(item))
```

Comprehensions are a tool, not a rule. If the one-liner is hard to read, use a loop.

---

## 7. Common Beginner Mistakes

#### Mistake 1 - Using a set comprehension when order matters

```python
## Sets are unordered - do not use them when position matters
letters = {word[0] for word in ["banana", "apple", "cherry"]}
print(letters)  ## could print in any order: {'b', 'a', 'c'}
```

Use a list comprehension if order matters.

#### Mistake 2 - Confusing `[]` and `{}`

```python
## List comprehension - preserves order, allows duplicates
result = [num * 2 for num in [1, 2, 2, 3]]
print(result)   ## [2, 4, 4, 6]

## Set comprehension - no order, no duplicates
result = {num * 2 for num in [1, 2, 2, 3]}
print(result)   ## {2, 4, 6}
```

#### Mistake 3 - Putting the condition in the wrong place

```python
## Wrong - condition is part of the expression, not a filter
result = [num if num > 0 for num in numbers]   ## SyntaxError

## Correct - condition comes after the for clause
result = [num for num in numbers if num > 0]
```

#### Mistake 4 - Making comprehensions too complex

```python
## Hard to read - better as a loop
result = [x * y for x in range(5) for y in range(5) if x != y if x + y > 4]
```

If you need nested loops or multiple conditions, a regular loop is usually clearer.

#### Mistake 5 - Forgetting that sets are unordered in output

```python
numbers = [3, 1, 4, 1, 5, 9, 2, 6]
unique = {num for num in numbers}
print(unique)  ## order is not guaranteed - do not rely on it
```

---

## 8. Practice Exercises

#### Exercise 1

Create a list comprehension that doubles each number in `[1, 2, 3, 4]`.

#### Exercise 2

Create a set comprehension that gets the first letter of each word in `["apple", "banana", "cherry"]`.

#### Exercise 3

Use a list comprehension to keep only numbers greater than 5 from `[3, 7, 1, 9, 4, 6]`.

#### Exercise 4

Use a list comprehension to get the length of each word in `["cat", "elephant", "dog"]`.

#### Exercise 5

Use a set comprehension to get unique lengths from `["a", "bb", "ccc", "dd", "eee"]`.

#### Exercise 6

Given `students = [{"name": "Alice", "grade": 90}, {"name": "Bob", "grade": 70}, {"name": "Carol", "grade": 85}]`, use a list comprehension to get the names of students with a grade above 80.

#### Exercise 7

Use a list comprehension with `range(1, 11)` to produce a list of squares for odd numbers only: $[1, 9, 25, 49, 81]$.

---

## 9. Key Takeaways

- list comprehensions use `[expression for item in iterable]`
- set comprehensions use `{expression for item in iterable}`
- add `if condition` after the `for` clause to filter items
- sets automatically remove duplicates and have no guaranteed order
- comprehensions are best for simple, readable one-liners - use a loop when logic gets complex
- you can transform and filter in the same comprehension

---

## Quick Reference
```bash
Pattern                                          Result
──────────────────────────────────────────────────────────────────────
[expr for x in lst]                              list, all items
[expr for x in lst if cond]                      list, filtered
{expr for x in lst}                              set, no duplicates
{expr for x in lst if cond}                      set, filtered
[x for x in range(n)]                            list from range
{x for x in range(n)}                            set from range
```