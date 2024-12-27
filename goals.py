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
    st.write("Welcome to the Goals page, set up and track your goals!")
    set_up_goals()

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


