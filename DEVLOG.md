# Development Log – The Torchbearer

**Student Name:** Ali Mansoor  
**Student ID:** 124060947

---

## Entry 1 – [May 14, 2026]: Initial Plan

I started by reading the assignment and separating the problem into two main parts. First I planned to compute shortest paths between important nodes using Dijkstra. Then I planned to search over the possible relic orders and keep the cheapest one. I expected the pruning and backtracking to be the trickiest part, so I planned to test after each function instead of waiting until the end.

---

## Entry 2 – [May 14, 2026]: Dijkstra and Precomputation

I implemented `select_sources`, `run_dijkstra`, and `precompute_distances`. My plan was to only run Dijkstra from the spawn and each relic, because those are the only places the route starts a new major leg from. I used a nested dictionary for the distance table so lookups like `dist_table[u][v]` are simple and fast.

---

## Entry 3 – [May 14, 2026]: Bug and Design Fix

At first, I was thinking about pruning only with the current cost so far. That was safe, but it did not cut many branches. I changed the design to use a simple lower bound that adds the cheapest next relic move and the cheapest possible final exit move. This still stays safe because it is optimistic and does not overestimate the real remaining cost.

---

## Entry 4 – [May 14, 2026]: Post-Implementation Reflection

After the implementation was complete, I tested the full pipeline with the provided tests. The recursive search worked by removing a relic from the remaining set, exploring that branch, and then adding it back during backtracking. If I had more time, I would add more custom tests with bigger graphs and edge cases involving unreachable relics.

---

## Final Entry – [May 14, 2026]: Time Estimate

| Part | Estimated Hours |
|---|---:|
| Part 1: Problem Analysis | 0.25 |
| Part 2: Precomputation Design | 0.50 |
| Part 3: Algorithm Correctness | 0.50 |
| Part 4: Search Design | 0.25 |
| Part 5: State and Search Space | 0.50 |
| Part 6: Pruning | 0.50 |
| Part 7: Implementation | 1.50 |
| README and DEVLOG writing | 0.75 |
| **Total** | **4.75** |
