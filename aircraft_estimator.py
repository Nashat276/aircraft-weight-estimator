import streamlit as st
import math

st.title("✈ Aircraft Preliminary Design Tool")

st.write("This tool estimates aircraft weights and range.")

# Inputs
st.header("Aircraft Inputs")

passengers = st.number_input("Number of passengers", value=34)
passenger_weight = st.number_input("Passenger weight (lbs)", value=175)
baggage_weight = st.number_input("Baggage weight (lbs)", value=30)

crew_weight = st.number_input("Crew weight (lbs)", value=600)

L_D = st.number_input("Lift-to-Drag Ratio (L/D)", value=15.0)
eta = st.number_input("Propulsive efficiency", value=0.85)
cp = st.number_input("Specific fuel consumption", value=0.5)

fuel_fraction = st.number_input("Mission fuel fraction", value=0.25)

empty_fraction = st.number_input("Empty weight fraction", value=0.55)

# Payload
payload = passengers * (passenger_weight + baggage_weight)

# Takeoff weight calculation
WTO = payload / (1 - fuel_fraction - empty_fraction)

fuel_weight = WTO * fuel_fraction
empty_weight = WTO * empty_fraction

# Range using Breguet
range_est = (eta / cp) * L_D * math.log(WTO / (WTO - fuel_weight))

# Results
st.header("Results")

st.metric("Payload Weight", f"{payload:,.0f} lbs")
st.metric("Fuel Weight", f"{fuel_weight:,.0f} lbs")
st.metric("Empty Weight", f"{empty_weight:,.0f} lbs")
st.metric("Takeoff Weight", f"{WTO:,.0f} lbs")
st.metric("Estimated Range", f"{range_est:,.0f} nm")

# Payload vs Range simple diagram
st.header("Payload vs Range")

ranges = []
payloads = []

for i in range(1, 10):
    p = payload * (1 - i*0.08)
    f = WTO * fuel_fraction * (1 + i*0.05)
    r = (eta / cp) * L_D * math.log(WTO / (WTO - f))
    ranges.append(r)
    payloads.append(p)

st.line_chart({"Range": ranges, "Payload": payloads})
