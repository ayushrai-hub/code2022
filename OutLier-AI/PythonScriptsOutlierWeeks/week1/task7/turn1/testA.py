import unittest
from ideal import LR1, LR2, update_x_based_on_flow, solve_Lagrange_Relaxtion, Lagrangian_Relaxation
import gurobipy as gb
import random

class TestColoredSteinerTreeSolver(unittest.TestCase):

    def test_LR1_empty_vertices(self):
        # Test LR1 function with empty vertices
        vertices = []
        edges = [(1, 2), (2, 3), (3, 4), (4, 1)]
        weights = {(1, 2): 'red', (2, 3): 'blue', (3, 4): 'green', (4, 1): 'yellow'}
        costs = {(1, 2): 1, (2, 3): 1, (3, 4): 1, (4, 1): 1}
        terminals = [1, 3]
        source = None
        with self.assertRaises(ValueError):
            LR1(vertices, edges, weights, costs, terminals, source)

    def test_LR1_empty_edges(self):
        # Test LR1 function with empty edges
        vertices = [1, 2, 3, 4]
        edges = []
        weights = {(1, 2): 'red', (2, 3): 'blue', (3, 4): 'green', (4, 1): 'yellow'}
        costs = {(1, 2): 1, (2, 3): 1, (3, 4): 1, (4, 1): 1}
        terminals = [1, 3]
        source = None
        with self.assertRaises(ValueError):
            LR1(vertices, edges, weights, costs, terminals, source)

    def test_LR1_empty_terminals(self):
        # Test LR1 function with empty terminals
        vertices = [1, 2, 3, 4]
        edges = [(1, 2), (2, 3), (3, 4), (4, 1)]
        weights = {(1, 2): 'red', (2, 3): 'blue', (3, 4): 'green', (4, 1): 'yellow'}
        costs = {(1, 2): 1, (2, 3): 1, (3, 4): 1, (4, 1): 1}
        terminals = []
        source = None
        with self.assertRaises(ValueError):
            LR1(vertices, edges, weights, costs, terminals, source)

    def test_LR1_valid_input(self):
        # Test LR1 function with valid input
        vertices = [1, 2, 3, 4]
        edges = [(1, 2), (2, 3), (3, 4), (4, 1)]
        weights = {(1, 2): 'red', (2, 3): 'blue', (3, 4): 'green', (4, 1): 'yellow'}
        costs = {(1, 2): 1, (2, 3): 1, (3, 4): 1, (4, 1): 1}
        terminals = [1, 3]
        source = None
        result = LR1(vertices, edges, weights, costs, terminals, source)
        self.assertIsNotNone(result)

    def test_LR2_empty_vertices(self):
        # Test LR2 function with empty vertices
        vertices = []
        edges = [(1, 2), (2, 3), (3, 4), (4, 1)]
        weights = {(1, 2): 'red', (2, 3): 'blue', (3, 4): 'green', (4, 1): 'yellow'}
        costs = {(1, 2): 1, (2, 3): 1, (3, 4): 1, (4, 1): 1}
        terminals = [1, 3]
        source = None
        mult = {}
        weight_map = {}
        with self.assertRaises(ValueError):
            LR2(vertices, edges, weights, costs, terminals, source, mult, weight_map)

    def test_LR2_empty_edges(self):
        # Test LR2 function with empty edges
        vertices = [1, 2, 3, 4]
        edges = []
        weights = {(1, 2): 'red', (2, 3): 'blue', (3, 4): 'green', (4, 1): 'yellow'}
        costs = {(1, 2): 1, (2, 3): 1, (3, 4): 1, (4, 1): 1}
        terminals = [1, 3]
        source = None
        mult = {}
        weight_map = {}
        with self.assertRaises(ValueError):
            LR2(vertices, edges, weights, costs, terminals, source, mult, weight_map)

    def test_LR2_empty_terminals(self):
        # Test LR2 function with empty terminals
        vertices = [1, 2, 3, 4]
        edges = [(1, 2), (2, 3), (3, 4), (4, 1)]
        weights = {(1, 2): 'red', (2, 3): 'blue', (3, 4): 'green', (4, 1): 'yellow'}
        costs = {(1, 2): 1, (2, 3): 1, (3, 4): 1, (4, 1): 1}
        terminals = []
        source = None
        mult = {}
        weight_map = {}
        with self.assertRaises(ValueError):
            LR2(vertices, edges, weights, costs, terminals, source, mult, weight_map)

    def test_LR2_valid_input(self):
        # Test LR2 function with valid input
        vertices = [1, 2, 3, 4]
        edges = [(1, 2), (2, 3), (3, 4), (4, 1)]
        weights = {(1, 2): 'red', (2, 3): 'blue', (3, 4): 'green', (4, 1): 'yellow'}
        costs = {(1, 2): 1, (2, 3): 1, (3, 4): 1, (4, 1): 1}
        terminals = [1, 3]
        source = None
        mult = {}
        weight_map = {}
        result = LR2(vertices, edges, weights, costs, terminals, source, mult, weight_map)
        self.assertIsNotNone(result)

    def test_update_x_based_on_flow_empty_flow_details(self):
        # Test update_x_based_on_flow function with empty flow_details
        flow_details = {}
        arcs = [(1, 2), (2, 3), (3, 4), (4, 1)]
        x = {}
        with self.assertRaises(ValueError):
            update_x_based_on_flow(flow_details, arcs, x)

    def test_update_x_based_on_flow_empty_arcs(self):
        # Test update_x_based_on_flow function with empty arcs
        flow_details = {1: {(1, 2): 1, (2, 3): 1}, 3: {(3, 4): 1, (4, 1): 1}}
        arcs = []
        x = {}
        with self.assertRaises(ValueError):
            update_x_based_on_flow(flow_details, arcs, x)

    def test_update_x_based_on_flow_empty_x(self):
        # Test update_x_based_on_flow function with empty x
        flow_details = {1: {(1, 2): 1, (2, 3): 1}, 3: {(3, 4): 1, (4, 1): 1}}
        arcs = [(1, 2), (2, 3), (3, 4), (4, 1)]
        x = {}
        with self.assertRaises(ValueError):
            update_x_based_on_flow(flow_details, arcs, x)

    def test_update_x_based_on_flow_valid_input(self):
        # Test update_x_based_on_flow function with valid input
        flow_details = {1: {(1, 2): 1, (2, 3): 1}, 3: {(3, 4): 1, (4, 1): 1}}
        arcs = [(1, 2), (2, 3), (3, 4), (4, 1)]
        x = {(1, 2): 0, (2, 3): 0, (3, 4): 0, (4, 1): 0}
        result = update_x_based_on_flow(flow_details, arcs, x)
        self.assertIsNotNone(result)

    def test_solve_Lagrange_Relaxtion_empty_nodes(self):
        # Test solve_Lagrange_Relaxtion function with empty nodes
        nodes = []
        edge_bar = [(1, 2), (2, 3), (3, 4), (4, 1)]
        weight_bar = {(1, 2): 'red', (2, 3): 'blue', (3, 4): 'green', (4, 1): 'yellow'}
        arcs = {(1, 2): 1, (2, 3): 1, (3, 4): 1, (4, 1): 1}
        terminals = [1, 3]
        source = None
        with self.assertRaises(ValueError):
            solve_Lagrange_Relaxtion(nodes, edge_bar, weight_bar, arcs, terminals, source)

    def test_solve_Lagrange_Relaxtion_empty_edge_bar(self):
        # Test solve_Lagrange_Relaxtion function with empty edge_bar
        nodes = [1, 2, 3, 4]
        edge_bar = []
        weight_bar = {(1, 2): 'red', (2, 3): 'blue', (3, 4): 'green', (4, 1): 'yellow'}
        arcs = {(1, 2): 1, (2, 3): 1, (3, 4): 1, (4, 1): 1}
        terminals = [1, 3]
        source = None
        with self.assertRaises(ValueError):
            solve_Lagrange_Relaxtion(nodes, edge_bar, weight_bar, arcs, terminals, source)

    def test_solve_Lagrange_Relaxtion_empty_terminals(self):
        # Test solve_Lagrange_Relaxtion function with empty terminals
        nodes = [1, 2, 3, 4]
        edge_bar = [(1, 2), (2, 3), (3, 4), (4, 1)]
        weight_bar = {(1, 2): 'red', (2, 3): 'blue', (3, 4): 'green', (4, 1): 'yellow'}
        arcs = {(1, 2): 1, (2, 3): 1, (3, 4): 1, (4, 1): 1}
        terminals = []
        source = None
        with self.assertRaises(ValueError):
            solve_Lagrange_Relaxtion(nodes, edge_bar, weight_bar, arcs, terminals, source)

    def test_solve_Lagrange_Relaxtion_valid_input(self):
        # Test solve_Lagrange_Relaxtion function with valid input
        nodes = [1, 2, 3, 4]
        edge_bar = [(1, 2), (2, 3), (3, 4), (4, 1)]
        weight_bar = {(1, 2): 'red', (2, 3): 'blue', (3, 4): 'green', (4, 1): 'yellow'}
        arcs = {(1, 2): 1, (2, 3): 1, (3, 4): 1, (4, 1): 1}
        terminals = [1, 3]
        source = None
        result = solve_Lagrange_Relaxtion(nodes, edge_bar, weight_bar, arcs, terminals, source)
        self.assertIsNotNone(result)

    def test_Lagrangian_Relaxation_empty_vertices(self):
        # Test Lagrangian_Relaxation function with empty vertices
        vertices = []
        edges = [(1, 2), (2, 3), (3, 4), (4, 1)]
        weights = {(1, 2): 'red', (2, 3): 'blue', (3, 4): 'green', (4, 1): 'yellow'}
        costs = {(1, 2): 1, (2, 3): 1, (3, 4): 1, (4, 1): 1}
        terminals = [1, 3]
        source = None
        with self.assertRaises(ValueError):
            Lagrangian_Relaxation(vertices, edges, weights, costs, terminals, source)

    def test_Lagrangian_Relaxation_empty_edges(self):
        # Test Lagrangian_Relaxation function with empty edges
        vertices = [1, 2, 3, 4]
        edges = []
        weights = {(1, 2): 'red', (2, 3): 'blue', (3, 4): 'green', (4, 1): 'yellow'}
        costs = {(1, 2): 1, (2, 3): 1, (3, 4): 1, (4, 1): 1}
        terminals = [1, 3]
        source = None
        with self.assertRaises(ValueError):
            Lagrangian_Relaxation(vertices, edges, weights, costs, terminals, source)

    def test_Lagrangian_Relaxation_empty_terminals(self):
        # Test Lagrangian_Relaxation function with empty terminals
        vertices = [1, 2, 3, 4]
        edges = [(1, 2), (2, 3), (3, 4), (4, 1)]
        weights = {(1, 2): 'red', (2, 3): 'blue', (3, 4): 'green', (4, 1): 'yellow'}
        costs = {(1, 2): 1, (2, 3): 1, (3, 4): 1, (4, 1): 1}
        terminals = []
        source = None
        with self.assertRaises(ValueError):
            Lagrangian_Relaxation(vertices, edges, weights, costs, terminals, source)

    def test_Lagrangian_Relaxation_valid_input(self):
        # Test Lagrangian_Relaxation function with valid input
        vertices = [1, 2, 3, 4]
        edges = [(1, 2), (2, 3), (3, 4), (4, 1)]
        weights = {(1, 2): 'red', (2, 3): 'blue', (3, 4): 'green', (4, 1): 'yellow'}
        costs = {(1, 2): 1, (2, 3): 1, (3, 4): 1, (4, 1): 1}
        terminals = [1, 3]
        source = None
        result = Lagrangian_Relaxation(vertices, edges, weights, costs, terminals, source)
        self.assertIsNotNone(result)

if __name__ == '__main__':
    unittest.main()