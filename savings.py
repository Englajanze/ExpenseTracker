import streamlit as st
import json

EXPENSES_FILE = "data/expenses.json"  # File to store expenses

def load_json(file_path, default):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return default

# Display the Savings Vault tab
def display_savings():
    st.title("🏦 Savings Vault")
    st.write("Track your total expenses and spending progress here.")

    # Load expenses
    expenses = load_json(EXPENSES_FILE, [])

    # Calculate total expenses by category
    total_expenses = {}
    for expense in expenses:
        category = expense.get("category", "Other")
        total_expenses[category] = total_expenses.get(category, 0) + expense.get("amount", 0)

    # Display total expenses
    st.subheader("Expenses Overview")
    if total_expenses:
        for category, amount in total_expenses.items():
            st.write(f"**{category}**: {amount}")
    else:
        st.info("No expenses recorded yet. Go to the Expenses tab to add your data.")

    # Add a divider for spacing
    st.write("---")
    st.write("This section is under development. Future updates will include progress bars and goal tracking!")

# reset monthly budget and move leftover money here(Haven't implemented yet will make it better!!!)