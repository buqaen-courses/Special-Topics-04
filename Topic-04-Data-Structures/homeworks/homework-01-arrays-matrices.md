# Homework 1: Advanced Arrays & Matrix Algorithms

**Section**: 6 - Advanced Arrays and Matrices (90 min)
**Level**: Intermediate
**Prerequisites**: Tutorial 1 (Advanced Arrays and Matrices)

---

## 🎯 Assignment Objectives

By completing this homework, you will:

1. **Implement complex matrix algorithms** with proper time/space complexity analysis
2. **Solve numerical computing problems** using efficient array operations
3. **Apply matrix algebra** in practical programming scenarios
4. **Optimize array operations** for memory efficiency and performance
5. **Analyze algorithmic complexity** and make informed implementation choices

---

## 📋 Assignment Structure

Complete 5 challenging algorithmic tasks:

1. [Task 1: Matrix Operations](#task-1-matrix-operations)
2. [Task 2: Gaussian Elimination](#task-2-gaussian-elimination)
3. [Task 3: Image Processing](#task-3-image-processing)
4. [Task 4: Performance Optimization](#task-4-performance-optimization)
5. [Task 5: Algorithm Analysis](#task-5-algorithm-analysis)

---

## 🏃 Task 1: Matrix Operations

**Objective:** Implement fundamental matrix operations with proper error handling and type hints.

Create a Python file `homework_01_arrays.py` with the following functions:

### Function 1: Matrix Multiplication
Implement matrix multiplication with O(n³) time complexity. Include proper dimension validation.

```python
from typing import List
Matrix = List[List[float]]

def matrix_multiply(A: Matrix, B: Matrix) -> Matrix:
    """
    Multiply two matrices A and B.
    Time complexity: O(n*m*p) where A is n×m, B is m×p
    """
    # TODO: Implement matrix multiplication
    # Check if matrices can be multiplied (A.cols == B.rows)
    # Return result matrix
    pass
```

### Function 2: Matrix Transpose
Implement matrix transposition with O(n*m) time complexity.

```python
def matrix_transpose(matrix: Matrix) -> Matrix:
    """
    Transpose a matrix (swap rows and columns).
    Time complexity: O(n*m)
    """
    # TODO: Implement matrix transpose
    # Handle empty matrices
    pass
```

### Function 3: Matrix Determinant (3×3)
Calculate determinant of 3×3 matrices using cofactor expansion.

```python
def matrix_determinant_3x3(matrix: Matrix) -> float:
    """
    Calculate determinant of 3x3 matrix using cofactor expansion.
    Time complexity: O(1) for fixed size
    """
    # TODO: Implement 3x3 determinant calculation
    # Validate matrix dimensions
    pass
```

---

## 🏃 Task 2: Matrix Basics

**Objective:** Create and manipulate basic matrices.

### Function 4: Create 2x2 Matrix
Write a function that creates a 2x2 matrix.

```python
def create_2x2_matrix():
    # TODO: Create matrix [[1, 2], [3, 4]]
    pass
```

### Function 5: Access Matrix Element
Write a function that returns an element at row 1, column 1 from a matrix.

```python
def get_matrix_element(matrix):
    # TODO: Return element at row 1, column 1
    pass
```

### Function 6: Count Matrix Elements
Write a function that counts total elements in any matrix.

```python
def count_matrix_elements(matrix):
    # TODO: Count all elements in matrix
    pass
```

---

## 🏃 Task 3: Simple Problems

**Objective:** Solve simple problems using arrays and matrices.

### Function 7: Array Sum
Write a function that calculates the sum of all numbers in an array.

```python
def sum_array(arr):
    # TODO: Calculate sum of all elements
    pass
```

### Function 8: Find Maximum
Write a function that finds the largest number in an array.

```python
def find_max(arr):
    # TODO: Find maximum value in array
    pass
```

### Function 9: Matrix Size
Write a function that returns the size of a matrix as (rows, columns).

```python
def get_matrix_size(matrix):
    # TODO: Return (rows, columns) tuple
    pass
```

---

## 📝 Submission Instructions

1. Create `homework_01_arrays.py` with all required functions and comprehensive tests
2. Include time complexity analysis comments for each algorithm
3. Add performance benchmarks comparing different approaches
4. Submit your Python file with detailed documentation

---

## ✅ Grading Criteria

- **Task 1: Matrix Operations** (25 points - correctness, efficiency, error handling)
- **Task 2: Gaussian Elimination** (25 points - algorithm implementation, numerical stability)
- **Task 3: Image Processing** (20 points - practical application, optimization)
- **Task 4: Performance Optimization** (15 points - benchmarking, analysis)
- **Task 5: Algorithm Analysis** (10 points - complexity analysis, trade-offs)
- **Code Quality** (5 points - documentation, type hints, readability)

**Total: 100 points**

---

**Homework Version**: 3.0 - Advanced
**Last Updated**: February 2026