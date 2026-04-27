# Workshop 1: Lists and Matrices
```bash
Section: Topic-01-Data-Structures — Workshop 1
Level: Beginner
Estimated Time: ~45 minutes
Prerequisites: Tutorial 1 (Lists and Matrices)
```
---

## Workshop Objectives

By the end of this workshop you will be able to:

- Create and access lists and matrices confidently
- Modify lists using append, insert, remove, and pop
- Use slicing to extract parts of a list
- Loop through lists and matrices
- Write functions that process lists and matrices
- Solve small problems using what you learned in Tutorial 1

---

## Workshop Structure

1. Warm-Up — Reading Code
2. Exercise 1: List Basics
3. Exercise 2: Slicing and Indexing
4. Exercise 3: Modifying Lists
5. Exercise 4: Looping Through Lists
6. Exercise 5: Matrix Basics
7. Exercise 6: Processing Problems
8. Challenge Exercise

---

## Setup

Create a new file called `workshop_lists.py` for all your exercises. Run it after each task to check your output.

---

## 1. Warm-Up — Reading Code

Before writing anything, read the code below and answer the questions. This trains you to understand code before running it.

```python
data = [10, 20, 30, 40, 50]

print(data[1])
print(data[-1])
print(data[1:4])
print(len(data))
```

Questions — write your answers as comments before running:

- What does `data[1]` print?
- What does `data[-1]` print?
- What does `data[1:4]` print?
- What does `len(data)` print?

Now run the code and check if you were right.

---

## 2. Exercise 1: List Basics

#### Task 1.1 — Create and Print a List

Create a list called `numbers` containing the values 1 through 5. Print the list and its length.

```python
## TODO: Create numbers list and print it and its length
```

Expected output:
[1, 2, 3, 4, 5]
5


---

#### Task 1.2 — Access Elements

Given the list below, print the first element, the last element, and the middle element (index 2).

```python
cities = ["Cairo", "Paris", "Tokyo", "London", "Sydney"]

## TODO: Print first, last, and middle element
```

Expected output:
Cairo
Sydney
Tokyo


---

#### Task 1.3 — Mixed Types

Create a list that stores a name (string), an age (integer), and a score (float). Print each element on its own line using a loop.

```python
## TODO: Create mixed list and loop through it
```

---

#### Task 1.4 — Negative Indexing

Given:

```python
letters = ["a", "b", "c", "d", "e"]
```

Without counting from the front, use negative indexing to print the last three elements: `c`, `d`, `e`.

```python
## TODO: Use negative indexing to print last 3 elements
```

---

## 3. Exercise 2: Slicing and Indexing

Recall the slicing syntax:

list[start:end]       ## end is not included
list[start:]          ## from start to end
list[:end]            ## from beginning to end
list[::step]          ## every step-th element
list[::-1]            ## reversed


#### Task 2.1 — Basic Slices

Given:

```python
numbers = [10, 20, 30, 40, 50, 60, 70, 80]
```

Write slices to produce each of the following. Add a comment explaining what each slice does.

```python
## TODO: Print first 3 elements       → [10, 20, 30]
## TODO: Print last 3 elements        → [60, 70, 80]
## TODO: Print middle 4 elements      → [30, 40, 50, 60]
## TODO: Print every second element   → [10, 30, 50, 70]
## TODO: Print reversed list          → [80, 70, 60, 50, 40, 30, 20, 10]
```

---

#### Task 2.2 — Slicing Strings

Strings behave like lists of characters. Given:

```python
word = "programming"
```

Use slicing to:

```python
## TODO: Print first 4 characters     → "prog"
## TODO: Print last 3 characters      → "ing"
## TODO: Print every other character  → "aramm"
## TODO: Print word reversed          → "gnimmargorp"
```

---

#### Task 2.3 — Predict the Output

Before running, write what you think each line prints:

```python
data = [5, 10, 15, 20, 25]

print(data[2:])
print(data[:2])
print(data[1:4])
print(data[::2])
print(data[-3:])
```

Run the code and check your predictions.

---

## 4. Exercise 3: Modifying Lists

#### Task 3.1 — Build a List Step by Step

Start with an empty list. Follow the steps below and print the list after each one.

```python
items = []

## Step 1: append "apple"
## Step 2: append "banana"
## Step 3: insert "mango" at index 1
## Step 4: extend with ["grape", "kiwi"]
## Step 5: change the first element to "pear"

## TODO: Implement each step and print after each one
```

Expected output after each step:
['apple']
['apple', 'banana']
['apple', 'mango', 'banana']
['apple', 'mango', 'banana', 'grape', 'kiwi']
['pear', 'mango', 'banana', 'grape', 'kiwi']


---

#### Task 3.2 — Remove Elements

Given:

```python
numbers = [10, 20, 30, 20, 40, 50]
```

```python
## TODO: Remove the first occurrence of 20
## TODO: Remove the last element using pop()
## TODO: Print the final list
```

Expected output:
[10, 30, 20, 40]


---

#### Task 3.3 — Modify a List in a Loop

Given:

```python
prices = [100, 200, 300, 400]
```

Apply a 10% discount to every price by modifying the list in place using a loop. Print the result.

