# add expenses (catagory, date, amount)
# list expenses based on catagory
# take input of catagory, date and amount
# ensure that it follows validate inputs
import streamlit as st
import json
from datetime import date
from streamlit_free_text_select import st_free_text_select

EXPENSES_FILE = "data/expenses.json"
CATEGORY_FILE = "data/expensecatagories.json"

# Function to load expenses from the JSON file
def load_expenses():
    try:
        with open(EXPENSES_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []  # Return an empty list if the file doesn't exist

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

# Display the page where the user can add expenses
def display_expenses():
    st.title("💸 Expense Tracker")
    st.write("Welcome to the Expenses page, where you can add your expenses!")
    display_add_expenses_form()
    display_all_expenses()

# Form for adding a new expense
def display_add_expenses_form():
    expenses = load_expenses()
    categories = load_categories()

    st.subheader("Add your expenses here")

    with st.form("add_expenses_form"):
        amount_expense = st.number_input("Amount:", min_value=0.0, step=0.01, format="%.2f")
        date_expense = st.date_input("Date", value=date.today())

        # Category selection with the editable dropdown using st_free_text_select
        category = st_free_text_select(
            label="Category",
            options=categories,
            index=None,
            format_func=lambda x: x.capitalize(),
            placeholder="Select or enter a category",
            disabled=False,
            delay=300,
            label_visibility="visible",
        )

        submit_button = st.form_submit_button("Submit Expense")

        # Handle form submission
        if submit_button:
            if amount_expense <= 0:
                st.error("Please enter a valid amount greater than 0.")
            elif date_expense > date.today():
                st.error("Cannot enter a date in the future.")
            else:
                # If the user typed a new category (not in predefined categories)
                if category not in categories:
                    categories.append(category)  # Add the new category
                    save_categories(categories)  # Save the updated categories

                # Add the expense to the list
                new_expense = {
                    "amount": amount_expense,
                    "date": str(date_expense),
                    "category": category
                }
                expenses.append(new_expense)
                save_expenses(expenses)
                st.success(f"Expense of {amount_expense} added in '{category}' on {date_expense}!")





# function to display all the expenses you have so far




# run a function for adding expenses
# the function should add amount, catagory and date
# there should be prefixed catagories, but you can also add new
# if you add a new catagory it should be saved in the json file and shown in the list when you do it agian
# the expenses should be added in the json file with the amount, date and catagory

