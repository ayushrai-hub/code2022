import matplotlib.pyplot as plt
from typing import Dict, Any

def validate_financial_data(data: Dict[str, Any]) -> None:
    """Validates the financial data structure and values.
    Raises ValueError if data is invalid."""
    
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

# Dataset
data = {
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

try:
    # Validate input data
    validate_financial_data(data)

    # Extracting values from the dataset
    monthly_income = data["financial_data"]["income"]["monthly_income"]
    fixed_expenses = data["total_expenses"]["fixed_expenses"]
    variable_expenses = data["total_expenses"]["variable_expenses"]
    monthly_savings = data["financial_data"]["savings"]["monthly_savings"]
    tax_rate = 0.18  # Fixed tax rate

    if not 0 <= tax_rate <= 1:
        raise ValueError("Tax rate must be between 0 and 1")

    # Calculations with error handling
    annual_income = monthly_income * 12
    annual_tax = sum(source["amount"] * 12 for source in data["financial_data"]["income"]["sources"]) * tax_rate
    annual_fixed_expenses = fixed_expenses * 12
    annual_variable_expenses = variable_expenses * 12
    annual_savings = monthly_savings * 12
    annual_expenses = annual_fixed_expenses + annual_variable_expenses
    remaining_balance = annual_income - (annual_expenses + annual_tax + annual_savings)

    # Verify calculations make sense
    if remaining_balance < 0:
        raise ValueError("Warning: Expenses exceed income!")
    if annual_expenses > annual_income:
        raise ValueError("Warning: Total expenses exceed total income!")

    # Data for visualization
    categories = ['Fixed Expenses', 'Variable Expenses', 'Savings', 'Taxes']
    values = [annual_fixed_expenses, annual_variable_expenses, annual_savings, annual_tax]
    
    # Verify all values are positive
    if any(value < 0 for value in values):
        raise ValueError("All financial values must be positive")
        
    percentages = [(value / annual_income) * 100 for value in values]
    
    # Verify percentages sum to less than or equal to 100
    if sum(percentages) > 100:
        raise ValueError("Total allocation exceeds 100% of income")

    # Print financial breakdown
    print("\nFinancial Breakdown:")
    print("-" * 50)
    print("Annual Income: ₹{:,.2f}".format(annual_income))
    print("\nCategory-wise Breakdown:")
    for category, value, pct in zip(categories, values, percentages):
        print(f"{category}: ₹{value:,.2f} ({pct:.1f}%)")

    print("\nBalance Calculation:")
    print("-" * 50)
    print(f"Total Annual Income:           ₹{annual_income:,.2f}")
    print(f"Total Annual Expenses:         ₹{annual_expenses:,.2f}")
    print(f"Total Annual Tax:              ₹{annual_tax:,.2f}")
    print(f"Total Annual Savings:          ₹{annual_savings:,.2f}")
    print(f"Remaining Balance:             ₹{remaining_balance:,.2f}")
    print(f"Monthly Remaining Balance:     ₹{remaining_balance/12:,.2f}")
    
    percentages = [(value / annual_income) * 100 for value in values]

    # Verify percentages sum to less than or equal to 100
    if sum(percentages) > 100:
        raise ValueError("Total allocation exceeds 100% of income")
        
    # Plotting the bar chart
    fig = plt.figure(figsize=(12, 8))  # Increased figure size
    ax = fig.add_subplot(111)
    bars = ax.bar(categories, values, color=['blue', 'green', 'purple', 'orange'])

    # Adding title and labels
    ax.set_title('Annual Financial Distribution', fontsize=16, pad=20)  # Added padding to title
    ax.set_ylabel('Amount (₹)', fontsize=12)
    ax.set_xlabel('Categories', fontsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    # Adding percentage labels above each bar
    for bar, value, pct in zip(bars, values, percentages):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 10000, 
                f"₹{value:,.2f}\n({pct:.1f}%)",
                ha='center', fontsize=10)

    # Adding a note for remaining balance
    # Adjusted the position and used figure coordinates
    fig.text(0.5, 0.02,  # Moved text up slightly
            f"Remaining Balance After Allocation: ₹{remaining_balance:,.2f}",
            ha='center', fontsize=12, color='red')

    # Adjust the layout with specific padding
    plt.subplots_adjust(bottom=0.15)  # Added more bottom margin

    # Show the plot
    plt.show()

except (KeyError, TypeError) as e:
    print(f"Error in data structure: {str(e)}")
except ValueError as e:
    print(f"Validation error: {str(e)}")
except Exception as e:
    print(f"An unexpected error occurred: {str(e)}")