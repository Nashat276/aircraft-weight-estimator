import streamlit as st
import math

# ------------------ Page Config ------------------
st.set_page_config(
    page_title="Aircraft Weight Estimator",
    page_icon="✈️",
    layout="wide"
)

# ------------------ Title ------------------
st.title("✈️ Aircraft Takeoff Weight Estimator")
st.markdown("### Preliminary Aircraft Design Tool")

# ------------------ Sidebar ------------------
st.sidebar.header("✏️ Input Parameters")

# Payload
st.sidebar.subheader("Payload")
passengers = st.sidebar.number_input("Passengers", min_value=0, value=34)
passenger_weight = st.sidebar.number_input("Passenger Weight (lb)", value=175.0)
baggage_weight = st.sidebar.number_input("Baggage Weight (lb)", value=30.0)

# Crew
st.sidebar.subheader("Crew")
crew_weight = st.sidebar.number_input("Crew Weight Total (lb)", value=615.0)
attendant_weight = st.sidebar.number_input("Attendant Weight (lb)", value=242.75)

# Cruise
st.sidebar.subheader("Cruise")
Rc = st.sidebar.number_input("Range (statute miles)", value=1265.847)
LD_cruise = st.sidebar.number_input("L/D Cruise", value=13.0)
Cp_cruise = st.sidebar.number_input("Cp Cruise", value=0.6)
np_cruise = st.sidebar.number_input("Prop Efficiency Cruise", value=0.85)

# Loiter
st.sidebar.subheader("Loiter")
E_loiter = st.sidebar.number_input("Endurance (hr)", value=0.75)
LD_loiter = st.sidebar.number_input("L/D Loiter", value=16.0)
Cp_loiter = st.sidebar.number_input("Cp Loiter", value=0.65)
np_loiter = st.sidebar.number_input("Prop Efficiency Loiter", value=0.77)
V_loiter = st.sidebar.number_input("Speed (mph)", value=287.69)

# WTO Guess
st.sidebar.subheader("Initial Guess")
WTO_guess = st.sidebar.number_input("WTO Guess (lb)", value=48550.0)

# Constants
A = 0.3774
B = 0.9647
Mtfo = 0.005
Mres = 0

# ------------------ Button ------------------
calculate = st.button("🚀 Calculate")

# ------------------ Calculation ------------------
if calculate:

    # Payload
    Wpl = passengers * (passenger_weight + baggage_weight)

    # Mission fractions
    W1_W0 = 0.99
    W2_W1 = 0.995
    W3_W2 = 0.995
    W4_W3 = 0.985

    # Cruise
    W5_W4 = 1 / math.exp(Rc / (375 * (np_cruise / Cp_cruise) * LD_cruise))

    # Loiter
    W6_W5 = 1 / math.exp(E_loiter / (375 * (1 / V_loiter) * (np_loiter / Cp_loiter) * LD_loiter))

    W7_W6 = 0.985
    W8_W7 = 0.995

    # Total fuel fraction
    Mff = (
        W1_W0 *
        W2_W1 *
        W3_W2 *
        W4_W3 *
        W5_W4 *
        W6_W5 *
        W7_W6 *
        W8_W7
    )

    # Fuel weight
    WF = WTO_guess * (1 - Mff)

    # Weights
    WOE = WTO_guess - WF - Wpl
    WE = WOE - attendant_weight - crew_weight

    # ✅ FIXED (log10 instead of ln)
    WE_allow = 10 ** ((math.log10(WTO_guess) - A) / B)

    diff = WE_allow - WE

    # Sensitivity
    C = 1 - (1 + Mres) * (1 - Mff) - Mtfo
    D = Wpl + crew_weight

    F = (-B * (WTO_guess ** 2) * (1 + Mres) * Mff) / (C * WTO_guess * (1 - B) - D)

    dWTO_dR = F * Cp_cruise / (375 * np_cruise * LD_cruise)

    # ------------------ Results ------------------
    st.subheader("📊 Results")

    col1, col2, col3 = st.columns(3)

    col1.metric("Payload (lb)", f"{Wpl:.2f}")
    col1.metric("Fuel Weight (lb)", f"{WF:.2f}")

    col2.metric("Empty Weight (lb)", f"{WE:.2f}")
    col2.metric("Allowable WE (lb)", f"{WE_allow:.2f}")

    col3.metric("Fuel Fraction", f"{Mff:.3f}")
    col3.metric("Difference", f"{diff:.2f}")

    # Debug
    with st.expander("🔍 Debug Values"):
        st.write("W5/W4 =", W5_W4)
        st.write("W6/W5 =", W6_W5)

    # Sensitivity
    st.subheader("📉 Sensitivity")

    st.write(f"F = {F:.2f}")
    st.write(f"dWTO/dR = {dWTO_dR:.2f} lb per mile")

else:
    st.info("👈 عدل القيم من اليسار واضغط Calculate")
