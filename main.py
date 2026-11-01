import csv
from pathlib import Path
from datetime import date

DATA_FILE = Path("expenses.csv")
FIELDS = ["date", "category", "description", "amount"]

def load_expenses():
    if not DATA_FILE.exists():
        return []
    with DATA_FILE.open("r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))

def save_expense(category, description, amount):
    file_exists = DATA_FILE.exists()
    with DATA_FILE.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            "date": date.today().isoformat(),
            "category": category,
            "description": description,
            "amount": f"{amount:.2f}",
        })

def show_expenses(expenses):
    if not expenses:
        print("\nNo expenses recorded yet.")
        return
    print("\nDATE        CATEGORY       DESCRIPTION                 AMOUNT")
    print("-" * 70)
    for item in expenses:
        print(f"{item['date']:<11}{item['category']:<15}"
              f"{item['description'][:25]:<27}₹{float(item['amount']):.2f}")

def show_summary(expenses):
    total = sum(float(item["amount"]) for item in expenses)
    by_category = {}
    for item in expenses:
        by_category[item["category"]] = (
            by_category.get(item["category"], 0) + float(item["amount"])
        )
    print(f"\nTotal expenses: ₹{total:.2f}")
    if by_category:
        print("Category-wise summary:")
        for category, amount in sorted(by_category.items()):
            print(f"  {category}: ₹{amount:.2f}")

def main():
    while True:
        print("\n=== Student Expense Tracker ===")
        print("1. Add expense")
        print("2. View expense history")
        print("3. View summary")
        print("4. Exit")
        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            category = input("Category (Food/Travel/Books/Other): ").strip()
            description = input("Description: ").strip()
            try:
                amount = float(input("Amount (₹): "))
                if amount <= 0:
                    raise ValueError
                if not category or not description:
                    print("Category and description cannot be empty.")
                    continue
                save_expense(category, description, amount)
                print("Expense saved successfully.")
            except ValueError:
                print("Please enter a valid amount greater than zero.")
        elif choice == "2":
            show_expenses(load_expenses())
        elif choice == "3":
            show_summary(load_expenses())
        elif choice == "4":
            print("Thank you for using Student Expense Tracker!")
            break
        else:
            print("Invalid choice. Please select 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()
