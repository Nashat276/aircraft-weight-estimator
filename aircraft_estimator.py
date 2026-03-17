import streamlit as st
import math
import numpy as np
import pandas as pd
import io
import plotly.express as px
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet
import tempfile
import os

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Aircraft Design Pro", layout="wide", page_icon="✈️")

st.title("✈️ Aircraft Design Cockpit")
st.markdown("### Engineering Analysis Tool (Based on Homework 2.8)")

# ------------------ SIDEBAR INPUTS ------------------
st.sidebar.header("⚙️ Mission Specification")

passengers = st.sidebar.number_input("Number of Passengers", value=34)
pax_w = st.sidebar.number_input("Passenger Weight (lbs)", value=175)
bag_w = st.sidebar.number_input("Baggage Weight (lbs)", value=30)
Rc = st.sidebar.number_input("Cruise Range (statute miles)", value=1265.8)
LD = st.sidebar.number_input("L/D (Cruise)", value=13.0)
Cp = st.sidebar.number_input("Cp (lbs/Hp/Hr)", value=0.6)
np_eff = st.sidebar.number_input("Propeller Efficiency (ηp)", value=0.85)
WTO_guess = st.sidebar.number_input("WTO Guess (lbs)", value=48550.0)

# Constants from Source
A = 0.3774
B = 0.9647
W_crew = 615
W_tfo = 242.75
W_payload = passengers * (pax_w + bag_w)

# ------------------ CALCULATION ENGINE ------------------
def run_analysis(wto_input, range_input, ld_input):
    # Phase Fuel Fractions
    w1_wto = 0.99   # Engine Start
    w2_w1 = 0.995   # Taxi
    w3_w2 = 0.995   # Takeoff
    w4_w3 = 0.985   # Climb
    
    # Cruise Phase (Eq 2.9)
    w5_w4 = 1 / math.exp(range_input / (375 * (np_eff / Cp) * ld_input))
    
    # Loiter & Others
    w6_w5 = 0.970   # Loiter
    w7_w6 = 0.985   # Descent
    w8_w7 = 0.995   # Landing
    
    mff = w1_wto * w2_w1 * w3_w2 * w4_w3 * w5_w4 * w6_w5 * w7_w6 * w8_w7
    wf = wto_input * (1 - mff)
    
    # Step 4 & 5: Tentative Weights
    woe_tent = wto_input - wf - W_payload
    we_tent = woe_tent - W_tfo - W_crew
    
    # Step 6: Allowable Empty Weight (Statistical)
    we_allow = 10**((math.log10(wto_input) - A) / B)
    
    return mff, wf, we_tent, we_allow

# ------------------ MAIN INTERFACE ------------------
if st.button("🚀 Run Analysis"):
    mff, wf, we_calculated, we_allowable = run_analysis(WTO_guess, Rc, LD)
    diff = we_calculated - we_allowable

    # Results Display
    st.subheader("📊 Results & Weight Matching")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Payload (lbs)", f"{W_payload:,.0f}")
    c2.metric("Fuel Fraction (Mff)", f"{mff:.4f}")
    c3.metric("Calculated WE", f"{we_calculated:,.1f} lbs")
    c4.metric("Allowable WE", f"{we_allowable:,.1f} lbs", delta=f"{diff:.2f} lbs", delta_color="inverse")

    if abs(diff) < 10:
        st.success("✅ Weight Convergence Achieved!")
    else:
        st.warning(f"⚠️ Weight mismatch: {diff:.2f} lbs. Adjust WTO Guess.")

    # ------------------ VISUALIZATION ------------------
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("📈 Range Sensitivity")
        ranges = np.linspace(500, 2000, 50)
        we_list = [run_analysis(WTO_guess, r, LD)[2] for r in ranges]
        df_range = pd.DataFrame({"Range": ranges, "Empty Weight": we_list})
        fig1 = px.line(df_range, x="Range", y="Empty Weight", title="WE vs Range")
        st.plotly_chart(fig1, use_container_width=True)

    with col_right:
        st.subheader("🎯 L/D vs Range Contour")
        ld_range = np.linspace(10, 18, 20)
        r_range = np.linspace(800, 1500, 20)
        z_data = np.array([[run_analysis(WTO_guess, r, ld)[0] for r in r_range] for ld in ld_range])
        fig2 = px.imshow(z_data, x=r_range, y=ld_range, labels=dict(x="Range", y="L/D", color="Mff"), title="Fuel Fraction Map")
        st.plotly_chart(fig2, use_container_width=True)

    # ------------------ PDF GENERATION ------------------
    st.divider()
    st.subheader("📄 Export Documentation")
    
    if st.button("Prepare PDF Report"):
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
                doc = SimpleDocTemplate(tmp_pdf.name)
                styles = getSampleStyleSheet()
                elements = []
                
                elements.append(Paragraph("Aircraft Design Analysis Report", styles["Title"]))
                elements.append(Paragraph(f"Mission: {passengers} Passengers, {Rc} miles Range.", styles["Normal"]))
                elements.append(Spacer(1, 12))
                
                data = [
                    ["Parameter", "Value"],
                    ["Take-off Weight Guess", f"{WTO_guess} lbs"],
                    ["Calculated Fuel Weight", f"{wf:.2f} lbs"],
                    ["Calculated Empty Weight", f"{we_calculated:.2f} lbs"],
                    ["Allowable Empty Weight", f"{we_allowable:.2f} lbs"]
                ]
                
                # Simple text table format
                for row in data:
                    elements.append(Paragraph(f"<b>{row[0]}:</b> {row[1]}", styles["Normal"]))
                
                doc.build(elements)
                
                with open(tmp_pdf.name, "rb") as f:
                    st.download_button("📥 Download PDF Now", f, file_name="Aircraft_Analysis.pdf")
        except Exception as e:
            st.error(f"Error generating PDF: {e}")

else:
    st.info("👈 Set parameters in the sidebar and click 'Run Analysis'")
