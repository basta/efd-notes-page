# Knapsack Problem — Worked Examples

> *This page collects worked examples mined from the lecture slides. Solutions are synthesised by Claude from the slides' stated algorithms — verify against the originals before relying on them for an exam.*

### 2-Approximation on $c=(6,20,2),\ w=(2,10,8),\ W=10$

> *Worked example identified and solved by Claude from the lecture slides — verify against the originals before relying on it for an exam.*

**Problem.** The slides give the instance

$$c = (6, 20, 2),\quad w = (2, 10, 8),\quad W = 10$$

and ask for the 2-approximate solution of the 0/1 Knapsack problem.

**Approach.** Apply the 2-approximation algorithm from the slides:

1. Verify $w_j \le W$ for every item and $\sum_i w_i > W$.
2. Sort items by relative cost $c_j / w_j$ in decreasing order and re-index.
3. Find $h = \min\{\,j : \sum_{i=1}^{j} w_i > W\,\}$.
4. Output the better of $\{1,\dots,h-1\}$ and $\{h\}$.

The theorem guarantees that this output has cost $\ge \tfrac{1}{2} J^{*}(I)$.

**Solution.**

1. Feasibility check: $w_1=2,\ w_2=10,\ w_3=8$, all $\le W=10$, and $\sum w_i = 20 > 10$, so the theorem applies.
2. Relative costs: $c_1/w_1 = 6/2 = 3$, $c_2/w_2 = 20/10 = 2$, $c_3/w_3 = 2/8 = 0.25$. The given ordering already satisfies $c_1/w_1 \ge c_2/w_2 \ge c_3/w_3$, so no re-indexing is needed.
3. Prefix weights along the sorted list:

    - $\sum_{i=1}^{1} w_i = 2 \le 10$,
    - $\sum_{i=1}^{2} w_i = 12 > 10$.

    Hence $h = 2$.

4. Candidate solutions:

    - $\{1,\dots,h-1\} = \{1\}$ with cost $c_1 = 6$ and weight $2$.
    - $\{h\} = \{2\}$ with cost $c_2 = 20$ and weight $10$.

    The better candidate is $\{2\}$ with cost $20$.

5. Upper bound used in the proof: $\sum_{i=1}^{h} c_i = c_1 + c_2 = 26$, so the algorithm guarantees at least $26/2 = 13$. The returned $20 \ge 13$. By exhaustive enumeration the true optimum is also $\{2\}$ with cost $20$, so on this instance the approximation is tight (it actually equals the optimum).

**Answer.** $S = \{2\}$, cost $20$, weight $10$.

**Pitfalls / insight.** The algorithm *only* compares the two specific candidates $\{1,\dots,h-1\}$ and $\{h\}$ — not, for example, $\{1, h\}$ or anything past $h$. The key inequality is that $\sum_{i=1}^{h} c_i$ upper-bounds the optimum (it is exactly the cost the *fractional* relaxation would attain on the first $h$ items if all were taken whole), and that taking the max of the two halves of this sum gives at least half of it. Make sure items are sorted by $c_j/w_j$ *before* picking $h$; sorting by raw cost or raw weight breaks the proof.

---

### Dynamic Programming on integer costs: $n=4,\ w=(21,35,52,17),\ c=(10,20,30,10),\ W=100$

> *Worked example identified and solved by Claude from the lecture slides — verify against the originals before relying on it for an exam.*

**Problem.** Blackboard instance from the slides:

$$n = 4,\quad w = (21, 35, 52, 17),\quad c = (10, 20, 30, 10),\quad W = 100.$$

Find an optimal subset $S$ by the integer-cost DP.

**Approach.** Use the slides' DP variable $x_k^{j}$ = *minimum weight* achievable by a subset of $\{1,\dots,j\}$ whose total cost equals $k$. Recursion:

$$x_k^{j} = \begin{cases} x_{k-c_j}^{j-1} + w_j & \text{if item } j \text{ is added,} \\ x_k^{j-1} & \text{otherwise,} \end{cases}$$

choosing the *added* branch whenever $x_{k-c_j}^{j-1} + w_j \le \min\{W, x_k^{j-1}\}$ and recording $s_k^{j} = 1$ in that case. Initial condition: $x_0^{0} = 0$, $x_k^{0} = \infty$ for $k \ge 1$. The optimum cost is $\max\{k : x_k^{n} \le W\}$.

**Solution.** Take the upper bound $C = c_1 + c_2 + c_3 + c_4 = 70$. Only finite entries are listed below; everything else stays at $\infty$.

1. Row $j = 0$: $x_0^{0} = 0$.
2. Row $j = 1$ ($c_1 = 10$, $w_1 = 21$). Update at $k \ge 10$:

    - $k=10$: $x_0^{0} + 21 = 21 \le \min(100,\infty)$, so $x_{10}^{1} = 21$, $s_{10}^{1} = 1$.

    Finite entries: $x_0^{1}=0,\ x_{10}^{1}=21$.

