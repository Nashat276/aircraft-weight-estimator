import streamlit as st
import math

# ------------------ Page Config ------------------
st.set_page_config(
    page_title="Aircraft Weight Tool",
    page_icon="✈️",
    layout="wide"
)

# ------------------ Custom CSS ------------------
st.markdown("""
<style>
.main {
    background-color: #0e1117;
}
.block-container {
    padding-top: 2rem;
}
.metric-card {
    background-color: #1c1f26;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0 0 10px rgba(0,0,0,0.5);
}
.metric-title {
    font-size: 18px;
    color: #aaa;
}
.metric-value {
    font-size: 28px;
    font-weight: bold;
    color: #00c6ff;
}
</style>
""", unsafe_allow_html=True)

# ------------------ Title ------------------
st.title("✈️ Aircraft Takeoff Weight Estimator")
st.markdown("### Smart Preliminary Aircraft Design Tool")

# ------------------ Sidebar Inputs ------------------
st.sidebar.header("✏️ Input Parameters")

# Payload
st.sidebar.subheader("Payload")
passengers = st.sidebar.number_input("Passengers", 0, 200, 34)
passenger_weight = st.sidebar.number_input("Passenger Weight (lb)", value=175)
baggage_weight = st.sidebar.number_input("Baggage (lb)", value=30)

# Crew
st.sidebar.subheader("Crew")
crew_weight = st.sidebar.number_input("Crew Total (lb)", value=615)
attendant_weight = st.sidebar.number_input("Attendant (lb)", value=242.75)

# Cruise
st.sidebar.subheader("Cruise")
Rc = st.sidebar.number_input("Range (mile)", value=1265.847)
LD_cruise = st.sidebar.number_input("L/D Cruise", value=13.0)
Cp_cruise = st.sidebar.number_input("Cp Cruise", value=0.6)
np_cruise = st.sidebar.number_input("Efficiency Cruise", value=0.85)

# Loiter
st.sidebar.subheader("Loiter")
E_loiter = st.sidebar.number_input("Endurance (hr)", value=0.75)
LD_loiter = st.sidebar.number_input("L/D Loiter", value=16.0)
Cp_loiter = st.sidebar.number_input("Cp Loiter", value=0.65)
np_loiter = st.sidebar.number_input("Efficiency Loiter", value=0.77)
V_loiter = st.sidebar.number_input("Speed Loiter (mph)", value=287.69)

# WTO Guess
st.sidebar.subheader("Initial Guess")
WTO_guess = st.sidebar.number_input("WTO Guess (lb)", value=48550)

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

    W5_W4 = 1 / math.exp(Rc/(375*(np_cruise/Cp_cruise)*LD_cruise))
    W6_W5 = 1 / math.exp(E_loiter/(375*(1/V_loiter)*(np_loiter/Cp_loiter)*LD_loiter))

    W7_W6 = 0.985
    W8_W7 = 0.995

    Mff = (
        W1_W0 * W2_W1 * W3_W2 * W4_W3 *
        W5_W4 * W6_W5 * W7_W6 * W8_W7
    )

    WF = WTO_guess * (1 - Mff)

    WOE = WTO_guess - WF - Wpl
    WE = WOE - attendant_weight - crew_weight

    WE_allow = math.exp((math.log(WTO_guess)-A)/B)
    diff = WE_allow - WE

    # Sensitivity
    C = 1 - (1+Mres)*(1-Mff) - Mtfo
    D = Wpl + crew_weight
    F = (-B*(WTO_guess**2)*(1+Mres)*Mff)/(C*WTO_guess*(1-B)-D)
    dWTO_dR = F*Cp_cruise/(375*np_cruise*LD_cruise)

    # ------------------ Results UI ------------------
    st.subheader("📊 Results")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Payload</div>
            <div class="metric-value">{Wpl:.2f} lb</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Fuel Weight</div>
            <div class="metric-value">{WF:.2f} lb</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Empty Weight</div>
            <div class="metric-value">{WE:.2f} lb</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Allowable WE</div>
            <div class="metric-value">{WE_allow:.2f} lb</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Fuel Fraction</div>
            <div class="metric-value">{Mff:.3f}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Difference</div>
            <div class="metric-value">{diff:.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    # Sensitivity
    st.subheader("📉 Sensitivity Analysis")

    st.write(f"F = {F:.2f}")
    st.write(f"dWTO/dR = {dWTO_dR:.2f} lb per mile")

else:
    st.info("👈 عدل القيم من اليسار واضغط Calculate")
