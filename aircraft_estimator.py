import streamlit as st
import math
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from fpdf import FPDF

# --- 1. AERO-INDUSTRIAL THEME ---
st.set_page_config(page_title="AeroOptimizer Pro | JUST Engineering", layout="wide")

st.markdown("""
    <style>
    /* Main Background */
    .main { background-color: #F1F5F9; }
    
    /* Metric Cards Styling */
    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    }
    
    /* Headers Styling */
    h1, h2, h3 { color: #1E293B; font-family: 'Inter', sans-serif; letter-spacing: -0.025em; }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] { background-color: #0F172A; color: white; }
    section[data-testid="stSidebar"] .stMarkdown p { color: #94A3B8; }
    
    /* Tabs & Divider */
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: transparent; border-radius: 4px 4px 0px 0px; font-weight: 600; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR: THE CONTROL CENTER ---
st.sidebar.title("✈️ AeroOptimizer Pro")
st.sidebar.markdown("Conceptual Design Suite v3.0")
st.sidebar.divider()

with st.sidebar:
    st.header("📍 Mission Constraints")
    rc = st.number_input("Design Range (miles)", value=1265.8, help="Cruise distance requirement")
    pax = st.number_input("Passenger Payload", value=34)
    w_pl = pax * 205
    w_crew = st.number_input("Crew Weight (lbs)", value=615.0)
    
    st.header("⚙️ Performance Ratios")
    ld_c = st.slider("L/D Ratio (Cruise)", 10.0, 25.0, 13.0)
    cp_c = st.number_input("SFC (Cp) - lbs/hp/hr", value=0.6)
    np_c = st.slider("Propeller Efficiency (ηp)", 0.6, 0.95, 0.85)
    
    st.header("🛡️ Safety Factors")
    m_res = st.selectbox("Reserve Fuel Ratio", [0.03, 0.05, 0.07], index=1)
    m_tfo = st.number_input("TFO Ratio", value=0.005, format="%.3f")

# Statistical Base (JUST Standards)
coeff_a, coeff_b = 0.3774, 0.9647

# --- 3. LOGIC ENGINE ---
def calculate_aero(wto):
    f_p = 0.990 * 0.995 * 0.995 * 0.985
    f_c = 1 / math.exp(rc / (375 * (np_c / cp_c) * ld_c))
    f_l = 0.970 
    f_e = 0.985 * 0.995
    mff = f_p * f_c * f_l * f_e
    
    c_val = 1 - (1 + m_res) * (1 - mff) - m_tfo
    d_val = w_pl + w_crew
    
    wf = wto * (1 - mff)
    we_req = wto - wf - d_val - (m_tfo * wto)
    we_allow = 10**((math.log10(wto) - coeff_a) / coeff_b)
    
    num_f = -coeff_b * (wto**2) * (1 + m_res) * mff
    den_f = (c_val * wto * (1 - coeff_b)) - d_val
    f_growth = num_f / den_f if den_f != 0 else 0
    
    dw_dr = (f_growth * cp_c) / (375 * np_c * ld_c)
    dw_dcp = (f_growth * rc) / (375 * np_c * ld_c)
    
    return locals()

# --- 4. MAIN CONTENT AREA ---
st.title("Conceptual Weight & Sensitivity Suite")
st.write("Professional Multidisciplinary Analysis for Fixed-Wing Aircraft.")

# Top Control Card
st.divider()
col_ctrl1, col_ctrl2 = st.columns([2, 1])
with col_ctrl1:
    wto_var = st.select_slider("Select Take-off Weight (WTO) for Equilibrium Analysis", 
                              options=np.round(np.arange(30000, 80005, 5), 2), value=48550.0)
with col_ctrl2:
    st.markdown("### Selection Summary")
    st.write(f"Testing WTO: **{wto_var:,.1f} lbs**")

data = calculate_aero(wto_var)

# TABS FOR ORGANIZED RESULTS
tab1, tab2, tab3 = st.tabs(["🚀 Mission Convergence", "📉 Sensitivity Matrix", "📄 Detailed Logs"])

with tab1:
    st.subheader("Weight Balance & Iteration")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Fuel Fraction (Mff)", f"{data['mff']:.4f}")
    m2.metric("Growth Factor (F)", f"{data['f_growth']:,.2f}")
    m3.metric("Required WE", f"{data['we_req']:,.1f} lb")
    m4.metric("Allowable WE", f"{data['we_allow']:,.1f} lb")

    # High-Definition Plot
    w_axis = np.linspace(35000, 75000, 100)
    sweep = [calculate_aero(w) for w in w_axis]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=w_axis, y=[x['we_req'] for x in sweep], name='Mission Required WE', line=dict(color='#2563EB', width=4)))
    fig.add_trace(go.Scatter(x=w_axis, y=[x['we_allow'] for x in sweep], name='Structural Allowable WE', line=dict(color='#E11D48', width=4)))
    fig.add_vline(x=wto_var, line_dash="dot", line_color="#475569")
    fig.update_layout(height=500, margin=dict(l=20, r=20, t=40, b=20), plot_bgcolor='white', hovermode='x unified')
    fig.update_xaxes(showgrid=True, gridcolor='#F1F5F9')
    fig.update_yaxes(showgrid=True, gridcolor='#F1F5F9')
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Design Sensitivity Matrix")
    c_s1, c_s2 = st.columns(2)
    with c_s1:
        st.write("#### 📏 Range Impact")
        st.metric("∂WTO / ∂Range", f"{data['dw_dr']:.2f} lbs/mi")
        st.caption("Weight increase for every additional nautical mile of mission range.")
    with c_s2:
        st.write("#### ⛽ Efficiency Impact")
        st.metric("∂WTO / ∂Cp", f"{data['dw_dcp']:.2f} lbs/unit")
        st.caption("Weight penalty for fuel consumption inefficiency (SFC).")

with tab3:
    st.subheader("Raw Intermediate Calculations")
    col_raw1, col_raw2 = st.columns(2)
    with col_raw1:
        st.json({"Efficiency_C": data['c_val'], "Payload_D": data['d_val'], "Fuel_Weight": data['wf']})
    with col_raw2:
        st.write("**Verification Note:**")
        st.write("Convergence is achieved when **Required WE** minus **Allowable WE** equals zero.")

# --- 5. REPORT EXPORT ---
st.divider()
def export_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 15, "Aviation Technical Analysis Report", ln=True, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Analysis for WTO: {wto_var:,.1f} lbs", ln=True)
    pdf.cell(0, 10, f"Growth Factor F: {data['f_growth']:.2f}", ln=True)
    pdf.cell(0, 10, f"Sensitivity dW/dR: {data['dw_dr']:.2f} lbs/mi", ln=True)
    return pdf.output(dest='S').encode('latin-1', 'ignore')

st.download_button("📥 Export Professional PDF Report", data=export_pdf(), file_name="Technical_Design_Analysis.pdf")
