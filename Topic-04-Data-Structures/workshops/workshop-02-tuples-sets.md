# Workshop 2: Tuples and Sets
```bash
Section: Topic-04-Data-Structures - Workshop 2
Level: Beginner
Estimated Time: ~45 minutes
Prerequisites: Tutorial 2 (Tuples and Sets)
```
---

## Workshop Objectives

By the end of this workshop you will be able to:

- Create and access tuples confidently
- Use tuple packing and unpacking in real scenarios
- Create sets and use add, remove, and membership operations
- Apply set operations (union, intersection, difference, symmetric difference)
- Choose between list, tuple, and set for a given problem

---

## Workshop Structure

1. Warm-Up - Reading Code
2. Exercise 1: Tuple Basics
3. Exercise 2: Tuple Packing and Unpacking
4. Exercise 3: Set Basics
5. Exercise 4: Set Operations
6. Exercise 5: Processing Problems
7. Challenge Exercise

---

## Setup

Create a new file called `workshop_tuples_sets.py` for all your exercises. Run it after each task to check your output.

---

## 1. Warm-Up - Reading Code

Read the code below and answer the questions before running it.

```python
point = (10, 20, 30)

print(point[0])
print(point[-1])
print(point[1:])

x, y, z = point
print(x + z)

s = {3, 1, 2, 2, 1}
print(len(s))
print(5 in s)
```

Questions - write your answers as comments first:

- What does `point[0]` print?
- What does `point[-1]` print?
- What does `point[1:]` print?
- What does `x + z` print?
- What does `len(s)` print? Why?
- What does `5 in s` print?

Run the code and check your predictions.

---

## 2. Exercise 1: Tuple Basics

#### Task 1.1 - Create and Access

Create a tuple called `colors` containing `"red"`, `"green"`, `"blue"`. Print the first and last element using both positive and negative indexing.

```python
## TODO: Create colors tuple
## TODO: Print first element using index 0
## TODO: Print last element using index -1
```

Expected output:
red
blue


---

#### Task 1.2 - Single-Element Tuple

Predict what each line prints, then run to verify:

```python
a = (42)
b = (42,)

print(type(a))
print(type(b))
print(len(b))
```

Write your predictions as comments before running.

---

#### Task 1.3 - Slicing a Tuple

Given:

```python
numbers = (10, 20, 30, 40, 50)
```

Write slices to produce each result:

```python
## TODO: Print first 3 elements       → (10, 20, 30)
## TODO: Print last 2 elements        → (40, 50)
## TODO: Print every other element    → (10, 30, 50)
## TODO: Print reversed               → (50, 40, 30, 20, 10)
```

---

#### Task 1.4 - Looping with enumerate()

Loop through `(2, 4, 6, 8)` using `enumerate()` and print each index and value. Start counting from 1.

```python
## TODO: Loop with enumerate, start=1
```

Expected output:
1 2
2 4
3 6
4 8


---

#### Task 1.5 - Immutability Check

Run this code and explain the error in a comment:

```python
t = (1, 2, 3)
t[0] = 99
```

Then show that a tuple containing a list still allows the list to be modified:

```python
t = ([1, 2], 3)
## TODO: append 99 to t[0] and print t
```

Expected output:
([1, 2, 99], 3)


---

## 3. Exercise 2: Tuple Packing and Unpacking

#### Task 2.1 - Basic Unpacking

Unpack the tuple below into three variables and print each one:

```python
person = ("Alice", 30, "Cairo")

## TODO: Unpack into name, age, city
## TODO: Print each variable
```

Expected output:
Alice
30
Cairo


---

#### Task 2.2 - Extended Unpacking

Use `*` to unpack the first element and collect the rest:

```python
scores = (95, 80, 70, 65, 55)

## TODO: Unpack first into 'top', rest into 'others'
## TODO: Print top and others
```

Expected output:
95
[80, 70, 65, 55]


---

#### Task 2.3 - Swap Variables

Use tuple unpacking to swap `a` and `b` without a temporary variable:

```python
a = 100
b = 200

## TODO: Swap a and b
print(a, b)   ## Expected: 200 100
```

