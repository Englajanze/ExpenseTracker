# add expenses (catagory, date, amount)
# list expenses based on catagory
# take input of catagory, date and amount
# ensure that it follows validate inputs
import streamlit as st
import json
from datetime import date
import pandas as pd
from streamlit_free_text_select import st_free_text_select
from streamlit_navigation_bar import st_navbar
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt



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

# Display the page where the user can add expenses
def display_expenses():
    st.title("💸 Expense Tracker")
    st.write("Welcome to the Expenses page, choose what you want to do:")
    selected = option_menu(
        menu_title=None,
        options=["Add expenses","View expenses", "Modify", "Visualize"],
        icons=["database-add", "search", "pen", "bar-chart-line"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal"
    )
    if selected == "Add expenses":
        display_add_expenses_form()
    if selected == "View expenses":
        show_my_expenses()
    if selected == "Modify":
        display_and_modifying_expenses()
    if selected == "Visualize":
        expenses_visualizations()





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
def show_my_expenses():
    st.title("DISPLAY YOUR EXPENSES")
    expenses = load_expenses()
    categories = load_categories()

    choose_selected_showing_expenses = st.selectbox("What would you like to display", ("All Expenses", "Category based", "Date based"))

    if choose_selected_showing_expenses == "All Expenses":
        if expenses:
            display_all_expenses = pd.DataFrame(expenses)
            st.dataframe(display_all_expenses)
            # shows the total expenses
            if 'amount' in display_all_expenses.columns:
            # Calculate the total sum of the amount column
                expense_sum_total = display_all_expenses['amount'].sum()
            # Display the total sum
                st.write(f"Total expenses: {expense_sum_total}")

            else:
                st.warning("The 'amount' column is missing from the expenses data.")

    elif choose_selected_showing_expenses == "Category based":
        # Category selection for filtering
        category_selected = st.selectbox("Choose a category", options=["Choose a category"] + categories)

        if category_selected != "Choose a category":
            # Filter the DataFrame based on the selected category
            filtered_expenses = [expense for expense in expenses if expense["category"] == category_selected]

            if filtered_expenses:
                filtered_expenses_df = pd.DataFrame(filtered_expenses)
                st.dataframe(filtered_expenses_df[['amount', 'date', 'category']])
                # shows the amount spent in that category
                if 'amount' in filtered_expenses_df.columns:
                    expense_category_sum = filtered_expenses_df['amount'].sum()
                    st.write(f"Total expenses in {category_selected} is {expense_category_sum}")
                else:
                    st.warning("The amount in {category_selected} is missing from expenses data")


            else:
                st.write(f"No expenses found for the category: {category_selected}")
        else:
            st.write("Please choose a category to filter your expenses.")
    elif choose_selected_showing_expenses == "Date based":
        date_input = st.date_input("Select a date")
        date_input_str = date_input.strftime("%Y-%m-%d")
        if date_input:

        #if date_input != "Select a date":
            filter_expenses_date = [expense for expense in expenses if expense["date"] == date_input_str]

            if filter_expenses_date:
                filtered_expenses_date_df = pd.DataFrame(filter_expenses_date)
                st.dataframe(filtered_expenses_date_df[["amount", "date", "category"]])
                # display the total amount spent on that specific date
                if 'amount' in filtered_expenses_date_df.columns:
                    expense_date_sum = filtered_expenses_date_df['amount'].sum()
                    st.write(f"Total expenses on {date_input_str} is {expense_date_sum}")

                else:
                    st.warning(f"The amount in {date_input_str} is missing from expenses data")
            else:
                st.write("no expenses found on the specific date")
        else:
            st.write("please choose a date to filter")

    else:
        st.write("no expenses recorded yet")

# this function will make it possible to edit or delete past expenses, this will update the JSON file
def display_and_modifying_expenses():
    st.title("Modify your expenses")
    expenses = load_expenses()  # Load expenses from the JSON file
    categories = load_categories()  # Load categories from the categories file

    if expenses:
        expenses_modifying_df = pd.DataFrame(expenses)
        expenses_modifying_df['date'] = pd.to_datetime(expenses_modifying_df['date'], errors='coerce')

        # Add a 'Select' column for deletion purposes
        expenses_modifying_df['Select'] = False

        column_config = {
            'Select': st.column_config.CheckboxColumn(label='Select for Deletion'),
            'amount': st.column_config.NumberColumn(label='Amount', min_value=0),
            'date': st.column_config.DateColumn(label='Date'),
            'category': st.column_config.SelectboxColumn(label='Category', options=categories)
        }

        # Display the data editor for modifying expenses
        edited_df = st.data_editor(
            expenses_modifying_df,
            column_config=column_config,
            num_rows="fixed",  # Prevent adding new rows
            hide_index=True  # Hide the index column
        )

        # Handle the "Commit changes" button when the user wants to save changes
        if st.button("Commit changes"):
            # Step 1: Handle deletions by removing selected rows from the original expenses list
            rows_to_delete = edited_df[edited_df['Select']].index
            if not rows_to_delete.empty:
                # Remove the selected rows from the original expenses list
                expenses = [expense for i, expense in enumerate(expenses) if i not in rows_to_delete]
                st.success(f"Deleted {len(rows_to_delete)} expense(s) successfully!")

            # Step 2: Handle edits by updating only the modified fields (amount and category)
            # Since rows were deleted, we need to make sure we are working with the updated expenses list
            for index, row in edited_df.iterrows():
                # If the row is selected for deletion, skip it
                if row['Select']:
                    continue

                # Find the corresponding expense in the original list to modify
                # Adjust the index due to deletion shifting the rows
                adjusted_index = index if index < len(expenses) else index - len(rows_to_delete)
                expense_to_modify = expenses[adjusted_index]

                # Check if there's a change in 'amount' or 'category' and update the corresponding field
                if row['amount'] != expense_to_modify['amount']:
                    expense_to_modify['amount'] = row['amount']  # Update the amount
                if row['category'] != expense_to_modify['category']:
                    expense_to_modify['category'] = row['category']  # Update the category

            # Step 3: Save the entire updated list (including both modified and unmodified expenses)
            save_expenses(expenses)  # Save the full list back to the JSON file
            st.success("Changes saved successfully!")

        # Display the updated DataFrame
        st.dataframe(expenses)
    else:
        st.write("No expenses to display yet.")

def expenses_visualizations():
    expenses = load_expenses()
    categories = load_categories()

    st.subheader("hello, here you will be able to visualize your spending trends, choose how you would like to display your expense trends")
    # Sample data
    column_user_input, column_displaying_vizuals = st.columns([1,2], border=True)
    with column_user_input:
        st.header("Displaying options")
        chart_type = st.selectbox("Select Chart type:", ["📈 Line chart", "🍰 Pie chart", "📊 Bar chart"])
        time_groupings = st.selectbox("Select your groupings:", ["Daily", "Weekly", "Montly", "Yearly"])
        date_range = st.date_input("Select a date range",value=(pd.to_datetime('2024-01-01'), pd.to_datetime('2024-01-02')), max_value = "today")
        if len(date_range) == 2:
            start_date, end_date = date_range
                # Display the selected date range
        else:
            st.write("Please select both start and end dates.")

        categories_displayed = st.selectbox("What expense categories would you like to display?", options=["All"] + categories)


    with column_displaying_vizuals:
        st.header("Your visuals")



# run a function for adding expenses
# the function should add amount, catagory and date
# there should be prefixed catagories, but you can also add new
# if you add a new catagory it should be saved in the json file and shown in the list when you do it agian
# the expenses should be added in the json file with the amount, date and catagory

