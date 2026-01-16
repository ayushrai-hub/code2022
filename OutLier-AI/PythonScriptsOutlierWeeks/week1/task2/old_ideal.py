import datetime
import numpy as np
from scipy.optimize import fsolve
from dateutil.relativedelta import relativedelta
import holidays
class Bond:
    def __init__(self, principal, coupon_rate, payment_frequency, maturity_date, market_price):
        """
        Initialize the Bond object.

        Args:
        - principal (float): The principal amount of the bond. Must be positive.
        - coupon_rate (float): The annual coupon rate of the bond. Must be between 0 and 100.
        - payment_frequency (str): The payment frequency of the bond. Can be 'annual' or 'semi-annual'.
        - maturity_date (str): The maturity date of the bond. Must be in YYYY-MM-DD format.
        - market_price (float): The current market price of the bond. Must be positive.
        """
        self.principal = self._validate_principal(principal)
        self.coupon_rate = self._validate_coupon_rate(coupon_rate)
        self.payment_frequency = self._validate_payment_frequency(payment_frequency)
        self.maturity_date = self._validate_maturity_date(maturity_date)
        self.market_price = self._validate_market_price(market_price)

    def _validate_principal(self, principal):
        if principal <= 0:
            raise ValueError("Principal amount must be positive.")
        return principal

    def _validate_coupon_rate(self, coupon_rate):
        if not 0 <= coupon_rate <= 100:
            raise ValueError("Coupon rate must be between 0 and 100.")
        return coupon_rate / 100  # Convert to decimal

    def _validate_payment_frequency(self, payment_frequency):
        if payment_frequency not in ['annual', 'semi-annual']:
            raise ValueError("Payment frequency must be 'annual' or 'semi-annual'.")
        return payment_frequency

    def _validate_maturity_date(self, maturity_date):
        try:
            maturity_date = datetime.datetime.strptime(maturity_date, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError("Maturity date must be in YYYY-MM-DD format.")
        return maturity_date

    def _validate_market_price(self, market_price):
        if market_price <= 0:
            raise ValueError("Market price must be positive.")
        return market_price

    def calculate_yield_to_maturity(self):
        """
        Calculate the yield to maturity of the bond using numerical methods.

        Returns:
        - ytm (float): The yield to maturity of the bond.
        """
        n = self._calculate_number_of_periods()
        coupon_payment = self._calculate_coupon_payment()

        def equation(ytm):
            present_value = sum(coupon_payment / (1 + ytm)**t for t in range(1, n+1)) + self.principal / (1 + ytm)**n
            return present_value - self.market_price

        ytm = fsolve(equation, 0.05)[0]  # Initial guess of 5%
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

    def generate_payment_schedule(self):
        """
        Generate the payment schedule of the bond.

        Returns:
        - payment_schedule (list): A list of dictionaries containing the payment date, amount, and status (past due or not).
        """
        n = self._calculate_number_of_periods()
        coupon_payment = self._calculate_coupon_payment()
        payment_schedule = []
        start_date = datetime.date.today()
        for t in range(1, n+1):
            if self.payment_frequency == 'annual':
                payment_date = start_date + relativedelta(years=t)
            elif self.payment_frequency == 'semi-annual':
                payment_date = start_date + relativedelta(months=6*t)
            # Move payment date to next business day if it falls on a weekend
            payment_date = self._next_business_day(payment_date)

            payment_amount = coupon_payment
            if t == n:
                payment_amount += self.principal

            payment_status = 'past due' if payment_date < datetime.date.today() else 'not past due'

            payment_schedule.append({
                'payment_date': payment_date.strftime('%Y-%m-%d'),
                'payment_amount': payment_amount,
                'payment_status': payment_status
            })

        return payment_schedule

    def _is_business_day(self, date):
        us_holidays = holidays.US()  # You can change this to your country
        return date.weekday() < 5 and date not in us_holidays

    def _next_business_day(self, date):
        while not self._is_business_day(date):
            date += datetime.timedelta(days=1)
        return date

# Example usage
bond = Bond(1000, 5, 'annual', '2030-12-31', 900)
print("Yield to Maturity:", bond.calculate_yield_to_maturity())
print("Payment Schedule:")
for payment in bond.generate_payment_schedule():
    print(payment)