---

#### Task 2.4 - Function Returning a Tuple

Write a function that takes a list of numbers and returns a tuple containing the minimum and maximum values. Do not use `min()` or `max()`.

```python
def min_max(numbers: list) -> tuple:
    """Return (min, max) of the list."""
    ## TODO: implement
    pass

low, high = min_max([4, 1, 9, 2, 7])
print(low, high)   ## 1 9
```

---

## 4. Exercise 3: Set Basics

#### Task 3.1 - Create a Set and Check Type

```python
## TODO: Create a set called 'fruits' with "apple", "banana", "mango"
## TODO: Print the set and its type
```

---

#### Task 3.2 - Empty Set Trap

Predict what each line prints, then run to verify:

```python
a = {}
b = set()

print(type(a))
print(type(b))
```

Write your predictions as comments first.

---

#### Task 3.3 - Duplicates Are Ignored

Create a set from the list below and print the result:

```python
tags = ["python", "tutorial", "python", "beginner", "tutorial"]

## TODO: Convert to set and print
```

Expected output (order may vary):
{'python', 'tutorial', 'beginner'}


---

#### Task 3.4 - Adding and Removing

Start with `numbers = {1, 2, 3}` and follow the steps:

```python
numbers = {1, 2, 3}

## Step 1: add 4
## Step 2: add 2 again (observe: no change)
## Step 3: update with [5, 6]
## Step 4: remove 3 using discard()
## Step 5: try to discard 99 (observe: no error)

## TODO: Print after each step
```

Expected output after each step:
```bash
{1, 2, 3, 4}
{1, 2, 3, 4}
{1, 2, 3, 4, 5, 6}
{1, 2, 4, 5, 6}
{1, 2, 4, 5, 6}
```

---

#### Task 3.5 - Membership Testing

Given:

```python
allowed_users = {"alice", "bob", "carol"}
```

Check whether each name below is in the set and print a message:

```python
names_to_check = ["alice", "dave", "carol", "eve"]

## TODO: Loop through names_to_check
## TODO: Print "alice: allowed" or "alice: not allowed" for each
```

Expected output:
```bash
alice: allowed
dave: not allowed
carol: allowed
eve: not allowed
```

---

## 5. Exercise 4: Set Operations

Use these two sets for all tasks in this exercise:

```python
A = {1, 2, 3, 4, 5}
B = {4, 5, 6, 7, 8}
```

#### Task 4.1 - Union

Print all elements from both sets combined. Use both the `|` operator and the `.union()` method and confirm they give the same result.

```python
## TODO: Print A | B
## TODO: Print A.union(B)
```

Expected output:
```bash
{1, 2, 3, 4, 5, 6, 7, 8}
```

---

#### Task 4.2 - Intersection

Print only the elements present in both sets.

```python
## TODO: Print A & B
```

Expected output:
{4, 5}


---

#### Task 4.3 - Difference

Print elements in A that are not in B, then elements in B that are not in A.

```python
## TODO: Print A - B
## TODO: Print B - A
```

Expected output:
```bash
{1, 2, 3}
{6, 7, 8}
```

---

#### Task 4.4 - Symmetric Difference

Print elements that are in either set but not in both.

```python
## TODO: Print A ^ B
```

Expected output:
```bash
{1, 2, 3, 6, 7, 8}
```

---

#### Task 4.5 - Student Enrollment

```python
students_math    = {"Ali", "Sara", "John", "Mia"}
students_science = {"Sara", "John", "Omar", "Lena"}
```

Use set operations to find:

```python
## TODO: Students enrolled in both classes
## TODO: All students across both classes
## TODO: Students only in math (not in science)
## TODO: Students in exactly one class (not both)
```

Expected output (order may vary):
```bash
Both:        {'Sara', 'John'}
All:         {'Ali', 'Sara', 'John', 'Mia', 'Omar', 'Lena'}
Math only:   {'Ali', 'Mia'}
Exactly one: {'Ali', 'Mia', 'Omar', 'Lena'}
```

---

