# Workshop 5: List and Set Comprehensions
```bash
Section: Topic-05-Data-Structures -  Workshop 5
Level: Beginner
Estimated Time: ~35 minutes
Prerequisites: Tutorial 5 (List and Set Comprehensions)
```

---

## Workshop Objectives

By the end of this workshop you will be able to:

- Build lists using list comprehensions
- Build sets using set comprehensions
- Filter items with conditions inside comprehensions
- Combine transformation and filtering in one line
- Choose confidently between a loop and a comprehension

---

## Workshop Structure

1. Warm-Up -  Reading Code
2. Exercise 1: Basic List Comprehensions
3. Exercise 2: Filtering with List Comprehensions
4. Exercise 3: Set Comprehensions
5. Exercise 4: Common Transformations
6. Exercise 5: Loop vs Comprehension
7. Exercise 6: Working with Dictionaries
8. Challenge Exercise

---

## Setup

Create a new file called `workshop_comprehensions.py`. Make sure you are running Python 3.8 or later.

---

## 1. Warm-Up -  Reading Code

Read the code below and answer the questions before running it.

```python
numbers = [1, 2, 3, 4, 5, 6]

result_a = [num * 3 for num in numbers]

result_b = [num for num in numbers if num % 2 != 0]

result_c = [num ** 2 for num in numbers if num > 3]

result_d = {num % 3 for num in numbers}

words = ["hello", "world", "python", "code"]
result_e = [word.upper() for word in words if len(word) > 4]

print(result_a)
print(result_b)
print(result_c)
print(result_d)
print(result_e)
```

Questions -  write your answers as comments first:

- What does `result_a` contain?
- What does `result_b` contain? What is the filter doing?
- What does `result_c` contain? What are the two steps happening?
- What type is `result_d`? What values does it contain?
- What does `result_e` contain? Why is `"code"` excluded?

Run the code and check your predictions.

---

## 2. Exercise 1: Basic List Comprehensions

#### Task 1.1 -  Triple Each Number

Write a list comprehension that multiplies each number by 3.

```python
numbers = [1, 2, 3, 4, 5]

## TODO: list comprehension → triple each number
tripled = ...

print(tripled)  ## [3, 6, 9, 12, 15]
```

---

#### Task 1.2 -  Convert to Strings

Write a list comprehension that converts each number to a string.

```python
numbers = [10, 20, 30, 40]

## TODO: list comprehension → convert each to str
as_strings = ...

print(as_strings)  ## ['10', '20', '30', '40']
```

---

#### Task 1.3 -  Word Lengths

Write a list comprehension that returns the length of each word.

```python
words = ["cat", "elephant", "dog", "butterfly"]

## TODO: list comprehension → length of each word
lengths = ...

print(lengths)  ## [3, 8, 3, 9]
```

---

#### Task 1.4 -  Boolean Check

Write a list comprehension that checks whether each number is even. The result should be a list of booleans.

```python
numbers = [1, 2, 3, 4, 5, 6]

## TODO: list comprehension → True if even, False if odd
is_even = ...

print(is_even)  ## [False, True, False, True, False, True]
```

---

#### Task 1.5 -  First Letters

Write a list comprehension that extracts the first letter of each word.

```python
words = ["Python", "Java", "C++", "Rust"]

## TODO: list comprehension → first letter of each word
first_letters = ...

print(first_letters)  ## ['P', 'J', 'C', 'R']
```

---

## 3. Exercise 2: Filtering with List Comprehensions

#### Task 2.1 -  Keep Odd Numbers

Write a list comprehension that keeps only odd numbers.

```python
numbers = [1, 2, 3, 4, 5, 6, 7, 8]

## TODO: keep only odd numbers
odds = ...

print(odds)  ## [1, 3, 5, 7]
```

---

#### Task 2.2 -  Short Words Only

Write a list comprehension that keeps only words with 3 or fewer characters.

```python
words = ["cat", "elephant", "dog", "ox", "butterfly"]

## TODO: keep words with length <= 3
short_words = ...

print(short_words)  ## ['cat', 'dog', 'ox']
```

---

#### Task 2.3 -  Filter and Transform Together

Write a list comprehension that squares only the odd numbers.

```python
numbers = [1, 2, 3, 4, 5, 6]

## TODO: square only the odd numbers
odd_squares = ...

print(odd_squares)  ## [1, 9, 25]
```

---

#### Task 2.4 -  Negative Numbers Only

Write a list comprehension that keeps only negative numbers, then makes them positive (absolute value).

