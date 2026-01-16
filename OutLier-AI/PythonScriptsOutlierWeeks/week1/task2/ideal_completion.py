import datetime
import numpy as np
from scipy.optimize import fsolve
from dateutil.relativedelta import relativedelta
import holidays
from typing import List, Dict, Union, Optional
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BondError(Exception):
    """Base exception class for bond errors"""
    pass

class ValidationError(BondError):
    """Input validation errors"""
    pass

class CalculationError(BondError):
    """Calculation failures"""
    pass

class MarketDataError(BondError):
    """Market data validation errors"""
    pass
class DayCount:
    """Handles different day count conventions for bond calculations"""
    
    @staticmethod
    def thirty_360(start_date, end_date):
        """Calculate day count fraction using 30/360 convention"""
        y1, m1, d1 = start_date.year, start_date.month, start_date.day
        y2, m2, d2 = end_date.year, end_date.month, end_date.day
        
        # Adjust day values according to 30/360 rules
        if d1 == 31: d1 = 30
        if d2 == 31 and d1 == 30: d2 = 30
        
        return ((360 * (y2 - y1) + 30 * (m2 - m1) + (d2 - d1)) / 360)
    
    @staticmethod
    def actual_360(start_date, end_date):
        """Calculate day count fraction using Actual/360 convention"""
        days = (end_date - start_date).days
        return days / 360
    
    @staticmethod
    def actual_365(start_date, end_date):
        """Calculate day count fraction using Actual/365 convention"""
        days = (end_date - start_date).days
        return days / 365
class BusinessDayAdjuster:
    """Handles business day adjustments for payment dates"""
    
    def __init__(self, calendar_name='US'):
        """
        Initialize with specified holiday calendar.
        
        Args:
            calendar_name (str): Name of the holiday calendar to use
        """
        self.calendar = getattr(holidays, calendar_name)()
    
    def is_business_day(self, date):
        """Check if given date is a business day"""
        return date.weekday() < 5 and date not in self.calendar
    
    def following(self, date):
        """Adjust to next business day"""
        while not self.is_business_day(date):
            date += datetime.timedelta(days=1)
        return date
    
    def modified_following(self, date):
        """
        Adjust to next business day unless it falls in next month,
        then adjust to previous business day
        """
        original_month = date.month
        adjusted_date = self.following(date)
        
        if adjusted_date.month != original_month:
            while not self.is_business_day(date):
                date -= datetime.timedelta(days=1)
            return date
        
        return adjusted_date
    
    def preceding(self, date):
        """Adjust to previous business day"""
        while not self.is_business_day(date):
            date -= datetime.timedelta(days=1)
        return date
