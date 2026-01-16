import matplotlib.pyplot as plt

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

# Extracting values from the dataset
monthly_income = data["financial_data"]["income"]["monthly_income"]
fixed_expenses = data["total_expenses"]["fixed_expenses"]
variable_expenses = data["total_expenses"]["variable_expenses"]
monthly_savings = data["financial_data"]["savings"]["monthly_savings"]
tax_rate = 0.18  # Fixed tax rate

# Calculations
annual_income = monthly_income * 12
annual_tax = sum([source["amount"] for source in data["financial_data"]["income"]["sources"]]) * 12 * tax_rate  # Tax on total income
annual_fixed_expenses = fixed_expenses * 12
annual_variable_expenses = variable_expenses * 12
annual_savings = monthly_savings * 12
annual_expenses = annual_fixed_expenses + annual_variable_expenses
remaining_balance = annual_income - (annual_expenses + annual_tax + annual_savings)

# Data for visualization
categories = ['Fixed Expenses', 'Variable Expenses', 'Savings', 'Taxes']
values = [annual_fixed_expenses, annual_variable_expenses, annual_savings, annual_tax]
percentages = [(value / annual_income) * 100 for value in values]

# Plotting the bar chart
plt.figure(figsize=(10, 7))
bars = plt.bar(categories, values, color=['blue', 'green', 'purple', 'orange'])

# Adding title and labels
plt.title('Annual Financial Distribution', fontsize=16)
plt.ylabel('Amount (₹)', fontsize=12)
plt.xlabel('Categories', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Adding percentage labels above each bar
for bar, value, pct in zip(bars, values, percentages):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 10000, f"₹{value:.2f}\n({pct:.1f}%)",
             ha='center', fontsize=10)

# Adding a note for remaining balance
plt.text(0.5, -0.15 * max(values), f"Remaining Balance After Allocation: ₹{remaining_balance:.2f}",
         ha='center', fontsize=12, color='red', transform=plt.gca().transAxes)
plt.tight_layout()

# Show the plot
plt.show()