```python
numbers = [-3, -1, 0, 2, -5, 4]

## TODO: keep negatives and convert to positive
positives = ...

print(positives)  ## [3, 1, 5]
```

---

#### Task 2.5 -  Predict the Output

Read the code below. Write your prediction as a comment, then run it.

```python
data = [10, 15, 20, 25, 30]

result = [x // 5 for x in data if x > 12]
print(result)
```

- What does `x // 5` do?
- Which items are filtered out?
- What is the final list?

---

## 4. Exercise 3: Set Comprehensions

#### Task 3.1 -  Unique Squares

Write a set comprehension that produces unique squares. Notice the input has duplicates.

```python
numbers = [1, 2, 2, 3, 3, 3, 4]

## TODO: set comprehension → unique squares
unique_squares = ...

print(unique_squares)  ## {1, 4, 9, 16}
```

---

#### Task 3.2 -  Unique First Letters

Write a set comprehension that collects unique first letters from the word list.

```python
words = ["apple", "banana", "avocado", "blueberry", "cherry"]

## TODO: set comprehension → unique first letters
first_letters = ...

print(first_letters)  ## {'a', 'b', 'c'}  (order may vary)
```

---

#### Task 3.3 -  Unique Word Lengths

Write a set comprehension that collects unique word lengths.

```python
words = ["cat", "dog", "bird", "fish", "elephant"]

## TODO: set comprehension → unique lengths
unique_lengths = ...

print(unique_lengths)  ## {3, 4, 8}  (order may vary)
```

---

#### Task 3.4 -  Unique Even Numbers

Write a set comprehension that keeps only even numbers. The input has duplicates.

```python
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 2, 4, 6]

## TODO: set comprehension → unique even numbers
even_set = ...

print(even_set)  ## {2, 4, 6, 8}  (order may vary)
```

---

#### Task 3.5 -  List vs Set

Run both versions below and observe the difference.

```python
numbers = [1, 2, 2, 3, 3, 3]

list_result = [num * 2 for num in numbers]
set_result  = {num * 2 for num in numbers}

print(list_result)
print(set_result)
```

Write a comment explaining:
- Why do the two results differ in length?
- When would you choose the set version?
- When would you choose the list version?

---

## 5. Exercise 4: Common Transformations

#### Task 4.1 -  Capitalize Names

Write a list comprehension that capitalizes each name.

```python
names = ["alice", "bob", "charlie", "diana"]

## TODO: capitalize each name
capitalized = ...

print(capitalized)  ## ['Alice', 'Bob', 'Charlie', 'Diana']
```

---

#### Task 4.2 -  Squares from a Range

Use `range` inside a list comprehension to produce squares of numbers 1 through 6.

```python
## TODO: squares of 1 through 6 using range
squares = ...

print(squares)  ## [1, 4, 9, 16, 25, 36]
```

---

#### Task 4.3 -  Even Numbers from a Range

Use `range(1, 21)` and a filter to produce only even numbers.

```python
## TODO: even numbers from 1 to 20
evens = ...

print(evens)  ## [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
```

---

#### Task 4.4 -  Multiples of 3

Use `range(1, 31)` to produce multiples of 3 up to 30.

```python
## TODO: multiples of 3 from 1 to 30
multiples = ...

print(multiples)  ## [3, 6, 9, 12, 15, 18, 21, 24, 27, 30]
```

---

#### Task 4.5 -  Odd Squares from a Range

Use `range(1, 11)` to produce squares of odd numbers only.

```python
## TODO: squares of odd numbers from 1 to 10
odd_squares = ...

print(odd_squares)  ## [1, 9, 25, 49, 81]
```

---

## 6. Exercise 5: Loop vs Comprehension

#### Task 5.1 -  Rewrite a Loop as a Comprehension

Rewrite the loop below as a list comprehension.

```python
numbers = [1, 2, 3, 4, 5]
result = []
for num in numbers:
    result.append(num + 10)

## TODO: rewrite as a list comprehension
result = ...

print(result)  ## [11, 12, 13, 14, 15]
```

---

#### Task 5.2 -  Rewrite a Filtered Loop

Rewrite the loop below as a list comprehension.

```python
words = ["hi", "hello", "hey", "howdy", "ok"]
result = []
for word in words:
    if word.startswith("h"):
        result.append(word.upper())

## TODO: rewrite as a list comprehension
result = ...

print(result)  ## ['HI', 'HELLO', 'HEY', 'HOWDY']
```

---

#### Task 5.3 -  Rewrite a Comprehension as a Loop

Rewrite the comprehension below as a regular for loop.

