from __future__ import annotations

import typing
from typing import Iterable, NamedTuple

import networkx as nx

from .matrix import Matrix, Vertex, DIRECTIONS          # same helpers as in level‑3


# ------------------------------------------------------------
# Helper that turns a list[Vertex] into "WASD" instructions
# ------------------------------------------------------------
def encode_route(route: list[Vertex]) -> str:
    DIR2SYM = {(0, -1): "W", (1, 0): "D", (0, 1): "S", (-1, 0): "A"}
    symbols: list[str] = []
    for a, b in zip(route, route[1:]):
        symbols.append(DIR2SYM[(b.x - a.x, b.y - a.y)])
    return "".join(symbols)


# ------------------------------------------------------------
# Build a Hamiltonian path for one lawn
# ------------------------------------------------------------
def build_snake_path(grid: list[list[str]]) -> str:
    h, w = len(grid), len(grid[0])
    # find the tree
    tree: Vertex | None = None
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c == "X":
                tree = Vertex(x, y)
                break
        if tree:
            break
    assert tree is not None, "every lawn contains exactly one tree"

    # produce snake order while skipping the tree,
    # insert a 4‑step detour around the tree the first time we meet it
    path: list[Vertex] = []

    def append(v: Vertex):
        if grid[v.y][v.x] != "X":
            path.append(v)

    for y in range(h):
        rng = range(w) if y % 2 == 0 else range(w - 1, -1, -1)
        for x in rng:
            v = Vertex(x, y)
            if v == tree:
                # Detour around the tree (4 cells, clockwise)
                #   left → down → right → up
                # Works because the tree is not on the border.
                if y % 2 == 0:          # we were going left→right
                    append(Vertex(x - 1, y))   # step left (already visited)
                    append(Vertex(x - 1, y + 1))
                    append(Vertex(x,     y + 1))
                else:                   # we were going right→left
                    append(Vertex(x + 1, y))   # step right (already visited)
                    append(Vertex(x + 1, y + 1))
                    append(Vertex(x,     y + 1))
                # continue, but skip the tree itself
                continue
            append(v)

    # finally encode to "WASD"
    return encode_route(path)


# ------------------------------------------------------------
# Main function requested by the judge
# ------------------------------------------------------------
def solve_level4(raw_input: str, plot: bool) -> str:
    """
    input  =
        N                       number of lawns
        w h                     width height of lawn‑1
        <h lines with . and X>  lawn‑1
        w h
        ...
    output =
        N lines, one route per lawn encoded with WASD
    """
    it = iter(raw_input.strip().splitlines())
    n = int(next(it))

    answers: list[str] = []
    for _ in range(n):
        w, h = map(int, next(it).split())
        lawn = [list(next(it)) for _ in range(h)]

        route = build_snake_path(lawn)
        answers.append(route)

        # optional visual check
        if plot:
            matrix = Matrix.from_grid(lawn)
            route_graph = nx.DiGraph()
            cur = Vertex(0, 0)
            route_graph.add_node(cur)
            for ch in route:
                dx, dy = {"W": (0, -1), "A": (-1, 0), "S": (0, 1), "D": (1, 0)}[ch]
                nxt = Vertex(cur.x + dx, cur.y + dy)
                route_graph.add_edge(cur, nxt)
                cur = nxt
            walkable = matrix.submatrix(lambda v: matrix.symbol_dict[v] != "X")
            walkable.graph_plot(node_color="lightgreen")
            nx.draw(route_graph, pos={v: (v.x, v.y) for v in route_graph.nodes},
                    node_color="blue", with_labels=True)
            import matplotlib.pyplot as plt
            plt.gca().invert_yaxis()
            plt.show()

    return "\n".join(answers)


# -----------------------------------------------------------------
# Hook for the framework you used in level‑3
# -----------------------------------------------------------------
if __name__ == "__main__":
    from solver import Solver, assert_fn  # the same helper from level‑3
    Solver(game_name="classic").solve(
        4,                # level‑4
        solve_fn=solve_level4,
        assert_fn=assert_fn,
        test=False,
        plot_all=False,
    )
