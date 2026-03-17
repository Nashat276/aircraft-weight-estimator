import streamlit as st
import math

# ------------------ Page Config ------------------
st.set_page_config(page_title="Aircraft Design Tool", page_icon="✈️", layout="wide")

st.title("✈️ Aircraft Preliminary Design Tool")
st.markdown("### Automatic WTO + Sensitivity Analysis")

# ------------------ Sidebar ------------------
st.sidebar.header("✏️ Inputs")

# Payload
passengers = st.sidebar.number_input("Passengers", value=34)
passenger_weight = st.sidebar.number_input("Passenger Weight (lb)", value=175.0)
baggage_weight = st.sidebar.number_input("Baggage (lb)", value=30.0)

# Crew
crew_weight = st.sidebar.number_input("Crew Weight (lb)", value=615.0)
attendant_weight = st.sidebar.number_input("Attendant (lb)", value=242.75)

# Cruise
Rc = st.sidebar.number_input("Range (mile)", value=1265.847)
LD_cruise = st.sidebar.number_input("L/D Cruise", value=13.0)
Cp_cruise = st.sidebar.number_input("Cp Cruise", value=0.6)
np_cruise = st.sidebar.number_input("ηp Cruise", value=0.85)

# Loiter
E_loiter = st.sidebar.number_input("Endurance (hr)", value=0.75)
LD_loiter = st.sidebar.number_input("L/D Loiter", value=16.0)
Cp_loiter = st.sidebar.number_input("Cp Loiter", value=0.65)
np_loiter = st.sidebar.number_input("ηp Loiter", value=0.77)
V_loiter = st.sidebar.number_input("Speed (mph)", value=287.69)

# Constants
A = 0.3774
B = 0.9647
Mtfo = 0.005
Mres = 0

# ------------------ Button ------------------
if st.button("🚀 Run Analysis"):

    # Payload
    Wpl = passengers * (passenger_weight + baggage_weight)

    # ------------------ Mission Fractions ------------------
    W1_W0 = 0.99
    W2_W1 = 0.995
    W3_W2 = 0.995
    W4_W3 = 0.985

    W5_W4 = 1 / math.exp(Rc / (375 * (np_cruise / Cp_cruise) * LD_cruise))
    W6_W5 = 1 / math.exp(E_loiter / (375 * (1 / V_loiter) * (np_loiter / Cp_loiter) * LD_loiter))

    W7_W6 = 0.985
    W8_W7 = 0.995

    Mff = W1_W0*W2_W1*W3_W2*W4_W3*W5_W4*W6_W5*W7_W6*W8_W7

    # ------------------ Solve WTO Automatically ------------------
    WTO = 50000  # initial guess

    for _ in range(100):
        WF = WTO * (1 - Mff)
        WOE = WTO - WF - Wpl
        WE = WOE - attendant_weight - crew_weight
        WE_allow = 10 ** ((math.log10(WTO) - A) / B)

        error = WE_allow - WE
        WTO = WTO + error * 0.5  # convergence factor

    # Final values
    WF = WTO * (1 - Mff)
    WOE = WTO - WF - Wpl
    WE = WOE - attendant_weight - crew_weight
    WE_allow = 10 ** ((math.log10(WTO) - A) / B)
    diff = WE_allow - WE

    # ------------------ Sensitivity ------------------
    C = 1 - (1 + Mres) * (1 - Mff) - Mtfo
    D = Wpl + crew_weight

    F = (-B * (WTO**2) * (1 + Mres) * Mff) / (C * WTO * (1 - B) - D)

    # Range case
    dWTO_dCp_R = F * Rc / (375 * np_cruise * LD_cruise)
    dWTO_dnp_R = -F * Rc * Cp_cruise / (375 * (np_cruise**2) * LD_cruise)
    dWTO_dLD_R = -F * Rc * Cp_cruise / (375 * np_cruise * (LD_cruise**2))

    # Endurance case
    dWTO_dCp_E = F * E_loiter * V_loiter / (375 * np_cruise * LD_cruise)
    dWTO_dnp_E = -F * E_loiter * V_loiter * Cp_cruise / (375 * (np_cruise**2) * LD_cruise)
    dWTO_dLD_E = -F * E_loiter * V_loiter * Cp_cruise / (375 * np_cruise * (LD_cruise**2))

    # Range sensitivity
    dWTO_dR = F * Cp_cruise / (375 * np_cruise * LD_cruise)

    # ------------------ UI ------------------
    st.subheader("📊 Results")

    col1, col2, col3 = st.columns(3)

    col1.metric("WTO (lb)", f"{WTO:.2f}")
    col1.metric("Fuel Weight", f"{WF:.2f}")

    col2.metric("Empty Weight", f"{WE:.2f}")
    col2.metric("Allowable WE", f"{WE_allow:.2f}")

    col3.metric("Fuel Fraction", f"{Mff:.3f}")
    col3.metric("Difference", f"{diff:.2f}")

    # ------------------ Sensitivity Display ------------------
    st.subheader("📉 Sensitivity Analysis")

    st.markdown("### Range Case")
    st.write("dWTO/dCp =", dWTO_dCp_R)
    st.write("dWTO/dηp =", dWTO_dnp_R)
    st.write("dWTO/d(L/D) =", dWTO_dLD_R)

    st.markdown("### Endurance Case")
    st.write("dWTO/dCp =", dWTO_dCp_E)
    st.write("dWTO/dηp =", dWTO_dnp_E)
    st.write("dWTO/d(L/D) =", dWTO_dLD_E)

    st.markdown("### Range Sensitivity")
    st.write("dWTO/dR =", dWTO_dR)

    # Debug
    with st.expander("🔍 Debug"):
        st.write("Mff =", Mff)
        st.write("F =", F)

else:
    st.info("👈 اضغط Run Analysis بعد تعديل القيم")
