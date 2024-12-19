# main page, connect all files here
# should contain a meny where user can choose to display
# add expenses, view expenses, view budget, view spending trends, view savings, set or view goals

import streamlit as st
from budget import display_budget
from expenses import display_expenses
from goals import display_goals
from randomtips import display_random_tips
from savings import display_savings
from visualization import display_visualization

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Choose a page",
    [
        "📂 Dashboard",  # Default page
        "💰 Budget Mastery",
        "💸 Expense Tracker",
        "🎯 Achieve Goals",
        "💡 Money Hacks",
        "🏦 Savings Vault",
        "📊 Insights & Charts",
    ],
    index=0  # Set the default to the first option
)

# Load the corresponding page based on selection
if page == "📂 Dashboard":
    st.title("📂 Dashboard")
    st.write("Welcome to your dashboard! We are here for you to make sure you follow and track your expenses, we know how hard it can be!")
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
    display_visualization()







