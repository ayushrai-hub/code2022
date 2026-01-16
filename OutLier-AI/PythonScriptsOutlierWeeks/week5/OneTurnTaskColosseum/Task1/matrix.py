from __future__ import annotations

import typing
from typing import Any, Callable, Iterable, NamedTuple

import networkx as nx

from .vector import DIRECTIONS

type Grid[T] = list[list[T]]

class Matrix:
    graph: nx.Graph
    grid: Grid

    def __init__(self, graph: nx.Graph, grid: Grid) -> None:
        self.graph = graph
        self.grid = grid

    def __iter__(self) -> Iterable[Vertex]:
        return iter(self.graph.nodes)

    @property
    def num_vertices(
        self,
        filter: Callable[[Vertex], bool] = lambda node: True,
    ) -> int:
        return self.subgraph(filter).number_of_nodes()

    @property
    def num_links(
        self,
        filter: Callable[[Vertex], bool] = lambda node: True,
    ) -> int:
        return self.subgraph(filter).number_of_edges()

    @property
    def coordinate_dict(self) -> dict[Vertex, tuple[float, float]]:
        return {node: (node.x, node.y) for node in self.graph.nodes}

    @property
    def symbol_dict(self) -> dict[Vertex, str]:
        return {node: self.grid[node.y][node.x] for node in self.graph.nodes}

    @property
    def rows(self) -> int:
        return len(self.grid)

    @property
    def columns(self) -> int:
        return len(self.grid[0])

    @property
    def boundary(
        self,
        filter: Callable[[Vertex], bool] = lambda node: True,
    ) -> Matrix:
        return self.submatrix(
            filter=lambda node: filter(node) and (node.x in [0, self.columns - 1] or node.y in [0, self.rows - 1])
        )

    def vertices(
        self,
        filter: Callable[[Vertex], bool] = lambda node: True,
    ) -> typing.Sequence[Vertex]:
        return self.subgraph(filter).nodes

    def has_vertex(
        self,
        node: Vertex,
        filter: Callable[[Vertex], bool] = lambda node: True,
    ) -> bool:
        return self.subgraph(filter).has_node(node)

    def subgraph(self, filter: Callable[[Vertex], bool]) -> nx.Graph:
        return self.graph.subgraph([node for node in self.graph.nodes if filter(node)])

    def submatrix(self, filter: Callable[[Vertex], bool]) -> Matrix:
        return Matrix(self.subgraph(filter), self.grid)

    def shortest_route(
        self,
        start: Vertex,
        end: Vertex,
        filter: Callable[[Vertex], bool] = lambda node: True,
    ) -> Iterable[Vertex]:
        return nx.shortest_path(
            self.subgraph(filter),
            source=start,
            target=end,
        )

    def has_route(
        self,
        start: Vertex,
        end: Vertex,
        filter: Callable[[Vertex], bool] = lambda node: True,
    ) -> bool:
        return nx.has_path(
            self.subgraph(filter),
            source=start,
            target=end,
        )

    def neighbors(
        self,
        node: Vertex,
        filter: Callable[[Vertex], bool] = lambda node: True,
    ) -> Iterable[Vertex]:
        return self.subgraph(filter).neighbors(node)

    def graph_plot(
        self,
        node_color: str = "skyblue",
        filter: Callable[[Vertex], bool] = lambda node: True,
    ) -> None:
        nx.draw(
            self.subgraph(filter),
            pos=self.coordinate_dict,
            labels=self.symbol_dict,
            with_labels=True,
            node_color=node_color,
            node_size=500,
            font_size=10,
            font_weight="bold",
        )

    def plot_shortest_route(
        self,
        start: Vertex,
        end: Vertex,
        filter: Callable[[Vertex], bool] = lambda node: True,
        node_color: str = "orange",
        edge_color: str = "red",
    ) -> None:
        route = nx.shortest_path(
            self.subgraph(filter),
            source=start,
            target=end,
        )
        route_edges = list(zip(route, route[1:]))
        nx.draw_networkx_nodes(
            self.graph,
            self.coordinate_dict,
            nodelist=route,
            node_color=node_color,
        )
        nx.draw_networkx_edges(
            self.graph,
            self.coordinate_dict,
            edgelist=route_edges,
            edge_color=edge_color,
            width=2,
        )

    @staticmethod
    def from_grid(
        input_grid: Grid | list[typing.Sequence],
        directions: list[tuple[int, int]] | None = DIRECTIONS,
        node_attrs: Callable[[Vertex], dict[str, Any]] = lambda node: {},
        edge_attrs: Callable[[Vertex, Vertex], dict[str, Any]] = lambda a, b: {},
    ) -> Matrix:
        graph = nx.Graph()
        grid: list[list] = []
        for y, row in enumerate(input_grid):
            grid.append([])
            for x, cell in enumerate(row):
                graph.add_node(Vertex(x, y), char=cell, **node_attrs(Vertex(x, y)))
                grid[y].append(cell)
                if directions is not None:
                    for dx, dy in directions:
                        if 0 <= x + dx < len(input_grid[y]) and 0 <= y + dy < len(input_grid):
                            graph.add_edge(
                                Vertex(x, y),
                                Vertex(x + dx, y + dy),
                                **edge_attrs(Vertex(x, y), Vertex(x + dx, y + dy)),
                            )
        return Matrix(graph=graph, grid=grid)
