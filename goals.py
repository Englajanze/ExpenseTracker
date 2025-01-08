# user can set goals and track progress
import streamlit as st
import json

EXPENSES_FILE = "data/expenses.json"
CATEGORY_FILE = "data/expensecatagories.json"

# Function to load expenses from the JSON file

def load_expenses():
    try:
        with open(EXPENSES_FILE, "r") as file:
            content = file.read().strip()
            if content:
                return json.loads(content)
            else:
                return []  # Return an empty list if the file is empty
    except FileNotFoundError:
        return []  # Return an empty list if the file doesn't exist
    except json.JSONDecodeError:
        st.error(f"Error decoding JSON from {EXPENSES_FILE}. Please check the file's content.")
        return []
# Function to save expenses back to the JSON file
def save_expenses(expenses):
    with open(EXPENSES_FILE, "w") as file:
        json.dump(expenses, file, indent=4)

# Function to load categories from the JSON file
def load_categories():
    try:
        with open(CATEGORY_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return ["Food", "Transport", "Entertainment", "Other"]  # Default categories if the file doesn't exist

# Function to save new categories to the JSON file
def save_categories(categories):
    with open(CATEGORY_FILE, "w") as file:
        json.dump(categories, file, indent=4)

def display_goals():
    st.title("🎯 Achieve Goals")
    st.subheader("Welcome to the Goals page, set up and track your goals!")
    set_up_goals()
    st.write("---")  # Divider line
    display_goal_calculator()  

def set_up_goals():
    categories = load_categories()
    expenses = load_expenses()
    goal_type = st.selectbox(
    "Step 1 to create your goals",
    ("Save money", "Spend less in specific category"),
    index=None,
    placeholder="Select your type of goal...",)

    if goal_type == "Save money":
        saving_goal_name = st.text_input("Enter the name of your goal here:")
        saving_goal_amount = st.number_input("How much would you like to save?")
        saving_goal_end_date = st.date_input("Enter when your goal should be reached")
    elif goal_type == "Spend less in specific category":
        spend_less_category = st.selectbox("In what category would you like to focus on?", options = categories)
        spend_less_goal_name = st.text_input("Enter the name of your goal here:")
        spend_less_goal_amount = st.number_input("How much would you like to save?")
        spend_less_goal_end_date = st.date_input("Enter when your goal should be reached")

# A goal/budget calculator to help users figure out their goals
def display_goal_calculator():
    st.subheader("Need help figuring how much your saving goal?")
    st.write("Use the calculator below to set your savings goal or get a general budget plan.")

    # Savings goal projection
    st.write("Savings Goal Calculator")
    monthly_saving = st.number_input(
        "How much would you like to save each month?", min_value=0.0, step=1.0
    )
    if monthly_saving > 0:
        st.write("Projected Savings:")
        for months in [3, 6, 12, 18, 24]:
            st.write(f"{months} months: {monthly_saving * months}")
    else:
        st.write("Enter a monthly savings amount to calculate projections.")

    # Budget planner
    st.write("Budget Planner")
    total_budget = st.number_input(
        "What is your total budget goal?", min_value=0.0, step=1.0
    )
    if total_budget > 0:
        st.write("Monthly Breakdown:")
        for months in [6, 12, 18, 24]:
            st.write(f"{months} months: {total_budget / months:.2f} per month")
    else:
        st.write("Enter a total budget goal to see the breakdown.")

#Thought this would be a cool addition? 
#I'll try and replicate the expenses.py navigation bar here so that I can make the savings.py file more interactive as well as implemement the note you had on savings.py as well :)