# Import necessary libraries
import streamlit as st
import json
import pandas as pd
import matplotlib.pyplot as plt

# Paths to JSON files
SAVINGS_FILE = "data/savings.json"

# Function to load data from a file or use default values
def load_data(file_path, default):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return default

# Function to save data to a file
def save_data(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

# Ensure the savings file is initialized with default values
def initialize_savings_file():
    default_savings = {"total_savings": 0, "history": []}
    current_savings = load_data(SAVINGS_FILE, default_savings)
    if "total_savings" not in current_savings:
        current_savings["total_savings"] = 0
    if "history" not in current_savings:
        current_savings["history"] = []
    save_data(SAVINGS_FILE, current_savings)

# Add savings and update total
def add_savings(amount):
    savings = load_data(SAVINGS_FILE, {"total_savings": 0, "history": []})
    if amount > 0:
        savings["total_savings"] += amount
        savings["history"].append({"date": pd.Timestamp.now().strftime("%Y-%m-%d"), "amount": savings["total_savings"]})
        save_data(SAVINGS_FILE, savings)

# Display savings data
def get_total_savings():
    savings = load_data(SAVINGS_FILE, {"total_savings": 0, "history": []})
    return savings.get("total_savings", 0)

def get_savings_history():
    savings = load_data(SAVINGS_FILE, {"total_savings": 0, "history": []})
    return pd.DataFrame(savings.get("history", []))

# Add Savings Page
def display_add_savings():
    st.subheader("Add to Your Savings")
    add_amount = st.number_input("Enter the amount to add:", min_value=0.0, step=10.0)
    if st.button("Add Savings"):
        add_savings(add_amount)
        st.success(f"Added {add_amount}! Your new total savings: {get_total_savings()}")

# View Savings Page
def display_view_savings():
    st.subheader("View Your Savings")
    total_savings = get_total_savings()
    st.write(f"**Total Savings**: {total_savings}")

    savings_history = get_savings_history()
    if not savings_history.empty:
        st.subheader("Savings History")
        st.dataframe(savings_history)
    else:
        st.info("No savings history yet.")

# Savings Charts Page
def display_charts():
    st.subheader("Savings Over Time")
    savings_history = get_savings_history()
    if not savings_history.empty:
        fig, ax = plt.subplots()
        ax.plot(pd.to_datetime(savings_history["date"]), savings_history["amount"], marker="o", linestyle="-", color="green")
        ax.set_title("Savings Growth")
        ax.set_xlabel("Date")
        ax.set_ylabel("Savings")
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.info("No savings history yet. Start saving to see your progress!")

# Main Savings Vault Function
def display_savings():
    st.title("💰 Savings Vault")
    st.write("Track your savings here. Add savings, view your progress, and see detailed charts.")

    # Initialize savings file
    initialize_savings_file()

    # Navigation bar for savings tabs
    selected = st.selectbox(
        "What would you like to do?",
        ["Add Savings", "View Savings", "Charts"]
    )

    if selected == "Add Savings":
        display_add_savings()
    elif selected == "View Savings":
        display_view_savings()
    elif selected == "Charts":
        display_charts()
