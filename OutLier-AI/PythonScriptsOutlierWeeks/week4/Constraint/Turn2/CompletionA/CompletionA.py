def solve_csp(input_dict):
    domains = {var: set(vals) for var, vals in input_dict['domains'].items()}
    constraints = input_dict['constraints']
    variables = list(domains.keys())

    # Build adjacency list
    neighbors = {var: [] for var in variables}
    for (x1, x2) in constraints:
        neighbors[x1].append(x2)
        neighbors[x2].append(x1)

    def is_consistent(var, val, assignment):
        for (v1, v2), constraint in constraints.items():
            if v1 == var and v2 in assignment:
                if not constraint(val, assignment[v2]):
                    return False
            elif v2 == var and v1 in assignment:
                if not constraint(assignment[v1], val):
                    return False
        return True

    def select_variable(assignment):
        # MRV heuristic with Degree heuristic for tie-breaks
        unassigned = [v for v in variables if v not in assignment]
        return min(
            unassigned,
            key=lambda var: (len(domains[var]), -len(neighbors[var]))
        )

    def order_values(var, assignment):
        # LCV heuristic
        if not neighbors[var]:
            return domains[var]

        def count_conflicts(value):
            conflicts = 0
            for neighbor in neighbors[var]:
                if neighbor not in assignment:
                    for n_val in domains[neighbor]:
                        constraint = constraints.get((var, neighbor))
                        if constraint and not constraint(value, n_val):
                            conflicts += 1
                        constraint_reverse = constraints.get((neighbor, var))
                        if constraint_reverse and not constraint_reverse(n_val, value):
                            conflicts += 1
            return conflicts
        
        return sorted(domains[var], key=count_conflicts)

    def backtrack(assignment):
        if len(assignment) == len(variables):
            return assignment.copy()

        var = select_variable(assignment)
        for value in order_values(var, assignment):
            if is_consistent(var, value, assignment):
                assignment[var] = value

                # Save the removed domains for forward checking
                removed_domains = {}
                if forward_check(var, value, assignment, removed_domains):
                    result = backtrack(assignment)
                    if result:
                        return result
                
                restore_domains(removed_domains)
                del assignment[var]
        return None

    def forward_check(var, value, assignment, removed_domains):
        for neighbor in neighbors[var]:
            if neighbor not in assignment:
                for n_val in domains[neighbor][:]:
                    constraint = constraints.get((var, neighbor))
                    if constraint and not constraint(value, n_val):
                        domains[neighbor].remove(n_val)
                        removed_domains.setdefault(neighbor, []).append(n_val)
                    constraint_reverse = constraints.get((neighbor, var))
                    if constraint_reverse and not constraint_reverse(n_val, value):
                        domains[neighbor].remove(n_val)
                        removed_domains.setdefault(neighbor, []).append(n_val)
                if not domains[neighbor]:
                    return False
        return True

    def restore_domains(removed_domains):
        for var, values in removed_domains.items():
            domains[var].update(values)

    return backtrack({})

# Example input for testing
example_input = {
    'domains': {
        'a': [1, 2, 3],
        'b': [2, 3, 4],
        'c': [3, 4, 5],
    },
    'constraints': {
        ('a', 'b'): lambda x, y: x + y == 5,
        ('b', 'c'): lambda x, y: x < y,
    }
}

print(solve_csp(example_input))
