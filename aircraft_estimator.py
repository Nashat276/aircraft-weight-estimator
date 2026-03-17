import streamlit as st
import math

st.title("✈ Aircraft Weight Estimator")

st.header("Inputs")

passengers = st.number_input("Number of passengers", value=34)
passenger_weight = st.number_input("Passenger weight (lbs)", value=175)
baggage = st.number_input("Baggage weight (lbs)", value=30)

crew_weight = st.number_input("Crew weight (lbs)", value=600)

L_D = st.number_input("Lift-to-Drag Ratio (L/D)", value=15.0)
eta = st.number_input("Propulsive efficiency", value=0.85)
cp = st.number_input("Specific fuel consumption", value=0.5)

fuel_fraction = st.number_input("Fuel fraction", value=0.25)
empty_fraction = st.number_input("Empty weight fraction", value=0.55)

# زر الحساب
if st.button("Calculate Aircraft Weights"):

    payload = passengers * (passenger_weight + baggage)

    WTO = payload / (1 - fuel_fraction - empty_fraction)

    fuel_weight = WTO * fuel_fraction
    empty_weight = WTO * empty_fraction

    range_est = (eta / cp) * L_D * math.log(WTO / (WTO - fuel_weight))

    st.header("Results")

    st.write("Payload weight:", round(payload,2), "lbs")
    st.write("Fuel weight:", round(fuel_weight,2), "lbs")
    st.write("Empty weight:", round(empty_weight,2), "lbs")
    st.write("Takeoff weight:", round(WTO,2), "lbs")
    st.write("Estimated range:", round(range_est,2), "nm")
