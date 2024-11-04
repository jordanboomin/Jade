# Feature 2: Personalized Tips and Recommendations
st.header("2. Personalized Tips for Reducing Water Use")

def get_personalized_tips(activity):
    if activity == "Shower":
        return "To save water when showering, maybe consider a a shower head that utilizes less water and aiming to make your showers shorter!"
    elif activity == "Garden":
        return "Water your garden in the early morning due to less evaporation and consider getting drip irrigation!"
    elif activity == "Car Wash":
        return "Consider using a bucket filled with soapy water and  sponge instead of a soap gun attachment. You will use less water that way!"
    else:
        return "Select an activity to receive tips!"
    
activity = st.selectbox("Select an activity to get tips:", ["Shower", "Garden", "Car Wash"])
if st.button("Get Tips"):
    tips = get_personalized_tips(activity)
    st.write(tips)
