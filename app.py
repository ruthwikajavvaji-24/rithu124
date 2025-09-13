import json
import os
from datetime import datetime
from collections import defaultdict

class FinanceManager:
    def _init_(self, data_file='finance_data.json'):
        self.data_file = data_file
        self.data = {
            "budget": 0.0,
            "expenses": []
        }
        self.load_data()

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                self.data = json.load(f)

    def save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=4)

    def set_budget(self, amount):
        try:
            amount = float(amount)
            if amount < 0:
                print("Budget cannot be negative.")
                return
            self.data['budget'] = amount
            self.save_data()
            print(f"Budget set to ${amount:.2f}")
        except ValueError:
            print("Invalid amount. Please enter a number.")

    def add_expense(self, category, amount, description=""):
        try:
            amount = float(amount)
            if amount < 0:
                print("Expense amount cannot be negative.")
                return
            expense = {
                "category": category.lower(),
                "amount": amount,
                "description": description,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.data['expenses'].append(expense)
            self.save_data()
            print(f"Added expense: ${amount:.2f} for {category}")
        except ValueError:
            print("Invalid amount. Please enter a number.")

    def get_total_expenses(self):
        return sum(exp['amount'] for exp in self.data['expenses'])

    def get_expenses_by_category(self):
        category_totals = defaultdict(float)
        for exp in self.data['expenses']:
            category_totals[exp['category']] += exp['amount']
        return category_totals

    def show_summary(self):
        budget = self.data['budget']
        total_expenses = self.get_total_expenses()
        remaining = budget - total_expenses

        print("\n--- Financial Summary ---")
        print(f"Budget: ${budget:.2f}")
        print(f"Total Expenses: ${total_expenses:.2f}")
        print(f"Remaining: ${remaining:.2f}")

        print("\nExpenses by Category:")
        category_totals = self.get_expenses_by_category()
        for cat, amt in category_totals.items():
            print(f"  {cat.title()}: ${amt:.2f}")

        self.suggest_budget_adjustments(remaining, category_totals)

    def suggest_budget_adjustments(self, remaining, category_totals):
        print("\n--- AI Suggestions ---")
        if remaining < 0:
            print("You have exceeded your budget! Consider reducing expenses in the following categories:")
            # Suggest top 3 categories with highest expenses
            sorted_cats = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
            for cat, amt in sorted_cats[:3]:
                print(f"  - {cat.title()} (${amt:.2f})")
        elif remaining < self.data['budget'] * 0.1:
            print("You are close to your budget limit. Monitor your spending carefully.")
        else:
            print("You are within your budget. Good job!")

        # Suggest saving tips based on categories
        self.suggest_saving_tips(category_totals)

    def suggest_saving_tips(self, category_totals):
        tips = {
            "food": "Try cooking at home more often to save on food expenses.",
            "entertainment": "Consider free or low-cost entertainment options like campus events.",
            "transportation": "Use public transport or bike to save on transportation costs.",
            "books": "Buy used textbooks or use library resources.",
            "utilities": "Turn off unused electronics to reduce utility bills."
        }
        print("\nSaving Tips:")
        for cat in category_totals:
            if cat in tips:
                print(f"  - {cat.title()}: {tips[cat]}")

def main():
    fm = FinanceManager()

    print("Welcome to the Intelligent Personal Finance Manager for Students!")
    while True:
        print("\nChoose an option:")
        print("1. Set Budget")
        print("2. Add Expense")
        print("3. Show Summary")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ").strip()

        if choice == '1':
            amount = input("Enter your monthly budget amount: ").strip()
            fm.set_budget(amount)
        elif choice == '2':
            category = input("Enter expense category (e.g., food, transport): ").strip()
            amount = input("Enter expense amount: ").strip()
            description = input("Enter description (optional): ").strip()
            fm.add_expense(category, amount, description)
        elif choice == '3':
            fm.show_summary()
        elif choice == '4':
            print("Goodbye! Stay financially smart.")
            break
        else:
            print("Invalid choice. Please select from 1 to 4.")

if __name__ == "__main__":
    main()