import streamlit as st
import pandas as pd
import numpy as np
import random
import openai
import os
import altair as alt

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")  # Replace with your actual API key

# Load or generate synthetic data
@st.cache_data
def generate_synthetic_data():
    num_households = 100
    np.random.seed(42)

    # Generate household data
    household_ids = range(1, num_households + 1)
    household_sizes = np.random.normal(loc=2.6, scale=0.5, size=num_households).round().astype(int)
    household_sizes = np.clip(household_sizes, 1, None)

    # Generate fixture-specific water usage data
    shower_usage = np.random.normal(loc=25, scale=5, size=num_households).round().astype(int)  # Gallons per day
    laundry_usage = np.random.normal(loc=30, scale=8, size=num_households).round().astype(int)
    dishwashing_usage = np.random.normal(loc=12, scale=3, size=num_households).round().astype(int)
    garden_usage = np.random.normal(loc=40, scale=15, size=num_households).round().astype(int)
    car_wash_usage = np.random.normal(loc=15, scale=5, size=num_households).round().astype(int)

    # Calculate total daily usage as a sum of all fixtures
    total_daily_usage = shower_usage + laundry_usage + dishwashing_usage + garden_usage + car_wash_usage

    # Add Zip Codes
    zip_codes = np.random.choice(["90001", "90002", "90003", "90004"], size=num_households)
    
    # Create DataFrame
    data = {
        'Household_ID': household_ids,
        'Zip_Code': zip_codes,
        'Household_Size': household_sizes,
        'Shower_Usage_Gallons': shower_usage,
        'Laundry_Usage_Gallons': laundry_usage,
        'Dishwashing_Usage_Gallons': dishwashing_usage,
        'Garden_Usage_Gallons': garden_usage,
        'Car_Wash_Usage_Gallons': car_wash_usage,
        'Total_Daily_Usage_Gallons': total_daily_usage,
    }
    return pd.DataFrame(data)

data = generate_synthetic_data()

# Recommendations
recommendations = {
    "Shower": [
        "Install WaterSense-certified showerheads to reduce water usage without compromising performance.",
        "Keep showers under 5 minutes to save water.",
        "Turn off the water while lathering or shampooing.",
    ],
    "Laundry": [
        "Wash only full loads of laundry to maximize water efficiency.",
        "Upgrade to a high-efficiency washing machine to reduce water and energy usage.",
        "Use the shortest cycle possible for lightly soiled clothes.",
    ],
    "Dishwashing": [
        "Run the dishwasher only when it’s fully loaded.",
        "Use a dishwasher instead of handwashing for better water efficiency.",
        "Scrape food off plates instead of rinsing them under running water before loading into the dishwasher.",
    ],
    "Garden": [
        "Water plants early in the morning or late in the evening to minimize evaporation.",
        "Install a drip irrigation system for targeted watering.",
        "Use mulch around plants to retain soil moisture.",
    ],
    "Car Wash": [
        "Wash your car using a bucket instead of a hose to save water—this can reduce water usage by up to 50%.",
        "Consider using a commercial car wash that recycles water—many use less than 50 gallons per wash.",
        "Limit car washes to once or twice per month to conserve water."
    ]
}

# Real average water usage
average_data = {
    "Region": ["Silicon Valley", "California", "National Average"],
    "Daily Usage (Gallons)": [75, 146, 82]
}
average_usage_df = pd.DataFrame(average_data)

# App Layout
st.title("JadeAI Water Conservation")
st.write("Get personalized insights, tips, and analytics to conserve water in your household.")

# Tabs for navigation
tabs = st.tabs(["Real-Time Feedback", "Recommendations", "Savings Calculator", "Regional Insights"])

# Tab 1: Real-Time Feedback
with tabs[0]:
    st.header("Real-Time Water Usage Feedback")
    st.write("This data shows **daily water usage** for key areas in your home.")

    fixture = st.selectbox("Select a fixture to find the average water usage:", 
                           ["Shower", "Garden", "Car Wash", "Laundry", "Dishwashing"])
    
    def get_csv_insights(fixture):
        fixture_mapping = {
            "Shower": "Shower_Usage_Gallons",
            "Garden": "Garden_Usage_Gallons",
            "Car Wash": "Car_Wash_Usage_Gallons",
            "Laundry": "Laundry_Usage_Gallons",
            "Dishwashing": "Dishwashing_Usage_Gallons",
        }
        column = fixture_mapping.get(fixture)
        avg_usage = data[column].mean()
        return avg_usage

    if st.button("Get Data"):
        avg_usage = get_csv_insights(fixture)
        st.metric(label=f"Average Daily {fixture} Usage", value=f"{avg_usage:.2f} gallons")

# Tab 2: Recommendations
with tabs[1]:
    st.header("Recommendations")
    activity = st.selectbox("Select an activity to get tips:", 
                            ["Shower", "Garden", "Car Wash", "Laundry", "Dishwashing"])
    
    if st.button("Show Recommendations"):
        tips = random.sample(recommendations[activity], k=min(2, len(recommendations[activity])))
        for tip in tips:
            st.write(f"- {tip}")

# Tab 3: Savings Calculator
with tabs[2]:
    st.header("Savings Calculator")
    user_usage = st.number_input("Enter your average daily water usage (gallons):", min_value=0, value=100)

    target_usage = 82  # National average
    if user_usage > target_usage:
        savings = user_usage - target_usage
        cost_savings = savings * 0.01065
        st.write(f"If you reduce your usage to the national average ({target_usage} gallons/day), you could save **{savings} gallons per day**.")
        st.write(f"Potential cost savings: **${cost_savings:.2f} per day**.")
    elif user_usage == target_usage:
        st.write("Great job! You're already using water at the national average level. Keep it up!")
    else:
        savings_below_avg = target_usage - user_usage
        st.write("Excellent! You're already using less water than the national average. Keep conserving!")
        st.write(f"You’re saving approximately **{savings_below_avg} gallons per day** compared to the average household.")
        st.write("Consider sharing your conservation tips with others or finding new ways to optimize even further!")

# Tab 4: Regional Insights
with tabs[3]:
    st.header("Regional Insights")

    # Create an Altair bar chart and customize label colors
    chart = alt.Chart(average_usage_df).mark_bar(color='#008000').encode(
        x=alt.X('Region', sort=None),
        y='Daily Usage (Gallons)'
    ).properties(
        width=600,
        height=400
    ).configure_axis(
        labelColor='#000000',  # Change tick label color (e.g., black)
        titleColor='#000000',   # Change axis title color (e.g., black)
        gridColor='#000000'
    ).configure_view(
        strokeWidth=0  # Optional: Remove the border around the chart
    )

    # Display the chart
    st.altair_chart(chart, use_container_width=True)

    st.write("""
    Californians use significantly more water daily than the national average. 
    Let's work together to lower this number!
    """)

    california_population = 39538223
    potential_savings_statewide = (146 - 82) * california_population
    st.write(f"If all Californians reduced their water usage to the national average, they could save approximately **{potential_savings_statewide:,} gallons of water per day**!")
