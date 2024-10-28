import streamlit as st
import openai
import pandas as pd
import numpy as np
import time

# Set up OpenAI API key
openai.api_key = "my-api-key"

# Title and introduction
st.title("AI Assistant for Water Conservation")

# Feature 1: Real-Time Water Usage Feedback
st.header("1. Real-Time Water Usage Feedback")
st.write("Simulated real-time water usage data for key areas in Bob's home.")

# Generate simulated water usage data
usage_data = {
    "Area": ["Shower", "Garden", "Car Wash"],
    "Current Usage (L)": [np.random.randint(5, 20), np.random.randint(10, 30), np.random.randint(5, 15)]
}
usage_df = pd.DataFrame(usage_data)
st.table(usage_df)

# Feature 2: Personalized Tips and Recommendations
st.header("2. Personalized Tips for Reducing Water Use")

# Prompt OpenAI for personalized water-saving tips
def get_personalized_tips(activity):
    prompt = f"Provide water-saving tips for someone who uses a lot of water in their {activity}."
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100
    )
    return response.choices[0].text.strip()

activity = st.selectbox("Select an activity to get tips:", ["Shower", "Garden", "Car Wash"])
if st.button("Get Tips"):
    tips = get_personalized_tips(activity)
    st.write(tips)

# Feature 3: Goal Setting and Progress Tracking
st.header("3. Goal Setting and Progress Tracking")

# Set a goal for daily water usage reduction
daily_goal = st.slider("Set your daily water usage reduction goal (liters):", 0, 50, 10)
st.write(f"Your goal is to reduce daily water usage by {daily_goal} liters.")

# Simulate tracking progress toward the goal
current_usage = np.random.randint(80, 120)  # Simulated current daily usage
remaining = max(current_usage - daily_goal, 0)
st.write(f"Today's Usage: {current_usage} liters")
st.write(f"Remaining after goal: {remaining} liters")
progress = min(daily_goal / current_usage, 1.0)
st.progress(progress)

st.write("Keep going! Every liter saved makes a difference.")