class Bond:
    def __init__(self, principal, coupon_rate, payment_frequency, maturity_date, 
                market_price, issue_date, day_count_convention='thirty_360', 
                business_day_convention='following', calendar='US'):
        """
        Initialize a Bond object with enhanced validation and flexibility.
        
        Args:
            principal (float): Face value of the bond
            coupon_rate (float): Annual coupon rate (in percent)
            payment_frequency (str): 'annual' or 'semi-annual'
            maturity_date (str): Maturity date in YYYY-MM-DD format
            market_price (float): Current market price of the bond
            day_count_convention (str): Day counting convention to use
            business_day_convention (str): Business day adjustment convention
            calendar (str): Holiday calendar to use
        """
        # First convert maturity_date to datetime
        self.maturity_date = self._validate_maturity_date(maturity_date)
        # Now validate issue_date (which can use the converted maturity_date)
        self.issue_date = self._validate_issue_date(issue_date, self.maturity_date)
        
        self.day_counter = DayCount()
        self.business_day_adjuster = BusinessDayAdjuster(calendar)
        self.day_count_convention = day_count_convention
        self.business_day_convention = business_day_convention
        
        # Rest of the validation
        self.principal = self._validate_principal(principal)
        self.coupon_rate = self._validate_coupon_rate(coupon_rate)
        self.payment_frequency = self._validate_payment_frequency(payment_frequency)
        self.market_price = self._validate_market_price(market_price)

    def _validate_principal(self, principal):
        """
        Validate principal amount with enhanced checks.
        
        Args:
            principal (float): Principal amount to validate
            
        Returns:
            float: Validated principal amount
            
        Raises:
            ValidationError: If principal amount is invalid
        """
        if not isinstance(principal, (int, float)):
            raise ValidationError("Principal must be a number")
        if principal <= 0:
            raise ValidationError("Principal amount must be positive")
        if principal > 1_000_000_000:  # $1 billion threshold
            raise ValidationError("Principal amount exceeds reasonable bounds")
        return float(principal)

    def _validate_coupon_rate(self, coupon_rate):
        """
        Validate coupon rate with enhanced checks.
        
        Args:
            coupon_rate (float): Coupon rate to validate
            
        Returns:
            float: Validated coupon rate as decimal
            
        Raises:
            ValidationError: If coupon rate is invalid
        """
        if not isinstance(coupon_rate, (int, float)):
            raise ValidationError("Coupon rate must be a number")
        if not 0 <= coupon_rate <= 100:
            raise ValidationError("Coupon rate must be between 0 and 100")
        if coupon_rate > 25:  # Typical maximum market rate
            raise ValidationError("Coupon rate unusually high - please verify")
        return coupon_rate / 100

    def _validate_payment_frequency(self, payment_frequency):
        if payment_frequency not in ['annual', 'semi-annual']:
            raise ValidationError("Payment frequency must be 'annual' or 'semi-annual'.")
        return payment_frequency

    def _validate_maturity_date(self, maturity_date):
        try:
            maturity_date = datetime.datetime.strptime(maturity_date, '%Y-%m-%d').date()
        except ValueError:
            raise ValidationError("Maturity date must be in YYYY-MM-DD format.")
        if maturity_date <= datetime.date.today():
            raise ValidationError("Maturity date must be in the future")
        return maturity_date

    def _validate_market_price(self, market_price):
        """
        Validate market price with enhanced checks.
        
        Args:
            market_price (float): Market price to validate
            
        Returns:
            float: Validated market price
            
        Raises:
            ValidationError: If market price is invalid
        """
        if not isinstance(market_price, (int, float)):
            raise ValidationError("Market price must be a number")
        if market_price <= 0:
            raise ValidationError("Market price must be positive")
        if market_price > self.principal * 3:
            raise ValidationError("Market price suspiciously high compared to principal")
        if market_price < self.principal * 0.1:
            raise ValidationError("Market price suspiciously low compared to principal")
        return float(market_price)
    
    def _validate_issue_date(self, issue_date, maturity_date):
        """Validate issue date is before maturity date"""
        try:
            issue_date = datetime.datetime.strptime(issue_date, '%Y-%m-%d').date()
            if issue_date >= maturity_date:
                raise ValidationError("Issue date must be before maturity date")
            return issue_date
        except ValueError:
            raise ValidationError("Issue date must be in YYYY-MM-DD format")

    def calculate_dirty_price(self) -> float:
        """
        Calculate dirty price including accrued interest
        
        Returns:
            float: Dirty price of the bond
        """
        clean_price = self.market_price
        accrued_interest = self.calculate_accrued_interest()
        return clean_price + accrued_interest

    def calculate_accrued_interest(self) -> float:
        """
        Calculate accrued interest since last payment
        
        Returns:
            float: Accrued interest amount
        """
        last_payment_date = self._get_previous_payment_date()
        days_accrued = getattr(self.day_counter, self.day_count_convention)(
            last_payment_date, 
            datetime.date.today()
        )
        return self._calculate_coupon_payment() * days_accrued

    def _get_previous_payment_date(self):
        """Get the date of the last payment"""
        today = datetime.date.today()
        schedule = self.generate_payment_schedule()
        return max((datetime.datetime.strptime(payment['payment_date'], '%Y-%m-%d').date()
                for payment in schedule 
                if datetime.datetime.strptime(payment['payment_date'], '%Y-%m-%d').date() < today),
                default=self.issue_date)

    def calculate_yield_to_maturity(self, max_iterations=100, tolerance=1e-6):
        """
        Calculate the yield to maturity using numerical methods.
        
        Args:
            max_iterations (int): Maximum number of iterations for solver
            tolerance (float): Convergence tolerance
            
        Returns:
            float: Yield to maturity as a decimal
            
        Raises:
            CalculationError: If YTM calculation fails or doesn't converge
        """
        n = self._calculate_number_of_periods()
        coupon_payment = self._calculate_coupon_payment()


        def equation(ytm):
            present_value = sum(coupon_payment / (1 + ytm)**t for t in range(1, n+1)) + self.principal / (1 + ytm)**n
            return present_value - self.market_price

        ytm = fsolve(equation, 0.05)[0]  # Initial guess of 5%
                # Improve initial guess based on simple yield
        initial_guess = (coupon_payment + (self.principal - self.market_price)/n) / self.market_price
        
        try:
            ytm = fsolve(equation, initial_guess, maxfev=max_iterations, xtol=tolerance)[0]
            if not np.isfinite(ytm):
                raise ValidationError("YTM calculation did not converge")
            return ytm
        except RuntimeError:
            raise ValidationError("Failed to calculate YTM - try different initial values")
        return ytm

    def _calculate_number_of_periods(self):
        today = datetime.date.today()
        if self.payment_frequency == 'annual':
            return (self.maturity_date.year - today.year) + \
                (1 if (self.maturity_date.month, self.maturity_date.day) > (today.month, today.day) else 0)
        else:  # semi-annual
            months_between = (self.maturity_date.year - today.year) * 12 + \
                        (self.maturity_date.month - today.month)
            return months_between // 6

    def _calculate_coupon_payment(self):
        if self.payment_frequency == 'annual':
            coupon_payment = self.principal * self.coupon_rate
        elif self.payment_frequency == 'semi-annual':
            coupon_payment = self.principal * self.coupon_rate / 2
        return coupon_payment

    def generate_payment_schedule(self) -> List[Dict[str, Union[str, float]]]:
        """
        Generate the bond's payment schedule using PaymentSchedule class
        
        Returns:
            List[Dict]: List of payment information
        """
        scheduler = PaymentSchedule(self)
        return scheduler.generate()

    def _is_business_day(self, date):
        us_holidays = holidays.US()  # You can change this to your country
        return date.weekday() < 5 and date not in us_holidays

    def _next_business_day(self, date):
        while not self._is_business_day(date):
            date += datetime.timedelta(days=1)
        return date
    def calculate_duration(self) -> float:
        """Calculate modified duration"""
        ytm = self.calculate_yield_to_maturity()
        n = self._calculate_number_of_periods()
        coupon_payment = self._calculate_coupon_payment()
        
        duration = sum(t * coupon_payment / (1 + ytm)**t 
                    for t in range(1, n+1))
        duration += n * self.principal / (1 + ytm)**n
        duration /= self.calculate_dirty_price()
        
        return duration / (1 + ytm)

    def calculate_convexity(self) -> float:
        """Calculate convexity"""
        ytm = self.calculate_yield_to_maturity()
        n = self._calculate_number_of_periods()
        coupon_payment = self._calculate_coupon_payment()
        
        convexity = sum(t * (t + 1) * coupon_payment / (1 + ytm)**(t + 2)
                        for t in range(1, n+1))
        convexity += n * (n + 1) * self.principal / (1 + ytm)**(n + 2)
        convexity /= self.calculate_dirty_price()
        
        return convexity

    def _calculate_simple_yield(self) -> float:
        """Calculate simple yield for initial YTM guess"""
        n = self._calculate_number_of_periods()
        coupon_payment = self._calculate_coupon_payment()
        return (coupon_payment + (self.principal - self.market_price)/n) / self.market_price
    @classmethod
    def create_zero_coupon(cls, principal, maturity_date, market_price):
        """Factory method for zero-coupon bonds"""
        return cls(principal, 0, 'annual', maturity_date, market_price)

    @classmethod
    def create_treasury(cls, principal, coupon_rate, maturity_date, market_price):
        """Factory method for treasury bonds"""
        return cls(principal, coupon_rate, 'semi-annual', maturity_date, market_price)

