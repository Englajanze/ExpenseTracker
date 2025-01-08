# main page, connect all files here
# should contain a meny where user can choose to display
# add expenses, view expenses, view budget, view spending trends, view savings, set or view goals



#importing libraries needed
import streamlit as st
from budget import display_budget
from expenses import display_expenses
from goals import display_goals
from randomtips import display_random_tips
from savings import display_savings
from visualization import display_visualizations

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Choose a page",
    [
        "📂 Dashboard",  # The first (home) page of the program
        "💰 Budget Mastery",
        "💸 Expense Tracker",
        "🎯 Achieve Goals",
        "💡 Money Hacks",
        "🏦 Savings Vault",
        "📊 Insights & Charts",
    ],
    index=0  # Set the default so when entering the program you arrive at dashboard
)

# Loading the correct file when side bar navigation is choicen
if page == "📂 Dashboard":
    st.title("📂 Dashboard")
    st.write("Welcome to your dashboard! We are here for you to make sure you follow and track your expenses, we know how hard it can be!")
    # have some top metrics shown like total spendings, total savings, last added expense, remaning of total budget for the month
    # lates months spending trends as visuals
elif page == "💰 Budget Mastery":
    display_budget()
elif page == "💸 Expense Tracker":
    display_expenses()
elif page == "🎯 Achieve Goals":
    display_goals()
elif page == "💡 Money Hacks":
    display_random_tips()
elif page == "🏦 Savings Vault":
    display_savings()
elif page == "📊 Insights & Charts":
    display_visualizations()



# todolist
# Have to have classes somewhere in the code!
# fox the goals, can be that the user can only say they want to save total 300kr in 3 months and then keep track, not specified in categories or anything
# fix a nice dashboard, interactive with bits and peices of information across the website
# being able to track the budget
# somehow resetting budget every month, but still keeping past expenses
# the income money that is left should be sent into savings at the end of every month
# visualize the budgeting
# display the savings, in both total and in categories (for example specific for the goals)




