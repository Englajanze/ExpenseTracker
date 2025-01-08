# Manage monthly/weekly budget and track spending
import streamlit as st
import json
import pandas as pd
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt

# File paths
CATEGORY_FILE = "data/expensecatagories.json"
EXPENSES_FILE = "data/expenses.json"
SAVINGS_FILE = "data/savings.json"
GOALS_FILE = "data/goals.json"

# Helper function: Load data from a file or return a default
def load_data(file_path, default):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return default

# Helper function: Save data to a file
def save_data(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

# Load budget categories or use default ones
def load_categories():
    return load_data(CATEGORY_FILE, ["Food", "Transport", "Entertainment", "Other"])

# Main budget page
def display_budget():
    st.title("💰 Budget Mastery")
    st.write("Manage your budget, spending, and savings all in one place.")

    # Tabs for navigation
    selected = option_menu(
        menu_title=None,
        options=["Start Budgeting", "Reset Budget", "Visualize"],
        icons=["piggy-bank", "refresh", "bar-chart-line"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal"
    )

    if selected == "Start Budgeting":
        show_progress_bars()
        income = start_budgeting()
        if income > 0:
            allocate_budget(income)
    elif selected == "Reset Budget":
        reset_budget()
    elif selected == "Visualize":
        visualize_budget()

# Show progress bars for expenses vs budget and savings vs goals
def show_progress_bars():
    st.subheader("📊 Progress Overview")

    # Load data
    savings = load_data(SAVINGS_FILE, {"total_savings": 0, "history": []})
    total_savings = savings.get("total_savings", 0)
    expenses = load_data(EXPENSES_FILE, [])
    total_expenses = sum(exp["amount"] for exp in expenses)
    category_budget = load_data(SAVINGS_FILE, {}).get("category_budget", {})
    goals = load_data(GOALS_FILE, [])

    # Budget progress
    total_budget = sum(category_budget.values())
    if total_budget > 0:
        st.write(f"**Expenses vs Budget**: {total_expenses} / {total_budget}")
        st.progress(min(total_expenses / total_budget, 1.0))
        if total_expenses > total_budget:
            st.error("Uh-oh! You've gone over your budget. Time to cut back!")
        else:
            st.success("You're on track! Keep it up!")
    else:
        st.info("No budget set yet. Start budgeting to track your spending.")

    # Savings goal progress
    st.subheader("Savings Goals")
    if goals:
        for goal in goals:
            target = goal.get("target", 0)
            progress = min(total_savings / target, 1.0) if target > 0 else 0
            st.write(f"**{goal.get('name', 'Unnamed Goal')}**: {total_savings} saved, {max(target - total_savings, 0)} remaining")
            st.progress(progress)
    else:
        st.info("No savings goals yet. Set some in the Goals tab!")

# Input total income
def start_budgeting():
    st.subheader("Set Your Income")
    income = st.number_input("Enter your monthly income:", min_value=0, step=10)
    if income > 0:
        st.success(f"Your income is set to {income}.")
    return income

# Allocate income to budget categories
def allocate_budget(income):
    st.subheader("Allocate Your Budget")
    categories = load_categories()
    total_allocated = 0
    category_budget = {}

    for category in categories:
        amount = st.number_input(f"Budget for {category}:", min_value=0, step=10)
        total_allocated += amount
        category_budget[category] = amount

    remaining = income - total_allocated

    if total_allocated > income:
        st.error("Yikes! You're trying to spend more than you earn. Adjust your budget.")
    else:
        st.success(f"Allocated: {total_allocated}. Remaining: {remaining}.")
        save_data(SAVINGS_FILE, {"category_budget": category_budget, "remaining_budget": remaining})

# Reset budget and move leftover funds to savings
def reset_budget():
    st.subheader("Reset Budget")
    savings = load_data(SAVINGS_FILE, {"total_savings": 0, "remaining_budget": 0})
    remaining_budget = savings.get("remaining_budget", 0)

    if st.button("Reset Now"):
        savings["total_savings"] += remaining_budget
        savings["remaining_budget"] = 0
        save_data(SAVINGS_FILE, savings)
        st.success(f"Remaining {remaining_budget} moved to savings!")

# Visualize budget and savings
def visualize_budget():
    st.subheader("📊 Visualize Spending and Savings")

    expenses = load_data(EXPENSES_FILE, [])
    savings = load_data(SAVINGS_FILE, {"total_savings": 0, "history": []})
    category_budget = load_data(SAVINGS_FILE, {}).get("category_budget", {})

    # Bar chart: Spending vs Budget
    st.write("### Spending vs Budget")
    category_expenses = pd.DataFrame(expenses).groupby("category")["amount"].sum().to_dict()
    categories = list(category_budget.keys())
    allocated = [category_budget.get(cat, 0) for cat in categories]
    spent = [category_expenses.get(cat, 0) for cat in categories]

    fig, ax = plt.subplots()
    ax.bar(categories, allocated, label="Budget Allocated", alpha=0.7)
    ax.bar(categories, spent, label="Amount Spent", alpha=0.7)
    ax.legend()
    st.pyplot(fig)

    # Line chart: Savings over time
    st.write("### Savings Over Time")
    savings_history = savings.get("history", [])
    if savings_history:
        dates = [entry["date"] for entry in savings_history]
        amounts = [entry["amount"] for entry in savings_history]
        st.line_chart(pd.DataFrame({"Date": dates, "Savings": amounts}).set_index("Date"))
    else:
        st.info("No savings history yet. Start saving to see trends!")

# Run the app
if __name__ == "__main__":
    display_budget()
