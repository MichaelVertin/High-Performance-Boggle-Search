# Running The Program
## Install Python
Install Python

## Execute the script
In The Command Line\
`python boggle.py <Board File Name>.txt <Dictionary File Name>.txt`

## Output
For a board file name \<FileName\>.txt, the output file name will be \<FileName\>_words.txt

# Optimization 1 - Reducing Redundant Iterations
## Problem
There are many duplicate prefixes when iterating over each word in the dictionary. 
```
# read all words in file
for word in open(filename):
    # iterate over selected indices
    for endIndex in range( len(word) ):
        prefix = word[:endIndex]
        beginsWithObject.add( prefix )
```
For example, after iterating over "programers", the beginsWithObject would contain {"p", "pr", "pro", "prog", "progr", "progra", "program", "programe", "programer"}. \
The next iteration would add each prefix of the next word, "programing", to the beginsWithObject in the order: "p", "pr", "pro", "prog", "progr", "progra", "program", "programi", "programin"\
Because these words start with the same 7 letters, 7 of the iterations try to add a prefix that already exists in the beginsWithObject, so each of those iterations are redundant. \

## Solution - Concept
Due to the large number of words in the dictionary, and many words having 8+ characters, the goal is to minimize the amount of redundant iterations. \
Due to extra data being added in each iteration, there is not enough information in any loop to determine if the next iteration(s) are redundant. \
This property can be removed by instead iterating from the largest prefix to the smallest prefix, so that information is being lost instead of gained. \
After iterating over "programers", the beginsWithObject would still contain {"p", "pr", "pro", "prog", "progr", "progra", "program", "programe", "programer"}. \
The next iteration would add each prefix of the next word, "programing", to the beginsWithObject in the order: "programin", "programi", "program", "progra", "progr", "prog", "pro", "pr", "p"
The same 7 redundant prefixes are still being added to the beginsWithObject. However, because they are at the end, a break statement can be used to skip over these iterations as soon as the redundancy begins. 
Instead of adding: ["programin", "programi", ..., "p"], the system can break out of the loop once a redundancy is detected. \
It instead can add just ["programin", "programi"] before identifying that "program" is already in the loop, and move on to the next word. \

## Solution - Correctness
### Conditions
1. The beginsWithObject contains every prefix of every word it has been exposed to.\
2. For any prefix in the beginsWithObject, the beginsWithObject contains every prefix of that prefix.\
### Iterations
The beginsWithObject starts empty when no words have been added -> Valid Initial State\
When a word is added that does not contain a prefix already in the beginsWithObject, it cannot break out because no prefixes exist yet, so every prefix being added -> Valid Step\
When a word is added that does contain a prefix in the beginsWithObject, the loop will break at a word of length n, when n is shown to already exist in the beginsWithObject. Before the word of length n, all prefixes greater than length n in the word have already been added. Due to condition 2, the beginsWithObject has all prefixes of the prefix of the word of length n. These are the same as all prefixes bewteen length 0 and n of the word. -> Valid Step

## Solution - Implementation
```
# read all words in file
for word in open(filename):
    # (inclusive) do not include the last char in word
    rangeMax = len( word ) - 1

    # iterate over selected indices (reversed)
    for endIndex in range( rangeMax, rangeMin, -1 ):
        prefix = word[:endIndex]

        # stop if already observed prefix
        if prefix in beginsWithObject:
            break
                
        beginsWithObject.add( prefix )
```
The system now iterates over all the words in reverse, and breaks out of the loop when a duplicate is encountered. The output of this implementation is identical to the output of the unoptimized implementation. 

# Optimization 2: Balancing Efficiency and Accuracy

## Problem
Most dictionary words are never used. Processing each word consumes significant time for little value.

## Solution (Conceptual)
The largest words both consume the most time to store and are the least likely to be in the result. \
I determined the chance that a word between 8 and 16 letters would be in the 4x4 board, and used this to identify what words could be skipped over. \
The resulting decision was words of length 8, as this was shown to reduce accuracy by only .11%, and more than halved runtime. 

---

# Optimization 3: Board-Specific Properties

## Problem
Building the complete prefix set for all dictionary words takes the same amount of time regardless of board size. But certain boards have unique qualities that can be taken advantage of to reduce the need for this structure.

## Solution (Conceptual)
When finding words in the board, after any letter, the next letter must be adjacent to that letter and not already selected. \
For large board setups, this can be done by implementing this behavior as written. However, for smaller boards, its properties allow for a simpler solution. \
If the board has size no greater than 2, then the list of valid following letters is equal to any letter that has not been used yet because all letters are adjacent. \
The list of valid letter combinations can quickly be identified by taking all permutations of the board as a 4-letter string, without need for the complex validity checks. \
Because there is no longer logic testing if the current progress is a prefix of a valid word, the prefix set does not need to be calculated, which is by far the most computationally expensive part of this project for small boards. 

## Solution (High-Level Implementation)
```
# Only read the dictionary words from the dictionary
# Store all letters in the board into a single string
# Find all permutations of the board string (both full and partial)
# Return all permutations that are in the dictionary
```
This reduces the time consumed from 80-120ms down to 20-40ms for a 2x2 board after the other optimizations. 

---

# Performance
Lost .03% accurracy on a 4x4 board and performed 300% faster. \
Lost near 0 accuracy on a 3x3 board and performed 300% faster. \
Lost no accuracy on a 2x2 board and performed 900% faster. \

The professor of the course used tested my submission against the next semester's course, and provided me with the following results:
<Graphs showing performance compared to next-semester students>