```python
## TODO: Apply 10% discount to each price
```

Expected output:
[90.0, 180.0, 270.0, 360.0]


Hint: use `range(len(prices))` to loop by index so you can modify each element.

---

## 5. Exercise 4: Looping Through Lists

#### Task 4.1 — Simple Loop

Print every element in the list on its own line:

```python
fruits = ["apple", "banana", "mango", "grape"]

## TODO: Loop and print each fruit
```

---

#### Task 4.2 — Loop with Index Using enumerate()

`enumerate()` gives you both the index and the value at the same time.

```python
for i, value in enumerate(fruits):
    print(i, value)
```

Use `enumerate()` to print each fruit with its position number starting from 1 (not 0):

```python
## TODO: Print each fruit with position starting at 1
```

Expected output:
1 apple
2 banana
3 mango
4 grape


Hint: `enumerate(fruits, start=1)` starts counting from 1.

---

#### Task 4.3 — Counting with a Loop

Count how many words in the list have more than 4 characters:

```python
words = ["cat", "elephant", "dog", "butterfly", "ant", "tiger"]

## TODO: Count words longer than 4 characters
```

Expected output:
3


---

## 6. Exercise 5: Matrix Basics

Recall: a matrix is a list of lists. Access elements with `matrix[row][column]`.

      Column
        0  1  2
Row 0   1  2  3
Row 1   4  5  6
Row 2   7  8  9


#### Task 5.1 — Create and Print a Matrix

Create the 3×3 matrix shown above and print it row by row using a loop.

```python
## TODO: Create matrix and print each row
```

Expected output:
[1, 2, 3]
[4, 5, 6]
[7, 8, 9]


---

#### Task 5.2 — Access Elements

Using the same matrix:

```python
## TODO: Print the element at row 0, column 2   → 3
## TODO: Print the element at row 1, column 1   → 5
## TODO: Print the element at row 2, column 0   → 7
```

---

#### Task 5.3 — Matrix Dimensions

Write code that prints the number of rows and columns without hardcoding the numbers:

```python
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

## TODO: Print number of rows and columns
```

Expected output:
Rows: 3
Columns: 3


Hint: `len(matrix)` gives rows, `len(matrix[0])` gives columns.

---

#### Task 5.4 — Extract a Column

Extract column 1 (the middle column) from the matrix into a new list using a loop:

```python
## TODO: Extract column 1 → [2, 5, 8]
```

---

## 7. Exercise 6: Processing Problems

Now you will write functions. Each function has a type hint and a docstring — read them carefully before writing the body.

#### Task 6.1 — Sum of a List

```python
def sum_list(numbers: list) -> int:
    """Return the sum of all numbers in the list.
    Do not use the built-in sum() function."""
    ## TODO: implement
    pass

## Tests
print(sum_list([1, 2, 3, 4, 5]))   ## 15
print(sum_list([10, 20, 30]))       ## 60
print(sum_list([]))                 ## 0
```

---

#### Task 6.2 — Find the Maximum

```python
def find_max(numbers: list) -> int:
    """Return the largest number in the list.
    Do not use the built-in max() function."""
    ## TODO: implement
    pass

## Tests
print(find_max([3, 1, 4, 1, 5, 9]))   ## 9
print(find_max([10]))                  ## 10
print(find_max([-5, -1, -3]))          ## -1
```

Hint: start with `max_value = numbers[0]` and compare each element.

---

#### Task 6.3 — Count Elements in a Matrix

```python
def count_elements(matrix: list) -> int:
    """Return the total number of elements in a matrix."""
    ## TODO: implement
    pass

## Tests
print(count_elements([[1, 2], [3, 4]]))          ## 4
print(count_elements([[1, 2, 3], [4, 5, 6]]))    ## 6
```

Hint: loop through each row and add `len(row)` to a counter.

---

#### Task 6.4 — Find a Value in a List

```python
def contains(numbers: list, target: int) -> bool:
    """Return True if target is in the list, False otherwise.
    Do not use the 'in' operator."""
    ## TODO: implement
    pass

## Tests
print(contains([1, 2, 3, 4], 3))    ## True
print(contains([1, 2, 3, 4], 9))    ## False
```

---

## 8. Challenge Exercise

This exercise combines everything from the workshop.

#### Task — Row Sums of a Matrix

Write a function that takes a matrix and returns a list where each element is the sum of the corresponding row.

```python
def row_sums(matrix: list) -> list:
    """Return a list of sums, one per row."""
    ## TODO: implement
    pass

## Tests
m = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

print(row_sums(m))   ## [6, 15, 24]
```

Once that works, extend it: also print which row has the largest sum.

```python
## TODO: Print the index of the row with the largest sum
## Expected: Row 2 has the largest sum: 24
```

---

## Key Takeaways

- lists are ordered, mutable, and indexed from 0
- negative indexes count from the end: `-1` is the last element
- slicing uses `[start:end:step]` — the end index is not included
- `append` adds one item, `extend` adds many, `insert` adds at a position
- `remove` deletes by value, `pop` removes the last item
- `enumerate()` gives index and value together in a loop
- matrices are lists of lists — access with `matrix[row][column]`
- `len(matrix)` gives rows, `len(matrix[0])` gives columns