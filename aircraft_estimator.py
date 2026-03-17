import streamlit as st
import math
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from fpdf import FPDF

# --- 1. SETTINGS & PROFESSIONAL THEME ---
st.set_page_config(page_title="Aircraft Design Suite | Professional Edition", layout="wide")

st.markdown("""
    <style>
    .stMetric { border: 1px solid #E2E8F0; background-color: #F8FAFC; border-radius: 8px; padding: 15px; }
    .main { background-color: #FFFFFF; }
    h1, h2, h3 { color: #0F172A; font-family: 'Inter', sans-serif; font-weight: 700; }
    .stSidebar { background-color: #F1F5F9; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR: MISSION DATA INPUTS (Boeing/Airbus Specs) ---
st.sidebar.header("🛠️ Mission Configuration")

with st.sidebar.expander("1. Payload & Logistics", expanded=True):
    pax = st.sidebar.number_input("Passenger Count", value=34)
    w_pax_payload = pax * 205 # Standard 175lb + 30lb baggage
    w_crew = st.sidebar.number_input("Crew Weight (lbs)", value=615.0)
    d_fixed = w_pax_payload + w_crew 

with st.sidebar.expander("2. Flight Profile", expanded=True):
    rc = st.sidebar.number_input("Design Range (miles)", value=1265.8)
    eltr = st.sidebar.number_input("Loiter Endurance (hrs)", value=0.75)
    m_res = st.sidebar.number_input("Reserve Fuel Ratio (Mres)", value=0.05)
    m_tfo = st.sidebar.number_input("Trapped Fuel/Oil (Mtfo)", value=0.005)

with st.sidebar.expander("3. Propulsion & Aero", expanded=True):
    ld_c = st.sidebar.number_input("L/D (Cruise)", value=13.0)
    cp_c = st.sidebar.number_input("Cp (lbs/Hp/Hr)", value=0.6)
    np_c = st.sidebar.number_input("Prop Efficiency (ηp)", value=0.85)
    ld_l = st.sidebar.number_input("L/D (Loiter)", value=16.0)
    cp_l = st.sidebar.number_input("Cp (Loiter)", value=0.65)

# Statistical Constants (Table 2.15)
coeff_a, coeff_b = 0.3774, 0.9647

# --- 3. MAIN INTERFACE ---
st.title("✈️ Aeronautical Systems Design & Sensitivity Dashboard")
st.markdown("---")

st.subheader("⚙️ Iteration Control: Variable Gross Weight (WTO)")
wto_input = st.slider("Select Gross Take-off Weight (WTO) for convergence check", 
                     min_value=30000.0, max_value=80000.0, value=48550.0, step=50.0)

# --- 4. CALCULATION ENGINE ---
def run_aerospace_logic(wto):
    # Mission Fuel Fractions
    f_phases = 0.990 * 0.995 * 0.995 * 0.985 
    f_cruise = 1 / math.exp(rc / (375 * (np_c / cp_c) * ld_c))
    f_loiter = 0.970 
    f_land = 0.985 * 0.995
    mff = f_phases * f_cruise * f_loiter * f_land
    
    # Weight Matching
    wf = wto * (1 - mff)
    we_req = wto - wf - d_fixed - (m_tfo * wto)
    we_allow = 10**((math.log10(wto) - coeff_a) / coeff_b)
    
    # Efficiency & Growth Factors
    c_val = 1 - (1 + m_res) * (1 - mff) - m_tfo
    num_f = -coeff_b * (wto**2) * (1 + m_res) * mff
    den_f = (c_val * wto * (1 - coeff_b)) - d_fixed
    f_growth = num_f / den_f if den_f != 0 else 0
    
    # Sensitivity Derivatives
    dw_dr = (f_growth * cp_c) / (375 * np_c * ld_c)
    dw_dcp = (f_growth * rc) / (375 * np_c * ld_c)
    
    return {
        "mff": mff, "wf": wf, "we_req": we_req, "we_allow": we_allow,
        "c_val": c_val, "f_growth": f_growth, "dw_dr": dw_dr, "dw_dcp": dw_dcp
    }

data = run_aerospace_logic(wto_input)

# --- 5. VISUALIZING RESULTS ---
st.header("📊 Performance & Weight Convergence")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Fuel Fraction (Mff)", f"{data['mff']:.4f}")
c2.metric("Growth Factor (F)", f"{data['f_growth']:,.2f}")
c3.metric("Efficiency (C)", f"{data['c_val']:.4f}")
c4.metric("Matching Error", f"{data['we_req'] - data['we_allow']:,.1f} lb")

st.divider()

col_graph, col_stats = st.columns([2, 1])

with col_graph:
    w_axis = np.linspace(35000, 75000, 100)
    sweep = [run_aerospace_logic(w) for w in w_axis]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=w_axis, y=[x['we_req'] for x in sweep], name='Required Empty Weight (Mission)', line=dict(color='#2563EB', width=3)))
    fig.add_trace(go.Scatter(x=w_axis, y=[x['we_allow'] for x in sweep], name='Allowable Empty Weight (Structure)', line=dict(color='#DC2626', width=3)))
    fig.add_vline(x=wto_input, line_dash="dot", line_color="#475569", annotation_text="Selected Design Point")
    fig.update_layout(title="Weight Equilibrium Chart", xaxis_title="Gross Weight (WTO) [lbs]", yaxis_title="Empty Weight (WE) [lbs]", 
                      plot_bgcolor='white', hovermode='x unified', legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    fig.update_xaxes(showgrid=True, gridcolor='#F1F5F9')
    fig.update_yaxes(showgrid=True, gridcolor='#F1F5F9')
    st.plotly_chart(fig, use_container_width=True)

with col_stats:
    st.info("**Design Feasibility Status**")
    st.write(f"Mission Required WE: **{data['we_req']:,.1f} lbs**")
    st.write(f"Structural Allowable WE: **{data['we_allow']:,.1f} lbs**")
    st.write("---")
    st.write(f"Fixed Asset Weight (D): **{d_fixed:,.1f} lbs**")

st.divider()
st.header("📉 Sensitivity Analysis Matrix")
s1, s2 = st.columns(2)
with s1:
    st.metric("∂WTO / ∂Range (lbs/mile)", f"{data['dw_dr']:.2f}")
    st.caption("Weight penalty per nautical mile added to design range.")
with s2:
    st.metric("∂WTO / ∂Cp (lbs/unit)", f"{data['dw_dcp']:.2f}")
    st.caption("Weight penalty for fuel consumption inefficiency.")

# --- 6. PDF REPORT GENERATOR ---
def generate_pdf_pro():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 15, "Aircraft Technical Design & Sensitivity Report", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "1. Executive Summary", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.multi_cell(0, 7, f"At the selected WTO of {wto_input:,.0f} lbs, the aircraft exhibits a growth factor (F) of {data['f_growth']:.2f}. "
                          "The design is technically converged when the Required Empty Weight matches the Allowable Empty Weight.")
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "2. Key Sensitivities", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 8, f"- Weight impact per mile (dW/dR): {data['dw_dr']:.2f} lbs/mi", ln=True)
    pdf.cell(0, 8, f"- Fuel efficiency impact (dW/dCp): {data['dw_dcp']:.2f} lbs/unit", ln=True)
    return pdf.output(dest='S').encode('latin-1', 'ignore')

st.divider()
st.download_button("📥 GENERATE TECHNICAL DOCUMENTATION (PDF)", 
                   data=generate_pdf_pro(), 
                   file_name="Aircraft_Technical_Report.pdf")
