# Workshop 2: Lists and Sets

**Section**: 7 - Lists and Sets (45 min)
**Level**: Beginner
**Prerequisites**: Tutorial 2 (Lists and Sets)

---

## 🎯 Workshop Objectives

By the end of this workshop, you will:

1. **Create and modify lists** using basic operations
2. **Create and use tuples** with basic operations
3. **Create and modify sets** using basic operations
4. **Solve simple problems** using lists, tuples, and sets

---

## 📋 Workshop Structure

1. [Setup](#setup)
2. [Exercise 1: List Operations](#exercise-1-list-operations)
3. [Exercise 2: Tuple Operations](#exercise-2-tuple-operations)
4. [Exercise 3: Set Operations](#exercise-3-set-operations)
5. [Exercise 4: Data Structure Problems](#exercise-4-data-structure-problems)

---

## 🛠️ Setup

Create a new Python file called `workshop_lists_sets.py` for your exercises.

---

## 🏃 Exercise 1: List Operations

### Task 1.1: List Creation and Access
Create a list with numbers 1-5 and print the first and last elements.

```python
# TODO: Create list and access elements
```

### Task 1.2: List Modification
Start with list `[1, 2, 3]`, add 4 to the end, then change the second element to 10.

```python
# TODO: Modify the list
```

### Task 1.3: List Building
Create an empty list and add 3 different fruits to it one by one.

```python
# TODO: Build a list step by step
```

---

## 🏃 Exercise 2: Tuple Operations

### Task 2.1: Tuple Creation
Create a tuple with numbers 1, 2, 3 and print the tuple.

```python
# TODO: Create and print a tuple
```

### Task 2.2: Tuple Access
Create a tuple with 5 elements and print the first and last elements.

```python
# TODO: Access tuple elements
```

### Task 2.3: Tuple Unpacking
Create a tuple with 3 values and unpack them into separate variables.

```python
# TODO: Unpack tuple into variables
```

---

## 🏃 Exercise 3: Set Operations

### Task 3.1: Set Creation
Create a set with colors "red", "blue", "green" and print the set.

```python
# TODO: Create and print a set
```

### Task 3.2: Set Modification
Create a set with 3 colors, add a new color, then add two more colors at once.

```python
# TODO: Modify a set
```

### Task 3.3: Set Checking
Create a set with numbers 1, 2, 3, 4, 5. Check if 3 is in the set and if 10 is in the set.

```python
# TODO: Check set membership
```

---

## 🏃 Exercise 4: Data Structure Problems

### Task 3.1: List Sum Function
Create a function that takes a list of numbers and returns their sum.

```python
def sum_list(numbers: list) -> int:
    # TODO: Calculate sum of all numbers in list
    pass

# Test your function
nums = [1, 2, 3, 4, 5]
result = sum_list(nums)
print(f"Sum: {result}")  # Should print 15
```

### Task 3.2: Unique Elements
Create a function that takes a list and returns a set of unique elements.

```python
def get_unique(items: list) -> set:
    # TODO: Convert list to set to get unique elements
    pass

# Test your function
data = [1, 2, 2, 3, 3, 3, 4]
unique = get_unique(data)
print(f"Unique: {unique}")  # Should print {1, 2, 3, 4}
```

### Task 3.3: List Length Counter
Create a function that counts how many items are in any list.

```python
def count_items(my_list: list) -> int:
    # TODO: Count items in list
    pass

# Test your function
fruits = ["apple", "banana", "orange"]
count = count_items(fruits)
print(f"Count: {count}")  # Should print 3
```

### Task 3.4: Set Intersection
Create two sets and find their common elements.

```python
def find_common(set1: set, set2: set) -> set:
    # TODO: Find intersection of two sets
    pass

# Test your function
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}
common = find_common(a, b)
print(f"Common: {common}")  # Should print {3, 4}
```

---

**Workshop Version**: 2.0 - Simplified
**Last Updated**: February 2026
**Estimated Time**: 45 minutes