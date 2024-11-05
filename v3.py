import streamlit as st
import openai
import pandas as pd
import numpy as np
import os

# Set up OpenAI API key
openai.api_key = ("my-api-key")  # Replace with direct key for testing if needed

# Title and introduction
st.title("AI Assistant for Water Conservation")
st.write("This assistant provides real-time feedback, tips, analytics, and cost-saving insights to help you conserve water at home.")

# Feature 1: Real-Time Water Usage Feedback
st.header("1. Real-Time Water Usage Feedback")
st.write("Simulated real-time water usage data for key areas in Bob's home.")

# Generate simulated water usage data
def get_water_usage_data(fixture):
    prompt = f"Generate a table displaying realistic water usage from one of the three {fixture} in a single-person household, based on the daily average water usage of 65 gallons in Santa Clara, California."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )
    return response.choices[0].message['content'].strip()

# Select a fixture to find average water usage and display data
fixture = st.selectbox("Select a fixture to find the average water usage:", ["Shower", "Garden", "Car Wash"])
if st.button("Get Data"):
    data = get_water_usage_data(fixture)
    st.write(data)

# Feature 2: Personalized Tips and Recommendations
st.header("2. Personalized Tips for Reducing Water Use")

# Get water-saving tips based on activity
def get_personalized_tips(activity):
    tips = {
        "Shower": "To save water when showering, consider using a low-flow showerhead and aiming to make your showers shorter!",
        "Garden": "Water your garden in the early morning to reduce evaporation and consider installing drip irrigation!",
        "Car Wash": "Use a bucket with soapy water and a sponge instead of a hose or attachment; it uses much less water!"
    }
    return tips.get(activity, "Select an activity to receive tips!")
    
activity = st.selectbox("Select an activity to get tips:", ["Shower", "Garden", "Car Wash"])
if st.button("Get Tips"):
    tips = get_personalized_tips(activity)
    st.write(tips)

# Feature 3: Goal Setting, Progress Tracking, and Estimated Savings
st.header("3. Goal Setting, Progress Tracking, and Estimated Savings")

# Set up daily water usage goal and cost calculation
cost_per_liter = 0.002  # Estimated cost per liter in dollars
daily_goal = st.slider("Set your daily water usage reduction goal (liters):", 0, 50, 10)
savings_goal_dollars = daily_goal * cost_per_liter
st.write(f"Goal: Save ${savings_goal_dollars:.2f} per day by reducing water usage.")

# Simulate daily usage and calculate actual savings
current_usage = np.random.randint(80, 120)  # Simulated current daily usage in liters
actual_savings = min(daily_goal, current_usage) * cost_per_liter

st.write(f"Today's Usage: {current_usage} liters")
st.write(f"Actual Savings Today: ${actual_savings:.2f}")
st.progress(actual_savings / savings_goal_dollars if savings_goal_dollars > 0 else 0)

# Generate an AI-based water-saving tip specific to the user's daily goal
def get_savings_insight(daily_goal):
    prompt = f"Provide a tip to help save {daily_goal} liters of water each day."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100
    )
    return response.choices[0].message['content'].strip()

if st.button("Get Savings Insight"):
    tips = get_savings_insight(daily_goal)
    st.write("Water-Saving Tip: ", tips)
