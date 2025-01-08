# Import necessary libraries
import streamlit as st
import json
import pandas as pd
import matplotlib.pyplot as plt

# Paths to JSON files
EXPENSES_FILE = "data/expenses.json"
SAVINGS_FILE = "data/savings.json"
GOALS_FILE = "data/goals.json"  # For tracking goals

# A simple class to manage savings and expenses
class SavingsManager:
    def __init__(self, expenses_file, savings_file):
        self.expenses_file = expenses_file
        self.savings_file = savings_file
        self.expenses = self.load_data(expenses_file, [])
        self.savings = self.load_data(savings_file, {"total_savings": 0, "history": []})

    # Load data from a JSON file
    def load_data(self, file_path, default):
        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return default

    # Save updated data to a JSON file
    def save_data(self, file_path, data):
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

    # Update savings and add to history
    def add_savings(self, amount):
        if amount > 0:
            self.savings["total_savings"] += amount
            self.savings["history"].append({"date": pd.Timestamp.now().strftime("%Y-%m-%d"), "amount": self.savings["total_savings"]})
            self.save_data(self.savings_file, self.savings)

    # Get total savings
    def get_total_savings(self):
        return self.savings["total_savings"]

    # Get savings history as a DataFrame
    def get_savings_history(self):
        return pd.DataFrame(self.savings.get("history", []))

    # Calculate total spending
    def get_total_expenses(self):
        return sum(exp["amount"] for exp in self.expenses)

    # Calculate spending by category
    def get_category_expenses(self):
        expenses_df = pd.DataFrame(self.expenses)
        return expenses_df.groupby("category")["amount"].sum().to_dict() if not expenses_df.empty else {}

# Check if goals are on track
def check_goals(manager):
    goals = manager.load_data(GOALS_FILE, [])
    results = []

    for goal in goals:
        target = goal.get("target", 0)
        saved = manager.get_total_savings()
        if saved >= target:
            results.append(f"🎉 Goal '{goal['name']}' is complete!")
        else:
            remaining = target - saved
            progress = (saved / target) * 100
            results.append(f"Goal '{goal['name']}' is {progress:.1f}% complete. {remaining} left to save.")
    return results

# Display charts and goal tracking
def show_charts(manager):
    st.header("📊 Charts")

    col1, col2 = st.columns(2)

    # Savings vs. Spending chart
    with col1:
        st.subheader("Savings vs. Spending")
        savings = manager.get_total_savings()
        expenses = manager.get_total_expenses()
        show_pie_chart(savings, expenses)

    # Savings over time chart
    with col2:
        st.subheader("Savings Over Time")
        savings_history = manager.get_savings_history()
        if not savings_history.empty:
            fig, ax = plt.subplots()
            ax.plot(pd.to_datetime(savings_history["date"]), savings_history["amount"], marker="o", linestyle="-", color="#93ccea")
            ax.set_title("Savings Growth")
            ax.set_xlabel("Date")
            ax.set_ylabel("Savings")
            plt.xticks(rotation=45)
            st.pyplot(fig)
        else:
            st.info("No savings history yet.")

    # Goal tracking below charts
    st.subheader("🎯 Goal Tracking")
    goals = check_goals(manager)
    if goals:
        for goal in goals:
            st.write(goal)
    else:
        st.info("No goals set yet. Add some in the Goals tab.")

# Show pie chart for savings and spending
def show_pie_chart(savings, expenses):
    data = {"Savings": savings, "Spending": expenses}
    labels = list(data.keys())
    values = list(data.values())
    colors = ["#a5d6a7", "#ef9a9a"]  # Soft green and red

    if sum(values) > 0:
        fig, ax = plt.subplots()
        ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90, colors=colors)
        ax.axis("equal")
        st.pyplot(fig)
    else:
        st.info("No data to show yet.")

# Display the My Savings tab
def show_savings(manager):
    st.header("💰 My Savings")

    # Total savings
    total_savings = manager.get_total_savings()
    st.write(f"**Total Savings**: {total_savings}")

    # Add to savings
    add_amount = st.number_input("Add to Savings", min_value=0.0, step=10.0)
    if st.button("Update Savings"):
        manager.add_savings(add_amount)
        st.success(f"Added {add_amount}. Total savings now: {manager.get_total_savings()}.")

    # Show total expenses
    st.subheader("Your Spending")
    total_expenses = manager.get_total_expenses()
    st.write(f"**Total Expenses**: {total_expenses}")

    # Tip for leftover money
    st.info("Tip: If you have leftover money after resetting your budget, add it here as savings!")

    # Reminder for budget reset
    today = pd.Timestamp.now()
    if today.day == 1:
        st.warning("Reminder: Reset your monthly budget in the Budget Mastery tab.")

# Main function for Savings Vault
def display_savings():
    st.title("🏦 Savings Vault")
    st.write("Track your savings, spending, and goals here.")

    # Navigation bar
    selected = st.sidebar.radio("Select a tab", ["My Savings", "Charts"])

    # Initialize manager
    manager = SavingsManager(EXPENSES_FILE, SAVINGS_FILE)

    # Route to selected tab
    if selected == "My Savings":
        show_savings(manager)
    elif selected == "Charts":
        show_charts(manager)