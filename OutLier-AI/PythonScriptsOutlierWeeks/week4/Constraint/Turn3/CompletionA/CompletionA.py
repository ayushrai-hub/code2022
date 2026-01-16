def solve_csp(input_dict):
    domains = {var: set(values) for var, values in input_dict['domains'].items()}
    constraints = input_dict['constraints']
    variables = list(domains.keys())

    neighbors = {var: set() for var in variables}
    for (var1, var2) in constraints:
        neighbors[var1].add(var2)
        neighbors[var2].add(var1)

    return backtrack({}, domains, constraints, neighbors)

def backtrack(assignment, domains, constraints, neighbors):
    if len(assignment) == len(domains):
        return assignment.copy()

    var = select_unassigned_var(assignment, domains, neighbors)

    for value in order_values(var, domains, assignment, constraints, neighbors):
        if is_consistent(var, value, assignment, constraints):
            assignment[var] = value
            removed = {}
            if forward_check(var, value, assignment, domains, constraints, neighbors, removed):
                result = backtrack(assignment, domains, constraints, neighbors)
                if result:
                    return result
            restore_domains(domains, removed)
            del assignment[var]

    return None

def is_consistent(var, value, assignment, constraints):
    for assigned_var, assigned_value in assignment.items():
        # Only check directly provided constraints
        constraint_fn = constraints.get((var, assigned_var))
        if constraint_fn and not constraint_fn(value, assigned_value):
            return False
        constraint_fn_rev = constraints.get((assigned_var, var))
        if constraint_fn_rev and not constraint_fn_rev(assigned_value, value):
            return False
    return True

def forward_check(var, value, assignment, domains, constraints, neighbors, removed):
    for neighbor in neighbors[var]:
        if neighbor not in assignment:
            neighbor_domain = domains[neighbor]
            to_remove = set()

            constraint_fn = constraints.get((var, neighbor))
            constraint_fn_rev = constraints.get((neighbor, var))

            for neighbor_val in neighbor_domain:
                constraint_satisfied = True
                if constraint_fn and not constraint_fn(value, neighbor_val):
                    constraint_satisfied = False
                elif constraint_fn_rev and not constraint_fn_rev(neighbor_val, value):
                    constraint_satisfied = False

                if not constraint_satisfied:
                    to_remove.add(neighbor_val)

            if to_remove:
                neighbor_domain.difference_update(to_remove)
                removed[neighbor] = to_remove

            if len(neighbor_domain) == 0:
                return False
    return True

def restore_domains(domains, removed):
    for var, values in removed.items():
        domains[var].update(values)

def select_unassigned_var(assignment, domains, neighbors):
    unassigned_vars = [var for var in domains if var not in assignment]
    # MRV heuristic
    min_remaining = min(len(domains[var]) for var in unassigned_vars)
    mrv_vars = [var for var in unassigned_vars if len(domains[var]) == min_remaining]
    if len(mrv_vars) == 1:
        return mrv_vars[0]
    # Degree heuristic as tie-breaker
    return max(mrv_vars, key=lambda var: sum(1 for neighbor in neighbors[var] if neighbor not in assignment))

def order_values(var, domains, assignment, constraints, neighbors):
    # LCV heuristic
    def conflicts(value):
        count = 0
        for neighbor in neighbors[var]:
            if neighbor not in assignment:
                constraint_fn = constraints.get((var, neighbor))
                constraint_fn_rev = constraints.get((neighbor, var))
                for neighbor_value in domains[neighbor]:
                    if constraint_fn and (not constraint_fn(value, neighbor_value)):
                        count += 1
                    elif constraint_fn_rev and (not constraint_fn_rev(neighbor_value, value)):
                        count += 1
        return count
    return sorted(domains[var], key=conflicts)
test_input = {
    'domains': {
        'a': [1, 2, 3, 4, 5],
        'b': [2, 3, 4, 5, 6],
        'c': [3, 4, 5, 6, 7],
        'd': [5, 7, 9, 11, 13]
    },
    'constraints': {
        ('a','b'): lambda a,b: a+b == 8 and a >= b,
        ('b','c'): lambda b,c: b <= c/2,
        ('c','d'): lambda c,d: (c+d) % 2 == 0
    }
}

result = solve_csp(test_input)
print(result) 
# Expected: {'a':5, 'b':3, 'c':7, 'd':5}


