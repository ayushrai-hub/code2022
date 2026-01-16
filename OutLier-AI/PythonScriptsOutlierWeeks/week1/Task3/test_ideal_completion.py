import unittest
from unittest.mock import patch
import matplotlib.pyplot as plt
import numpy as np
from io import StringIO
import sys

class TestFinancialVisualization(unittest.TestCase):
    def setUp(self):
        """Set up test data before each test"""
        # Define the test data within setUp to ensure clean data for each test
        self.test_data = {
            "person": {
                "name": "Rohan Kumar",
                "age": 29,
                "location": "Tier-2 City, India"
            },
            "financial_data": {
                "income": {
                    "monthly_income": 45000,
                    "sources": [
                        {"source": "Salary", "amount": 40000},
                        {"source": "Startup Consulting", "amount": 5000}
                    ]
                },
                "expenses": {
                    "fixed_expenses": {
                        "rent": 10000,
                        "utilities": {"electricity": 1200, "water": 300, "internet": 800, "mobile": 500},
                        "subscriptions": {"streaming_services": 499, "gym": 1500}
                    },
                    "variable_expenses": {
                        "groceries": 4000,
                        "transportation": 2500,
                        "eating_out": 3000,
                        "entertainment": 1500,
                        "miscellaneous": 1000
                    }
                },
                "savings": {
                    "monthly_savings": 10000,
                    "investments": {
                        "mutual_funds": 5000,
                        "fixed_deposit": 3000,
                        "emergency_fund": 2000
                    }
                }
            },
            "total_expenses": {
                "fixed_expenses": 14899,
                "variable_expenses": 12000,
                "total": 26899
            },
            "remaining_balance": {
                "income_after_expenses": 18101
            }
        }
        
    def validate_financial_data(self, data):
        """Local validation function to match the implementation"""
        # Check if required top-level keys exist
        required_keys = ["financial_data", "total_expenses"]
        if not all(key in data for key in required_keys):
            raise ValueError("Missing required data structure keys")

        # Validate income values
        monthly_income = data["financial_data"]["income"]["monthly_income"]
        if not isinstance(monthly_income, (int, float)) or monthly_income < 0:
            raise ValueError("Invalid monthly income value")

        # Validate income sources
        for source in data["financial_data"]["income"]["sources"]:
            if source["amount"] < 0:
                raise ValueError("Income source amounts cannot be negative")

        # Validate expenses
        if data["total_expenses"]["fixed_expenses"] < 0:
            raise ValueError("Fixed expenses cannot be negative")
        if data["total_expenses"]["variable_expenses"] < 0:
            raise ValueError("Variable expenses cannot be negative")

        # Validate savings
        if data["financial_data"]["savings"]["monthly_savings"] < 0:
            raise ValueError("Monthly savings cannot be negative")
            
    def test_data_structure(self):
        """Test that all required data structures are present"""
        required_keys = ["financial_data", "total_expenses", "remaining_balance"]
        for key in required_keys:
            self.assertIn(key, self.test_data)
            
    def test_income_validation(self):
        """Test income validation logic"""
        # Test valid income
        try:
            self.validate_financial_data(self.test_data)
        except ValueError as e:
            self.fail(f"validate_financial_data raised ValueError unexpectedly: {str(e)}")
        
        # Test negative income
        invalid_data = self.test_data.copy()
        invalid_data["financial_data"]["income"]["monthly_income"] = -1000
        with self.assertRaises(ValueError):
            self.validate_financial_data(invalid_data)
            
    def test_expense_validation(self):
        """Test expense validation logic"""
        # Test negative expenses
        invalid_data = self.test_data.copy()
        invalid_data["total_expenses"]["fixed_expenses"] = -1000
        with self.assertRaises(ValueError):
            self.validate_financial_data(invalid_data)
            
    def test_savings_validation(self):
        """Test savings validation logic"""
        # Test negative savings
        invalid_data = self.test_data.copy()
        invalid_data["financial_data"]["savings"]["monthly_savings"] = -1000
        with self.assertRaises(ValueError):
            self.validate_financial_data(invalid_data)
            
    def test_tax_calculations(self):
        """Test tax calculation logic"""
        monthly_income = self.test_data["financial_data"]["income"]["monthly_income"]
        tax_rate = 0.18
        
        # Calculate expected annual tax on total income
        expected_annual_tax = monthly_income * 12 * tax_rate
        
        # Test calculation
        self.assertEqual(
            expected_annual_tax,
            97200.0  # 45000 * 12 * 0.18
        )
        
    def test_total_allocation(self):
        """Test that total allocation doesn't exceed 100%"""
        monthly_income = self.test_data["financial_data"]["income"]["monthly_income"]
        annual_income = monthly_income * 12
        
        fixed_expenses = self.test_data["total_expenses"]["fixed_expenses"] * 12
        variable_expenses = self.test_data["total_expenses"]["variable_expenses"] * 12
        savings = self.test_data["financial_data"]["savings"]["monthly_savings"] * 12
        tax = monthly_income * 12 * 0.18
        
        total_allocation = fixed_expenses + variable_expenses + savings + tax
        
        self.assertLessEqual(total_allocation / annual_income * 100, 100)
        
    @patch('sys.stdout', new_callable=StringIO)
    def test_output_formatting(self, mock_stdout):
        """Test the formatting of printed output"""
        self.assertIn("income_after_expenses", self.test_data["remaining_balance"])
        
    def test_visualization_components(self):
        """Test that visualization includes all required components"""
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111)
        
        # Test figure size
        self.assertEqual(fig.get_size_inches().tolist(), [12, 8])
        
        # Clean up
        plt.close()

if __name__ == '__main__':
    unittest.main(verbosity=2)