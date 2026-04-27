
# Tutorial 2: Tuples and Sets in Python
```bash
Section: Topic-04-Data-Structures — Section 2 (Tuples and Sets)
Level: Beginner
Estimated Time: ~35–40 minutes
Prerequisites: Basic Python, Lists
```
---

# Learning Objectives

By the end of this tutorial you will be able to:

- Understand the internal structure of tuples and why immutability matters
- Create tuples, access elements, and use packing/unpacking
- Understand how sets store data using hashing
- Perform set operations and recognize their mathematical equivalents
- Choose the right data structure for a given problem

---

# Table of Contents

1. What Are Tuples?
2. Creating Tuples
3. Accessing Tuple Elements
4. Tuple Immutability
5. Looping Through Tuples
6. Tuple Packing and Unpacking
7. What Are Sets?
8. Creating Sets
9. Adding Elements to Sets
10. Removing Elements from Sets
11. Set Operations
12. Checking Membership in Sets
13. Practical Example: Removing Duplicates
14. Common Beginner Mistakes
15. Practice Exercises
16. Key Takeaways
17. List vs Tuple vs Set — Quick Comparison
18. Real-World Examples
19. Visual Venn Diagrams for Set Operations

---

# 1. What Are Tuples?

A tuple is an ordered, immutable sequence of elements stored in contiguous memory.

Unlike lists, tuples are fixed at creation time. Python allocates their memory once and never resizes them.

```python
point = (3, 5)
```
Memory layout:

```bash
Index:    0      1
        +------+------+
Value   |  3   |  5   |
        +------+------+
Address  0x100  0x108     ← fixed, cannot shift
```

Tuples are commonly used for:

- coordinates and geometric data
- fixed configuration values
- returning multiple values from functions
- dictionary keys (lists cannot be used as keys; tuples can)

```python
location = (40.7128, -74.0060)   # (latitude, longitude)
```
> Technical note: because tuples are immutable, Python can optimize their storage. A tuple of integers is faster to create and iterate than an equivalent list.

---

### Mini Exercise

Create a tuple containing `10, 20, 30` and print it.

---

# 2. Creating Tuples

### Basic Tuple

```python
numbers = (1, 2, 3)
```
### Tuple of Strings

```python
colors = ("red", "green", "blue")
```
### Mixed Types

Tuples can hold any combination of types because each element is stored as a reference (pointer) to an object.

```python
data = ("Alice", 25, True)

```
#### data:
```bash

  [0] → str object  "Alice"
  [1] → int object  25
  [2] → bool object True
```
### Single-Element Tuple

The trailing comma is required. Without it, Python treats the parentheses as grouping, not a tuple.

```python
t = (5)    # int, not a tuple
t = (5,)   # tuple with one element
```
Verify with `type()`:

```python
print(type((5)))    # <class 'int'>
print(type((5,)))   # <class 'tuple'>
```
### Counting Elements

```python
numbers = (10, 20, 30)
print(len(numbers))   # 3
```
---

### Mini Exercise

Create a tuple with 4 country names and print its length.

---

# 3. Accessing Tuple Elements

Tuples use zero-based integer indexing, identical to lists.

```python
numbers = (10, 20, 30, 40)
print(numbers[0])   # 10
```
### Index Map

```python
numbers = (10, 20, 30, 40)
```

```bash
Positive index:   0    1    2    3
                +----+----+----+----+
Value           | 10 | 20 | 30 | 40 |
                +----+----+----+----+
Negative index:  -4   -3   -2   -1
```
Negative indices count from the end. `numbers[-1]` is equivalent to `numbers[len(numbers) - 1]`.

```python
print(numbers[-1])   # 40
print(numbers[-2])   # 30
```
### Slicing

Tuples support slicing with the syntax `tuple[start:stop:step]`.

```python
print(numbers[1:3])    # (20, 30)
print(numbers[::2])    # (10, 30)   every second element
```
---

### Mini Exercise

Given `t = (5, 10, 15, 20)`, print the first element and the last element.

---

# 4. Tuple Immutability

Attempting to modify a tuple raises a `TypeError` at runtime.

```python
numbers = (10, 20, 30)
numbers[0] = 100
```
##### TypeError
```bash
# TypeError: 'tuple' object does not support item assignment
```
Why immutability is useful:

