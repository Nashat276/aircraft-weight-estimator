import streamlit as st
import math
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from fpdf import FPDF
import io

# --- 1. AERO-INDUSTRIAL THEME ---
st.set_page_config(page_title="AeroOptimizer Pro | Executive Edition", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #F8FAFC; }
    div[data-testid="stMetric"] { background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; }
    h1, h2, h3 { color: #0F172A; font-family: 'Inter', sans-serif; }
    .stSidebar { background-color: #0F172A !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR: THE DATA VAULT (All Inputs) ---
st.sidebar.title("🛠️ Project Inputs")

with st.sidebar.expander("Mission Payload", expanded=True):
    pax = st.number_input("Passengers", value=34)
    w_pl = pax * 205
    w_crew = st.number_input("Crew Weight (lbs)", value=615.0)
    d_fixed = w_pl + w_crew

with st.sidebar.expander("Flight Profile", expanded=True):
    rc = st.number_input("Design Range (mi)", value=1265.8)
    eltr = st.number_input("Endurance (hrs)", value=0.75)
    m_res = st.number_input("Reserves (Mres)", value=0.05)
    m_tfo = st.number_input("TFO Ratio", value=0.005)

with st.sidebar.expander("Aerodynamics", expanded=True):
    ld_c = st.slider("Cruise L/D", 10.0, 20.0, 13.0)
    cp_c = st.number_input("SFC (Cp)", value=0.6)
    np_c = st.slider("Prop Eff (ηp)", 0.6, 0.95, 0.85)

# --- 3. CORE LOGIC ENGINE ---
def run_solver(wto):
    # Phase Fractions
    f_p = 0.990 * 0.995 * 0.995 * 0.985
    f_c = 1 / math.exp(rc / (375 * (np_c / cp_c) * ld_c))
    f_l = 0.970 
    f_e = 0.985 * 0.995
    mff = f_p * f_c * f_l * f_e
    
    # Matching Logic
    wf = wto * (1 - mff)
    we_req = wto - wf - d_fixed - (m_tfo * wto)
    we_allow = 10**((math.log10(wto) - 0.3774) / 0.9647)
    
    # Sensitivity (Growth Factors)
    c_val = 1 - (1 + m_res) * (1 - mff) - m_tfo
    num_f = -0.9647 * (wto**2) * (1 + m_res) * mff
    den_f = (c_val * wto * (1 - 0.9647)) - d_fixed
    f_growth = num_f / den_f if den_f != 0 else 0
    
    # Derivatives
    dw_dr = (f_growth * cp_c) / (375 * np_c * ld_c)
    dw_dcp = (f_growth * rc) / (375 * np_c * ld_c)
    
    return locals()

# --- 4. MAIN INTERFACE ---
st.title("Aeronautical Weight & Sensitivity Dashboard")
st.write("Professional MDAO Environment for Conceptual Sizing")
st.divider()

wto_var = st.select_slider("Select WTO for Analysis (lbs)", options=np.round(np.arange(30000, 80005, 5), 2), value=48550.0)
res = run_solver(wto_var)

# Results Matrix
m1, m2, m3, m4 = st.columns(4)
m1.metric("Fuel Fraction (Mff)", f"{res['mff']:.4f}")
m2.metric("Growth Factor (F)", f"{res['f_growth']:,.2f}")
m3.metric("Matching Error", f"{res['we_req'] - res['we_allow']:,.1f} lb")
m4.metric("Sensitivity dW/dR", f"{res['dw_dr']:.2f}")

# --- 5. ADVANCED ENGINEERING GRAPH ---
st.subheader("Weight Convergence & Feasibility Map")
w_axis = np.linspace(35000, 75000, 100)
sweep = [run_solver(w) for w in w_axis]

fig = go.Figure()
# Required WE Curve
fig.add_trace(go.Scatter(x=w_axis, y=[x['we_req'] for x in sweep], name='Mission Required WE', 
                         line=dict(color='#0F172A', width=3), fill='tonexty', fillcolor='rgba(15, 23, 42, 0.05)'))
# Allowable WE Curve
fig.add_trace(go.Scatter(x=w_axis, y=[x['we_allow'] for x in sweep], name='Structural Allowable WE', 
                         line=dict(color='#E11D48', width=3, dash='dash')))

# Interaction Point Marker
fig.add_trace(go.Scatter(x=[wto_var], y=[res['we_req']], mode='markers+text', name='Current Selection',
                         marker=dict(size=12, color='#10B981'), text=["Design Point"], textposition="top center"))

fig.update_layout(height=600, plot_bgcolor='white', hovermode='x unified',
                  xaxis=dict(showgrid=True, gridcolor='#F1F5F9', title="Gross Weight (WTO) [lbs]"),
                  yaxis=dict(showgrid=True, gridcolor='#F1F5F9', title="Empty Weight (WE) [lbs]"),
                  legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
st.plotly_chart(fig, use_container_width=True)

# --- 6. UNIFIED PDF DOCUMENT GENERATOR ---
def generate_master_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    
    # Header
    pdf.set_fill_color(15, 23, 42)
    pdf.rect(0, 0, 210, 40, 'F')
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", 'B', 20)
    pdf.cell(0, 20, "AIRCRAFT DESIGN MASTER REPORT", ln=True, align='C')
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 5, "Generated via AeroOptimizer Pro | Precision Engineering Suite", ln=True, align='C')
    
    pdf.set_text_color(0, 0, 0)
    pdf.ln(25)
    
    # Section 1: Inputs
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "1. MISSION CONFIGURATION & INPUTS", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.cell(95, 8, f"- Design Range: {rc} miles", ln=0)
    pdf.cell(95, 8, f"- Passenger Count: {pax}", ln=1)
    pdf.cell(95, 8, f"- Cruise L/D: {ld_c}", ln=0)
    pdf.cell(95, 8, f"- SFC (Cp): {cp_c} lbs/hp/hr", ln=1)
    pdf.ln(5)
    
    # Section 2: Core Calculations
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "2. CORE CALCULATIONS & GROWTH FACTORS", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.cell(95, 8, f"- Final Fuel Fraction (Mff): {data['mff']:.4f}", ln=0)
    pdf.cell(95, 8, f"- Growth Factor (F): {data['f_growth']:,.2f}", ln=1)
    pdf.cell(95, 8, f"- Efficiency Factor (C): {data['c_val']:.4f}", ln=0)
    pdf.cell(95, 8, f"- Fixed Asset Weight (D): {d_fixed:,.1f} lbs", ln=1)
    pdf.ln(5)

    # Section 3: Convergence Analysis
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "3. WEIGHT CONVERGENCE SUMMARY", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 8, f"Selected Take-off Weight: {wto_var:,.1f} lbs", ln=True)
    pdf.cell(0, 8, f"Mission Required Empty Weight: {data['we_req']:,.1f} lbs", ln=True)
    pdf.cell(0, 8, f"Structural Allowable Empty Weight: {data['we_allow']:,.1f} lbs", ln=True)
    error = data['we_req'] - data['we_allow']
    pdf.cell(0, 8, f"Convergence Error (Delta): {error:,.1f} lbs", ln=True)
    pdf.ln(5)
    
    # Section 4: Sensitivity Derivatives
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "4. DESIGN SENSITIVITY MATRIX", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 8, f"- Weight Penalty per Mile (dW/dR): {data['dw_dr']:.4f} lbs/mi", ln=True)
    pdf.cell(0, 8, f"- Weight Penalty per SFC Unit (dW/dCp): {data['dw_dcp']:.2f} lbs/unit", ln=True)
    
    return pdf.output(dest='S').encode('latin-1', 'ignore')

st.divider()
st.download_button("📥 DOWNLOAD COMPLETE MASTER REPORT (PDF)", 
                   data=generate_master_pdf(res), 
                   file_name="Aircraft_Master_Design_Package.pdf")
