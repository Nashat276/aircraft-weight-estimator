import streamlit as st
import math
import numpy as np
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import io

# --- 1. UI Configuration & Branding ---
st.set_page_config(page_title="AeroDesign Pro: Integrated Solver", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #FFFFFF; color: #1A202C; }
    .stMetric { border-top: 5px solid #002D72; background-color: #F8F9FA; border-radius: 8px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    h1, h2, h3 { color: #002D72; font-family: 'Helvetica Neue', Arial, sans-serif; }
    .stButton>button { background: linear-gradient(90deg, #002D72 0%, #0056b3 100%); color: white; height: 3.5em; font-weight: bold; border-radius: 8px; border: none; }
    </style>
    """, unsafe_allow_html=True)

st.title("✈️ Aircraft Design Optimization & Sensitivity Suite")
st.caption("Professional Aerospace Engineering Tool | High-Precision Weight Iteration")
st.divider()

# --- 2. Sidebar Parameters (Based on Homework Details) ---
st.sidebar.header("📊 Engineering Input Module")

with st.sidebar.expander("Payload & Crew Logistics", expanded=True):
    pax = st.number_input("Number of Passengers", value=34)
    w_pl = pax * 205 # Standard: 175 (pax) + 30 (baggage)
    w_crew = st.number_input("Crew Weight (lbs)", value=615.0)
    w_tfo = st.number_input("Trapped Fuel & Oil (lbs)", value=242.75)

with st.sidebar.expander("Mission Profile & Performance", expanded=True):
    rc = st.number_input("Cruise Range (miles)", value=1265.847)
    ld_c = st.number_input("L/D (Cruise Phase)", value=13.0)
    cp_c = st.number_input("Cp Cruise (lbs/Hp/Hr)", value=0.6)
    np_c = st.number_input("ηp (Propeller Efficiency)", value=0.85)
    
    eltr = st.number_input("Loiter Endurance (hrs)", value=0.75)
    ld_l = st.number_input("L/D (Loiter Phase)", value=16.0)
    cp_l = st.number_input("Cp Loiter", value=0.65)

# Aircraft Statistical Constants (Table 2.15)
coeff_a = 0.3774
coeff_b = 0.9647

# --- 3. Professional Engineering Engine ---
def analyze_design(wto):
    # Phase 1-4 Fractions
    f_fixed = 0.990 * 0.995 * 0.995 * 0.985
    # Phase 5: Cruise (Breguet Range - Base e)
    f_cruise = 1 / math.exp(rc / (375 * (np_c / cp_c) * ld_c))
    # Phase 6: Loiter (Simplified constant from file)
    f_loiter = 0.970 
    # Phase 7-8: Descent & Landing
    f_end = 0.985 * 0.995
    
    mff = f_fixed * f_cruise * f_loiter * f_end
    wf = wto * (1 - mff)
    
    # Empty Weight Calculation
    we_tentative = wto - wf - w_pl - w_tfo - w_crew
    # ALLOWABLE WE (Using Log10 as per official standards)
    we_allowable = 10**((math.log10(wto) - coeff_a) / coeff_b)
    
    # SENSITIVITY CALCULATIONS (Direct Partial Derivatives)
    # Range Sensitivity
    s_r_cp = -rc / cp_c
    s_r_ld = rc / ld_c
    # Endurance Sensitivity
    s_e_cp = -eltr / cp_l
    s_e_ld = eltr / ld_l

    return {
        "mff": mff, "wf": wf, "we_c": we_tentative, "we_a": we_allowable,
        "sens": {"r_cp": s_r_cp, "r_ld": s_r_ld, "e_cp": s_e_cp, "e_ld": s_e_ld}
    }

# --- 4. Main Solver & Execution ---
if st.button("🚀 EXECUTE 100% PROFESSIONAL ANALYSIS"):
    # Automatic Solver to find Equilibrium WTO
    def solver():
        low, high = 10000.0, 150000.0
        for _ in range(100):
            mid = (low + high) / 2
            res = analyze_design(mid)
            if res['we_a'] > res['we_c']: low = mid
            else: high = mid
        return mid

    final_wto = solver()
    res = analyze_design(final_wto)

    # A. Metrics Dashboard
    st.subheader("🏁 Optimization Results")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Optimized WTO", f"{final_wto:,.1f} lb")
    m2.metric("Fuel Weight (Wf)", f"{res['wf']:,.1f} lb")
    m3.metric("Empty Weight (We)", f"{res['we_c']:,.1f} lb")
    m4.metric("Fuel Fraction (Mff)", f"{res['mff']:.4f}")

    # B. Detailed Sensitivity Report (Table Logic)
    st.divider()
    st.subheader("📉 Design Sensitivity Analysis")
    sc1, sc2 = st.columns(2)
    
    with sc1:
        st.info("**Range Sensitivity (Breguet Case)**")
        st.write(f"∂R / ∂Cp: `{res['sens']['r_cp']:,.2f}` miles/unit")
        st.write(f"∂R / ∂(L/D): `{res['sens']['r_ld']:,.2f}` miles/unit")
    
    with sc2:
        st.info("**Endurance Sensitivity (Loiter Case)**")
        st.write(f"∂E / ∂Cp: `{res['sens']['e_cp']:,.4f}` hrs/unit")
        st.write(f"∂E / ∂(L/D): `{res['sens']['e_ld']:,.4f}` hrs/unit")

    # C. High-Fidelity Convergence Plot
    st.divider()
    st.subheader("📈 Weight Convergence Mapping")
    w_axis = np.linspace(final_wto*0.7, final_wto*1.3, 60)
    sweep = [analyze_design(w) for w in w_axis]
    df_plot = pd.DataFrame({
        "Gross Weight (WTO)": w_axis,
        "Tentative Empty Weight": [x['we_c'] for x in sweep],
        "Allowable Empty Weight": [x['we_a'] for x in sweep]
    })
    
    fig = px.line(df_plot, x="Gross Weight (WTO)", y=["Tentative Empty Weight", "Allowable Empty Weight"],
                  color_discrete_map={"Tentative Empty Weight": "#002D72", "Allowable Empty Weight": "#D62728"})
    fig.add_vline(x=final_wto, line_dash="dash", line_color="green", annotation_text="Converged WTO")
    fig.update_layout(plot_bgcolor='white', hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

    # D. PDF Technical Report
    def generate_pdf():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 15, "Engineering Design & Weight Analysis Report", ln=True, align='C')
        pdf.ln(10)
        pdf.set_font("Arial", '', 12)
        lines = [
            f"Final Optimized WTO: {final_wto:,.2f} lbs",
            f"Calculated Fuel Weight: {res['wf']:,.2f} lbs",
            f"Calculated Empty Weight: {res['we_c']:,.2f} lbs",
            f"Mission Fuel Fraction: {res['mff']:.4f}",
            "",
            "Sensitivity Results:",
            f"- Range Sensitivity (dR/dCp): {res['sens']['r_cp']:,.2f}",
            f"- Endurance Sensitivity (dE/dCp): {res['sens']['e_cp']:,.4f}"
        ]
        for line in lines:
            pdf.cell(0, 10, line, ln=True)
        return pdf.output(dest='S').encode('latin-1')

    pdf_report = generate_pdf()
    st.download_button("📥 DOWNLOAD TECHNICAL REPORT (PDF)", data=pdf_report, file_name="Aircraft_Technical_Analysis.pdf")

else:
    st.info("System Standby. Configuration loaded. Press 'Execute' to start the solver.")