- prevents accidental modification of fixed data
- allows tuples to be used as dictionary keys
- Python can cache and reuse small tuples internally (optimization)
- signals intent: this data is not meant to change

```python
days = ("Mon", "Tue", "Wed", "Thu", "Fri")
```
> Note: if a tuple contains a mutable object (like a list), the list itself can still be modified. The tuple's reference to that list is fixed, but the list's contents are not.

```python
t = ([1, 2], 3)
t[0].append(99)   # allowed — modifying the list, not the tuple
print(t)          # ([1, 2, 99], 3)
```
---

### Mini Exercise

Create a tuple `(255, 128, 0)` representing an RGB color. Print each value.

---

# 5. Looping Through Tuples

### Direct Iteration

```python
numbers = (10, 20, 30)

for n in numbers:
    print(n)
```
Output:

```bash
10
20
30
```
### Index-Based Iteration

```python
for i in range(len(numbers)):
    print(i, numbers[i])
```
### Using enumerate()

`enumerate()` is the preferred approach when you need both index and value.

```python
for i, val in enumerate(numbers):
    print(i, val)
```
Output:

```bash
0 10
1 20
2 30
```
---

### Mini Exercise

Loop through `(2, 4, 6, 8)` using `enumerate()` and print each index and value.

---

# 6. Tuple Packing and Unpacking

### Packing

Assigning multiple values into a single tuple.

```python
point = (3, 7)
```
Python also allows packing without parentheses:

```python
point = 3, 7   # same result
```
### Unpacking

Extracting values from a tuple into separate variables. The number of variables must match the number of elements.

```python
x, y = point
print(x)   # 3
print(y)   # 7
```
```bash
Tuple:  (  3  ,  7  )
             ↓     ↓
             x     y
```
### Extended Unpacking with `*`

The `*` operator captures remaining elements into a list.

```python
first, *rest = (1, 2, 3, 4, 5)
print(first)   # 1
print(rest)    # [2, 3, 4, 5]
```
### Swapping Variables

Tuple unpacking makes variable swapping clean and Pythonic.

```python
a, b = 10, 20
a, b = b, a
print(a, b)   # 20 10
```
---

### Mini Exercise

Unpack `person = ("Alice", 25)` into variables `name` and `age`.

---

# 7. What Are Sets?

A set is an unordered collection of unique, hashable elements.

Internally, Python implements sets using a hash table. Each element is hashed to determine its storage slot. This is why:

- sets have no defined order
- duplicate values are silently ignored (same hash, same slot)
- membership testing is $O(1)$ on average, compared to $O(n)$ for lists

```python
numbers = {1, 2, 3}
```
Conceptual structure:


Hash Table (simplified):
```bash
Slot 0: empty
Slot 1: 1
Slot 2: 2
Slot 3: 3
Slot 4: empty
...
```
No indexes. No duplicates. No guaranteed order.

### Duplicate Removal

```python
numbers = {1, 2, 2, 3, 3, 3}
print(numbers)   # {1, 2, 3}
```
---

### Mini Exercise

Create a set containing `5, 10, 15` and print it.

---

# 8. Creating Sets

### Basic Set

```python
numbers = {1, 2, 3}
```
### Set of Strings

```python
fruits = {"apple", "banana", "orange"}
```
### Empty Set

`{}` creates an empty dictionary, not a set. Always use `set()` for an empty set.

```python
wrong = {}       # dict
correct = set()  # set
```
print(type(wrong))    # <class 'dict'>
print(type(correct))  # <class 'set'>

### Creating a Set from a List

```python
numbers = set([1, 2, 2, 3])
print(numbers)   # {1, 2, 3}
```
---

### Mini Exercise

Create an empty set and add one number to it.

---

# 9. Adding Elements to Sets

### add()

Adds a single hashable element. If the element already exists, the set is unchanged.

```python
numbers = {1, 2, 3}
numbers.add(4)
print(numbers)   # {1, 2, 3, 4}

numbers.add(2)   # already exists, no change
print(numbers)   # {1, 2, 3, 4}
```
### update()

Adds multiple elements from any iterable.

```python
numbers.update([5, 6])
numbers.update((7, 8))     # works with tuples too
numbers.update("ab")       # adds 'a' and 'b' as characters
```
---

### Mini Exercise

Add `10` to the set `{1, 2, 3}`.

