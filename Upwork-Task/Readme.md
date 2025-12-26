# Influence Recommendation System


## Proposed Solution

### 1. Graph Modeling
- Used an adjacency list (`map[int]bool`) for fast friendship lookup.
- Compute degree (friend count) for every user.

### 2. Candidate Classification
For every user U:
- Skip if U == K or already a friend of K.
- Count mutual friends between U and K.
- Separate candidates into:
  - With mutual friends
  - Without mutual friends

### 3. Sorting Rules

#### Candidates with Mutual Friends
Sorted by:
1. Mutual friends (descending)
2. Total friend count (descending)
3. User ID (ascending)

#### Candidates without Mutual Friends
Sorted by:
1. Total friend count (descending)
2. User ID (ascending)

### 4. Result Assembly
- Select from mutual candidates first.
- If less than L, fill from non-mutual candidates.
- If still insufficient, pad with `0`.

---

## Correctness Argument

- All recommendations exclude existing friends of K.
- Mutual friend counts are computed exactly via set intersection.
- Sorting strictly follows problem priority rules.
- Fallback logic guarantees exactly L outputs.

Therefore, the algorithm always produces a valid and optimal recommendation list.

---

## Complexity Analysis

Let:
- N = number of users (≤ 1024)
- M = number of friendships (≤ 10240)

### Time Complexity
- Graph construction: **O(M)**
- Mutual friend counting: **O(N × avg_degree)** (bounded, small)
- Sorting: **O(N log N)**

Overall: **O(N log N)**

### Space Complexity
- Adjacency lists: **O(N + M)**
- Candidate lists: **O(N)**

---

## Example

**Input**
6 8 1 2
1 2
1 3
2 4
3 4
4 5
5 6
2 5
3 6


**Output**
4 5