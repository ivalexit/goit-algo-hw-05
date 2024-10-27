def binary_search(arr, x):
    low = 0
    high = len(arr) - 1
    iterations = 0
    upper_border = None
 
    while low <= high:
        iterations += 1
        mid = (high + low) // 2

        # Якщо елемент знайдено, повертаємо його та кількість ітерацій
        if arr[mid] == x:
            return (iterations, arr[mid])
 
        # якщо x більше за значення посередині списку, ігноруємо ліву половину
        elif arr[mid] < x:
            low = mid + 1
 
        # якщо x менше за значення посередині списку, ігноруємо праву половину
        else:
            high = mid - 1
            upper_border = arr[mid]
            
    return (iterations, upper_border)
 

arr = [1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8]
x = 7.5
result = binary_search(arr, x)

print(f"Iterations {result[0]}, Upper border: {result[1]}")