---

# 10. Removing Elements from Sets

| Method | Behavior |
|---|---|
| `remove(x)` | removes `x`; raises `KeyError` if not found |
| `discard(x)` | removes `x`; does nothing if not found |
| `pop()` | removes and returns an arbitrary element |
| `clear()` | removes all elements |


```python
numbers = {1, 2, 3, 4}

numbers.remove(2)    # {1, 3, 4}
numbers.discard(5)   # no error, set unchanged
numbers.pop()        # removes arbitrary element
```
Use `discard()` when you are not sure if the element exists. Use `remove()` when its absence should be treated as an error.

---

### Mini Exercise

Remove `3` from `{1, 2, 3, 4}` safely using `discard()`.

---

# 11. Set Operations

Sets support the four standard mathematical set operations.

```python
A = {1, 2, 3}
B = {3, 4, 5}
```
### Union — $A \cup B$

All elements from both sets, with no duplicates.

```python
print(A | B)          # {1, 2, 3, 4, 5}
print(A.union(B))     # same result
```
### Intersection — $A \cap B$

Only elements present in both sets.

```python
print(A & B)               # {3}
print(A.intersection(B))   # same result
```
### Difference — $A \setminus B$

Elements in A that are not in B.

```python
print(A - B)              # {1, 2}
print(A.difference(B))    # same result
```
### Symmetric Difference — $A \triangle B$

Elements in either set, but not in both.

```python
print(A ^ B)                         # {1, 2, 4, 5}
print(A.symmetric_difference(B))     # same result
```
---

### Mini Exercise

Given `A = {1, 2, 3}` and `B = {3, 4}`, find the union and intersection.

---

# 12. Checking Membership

The `in` operator checks whether an element exists in a set.

```python
numbers = {1, 2, 3, 4}
print(3 in numbers)    # True
print(5 in numbers)    # False
```
### Why Sets Are Faster Than Lists for Membership

| Structure | Membership check | Time complexity |
|---|---|---|
| List | scans each element | $O(n)$ |
| Set | computes hash, checks slot | $O(1)$ average |

For large collections, this difference is significant.

```python
# list: may scan all 1,000,000 elements
big_list = list(range(1_000_000))
999_999 in big_list   # slow

# set: one hash lookup
big_set = set(range(1_000_000))
999_999 in big_set    # fast
```
---

### Mini Exercise

Check if `5` is in `{1, 2, 3, 4}`.

---

# 13. Practical Example: Removing Duplicates

```python
numbers = [1, 2, 2, 3, 3, 4]
unique_numbers = set(numbers)
print(unique_numbers)   # {1, 2, 3, 4}
```
If you need the result back as a list:

```python
unique_list = list(set(numbers))
```
> Note: converting to a set does not preserve the original order. If order matters, use `dict.fromkeys()` instead:

```python
ordered_unique = list(dict.fromkeys(numbers))
print(ordered_unique)   # [1, 2, 3, 4]  — order preserved
```
---

### Mini Exercise

Remove duplicates from `[5, 5, 6, 6, 7]`.

---

# 14. Common Beginner Mistakes

### Mistake 1 — Expecting order in sets

Sets are unordered. The printed order may vary between runs and Python versions.

```python
s = {3, 1, 2}
print(s)   # could be {1, 2, 3} or any order
```
### Mistake 2 — Using `{}` for an empty set

```python
s = {}       # creates a dict, not a set
s = set()    # correct
```
### Mistake 3 — Trying to modify a tuple

```python
t = (1, 2, 3)
t[0] = 5   # TypeError
```
### Mistake 4 — Expecting duplicates in sets

```python
s = {1, 1, 1, 2}
print(s)   # {1, 2}
```
### Mistake 5 — Forgetting the comma in a single-element tuple

```python
t = (5)    # int
t = (5,)   # tuple
```
### Mistake 6 — Adding unhashable types to a set

Sets require elements to be hashable. Lists are not hashable.

```python
s = {[1, 2]}   # TypeError: unhashable type: 'list'
s = {(1, 2)}   # OK — tuples are hashable
```
---

# 15. Practice Exercises

### Exercise 1

Create a tuple `(10, 20, 30)` and print each element using `enumerate()`.

### Exercise 2

Unpack `point = (4, 9)` into variables `x` and `y`.

