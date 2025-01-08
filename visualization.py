# Visualize our spending, savings, and goals
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
from datetime import datetime
EXPENSES_FILE = "data/expenses.json"
SAVINGS_FILE = "data/savings.json"
GOALS_FILE = "data/goals.json"

# Load data from JSON or return a default
def load_data(file_path, default):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return default

# Main visualizations page
def display_visualizations():
    st.title("📊 Visualizations")
    st.write("Explore your spending and savings trends with these visuals.")

    # Tabs for visualizations
    tab1, tab2, tab3 = st.tabs(["💸 Spending", "🏦 Savings", "🔍 Insights"])

    with tab1:
        spending_visualizations()
    with tab2:
        savings_visualizations()
    with tab3:
        insights_visualizations()

# Spending Visualizations
def spending_visualizations():
    st.subheader("💸 Spending Overview")

    # Load data
    expenses = load_data(EXPENSES_FILE, [])
    savings = load_data(SAVINGS_FILE, {"category_budget": {}})
    category_budget = savings.get("category_budget", {})

    # Total expenses and budget
    total_expenses = sum(exp["amount"] for exp in expenses)
    total_budget = sum(category_budget.values())

    # Progress bar: Expenses vs Budget
    st.write("### Total Expenses vs Budget")
    if total_budget > 0:
        progress = min(total_expenses / total_budget, 1.0)
        st.write(f"**Spent:** {total_expenses} / **Budget:** {total_budget}")
        st.progress(progress)
        if total_expenses > total_budget:
            st.error("Oops! You've overspent. Time to review your spending.")
        else:
            st.success("You're on track. Keep it up!")
    else:
        st.info("No budget set yet. Add a budget to start tracking.")

    # Bar chart: Spending by Category
    st.write("### Spending by Category")
    category_expenses = pd.DataFrame(expenses).groupby("category")["amount"].sum().to_dict()
    categories = list(category_budget.keys())
    allocated = [category_budget.get(cat, 0) for cat in categories]
    spent = [category_expenses.get(cat, 0) for cat in categories]

    fig, ax = plt.subplots()
    ax.bar(categories, allocated, label="Budget Allocated", alpha=0.7, color="#a3c1ad")
    ax.bar(categories, spent, label="Amount Spent", alpha=0.7, color="#f77670")
    ax.legend()
    st.pyplot(fig)

# Savings Visualizations
def savings_visualizations():
    st.subheader("🏦 Savings Overview")

    # Load data
    savings = load_data(SAVINGS_FILE, {"total_savings": 0, "history": []})
    total_savings = savings.get("total_savings", 0)

    # Line chart: Savings Over Time
    st.write("### Savings Over Time")
    savings_history = savings.get("history", [])
    if savings_history:
        dates = [entry["date"] for entry in savings_history]
        amounts = [entry["amount"] for entry in savings_history]
        st.line_chart(pd.DataFrame({"Date": dates, "Savings": amounts}).set_index("Date"))
    else:
        st.info("No savings history yet. Start saving to see trends!")

# Insights Visualizations
def insights_visualizations():
    st.subheader("🔍 Key Insights")

    # Load data
    expenses = load_data(EXPENSES_FILE, [])
    savings = load_data(SAVINGS_FILE, {"total_savings": 0})
    category_budget = savings.get("category_budget", {})

    # Overspending Alerts
    st.write("### Overspending Alerts")
    category_expenses = pd.DataFrame(expenses).groupby("category")["amount"].sum().to_dict()
    for category, allocated in category_budget.items():
        spent = category_expenses.get(category, 0)
        if spent > allocated:
            st.error(f"You're overspending in **{category}** by {spent - allocated}.")
        elif spent == allocated:
            st.warning(f"**{category}** budget fully utilized.")
        else:
            st.success(f"**{category}**: Within budget with {allocated - spent} remaining.")

    # Savings vs Expenses Comparison
    st.write("### Savings vs Expenses")
    total_expenses = sum(exp["amount"] for exp in expenses)
    total_savings = savings.get("total_savings", 0)

    labels = ["Savings", "Expenses"]
    values = [total_savings, total_expenses]
    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90, colors=["#8fd694", "#f77670"])
    ax.axis("equal")
    st.pyplot(fig)

# Run visualizations
if __name__ == "__main__":
    display_visualizations()
