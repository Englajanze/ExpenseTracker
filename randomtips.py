# generate random saving tips for the user
import random


import streamlit as st


def display_random_tips():
    st.title("💡 Money Hacks")
    st.write("Click the button below to get a new random tip!")

    if st.button("Generate Tip"):
        tip = random.choice(saving_tips)
        st.info(tip)





saving_tips = [
    "Skip the café – brew your coffee at home and save 100kr per week!",
    "Challenge yourself: 'No Spend Weekends' – fun doesn't have to cost a dime!",
    "Bring your lunchbox to work and save enough for a weekend dinner out.",
    "Unsubscribe from one streaming service for a month – Netflix isn't going anywhere.",
    "Set a timer when shopping online. If you still want it in 24 hours, buy it.",
    "Use a 'one in, one out' rule: sell something before buying something new.",
    "Turn saving into a game: save 20kr every time you skip an impulse buy.",
    "Create a DIY spa night at home instead of going to the salon.",
    "Host a clothing swap with friends – save money and freshen up your wardrobe.",
    "Cook a 'Leftover Mystery Meal' once a week – turn scraps into a creative dinner!",
    "Cut back on energy costs: turn off lights, unplug devices, and layer up indoors.",
    "Use public transport or carpool – your wallet (and the planet) will thank you!",
    "Every time you crave takeout, transfer that money to your savings instead.",
    "Do a 'Pantry Challenge': eat only what's in your kitchen for a week.",
    "DIY gifts are heartfelt and cheap – make a photo album or bake cookies!",
    "Take free online classes instead of paying for hobbies or workshops.",
    "Track every expense for a month – the results may shock (and motivate) you!",
    "Make coffee dates at home with friends instead of expensive brunches.",
    "Cancel subscriptions you don't use – do you really need three fitness apps?",
    "Use cash-only for a week and leave your card at home – goodbye overspending!"
]


