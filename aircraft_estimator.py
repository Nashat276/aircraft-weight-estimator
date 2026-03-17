import streamlit as st
import math
import numpy as np
import plotly.graph_objects as go
from fpdf import FPDF

# --- 1. RADICAL UI REDESIGN (AERO-MODERN) ---
st.set_page_config(page_title="AeroOptimizer Pro | Sizing Suite", layout="wide")

st.markdown("""
    <style>
    /* Dark Aero Theme */
    .main { background-color: #0F172A; color: #F8FAFC; }
    
    /* Sidebar Customization - Fixed Text Visibility */
    section[data-testid="stSidebar"] {
        background-color: #1E293B !important;
        border-right: 1px solid #334155;
    }
    section[data-testid="stSidebar"] label, section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2 {
        color: #38BDF8 !important; /* Sky Blue for clarity */
        font-weight: 600 !important;
    }
    
    /* Input Boxes */
    .stNumberInput input {
        background-color: #0F172A !important;
        color: #F8FAFC !important;
        border: 1px solid #38BDF8 !important;
    }

    /* Professional Cards */
    div[data-testid="stMetric"] {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 20px;
    }
    
    h1, h2, h3 { color: #38BDF8; font-family: 'Inter', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR: DATA VAULT (Unified Inputs) ---
st.sidebar.title("✈️ Design Control Center")

with st.sidebar:
    st.header("📍 Primary Sizing Variable")
    wto_input = st.number_input("Gross Weight (WTO) - lbs", value=48550.0, step=10.0)
    
    st.divider()
    
    with st.expander("📦 Payload & Weights", expanded=True):
        pax = st.number_input("Passenger Count", value=34)
        w_pax_total = pax * 205
        w_crew = st.number_input("Crew Weight", value=615.0)
        d_val = w_pax_total + w_crew # Calculated D Factor

    with st.expander("🚀 Cruise Phase (Table 2.20)", expanded=True):
        rc = st.number_input("Range (Rc) - miles", value=1265.8)
        ld_c = st.number_input("L/D (Cruise)", value=13.0)
        cp_c = st.number_input("SFC (Cp)", value=0.6)
        np_c = st.number_input("Prop Efficiency (ηp)", value=0.85)

    with st.expander("🛡️ Loiter & Reserves", expanded=False):
        eltr = st.number_input("Endurance (E) - hrs", value=0.75)
        ld_l = st.number_input("L/D (Loiter)", value=16.0)
        cp_l = st.number_input("SFC (Loiter)", value=0.65)
        m_res = st.number_input("Reserve Ratio", value=0.05)
        m_tfo = st.number_input("TFO Ratio", value=0.005)

# --- 3. PHYSICS ENGINE (TABLE 2.20 ACCURACY) ---
def compute_sizing(wto):
    # Mission Fuel Fractions
    f_start_climb = 0.990 * 0.995 * 0.995 * 0.985 
    f_cruise = 1 / math.exp(rc / (375 * (np_c / cp_c) * ld_c))
    f_loiter = 1 / math.exp(eltr / (375 * (0.80 / cp_l) * ld_l)) # ηp_loiter = 0.80
    f_land = 0.985 * 0.995
    mff = f_start_climb * f_cruise * f_loiter * f_land
    
    # Efficiency Factor (C) - Equation 2.22
    c_val = 1 - (1 + m_res) * (1 - mff) - m_tfo
    
    # Weight Matching Logic
    wf = wto * (1 - mff)
    we_req = wto - wf - d_val - (m_tfo * wto)
    we_allow = 10**((math.log10(wto) - 0.3774) / 0.9647)
    
    # Growth Factor (F) - Ref Table 2.20
    # Calculates dWTO / dD (Sensitivity to Fixed Weight)
    num_f = -0.9647 * (wto**2) * (1 + m_res) * mff
    den_f = (c_val * wto * (1 - 0.9647)) - d_val
    f_growth = num_f / den_f if den_f != 0 else 0
    
    # Sensitivity Derivatives (Eq 2.49 - 2.51)
    dw_dr = (f_growth * cp_c) / (375 * np_c * ld_c)
    dw_dcp = (f_growth * rc) / (375 * np_c * ld_c)
    
    # Returning all variables to avoid KeyError
    return {
        "mff": mff, "f_growth": f_growth, "c_val": c_val,
        "we_req": we_req, "we_allow": we_allow, "wf": wf,
        "dw_dr": dw_dr, "dw_dcp": dw_dcp, "d_val": d_val
    }

# Execute calculation
res = compute_sizing(wto_input)

# --- 4. MAIN DASHBOARD ---
st.title("🛡️ AeroOptimizer | Conceptual Design Suite")
st.markdown("Professional Multidisciplinary Analysis (MDAO) for Aircraft Sizing")
st.divider()

# Top Metrics
m1, m2, m3, m4 = st.columns(4)
m1.metric("Mission Mff", f"{res['mff']:.4f}")
m2.metric("Growth Factor (F)", f"{res['f_growth']:,.2f}")
m3.metric("Current Error", f"{res['we_req'] - res['we_allow']:,.1f} lb")
m4.metric("Efficiency (C)", f"{res['c_val']:.4f}")

st.divider()

# Graphical Analysis
col_plot, col_log = st.columns([2, 1])

with col_plot:
    st.subheader("📊 Convergence & Feasibility Map")
    w_axis = np.linspace(35000, 75000, 100)
    sweep = [compute_sizing(w) for w in w_axis]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=w_axis, y=[x['we_req'] for x in sweep], name='Mission Required Weight', line=dict(color='#38BDF8', width=4)))
    fig.add_trace(go.Scatter(x=w_axis, y=[x['we_allow'] for x in sweep], name='Structural Limit', line=dict(color='#F87171', width=4, dash='dot')))
    fig.add_trace(go.Scatter(x=[wto_input], y=[res['we_req']], mode='markers', marker=dict(size=15, color='#34D399'), name='Current Design'))
    
    fig.update_layout(plot_bgcolor='#0F172A', paper_bgcolor='#0F172A', font_color='#F8FAFC', margin=dict(l=0,r=0,t=20,b=0))
    fig.update_xaxes(showgrid=True, gridcolor='#334155')
    fig.update_yaxes(showgrid=True, gridcolor='#334155')
    st.plotly_chart(fig, use_container_width=True)

with col_log:
    st.subheader("📑 Design Summary")
    st.write(f"**Payload Asset (D):** {res['d_val']:,.1f} lbs")
    st.write(f"**Total Fuel Weight:** {res['wf']:,.1f} lbs")
    st.info("Intersection point (where Error = 0) represents the technically optimal WTO.")

st.divider()

# Sensitivity Table 2.20
st.subheader("📉 Design Sensitivity Matrix (Ref Table 2.20)")
s1, s2 = st.columns(2)
s1.metric("Range Penalty (dW/dR)", f"{res['dw_dr']:.4f} lbs/mi")
s2.metric("SFC Penalty (dW/dCp)", f"{res['dw_dcp']:,.1f} lbs/unit")

# --- 5. MASTER PDF REPORT (PRO FORMATTING) ---
def generate_master_pdf(d):
    pdf = FPDF()
    pdf.add_page()
    
    # Frame & Style
    pdf.set_draw_color(56, 189, 248)
    pdf.rect(5, 5, 200, 287)
    
    # Header
    pdf.set_fill_color(30, 41, 59)
    pdf.rect(5, 5, 200, 45, 'F')
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", 'B', 22)
    pdf.cell(0, 20, "AIRCRAFT MASTER DESIGN PACKAGE", ln=True, align='C')
    pdf.set_font("Arial", 'I', 11)
    pdf.cell(0, 10, "Technical Specification & Weight Convergence Report", ln=True, align='C')
    
    pdf.set_text_color(0, 0, 0)
    pdf.ln(25)
    
    # Sections with Explanations
    pdf.set_font("Arial", 'B', 14)
    pdf.set_fill_color(241, 245, 249)
    pdf.cell(0, 10, " 1. SYSTEM METHODOLOGY", ln=True, fill=True)
    pdf.set_font("Arial", '', 11)
    pdf.multi_cell(0, 7, (
        "This sizing analysis utilizes the multidisciplinary iteration of Take-off Weight (WTO). "
        "The process establishes equilibrium between mission-required empty weight (derived from fuel fractions) "
        "and allowable structural empty weight (based on statistical log-models). This ensures the airframe "
        "is both missions-capable and structurally sound."
    ))
    
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, " 2. DESIGN CONFIGURATION & INPUTS", ln=True, fill=True)
    pdf.set_font("Arial", '', 11)
    pdf.cell(95, 8, f"- Analysis WTO: {wto_input:,.1f} lbs", ln=0)
    pdf.cell(95, 8, f"- Design Range: {rc} miles", ln=1)
    pdf.cell(95, 8, f"- Total Payload (D Factor): {d_val:,.1f} lbs", ln=0)
    pdf.cell(95, 8, f"- Cruise L/D: {ld_c}", ln=1)
    
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, " 3. SENSITIVITY DERIVATIVES (TABLE 2.20)", ln=True, fill=True)
    pdf.set_font("Arial", '', 11)
    pdf.multi_cell(0, 7, (
        f"The calculated Growth Factor (F = {d['f_growth']:.2f}) represents the sensitivity of the entire airframe. "
        f"Based on our sensitivity analysis, the range derivative (dW/dR) is {d['dw_dr']:.4f} lbs/mile, "
        "which quantifies the weight penalty for extending the aircraft's mission profile."
    ))

    return pdf.output(dest='S').encode('latin-1', 'ignore')

st.divider()
st.download_button("📥 DOWNLOAD COMPREHENSIVE DESIGN DOCUMENT (PDF)", data=generate_master_pdf(res), file_name="Aero_Master_Report.pdf")
