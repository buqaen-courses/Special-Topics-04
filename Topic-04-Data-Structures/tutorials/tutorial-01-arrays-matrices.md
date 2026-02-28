# Tutorial 1: Advanced Arrays & Matrix Operations

**Section**: 6 - Advanced Arrays and Matrices (60 min)
**Level**: Intermediate
**Prerequisites**: Solid Python fundamentals, basic algorithms, understanding of Big O notation

---

## 📋 Learning Objectives

By the end of this tutorial, you will be able to:

1. **Implement efficient multi-dimensional array operations** with performance considerations
2. **Apply matrix algebra algorithms** including multiplication, transposition, and inversion
3. **Solve numerical computing problems** using array-based approaches
4. **Optimize memory usage** for large-scale array operations
5. **Analyze algorithmic complexity** of array and matrix operations

---

## 📚 Table of Contents

1. [Advanced Array Operations](#advanced-array-operations)
2. [Matrix Algebra & Algorithms](#matrix-algebra--algorithms)
3. [Numerical Computing Techniques](#numerical-computing-techniques)
4. [Performance Optimization](#performance-optimization)
5. [Real-World Applications](#real-world-applications)

---

## 🔸 Advanced Array Operations

### Multi-dimensional Arrays and Memory Efficiency

```python
import sys
from typing import List, Any
from array import array

# Type hints for complex arrays
Matrix = List[List[float]]
Vector = List[float]

# Memory-efficient arrays using array module
def create_efficient_array(size: int, default_value: float = 0.0) -> array:
    """Create memory-efficient array with specified size."""
    return array('f', [default_value] * size)

# Multi-dimensional array with type safety
def create_matrix(rows: int, cols: int, default_value: float = 0.0) -> Matrix:
    """Create a matrix with proper initialization."""
    return [[default_value for _ in range(cols)] for _ in range(rows)]

# Memory usage comparison
regular_list = [0.0] * 1000000
efficient_array = array('f', [0.0] * 1000000)

print(f"List memory: {sys.getsizeof(regular_list)} bytes")
print(f"Array memory: {sys.getsizeof(efficient_array)} bytes")
print(f"Memory saved: {sys.getsizeof(regular_list) - sys.getsizeof(efficient_array)} bytes")

# Advanced slicing with stride patterns
data = list(range(20))
print("Original:", data)
print("Every 3rd element:", data[::3])
print("Reverse every 2nd:", data[::-2])
print("Middle section reversed:", data[5:15][::-1])

# In-place operations for memory efficiency
def normalize_array(arr: list) -> None:
    """Normalize array in-place to save memory."""
    if not arr:
        return
    min_val, max_val = min(arr), max(arr)
    if max_val == min_val:
        return
    for i in range(len(arr)):
        arr[i] = (arr[i] - min_val) / (max_val - min_val)
```

---

## 🔸 Matrix Algebra & Algorithms

### Matrix Operations with O(n) Complexity Analysis

```python
from typing import List, Tuple

def matrix_multiply(A: Matrix, B: Matrix) -> Matrix:
    """
    Matrix multiplication with O(n^3) time complexity.
    Returns C where C[i][j] = sum(A[i][k] * B[k][j])
    """
    if len(A[0]) != len(B):
        raise ValueError("Matrix dimensions incompatible for multiplication")

    result = [[0 for _ in range(len(B[0]))] for _ in range(len(A))]

    for i in range(len(A)):          # O(rows_A)
        for j in range(len(B[0])):    # O(cols_B)
            for k in range(len(B)):  # O(cols_A/rows_B)
                result[i][j] += A[i][k] * B[k][j]

    return result

def matrix_transpose(matrix: Matrix) -> Matrix:
    """Transpose matrix in O(n*m) time."""
    if not matrix:
        return []
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]

def matrix_add(A: Matrix, B: Matrix) -> Matrix:
    """Matrix addition with O(n*m) time complexity."""
    if len(A) != len(B) or len(A[0]) != len(B[0]):
        raise ValueError("Matrices must have same dimensions")
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

# Example usage
A = [[1, 2], [3, 4]]
B = [[5, 6], [7, 8]]

print("Matrix A:", A)
print("Matrix B:", B)
print("A * B:", matrix_multiply(A, B))
print("A^T:", matrix_transpose(A))
print("A + B:", matrix_add(A, B))
```

### Advanced Matrix Algorithms

```python
import math

def gaussian_elimination(A: Matrix, b: Vector) -> Vector:
    """
    Solve Ax = b using Gaussian elimination.
    Time complexity: O(n^3) for general matrices.
    """
    n = len(A)
    # Create augmented matrix [A|b]
    augmented = [row[:] + [b[i]] for i, row in enumerate(A)]

    # Forward elimination
    for i in range(n):
        # Find pivot
        max_row = i
        for k in range(i + 1, n):
            if abs(augmented[k][i]) > abs(augmented[max_row][i]):
                max_row = k

        # Swap rows
        augmented[i], augmented[max_row] = augmented[max_row], augmented[i]

        # Eliminate
        for k in range(i + 1, n):
            factor = augmented[k][i] / augmented[i][i]
            for j in range(i, n + 1):
                augmented[k][j] -= factor * augmented[i][j]

    # Back substitution
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = augmented[i][n]
        for j in range(i + 1, n):
            x[i] -= augmented[i][j] * x[j]
        x[i] /= augmented[i][i]

    return x

def matrix_determinant(matrix: Matrix) -> float:
    """Calculate matrix determinant using Gaussian elimination."""
    n = len(matrix)
    if n != len(matrix[0]):
        raise ValueError("Matrix must be square")

    # Make a copy to avoid modifying original
    A = [row[:] for row in matrix]
    det = 1.0
    sign = 1

    for i in range(n):
        # Find pivot
        pivot = i
        for j in range(i + 1, n):
            if abs(A[j][i]) > abs(A[pivot][i]):
                pivot = j

        if A[pivot][i] == 0:
            return 0.0

        # Swap rows
        if pivot != i:
            A[i], A[pivot] = A[pivot], A[i]
            sign = -sign

        # Eliminate
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]

        det *= A[i][i]

    return det * sign

# Example: Solving system of equations
# 2x + y - z = 8
# -3x - y + 2z = -11
# -2x + y + 2z = -3

A = [[2, 1, -1], [-3, -1, 2], [-2, 1, 2]]
b = [8, -11, -3]

solution = gaussian_elimination(A, b)
print(f"Solution: x={solution[0]:.2f}, y={solution[1]:.2f}, z={solution[2]:.2f}")

# Verify determinant
det = matrix_determinant(A)
print(f"Determinant: {det:.2f}")
```

## 🔸 Numerical Computing Techniques

### Vectorized Operations and Performance

```python
import time
import numpy as np  # For comparison with NumPy

def dot_product_loop(a: Vector, b: Vector) -> float:
    """Traditional loop-based dot product - O(n) time."""
    if len(a) != len(b):
        raise ValueError("Vectors must have same length")
    return sum(x * y for x, y in zip(a, b))

def dot_product_vectorized(a: Vector, b: Vector) -> float:
    """Vectorized dot product using list comprehensions."""
    if len(a) != len(b):
        raise ValueError("Vectors must have same length")
    return sum(x * y for x, y in zip(a, b))  # Same as loop but more Pythonic

# Performance comparison
size = 100000
a = list(range(size))
b = list(range(size, 2*size))

# Time loop-based approach
start = time.time()
result_loop = dot_product_loop(a, b)
time_loop = time.time() - start

# Time vectorized approach (same implementation, different style)
start = time.time()
result_vec = dot_product_vectorized(a, b)
time_vec = time.time() - start

print(f"Loop result: {result_loop}, Time: {time_loop:.4f}s")
print(f"Vectorized result: {result_vec}, Time: {time_vec:.4f}s")

# Compare with NumPy (if available)
try:
    a_np = np.array(a)
    b_np = np.array(b)
    start = time.time()
    result_np = np.dot(a_np, b_np)
    time_np = time.time() - start
    print(f"NumPy result: {result_np}, Time: {time_np:.4f}s")
    print(f"Speedup vs loop: {time_loop/time_np:.1f}x")
except ImportError:
    print("NumPy not available for comparison")
```

### Convolution and Signal Processing

```python
def convolve_1d(signal: Vector, kernel: Vector) -> Vector:
    """
    1D convolution for signal processing.
    Time complexity: O(len(signal) * len(kernel))
    """
    result = []
    kernel_size = len(kernel)
    signal_size = len(signal)

    for i in range(signal_size - kernel_size + 1):
        sum_val = 0
        for j in range(kernel_size):
            sum_val += signal[i + j] * kernel[j]
        result.append(sum_val)

    return result

def moving_average(data: Vector, window_size: int) -> Vector:
    """Calculate moving average using convolution."""
    if window_size <= 0 or window_size > len(data):
        raise ValueError("Invalid window size")

    kernel = [1.0 / window_size] * window_size
    return convolve_1d(data, kernel)

# Example: Stock price smoothing
stock_prices = [100, 102, 98, 105, 103, 108, 106, 110, 107, 112]
smoothed = moving_average(stock_prices, 3)
print("Original prices:", stock_prices)
print("3-day moving average:", [f"{x:.1f}" for x in smoothed])

# Edge detection kernel
def apply_kernel(image_row: Vector, kernel: Vector) -> Vector:
    """Apply convolution kernel to image row."""
    return convolve_1d(image_row, kernel)

# Sobel edge detection kernel
sobel_kernel = [-1, 0, 1]
sample_image_row = [50, 52, 48, 55, 53, 58, 56, 60, 57, 62]
edges = apply_kernel(sample_image_row, sobel_kernel)
print("Original image row:", sample_image_row)
print("Edge detection result:", [f"{x:.1f}" for x in edges])
```

## 🔸 Performance Optimization

### Memory Layout and Cache Efficiency

```python
import sys

def analyze_memory_layout():
    """Demonstrate memory layout importance for performance."""
    # Row-major vs Column-major access patterns

    # Create a large matrix
    size = 1000
    matrix = [[i * size + j for j in range(size)] for i in range(size)]

    # Row-major access (cache-friendly)
    def sum_row_major(mat):
        total = 0
        for i in range(size):
            for j in range(size):
                total += mat[i][j]
        return total

    # Column-major access (cache-unfriendly)
    def sum_column_major(mat):
        total = 0
        for j in range(size):
            for i in range(size):
                total += mat[i][j]
        return total

    import time
    start = time.time()
    result1 = sum_row_major(matrix)
    time_row = time.time() - start

    start = time.time()
    result2 = sum_column_major(matrix)
    time_col = time.time() - start

    print(f"Row-major: {time_row:.4f}s, Result: {result1}")
    print(f"Column-major: {time_col:.4f}s, Result: {result2}")
    print(f"Performance ratio: {time_col/time_row:.2f}x")

def optimize_matrix_multiplication(A: Matrix, B: Matrix) -> Matrix:
    """Optimized matrix multiplication with better cache utilization."""
    if len(A[0]) != len(B):
        raise ValueError("Incompatible dimensions")

    # Transpose B for better cache performance
    B_T = matrix_transpose(B)

    result = [[0 for _ in range(len(B[0]))] for _ in range(len(A))]

    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(A[0])):
                result[i][j] += A[i][k] * B_T[j][k]  # Better cache access

    return result
```

## 🔸 Real-World Applications

### Image Processing Pipeline

```python
from typing import List, Tuple

def rgb_to_grayscale(image: List[List[List[int]]]) -> List[List[float]]:
    """Convert RGB image to grayscale using matrix operations."""
    if not image or not image[0] or len(image[0][0]) != 3:
        raise ValueError("Invalid RGB image format")

    height, width = len(image), len(image[0])
    grayscale = [[0.0 for _ in range(width)] for _ in range(height)]

    for i in range(height):
        for j in range(width):
            r, g, b = image[i][j]
            # Luminance formula
            grayscale[i][j] = 0.299 * r + 0.587 * g + 0.114 * b

    return grayscale

def image_convolution(image: List[List[float]], kernel: Matrix) -> List[List[float]]:
    """Apply 2D convolution to image."""
    if not kernel or not kernel[0]:
        raise ValueError("Invalid kernel")

    height, width = len(image), len(image[0])
    k_height, k_width = len(kernel), len(kernel[0])

    result = [[0.0 for _ in range(width - k_width + 1)]
              for _ in range(height - k_height + 1)]

    for i in range(len(result)):
        for j in range(len(result[0])):
            sum_val = 0.0
            for ki in range(k_height):
                for kj in range(k_width):
                    sum_val += image[i + ki][j + kj] * kernel[ki][kj]
            result[i][j] = sum_val

    return result

# Example usage
sample_image = [
    [[255, 0, 0], [0, 255, 0], [0, 0, 255]],
    [[128, 128, 128], [64, 64, 64], [192, 192, 192]],
    [[0, 0, 0], [255, 255, 255], [128, 128, 128]]
]

gray_image = rgb_to_grayscale(sample_image)
print("Grayscale conversion completed")

# Gaussian blur kernel
gaussian_kernel = [
    [1/16, 2/16, 1/16],
    [2/16, 4/16, 2/16],
    [1/16, 2/16, 1/16]
]

blurred = image_convolution(gray_image, gaussian_kernel)
print("Gaussian blur applied")
```

---

## 🎯 Practice Exercises

### Exercise 1: Matrix Operations
Implement matrix multiplication and compare performance with different input sizes. Analyze the time complexity.

### Exercise 2: Gaussian Elimination
Solve a system of linear equations using Gaussian elimination. Verify your solution by back-substitution.

### Exercise 3: Convolution Algorithms
Implement 1D convolution and use it for signal smoothing. Compare different kernel sizes.

### Exercise 4: Memory Optimization
Compare memory usage of different array storage methods (lists vs arrays vs NumPy if available).

---

## 🎯 Key Takeaways

1. **Matrix operations have specific time complexities** (multiplication is O(n^3), addition is O(n^2))
2. **Memory layout affects performance** significantly due to CPU cache behavior
3. **Algorithm choice matters** - vectorized operations can be much faster than loops
4. **Real-world applications** use matrix operations extensively (image processing, machine learning, physics simulations)

---

**Tutorial Version**: 3.0 - Advanced
**Last Updated**: February 2026
**Estimated Reading Time**: 45-60 minutes