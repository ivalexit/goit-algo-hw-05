import timeit

# Boyer Moore algorithm
def build_shift_table(pattern):
   
    table = {}
    length = len(pattern)
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    table.setdefault(pattern[-1], length)
    return table

def boyer_moore_search(text, pattern):
    shift_table = build_shift_table(pattern)
    i = 0
    while i <= len(text) - len(pattern):
        j = len(pattern) - 1
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1
        if j < 0:
            return i
        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))
    return -1


# Knuth Morris Pratt
def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

def kmp_search(main_string, pattern):
    M = len(pattern)
    N = len(main_string)
    lps = compute_lps(pattern)
    i = j = 0
    while i < N:
        if pattern[j] == main_string[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1
        if j == M:
            return i - j
    return -1


# Rabin Karp algorithm
def polynomial_hash(s, base=256, modulus=101):
    n = len(s)
    hash_value = 0
    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1, modulus)
        hash_value = (hash_value + ord(char) * power_of_base) % modulus
    return hash_value

def rabin_karp_search(main_string, substring):
    substring_length = len(substring)
    main_string_length = len(main_string)
    base = 256
    modulus = 101
    substring_hash = polynomial_hash(substring, base, modulus)
    current_slice_hash = polynomial_hash(main_string[:substring_length], base, modulus)
    h_multiplier = pow(base, substring_length - 1, modulus)
    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash:
            if main_string[i:i + substring_length] == substring:
                return i
        if i < main_string_length - substring_length:
            current_slice_hash = (current_slice_hash - ord(main_string[i]) * h_multiplier) % modulus
            current_slice_hash = (current_slice_hash * base + ord(main_string[i + substring_length])) % modulus
            if current_slice_hash < 0:
                current_slice_hash += modulus
    return -1



# Time measure function
def measure_time(search_func, text, pattern):
    timer = timeit.Timer(lambda: search_func(text, pattern))
    return timer.timeit(number=10)

# Reading files
with open("/Users/ivalextar/Desktop/GoIT-PROJECTS/goit_algo/goit-algo-hw-05/hw5_3_docs/стаття 1.txt", "r", encoding="utf-8") as f:
    article1 = f.read()
with open("/Users/ivalextar/Desktop/GoIT-PROJECTS/goit_algo/goit-algo-hw-05/hw5_3_docs/стаття 2 (1).txt", "r", encoding="utf-8") as f:
    article2 = f.read()

# Test substrings

existing_substr = "елемент"
non_existing_substr = "єнотик"

print("Article 1:")
print(f"Boyer Moore (existing): {measure_time(boyer_moore_search, article1, existing_substr):.5f} sec")
print(f"Boyer Moore (non existing): {measure_time(boyer_moore_search, article1, non_existing_substr):.5f} sec")

print(f"Knuth Morris Pratt (existing): {measure_time(kmp_search, article1, existing_substr):.5f} sec")
print(f"Knuth Morris Pratt (non existing): {measure_time(kmp_search, article1, non_existing_substr):.5f} sec")

print(f"Rabin Karp (existing): {measure_time(rabin_karp_search, article1, existing_substr):.5f} sec")
print(f"Rabin Karp Pratt (non existing): {measure_time(rabin_karp_search, article1, non_existing_substr):.5f} sec")

print("Article 2:")
print(f"Boyer Moore (existing): {measure_time(boyer_moore_search, article2, existing_substr):.5f} sec")
print(f"Boyer Moore (non existing): {measure_time(boyer_moore_search, article2, non_existing_substr):.5f} sec")

print(f"Knuth Morris Pratt (existing): {measure_time(kmp_search, article2, existing_substr):.5f} sec")
print(f"Knuth Morris Pratt (non existing): {measure_time(kmp_search, article2, non_existing_substr):.5f} sec")

print(f"Rabin Karp (existing): {measure_time(rabin_karp_search, article2, existing_substr):.5f} sec")
print(f"Rabin Karp Pratt (non existing): {measure_time(rabin_karp_search, article2, non_existing_substr):.5f} sec")

# Store execution time results for each algorithm
time_boyer_moore_real = measure_time(boyer_moore_search, article1, existing_substr)
time_boyer_moore_fake = measure_time(boyer_moore_search, article1, non_existing_substr)
time_kmp_real = measure_time(kmp_search, article1, existing_substr)
time_kmp_fake = measure_time(kmp_search, article1, non_existing_substr)
time_rabin_karp_real = measure_time(rabin_karp_search, article1, existing_substr)
time_rabin_karp_fake = measure_time(rabin_karp_search, article1, non_existing_substr)

# Generate summary in markdown format
summary = f"""
# Comparison of Substring Search Algorithm Efficiency

| Algorithm           | Existing Substring (sec) | Non-Existing Substring (sec) |
|---------------------|--------------------------|------------------------------|
| Boyer-Moore         | {time_boyer_moore_real:.5f}         | {time_boyer_moore_fake:.5f}         |
| Knuth-Morris-Pratt  | {time_kmp_real:.5f}               | {time_kmp_fake:.5f}              |
| Rabin-Karp          | {time_rabin_karp_real:.5f}         | {time_rabin_karp_fake:.5f}        |

## Summary:
- Fastest algorithm for the existing substring: {min(time_boyer_moore_real, time_kmp_real, time_rabin_karp_real):.5f} sec.
- Fastest algorithm for the non-existing substring: {min(time_boyer_moore_fake, time_kmp_fake, time_rabin_karp_fake):.5f} sec.
- Overall most efficient algorithm for the given texts: {min(time_boyer_moore_real + time_boyer_moore_fake, time_kmp_real + time_kmp_fake, time_rabin_karp_real + time_rabin_karp_fake):.5f} sec.
"""

# Write summary to a markdown file
with open("summary.md", "w", encoding="utf-8") as f:
    f.write(summary)

print("Summary written to summary.md")