### Exercise 3

Given `A = {1, 2, 3}` and `B = {3, 4, 5}`, find the intersection.

### Exercise 4

Remove duplicates from `[1, 1, 2, 2, 3, 3]` using a set.

### Exercise 5

Check if `"banana"` is in `{"apple", "mango", "grape"}` and print the result.

---

# 16. Key Takeaways

- Tuples are immutable sequences stored in fixed memory
- Tuples support indexing, slicing, and unpacking
- Tuples can be used as dictionary keys; lists cannot
- Sets store unique, hashable elements in a hash table
- Sets are unordered — do not rely on element order
- Set membership testing is $O(1)$ on average
- Sets support union $\cup$, intersection $\cap$, difference $\setminus$, and symmetric difference $\triangle$
- Use `set()` for an empty set, never `{}`

---

# 17. List vs Tuple vs Set — Quick Comparison

| Feature | List | Tuple | Set |
|---|---|---|---|
| Syntax | `[1, 2, 3]` | `(1, 2, 3)` | `{1, 2, 3}` |
| Ordered | Yes | Yes | No |
| Mutable | Yes | No | Yes |
| Duplicates | Yes | Yes | No |
| Indexed access | Yes | Yes | No |
| Hashable (as key) | No | Yes | No |
| Membership $O(n)$ / $O(1)$ | $O(n)$ | $O(n)$ | $O(1)$ avg |
| Use case | General data | Fixed data | Unique items / fast lookup |

Decision guide:

- need to change items later → list
- data should never change, or need a dict key → tuple
- need unique items or fast membership testing → set

---

# 18. Real-World Examples

### Tuples — GPS Coordinates

Latitude and longitude are a natural tuple: they represent a fixed pair.

```python
new_york = (40.7128, -74.0060)
london   = (51.5074, -0.1278)

print(new_york[0])   # latitude
print(new_york[1])   # longitude
```
Tuples can also be used as dictionary keys, which lists cannot:

```python
locations = {
    (40.7128, -74.0060): "New York",
    (51.5074, -0.1278):  "London",
}
```
### Tuples — Returning Multiple Values from a Function

```python
def get_dimensions():
    return (1920, 1080)

width, height = get_dimensions()
print(width, height)   # 1920 1080
```
### Sets — Unique Tags on a Blog Post

```python
post_tags = {"python", "tutorial", "beginner", "python"}
print(post_tags)   # {'python', 'tutorial', 'beginner'}
```
### Sets — Tracking Unique Visitors

```python
visitors = set()

visitors.add("user_001")
visitors.add("user_002")
visitors.add("user_001")   # duplicate, ignored

print(len(visitors))   # 2
```
---

### Mini Exercise

```python
cities = ["Cairo", "Dubai", "Cairo", "London", "Dubai"]
```
Convert to a set and print the unique cities.

---

# 19. Set Operations

```python
A = {1, 2, 3}
B = {3, 4, 5}
```
### Union — $A \cup B$

Everything in A or B (or both).

Result: {1, 2, 3, 4, 5}
```
```python
print(A | B)   # {1, 2, 3, 4, 5}
```
---

### Intersection — $A \cap B$

Only elements in both A and B.

Result: {3}

```python
print(A & B)   # {3}
```
---

### Difference — $A \setminus B$

Elements in A that are not in B.


Result: {1, 2}

```python
print(A - B)   # {1, 2}
```
---

### Symmetric Difference — $A \triangle B$

Elements in either set, but not in both.


Result: {1, 2, 4, 5}

```python
print(A ^ B)   # {1, 2, 4, 5}
```
---

### All Four Operations at a Glance


A = {1, 2, 3}    B = {3, 4, 5}
```bash
Operation              Symbol     Method                  Result
────────────────────────────────────────────────────────────────
Union                  A | B      A.union(B)          → {1,2,3,4,5}
Intersection           A & B      A.intersection(B)   → {3}
Difference (A−B)       A - B      A.difference(B)     → {1,2}
Symmetric Difference   A ^ B      A.symmetric_difference(B) → {1,2,4,5}
```
---

### Mini Exercise

```python
students_math    = {"Ali", "Sara", "John"}
students_science = {"Sara", "John", "Mia"}
```
Find:

- students in both classes (intersection)
- all students across both classes (union)
- students only in math (difference)
`

