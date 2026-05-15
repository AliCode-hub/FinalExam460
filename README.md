# The Torchbearer

**Student Name:** Ali Mansoor  
**Student ID:** 124060947  
**Course:** CS 460 – Algorithms | Spring 2026

---

## Part 1: Problem Analysis

- **Why a single shortest-path run from S is not enough:**
  A single shortest-path run from S is not enough because it only gives cheapest distances from the entrance. It does not decide which relic should be collected first, second, and so on.

- **What decision remains after all inter-location costs are known:**
  After the inter-location costs are known, the remaining decision is the order of the relic chambers before ending at T.

- **Why this requires a search over orders (one sentence):**
  This requires a search over orders because different relic orders can use the same distance table but still produce different total fuel costs.

---

## Part 2: Precomputation Design

### Part 2a: Source Selection

| Source Node Type | Why it is a source |
|---|---|
| Spawn / entrance node | The route starts here, so I need distances from S to every relic. |
| Relic chamber nodes | After collecting a relic, the route may need to go to another relic or to the exit. |

### Part 2b: Distance Storage

| Property | Your answer |
|---|---|
| Data structure name | Nested dictionary called `dist_table` |
| What the keys represent | Outer key is the source node, inner key is the destination node |
| What the values represent | Cheapest fuel cost from the source node to the destination node |
| Lookup time complexity | O(1) average case |
| Why O(1) lookup is possible | Python dictionaries use hashing for direct key lookup |

### Part 2c: Precomputation Complexity

- **Number of Dijkstra runs:** k + 1 runs, one from the spawn and one from each relic.
- **Cost per run:** O(m log n).
- **Total complexity:** O((k + 1)m log n), which simplifies to O(km log n).
- **Justification (one line):** There are k relics plus the spawn, and each source runs Dijkstra once.

---

## Part 3: Algorithm Correctness

### Part 3a: Invariant Explanation

- **For nodes already finalized (in S):**
  Finalized nodes already have their real shortest distance from the source. Once a node is finalized, the algorithm does not need to improve it later.

- **For nodes not yet finalized (not in S):**
  Non-finalized nodes only have the best distance found so far. That estimate is based on paths that have already gone through finalized nodes.

### Part 3b: Invariant Maintenance

- **Initialization : why the invariant holds before iteration 1:**
  The source starts with distance 0 because it costs nothing to be where we already are. Every other node starts at infinity because no path has been found yet.

- **Maintenance : why finalizing the min-dist node is always correct:**
  The node with the smallest current distance is safe to finalize because all edge weights are nonnegative. A later path cannot go through extra nonnegative edges and somehow become cheaper than the current minimum.

- **Termination : what the invariant guarantees when the algorithm ends:**
  When the algorithm ends, every reachable node has its true shortest-path distance from the source. Any node still at infinity is unreachable.

### Part 3c: Why This Matters for the Route Planner

Correct shortest-path distances matter because the route planner compares relic orders using those costs, so bad distances would make it choose the wrong route.

---

## Part 4: Search Design

### Why Greedy Fails

- **The failure mode:** Greedy fails because the closest next relic is not always part of the cheapest full route.
- **Counter-example setup:** S to A costs 1, S to B costs 2, A to B costs 100, B to A costs 1, A to T costs 1, and B to T costs 1.
- **What greedy picks:** Greedy picks A first because A is closest from S, giving S -> A -> B -> T with cost 102.
- **What optimal picks:** The optimal route is S -> B -> A -> T, with total fuel cost 4.
- **Why greedy loses:** Greedy loses because the cheap first move to A creates a very expensive move from A to B later.

### What the Algorithm Must Explore

- The algorithm must explore possible relic collection order choices and keep the cheapest complete route it finds.

---

## Part 5: State and Search Space

### Part 5a: State Representation

| Component | Variable name in code | Data type | Description |
|---|---|---|---|
| Current location | `current_loc` | node | The node where the search currently is |
| Relics already collected | `relics_visited_order` | list[node] | The relics collected so far, in order |
| Fuel cost so far | `cost_so_far` | float/int | The total fuel spent so far |

### Part 5b: Data Structure for Visited Relics

| Property | Your answer |
|---|---|
| Data structure chosen | `set` named `relics_remaining` |
| Operation: check if relic already collected | Time complexity: O(1) average case |
| Operation: mark a relic as collected | Time complexity: O(1) average case with `remove` |
| Operation: unmark a relic (backtrack) | Time complexity: O(1) average case with `add` |
| Why this structure fits | A set makes it fast to track which relics still need to be explored |

### Part 5c: Worst-Case Search Space

- **Worst-case number of orders considered:** k! orders.
- **Why:** In the worst case, every relic can be chosen in any position, so the search may try every permutation.

---

## Part 6: Pruning

### Part 6a: Best-So-Far Tracking

- **What is tracked:** The algorithm tracks the best complete route cost and the relic order that produced it.
- **When it is used:** It is used during recursion before continuing deeper into a branch.
- **What it allows the algorithm to skip:** It skips any branch that already cannot beat the best complete solution found so far.

### Part 6b: Lower Bound Estimation

- **What information is available at the current state:** The search knows the current location, the remaining relics, the cost so far, the exit, and the precomputed distances.
- **What the lower bound accounts for:** The lower bound accounts for the cost already spent, the cheapest required move to some remaining relic, and the cheapest final move from a remaining relic to the exit.
- **Why it never overestimates:** It uses minimum possible costs, so it is optimistic and can only be less than or equal to a real completion cost.

### Part 6c: Pruning Correctness

- If the lower bound is already greater than or equal to the best complete route, then no route under that branch can improve the answer.
- This is safe because the lower bound does not exaggerate future cost, so it cannot accidentally remove the true optimal route.

---

## References

- Lecture notes only.
