# Tutorial 1: Lists and Matrices in Python


## 1. What Are Lists?

A **list** is a container that stores multiple values in one variable.

> List and Array are the same topic in Python

Example:

```python
numbers = [10, 20, 30, 40]
```

You can imagine a list as **a row of boxes**:

```
Index:   0    1    2    3
       +----+----+----+----+
Value  |10  |20  |30  |40  |
       +----+----+----+----+
```

Important properties:

• Lists are **ordered**  
• Lists can store **different data types**  
• Lists are **mutable** (they can change)

Example with mixed types:

```python
data = ["Alice", 25, True]
```

---

#### Mini Exercise

Create a list containing the values:

```
5, 10, 15
```

Print the list.

---

## 2. Creating Lists

#### Empty List

```python
items = []
```

---

#### List of Numbers

```python
numbers = [1, 2, 3, 4, 5]
```

---

#### List of Strings

```python
fruits = ["apple", "banana", "orange"]
```

---

#### List With Mixed Types

```python
items = ["apple", 10, 3.14, True]
```

---

#### Counting Elements

Use `len()`.

```python
numbers = [10, 20, 30, 40]

print(len(numbers))
```

Output

```
4
```

---

#### Mini Exercise

Create a list with 4 cities and print the number of cities using `len()`.

---

## 3. Accessing List Elements

List elements are accessed using **index numbers**.

Important rule:

Python indexing **starts at 0**.

Example:

```python
numbers = [10, 20, 30, 40, 50]

print(numbers[0])
```

Output

```
10
```

---

#### Visual Diagram

```
numbers = [10, 20, 30, 40, 50]

Index:     0    1    2    3    4
         +----+----+----+----+----+
Value    |10  |20  |30  |40  |50  |
         +----+----+----+----+----+
```

Accessing element:

```
numbers[2] → 30
```

---

#### Negative Indexing

You can access elements from the end.

```
Index:   -5   -4   -3   -2   -1
Value:   10   20   30   40   50
```

Example:

```python
print(numbers[-1])
```

Output

```
50
```

---

#### Mini Exercise

Given

```python
numbers = [5, 10, 15, 20]
```

Print:

• the first element  
• the last element  

---

## 4. List Slicing

Slicing extracts **a portion of a list**.

Syntax

```
list[start:end]
```

The `end` index is **not included**.

---

#### Example

```python
numbers = [10, 20, 30, 40, 50]

print(numbers[0:3])
```

Output

```
[10, 20, 30]
```

Diagram

```
Index:    0    1    2    3    4
        +----+----+----+----+----+
Value   |10  |20  |30  |40  |50  |
        +----+----+----+----+----+

numbers[0:3]

        +----+----+----+
        |10  |20  |30  |
        +----+----+----+
```

---

#### Slice From Middle

```python
print(numbers[1:4])
```

Output

```
[20, 30, 40]
```

---

#### Slice From Index to End

```python
print(numbers[2:])
```

Output

```
[30, 40, 50]
```

---

#### Slice Beginning to Index

```python
print(numbers[:3])
```

Output

```
[10, 20, 30]
```

---

#### Step in Slicing

You can skip elements using **step**.

Example:

```python
numbers = [10, 20, 30, 40, 50, 60]

print(numbers[1::2])
```

Output

```
[20, 40, 60]
```

Explanation

```
Index:     0    1    2    3    4    5
Value:    10   20   30   40   50   60

numbers[1::2]

Start at index 1 → 20  
Skip every 2 elements

Result → 20, 40, 60
```

---

#### Reverse a List

```python
print(numbers[::-1])
```

Output

```
[60, 50, 40, 30, 20, 10]
```

---

#### Mini Exercise

Given

```
numbers = [1,2,3,4,5,6,7,8]
```

Print:

• first 4 elements  
• every second element  
• reversed list  

---

## 5. Modifying Lists

Lists can be modified after creation.

#### Changing an Element

```python
numbers = [10, 20, 30]

numbers[0] = 100

print(numbers)
```

Output

```
[100, 20, 30]
```

---

#### Adding Elements

##### append()

Adds an element to the end.

```python
numbers = [1, 2, 3]

numbers.append(4)
```

Result

```
[1,2,3,4]
```

---

##### insert()

Insert at a specific position.

```python
numbers.insert(1, 10)
```

Result

```
[1,10,2,3,4]
```

---

##### extend()

Add multiple items.

```python
numbers.extend([5,6])
```

Result

```
[1,10,2,3,4,5,6]
```

