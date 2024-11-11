import streamlit as st
import pandas as pd
import numpy as np
import random
import openai

# Set up OpenAI API key
openai.api_key = "my-api-key"  # Replace with your actual API key

# Load or generate synthetic data
@st.cache_data
def generate_synthetic_data():
    num_households = 100
    np.random.seed(42)

    # Generate household data
    household_ids = range(1, num_households + 1)
    household_sizes = np.random.normal(loc=2.6, scale=0.5, size=num_households).round().astype(int)
    household_sizes = np.clip(household_sizes, 1, None)

    # Generate daily water usage
    daily_usage_per_person = np.random.normal(loc=90, scale=10, size=num_households).round().astype(int)
    total_daily_usage = household_sizes * daily_usage_per_person

    # Generate shower water usage
    shower_usage_per_person = np.random.normal(loc=17.2, scale=2, size=num_households).round(1)
    total_shower_usage = household_sizes * shower_usage_per_person

    # Generate laundry water usage
    laundry_usage = np.random.normal(loc=30, scale=5, size=num_households).round(1)  # Gallons per load
    avg_weekly_laundry = np.random.randint(3, 7, size=num_households)  # Loads per week
    total_laundry_usage = (laundry_usage * avg_weekly_laundry / 7).round(1)  # Daily average

    # Generate dishwashing water usage
    dishwashing_usage = np.random.normal(loc=6, scale=1, size=num_households).round(1)  # Gallons per load
    avg_daily_dishwashing = np.random.randint(1, 3, size=num_households)  # Loads per day
    total_dishwashing_usage = (dishwashing_usage * avg_daily_dishwashing).round(1)

    # Generate car wash water usage
    car_wash_usage_per_wash = np.random.uniform(40, 70, size=num_households)  # Gallons per wash
    car_washes_per_month = np.random.randint(1, 5, size=num_households)  # 1-4 washes per month
    total_car_wash_usage_monthly = car_wash_usage_per_wash * car_washes_per_month  # Total gallons per month
    avg_daily_car_wash_usage = (total_car_wash_usage_monthly / 30).round(1)  # Convert to daily average

    # Create DataFrame
    data = {
        'Household_ID': household_ids,
        'Household_Size': household_sizes,
        'Daily_Usage_Per_Person_Gallons': daily_usage_per_person,
        'Total_Daily_Usage_Gallons': total_daily_usage,
        'Shower_Usage_Per_Person_Gallons': shower_usage_per_person,
        'Total_Shower_Usage_Gallons': total_shower_usage,
        'Laundry_Usage_Gallons': total_laundry_usage,
        'Dishwashing_Usage_Gallons': total_dishwashing_usage,
        'Car_Wash_Usage_Daily_Avg_Gallons': avg_daily_car_wash_usage  # New column for car wash
    }
    return pd.DataFrame(data)

data = generate_synthetic_data()

# Pool of predefined recommendations
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

# OpenAI API function for dynamic tips
def get_openai_tip(activity, avg_usage):
    prompt = f"Provide a water-saving tip for {activity} based on an average daily water usage of {avg_usage:.2f} gallons."
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Error fetching OpenAI tip: {e}"

# Add custom CSS styling
st.markdown(
    """
    <style>
    h1 {
        color: #2196F3; /* Blue */
    }
    h2 {
        color: #4CAF50; /* Green */
    }
    .stButton>button {
        background-color: #4CAF50; /* Green */
        color: white;
        border-radius: 5px;
        border: none;
        font-size: 16px;
        padding: 8px 12px;
    }
    .stButton>button:hover {
        background-color: #2196F3; /* Blue */
    }
    .stMetric-label {
        color: #4CAF50; /* Matches button */
        font-size: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# App Layout
st.title("AI Assistant for Water Conservation")
st.write("Get personalized insights, tips, and analytics to conserve water in your household.")

# Tabs for navigation
tabs = st.tabs(["Real-Time Feedback", "Recommendations", "Savings Calculator"])

# Tab 1: Real-Time Feedback
with tabs[0]:
    st.header("Real-Time Water Usage Feedback")
    st.write("This data shows **daily water usage** for key areas in your home.")

    fixture = st.selectbox("Select a fixture to find the average water usage:", 
                           ["Shower", "Garden", "Car Wash", "Laundry", "Dishwashing"])
    
    def get_csv_insights(fixture):
        fixture_mapping = {
            "Shower": "Shower_Usage_Per_Person_Gallons",
            "Garden": "Total_Daily_Usage_Gallons",  # Placeholder
            "Car Wash": "Car_Wash_Usage_Daily_Avg_Gallons",  # Updated for daily average
            "Laundry": "Laundry_Usage_Gallons",
            "Dishwashing": "Dishwashing_Usage_Gallons"
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
    st.write("Here are some specific tips to help you save water:")

    activity = st.selectbox("Select an activity to get tips:", 
                            ["Shower", "Garden", "Car Wash", "Laundry", "Dishwashing"])
    
    if st.button("Show Recommendations"):
        avg_usage = get_csv_insights(activity)
        tips = random.sample(recommendations[activity], k=min(2, len(recommendations[activity])))
        openai_tip = get_openai_tip(activity, avg_usage)
        
        for tip in tips:
            st.write(f"- {tip}")
        st.write(f"- {openai_tip}")

# Tab 3: Savings Calculator
with tabs[2]:
    st.header("Savings Calculator")
    st.write("Estimate your savings by implementing specific water-saving measures.")

    options = {
        "Install low-flow showerheads (save ~10 gallons/day)": 10,
        "Upgrade to a high-efficiency washer (save ~15 gallons/load)": 15,
        "Use drip irrigation for gardens (save ~20 gallons/day)": 20
    }
    selected_options = st.multiselect("Select measures you plan to implement:", list(options.keys()))
    total_savings = sum(options[option] for option in selected_options)

    st.write(f"### Total Estimated Savings: {total_savings} gallons/day")
    st.write(f"### Potential Cost Savings: ${total_savings * 0.01065:.2f} per day")
