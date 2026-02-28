# Tutorial 2: Advanced Lists & Sets with Algorithms

**Section**: 7 - Advanced Lists and Sets (60 min)
**Level**: Intermediate
**Prerequisites**: Tutorial 1 (Advanced Arrays and Matrices), basic algorithms

---

## 📋 Learning Objectives

By the end of this tutorial, you will be able to:

1. **Implement efficient list and set algorithms** with proper time complexity analysis
2. **Apply advanced data structure operations** for real-world problem solving
3. **Optimize memory usage and performance** in list/set operations
4. **Use collections.deque and other specialized containers** for specific use cases
5. **Analyze algorithmic trade-offs** between different data structure choices

---

## 📚 Table of Contents

1. [Advanced List Operations & Algorithms](#advanced-list-operations--algorithms)
2. [Set Theory & Efficient Operations](#set-theory--efficient-operations)
3. [Collections Module & Specialized Containers](#collections-module--specialized-containers)
4. [Algorithmic Problem Solving](#algorithmic-problem-solving)
5. [Performance Optimization Techniques](#performance-optimization-techniques)

---

## 🔸 Advanced List Operations & Algorithms

### Efficient List Algorithms with Complexity Analysis

```python
from typing import List, TypeVar, Callable
import time

T = TypeVar('T')

def binary_search(arr: List[T], target: T) -> int:
    """
    Binary search algorithm - O(log n) time complexity.
    Requires sorted array.
    """
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1  # Not found

def quicksort(arr: List[T]) -> List[T]:
    """
    Quicksort algorithm - O(n log n) average case.
    In-place sorting with recursion.
    """
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    return quicksort(left) + middle + quicksort(right)

def merge_sorted_lists(a: List[T], b: List[T]) -> List[T]:
    """
    Merge two sorted lists - O(n + m) time complexity.
    Used in merge sort algorithm.
    """
    result = []
    i = j = 0

    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            result.append(a[i])
            i += 1
        else:
            result.append(b[j])
            j += 1

    result.extend(a[i:])
    result.extend(b[j:])
    return result

# Example usage and performance comparison
import random

# Generate test data
data = list(range(10000))
random.shuffle(data)
target = 5000

# Linear search (built-in)
start = time.time()
linear_result = data.index(target) if target in data else -1
linear_time = time.time() - start

# Binary search (requires sorted data)
sorted_data = sorted(data)
start = time.time()
binary_result = binary_search(sorted_data, target)
binary_time = time.time() - start

print(f"Linear search: index {linear_result}, time: {linear_time:.6f}s")
print(f"Binary search: index {binary_result}, time: {binary_time:.6f}s")
print(f"Speedup: {linear_time/binary_time:.1f}x")

# Test sorting algorithms
unsorted = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
print("Original:", unsorted)
print("Quicksort:", quicksort(unsorted))

# Test merging
list1 = [1, 3, 5, 7]
list2 = [2, 4, 6, 8]
print("Merge result:", merge_sorted_lists(list1, list2))
```

## 🔸 Set Theory & Efficient Operations

### Set Operations and Mathematical Properties

```python
from typing import Set, List

def set_operations_demo():
    """Demonstrate set theory operations with O(1) average complexity."""
    A = {1, 2, 3, 4, 5}
    B = {4, 5, 6, 7, 8}

    print("Set A:", A)
    print("Set B:", B)
    print("Union (A ∪ B):", A | B)
    print("Intersection (A ∩ B):", A & B)
    print("Difference (A - B):", A - B)
    print("Symmetric difference (A △ B):", A ^ B)
    print("A is subset of B:", A <= B)
    print("A is superset of B:", A >= B)

def power_set(s: Set[T]) -> List[Set[T]]:
    """
    Generate power set - O(2^n) time and space complexity.
    Returns all possible subsets of the set.
    """
    if not s:
        return [set()]

    # Convert to list for indexing
    elements = list(s)
    n = len(elements)
    power_set_size = 1 << n  # 2^n

    result = []
    for i in range(power_set_size):
        subset = set()
        for j in range(n):
            if i & (1 << j):
                subset.add(elements[j])
        result.append(subset)

    return result

def cartesian_product(A: Set[T], B: Set[U]) -> Set[tuple]:
    """Cartesian product A × B - O(|A| * |B|) time complexity."""
    return {(a, b) for a in A for b in B}

# Advanced set operations
def jaccard_similarity(A: Set[T], B: Set[T]) -> float:
    """Jaccard similarity coefficient - measure of set similarity."""
    intersection = len(A & B)
    union = len(A | B)
    return intersection / union if union > 0 else 0.0

def set_partition(items: List[T], predicate: Callable[[T], bool]) -> tuple:
    """Partition list into two sets based on predicate."""
    true_set = set()
    false_set = set()

    for item in items:
        if predicate(item):
            true_set.add(item)
        else:
            false_set.add(item)

    return true_set, false_set

# Example usage
set_A = {1, 2, 3}
set_B = {3, 4, 5}

print("Jaccard similarity:", jaccard_similarity(set_A, set_B))

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
even_set, odd_set = set_partition(numbers, lambda x: x % 2 == 0)
print("Even numbers:", even_set)
print("Odd numbers:", odd_set)

# Power set example (small set to avoid exponential explosion)
small_set = {1, 2, 3}
power = power_set(small_set)
print(f"Power set of {small_set}: {power}")
print(f"Power set size: {len(power)} (should be 2^{len(small_set)})")

# Cartesian product
X = {'a', 'b'}
Y = {1, 2}
cartesian = cartesian_product(X, Y)
print(f"Cartesian product {X} × {Y}: {cartesian}")
```

## 🔸 Collections Module & Specialized Containers

### Advanced Data Structures for Specific Use Cases

```python
from collections import deque, Counter, defaultdict, OrderedDict
import heapq
from typing import Dict, List, Any

def deque_operations():
    """Deque: Double-ended queue for efficient O(1) append/pop operations."""
    # Perfect for queues, stacks, and sliding windows
    dq = deque()

    # Add elements
    dq.append(1)      # Add to right: deque([1])
    dq.appendleft(2)  # Add to left: deque([2, 1])
    dq.extend([3, 4]) # Add multiple to right: deque([2, 1, 3, 4])
    dq.extendleft([5, 6])  # Add multiple to left: deque([6, 5, 2, 1, 3, 4])

    print("Deque:", dq)

    # Remove elements
    right = dq.pop()      # Remove from right: 4
    left = dq.popleft()   # Remove from left: 6

    print("After pop operations:", dq)
    print(f"Removed right: {right}, left: {left}")

    # Rotation operations
    dq.rotate(2)   # Rotate right by 2: deque([1, 3, 5, 2])
    print("After rotate(2):", dq)

    dq.rotate(-1)  # Rotate left by 1: deque([3, 5, 2, 1])
    print("After rotate(-1):", dq)

def counter_advanced():
    """Counter: Efficient counting with mathematical operations."""
    # Document term frequency analysis
    text1 = "the quick brown fox jumps over the lazy dog"
    text2 = "the lazy dog sleeps under the warm sun"

    counter1 = Counter(text1.split())
    counter2 = Counter(text2.split())

    print("Text 1 frequencies:", dict(counter1))
    print("Text 2 frequencies:", dict(counter2))

    # Mathematical operations on counters
    print("Union (all words):", dict(counter1 | counter2))
    print("Intersection (common words):", dict(counter1 & counter2))
    print("Difference (unique to text1):", dict(counter1 - counter2))

    # Most common elements
    print("Most common in text1:", counter1.most_common(3))

    # Total word count
    print("Total words in text1:", sum(counter1.values()))

def defaultdict_power():
    """Defaultdict: Automatic key initialization."""
    # Grouping operations
    words = ["apple", "banana", "cherry", "date", "elderberry"]

    # Group by first letter
    groups = defaultdict(list)
    for word in words:
        groups[word[0]].append(word)

    print("Grouped by first letter:", dict(groups))

    # Count occurrences with automatic initialization
    word_counts = defaultdict(int)
    text = "the cat sat on the mat with the rat"
    for word in text.split():
        word_counts[word] += 1

    print("Word counts:", dict(word_counts))

    # Nested defaultdict for complex data structures
    tree = defaultdict(lambda: defaultdict(int))
    data = [("A", "X", 1), ("A", "Y", 2), ("B", "X", 3)]

    for category, subcategory, value in data:
        tree[category][subcategory] += value

    print("Nested structure:", dict(tree))

def heap_operations():
    """Heap operations for priority queues - O(log n) insertions/deletions."""
    # Min-heap by default
    heap = []
    data = [3, 1, 4, 1, 5, 9, 2, 6]

    # Build heap
    for item in data:
        heapq.heappush(heap, item)

    print("Heap:", heap)  # Note: heap property maintained, but not sorted

    # Extract minimum elements
    print("Smallest elements:", [heapq.heappop(heap) for _ in range(3)])

    # Heapify existing list
    data_copy = data.copy()
    heapq.heapify(data_copy)
    print("Heapified list:", data_copy)

    # nlargest/nsmallest for top-k problems
    numbers = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    print("Top 3 largest:", heapq.nlargest(3, numbers))
    print("Top 3 smallest:", heapq.nsmallest(3, numbers))

# Demonstrate all collections
deque_operations()
print("\n" + "="*50 + "\n")
counter_advanced()
print("\n" + "="*50 + "\n")
defaultdict_power()
print("\n" + "="*50 + "\n")
heap_operations()
```

## 🔸 Algorithmic Problem Solving

### Real-World Applications with Lists and Sets

```python
def find_duplicates_efficient(nums: List[int]) -> List[int]:
    """Find all duplicates in array using set - O(n) time, O(n) space."""
    seen = set()
    duplicates = set()

    for num in nums:
        if num in seen:
            duplicates.add(num)
        else:
            seen.add(num)

    return list(duplicates)

def two_sum_problem(nums: List[int], target: int) -> List[tuple]:
    """Find all pairs that sum to target - O(n) time with hash set."""
    seen = set()
    pairs = []

    for num in nums:
        complement = target - num
        if complement in seen:
            pairs.append((complement, num))
        seen.add(num)

    return pairs

def sliding_window_maximum(nums: List[int], k: int) -> List[int]:
    """Sliding window maximum using deque - O(n) time."""
    if not nums or k <= 0:
        return []

    result = []
    dq = deque()  # Store indices

    for i in range(len(nums)):
        # Remove elements outside current window
        while dq and dq[0] <= i - k:
            dq.popleft()

        # Remove smaller elements from back
        while dq and nums[dq[-1]] <= nums[i]:
            dq.pop()

        dq.append(i)

        # Add maximum for current window
        if i >= k - 1:
            result.append(nums[dq[0]])

    return result

def longest_consecutive_sequence(nums: List[int]) -> int:
    """Find longest consecutive sequence - O(n) time using sets."""
    num_set = set(nums)
    max_length = 0

    for num in num_set:
        # Only start from beginning of sequence
        if num - 1 not in num_set:
            current_num = num
            current_length = 1

            # Count consecutive numbers
            while current_num + 1 in num_set:
                current_num += 1
                current_length += 1

            max_length = max(max_length, current_length)

    return max_length

# Example usage
print("Finding duplicates:")
data = [1, 2, 3, 2, 4, 3, 5, 1]
print(f"Duplicates in {data}: {find_duplicates_efficient(data)}")

print("\nTwo sum problem:")
nums = [2, 7, 11, 15, 3, 6, 9, 4]
target = 9
print(f"Pairs summing to {target} in {nums}: {two_sum_problem(nums, target)}")

print("\nSliding window maximum:")
window_data = [1, 3, -1, -3, 5, 3, 6, 7]
k = 3
print(f"Max in each window of size {k}: {sliding_window_maximum(window_data, k)}")

print("\nLongest consecutive sequence:")
sequence_data = [100, 4, 200, 1, 3, 2, 5, 6]
print(f"Longest consecutive in {sequence_data}: {longest_consecutive_sequence(sequence_data)}")
```

## 🔸 Performance Optimization Techniques

### Memory and Time Complexity Trade-offs

```python
import sys
import time
from collections import Counter

def list_vs_set_lookup_comparison():
    """Compare lookup performance between list and set."""
    # Create test data
    size = 10000
    data = list(range(size))
    data_set = set(data)

    # Test lookups
    lookups = [size//2, size-1, 0, size//4] * 100  # 400 lookups

    # List lookup - O(n)
    start = time.time()
    list_results = [item in data for item in lookups]
    list_time = time.time() - start

    # Set lookup - O(1) average
    start = time.time()
    set_results = [item in data_set for item in lookups]
    set_time = time.time() - start

    print(f"List lookup time: {list_time:.6f}s")
    print(f"Set lookup time: {set_time:.6f}s")
    print(f"Set is {list_time/set_time:.1f}x faster")
    print(f"Memory: List={sys.getsizeof(data)}, Set={sys.getsizeof(data_set)}")

def optimize_with_counter():
    """Counter for frequency analysis - more efficient than manual counting."""
    text = "the quick brown fox jumps over the lazy dog the fox is quick"

    # Manual counting - O(n^2) in worst case
    start = time.time()
    manual_count = {}
    for word in text.split():
        if word in manual_count:
            manual_count[word] += 1
        else:
            manual_count[word] = 1
    manual_time = time.time() - start

    # Counter - O(n)
    start = time.time()
    counter_count = Counter(text.split())
    counter_time = time.time() - start

    print("Manual counting:", dict(manual_count))
    print("Counter result:", dict(counter_count))
    print(f"Manual time: {manual_time:.6f}s")
    print(f"Counter time: {counter_time:.6f}s")
    print(f"Counter is {manual_time/counter_time:.1f}x faster")

def list_comprehension_vs_loop():
    """Compare list comprehension vs traditional loop performance."""
    size = 100000
    data = list(range(size))

    # Traditional loop
    start = time.time()
    squared_loop = []
    for x in data:
        squared_loop.append(x * x)
    loop_time = time.time() - start

    # List comprehension
    start = time.time()
    squared_comp = [x * x for x in data]
    comp_time = time.time() - start

    print(f"Loop time: {loop_time:.6f}s")
    print(f"Comprehension time: {comp_time:.6f}s")
    print(f"Comprehension is {loop_time/comp_time:.2f}x faster")
    print(f"Results equal: {squared_loop == squared_comp}")

# Run performance comparisons
list_vs_set_lookup_comparison()
print("\n" + "="*50)
optimize_with_counter()
print("\n" + "="*50)
list_comprehension_vs_loop()
```

---

## 🎯 Practice Exercises

### Exercise 1: Algorithm Implementation
Implement binary search on a sorted list and compare its performance with linear search for different data sizes.

### Exercise 2: Set Operations
Given two large datasets, find their intersection, union, and symmetric difference. Analyze the time complexity.

### Exercise 3: Deque Applications
Implement a sliding window maximum algorithm using deque and compare with a naive O(n*k) approach.

### Exercise 4: Counter Optimization
Use Counter to analyze word frequencies in a large text file. Compare performance with manual dictionary counting.

### Exercise 5: Real-World Problem
Implement a duplicate detection algorithm for a list of user records using sets for efficient comparison.

---

## 🎯 Key Takeaways

1. **Algorithm choice affects performance dramatically** - O(log n) vs O(n) vs O(n²)
2. **Data structure selection is crucial** - sets for O(1) lookups, lists for ordered access
3. **Collections module provides specialized containers** - deque for queues, Counter for counting, defaultdict for automatic initialization
4. **Memory vs time trade-offs** exist - sometimes O(n) space enables O(1) time operations
5. **Real-world problems require algorithmic thinking** - two-sum, sliding windows, duplicate detection

---

**Tutorial Version**: 3.0 - Advanced
**Last Updated**: February 2026
**Estimated Reading Time**: 45-60 minutes