# Boggle Solver

## Running the Program

### Requirements
- Python 3.x

### Execution
Run the script from the command line:

```
python boggle.py <BoardFileName>.txt <DictionaryFileName>.txt
```

The program outputs results to: `<BoardFileName>_words.txt`.

---

# Optimization 1: Eliminating Redundant Iterations

## Problem
Many words in the dictionary share common prefixes. In the original prefix-building implementation, these shared prefixes were added many times. 

**Example:**  
After processing `"programmers"`, the prefix set contains:
```
{"p", "pr", "pro", "prog", "progr", "progra", "program", "programm", "programme", "programmer" }
```
The next word, `"programming"`, shares 8 of these prefixes. These 8 additions are redundant.

## Solution
Instead of adding prefixes from the start of the word, iterate from the longest prefix to the shortest. Stop as soon as a prefix is found in the set. This ensures no more than one duplicate prefix is handled. 

**Original approach:**
```python
for endIndex in range(len(word)):
    prefix = word[:endIndex]
    beginsWithObject.add(prefix)
```

**Optimized approach:**
```python
for endIndex in range(len(word) - 1, 0, -1):
    prefix = word[:endIndex]
    if prefix in beginsWithObject:
        break
    beginsWithObject.add(prefix)
```

## Why it works
- The set always includes every prefix of previously seen words.
- If a prefix is already in the set, shorter prefixes must also be present.
- Therefore, skipping once a known prefix is found does not miss necessary entries.

---


# Optimization 2: Balancing Efficiency and Accuracy

## Problem
Most dictionary words are never used, and processing them adds unnecessary runtime.

## Solution
Longer words are both less likely to appear and take more time to process. 
Analyzing the probability of words of length >= showed:
- Excluding words of length > 8 reduced accuracy by only **0.11%**
- Runtime was cut by more than **50%**
This tradeoff significantly decreased runtime while maintaining high accuracy. 

---

# Optimization 3: Board-Specific Properties

## Problem
Prefix construction takes the same time for all boards sizes, even if the board's layout makes prefix analysis unnecessary. 

## Solution
When finding words, each next letter must be adjacent to the current one and not already used.  
For large boards, this requires adjacency checks at every step.  

For **boards of size <= 2x2**, every letter is adjacent to every other letter. This means:
- Adjacent checks are not necessary. 
- Word iteration in the board can be replaced by generatic all permutation of board letters. 

## High-Level Implementation
```
# Read only the dictionary words
# Store all letters in the board as a single string
# Generate all permutations of the board string (both full and partial)
# Return all permutations that are in the dictionary
```
This allows generating all possible letter combinations directly, avoiding prefix checks entirely. Since prefix-set construction is the most expensive part of the process for small boards, skipping it yields a major speedup.

Impact:
- Completely removed the prefix building
- 2x2 runtime dropped from 80-120 ms to 20-40 ms.

# Post-Optimization Results

| Board Size | Accuracy Loss | Speedup |
| ---------- | ------------: | ------: |
| 6×6        |          0.1% |    590% |
| 4×4        |         0.03% |    550% |
| 2×2        |            0% |   1300% |

When the professor benchmarked after the competition, this implementation completed a 6×6 board 375% faster than the next-fastest program from a later semester.

<img width="756" height="755" alt="image" src="https://github.com/user-attachments/assets/3cc8db55-968b-4f90-85e6-cf027d827f06" />
