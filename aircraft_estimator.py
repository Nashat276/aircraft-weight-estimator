import streamlit as st
import math
import numpy as np
import plotly.graph_objects as go
from fpdf import FPDF

# --- 1. PRESTIGE UI DESIGN ---
st.set_page_config(page_title="AeroOptimizer Ultra | Professional Sizing", layout="wide")

st.markdown("""
    <style>
    /* Dark Mode Global */
    .main { background-color: #05070A; color: #E2E8F0; }
    
    /* Sidebar: High Contrast Glassmorphism */
    section[data-testid="stSidebar"] {
        background-color: #0D1117 !important;
        border-right: 2px solid #1f6feb;
    }
    section[data-testid="stSidebar"] .stMarkdown p, section[data-testid="stSidebar"] label {
        color: #58A6FF !important; /* Cyber Blue */
        font-size: 15px !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Metrics Styling */
    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, #0d1117, #161b22);
        border: 1px solid #30363d;
        border-left: 5px solid #1f6feb;
        border-radius: 10px;
        padding: 20px;
    }
    
    /* Buttons & Inputs */
    .stNumberInput input {
        background-color: #0D1117 !important;
        color: #FFFFFF !important;
        border: 1px solid #30363d !important;
    }
    
    h1, h2, h3 { color: #58A6FF; font-family: 'Orbitron', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR: THE ENGINEERING DASHBOARD ---
st.sidebar.markdown("### 🛠️ Configuration")

with st.sidebar:
    st.markdown("---")
    wto_input = st.number_input("Design WTO (lbs)", value=48550.0, step=10.0)
    
    with st.expander("📦 PAYLOAD & CREW", expanded=True):
        pax = st.number_input("PAX Count", value=34)
        w_pax_payload = pax * 205
        w_crew = st.number_input("Crew Assets (lbs)", value=615.0)
        d_val = w_pax_payload + w_crew

    with st.expander("🚀 CRUISE PARAMETERS", expanded=True):
        rc = st.number_input("Range (mi)", value=1265.8)
        ld_c = st.number_input("Cruise L/D", value=13.0)
        cp_c = st.number_input("Cruise SFC (Cp)", value=0.6)
        np_c = st.number_input("Prop ηp", value=0.85)

    with st.expander("🔄 LOITER & SAFETY", expanded=False):
        eltr = st.number_input("Endurance (hrs)", value=0.75)
        ld_l = st.number_input("Loiter L/D", value=16.0)
        cp_l = st.number_input("Loiter SFC", value=0.65)
        m_res = st.number_input("Reserves (Mres)", value=0.05)
        m_tfo = st.number_input("TFO Ratio", value=0.005)

# --- 3. AEROSPACE PHYSICS ENGINE ---
def run_solver(wto):
    # Mission Profile Fractions
    f_p = 0.990 * 0.995 * 0.995 * 0.985 
    f_c = 1 / math.exp(rc / (375 * (np_c / cp_c) * ld_c))
    f_l = 1 / math.exp(eltr / (375 * (0.80 / cp_l) * ld_l))
    f_e = 0.985 * 0.995
    mff = f_p * f_c * f_l * f_e
    
    # Matching Logic (Eq 2.22)
    c_val = 1 - (1 + m_res) * (1 - mff) - m_tfo
    wf = wto * (1 - mff)
    we_req = wto - wf - d_val - (m_tfo * wto)
    we_allow = 10**((math.log10(wto) - 0.3774) / 0.9647)
    
    # Sensitivity (Table 2.20 Framework)
    num_f = -0.9647 * (wto**2) * (1 + m_res) * mff
    den_f = (c_val * wto * (1 - 0.9647)) - d_val
    f_growth = num_f / den_f if den_f != 0 else 0
    
    # Sensitivity Derivatives
    dw_dr = (f_growth * cp_c) / (375 * np_c * ld_c)
    dw_dcp = (f_growth * rc) / (375 * np_c * ld_c)
    
    return locals()

res = run_solver(wto_input)

# --- 4. MAIN INTERFACE: AERO COMMAND CENTER ---
st.title("✈️ AeroOptimizer Ultra")
st.markdown("##### Sizing, Convergence & Sensitivity Analysis | JUST Engineering Standards")
st.divider()

# High-Visibility Metrics
c1, c2, c3, c4 = st.columns(4)
c1.metric("Mission Fuel Fraction", f"{res['mff']:.4f}")
c2.metric("Growth Factor (F)", f"{res['f_growth']:,.2f}")
c3.metric("Efficiency (C)", f"{res['c_val']:.4f}")
delta = res['we_req'] - res['we_allow']
c4.metric("Convergence Delta", f"{delta:,.1f} lb", delta=delta, delta_color="inverse")

st.divider()

# Advanced Graphical Section
col_map, col_stats = st.columns([2, 1])

with col_map:
    st.subheader("🌐 Convergence Map")
    w_axis = np.linspace(35000, 75000, 100)
    sweep = [run_solver(w) for w in w_axis]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=w_axis, y=[x['we_req'] for x in sweep], name='Mission Required WE', line=dict(color='#1f6feb', width=4)))
    fig.add_trace(go.Scatter(x=w_axis, y=[x['we_allow'] for x in sweep], name='Structural Allowable WE', line=dict(color='#f85149', width=4, dash='dot')))
    fig.add_trace(go.Scatter(x=[wto_input], y=[res['we_req']], mode='markers', marker=dict(size=15, color='#3fb950', symbol='diamond'), name='Design Point'))
    
    fig.update_layout(plot_bgcolor='#0D1117', paper_bgcolor='#05070A', font_color='#8b949e', margin=dict(l=0,r=0,t=20,b=0))
    fig.update_xaxes(showgrid=True, gridcolor='#30363d', title="Gross Weight (WTO) [lbs]")
    fig.update_yaxes(showgrid=True, gridcolor='#30363d', title="Empty Weight (WE) [lbs]")
    st.plotly_chart(fig, use_container_width=True)

with col_stats:
    st.subheader("📑 Design Summary")
    st.write(f"**Payload Asset (D):** {res['d_val']:,.1f} lbs")
    st.write(f"**Mission Fuel (Wf):** {res['wf']:,.1f} lbs")
    st.info("Technical Convergence is achieved at the intersection of 'Required' and 'Allowable' curves.")

st.divider()

# Sensitivity Table 2.20
st.subheader("📉 Sensitivity Analysis (Table 2.20 Logic)")
sc1, sc2 = st.columns(2)
sc1.metric("Range Penalty (dW/dR)", f"{res['dw_dr']:.4f} lbs/mi")
sc2.metric("Efficiency Penalty (dW/dCp)", f"{res['dw_dcp']:,.1f} lbs/unit")

# --- 5. THE ULTIMATE PDF PACKAGE ---
def generate_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    
    # Border
    pdf.set_draw_color(31, 111, 235)
    pdf.rect(5, 5, 200, 287)
    
    # Professional Header
    pdf.set_fill_color(13, 17, 23)
    pdf.rect(5, 5, 200, 40, 'F')
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", 'B', 20)
    pdf.cell(0, 20, "AIRCRAFT MASTER DESIGN REPORT", ln=True, align='C')
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(0, 5, "Quantitative Sizing & Sensitivity Matrix | Ref: Table 2.20", ln=True, align='C')
    
    pdf.set_text_color(0, 0, 0)
    pdf.ln(25)
    
    # Section 1: Philosophy
    pdf.set_font("Arial", 'B', 14)
    pdf.set_fill_color(241, 245, 249)
    pdf.cell(0, 10, " 1. DESIGN METHODOLOGY", ln=True, fill=True)
    pdf.set_font("Arial", '', 11)
    pdf.multi_cell(0, 7, "This report documents the iterative sizing of a fixed-wing aircraft. The methodology balances the Breguet Range requirements against structural weight statistics. The objective is to ensure that the required empty weight for the mission matches the structural capacity of the airframe.")
    
    # Section 2: Input Matrix
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, " 2. CONFIGURATION INPUTS", ln=True, fill=True)
    pdf.set_font("Arial", '', 11)
    pdf.cell(95, 8, f"- Selected WTO: {wto_input:,.1f} lbs", ln=0)
    pdf.cell(95, 8, f"- Target Range: {rc} miles", ln=1)
    pdf.cell(95, 8, f"- Fixed Asset Weight (D): {d_val:,.1f} lbs", ln=0)
    pdf.cell(95, 8, f"- L/D Cruise: {ld_c}", ln=1)
    
    # Section 3: Performance Analysis
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, " 3. PERFORMANCE & CONVERGENCE", ln=True, fill=True)
    pdf.set_font("Arial", '', 11)
    pdf.multi_cell(0, 7, f"At the current WTO, the Mission Fuel Fraction (Mff) is {data['mff']:.4f}. The matching process yields a structural error of {data['we_req'] - data['we_allow']:,.1f} lbs. A zero-delta intersection indicates a technically feasible design.")
    
    # Section 4: Sensitivity (Table 2.20)
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, " 4. SENSITIVITY DERIVATIVES", ln=True, fill=True)
    pdf.set_font("Arial", '', 11)
    pdf.multi_cell(0, 7, f"The Growth Factor (F = {data['f_growth']:.2f}) defines the airframe's response to weight additions. Range sensitivity (dW/dR) is {data['dw_dr']:.4f} lbs/mi, while efficiency sensitivity (dW/dCp) is {data['dw_dcp']:.2f} lbs/unit.")
    
    return pdf.output(dest='S').encode('latin-1', 'ignore')

st.divider()
st.download_button("📥 GENERATE MASTER DESIGN PACKAGE (PDF)", data=generate_pdf(res), file_name="Aero_Master_Design.pdf")
