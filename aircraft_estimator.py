import streamlit as st
import math

st.title("✈ Aircraft Preliminary Design Tool")

# حفظ القيم حتى بعد الحساب
if "results" not in st.session_state:
    st.session_state.results = None

st.header("Aircraft Input Data")

passengers = st.number_input(
    "Number of passengers",
    min_value=1,
    value=34,
    step=1
)

passenger_weight = st.number_input(
    "Passenger weight (lb)",
    min_value=50.0,
    value=175.0
)

baggage_weight = st.number_input(
    "Baggage weight (lb)",
    min_value=0.0,
    value=30.0
)

crew_weight = st.number_input(
    "Crew weight total (lb)",
    min_value=0.0,
    value=600.0
)

L_D = st.number_input(
    "Lift to Drag Ratio (L/D)",
    min_value=1.0,
    value=15.0
)

cp = st.number_input(
    "Specific fuel consumption",
    min_value=0.01,
    value=0.5
)

eta = st.number_input(
    "Propulsive efficiency",
    min_value=0.1,
    value=0.85
)

fuel_fraction = st.number_input(
    "Fuel fraction",
    min_value=0.01,
    max_value=0.9,
    value=0.25
)

empty_fraction = st.number_input(
    "Empty weight fraction",
    min_value=0.01,
    max_value=0.9,
    value=0.55
)

# زر الحساب
if st.button("Calculate Aircraft Data"):

    payload = passengers * (passenger_weight + baggage_weight)

    WTO = payload / (1 - fuel_fraction - empty_fraction)

    fuel_weight = WTO * fuel_fraction

    empty_weight = WTO * empty_fraction

    range_est = (eta / cp) * L_D * math.log(WTO / (WTO - fuel_weight))

    st.session_state.results = {
        "payload": payload,
        "fuel": fuel_weight,
        "empty": empty_weight,
        "wto": WTO,
        "range": range_est
    }

# عرض النتائج
if st.session_state.results:

    st.header("Results")

    st.write("Payload Weight:", round(st.session_state.results["payload"],2),"lb")

    st.write("Fuel Weight:", round(st.session_state.results["fuel"],2),"lb")

    st.write("Empty Weight:", round(st.session_state.results["empty"],2),"lb")

    st.write("Takeoff Weight:", round(st.session_state.results["wto"],2),"lb")

    st.write("Estimated Range:", round(st.session_state.results["range"],2),"nm")
