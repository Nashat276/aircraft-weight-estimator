import streamlit as st

st.set_page_config(page_title="Aircraft Weight Estimator", layout="centered")

st.title("✈ Aircraft Preliminary Weight Estimator")

st.write("Enter aircraft parameters to estimate weights.")

# Inputs
passengers = st.number_input("Number of passengers", value=34)
passenger_weight = st.number_input("Passenger weight (lbs)", value=175)
baggage_weight = st.number_input("Baggage weight (lbs)", value=30)

crew_weight = st.number_input("Total crew weight (lbs)", value=615)
WTO_guess = st.number_input("Initial Takeoff Weight guess (lbs)", value=48550)

Mff = st.number_input("Mission Fuel Fraction", value=0.764)

# Calculations
payload = passengers * (passenger_weight + baggage_weight) + crew_weight
fuel_weight = WTO_guess * (1 - Mff)
empty_weight = WTO_guess - fuel_weight - payload

st.subheader("Results")

st.metric("Payload Weight", f"{payload:,.0f} lbs")
st.metric("Fuel Weight", f"{fuel_weight:,.0f} lbs")
st.metric("Empty Weight", f"{empty_weight:,.0f} lbs")
st.metric("Takeoff Weight (WTO)", f"{WTO_guess:,.0f} lbs")

st.success("Calculation complete ✔") 
