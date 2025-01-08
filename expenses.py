# Import necessary libraries
import streamlit as st
import json
import pandas as pd
from streamlit_free_text_select import st_free_text_select
from streamlit_option_menu import option_menu
from datetime import date

# Paths to JSON files
EXPENSES_FILE = "data/expenses.json"  # File to store expenses
CATEGORY_FILE = "data/expensecatagories.json"  # File to store categories

# Manage expenses and categories
class ExpenseManager:
    def __init__(self, expenses_file, categories_file):
        # Load files on initialization
        self.expenses_file = expenses_file
        self.categories_file = categories_file
        self.expenses = self.load_file(self.expenses_file, [])
        self.categories = self.load_file(self.categories_file, ["Food", "Transport", "Entertainment", "Other"])

    # Load JSON data from a file
    def load_file(self, file_path, default):
        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return default

    # Save JSON data to a file
    def save_file(self, file_path, data):
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

    # Add an expense and save it
    def add_expense(self, amount, category, date):
        self.expenses.append({"amount": amount, "category": category, "date": str(date)})
        self.save_file(self.expenses_file, self.expenses)

    # Add a category if it doesn't already exist
    def add_category(self, category):
        if category not in self.categories:
            self.categories.append(category)
            self.save_file(self.categories_file, self.categories)

    # Filter expenses by category
    def filter_by_category(self, category):
        return [expense for expense in self.expenses if expense["category"] == category]

    # Filter expenses by date
    def filter_by_date(self, selected_date):
        return [expense for expense in self.expenses if expense["date"] == selected_date]

    # Get total expenses
    def total_expenses(self):
        return sum(expense["amount"] for expense in self.expenses)

    # Get total expenses grouped by category
    def expenses_by_category(self):
        totals = {}
        for expense in self.expenses:
            totals[expense["category"]] = totals.get(expense["category"], 0) + expense["amount"]
        return totals


# Main function to display the expense tracker
def display_expenses():
    st.title("💸 Expense Tracker")
    st.write("Track your expenses, add new ones, and modify existing records.")

    # Initialize manager
    manager = ExpenseManager(EXPENSES_FILE, CATEGORY_FILE)

    # Navigation menu
    selected = option_menu(
        menu_title=None,
        options=["Add expenses", "View expenses", "Modify"],
        icons=["plus-circle", "eye", "pencil"],
        default_index=0,
        orientation="horizontal",
    )

    # Load relevant sections
    if selected == "Add expenses":
        add_expenses(manager)
    elif selected == "View expenses":
        view_expenses(manager)
    elif selected == "Modify":
        modify_expenses(manager)


# Add a new expense
def add_expenses(manager):
    st.subheader("Add a new expense")

    # Form for input
    with st.form("expense_form"):
        amount = st.number_input("Amount", min_value=0.0, step=0.01, format="%.2f")
        date_selected = st.date_input("Date", value=date.today())
        category = st_free_text_select(
            "Category",
            options=manager.categories,
            placeholder="Select or add a category",
        )

        # Submit button
        submitted = st.form_submit_button("Add Expense")
        if submitted:
            if amount <= 0:
                st.error("Please enter a valid amount.")
            else:
                manager.add_category(category)  # Add category if new
                manager.add_expense(amount, category, date_selected)
                st.success(f"Added: {amount} to '{category}' on {date_selected}.")


# View expenses (all, by category, or by date)
def view_expenses(manager):
    st.subheader("View Expenses")

    # Selection option
    view_option = st.selectbox(
        "View by", ["All Expenses", "Category", "Date"]
    )

    # Show all expenses
    if view_option == "All Expenses":
        st.write("All Expenses")
        if manager.expenses:
            st.dataframe(pd.DataFrame(manager.expenses))
            st.write(f"Total: {manager.total_expenses()}")
        else:
            st.info("No expenses recorded.")

    # Show expenses by category
    elif view_option == "Category":
        category = st.selectbox("Select a category", manager.categories)
        filtered = manager.filter_by_category(category)
        if filtered:
            st.dataframe(pd.DataFrame(filtered))
            total = sum(exp["amount"] for exp in filtered)
            st.write(f"Total in '{category}': {total}")
        else:
            st.info(f"No expenses in category '{category}'.")

    # Show expenses by date
    elif view_option == "Date":
        selected_date = st.date_input("Select a date")
        filtered = manager.filter_by_date(str(selected_date))
        if filtered:
            st.dataframe(pd.DataFrame(filtered))
            total = sum(exp["amount"] for exp in filtered)
            st.write(f"Total on {selected_date}: {total}")
        else:
            st.info(f"No expenses on {selected_date}.")


# Modify or delete expenses
def modify_expenses(manager):
    st.subheader("Modify Expenses")

    # Check if expenses exist
    if manager.expenses:
        # Display as editable table
        expenses_df = pd.DataFrame(manager.expenses)
        expenses_df["Delete"] = False
        edited_df = st.data_editor(expenses_df, num_rows="dynamic", hide_index=True)

        # Save changes button
        if st.button("Save Changes"):
            # Filter out rows marked for deletion
            updated_expenses = edited_df[~edited_df["Delete"]].to_dict("records")
            manager.expenses = updated_expenses
            manager.save_file(EXPENSES_FILE, updated_expenses)
            st.success("Expenses updated successfully!")
    else:
        st.info("No expenses available to modify.")
        