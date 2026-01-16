import unittest
import datetime
from datetime import date
from unittest.mock import patch
from ideal_completion import Bond  # Assuming the Bond class is in bond.py

class TestBond(unittest.TestCase):
    def setUp(self):
        """Set up test cases with valid bond parameters"""
        self.valid_principal = 1000
        self.valid_coupon_rate = 5
        self.valid_payment_freq = 'annual'
        self.valid_maturity = '2030-12-31'
        self.valid_market_price = 900

    def test_valid_initialization(self):
        """Test initialization with valid parameters"""
        bond = Bond(
            self.valid_principal,
            self.valid_coupon_rate,
            self.valid_payment_freq,
            self.valid_maturity,
            self.valid_market_price
        )
        self.assertEqual(bond.principal, self.valid_principal)
        self.assertEqual(bond.coupon_rate, self.valid_coupon_rate/100)
        self.assertEqual(bond.payment_frequency, self.valid_payment_freq)
        self.assertEqual(bond.maturity_date, datetime.datetime.strptime(self.valid_maturity, '%Y-%m-%d').date())
        self.assertEqual(bond.market_price, self.valid_market_price)

    def test_invalid_principal(self):
        """Test initialization with invalid principal amounts"""
        invalid_principals = [0, -1000]
        for principal in invalid_principals:
            with self.assertRaises(ValueError) as context:
                Bond(principal, self.valid_coupon_rate, self.valid_payment_freq, 
                    self.valid_maturity, self.valid_market_price)
            self.assertEqual(str(context.exception), "Principal amount must be positive.")

    def test_invalid_coupon_rate(self):
        """Test initialization with invalid coupon rates"""
        invalid_rates = [-1, 101]
        for rate in invalid_rates:
            with self.assertRaises(ValueError) as context:
                Bond(self.valid_principal, rate, self.valid_payment_freq,
                    self.valid_maturity, self.valid_market_price)
            self.assertEqual(str(context.exception), "Coupon rate must be between 0 and 100.")

    def test_invalid_payment_frequency(self):
        """Test initialization with invalid payment frequency"""
        invalid_freqs = ['quarterly', 'monthly', '']
        for freq in invalid_freqs:
            with self.assertRaises(ValueError) as context:
                Bond(self.valid_principal, self.valid_coupon_rate, freq,
                    self.valid_maturity, self.valid_market_price)
            self.assertEqual(str(context.exception), "Payment frequency must be 'annual' or 'semi-annual'.")

    def test_invalid_maturity_date(self):
        """Test initialization with invalid maturity dates"""
        invalid_dates = ['2030/12/31', '2030-13-31', '2030-12-32', 'invalid']
        for maturity in invalid_dates:
            with self.assertRaises(ValueError) as context:
                Bond(self.valid_principal, self.valid_coupon_rate, self.valid_payment_freq,
                    maturity, self.valid_market_price)
            self.assertEqual(str(context.exception), "Maturity date must be in YYYY-MM-DD format.")

    def test_invalid_market_price(self):
        """Test initialization with invalid market prices"""
        invalid_prices = [0, -900]
        for price in invalid_prices:
            with self.assertRaises(ValueError) as context:
                Bond(self.valid_principal, self.valid_coupon_rate, self.valid_payment_freq,
                    self.valid_maturity, price)
            self.assertEqual(str(context.exception), "Market price must be positive.")

    def test_payment_schedule_generation(self):
        """Test payment schedule generation"""
        bond = Bond(1000, 5, 'annual', '2025-12-31', 900)
        schedule = bond.generate_payment_schedule()
        
        # Check that schedule is not empty
        self.assertTrue(len(schedule) > 0)
        
        # Check that all payments have required keys
        required_keys = {'payment_date', 'payment_amount', 'payment_status'}
        for payment in schedule:
            self.assertTrue(all(key in payment for key in required_keys))

    def test_business_day_adjustment(self):
        """Test business day adjustments for weekend payments"""
        # Mock a payment date that falls on a Sunday
        sunday_date = date(2024, 1, 7)  # This is a Sunday
        bond = Bond(1000, 5, 'annual', '2025-12-31', 900)
        next_business_day = bond._next_business_day(sunday_date)
        
        # Should move to Monday
        self.assertEqual(next_business_day, date(2024, 1, 8))
        
if __name__ == '__main__':
    unittest.main(verbosity=2)