3. Row $j = 2$ ($c_2 = 20$, $w_2 = 35$). Update at $k \ge 20$:

    - $k=20$: $x_0^{1}+35 = 35$, store $x_{20}^{2}=35$, $s=1$.
    - $k=30$: $x_{10}^{1}+35 = 56$, store $x_{30}^{2}=56$, $s=1$.

    Finite entries: $x_0^{2}=0,\ x_{10}^{2}=21,\ x_{20}^{2}=35,\ x_{30}^{2}=56$.

4. Row $j = 3$ ($c_3 = 30$, $w_3 = 52$). Update at $k \ge 30$:

    - $k=30$: $x_0^{2}+52 = 52 \le \min(100, 56)$, replace: $x_{30}^{3}=52$, $s=1$.
    - $k=40$: $x_{10}^{2}+52 = 73$, store $x_{40}^{3}=73$, $s=1$.
    - $k=50$: $x_{20}^{2}+52 = 87$, store $x_{50}^{3}=87$, $s=1$.
    - $k=60$: $x_{30}^{2}+52 = 108 > W = 100$, reject.

    Finite entries: $x_0^{3}=0,\ x_{10}^{3}=21,\ x_{20}^{3}=35,\ x_{30}^{3}=52,\ x_{40}^{3}=73,\ x_{50}^{3}=87$.

5. Row $j = 4$ ($c_4 = 10$, $w_4 = 17$). Update at $k \ge 10$:

    - $k=10$: $x_0^{3}+17 = 17 \le \min(100, 21)$, replace: $x_{10}^{4}=17$, $s=1$.
    - $k=20$: $x_{10}^{3}+17 = 38 > 35 = x_{20}^{3}$, reject; keep $x_{20}^{4}=35$, $s=0$.
    - $k=30$: $x_{20}^{3}+17 = 52 \le 52 = x_{30}^{3}$, replace: $x_{30}^{4}=52$, $s=1$.
    - $k=40$: $x_{30}^{3}+17 = 69 \le 73 = x_{40}^{3}$, replace: $x_{40}^{4}=69$, $s=1$.
    - $k=50$: $x_{40}^{3}+17 = 90 > 87 = x_{50}^{3}$, reject; keep $x_{50}^{4}=87$, $s=0$.
    - $k=60$: $x_{50}^{3}+17 = 104 > 100$, reject.

    Finite entries: $x_0^{4}=0,\ x_{10}^{4}=17,\ x_{20}^{4}=35,\ x_{30}^{4}=52,\ x_{40}^{4}=69,\ x_{50}^{4}=87$.

6. Pick the largest $k$ with $x_k^{4} \le W=100$: $k^{*} = 50$, achieving weight $87$.
7. Reconstruct backwards from $(j,k) = (4, 50)$:

    - $s_{50}^{4} = 0$ → item $4$ excluded; move to $(3, 50)$.
    - $s_{50}^{3} = 1$ → item $3$ included; move to $(2, 50-30) = (2, 20)$.
    - $s_{20}^{2} = 1$ → item $2$ included; move to $(1, 20-20) = (1, 0)$.
    - $s_0^{1} = 0$ → item $1$ excluded.

**Answer.** $S = \{2, 3\}$, total cost $50$, total weight $87 \le 100$.

**Pitfalls / insight.** The state is indexed by *cost* (not weight), and the table stores the *minimum weight* to realise that cost. The condition for replacing $x_k^{j}$ is non-strict ($\le$), and you genuinely need the $\min\{W, x_k^{j-1}\}$ guard — both to prune infeasible cells and to keep only the lighter realisation of the same cost. When two solutions have equal weight (as at $k=30$ in row $4$), the algorithm overwrites and prefers including the newer item; this can shift the recovered set but never its cost.

---

### Dynamic Programming on integer weights: $n=4,\ w=(2,3,4,5),\ c=(3.1,4.2,5.1,4.3),\ W=8$

> *Worked example identified and solved by Claude from the lecture slides — verify against the originals before relying on it for an exam.*

**Problem.** Blackboard instance from the slides:

$$n = 4,\quad w = (2, 3, 4, 5),\quad c = (3.1, 4.2, 5.1, 4.3),\quad W = 8.$$

Costs are real-valued, weights are integers. Find an optimal subset.

**Approach.** The slides note that when *weights* are integers we flip the DP: index the table by weight $k$, store the **maximum cost** $y_k^{j}$ achievable on $\{1,\dots,j\}$ with total weight exactly $k$, and initialise $y_k^{0} := -\infty$ for $k \ge 1$, $y_0^{0} := 0$. Recursion:

$$y_k^{j} = \max\!\left\{\, y_k^{j-1},\ y_{k-w_j}^{j-1} + c_j \,\right\}$$

