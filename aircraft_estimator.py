import streamlit as st

st.set_page_config(page_title="Aircraft Weight Estimator", layout="centered")
st.title("✈ Aircraft Preliminary Weight Estimator")

st.markdown("""
This tool estimates:
- Payload Weight
- Fuel Weight
- Mission Fuel Fraction
- Takeoff Weight (WTO)
- Estimated Empty Weight
""")

# --- User Inputs ---
st.header("Aircraft Mission Parameters")

passengers = st.number_input("Number of passengers", value=34, min_value=0)
passenger_weight = st.number_input("Passenger weight (lbs)", value=175, min_value=0)
baggage_weight = st.number_input("Baggage weight per passenger (lbs)", value=30, min_value=0)
crew_weight = st.number_input("Total crew weight (lbs)", value=615, min_value=0)
WTO_guess = st.number_input("Initial Takeoff Weight guess (lbs)", value=48550, min_value=0)
Mff = st.number_input("Mission Fuel Fraction", value=0.764, min_value=0.0, max_value=1.0)
L_D = st.number_input("Lift-to-Drag Ratio (L/D)", value=15.0, min_value=1.0)
Cp = st.number_input("Power Coefficient (Cp)", value=0.5, min_value=0.0)
eta_p = st.number_input("Propulsive Efficiency (ηp)", value=0.85, min_value=0.0, max_value=1.0)
range_nm = st.number_input("Range (nautical miles)", value=500, min_value=0)
loiter_hr = st.number_input("Loiter time (hours)", value=0.5, min_value=0.0)

# --- Calculations ---
payload_weight = passengers * (passenger_weight + baggage_weight) + crew_weight
fuel_weight = WTO_guess * (1 - Mff)
empty_weight = WTO_guess - fuel_weight - payload_weight

# Optional: Simplified range fuel fraction (Breguet equation for propeller aircraft)
import math
if L_D > 0 and Cp > 0 and eta_p > 0:
    mission_efficiency = (range_nm / (L_D * eta_p / Cp)) if range_nm > 0 else 0
    st.write(f"Estimated Mission Efficiency Factor (simplified): {mission_efficiency:.2f}")

# --- Display Results ---
st.header("📊 Results")
st.metric("Payload Weight (lbs)", f"{payload_weight:,.0f}")
st.metric("Fuel Weight (lbs)", f"{fuel_weight:,.0f}")
st.metric("Estimated Empty Weight (lbs)", f"{empty_weight:,.0f}")
st.metric("Takeoff Weight (WTO guess) (lbs)", f"{WTO_guess:,.0f}")
st.metric("Mission Fuel Fraction", f"{Mff:.3f}")

st.markdown("---")
st.info("This is a preliminary sizing tool. For detailed aircraft design, advanced models are required.")
