import streamlit as st
from openai import OpenAI
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set up OpenAI API key
client = OpenAI(api_key="my-api")

# Title and introduction
st.title("AI Assistant for Water Conservation")
st.write("This assistant provides real-time feedback, tips, analytics, and cost-saving insights to help you conserve water at home.")

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

# Added feature: Trend visualization with synthetic data
st.subheader("Water Usage Trends")
dates = pd.date_range(start="2024-01-01", periods=30)
synthetic_data = np.random.randint(50, 150, size=(30,))
trend_df = pd.DataFrame({"Date": dates, "Daily Usage (L)": synthetic_data})

# Plot using matplotlib
fig, ax = plt.subplots()
ax.plot(trend_df["Date"], trend_df["Daily Usage (L)"], color='blue', marker='o', linestyle='-')
ax.set_title("Synthetic Daily Water Usage Over 30 Days")
ax.set_xlabel("Date")
ax.set_ylabel("Water Usage (L)")
ax.grid(True)
st.pyplot(fig)

st.write("This chart shows a simulated trend of daily water usage. Try to spot patterns and adjust habits accordingly!")

# Feature 2: Personalized Tips and Recommendations
st.header("2. Personalized Tips for Reducing Water Use")

# Enhanced prompt for OpenAI to improve response quality
def get_personalized_tips(activity, current_usage, model="gpt-4"):
    prompt = (
        f"As an AI focused on water conservation, provide detailed and actionable water-saving tips "
        f"for someone who uses a lot of water in their {activity}. Their current usage is {current_usage} liters. "
        f"Suggest ways to reduce this by at least 20%."
    )
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant focused on water conservation and sustainability."},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content

activity = st.selectbox("Select an activity to get tips:", ["Shower", "Garden", "Car Wash"])
if st.button("Get Tips"):
    current_activity_usage = usage_df.loc[usage_df['Area'] == activity, 'Current Usage (L)'].values[0]
    tips = get_personalized_tips(activity, current_activity_usage)
    st.write(tips)

# Feature 3: Goal Setting, Progress Tracking, and Cost Savings Estimation
st.header("3. Goal Setting, Progress Tracking, and Estimated Savings")

# Set a goal for daily water usage reduction
daily_goal = st.slider("Set your daily water usage reduction goal (liters):", 0, 50, 10)
st.write(f"Your goal is to reduce daily water usage by {daily_goal} liters.")

# Simulate daily usage and cost savings calculation
current_usage = np.random.randint(80, 120)  # Simulated current daily usage
remaining = max(current_usage - daily_goal, 0)
st.write(f"Today's Usage: {current_usage} liters")
st.write(f"Remaining after goal: {remaining} liters")

# Assume a cost per liter (e.g., $0.001 per liter)
cost_per_liter = 0.001
daily_savings = daily_goal * cost_per_liter
monthly_savings = daily_savings * 30  # Projected over a month

st.write(f"Daily Estimated Savings: ${daily_savings:.2f}")
st.write(f"Projected Monthly Savings if goal is met daily: ${monthly_savings:.2f}")

# AI-generated insight about the impact of savings
def get_savings_insight(daily_savings, monthly_savings):
    prompt = (
        f"Given a daily savings of ${daily_savings:.2f} and a monthly savings of ${monthly_savings:.2f}, "
        f"generate a motivational message to encourage the user to continue their water-saving efforts."
    )
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a motivational assistant focused on sustainability."},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content

if st.button("Get Savings Insight"):
    insight = get_savings_insight(daily_savings, monthly_savings)
    st.write(insight)

st.write("Keep up the good work! Every liter saved not only helps the planet but also reduces your bills.")
