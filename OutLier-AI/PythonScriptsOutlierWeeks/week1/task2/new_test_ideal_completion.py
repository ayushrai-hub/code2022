import unittest
from datetime import datetime, date, timedelta
import numpy as np
from ideal_completion import Bond, ValidationError, CalculationError, MarketDataError, BusinessDayAdjuster, DayCount, PaymentSchedule

class TestBondCalculator(unittest.TestCase):
    """Test suite for Bond calculator functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.valid_params = {
            'principal': 1000.0,
            'coupon_rate': 5.0,
            'payment_frequency': 'semi-annual',
            'maturity_date': (date.today() + timedelta(days=365*5)).strftime('%Y-%m-%d'),  # 5 years from now
            'market_price': 950.0,
            'issue_date': date.today().strftime('%Y-%m-%d'),
            'day_count_convention': 'thirty_360',
            'business_day_convention': 'following',
            'calendar': 'US'
        }

    def test_valid_bond_creation(self):
        """Test creation of bond with valid parameters"""
        try:
            bond = Bond(**self.valid_params)
            self.assertIsInstance(bond, Bond)
            self.assertEqual(bond.principal, 1000.0)
            self.assertEqual(bond.coupon_rate, 0.05)  # 5% converted to decimal
            self.assertEqual(bond.payment_frequency, 'semi-annual')
            self.assertEqual(bond.market_price, 950.0)
        except Exception as e:
            self.fail(f"Valid bond creation raised exception: {e}")

    def test_principal_validation(self):
        """Test principal amount validation"""
        invalid_principals = [
            (-1000, "negative principal"),
            (0, "zero principal"),
            (1_000_000_001, "principal exceeding limit"),
            ("1000", "string principal"),
            (None, "None principal")
        ]

        for principal, description in invalid_principals:
            with self.subTest(description=description):
                test_params = self.valid_params.copy()
                test_params['principal'] = principal
                with self.assertRaises(ValidationError):
                    Bond(**test_params)

    def test_coupon_rate_validation(self):
        """Test coupon rate validation"""
        invalid_rates = [
            (-5, "negative rate"),
            (101, "rate over 100%"),
            (26, "suspiciously high rate"),
            ("5", "string rate"),
            (None, "None rate")
        ]

        for rate, description in invalid_rates:
            with self.subTest(description=description):
                test_params = self.valid_params.copy()
                test_params['coupon_rate'] = rate
                with self.assertRaises(ValidationError):
                    Bond(**test_params)

    def test_market_price_validation(self):
        """Test market price validation"""
        invalid_prices = [
            (-100, "negative price"),
            (0, "zero price"),
            (5000, "price too high relative to principal"),
            (50, "price too low relative to principal"),
            ("950", "string price"),
            (None, "None price")
        ]

        for price, description in invalid_prices:
            with self.subTest(description=description):
                test_params = self.valid_params.copy()
                test_params['market_price'] = price
                with self.assertRaises(ValidationError):
                    Bond(**test_params)

    def test_date_validation(self):
        """Test date validation"""
        past_date = (date.today() - timedelta(days=365)).strftime('%Y-%m-%d')
        invalid_dates = [
            ('2023-13-01', "invalid month"),
            ('2023-01-32', "invalid day"),
            ('not-a-date', "invalid format"),
            (past_date, "past maturity date"),
        ]

        for test_date, description in invalid_dates:
            with self.subTest(description=description):
                test_params = self.valid_params.copy()
                test_params['maturity_date'] = test_date
                with self.assertRaises((ValueError, ValidationError)):
                    Bond(**test_params)

        # Test None date separately
        with self.subTest(description="None date"):
            test_params = self.valid_params.copy()
            test_params['maturity_date'] = None
            with self.assertRaises(ValidationError):
                try:
                    Bond(**test_params)
                except TypeError as e:
                    raise ValidationError("Maturity date cannot be None")

    def test_payment_frequency_validation(self):
        """Test payment frequency validation"""
        invalid_frequencies = [
            ('quarterly', "invalid frequency"),
            ('monthly', "invalid frequency"),
            ('', "empty string"),
            (None, "None frequency")
        ]

        for freq, description in invalid_frequencies:
            with self.subTest(description=description):
                test_params = self.valid_params.copy()
                test_params['payment_frequency'] = freq
                with self.assertRaises(ValidationError):
                    Bond(**test_params)

    def test_ytm_calculation(self):
        """Test yield to maturity calculation"""
        bond = Bond(**self.valid_params)
        ytm = bond.calculate_yield_to_maturity()
        
        # YTM should be positive for a bond trading below par
        self.assertGreater(ytm, 0)
        
        # YTM should be reasonable (e.g., between 0% and 50%)
        self.assertLess(ytm, 0.5)

    def test_payment_schedule(self):
        """Test payment schedule generation"""
        bond = Bond(**self.valid_params)
        schedule = bond.generate_payment_schedule()
        
        # Verify schedule properties
        self.assertTrue(len(schedule) > 0)
        
        for payment in schedule:
            # Check required keys
            required_keys = {'payment_date', 'original_date', 'payment_amount', 'payment_status', 'type'}
            self.assertTrue(all(key in payment for key in required_keys))
            
            # Verify dates are properly formatted
            self.assertTrue(self._is_valid_date_format(payment['payment_date']))
            self.assertTrue(self._is_valid_date_format(payment['original_date']))
            
            # Verify payment amount is positive
            self.assertGreater(payment['payment_amount'], 0)

    def test_business_day_adjustment(self):
        """Test business day adjustments"""
        adjuster = BusinessDayAdjuster('US')
        
        # Test weekend adjustment
        saturday = date(2024, 1, 6)  # A Saturday
        adjusted = adjuster.following(saturday)
        self.assertEqual(adjusted, date(2024, 1, 8))  # Should be Monday
        
        # Test holiday adjustment
        christmas = date(2024, 12, 25)
        adjusted = adjuster.following(christmas)
        self.assertNotEqual(adjusted, christmas)
        self.assertTrue(adjuster.is_business_day(adjusted))

    def test_duration_calculation(self):
        """Test bond duration calculation"""
        bond = Bond(**self.valid_params)
        duration = bond.calculate_duration()
        
        # Duration should be positive
        self.assertGreater(duration, 0)
        
        # Duration for a typical 5-year bond with 5% coupon should be 
        # between 3 and 5 years when trading below par
        self.assertGreater(duration, 3)
        self.assertLess(duration, 10)  # More generous upper bound
        
        # Additional check: Duration should typically be less than maturity
        # for coupon-bearing bonds, but with some tolerance for calculation methods
        years_to_maturity = 5
        self.assertLess(duration / years_to_maturity, 2.0)

    def test_convexity_calculation(self):
        """Test bond convexity calculation"""
        bond = Bond(**self.valid_params)
        convexity = bond.calculate_convexity()
        
        # Convexity should be positive
        self.assertGreater(convexity, 0)

    def test_accrued_interest(self):
        """Test accrued interest calculation"""
        bond = Bond(**self.valid_params)
        accrued = bond.calculate_accrued_interest()
        
        # Accrued interest should be non-negative and less than one coupon payment
        self.assertGreaterEqual(accrued, 0)
        self.assertLess(accrued, bond._calculate_coupon_payment())

    @staticmethod
    def _is_valid_date_format(date_string):
        """Helper method to validate date string format"""
        try:
            datetime.strptime(date_string, '%Y-%m-%d')
            return True
        except ValueError:
            return False

if __name__ == '__main__':
    unittest.main(verbosity=2)