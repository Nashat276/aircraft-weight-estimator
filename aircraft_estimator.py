import streamlit as st
import math
import numpy as np
import pandas as pd

# ------------------ Page ------------------
st.set_page_config(page_title="Aircraft Cockpit", page_icon="✈️", layout="wide")

# ------------------ Style ------------------
st.markdown("""
<style>
body {background-color: #0b0f19;}
.metric-card {
    background: linear-gradient(145deg, #1c2333, #0f1424);
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0 0 15px rgba(0,255,255,0.2);
}
</style>
""", unsafe_allow_html=True)

# ------------------ Title ------------------
st.title("✈️ Aircraft Cockpit Dashboard")
st.markdown("### Real-Time Aircraft Design System")

# ------------------ Sidebar ------------------
st.sidebar.header("⚙️ Controls")

passengers = st.sidebar.slider("Passengers", 0, 100, 34)
Rc = st.sidebar.slider("Range (mile)", 100, 2000, 1265)
LD = st.sidebar.slider("L/D", 5.0, 25.0, 13.0)
Cp = st.sidebar.slider("Cp", 0.3, 1.0, 0.6)
np_eff = st.sidebar.slider("Efficiency", 0.5, 1.0, 0.85)

# Constants
A = 0.3774
B = 0.9647
crew = 615
att = 242.75
payload = passengers * (175 + 30)

# ------------------ Calculate ------------------
if st.button("🚀 Run Simulation"):

    # Fuel fraction
    W5_W4 = 1 / math.exp(Rc / (375 * (np_eff / Cp) * LD))
    Mff = 0.99*0.995*0.995*0.985*W5_W4*0.97*0.985*0.995

    # Solve WTO
    WTO = 50000
    for _ in range(50):
        WF = WTO * (1 - Mff)
        WE = WTO - WF - payload - crew - att
        WE_allow = 10 ** ((math.log10(WTO) - A) / B)
        WTO += (WE_allow - WE) * 0.5

    # ------------------ Dashboard ------------------
    col1, col2, col3 = st.columns(3)

    col1.metric("✈️ WTO", f"{WTO:.0f} lb")
    col1.metric("⛽ Fuel", f"{WF:.0f} lb")

    col2.metric("⚙️ Empty Weight", f"{WE:.0f} lb")
    col2.metric("📏 Allowable WE", f"{WE_allow:.0f} lb")

    col3.metric("🔥 Fuel Fraction", f"{Mff:.3f}")

    # ------------------ Graph ------------------
    st.subheader("📊 Range vs Weight")

    ranges = np.linspace(200, 2000, 50)
    weights = []

    for r in ranges:
        W5_W4 = 1 / math.exp(r / (375 * (np_eff / Cp) * LD))
        Mff_temp = 0.99*0.995*0.995*0.985*W5_W4*0.97*0.985*0.995

        WTO_temp = 50000
        for _ in range(20):
            WF = WTO_temp * (1 - Mff_temp)
            WE = WTO_temp - WF - payload - crew - att
            WE_allow = 10 ** ((math.log10(WTO_temp) - A) / B)
            WTO_temp += (WE_allow - WE) * 0.5

        weights.append(WTO_temp)

    df = pd.DataFrame({"Range": ranges, "WTO": weights})

    st.line_chart(df.set_index("Range"))

else:
    st.info("👈 اضغط Run Simulation لتشغيل النظام")
