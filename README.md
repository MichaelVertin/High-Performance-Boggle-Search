# Running the Program

## Requirements
- Python 3.x

## Execution
Run the script from the command line:

```bash
python boggle.py <BoardFileName>.txt <DictionaryFileName>.txt
```

The output will be saved to a file named `<BoardFileName>_words.txt`.

---

# Optimization 1: Reducing Redundant Iterations

## Problem
Many words in the dictionary share common prefixes. When iterating over each word to build a prefix set (`beginsWithObject`), redundant work is done repeatedly for shared prefixes.

**Example:**  
After processing `"programmers"`, the prefix set includes:
```
{"p", "pr", "pro", "prog", "progr", "progra", "program", "programm", "programme", "programmer" }
```
The next word, `"programming"`, shares 8 of these prefixes. These 8 additions are redundant.

## Solution
Instead of adding prefixes from the start of the word, iterate from the longest prefix to the shortest. Stop as soon as a prefix is found in the set. This restricts duplicate operations to one per word. 

**Old approach:**
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

## Correctness
- The set always includes every prefix of previously seen words.
- If a prefix is already in the set, shorter prefixes must also be present.
- Skipping once a known prefix is found does not miss necessary entries.

---


# Optimization 2: Balancing Efficiency and Accuracy

## Problem
Most dictionary words are never used, and processing each one consumes time with little benefit.

## Solution (Conceptual)
Longer words both take more time to store and are less likely to appear on the board.  
I calculated the probability of a word (length 8–16) appearing in a 4×4 board and used this to determine a safe cutoff.  

The analysis showed that excluding words of length >= **8** reduced accuracy by only **0.11%**, while **more than halving** the runtime.

---

# Optimization 3: Board-Specific Properties

## Problem
Building the complete prefix set for all dictionary words takes the same time regardless of board size. However, some board sizes allow simpler solutions that avoid building this expensive structure.

## Solution (Conceptual)
When finding words, each next letter must be adjacent to the current one and not already used.  
For large boards, this requires adjacency checks at every step.  

However, for **boards of size ≤ 2**, every letter is adjacent to every other letter, so the next letter is simply **any unused letter**.  

This allows generating all possible letter combinations directly, avoiding prefix checks entirely. Since prefix-set construction is the most expensive part of the process for small boards, skipping it yields a major speedup.

## High-Level Implementation
```
# Read only the dictionary words
# Store all letters in the board as a single string
# Generate all permutations of the board string (both full and partial)
# Return all permutations that are in the dictionary
```
Performance Impact:
For a 2×2 board, runtime dropped from 80–120 ms to 20–40 ms after adding this optimization.


# Post-Optimization Performance

- **6x6 board**: 0.1% accuracy loss, **590% faster**
- **4x4 board**: 0.03% accuracy loss, **550% faster**
- **2x2 board**: No accuracy loss, **1300% faster**

After winning the competition, the professor benchmarked this implementation against the next semester’s submissions. On a 6×6 board, it completed over 375% faster than the next fastest program, as shown below.

<img width="756" height="755" alt="image" src="https://github.com/user-attachments/assets/3cc8db55-968b-4f90-85e6-cf027d827f06" />