class PaymentSchedule:
    """Handles all payment schedule calculations and business day adjustments"""
    
    def __init__(self, bond):
        """
        Initialize with a bond instance
        
        Args:
            bond (Bond): The bond to generate schedules for
        """
        self.bond = bond

    def generate(self) -> List[Dict[str, Union[str, float]]]:
        """
        Generate complete payment schedule for the bond
        
        Returns:
            List[Dict]: List of payment dictionaries containing dates and amounts
        """
        n = self.bond._calculate_number_of_periods()
        coupon_payment = self.bond._calculate_coupon_payment()
        schedule = []
        start_date = self.bond.issue_date

        for t in range(1, n+1):
            # Calculate payment date based on frequency
            if self.bond.payment_frequency == 'annual':
                payment_date = start_date + relativedelta(years=t)
            else:  # semi-annual
                payment_date = start_date + relativedelta(months=6*t)
            
            # Apply business day adjustment
            adjusted_date = self.bond.business_day_adjuster.following(payment_date)
            
            # Calculate payment amount
            amount = coupon_payment
            if t == n:  # Final payment includes principal
                amount += self.bond.principal

            # Determine payment status
            is_past_due = adjusted_date < datetime.date.today()

            # Add payment to schedule
            schedule.append({
                'payment_date': adjusted_date.strftime('%Y-%m-%d'),
                'original_date': payment_date.strftime('%Y-%m-%d'),
                'payment_amount': amount,
                'payment_status': 'past due' if is_past_due else 'not past due',
                'type': 'final payment' if t == n else 'coupon payment'
            })

        return schedule

if __name__ == "__main__":
    try:
        bond = Bond(
            principal=1000,
            coupon_rate=5,
            payment_frequency='annual',
            maturity_date='2030-12-31',
            market_price=900,
            issue_date='2023-01-01',
            day_count_convention='thirty_360',
            business_day_convention='following',
            calendar='US'
        )
        
        print(f"Yield to Maturity: {bond.calculate_yield_to_maturity():.4%}")
        print(f"Dirty Price: ${bond.calculate_dirty_price():.2f}")
        print(f"Duration: {bond.calculate_duration():.2f} years")
        print(f"Convexity: {bond.calculate_convexity():.2f}")
        print("\nPayment Schedule:")
        for payment in bond.generate_payment_schedule():
            print(payment)
            
    except BondError as e:
        logger.error(f"Bond calculation error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")