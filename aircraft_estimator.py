import streamlit as st
import math
import numpy as np
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import io

# --- 1. UI Configuration (Clean Corporate Style) ---
st.set_page_config(page_title="AeroDesign Solver Pro", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #F8F9FA; color: #1A202C; }
    .stMetric { background-color: white; border-left: 5px solid #0056b3; border-radius: 4px; padding: 15px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
    h1, h2, h3 { color: #002D72; }
    .stButton>button { background-color: #002D72; color: white; height: 3em; font-weight: bold; width: 100%; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

st.title("✈️ Aircraft Design Optimization & Sensitivity Tool")
st.markdown("---")

# --- 2. Input Parameters from Homework 1 ---
st.sidebar.header("🕹️ Engineering Data Entry")

with st.sidebar.expander("Mission Payload & Crew", expanded=True):
    pax = st.number_input("Number of Passengers", value=34)
    w_pl = pax * (175 + 30) # 6970 lbs per file
    w_crew = st.number_input("Crew Weight (Wcrew)", value=615.0)
    w_tfo = st.number_input("Trapped Fuel & Oil (Wtfo)", value=242.75)

with st.sidebar.expander("Cruise & Loiter Specs", expanded=True):
    rc = st.number_input("Range (Rc) - Statute Miles", value=1265.847)
    ld_c = st.number_input("L/D Cruise", value=13.0)
    cp_c = st.number_input("Cp Cruise (lbs/Hp/Hr)", value=0.6)
    np_c = st.number_input("Prop Efficiency (ηp)", value=0.85)
    
    eltr = st.number_input("Loiter Endurance (hrs)", value=0.75)
    ld_l = st.number_input("L/D Loiter", value=16.0)
    cp_l = st.number_input("Cp Loiter", value=0.65)
    np_l = st.number_input("ηp Loiter", value=0.80)

# Statistical Constants (Source: Table 2.15)
coeff_a = 0.3774
coeff_b = 0.9647

# --- 3. Calculation Core (Verified Formulas) ---
def compute_design(wto):
    # Phase 1-4: (Standard Fractions)
    f_fixed = 0.990 * 0.995 * 0.995 * 0.985
    # Phase 5: Cruise (Breguet Range - Natural Log base exp)
    f_cruise = 1 / math.exp(rc / (375 * (np_c / cp_c) * ld_c))
    # Phase 6: Loiter (Simplified as 0.970 in your file)
    f_loiter = 0.970 
    # Phase 7-8: (Standard Fractions)
    f_end = 0.985 * 0.995
    
    mff = f_fixed * f_cruise * f_loiter * f_end
    wf = wto * (1 - mff)
    
    # Empty Weight Logic
    we_calc = wto - wf - w_pl - w_tfo - w_crew
    # ALLOWABLE WE (Using Log10 as requested)
    we_allow = 10**((math.log10(wto) - coeff_a) / coeff_b)
    
    # SENSITIVITY CALCULATIONS (From Page 2 of File)
    # Range Case Derivatives
    dr_dcp = -rc / cp_c
    dr_dld = rc / ld_c
    dr_dnp = -rc / np_c # Simplified derivative
    
    # Endurance Case Derivatives
    de_dcp = -eltr / cp_l
    de_dld = eltr / ld_l

    return {
        "mff": mff, "wf": wf, "we_c": we_calc, "we_a": we_allow,
        "sens": {"dr_dcp": dr_dcp, "dr_dld": dr_dld, "de_dcp": de_dcp, "de_dld": de_dld}
    }

# --- 4. Main Solver & Dashboard ---
if st.button("🚀 RUN COMPLETE OPTIMIZATION & SENSITIVITY"):
    # Iterative Solver to find Equilibrium WTO
    def solve_wto():
        w = 10000.0
        for _ in range(100):
            res = compute_design(w)
            # Simple iteration to converge weights
            w = w + (res['we_a'] - res['we_c']) * 1.2
        return w

    final_wto = solve_wto()
    data = compute_design(final_wto)

    # A. Executive Summary
    st.subheader("📊 Final Design Convergence")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Optimized WTO", f"{final_wto:,.1f} lb")
    m2.metric("Total Fuel (Wf)", f"{data['wf']:,.1f} lb")
    m3.metric("Empty Weight (We)", f"{data['we_c']:,.1f} lb")
    m4.metric("Fuel Fraction (Mff)", f"{data['mff']:.4f}")

    # B. Detailed Sensitivity Table (The requested update)
    st.divider()
    st.subheader("📉 Detailed Sensitivity Analysis (Breguet Derivatives)")
    s_col1, s_col2 = st.columns(2)
    
    with s_col1:
        st.info("**Range Case Analysis**")
        st.write(f"∂R / ∂Cp: `{data['sens']['dr_dcp']:,.2f}` miles/unit")
        st.write(f"∂R / ∂(L/D): `{data['sens']['dr_dld']:,.2f}` miles/unit")
        st.caption("How Range changes per unit change in Cruise parameters.")

    with s_col2:
        st.info("**Endurance Case Analysis**")
        st.write(f"∂E / ∂Cp: `{data['sens']['de_dcp']:,.4f}` hrs/unit")
        st.write(f"∂E / ∂(L/D): `{data['sens']['de_dld']:,.4f}` hrs/unit")
        st.caption("How Loiter time changes per unit change in Loiter parameters.")

    # C. High-Resolution Graphics
    st.divider()
    st.subheader("📈 Visualization of Design Space")
    w_sweep = np.linspace(final_wto*0.7, final_wto*1.3, 50)
    sweep_results = [compute_design(w) for w in w_sweep]
    
    df_plot = pd.DataFrame({
        "Take-off Weight (WTO)": w_sweep,
        "Tentative Empty Weight": [r['we_c'] for r in sweep_results],
        "Allowable Empty Weight": [r['we_a'] for r in sweep_results]
    })
    
    fig = px.line(df_plot, x="Take-off Weight (WTO)", y=["Tentative Empty Weight", "Allowable Empty Weight"],
                  title="Weight Convergence Plot (Finding the Equilibrium Point)",
                  color_discrete_sequence=["#002D72", "#D62728"])
    fig.add_vline(x=final_wto, line_dash="dash", line_color="green", annotation_text="Optimum WTO")
    fig.update_layout(hovermode="x unified", plot_bgcolor='white')
    st.plotly_chart(fig, use_container_width=True)

    # D. Professional PDF Generator
    def generate_report():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, "Technical Aircraft Design Report", ln=True, align='C')
        pdf.ln(10)
        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 10, f"Optimized Take-off Weight: {final_wto:,.2f} lbs", ln=True)
        pdf.cell(0, 10, f"Sensitivity dR/dCp: {data['sens']['dr_dcp']:,.2f}", ln=True)
        pdf.cell(0, 10, f"Sensitivity dE/dCp: {data['sens']['de_dcp']:,.4f}", ln=True)
        return pdf.output(dest='S').encode('latin-1')

    pdf_bytes = generate_report()
    st.download_button("📥 Download Technical Report (PDF)", data=pdf_bytes, file_name="Design_Report.pdf")

else:
    st.info("System Ready. Please check mission parameters and execute the solver.")