```python
numbers = [1, 2, 3, 4, 5, 6]
result = [num ** 2 for num in numbers if num % 2 == 0]

## TODO: rewrite as a for loop
result = []
## ...

print(result)  ## [4, 16, 36]
```

---

#### Task 5.4 -  Choose the Right Tool

For each situation below, write a comment saying whether you would use a comprehension or a loop and why.

```python
## Situation 1: print each item in a list as you process it
## Situation 2: build a list of squares from a range
## Situation 3: read lines from a file and stop at a blank line
## Situation 4: collect unique first letters from a list of words
## Situation 5: build a result that requires 3 nested conditions and a helper function call
```

---

## 7. Exercise 6: Working with Dictionaries

#### Task 6.1 -  Extract Names

Use a list comprehension to extract all names from the list of dictionaries.

```python
students = [
    {"name": "Alice",   "grade": 90},
    {"name": "Bob",     "grade": 72},
    {"name": "Carol",   "grade": 85},
    {"name": "David",   "grade": 60},
]

## TODO: list comprehension → all names
names = ...

print(names)  ## ['Alice', 'Bob', 'Carol', 'David']
```

---

#### Task 6.2 -  Filter by Grade

Use a list comprehension to get names of students who passed (grade $\geq$ 75).

```python
students = [
    {"name": "Alice",   "grade": 90},
    {"name": "Bob",     "grade": 72},
    {"name": "Carol",   "grade": 85},
    {"name": "David",   "grade": 60},
]

## TODO: list comprehension → names of students with grade >= 75
passed = ...

print(passed)  ## ['Alice', 'Carol']
```

---

#### Task 6.3 -  Unique Grades

Use a set comprehension to collect unique grade values.

```python
students = [
    {"name": "Alice",   "grade": 90},
    {"name": "Bob",     "grade": 72},
    {"name": "Carol",   "grade": 90},
    {"name": "David",   "grade": 72},
    {"name": "Eve",     "grade": 85},
]

## TODO: set comprehension → unique grades
unique_grades = ...

print(unique_grades)  ## {72, 85, 90}  (order may vary)
```

---

#### Task 6.4 -  Grade Labels

Use a list comprehension to produce a label for each student. If grade $\geq$ 80 the label is `"Pass"`, otherwise `"Fail"`. Use a conditional expression inside the comprehension: `"Pass" if ... else "Fail"`.

```python
students = [
    {"name": "Alice",   "grade": 90},
    {"name": "Bob",     "grade": 72},
    {"name": "Carol",   "grade": 85},
    {"name": "David",   "grade": 60},
]

## TODO: list comprehension → "Pass" or "Fail" for each student
labels = ...

print(labels)  ## ['Pass', 'Fail', 'Pass', 'Fail']
```

---

## 8. Challenge Exercise

#### Task -  Student Report

You are given a list of students. Complete all four tasks using comprehensions only -  no loops.

```python
students = [
    {"name": "Alice",   "grade": 92, "subject": "Math"},
    {"name": "Bob",     "grade": 68, "subject": "Science"},
    {"name": "Carol",   "grade": 85, "subject": "Math"},
    {"name": "David",   "grade": 55, "subject": "History"},
    {"name": "Eve",     "grade": 78, "subject": "Science"},
    {"name": "Frank",   "grade": 91, "subject": "History"},
    {"name": "Grace",   "grade": 73, "subject": "Math"},
]

## Task A: list of all names in uppercase
all_names = ...
print(all_names)
## ['ALICE', 'BOB', 'CAROL', 'DAVID', 'EVE', 'FRANK', 'GRACE']

## Task B: names of students who scored above 80
high_scorers = ...
print(high_scorers)
## ['Alice', 'Carol', 'Frank']

## Task C: set of unique subjects
subjects = ...
print(subjects)
## {'Math', 'Science', 'History'}  (order may vary)

## Task D: list of strings in the format "Name: grade"
##         but only for students who passed (grade >= 70)
report = ...
print(report)
## ['Alice: 92', 'Carol: 85', 'Eve: 78', 'Frank: 91', 'Grace: 73']
```

---

## Key Takeaways

- list comprehensions use `[expression for item in iterable]`
- set comprehensions use `{expression for item in iterable}` and remove duplicates automatically
- add `if condition` after the `for` clause to filter items
- transformation and filtering can happen in the same comprehension
- sets have no guaranteed order -  do not rely on position
- use a loop when you need side effects, early exit, or the logic gets hard to read on one line
- `"Pass" if condition else "Fail"` inside a comprehension lets you map values without filtering