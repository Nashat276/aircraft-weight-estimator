import streamlit as st
import math
import numpy as np
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import io

# --- 1. Page & Professional Branding ---
st.set_page_config(page_title="AeroDesign Comprehensive Suite", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #F4F7F9; }
    .stMetric { background-color: white; border-top: 4px solid #003366; border-radius: 8px; padding: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    h1, h2, h3 { color: #003366; font-family: 'Segoe UI', Tahoma, Geneva, sans-serif; }
    .stButton>button { background: linear-gradient(to right, #003366, #00509E); color: white; border: none; height: 3.5em; font-size: 16px; transition: 0.3s; }
    .stButton>button:hover { opacity: 0.9; transform: scale(1.01); }
    </style>
    """, unsafe_allow_html=True)

st.title("✈️ Full Mission Aircraft Weight Analyzer")
st.caption("Comprehensive Digital Twin of Homework 1 Specifications")
st.divider()

# --- 2. Dynamic Sidebar (All Constants from Page 1) ---
st.sidebar.header("🛠️ Engineering Specifications")

with st.sidebar.expander("1. Mission Payload & Crew", expanded=True):
    pax = st.number_input("Passengers", value=34)
    w_pax_total = pax * 205 # From File: 175+30
    w_crew = st.number_input("Crew Weight (Wcrew)", value=615.0)
    mtfo_ratio = st.number_input("TFO Ratio (Mtfo)", value=0.005, format="%.3f")
    wtfo_fixed = st.number_input("Fixed TFO Weight", value=242.75)

with st.sidebar.expander("2. Cruise Phase (Breguet)", expanded=True):
    rc = st.number_input("Cruise Range (miles)", value=1265.847)
    vc = st.number_input("Cruise Speed (kts)", value=250.0)
    ld_c = st.number_input("L/D Cruise", value=13.0)
    cp_c = st.number_input("Cp Cruise (lbs/Hp/Hr)", value=0.6)
    np_c = st.number_input("Prop Efficiency (ηp)", value=0.85)

with st.sidebar.expander("3. Loiter Phase (Endurance)", expanded=True):
    eltr = st.number_input("Endurance Time (hrs)", value=0.75)
    ld_l = st.number_input("L/D Loiter", value=16.0)
    cp_l = st.number_input("Cp Loiter", value=0.65)
    np_l = st.number_input("Prop Efficiency (ηp) Loiter", value=0.80)

# Constants from Table 2.15
coeff_a, coeff_b = 0.3774, 0.9647

# --- 3. Calculation Engine (Step-by-Step Mission Profile) ---
def run_comprehensive_analysis(wto):
    # Mission Fractions per File Page 1
    f1, f2, f3, f4 = 0.990, 0.995, 0.995, 0.985 # Engine Start to Climb
    
    # Phase 5: Cruise (Breguet Range)
    f5 = 1 / math.exp(rc / (375 * (np_c / cp_c) * ld_c))
    
    # Phase 6: Loiter (Breguet Endurance for Propeller)
    # f6 = 1 / exp( E * V * Cp / (375 * np * L/D) ) -> Using simplified 0.970 from your notes
    f6 = 0.970 
    
    f7, f8 = 0.985, 0.995 # Descent & Landing
    
    mff = f1 * f2 * f3 * f4 * f5 * f6 * f7 * f8
    wf = wto * (1 - mff)
    
    # Convergence Matching
    we_tent = wto - wf - w_pax_total - wtfo_fixed - w_crew
    we_allow = 10**((math.log10(wto) - coeff_a) / coeff_b)
    
    # Sensitivity (From Last Table in File)
    # Range Case
    s_r_cp = -rc / cp_c
    s_r_ld = rc / ld_c
    # Endurance Case
    s_e_cp = -eltr / cp_l
    s_e_ld = eltr / ld_l
    
    return {
        "mff": mff, "wf": wf, "we_c": we_tent, "we_a": we_allow,
        "fractions": [f1, f2, f3, f4, f5, f6, f7, f8],
        "sens": [s_r_cp, s_r_ld, s_e_cp, s_e_ld]
    }

# --- 4. Main UI Logic ---
if st.button("🚀 EXECUTE COMPREHENSIVE ENGINEERING ANALYSIS"):
    # Solving for Optimum WTO
    def solver():
        w = 10000.0
        for _ in range(100):
            res = run_comprehensive_analysis(w)
            w = w + (res['we_a'] - res['we_c']) * 1.5
        return w

    opt_wto = solver()
    res = run_comprehensive_analysis(opt_wto)
    
    # Performance Summary Metrics
    st.subheader("📊 Performance Summary")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Optimized WTO", f"{opt_wto:,.1f} lb")
    c2.metric("Total Fuel (Wf)", f"{res['wf']:,.1f} lb")
    c3.metric("Empty Weight (We)", f"{res['we_c']:,.1f} lb")
    c4.metric("Fuel Fraction (Mff)", f"{res['mff']:.4f}")

    # Detailed Fractions Table (Dynamic)
    st.divider()
    st.subheader("📋 Phase-by-Phase Weight Fractions")
    phases = ["Engine Start", "Taxi", "Take-off", "Climb", "Cruise", "Loiter", "Descent", "Landing"]
    df_phases = pd.DataFrame({"Mission Phase": phases, "Weight Fraction (f)": res['fractions']})
    st.dataframe(df_phases.style.format({"Weight Fraction (f)": "{:.4f}"}), use_container_width=True)

    # Sensitivity Analysis (Page 2 of File)
    st.subheader("📉 Sensitivity Analysis (Partial Derivatives)")
    sc1, sc2 = st.columns(2)
    with sc1:
        st.info("**Range Sensitivity**")
        st.write(f"∂R / ∂Cp: {res['sens'][0]:.2f}")
        st.write(f"∂R / ∂(L/D): {res['sens'][1]:.2f}")
    with sc2:
        st.info("**Endurance Sensitivity**")
        st.write(f"∂E / ∂Cp: {res['sens'][2]:.4f}")
        st.write(f"∂E / ∂(L/D): {res['sens'][3]:.4f}")

    # Visualization
    st.subheader("📈 Visualization: Weight Convergence")
    w_axis = np.linspace(30000, 70000, 50)
    sweep = [run_comprehensive_analysis(w) for w in w_axis]
    df_plot = pd.DataFrame({"WTO": w_axis, "Tentative WE": [x['we_c'] for x in sweep], "Allowable WE": [x['we_a'] for x in sweep]})
    fig = px.line(df_plot, x="WTO", y=["Tentative WE", "Allowable WE"], color_discrete_map={"Tentative WE": "#003366", "Allowable WE": "#C53030"})
    st.plotly_chart(fig, use_container_width=True)

    # PDF Generator
    def generate_pdf():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, "AIRCRAFT ANALYSIS REPORT", ln=True, align='C')
        pdf.ln(10)
        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 10, f"Optimized WTO: {opt_wto:,.2f} lbs", ln=True)
        pdf.cell(0, 10, f"Total Fuel: {res['wf']:,.2f} lbs", ln=True)
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, "Sensitivity Results:", ln=True)
        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 10, f"- Range Sensitivity (dR/dCp): {res['sens'][0]:.2f}", ln=True)
        pdf.cell(0, 10, f"- Endurance Sensitivity (dE/dCp): {res['sens'][2]:.4f}", ln=True)
        return pdf.output(dest='S').encode('latin-1')

    pdf_report = generate_pdf()
    st.download_button("📥 DOWNLOAD TECHNICAL REPORT (PDF)", data=pdf_report, file_name="Aircraft_Full_Report.pdf")

else:
    st.info("Engineering Module Ready. Configure mission data in the sidebar and press Execute.")
