def find_hamiltonian_path(graph, start_node=None):
    """Find a Hamiltonian path (visits all nodes exactly once)"""
    if not start_node:
        start_node = next(iter(graph.nodes))
    
    def dfs_hamiltonian(current_path, visited):
        if len(current_path) == len(graph.nodes):
            return current_path
        
        current_node = current_path[-1]
        for neighbor in graph.neighbors(current_node):
            if neighbor not in visited:
                visited.add(neighbor)
                result = dfs_hamiltonian(current_path + [neighbor], visited)
                if result:
                    return result
                visited.remove(neighbor)
        return None
    
    return dfs_hamiltonian([start_node], {start_node})
def l4(raw_input: str, plot: bool) -> str:
    lines = raw_input.strip().splitlines()
    n: int = int(lines.pop(0))
    output: list[str] = []

    while lines:
        lawn_width, lawn_height = tuple(map(int, lines.pop(0).split()))
        lawn: list[list[str]] = [list(row) for row in lines[:lawn_height]]
        lines = lines[lawn_height:]

        lattice = Lattice.from_grid(lawn, directions=DIRECTIONS)
        walkable = lattice.subgraph(only=lambda node: lattice.label_dict[node] != "X")
        
        # Find any starting point
        start_node = next(iter(walkable.nodes))
        
        # Find Hamiltonian path (visits all nodes exactly once)
        hamiltonian_path = find_hamiltonian_path(walkable, start_node)
        
        if hamiltonian_path:
            path_string = translate_path_to_directions(hamiltonian_path)
            output.append(path_string)
        else:
            output.append("NO_SOLUTION")  # No valid path exists

    return "\n".join(output)
