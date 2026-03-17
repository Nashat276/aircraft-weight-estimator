import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Aircraft Weight Estimator", layout="centered")
st.title("✈ Aircraft Preliminary Weight Estimator")

st.markdown("""
This tool estimates:
- Payload Weight
- Fuel Weight
- Empty Weight
- Takeoff Weight (WTO)
""")

# --- User Inputs ---
st.header("Aircraft Mission Parameters")
col1, col2 = st.columns(2)

with col1:
    passengers = st.number_input("Number of passengers", value=34, min_value=0)
    passenger_weight = st.number_input("Passenger weight (lbs)", value=175, min_value=0)
    baggage_weight = st.number_input("Baggage weight per passenger (lbs)", value=30, min_value=0)

with col2:
    crew_weight = st.number_input("Total crew weight (lbs)", value=615, min_value=0)
    WTO_guess = st.number_input("Initial Takeoff Weight guess (lbs)", value=48550, min_value=0)
    Mff = st.number_input("Mission Fuel Fraction", value=0.764, min_value=0.0, max_value=1.0)

# --- Calculations ---
payload_weight = passengers * (passenger_weight + baggage_weight) + crew_weight
fuel_weight = WTO_guess * (1 - Mff)
empty_weight = WTO_guess - fuel_weight - payload_weight

# --- Display Results ---
st.header("📊 Results")
st.metric("Payload Weight (lbs)", f"{payload_weight:,.0f}", delta_color="normal")
st.metric("Fuel Weight (lbs)", f"{fuel_weight:,.0f}", delta_color="normal")
st.metric("Empty Weight (lbs)", f"{empty_weight:,.0f}", delta_color="normal")
st.metric("Takeoff Weight (WTO) (lbs)", f"{WTO_guess:,.0f}", delta_color="off")

# --- Pie Chart Visualization ---
st.subheader("Weight Distribution")
weights = [payload_weight, fuel_weight, empty_weight]
labels = ['Payload', 'Fuel', 'Empty']
colors = ['#ff9999','#66b3ff','#99ff99']

fig, ax = plt.subplots()
ax.pie(weights, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
ax.axis('equal')
st.pyplot(fig)

st.markdown("---")
st.info("This is a preliminary sizing tool. For detailed aircraft design, advanced models are required.")
