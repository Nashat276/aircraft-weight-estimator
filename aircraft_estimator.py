import streamlit as st
import math
import numpy as np
import plotly.graph_objects as go
from fpdf import FPDF

# --- 1. SETTINGS & STYLING (Professional Dashboard) ---
st.set_page_config(page_title="AeroOptimizer | Engineering Suite", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0E1117; color: #E2E8F0; }
    section[data-testid="stSidebar"] { background-color: #161B22 !important; border-right: 1px solid #30363D; }
    /* Metric Cards */
    div[data-testid="stMetric"] {
        background: #1C2128;
        border: 1px solid #30363D;
        border-radius: 8px;
        padding: 15px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
    }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #161B22;
        border-radius: 4px 4px 0 0;
        padding: 10px 20px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] { background-color: #58A6FF !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SOLVER ENGINE (MDAO Logic) ---
def aircraft_solver(wto_guess, range_mi, sfc, ld_c, pax, crew_w, ld_l, endur):
    # Constants (Standard Aero Logic)
    m_res, m_tfo = 0.05, 0.005
    eta_p = 0.85
    
    # Payload Calculation (D-Factor)
    d_val = (pax * 205) + crew_w
    
    # Mission Fuel Fractions (Ref: Table 2.20)
    f_p = 0.990 * 0.995 * 0.995 * 0.985 # Start, Taxi, Takeoff, Climb
    f_c = 1 / math.exp(range_mi / (375 * (eta_p / sfc) * ld_c)) # Cruise
    f_l = 1 / math.exp(endur / (375 * (0.8 / sfc) * ld_l)) # Loiter (Assumed 0.8 ηp)
    f_e = 0.985 * 0.995 # Descent, Landing
    mff = f_p * f_c * f_l * f_e
    
    # WTO Matching
    c_val = 1 - (1 + m_res) * (1 - mff) - m_tfo
    wf = wto_guess * (1 - mff)
    we_req = wto_guess - wf - d_val - (m_tfo * wto_guess)
    we_allow = 10**((math.log10(wto_guess) - 0.3774) / 0.9647) # Statistical Model
    
    # Sensitivity (Growth Factor F)
    num_f = -0.9647 * (wto_guess**2) * (1 + m_res) * mff
    den_f = (c_val * wto_guess * (1 - 0.9647)) - d_val
    f_growth = num_f / den_f if den_f != 0 else 0
    
    # Derivatives
    dw_dr = (f_growth * sfc) / (375 * eta_p * ld_c)
    dw_dcp = (f_growth * range_mi) / (375 * eta_p * ld_c)

    return {
        "mff": mff, "f_growth": f_growth, "c_val": c_val,
        "we_req": we_req, "we_allow": we_allow, "wf": wf,
        "dw_dr": dw_dr, "dw_dcp": dw_dcp, "d_val": d_val,
        "wto": wto_guess
    }

# --- 3. SIDEBAR: DATA CONSOLE ---
st.sidebar.header("🕹️ DESIGN CONSOLE")
with st.sidebar:
    st.subheader("📍 Operating Weights")
    wto_in = st.number_input("Design WTO (lbs)", 30000.0, 80000.0, 48550.0)
    
    with st.expander("📦 Payload Configuration", expanded=True):
        pax_in = st.number_input("Passenger Count", 0, 100, 34)
        crew_in = st.number_input("Crew & Misc (lbs)", 0.0, 2000.0, 615.0)
        
    with st.expander("🚀 Mission Profile", expanded=True):
        range_in = st.number_input("Target Range (mi)", 100.0, 5000.0, 1265.8)
        sfc_in = st.number_input("Cruise SFC (Cp)", 0.1, 1.2, 0.6)
        ld_in = st.number_input("Cruise L/D", 5.0, 25.0, 13.0)
        endur_in = st.number_input("Loiter Time (hrs)", 0.0, 5.0, 0.75)
        ld_l_in = st.number_input("Loiter L/D", 5.0, 25.0, 16.0)

# Run Calculation
res = aircraft_solver(wto_in, range_in, sfc_in, ld_in, pax_in, crew_in, ld_l_in, endur_in)

# --- 4. MAIN DASHBOARD: FROM A TO Z ---
st.title("🛡️ AeroOptimizer Enterprise Suite")
st.markdown("---")

# A. SUMMARY KPIS (The High-Level View)
st.subheader("🟢 Performance Summary")
k1, k2, k3, k4 = st.columns(4)
k1.metric("Fuel Fraction (Mff)", f"{res['mff']:.4f}")
k2.metric("Growth Factor (F)", f"{res['f_growth']:,.2f}")
k3.metric("Payload Factor (D)", f"{res['d_val']:,.1f} lb")
error = res['we_req'] - res['we_allow']
k4.metric("Matching Error", f"{error:,.1f} lb", delta=error, delta_color="inverse")

st.divider()

# B. DETAILED ANALYSIS TABS
tab1, tab2, tab3, tab4 = st.tabs(["📊 Weight Matching", "📉 Sensitivity Analysis", "📑 Detailed Log", "📥 Export Report"])

with tab1:
    st.subheader("Sizing Convergence Map")
    w_axis = np.linspace(30000, 75000, 100)
    sweep = [aircraft_solver(w, range_in, sfc_in, ld_in, pax_in, crew_in, ld_l_in, endur_in) for w in w_axis]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=w_axis, y=[x['we_req'] for x in sweep], name='Req. Empty Weight (Mission)', line=dict(color='#58A6FF', width=3)))
    fig.add_trace(go.Scatter(x=w_axis, y=[x['we_allow'] for x in sweep], name='Allow. Empty Weight (Structural)', line=dict(color='#F85149', width=3, dash='dot')))
    fig.add_trace(go.Scatter(x=[wto_in], y=[res['we_req']], mode='markers+text', marker=dict(size=12, color='#3FB950'), text=["Current Design"], textposition="top center"))
    
    fig.update_layout(plot_bgcolor='#0D1117', paper_bgcolor='#0D1117', font_color='#8B949E', margin=dict(l=0,r=0,t=40,b=0))
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Design Sensitivity Derivatives (Ref: Table 2.20)")
    s1, s2 = st.columns(2)
    s1.metric("Range Penalty (dW/dR)", f"{res['dw_dr']:.4f} lb/mi")
    s2.metric("SFC Penalty (dW/dCp)", f"{res['dw_dcp']:,.1f} lb/unit")
    st.info("How to read: If range increases by 10 miles, WTO increases by approx. " + f"{res['dw_dr']*10:.1f} lbs.")