---

#### Mini Exercise

Start with:

```
[1,2,3]
```

Add `4` and `5` to the list.

---

## 6. Removing Elements

#### remove()

Removes by value.

```python
numbers = [10, 20, 30, 20]

numbers.remove(20)
```

Result

```
[10, 30, 20]
```

---

#### pop()

Removes the last item.

```python
numbers.pop()
```

---

#### clear()

Removes all elements.

```python
numbers.clear()
```

---

#### Mini Exercise

Remove the last element from:

```
[5,10,15,20]
```

---

## 7. Looping Through Lists

Lists are often processed using loops.

#### Simple Loop

```python
numbers = [10, 20, 30]

for num in numbers:
    print(num)
```

---

#### Loop Using Index

```python
for i in range(len(numbers)):
    print(i, numbers[i])
```

---

#### Mini Exercise

Print all elements of:

```
[3,6,9,12]
```

---

## 8. Basic List Processing

Lists are useful for data processing.

#### Sum Example

```python
numbers = [1,2,3,4]

total = 0

for num in numbers:
    total += num

print(total)
```

Output

```
10
```

---

#### Maximum Example

```python
numbers = [10, 50, 30, 20]

max_value = numbers[0]

for num in numbers:
    if num > max_value:
        max_value = num

print(max_value)
```

---

#### Mini Exercise

Find the **minimum value** in a list.

---

## 9. Strings as Lists of Characters

A string behaves like a **list of characters**.

Example:

```python
word = "hello"
```

Visual view

```
Index:   0    1    2    3    4
       +----+----+----+----+----+
Value  | h  | e  | l  | l  | o  |
       +----+----+----+----+----+
```

---

#### Access Characters

```python
print(word[0])
```

Output

```
h
```

---

#### Loop Through Characters

```python
for ch in word:
    print(ch)
```

Output

```
h
e
l
l
o
```

---

#### Character Processing Example

Count vowels.

```python
word = "education"

count = 0

for ch in word:
    if ch in "aeiou":
        count += 1

print(count)
```

---

#### Mini Exercise

Print every character in the string:

```
python
```

---

## 10. What Are Matrices?

A **matrix** is a **list of lists**.

Example matrix:

```
1 2 3
4 5 6
7 8 9
```

Python representation:

```python
matrix = [
    [1,2,3],
    [4,5,6],
    [7,8,9]
]
```

Visual diagram:

```
      Column
        0 1 2
Row 0   1 2 3
Row 1   4 5 6
Row 2   7 8 9
```

---

#### Mini Exercise

Create a **2×2 matrix**.

---

## 11. Accessing Matrix Elements

Matrix indexing:

```
matrix[row][column]
```

Example:

```python
matrix[1][2]
```

Diagram

```
matrix =

[1 2 3]
[4 5 6]
[7 8 9]

matrix[1][2] = 6
```

---

#### Access Whole Row

```python
print(matrix[1])
```

Result

```
[4,5,6]
```

---

#### Mini Exercise

Print the element at:

```
row 2
column 1
```

---

## 12. Extracting a Column

Columns require looping.

```python
column = []

for row in matrix:
    column.append(row[0])
```

Result

```
[1,4,7]
```

---

#### Mini Exercise

Extract column **2**.

---

## 13. Enumeration

`enumerate()` gives both index and value.

```python
items = ["apple","banana","orange"]

for i, value in enumerate(items):
    print(i, value)
```

Output

```
0 apple
1 banana
2 orange
```

---

#### Mini Exercise

Print indexes and values for:

```
["A","B","C"]
```

---

## 14. Common Beginner Mistakes

#### Mistake 1 - Forgetting index starts at 0

Wrong:

```python
numbers[1]  ## expecting first element
```

Correct:

```
numbers[0]
```

---

#### Mistake 2 - Going out of range

Wrong:

```python
numbers = [10,20,30]
print(numbers[3])
```

Error

```
IndexError
```

---

#### Mistake 3 - Confusing append and extend

```
append → adds one item
extend → adds multiple items
```

---

#### Mistake 4 - Treating string like a mutable list

This is wrong:

```python
word = "hello"
word[0] = "H"
```

Strings **cannot be modified directly**.

---

## 15. Key Takeaways

• Lists store multiple values  
• Indexing starts at **0**  
• Lists are **mutable**  
• Slicing extracts parts of lists  
• Strings behave like **lists of characters** for iteration  
• Matrices are **lists of lists**  
• `enumerate()` helps access index and value together  

---
