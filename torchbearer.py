"""
CS 460 – Algorithms: Final Programming Assignment
The Torchbearer

Student Name: Ali Mansoor
Student ID:   124060947

INSTRUCTIONS
------------
- Implement every function marked TODO.
- Do not change any function signature.
- Do not remove or rename required functions.
- You may add helper functions.
- Variable names in your code must match what you define in README Part 5a.
- The pruning safety comment inside _explore() is graded. Do not skip it.

Submit this file as: torchbearer.py
"""

import heapq


# =============================================================================
# PART 1
# =============================================================================

def explain_problem():
    """
    Returns
    -------
    str
        Your Part 1 README answers, written as a string.
        Must match what you wrote in README Part 1.
    """
    return (
        "A single shortest-path run from S is not enough because it only gives cheapest "
        "distances from the entrance. It does not decide which relic should be collected "
        "first, second, and so on.\n"
        "After the inter-location costs are known, the remaining decision is the order of "
        "the relic chambers before ending at T.\n"
        "This requires a search over orders because different relic orders can use the same "
        "distance table but still produce different total fuel costs."
    )


# =============================================================================
# PART 2
# =============================================================================

def select_sources(spawn, relics, exit_node):
    """
    Parameters
    ----------
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    list[node]
        No duplicates. Order does not matter.
    """
    sources = []
    for node in [spawn] + list(relics):
        if node not in sources:
            sources.append(node)
    return sources


def run_dijkstra(graph, source):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
        graph[u] = [(v, cost), ...]. All costs are nonnegative integers.
    source : node

    Returns
    -------
    dict[node, float]
        Minimum cost from source to every node in graph.
        Unreachable nodes map to float('inf').
    """
    dist = {node: float('inf') for node in graph}
    dist[source] = 0
    counter = 0
    pq = [(0, counter, source)]

    while pq:
        current_dist, _, current_node = heapq.heappop(pq)

        if current_dist != dist[current_node]:
            continue

        for neighbor, edge_cost in graph.get(current_node, []):
            new_dist = current_dist + edge_cost
            if neighbor not in dist:
                dist[neighbor] = float('inf')
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                counter += 1
                heapq.heappush(pq, (new_dist, counter, neighbor))

    return dist


def precompute_distances(graph, spawn, relics, exit_node):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    dict[node, dict[node, float]]
        Nested structure supporting dist_table[u][v] lookups
        for every source u your design requires.
    """
    dist_table = {}
    for source in select_sources(spawn, relics, exit_node):
        dist_table[source] = run_dijkstra(graph, source)
    return dist_table


# =============================================================================
# PART 3
# =============================================================================

def dijkstra_invariant_check():
    """
    Returns
    -------
    str
        Your Part 3 README answers, written as a string.
        Must match what you wrote in README Part 3.
    """
    return (
        "Finalized nodes already have their real shortest distance from the source, so they "
        "do not need to be changed later.\n"
        "Non-finalized nodes only have the best distance found so far using paths that go "
        "through finalized nodes first.\n"
        "At initialization, the source has distance 0 and every other node starts at infinity.\n"
        "During maintenance, the smallest-distance node can be finalized because all edge "
        "weights are nonnegative, so a later path cannot come back and make it cheaper.\n"
        "At termination, every reachable node has its true shortest distance and unreachable "
        "nodes stay at infinity.\n"
        "This matters because the route planner depends on these distances when comparing "
        "different relic orders."
    )


# =============================================================================
# PART 4
# =============================================================================

def explain_search():
    """
    Returns
    -------
    str
        Your Part 4 README answers, written as a string.
        Must match what you wrote in README Part 4.
    """
    return (
        "Greedy fails because the closest next relic is not always part of the cheapest full route.\n"
        "Counter-example: S to A costs 1, S to B costs 2, A to B costs 100, B to A costs 1, "
        "A to T costs 1, and B to T costs 1.\n"
        "Greedy picks A first because A is closest from S, giving S -> A -> B -> T with cost 102.\n"
        "The optimal route is S -> B -> A -> T with total cost 4.\n"
        "The algorithm must explore more than one order because a locally cheap step can make "
        "the rest of the route more expensive."
    )


# =============================================================================
# PARTS 5 + 6
# =============================================================================

def find_optimal_route(dist_table, spawn, relics, exit_node):
    """
    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
        Output of precompute_distances.
    spawn : node
    relics : list[node]
        Every node in this list must be visited at least once.
    exit_node : node
        The route must end here.

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.
    """
    current_loc = spawn
    relics_remaining = set(relics)
    relics_visited_order = []
    cost_so_far = 0
    best = [float('inf'), []]

    _explore(
        dist_table,
        current_loc,
        relics_remaining,
        relics_visited_order,
        cost_so_far,
        exit_node,
        best,
    )

    if best[0] == float('inf'):
        return (float('inf'), [])
    return (best[0], best[1])