(the second branch is used only when $k \ge w_j$). Record $s_k^{j} = 1$ when the second branch wins. The optimum is $\max_{0 \le k \le W} y_k^{n}$.

**Solution.** $W = 8$, so we maintain columns $k = 0,1,\dots,8$. Entries shown as $-\infty$ are omitted from the listing.

1. Row $j=0$: $y_0^{0} = 0$; all other $y_k^{0} = -\infty$.
2. Row $j=1$ ($w_1=2$, $c_1=3.1$):

    - $k=0$: keep $0$.
    - $k=2$: $y_0^{0} + 3.1 = 3.1 > -\infty$, store $y_2^{1}=3.1$, $s=1$.
    - All other $k$: $-\infty$.

    Row: $y^{1} = (0,\, -\infty,\, 3.1,\, -\infty,\, -\infty,\, -\infty,\, -\infty,\, -\infty,\, -\infty)$.

3. Row $j=2$ ($w_2=3$, $c_2=4.2$):

    - $k=3$: $y_0^{1} + 4.2 = 4.2$, store $y_3^{2}=4.2$, $s=1$.
    - $k=5$: $y_2^{1} + 4.2 = 3.1 + 4.2 = 7.3$, store $y_5^{2}=7.3$, $s=1$.
    - Other reachable $k$ inherit row $j=1$.

    Finite entries: $y_0^{2}=0,\ y_2^{2}=3.1,\ y_3^{2}=4.2,\ y_5^{2}=7.3$.

4. Row $j=3$ ($w_3=4$, $c_3=5.1$):

    - $k=4$: $y_0^{2} + 5.1 = 5.1$, store $y_4^{3}=5.1$, $s=1$.
    - $k=5$: $\max(y_5^{2}=7.3,\ y_1^{2}+5.1=-\infty) = 7.3$, keep, $s=0$.
    - $k=6$: $y_2^{2} + 5.1 = 3.1 + 5.1 = 8.2$, store $y_6^{3}=8.2$, $s=1$.
    - $k=7$: $y_3^{2} + 5.1 = 4.2 + 5.1 = 9.3$, store $y_7^{3}=9.3$, $s=1$.
    - $k=8$: $y_4^{2}+5.1 = -\infty$, stays $-\infty$.

    Finite entries: $y_0^{3}=0,\ y_2^{3}=3.1,\ y_3^{3}=4.2,\ y_4^{3}=5.1,\ y_5^{3}=7.3,\ y_6^{3}=8.2,\ y_7^{3}=9.3$.

5. Row $j=4$ ($w_4=5$, $c_4=4.3$):

    - $k=5$: $\max(7.3,\ y_0^{3}+4.3=4.3) = 7.3$, $s=0$.
    - $k=6$: $\max(8.2,\ y_1^{3}+4.3=-\infty) = 8.2$, $s=0$.
    - $k=7$: $\max(9.3,\ y_2^{3}+4.3=3.1+4.3=7.4) = 9.3$, $s=0$.
    - $k=8$: $\max(-\infty,\ y_3^{3}+4.3=4.2+4.3=8.5) = 8.5$, $s=1$.

    Finite entries: $y_0^{4}=0,\ y_2^{4}=3.1,\ y_3^{4}=4.2,\ y_4^{4}=5.1,\ y_5^{4}=7.3,\ y_6^{4}=8.2,\ y_7^{4}=9.3,\ y_8^{4}=8.5$.

6. Maximum over $k \le 8$: $y_7^{4} = 9.3$ wins (note $y_8^{4} = 8.5 < 9.3$, so the heaviest legal knapsack is *not* the best).
7. Reconstruct from $(j,k) = (4, 7)$:

    - $s_7^{4} = 0$ → item $4$ excluded; go to $(3, 7)$.
    - $s_7^{3} = 1$ → item $3$ included; go to $(2, 7-4) = (2, 3)$.
    - $s_3^{2} = 1$ → item $2$ included; go to $(1, 3-3) = (1, 0)$.
    - $y_0^{1} = 0 = y_0^{0}$, $s_0^{1} = 0$ → item $1$ excluded.

**Answer.** $S = \{2, 3\}$, total weight $3 + 4 = 7$, total cost $4.2 + 5.1 = 9.3$.

**Pitfalls / insight.** Two things flip relative to the integer-cost DP:

- The table is indexed by **weight** and stores the **max cost**, so initialisation uses $-\infty$ (not $\infty$) and the recursion uses $\max$ (not $\min$).
- The optimum is *not necessarily* at $k = W$. Here $k = 7 < W = 8$ wins because adding any single remaining item would either overshoot $W$ or replace a high-value item with a lower-value one. Always scan the whole last row up to $W$ for the maximum, never just read off $y_W^{n}$.

Also note this DP runs in $O(n W)$ — pseudopolynomial in the weights, which is fine because $W$ is integer; the *costs* may be irrational without breaking the algorithm.
