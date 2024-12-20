# set and track montly/weekly budget
# check remaining budget and daily spending cap
import streamlit as st
import json
import expenses


CATEGORY_FILE = "data/expensecatagories.json"

def load_categories():
    try:
        with open(CATEGORY_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return ["Food", "Transport", "Entertainment", "Other"]

def display_budget():
    st.title("💰 Budget Mastery")
    st.write("Welcome to the Budget Mastery page!")
    income_input = total_income_budget()
    category_budget_divisions(income_input)

# this funtion lets the user input their total income
def total_income_budget():
    st.subheader("Here you can insert your income and plan your budget")
    income_input = st.number_input("Please insert your total income here:", min_value=0, step=10)
    return income_input

# this function lets the user divide up the income into a budgeting, based on the categories existing in the categories.json file
def category_budget_divisions(income_input):
    categories = load_categories()
    st.subheader("Please select how you want to divide your income in the different categories")
    total_sum_budgeting = 0
    # displays all categories that exists in the expensescategories.json file
    # calculates the total cetgory budgeting for every input
    for category in categories:
        category_inputs = st.number_input(f"Insert how much you want to budget for {category}", min_value=0, step=10)
        total_sum_budgeting += category_inputs
    remaining_budget = income_input - total_sum_budgeting
    if income_input < total_sum_budgeting:
        st.error("negative")
    else:
        st.write(f"Your total budgeting by categories is now {total_sum_budgeting}")
        st.write(f"your remaining budget is {remaining_budget}")

def remaining_all_budget_by_expenses():
    total_remaining = income_input - expenses


if __name__ == "__main__":
    display_budget()



