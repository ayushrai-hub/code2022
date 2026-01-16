def solve_csp(input):
    domains = {var: list(vals) for var, vals in input['domains'].items()}
    constraints = input['constraints']
    variables = list(domains.keys())
    
    # Build neighbors
    neighbors = {var: set() for var in variables}
    for (var1, var2) in constraints:
        neighbors[var1].add(var2)
        neighbors[var2].add(var1)

    def is_consistent(var, val, assignment):
        for (var1, var2), constraint in constraints.items():
            if var1 == var and var2 in assignment:
                if not constraint(val, assignment[var2]):
                    return False
            elif var2 == var and var1 in assignment:
                if not constraint(assignment[var1], val):
                    return False
        return True

    def forward_check(var, val, domains, assignment, removed_vals):
        # Check constraints on neighbors of var
        for neigh in neighbors[var]:
            if neigh not in assignment:
                to_remove = []
                for neigh_val in domains[neigh]:
                    if (var, neigh) in constraints and not constraints[(var, neigh)](val, neigh_val):
                        to_remove.append(neigh_val)
                    elif (neigh, var) in constraints and not constraints[(neigh, var)](neigh_val, val):
                        to_remove.append(neigh_val)
                if to_remove:
                    removed_vals[neigh] = to_remove
                    for rv in to_remove:
                        domains[neigh].remove(rv)
                    if not domains[neigh]:
                        return False
        return True

    def restore(domains, removed_vals):
        for var in removed_vals:
            domains[var].extend(removed_vals[var])

    def select_unassigned_var(assignment, domains):
        # MRV heuristic
        unassigned = [v for v in variables if v not in assignment]
        mrv_var = min(unassigned, key=lambda v: len(domains[v]))
        return mrv_var

    def backtrack(assignment):
        if len(assignment) == len(variables):
            return assignment.copy()
        
        curr_var = select_unassigned_var(assignment, domains)
        for val in domains[curr_var]:
            if is_consistent(curr_var, val, assignment):
                assignment[curr_var] = val
                removed_vals = {}
                if forward_check(curr_var, val, domains, assignment, removed_vals):
                    result = backtrack(assignment)
                    if result:
                        return result
                restore(domains, removed_vals)
                del assignment[curr_var]
        return None

    return backtrack({})
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

res = solve_csp(example_input)
print(res)