def _lower_bound(dist_table, current_loc, relics_remaining, cost_so_far, exit_node):
    """Return a safe lower bound for any completion from this state."""
    if not relics_remaining:
        return cost_so_far + dist_table.get(current_loc, {}).get(exit_node, float('inf'))

    first_step = min(
        dist_table.get(current_loc, {}).get(relic, float('inf'))
        for relic in relics_remaining
    )
    exit_step = min(
        dist_table.get(relic, {}).get(exit_node, float('inf'))
        for relic in relics_remaining
    )
    return cost_so_far + first_step + exit_step


def _explore(dist_table, current_loc, relics_remaining, relics_visited_order,
             cost_so_far, exit_node, best):
    """
    Recursive helper for find_optimal_route.

    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
    current_loc : node
    relics_remaining : collection
        Your chosen data structure from README Part 5b.
    relics_visited_order : list[node]
    cost_so_far : float
    exit_node : node
    best : list
        Mutable container for the best solution found so far.

    Returns
    -------
    None
        Updates best in place.
    """
    lower_bound = _lower_bound(
        dist_table, current_loc, relics_remaining, cost_so_far, exit_node
    )

    # This pruning is safe because lower_bound only counts costs that every completion
    # must still pay. If it is already not better than best, this branch cannot become optimal.
    if lower_bound >= best[0]:
        return

    if not relics_remaining:
        total_cost = cost_so_far + dist_table.get(current_loc, {}).get(exit_node, float('inf'))
        if total_cost < best[0]:
            best[0] = total_cost
            best[1] = list(relics_visited_order)
        return

    for next_relic in list(relics_remaining):
        travel_cost = dist_table.get(current_loc, {}).get(next_relic, float('inf'))
        if travel_cost == float('inf'):
            continue

        relics_remaining.remove(next_relic)
        relics_visited_order.append(next_relic)

        _explore(
            dist_table,
            next_relic,
            relics_remaining,
            relics_visited_order,
            cost_so_far + travel_cost,
            exit_node,
            best,
        )

        relics_visited_order.pop()
        relics_remaining.add(next_relic)


# =============================================================================
# PIPELINE
# =============================================================================

def solve(graph, spawn, relics, exit_node):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.
    """
    dist_table = precompute_distances(graph, spawn, relics, exit_node)
    return find_optimal_route(dist_table, spawn, relics, exit_node)


# =============================================================================
# PROVIDED TESTS (do not modify)
# Graders will run additional tests beyond these.
# =============================================================================

def _run_tests():
    print("Running provided tests...")

    # Test 1: Spec illustration. Optimal cost = 4.
    graph_1 = {
        'S': [('B', 1), ('C', 2), ('D', 2)],
        'B': [('D', 1), ('T', 1)],
        'C': [('B', 1), ('T', 1)],
        'D': [('B', 1), ('C', 1)],
        'T': []
    }
    cost, order = solve(graph_1, 'S', ['B', 'C', 'D'], 'T')
    assert cost == 4, f"Test 1 FAILED: expected 4, got {cost}"
    print(f"  Test 1 passed  cost={cost}  order={order}")

    # Test 2: Single relic. Optimal cost = 5.
    graph_2 = {
        'S': [('R', 3)],
        'R': [('T', 2)],
        'T': []
    }
    cost, order = solve(graph_2, 'S', ['R'], 'T')
    assert cost == 5, f"Test 2 FAILED: expected 5, got {cost}"
    print(f"  Test 2 passed  cost={cost}  order={order}")

    # Test 3: No valid path to exit. Must return (inf, []).
    graph_3 = {
        'S': [('R', 1)],
        'R': [],
        'T': []
    }
    cost, order = solve(graph_3, 'S', ['R'], 'T')
    assert cost == float('inf'), f"Test 3 FAILED: expected inf, got {cost}"
    print(f"  Test 3 passed  cost={cost}")

    # Test 4: Relics reachable only through intermediate rooms.
    # Optimal cost = 6.
    graph_4 = {
        'S': [('X', 1)],
        'X': [('R1', 2), ('R2', 5)],
        'R1': [('Y', 1)],
        'Y': [('R2', 1)],
        'R2': [('T', 1)],
        'T': []
    }
    cost, order = solve(graph_4, 'S', ['R1', 'R2'], 'T')
    assert cost == 6, f"Test 4 FAILED: expected 6, got {cost}"
    print(f"  Test 4 passed  cost={cost}  order={order}")

    # Test 5: Explanation functions must return non-placeholder strings.
    for fn in [explain_problem, dijkstra_invariant_check, explain_search]:
        result = fn()
        assert isinstance(result, str) and result != "TODO" and len(result) > 20, \
            f"Test 5 FAILED: {fn.__name__} returned placeholder or empty string"
    print("  Test 5 passed  explanation functions are non-empty")

    print("\nAll provided tests passed.")


if __name__ == "__main__":
    _run_tests()
