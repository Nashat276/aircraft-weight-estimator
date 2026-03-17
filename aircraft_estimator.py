import streamlit as st
import math

st.title("✈ Aircraft Preliminary Sizing Tool")

st.write("Tool based on aircraft sizing calculations")

# ------------------------
# Inputs
# ------------------------

st.header("Mission Inputs")

passengers = st.number_input("Number of passengers", value=34)
passenger_weight = st.number_input("Passenger weight (lb)", value=175)
baggage_weight = st.number_input("Baggage weight (lb)", value=30)

crew_weight = st.number_input("Total crew weight (lb)", value=600)

range_nm = st.number_input("Range (nautical miles)", value=800)

loiter_time = st.number_input("Loiter time (hours)", value=0.5)

L_D = st.number_input("Lift-to-Drag ratio (L/D)", value=15.0)

cp = st.number_input("Specific fuel consumption", value=0.5)

eta = st.number_input("Propulsive efficiency", value=0.85)

Mff = st.number_input("Mission fuel fraction", value=0.764)

# ------------------------
# Calculate Button
# ------------------------

if st.button("Calculate Aircraft Size"):

    # Payload
    payload = passengers * (passenger_weight + baggage_weight)

    # Initial Takeoff weight guess
    WTO_guess = payload * 3

    # Fuel weight
    fuel_weight = WTO_guess * (1 - Mff)

    # Empty weight
    empty_weight = WTO_guess - payload - fuel_weight

    # Range using Breguet
    range_est = (eta / cp) * L_D * math.log(WTO_guess / (WTO_guess - fuel_weight))

    # ------------------------
    # Results
    # ------------------------

    st.header("Results")

    st.write("Payload Weight:", round(payload,2), "lb")
    st.write("Fuel Weight:", round(fuel_weight,2), "lb")
    st.write("Empty Weight:", round(empty_weight,2), "lb")
    st.write("Takeoff Weight (WTO):", round(WTO_guess,2), "lb")
    st.write("Estimated Range:", round(range_est,2), "nm")
