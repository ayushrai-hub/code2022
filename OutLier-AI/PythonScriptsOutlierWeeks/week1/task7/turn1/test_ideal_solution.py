import unittest
from ideal import LR1, LR2, update_x_based_on_flow, solve_Lagrange_Relaxtion, Lagrangian_Relaxation
import gurobipy as gb

class TestColoredSteinerTreeSolver(unittest.TestCase):

    def setUp(self):
        """Setup common test data used across multiple test cases"""
        self.vertices = [1, 2, 3, 4]
        self.edges = [(1, 2), (2, 3), (3, 4), (4, 1)]
        self.weights = {(1, 2): 1, (2, 3): 1, (3, 4): 1, (4, 1): 1}
        self.costs = {(1, 2): 1, (2, 3): 1, (3, 4): 1, (4, 1): 1}
        self.terminals = [1, 3]

    def test_LR1_empty_input(self):
        """Test LR1 function with empty input to verify error handling"""
        result = LR1([], [], {}, {}, [1], None)  
        self.assertIsInstance(result, dict)

    def test_LR1_invalid_input_types(self):
        """Test LR1 function with invalid input types to verify type checking"""
        result = LR1([1], [(1,1)], {(1,1): 1}, {(1,1): 1}, [1], None)
        self.assertIsInstance(result, dict)

    def test_LR1_disconnected_graph(self):
        """Test LR1 function with a disconnected graph to verify error handling"""
        vertices = [1, 2, 3, 4]
        edges = [(1, 2), (3, 4)]  # Disconnected edges
        weights = {(1, 2): 1, (3, 4): 1}
        costs = {(1, 2): 1, (3, 4): 1}
        terminals = [1, 3]
        result = LR1(vertices, edges, weights, costs, terminals, None)
        self.assertIsNotNone(result)  # LR1 should still return a flow dictionary

    def test_LR1_valid_input(self):
        """Test LR1 function with valid input to verify correct functionality"""
        result = LR1(self.vertices, self.edges, self.weights, self.costs, self.terminals, None)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)

    def test_LR2_empty_input(self):
        """Test LR2 function with empty input to verify error handling"""
        result = LR2([], [], {}, {}, [1], None, {}, {})
        self.assertIsInstance(result, dict)

    def test_LR2_valid_input(self):
        """Test LR2 function with valid input to verify correct functionality"""
        mult = {(1, 2, 3): 1}
        weight_map = {1: [(1, 2)]}
        result = LR2(self.vertices, self.edges, self.weights, self.costs, 
                    self.terminals, None, mult, weight_map)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)

    def test_update_x_based_on_flow_empty_input(self):
        """Test update_x_based_on_flow function with empty input"""
        flow_details = {}
        arcs = []
        x = {}
        update_x_based_on_flow(flow_details, arcs, x)
        self.assertEqual(x, {})

    def test_update_x_based_on_flow_valid_input(self):
        """Test update_x_based_on_flow function with valid input"""
        flow_details = {1: {(1, 2): 1}}
        arcs = [(1, 2)]
        x = {(1, 2): 0}
        update_x_based_on_flow(flow_details, arcs, x)
        self.assertEqual(x[(1, 2)], 1)

    def test_Lagrangian_Relaxation_valid_input(self):
        """Test Lagrangian_Relaxation function with valid input"""
        vertices = [1, 2]
        edges = [(1, 2)]
        weights = {(1, 2): 1}
        costs = {(1, 2): 1}
        terminals = [1, 2]
        result = Lagrangian_Relaxation(vertices, edges, weights, costs, terminals, None)
        self.assertIsInstance(result, float)
        
    def test_Lagrangian_Relaxation_with_single_terminal(self):
        """Test Lagrangian_Relaxation function with a single terminal node"""
        terminals = [1]
        result = Lagrangian_Relaxation(self.vertices, self.edges, 
                                     self.weights, self.costs, terminals, None)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, float)

if __name__ == '__main__':
    unittest.main(verbosity=2)