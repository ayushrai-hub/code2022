def solve_task(data_input):
    # Convert domains to sets for O(1) removal/addition
    dms = {one: set(options) for one, options in data_input['domains'].items()}
    cts = data_input['constraints']
    var_list = list(dms.keys())

    # Build bidirectional adjacency structure once
    adjacency = {single: set() for single in var_list}
    for x1, x2 in cts:
        adjacency[x1].add(x2)
        adjacency[x2].add(x1)  # Ensure bidirectionality

    # Backtrack with optimized domains
    my_assignment = {}
    outcome = backtrack_proc(my_assignment, dms, cts, adjacency)
    return outcome if outcome else None

def backtrack_proc(my_assignment, dms, cts, adjacency):
    if len(my_assignment) == len(dms):
        return my_assignment.copy()

    chosen = pick_unassigned(my_assignment, dms, adjacency)
    for val in arrange_values(chosen, dms, my_assignment, cts, adjacency):
        if consistent(chosen, val, my_assignment, cts):
            my_assignment[chosen] = val
            removed_items = {}
            if forward_look(chosen, val, my_assignment, dms, cts, adjacency, removed_items):
                outcome = backtrack_proc(my_assignment, dms, cts, adjacency)
                if outcome:
                    return outcome
            revert(dms, removed_items)
            del my_assignment[chosen]
    return None

def revert(dms, removed_items):
    for one, items in removed_items.items():
        dms[one].update(items)  # O(1) per item with sets

def pick_unassigned(my_assignment, dms, adjacency):
    # Single pass for MRV and degree
    unassigned = [(v, len(dms[v]), sum(1 for n in adjacency[v] if n not in my_assignment))
                  for v in dms if v not in my_assignment]
    # Sort by MRV (ascending), then degree (descending) if tied
    return min(unassigned, key=lambda x: (x[1], -x[2]))[0]

def arrange_values(chosen, dms, my_assignment, cts, adjacency):
    # LCV: Precompute conflict counts
    counts = {}
    for val in dms[chosen]:
        accum = 0
        for neigh in adjacency[chosen]:
            if neigh not in my_assignment:
                accum += sum(1 for alt in dms[neigh]
                           if not constraint_ok(chosen, val, neigh, alt, cts))
        counts[val] = accum
    return sorted(dms[chosen], key=lambda v: counts[v])

def consistent(chosen, val, my_assignment, cts):
    for assigned, assigned_val in my_assignment.items():
        if (chosen, assigned) in cts and not cts[(chosen, assigned)](val, assigned_val):
            return False
        if (assigned, chosen) in cts and not cts[(assigned, chosen)](assigned_val, val):
            return False
    return True

def constraint_ok(a1, v1, a2, v2, cts):
    return (cts.get((a1, a2), lambda x, y: True)(v1, v2) and
            cts.get((a2, a1), lambda x, y: True)(v2, v1))

def forward_look(chosen, val, my_assignment, dms, cts, adjacency, removed_items):
    for friend in adjacency[chosen]:
        if friend not in my_assignment:
            to_remove = {poss for poss in dms[friend]
                        if not constraint_ok(chosen, val, friend, poss, cts)}
            if to_remove:
                dms[friend].difference_update(to_remove)  # Bulk removal
                removed_items[friend] = to_remove
                if not dms[friend]:
                    return False
    return True
example_input = {
    'domains': {
        'q': [1, 2, 3, 4],
        'r': [2, 3, 5, 7],
        's': [4, 6, 8],
    },
    'constraints': {
        ('q', 'r'): lambda q, r: q + r == 5,
        ('r', 's'): lambda r, s: (r + s) % 2 == 0
    }
}

res = solve_task(example_input)
print(res)
