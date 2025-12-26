# Algorithm and Programming Ability Test

**Instructions:**
Please choose **one** of the following two algorithm problems to answer.

**Submission Contents** (e.g., using Java):
1.  **Code File**: A compilable and runnable `.java` source file.
2.  **Documentation**: A Markdown (`.md`) document containing your understanding of the problem, solution approach, and algorithm complexity analysis.

---

## Problem 1: Binary Tree Difference Check

### Problem Description
Given an **Expected State Binary Tree** and an **Actual State Binary Tree**.
*   Both trees are **Perfect Binary Trees** (each node has exactly two children, except for leaf nodes, and all leaves are at the same level).
*   Input is given as an array in **Level Order Traversal**.
*   Node values range from $[1, 1000]$, and the depth of the binary tree does not exceed $1000$.

**Check Rules**:
Compare nodes at the **same level and same position** in both trees:
*   Calculate the **Difference Value**: $Diff = | \text{Expected Value} - \text{Actual Value} |$ (absolute difference).
*   If $Diff = 0$, the states are consistent, ignore this node.
*   If $Diff > 0$, a discrepancy exists, keep this difference value.

**Output Requirements**:
Collect all **non-zero difference values** and sort them according to the following priority:
1.  Sort by **Frequency** from high to low.
2.  If frequencies are the same, sort by **Difference Value** from large to small.
3.  If the trees are identical (no non-zero differences), return 0.

### Input Description
Input consists of four lines:
1.  Number of nodes in the Expected Binary Tree.
2.  Node values of the Expected Binary Tree (Level Order Traversal, space-separated).
3.  Number of nodes in the Actual Binary Tree.
4.  Node values of the Actual Binary Tree (Level Order Traversal, space-separated).

### Output Description
Output a single string representing the sorted difference values (concatenated directly without separators).

### Example

**Input**
```text
7
10 5 15 2 8 12 20
7
10 8 15 5 5 18 20
```

**Output**
```text
3336
```

**Example Explanation**
1.  **Node Comparison**:
    *   **Level 1**: `10` vs `10` -> $Diff=0$ (Ignore).
    *   **Level 2**:
        *   Left: `5` vs `8` -> $Diff=|5-8|=3$.
        *   Right: `15` vs `15` -> $Diff=0$ (Ignore).
    *   **Level 3**:
        *   Pos 1: `2` vs `5` -> $Diff=|2-5|=3$.
        *   Pos 2: `8` vs `5` -> $Diff=|8-5|=3$.
        *   Pos 3: `12` vs `18` -> $Diff=|12-18|=6$.
        *   Pos 4: `20` vs `20` -> $Diff=0$ (Ignore).
2.  **Difference Collection**: `3, 3, 3, 6`.
3.  **Frequency Statistics**:
    *   `3`: 3 times
    *   `6`: 1 time
4.  **Sorting**: Higher frequency first (`3`), same frequency sorted by value descending (`6` comes after).
    *   The sequence is `3, 3, 3` followed by `6`.
    *   Concatenated result: `3336`.

---

## Problem 2: Influence Recommendation System

### Problem Description
You are developing an influence recommendation module for a social network platform. There are $N$ users (numbered $1$ to $N$), and the system maintains friendship records.
To help users expand high-quality social circles, the system recommends friends based on "**Mutual Friends Count**" and "**Candidate Activity Level**".

**Recommendation Rules**:
Given a user ID $K$, output the top $L$ users with the strongest potential connection to user $K$.
1.  **Candidate Eligibility**: Recommended users must NOT already be friends with $K$ (only non-friends can be recommended).
2.  **Similarity Calculation**: Similarity between two non-friend users = Number of mutual friends they share.
3.  **Sorting Rules**:
    *   **1st Priority**: Sort by **Similarity** (Mutual Friends Count) from high to low.
    *   **2nd Priority**: If similarity is the same, sort by **Candidate's Total Friend Count** (Degree) from high to low (prioritize active users).
    *   **3rd Priority**: If both above are the same, sort by **User ID** from small to large.
4.  **Quota Filling**:
    *   If the number of recommended users meeting the condition (having mutual friends) is less than $L$, fill the remaining spots with other non-friends (strangers) who have **no mutual friends** with $K$, sorted by **Total Friend Count from high to low** (then by ID ascending).
    *   If all non-friends are exhausted and the count is still less than $L$, use `0` as a placeholder for remaining spots.

### Input Description
The first line contains four integers $N, M, K, L$:
*   $N$: Number of users ($N \le 1024$)
*   $M$: Number of friendship records ($M \le 10240$)
*   $K$: Query User ID
*   $L$: Number of friends to recommend

The following $M$ lines each contain two integers $X$ and $Y$, indicating that user $X$ and user $Y$ are friends.
(Input guarantees $X \neq Y$, and the same friendship pair will not be repeated).

### Output Description
Output a single line containing $L$ integers, representing the recommended user IDs, separated by spaces.

### Example

**Input**
```text
6 8 1 2
1 2
1 3
2 4
3 4
4 5
5 6
2 5
3 6
```

**Output**
```text
4 5
```

**Example Explanation**
1.  **User Relationships**:
    *   User 1's Friends: `2, 3`.
    *   User 1's Non-Friends: `4, 5, 6`.
2.  **Analyze Non-Friends**:
    *   **User 4**:
        *   Friend List: `2, 3, 5` (Total 3).
        *   Mutual Friends with User 1: `2, 3` (Count: 2).
    *   **User 5**:
        *   Friend List: `4, 6, 2` (Total 3).
        *   Mutual Friends with User 1: `2` (Count: 1).
    *   **User 6**:
        *   Friend List: `5, 3` (Total 2).
        *   Mutual Friends with User 1: `3` (Count: 1).
3.  **Sorting Logic**:
    *   **Rank 1**: User 4. Similarity = 2 (Highest).
    *   **Rank 2 Contest**: User 5 vs User 6.
        *   Similarity is both 1.
        *   Compare Activity (Total Friend Count):
            *   User 5 has 3 friends.
            *   User 6 has 2 friends.
        *   User 5 wins.
4.  **Final Recommendation**: `4 5`.
