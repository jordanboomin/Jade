import streamlit as st
import openai
import pandas as pd
import numpy as np
import time
import os

# Set up OpenAI API key
openai.api_key = os.environ["OPENAI_API_KEY"]

# Title and introduction
st.title("AI Assistant for Water Conservation")

# Feature 1: Real-Time Water Usage Feedback
st.header("1. Real-Time Water Usage Feedback")
st.write("Simulated real-time water usage data for key areas in Bob's home.")

def get_water_usage_data(fixture):
    prompt = f"Generate a table displaying realistic water usage from the one of the three {fixture} in the small single person household, based on the fact that the daily average of water usage by a single person is 65 gallons in the district of Santa Clara, California."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
        
    )
    return response.choices[0].message['content'].strip()
    
# Generate simulated water usage data
fixture = st.selectbox("Select a fixture to find the average water usage:", ["Shower", "Garden", "Car Wash"])
if st.button("Get Data"):
    data=get_water_usage_data(fixture)
    st.write(data)

