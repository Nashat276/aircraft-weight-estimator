import streamlit as st
import math
import numpy as np
import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# ------------------ Page ------------------
st.set_page_config(page_title="Aircraft Cockpit", page_icon="✈️", layout="wide")

st.title("✈️ Aircraft Cockpit Pro")

# ------------------ Sidebar Inputs ------------------
st.sidebar.header("✏️ Manual Inputs")

passengers = st.sidebar.number_input("Passengers", value=34)
passenger_weight = st.sidebar.number_input("Passenger Weight", value=175.0)
baggage_weight = st.sidebar.number_input("Baggage", value=30.0)

crew = st.sidebar.number_input("Crew Weight", value=615.0)
att = st.sidebar.number_input("Attendant", value=242.75)

Rc = st.sidebar.number_input("Range (mile)", value=1265.847)
LD = st.sidebar.number_input("L/D", value=13.0)
Cp = st.sidebar.number_input("Cp", value=0.6)
np_eff = st.sidebar.number_input("Efficiency", value=0.85)

# 🔥 WTO Guess
WTO = st.sidebar.number_input("WTO Guess", value=48550.0)

# Constants
A = 0.3774
B = 0.9647

payload = passengers * (passenger_weight + baggage_weight)

# ------------------ Button ------------------
if st.button("🚀 Calculate"):

    # Fuel fraction
    W5_W4 = 1 / math.exp(Rc / (375 * (np_eff / Cp) * LD))
    Mff = 0.99*0.995*0.995*0.985*W5_W4*0.97*0.985*0.995

    # Weights
    WF = WTO * (1 - Mff)
    WE = WTO - WF - payload - crew - att
    WE_allow = 10 ** ((math.log10(WTO) - A) / B)

    # ------------------ Metrics ------------------
    col1, col2, col3 = st.columns(3)

    col1.metric("WTO", f"{WTO:.0f}")
    col1.metric("Fuel", f"{WF:.0f}")

    col2.metric("Empty Weight", f"{WE:.0f}")
    col2.metric("Allowable WE", f"{WE_allow:.0f}")

    col3.metric("Fuel Fraction", f"{Mff:.3f}")

    # ------------------ Gauge ------------------
    st.subheader("🎯 Fuel Fraction Gauge")

    st.progress(Mff)

    # ------------------ Animation ------------------
    st.subheader("🛫 Flight Animation")

    progress = st.progress(0)
    for i in range(100):
        progress.progress(i+1)

    st.success("Flight Completed ✈️")

    # ------------------ Graph ------------------
    st.subheader("📊 Range vs Weight")

    ranges = np.linspace(200, 2000, 30)
    weights = []

    for r in ranges:
        W5_W4 = 1 / math.exp(r / (375 * (np_eff / Cp) * LD))
        Mff_temp = 0.99*0.995*0.995*0.985*W5_W4*0.97*0.985*0.995
        WF_temp = WTO * (1 - Mff_temp)
        WE_temp = WTO - WF_temp - payload - crew - att
        weights.append(WE_temp)

    df = pd.DataFrame({"Range": ranges, "Weight": weights})
    st.line_chart(df.set_index("Range"))

    # ------------------ Comparison ------------------
    st.subheader("📊 Aircraft Comparison")

    other_WTO = st.number_input("Compare with WTO", value=40000.0)

    compare_df = pd.DataFrame({
        "Aircraft": ["Your Aircraft", "Other"],
        "WTO": [WTO, other_WTO]
    })

    st.bar_chart(compare_df.set_index("Aircraft"))

    # ------------------ PDF Export ------------------
    st.subheader("📄 Export Report")

    if st.button("Generate PDF"):
        doc = SimpleDocTemplate("report.pdf")
        styles = getSampleStyleSheet()

        content = []
        content.append(Paragraph(f"WTO: {WTO}", styles["Normal"]))
        content.append(Paragraph(f"Fuel: {WF}", styles["Normal"]))
        content.append(Paragraph(f"Empty Weight: {WE}", styles["Normal"]))

        doc.build(content)

        with open("report.pdf", "rb") as f:
            st.download_button("Download PDF", f, file_name="aircraft_report.pdf")

else:
    st.info("👈 اضغط Calculate")
