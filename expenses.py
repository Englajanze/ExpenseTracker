# add expenses (catagory, date, amount)
# list expenses based on catagory
# take input of catagory, date and amount
# ensure that it follows validate inputs

import json

EXPENSES_FILE = "data/expenses.json"

def load_expenses():
    # Loading expenses from JSON file
    try:
        with open(EXPENSES_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # If the file doesn't exist or is empty, return an empty list
        return []


expenses = load_expenses()
print("Current Expenses:", expenses)
