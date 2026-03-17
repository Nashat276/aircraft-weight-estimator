import streamlit as st
import math
import numpy as np
import plotly.graph_objects as go
from fpdf import FPDF

# --- 1. INDUSTRIAL UI LAYOUT (Clean & Sharp) ---
st.set_page_config(page_title="AeroOptimizer | Engineering Suite", layout="wide")

st.markdown("""
    <style>
    /* Professional Industrial Theme */
    .main { background-color: #0E1117; color: #C9D1D9; font-family: 'Segoe UI', sans-serif; }
    
    /* Clean Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #161B22 !important;
        border-right: 1px solid #30363D;
    }
    section[data-testid="stSidebar"] .stMarkdown p {
        color: #58A6FF !important;
        font-weight: 600;
        font-size: 14px;
    }
    
    /* Result Cards - No fancy gradients, just clean borders */
    div[data-testid="stMetric"] {
        background: #1C2128;
        border: 1px solid #30363D;
        border-radius: 4px;
        padding: 15px;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #161B22;
        border-radius: 4px 4px 0 0;
        padding: 10px 20px;
        color: #8B949E;
    }
    .stTabs [aria-selected="true"] { background-color: #58A6FF !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGICAL DATA INPUT (Organized by Domain) ---
st.sidebar.title("✈️ DESIGN INPUTS")

with st.sidebar:
    st.subheader("📍 Primary Weight")
    wto_input = st.number_input("Gross Weight (WTO) - lbs", value=48550.0, step=100.0)
    
    st.divider()
    
    st.subheader("📦 Payload Matrix")
    pax_count = st.number_input("Passengers", value=34)
    w_crew_input = st.number_input("Crew & Ops (lbs)", value=615.0)
    # Calculated Fixed Weight (D)
    d_factor = (pax_count * 205) + w_crew_input

    st.subheader("🚀 Mission Profile")
    range_mi = st.number_input("Range (mi)", value=1265.8)
    ld_cruise = st.number_input("L/D Cruise", value=13.0)
    sfc_cruise = st.number_input("SFC (lb/hp/hr)", value=0.6)
    eta_prop = st.number_input("Prop Efficiency (ηp)", value=0.85)

# --- 3. PHYSICS ENGINE (TABLE 2.20 & SENSITIVITY) ---
def solver(wto):
    # Mission Segments
    f_start_climb = 0.990 * 0.995 * 0.995 * 0.985 
    f_cruise = 1 / math.exp(range_mi / (375 * (eta_prop / sfc_cruise) * ld_cruise))
    f_loiter = 0.990 # Assumed fixed for convergence stability
    f_landing = 0.985 * 0.995
    mff = f_start_climb * f_cruise * f_loiter * f_landing
    
    # Matching Constants (JUST/Table 2.20 Logic)
    m_res, m_tfo = 0.05, 0.005
    c_val = 1 - (1 + m_res) * (1 - mff) - m_tfo
    
    # Weight Matching
    wf = wto * (1 - mff)
    we_req = wto - wf - d_factor - (m_tfo * wto)
    we_allow = 10**((math.log10(wto) - 0.3774) / 0.9647)
    
    # Growth Factor (F = dWTO / dD)
    num_f = -0.9647 * (wto**2) * (1 + m_res) * mff
    den_f = (c_val * wto * (1 - 0.9647)) - d_factor
    f_growth = num_f / den_f if den_f != 0 else 0
    
    # Sensitivity Matrix
    dw_dr = (f_growth * sfc_cruise) / (375 * eta_prop * ld_cruise)
    dw_dcp = (f_growth * range_mi) / (375 * eta_prop * ld_cruise)
    
    return {
        "mff": mff, "f_growth": f_growth, "c_val": c_val,
        "we_req": we_req, "we_allow": we_allow, "wf": wf,
        "dw_dr": dw_dr, "dw_dcp": dw_dcp, "d_val": d_factor
    }

# Execute
res = solver(wto_input)

# --- 4. DATA PRESENTATION (The Professional View) ---
st.title("🛡️ Aircraft Sizing & Analysis Suite")
st.markdown("---")

# Row 1: Key Performance Indicators (KPIs)
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Fuel Fraction (Mff)", f"{res['mff']:.4f}")
kpi2.metric("Growth Factor (F)", f"{res['f_growth']:,.2f}")
kpi3.metric("Payload Factor (D)", f"{res['d_val']:,.1f} lb")
diff = res['we_req'] - res['we_allow']
kpi4.metric("Matching Delta", f"{diff:,.1f} lb", delta=diff, delta_color="inverse")

st.divider()

# Row 2: Tabs for Detailed Analysis
tab1, tab2, tab3 = st.tabs(["📊 Weight Convergence", "📉 Sensitivity Matrix", "📑 Engineering Report"])

with tab1:
    col_chart, col_data = st.columns([2, 1])
    with col_chart:
        st.subheader("Sizing Convergence Map")
        
        w_axis = np.linspace(30000, 70000, 100)
        sweep = [solver(w) for w in w_axis]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=w_axis, y=[x['we_req'] for x in sweep], name='Required WE', line=dict(color='#58A6FF', width=3)))
        fig.add_trace(go.Scatter(x=w_axis, y=[x['we_allow'] for x in sweep], name='Allowable WE', line=dict(color='#F85149', width=3, dash='dot')))
        fig.add_trace(go.Scatter(x=[wto_input], y=[res['we_req']], mode='markers+text', marker=dict(size=12, color='#3FB950'), text=["DESIGN POINT"], textposition="top center"))
        fig.update_layout(plot_bgcolor='#0D1117', paper_bgcolor='#0D1117', font_color='#8B949E', margin=dict(l=0,r=0,t=40,b=0))
        st.plotly_chart(fig, use_container_width=True)
    
    with col_data:
        st.subheader("Weight Breakdown")
        st.table({
            "Component": ["Payload + Crew (D)", "Mission Fuel (Wf)", "Empty Weight (Req)", "Empty Weight (Allow)"],
            "Weight (lbs)": [f"{res['d_val']:,.1f}", f"{res['wf']:,.1f}", f"{res['we_req']:,.1f}", f"{res['we_allow']:,.1f}"]
        })

with tab2:
    st.subheader("Sensitivity Derivatives (Ref: Table 2.20)")
    s1, s2 = st.columns(2)
    s1.metric("Range Penalty (dW/dR)", f"{res['dw_dr']:.4f} lb/mi")
    s2.metric("SFC Penalty (dW/dCp)", f"{res['dw_dcp']:,.1f} lb/unit")
    st.info("These values indicate how much the WTO will increase for every unit increase in Range or SFC.")

with tab3:
    st.subheader("Generate Technical Documentation")
    def create_pdf(d):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "AIRCRAFT SIZING SUMMARY REPORT", ln=True, align='C')
        pdf.ln(10)
        pdf.set_font("Arial", '', 12)
        data_lines = [
            f"Gross Weight (WTO): {wto_input:,.1f} lbs",
            f"Payload Asset (D): {d['d_val']:,.1f} lbs",
            f"Mission Fuel Fraction: {d['mff']:.4f}",
            f"Growth Factor (F): {d['f_growth']:.2f}",
            f"Range Sensitivity: {d['dw_dr']:.4f} lb/mi",
            f"SFC Sensitivity: {d['dw_dcp']:.2f} lb/unit"
        ]
        for line in data_lines:
            pdf.cell(0, 10, line, ln=True)
        return pdf.output(dest='S').encode('latin-1')

    st.download_button("📥 DOWNLOAD PDF REPORT", data=create_pdf(res), file_name="Aero_Design_Report.pdf")

# --- 5. TECHNICAL NOTATION ---
st.divider()
st.caption("AeroOptimizer v2.0 | Developed for JUST Aeronautical Engineering Standards. (MDAO Approach)")
