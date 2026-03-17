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
    .main { background-color: #0B0E14; color: #E2E8F0; }
    
    /* Sidebar Styling - Fixing Text/Background Contrast */
    section[data-testid="stSidebar"] {
        background-color: #161B22 !important;
        border-right: 1px solid #30363D;
    }
    section[data-testid="stSidebar"] .stMarkdown p, section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2 {
        color: #58A6FF !important; /* Professional Aero Blue */
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Input Boxes Styling */
    .stNumberInput input, .stSelectbox div {
        background-color: #0D1117 !important;
        color: #C9D1D9 !important;
        border: 1px solid #30363D !important;
    }

    /* Metric Cards */
    div[data-testid="stMetric"] {
        background-color: #161B22;
        border: 1px solid #30363D;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
    }
    
    /* Headers */
    h1, h2, h3 { color: #58A6FF; font-weight: 800; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR: DATA VAULT (FIXED & EXTENDED) ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Placeholder_view_vector.svg/640px-Placeholder_view_vector.svg.png", width=100) # يمكنك وضع شعار JUST هنا
st.sidebar.title("✈️ Design Control")

with st.sidebar:
    st.header("📍 Primary Variable")
    wto_input = st.number_input("Gross Weight (WTO) - lbs", value=48550.0, step=10.0)
    
    st.divider()
    
    with st.expander("📦 Payload & Fixed Weights", expanded=True):
        pax = st.number_input("Passengers", value=34)
        w_pax = pax * 205
        w_crew = st.number_input("Crew Assets", value=615.0)
        d_val = w_pax + w_crew # The 'D' in Eq 2.22

    with st.expander("🚀 Cruise Phase (Table 2.20)", expanded=True):
        rc = st.number_input("Range (Rc) - mi", value=1265.8)
        ld_c = st.number_input("L/D (Cruise)", value=13.0)
        cp_c = st.number_input("SFC (Cp)", value=0.6)
        np_c = st.number_input("Prop Eff (ηp)", value=0.85)

    with st.expander("🔄 Loiter & Safety Phase", expanded=False):
        eltr = st.number_input("Endurance (E) - hrs", value=0.75)
        ld_l = st.number_input("L/D (Loiter)", value=16.0)
        cp_l = st.number_input("SFC (Loiter)", value=0.65)
        m_res = st.number_input("Reserves (Mres)", value=0.05)
        m_tfo = st.number_input("TFO Ratio", value=0.005)

    with st.expander("🏗️ Structural Constants", expanded=False):
        coeff_a = 0.3774 # Log-stat constant
        coeff_b = 0.9647 # Log-stat slope

# --- 3. THE PHYSICS ENGINE (TABLE 2.20 COMPLIANT) ---
def compute_sizing(wto):
    # Mission Fuel Fractions
    f_phases = 0.990 * 0.995 * 0.995 * 0.985 # Engine start to climb
    f_cruise = 1 / math.exp(rc / (375 * (np_c / cp_c) * ld_c))
    f_loiter = 1 / math.exp(eltr / (375 * (0.80 / cp_l) * ld_l)) # ηp_loiter assumed 0.80
    f_land = 0.985 * 0.995
    mff = f_phases * f_cruise * f_loiter * f_land
    
    # Efficiency Factor (C) - Equation 2.22
    c_val = 1 - (1 + m_res) * (1 - mff) - m_tfo
    
    # Weight Matching
    wf = wto * (1 - mff)
    we_req = wto - wf - d_val - (m_tfo * wto)
    we_allow = 10**((math.log10(wto) - coeff_a) / coeff_b)
    
    # Growth Factor (F) - EXACT TABLE 2.20 LOGIC
    # F = dWTO / dD (Sensitivity of gross weight to fixed weight)
    num_f = -coeff_b * (wto**2) * (1 + m_res) * mff
    den_f = (c_val * wto * (1 - coeff_b)) - d_val
    f_growth = num_f / den_f if den_f != 0 else 0
    
    # Sensitivity Matrix (Eq 2.49 - 2.51)
    dw_dr = (f_growth * cp_c) / (375 * np_c * ld_c) # Range Sensitivity
    dw_dcp = (f_growth * rc) / (375 * np_c * ld_c) # Efficiency Sensitivity
    
    return locals()

res = compute_sizing(wto_input)

# --- 4. DASHBOARD PRESENTATION ---
st.title("🛡️ AeroOptimizer | Conceptual Sizing Suite")
st.markdown("---")

# Row 1: Key Metrics
c1, c2, c3, c4 = st.columns(4)
c1.metric("Mission Fuel Fraction", f"{res['mff']:.4f}")
c2.metric("Growth Factor (F)", f"{res['f_growth']:,.2f}")
c3.metric("Structural Error", f"{res['we_req'] - res['we_allow']:,.1f} lb")
c4.metric("Efficiency Index (C)", f"{res['c_val']:.4f}")

st.divider()

# Row 2: Advanced Graphing
col_plot, col_info = st.columns([2, 1])

with col_plot:
    st.subheader("📊 Weight Equilibrium & Convergence")
    
    w_range = np.linspace(35000, 75000, 100)
    sweep = [compute_sizing(w) for w in w_range]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=w_range, y=[x['we_req'] for x in sweep], name='Required WE', line=dict(color='#58A6FF', width=4)))
    fig.add_trace(go.Scatter(x=w_range, y=[x['we_allow'] for x in sweep], name='Allowable WE', line=dict(color='#F85149', width=4, dash='dot')))
    fig.add_trace(go.Scatter(x=[wto_input], y=[res['we_req']], mode='markers+text', name='Design Point', 
                             marker=dict(size=14, color='#3FB950'), text=["Current WTO"], textposition="top center"))
    
    fig.update_layout(plot_bgcolor='#0D1117', paper_bgcolor='#0D1117', font_color='#C9D1D9', margin=dict(l=0,r=0,t=20,b=0))
    fig.update_xaxes(showgrid=True, gridcolor='#30363D')
    fig.update_yaxes(showgrid=True, gridcolor='#30363D')
    st.plotly_chart(fig, use_container_width=True)

with col_info:
    st.subheader("📑 Analysis Logs")
    st.write(f"**Payload D:** {res['d_val']:,.1f} lbs")
    st.write(f"**Calculated Fuel:** {res['wf']:,.1f} lbs")
    st.write("---")
    st.info("The intersection point represents a design where mission fuel requirements perfectly match structural capacity.")

# Row 3: Sensitivity Matrix (Table 2.20)
st.subheader("📉 Design Sensitivity Derivatives (Table 2.20)")
sc1, sc2 = st.columns(2)
sc1.metric("Range Penalty (dW/dR)", f"{res['dw_dr']:.4f} lbs/mi")
sc2.metric("Efficiency Penalty (dW/dCp)", f"{res['dw_dcp']:,.1f} lbs/unit")

# --- 5. MASTER PDF REPORT ---
def generate_pro_pdf(d):
    pdf = FPDF()
    pdf.add_page()
    
    # Professional Header
    pdf.set_fill_color(22, 27, 34)
    pdf.rect(0, 0, 210, 50, 'F')
    pdf.set_text_color(88, 166, 255)
    pdf.set_font("Arial", 'B', 22)
    pdf.cell(0, 25, "TECHNICAL DESIGN PACKAGE", ln=True, align='C')
    pdf.set_font("Arial", 'I', 12)
    pdf.cell(0, 10, "Conceptual Sizing & Growth Factor Analysis", ln=True, align='C')
    
    pdf.ln(20)
    pdf.set_text_color(0, 0, 0)
    
    # Detailed Content
    sections = [
        ("1. Methodology", "Based on Table 2.20 and Eq 2.22, this sizing process iterates WTO to find the design equilibrium. It accounts for mission fuel fractions, structural limitations, and growth feedback loops."),
        ("2. Input Configuration", f"Gross Weight: {wto_input:,.1f} lb\nRange: {rc} mi\nPassengers: {pax}\nL/D (Cruise): {ld_c}"),
        ("3. Convergence Results", f"Growth Factor F: {d['f_growth']:.2f}\nMission Mff: {d['mff']:.4f}\nEfficiency C: {d['c_val']:.4f}\nMatching Error: {d['we_req'] - d['we_allow']:,.2f} lb"),
        ("4. Sensitivity Analysis", f"dW/dR (Range): {d['dw_dr']:.4f} lb/mi\ndW/dCp (SFC): {d['dw_dcp']:.2f} lb/unit\n\nThese derivatives define how the aircraft weight grows as design requirements are expanded.")
    ]
    
    for title, content in sections:
        pdf.set_font("Arial", 'B', 14)
        pdf.set_fill_color(240, 240, 240)
        pdf.cell(0, 10, f" {title}", ln=True, fill=True)
        pdf.set_font("Arial", '', 11)
        pdf.multi_cell(0, 8, content)
        pdf.ln(5)

    return pdf.output(dest='S').encode('latin-1', 'ignore')

st.divider()
st.download_button("📥 GENERATE MASTER REPORT (PDF)", data=generate_pro_pdf(res), file_name="Aircraft_Sizing_Report.pdf")