with tab3:
    st.subheader("Full Weight Breakdown (A to Z)")
    col_a, col_b = st.columns(2)
    with col_a:
        st.write("**Fixed Weights**")
        st.table({
            "Parameter": ["Payload + Crew (D)", "TFO Weight", "Empty Weight (Structural)"],
            "Value (lbs)": [f"{res['d_val']:,.1f}", f"{wto_in*0.005:,.1f}", f"{res['we_allow']:,.1f}"]
        })
    with col_b:
        st.write("**Variable Mission Weights**")
        st.table({
            "Parameter": ["Total Mission Fuel (Wf)", "Reserve Fuel", "Empty Weight (Req. for Mission)"],
            "Value (lbs)": [f"{res['wf']:,.1f}", f"{res['wf']*0.05:,.1f}", f"{res['we_req']:,.1f}"]
        })

with tab4:
    st.subheader("Technical Documentation Export")
    def generate_pdf(d):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "AIRCRAFT MASTER SIZING REPORT", ln=True, align='C')
        pdf.ln(10)
        pdf.set_font("Arial", '', 12)
        rows = [
            f"Gross Take-off Weight (WTO): {d['wto']:,.1f} lbs",
            f"Payload & Crew (D): {d['d_val']:,.1f} lbs",
            f"Mission Fuel Fraction (Mff): {d['mff']:.4f}",
            f"Growth Factor (F): {d['f_growth']:.2f}",
            f"Range Sensitivity: {d['dw_dr']:.4f} lb/mi",
            f"SFC Sensitivity: {d['dw_dcp']:.2f} lb/unit"
        ]
        for row in rows:
            pdf.cell(0, 10, row, ln=True)
        return pdf.output(dest='S').encode('latin-1')

    st.download_button("📥 DOWNLOAD COMPREHENSIVE PDF", data=generate_pdf(res), file_name="Design_Report_Full.pdf")

st.divider()
st.caption("AeroOptimizer Enterprise v3.0 | MDAO Standards | JUST Aero Dept.")
