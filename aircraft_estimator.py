import streamlit as st
import math
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from fpdf import FPDF
import io

# --- 1. UI Configuration (Clean Excel/Corporate Style) ---
st.set_page_config(page_title="Aeronautical Design Analysis Suite", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #FFFFFF; }
    .stMetric { border: 1px solid #D1D5DB; background-color: #F9FAFB; border-radius: 4px; }
    h1, h2, h3 { color: #1E3A8A; font-family: 'Segoe UI', sans-serif; }
    .report-text { font-size: 14px; color: #374151; line-height: 1.6; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Aircraft Design & Sensitivity Control Center")
st.info("Manual WTO Control Mode | Comprehensive Engineering Insights")

# --- 2. Sidebar: Full Data Entry (All Homework Parameters) ---
st.sidebar.header("📋 Input Data Sheet")
with st.sidebar.expander("Mission Parameters", expanded=True):
    rc = st.number_input("Range (Rc) - miles", value=1265.8)
    eltr = st.number_input("Endurance (E) - hrs", value=0.75)
    pax = st.number_input("Passengers", value=34)
    w_pax = pax * 205
    w_crew = st.number_input("Wcrew (lbs)", value=615.0)

with st.sidebar.expander("Performance Ratios", expanded=True):
    ld_c = st.number_input("L/D Cruise", value=13.0)
    cp_c = st.number_input("Cp Cruise", value=0.6)
    np_c = st.number_input("ηp Cruise", value=0.85)
    m_res = st.number_input("Mres (Reserves)", value=0.05)
    m_tfo = st.number_input("Mtfo (Trapped Fuel)", value=0.005)

# --- 3. The Variable WTO Control ---
st.subheader("⚙️ Take-off Weight (WTO) Manual Adjustment")
wto_input = st.number_input("Enter/Adjust Gross Weight (WTO) - lbs", value=48550.0, step=50.0)

# --- 4. Engineering Engine (Equations 2.22 - 2.51) ---
def run_analysis(wto):
    # Constants from Table 2.15
    coeff_a, coeff_b = 0.3774, 0.9647
    
    # Fuel Fractions
    f_fixed = 0.990 * 0.995 * 0.995 * 0.985
    f_cruise = 1 / math.exp(rc / (375 * (np_c / cp_c) * ld_c))
    f_loiter = 0.970 
    f_end = 0.985 * 0.995
    mff = f_fixed * f_cruise * f_loiter * f_end
    
    # Factor C & D (Logic: Defining the design capability)
    c_val = 1 - (1 + m_res) * (1 - mff) - m_tfo
    d_val = w_pax + w_crew
    
    # Weight Verification
    wf = wto * (1 - mff)
    we_calc = wto - wf - d_val - (m_tfo * wto)
    we_allow = 10**((math.log10(wto) - coeff_a) / coeff_b) # Log10 as requested
    
    # Sensitivity F (Logic: How sensitive the airframe is to changes)
    num_f = -coeff_b * (wto**2) * (1 + m_res) * mff
    den_f = (c_val * wto * (1 - coeff_b)) - d_val
    f_factor = num_f / den_f if den_f != 0 else 0
    
    # Derivatives
    dw_dr = (f_factor * cp_c) / (375 * np_c * ld_c)
    dw_dcp = (f_factor * rc) / (375 * np_c * ld_c)
    
    return locals()

data = run_analysis(wto_input)

# --- 5. Dashboard & Excel-Style Plot ---
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📈 Numerical Results")
    st.metric("Current WTO", f"{wto_input:,.0f} lb")
    st.metric("Matching Error", f"{data['we_calc'] - data['we_allow']:,.1f} lb")
    st.metric("Sensitivity Factor (F)", f"{data['f_factor']:,.0f}")
    st.write(f"**C Factor:** {data['c_val']:.4f}")
    st.write(f"**∂WTO / ∂R:** {data['dw_dr']:.2f} lbs/mi")

with col2:
    # Excel-Style Chart using Plotly Graph Objects
    w_range = np.linspace(30000, 80000, 50)
    sweep = [run_analysis(w) for w in w_range]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=w_range, y=[x['we_calc'] for x in sweep], name='Tentative WE', line=dict(color='#1E3A8A', width=3)))
    fig.add_trace(go.Scatter(x=w_range, y=[x['we_allow'] for x in sweep], name='Allowable WE', line=dict(color='#DC2626', width=3)))
    # Intersection Point Marker
    fig.add_vline(x=wto_input, line_dash="dot", line_color="#4B5563")
    fig.update_layout(title="Weight Equilibrium Chart (Excel Style)", xaxis_title="Gross Weight (WTO)", yaxis_title="Empty Weight (WE)", 
                      plot_bgcolor='white', hovermode='x')
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#E5E7EB')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#E5E7EB')
    st.plotly_chart(fig, use_container_width=True)

# --- 6. Comprehensive PDF Explanation ---
def generate_detailed_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Comprehensive Aircraft Design Analysis Report", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "1. Objective of the Study", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.multi_cell(0, 10, "The goal is to determine the optimal Gross Weight (WTO) for a 34-passenger aircraft while ensuring the structural weight (Allowable WE) matches the weight required to carry the mission fuel and payload (Calculated WE).")
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "2. Key Parameters Explained", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.multi_cell(0, 10, f"- Factor C ({data['c_val']:.4f}): Represents the fuel-carrying efficiency. It subtracts trapped fuel and reserves from the fuel fraction.\n- Factor D ({data['d_val']:.0f} lbs): Total fixed weight (Payload + Crew).\n- Sensitivity Factor F ({data['f_factor']:,.0f}): Tells us how 'penalizing' adding weight is. A high F means a small design change causes a massive increase in WTO.")
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "3. Why Sensitivity Matters (Equations 2.49 - 2.51)", ln=True)
    pdf.multi_cell(0, 10, f"Based on our results, ∂WTO / ∂R = {data['dw_dr']:.2f}. This means for every 1 mile added to the mission range, the aircraft weight must increase by {data['dw_dr']:.2f} lbs to remain feasible. This allows engineers to make trade-off decisions between range, payload, and fuel efficiency.")
    
    return pdf.output(dest='S').encode('latin-1')

st.divider()
if st.download_button("📥 DOWNLOAD COMPREHENSIVE PDF REPORT", data=generate_detailed_pdf(), file_name="Aircraft_Technical_Analysis.pdf"):
    st.success("Report generated with full engineering explanations!")