## 6. Exercise 5: Processing Problems

#### Task 5.1 - Remove Duplicates, Preserve Order

Write a function that removes duplicates from a list while keeping the original order.

```python
def remove_duplicates(items: list) -> list:
    """Return a new list with duplicates removed, order preserved."""
    ## TODO: implement using dict.fromkeys()
    pass

print(remove_duplicates([3, 1, 2, 1, 3, 4]))   ## [3, 1, 2, 4]
print(remove_duplicates(["a", "b", "a", "c"]))  ## ['a', 'b', 'c']
```

---

#### Task 5.2 - Count Unique Elements

Write a function that returns the number of unique elements in a list.

```python
def count_unique(items: list) -> int:
    """Return the number of unique elements."""
    ## TODO: implement
    pass

print(count_unique([1, 2, 2, 3, 3, 3]))   ## 3
print(count_unique(["a", "a", "b"]))       ## 2
```

---

#### Task 5.3 - Common Elements

Write a function that returns the elements common to two lists.

```python
def common_elements(a: list, b: list) -> set:
    """Return elements that appear in both lists."""
    ## TODO: implement using set intersection
    pass

print(common_elements([1, 2, 3, 4], [3, 4, 5, 6]))   ## {3, 4}
print(common_elements(["x", "y"], ["y", "z"]))         ## {'y'}
```

---

#### Task 5.4 - GPS Coordinates as Tuple Keys

Store city names in a dictionary using coordinate tuples as keys. Then look up a city by its coordinates.

```python
locations = {
    (40.7128, -74.0060): "New York",
    (51.5074, -0.1278):  "London",
    (35.6762, 139.6503): "Tokyo",
}

## TODO: Print the city at coordinates (51.5074, -0.1278)
## TODO: Loop through the dictionary and print each coordinate and city name
```

Expected output:
```bash
London
(40.7128, -74.006) → New York
(51.5074, -0.1278) → London
(35.6762, 139.6503) → Tokyo
```

---

## 7. Challenge Exercise

#### Task - Analyze Two Word Lists

You are given two lists of words. Use tuples and sets to answer several questions about them.

```python
text_a = ["the", "cat", "sat", "on", "the", "mat", "the"]
text_b = ["the", "dog", "sat", "on", "the", "log", "sat"]
```

Complete each task:

```python
## Task 1: Find the unique words in text_a
## Task 2: Find the unique words in text_b
## Task 3: Find words that appear in both texts
## Task 4: Find words that appear in text_a but not text_b
## Task 5: Find words that appear in exactly one of the two texts
```

Expected output (order may vary):
```bash
Unique in A:    {'the', 'cat', 'sat', 'on', 'mat'}
Unique in B:    {'the', 'dog', 'sat', 'on', 'log'}
In both:        {'the', 'sat', 'on'}
Only in A:      {'cat', 'mat'}
Exactly one:    {'cat', 'mat', 'dog', 'log'}
```

Then write a function that takes two word lists and returns all five results as a tuple:

```python
def analyze_texts(a: list, b: list) -> tuple:
    """Return (unique_a, unique_b, both, only_a, exactly_one)."""
    ## TODO: implement
    pass

results = analyze_texts(text_a, text_b)
unique_a, unique_b, both, only_a, exactly_one = results

print("Unique in A:  ", unique_a)
print("Unique in B:  ", unique_b)
print("In both:      ", both)
print("Only in A:    ", only_a)
print("Exactly one:  ", exactly_one)
```

---

## Key Takeaways

- tuples are immutable - use them for fixed data or dictionary keys
- single-element tuples need a trailing comma: `(5,)` not `(5)`
- unpacking assigns tuple elements to variables in one line
- `*` in unpacking captures remaining elements into a list
- sets store only unique, hashable elements - no duplicates, no order
- always use `set()` for an empty set, never `{}`
- `discard()` is safe when you are unsure if the element exists
- set operations mirror math: $\cup$ union, $\cap$ intersection, $\setminus$ difference, $\triangle$ symmetric difference
- membership testing in sets is $O(1)$ on average - much faster than lists for large data