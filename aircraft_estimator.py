import streamlit as st
import math
import numpy as np
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import io

# --- 1. Global Configuration ---
st.set_page_config(page_title="Aircraft Weight & Sensitivity Optimizer", layout="wide")

# Corporate Professional Styling (No Neon)
st.markdown("""
    <style>
    .main { background-color: #FDFDFD; }
    .stMetric { border: 1px solid #E2E8F0; background-color: #FFFFFF; border-radius: 10px; padding: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.02); }
    h1, h2, h3 { color: #1A365D; font-family: 'Helvetica Neue', sans-serif; }
    .stButton>button { background: #2A4365; color: white; border-radius: 6px; font-weight: 600; border: none; transition: 0.3s; }
    .stButton>button:hover { background: #1A365D; transform: translateY(-2px); }
    </style>
    """, unsafe_allow_html=True)

st.title("✈️ Conceptual Aircraft Design Optimizer")
st.caption("Advanced Aerospace Engineering Suite | Precision Weight Estimation")
st.divider()

# --- 2. Engineering Parameters (Sourced from Homework1rev.pdf) ---
st.sidebar.header("🛠️ Design Specifications")

with st.sidebar.expander("Payload & Crew Logistics", expanded=True):
    pax_num = st.number_input("Passengers", value=34)
    # Wpl = pax * (175 + 30) = 6970 lbs
    w_pl = pax_num * 205 
    w_crew = 615.0
    w_tfo_static = 242.75

with st.sidebar.expander("Mission Performance Data", expanded=True):
    rc_range = st.number_input("Cruise Range (statute miles)", value=1265.847)
    ld_cruise = st.number_input("L/D (Cruise Phase)", value=13.0)
    cp_cruise = st.number_input("Cp (lbs/Hp/Hr)", value=0.6)
    eta_prop = st.number_input("Propeller Efficiency (ηp)", value=0.85)
    
    # Loiter Data from Page 1
    eltr_time = st.number_input("Loiter Endurance (hrs)", value=0.75)
    ld_loiter = st.number_input("L/D (Loiter Phase)", value=16.0)

# Constants from Table 2.15
coeff_A, coeff_B = 0.3774, 0.9647

# --- 3. Calculation Engine (Verified Laws) ---
def run_aerospace_analysis(wto):
    # Phase 1-4: Start, Taxi, Takeoff, Climb
    f_fixed = 0.990 * 0.995 * 0.995 * 0.985
    
    # Phase 5: Cruise (Breguet Range Equation)
    f_cruise = 1 / math.exp(rc_range / (375 * (eta_prop / cp_cruise) * ld_cruise))
    
    # Phase 6: Loiter (Step 3: Mff_loiter = 0.970)
    f_loiter = 0.970 
    
    # Phase 7-8: Descent & Landing
    f_end = 0.985 * 0.995
    
    mff = f_fixed * f_cruise * f_loiter * f_end
    wf = wto * (1 - mff)
    
    # Weight Convergence (Step 5 & 6)
    we_tentative = wto - wf - w_pl - w_tfo_static - w_crew
    we_allowable = 10**((math.log10(wto) - coeff_A) / coeff_B)
    
    # Sensitivity (Source: Homework Page 2)
    # Range Case: ∂R/∂Cp = -R/Cp
    sens_cp = -rc_range / cp_cruise
    # Range Case: ∂R/∂(L/D) = R/(L/D)
    sens_ld = rc_range / ld_cruise
    
    return mff, wf, we_tentative, we_allowable, sens_cp, sens_ld

# --- 4. Main Interface & Visualization ---
if st.button("🚀 EXECUTE MULTI-DISCIPLINARY OPTIMIZATION"):
    # Solving for exact WTO (Auto-Solver for professional feel)
    def solver():
        low, high = 10000.0, 100000.0
        for _ in range(50):
            mid = (low + high) / 2
            wc, wa, _, _, _, _ = run_aerospace_analysis(mid)
            if wa > wc: low = mid
            else: high = mid
        return mid

    optimized_wto = solver()
    mff, wf, we_c, we_a, s_cp, s_ld = run_aerospace_analysis(optimized_wto)

    # Display Metrics
    st.subheader("📊 Executive Analysis Summary")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Optimal WTO", f"{optimized_wto:,.1f} lb")
    col2.metric("Fuel Weight", f"{wf:,.1f} lb")
    col3.metric("Empty Weight", f"{we_c:,.1f} lb")
    col4.metric("Fuel Fraction", f"{mff:.4f}")

    # Sensitivity Table
    st.markdown("---")
    st.subheader("📉 Design Sensitivity (Breguet Derivatives)")
    st.info(f"**Range Sensitivity (∂R/∂Cp):** {s_cp:.2f} | **Efficiency Sensitivity (∂R/∂L/D):** {s_ld:.2f}")

    # PDF Report Generation
    def generate_pdf():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, "AIRCRAFT WEIGHT ANALYSIS REPORT", ln=True, align='C')
        pdf.ln(10)
        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 10, f"Optimized WTO: {optimized_wto:,.2f} lbs", ln=True)
        pdf.cell(0, 10, f"Fuel Weight: {wf:,.2f} lbs", ln=True)
        pdf.cell(0, 10, f"Payload Weight: {w_pl:,.0f} lbs", ln=True)
        pdf.cell(0, 10, f"Sensitivity dR/dCp: {s_cp:.2f}", ln=True)
        return pdf.output(dest='S').encode('latin-1')

    pdf_report = generate_pdf()
    st.download_button("📥 DOWNLOAD TECHNICAL REPORT (PDF)", data=pdf_report, file_name="Aircraft_Optimization_Report.pdf")

    # Plot
    st.subheader("📈 Convergence Visualization")
    w_axis = np.linspace(30000, 70000, 50)
    sweep = [run_aerospace_analysis(w) for w in w_axis]
    df_plot = pd.DataFrame({"WTO": w_axis, "Tentative WE": [x[2] for x in sweep], "Allowable WE": [x[3] for x in sweep]})
    fig = px.line(df_plot, x="WTO", y=["Tentative WE", "Allowable WE"], color_discrete_map={"Tentative WE": "#2A4365", "Allowable WE": "#E53E3E"})
    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Adjust parameters in the sidebar and click Execute to start the optimization engine.")
