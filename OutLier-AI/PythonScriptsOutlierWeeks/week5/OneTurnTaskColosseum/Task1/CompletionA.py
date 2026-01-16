import networkx as nx
from matplotlib import pyplot as plt
def create_path_graph(route: str) -> nx.DiGraph:
    # Direction mappings
    directions = {
        'W': (0, -1),  # North (up)
        'D': (1, 0),   # East (right)
        'S': (0, 1),   # South (down)
        'A': (-1, 0)   # West (left)
    }
    
    graph = nx.DiGraph()
    current_pos = (0, 0)
    graph.add_node(current_pos)
    
    for move in route:
        dx, dy = directions[move]
        next_pos = (current_pos[0] + dx, current_pos[1] + dy)
        graph.add_node(next_pos)
        graph.add_edge(current_pos, next_pos)
        current_pos = next_pos
    
    return graph

def find_hamiltonian_path(matrix: Matrix) -> list[Vertex] | None:
    walkable_filter = lambda node: matrix.symbol_dict[node] != 'X'
    walkable_nodes = [node for node in matrix.vertices() if walkable_filter(node)]
    
    def dfs(current: Vertex, path: list[Vertex], visited: set[Vertex]) -> bool:
        if len(path) == len(walkable_nodes):
            return True
        
        # Try neighbors in a specific order
        neighbors = list(matrix.neighbors(current, filter=walkable_filter))
        neighbors.sort(key=lambda n: (n.x, n.y))
        
        for neighbor in neighbors:
            if neighbor not in visited:
                path.append(neighbor)
                visited.add(neighbor)
                if dfs(neighbor, path, visited):
                    return True
                path.pop()
                visited.remove(neighbor)
        
        return False
    
    # Try starting from nodes with fewer walkable neighbors (corners/edges first)
    node_degrees = [(node, len(list(matrix.neighbors(node, filter=walkable_filter)))) 
                   for node in walkable_nodes]
    node_degrees.sort(key=lambda x: x[1])  # Sort by degree (ascending)
    
    for start_node, _ in node_degrees:
        path = [start_node]
        visited = {start_node}
        if dfs(start_node, path, visited):
            return path
    
    return None

def path_to_directions(path: list[Vertex]) -> str:
    directions = []
    direction_map = {
        (0, -1): 'W',  # North
        (1, 0): 'D',   # East
        (0, 1): 'S',   # South
        (-1, 0): 'A'   # West
    }
    
    for i in range(len(path) - 1):
        current = path[i]
        next_node = path[i + 1]
        dx = next_node.x - current.x
        dy = next_node.y - current.y
        directions.append(direction_map[(dx, dy)])
    
    return ''.join(directions)

def check_level4(raw_input: str, plot: bool) -> str:
    lines = raw_input.strip().splitlines()
    n: int = int(lines.pop(0))

    output: list[str] = []

    graph_i = 0
    while lines:
        graph_i += 1

        lawn_width, lawn_height = tuple(map(int, lines.pop(0).split()))
        lawn: list[list[str]] = [list(row) for row in lines[:lawn_height]]
        lines = lines[lawn_height:]

        matrix = Matrix.from_grid(lawn, directions=DIRECTIONS)
        
        # Find Hamiltonian path
        path = find_hamiltonian_path(matrix)
        
        if path is None:
            output.append("NO SOLUTION")
        else:
            route = path_to_directions(path)
            output.append(route)

        if plot:
            plt.gca().invert_yaxis()
            plt.title(f"Lawn {graph_i}")
            walkable = matrix.submatrix(filter=lambda node: matrix.symbol_dict[node] != "X")
            walkable.graph_plot(node_color="green")
            if path:
                # Draw the path
                path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
                nx.draw_networkx_edges(
                    matrix.graph,
                    pos=matrix.coordinate_dict,
                    edgelist=path_edges,
                    edge_color="red",
                    width=3
                )
            plt.show()

    return "\n".join(output)

if __name__ == "__main__":
    solver = Solver(game_name="classic")
    solver.solve(4, solve_fn=check_level4, assert_fn=assert_fn, test=False, plot_all=False)
