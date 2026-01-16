import random
import time

def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)

def mergesort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]
    return merge(mergesort(left), mergesort(right))

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def bubblesort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

# Generate a dataset of 10,000 random integers
data = [random.randint(1, 100000) for _ in range(10000)]

# Quicksort
start_time = time.time()
quicksort(data.copy())  # Use copy to avoid modifying original data
quicksort_time = time.time() - start_time

# Mergesort
start_time = time.time()
mergesort(data.copy())
mergesort_time = time.time() - start_time

# Bubblesort
start_time = time.time()
bubblesort(data.copy())
bubblesort_time = time.time() - start_time

print(f"Quicksort time: {quicksort_time:.4f} seconds")
print(f"Mergesort time: {mergesort_time:.4f} seconds")
print(f"Bubblesort time: {bubblesort_time:.4f} seconds")

# Determine the fastest algorithm
fastest_time = min(quicksort_time, mergesort_time, bubblesort_time)

if fastest_time == quicksort_time:
    print("Quicksort is the fastest.")
elif fastest_time == mergesort_time:
    print("Mergesort is the fastest.")
else:
    print("Bubblesort is the fastest.")