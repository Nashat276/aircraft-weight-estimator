import streamlit as st
import math
import numpy as np
import plotly.graph_objects as go
from fpdf import FPDF

# --- 1. PRESTIGE UI DESIGN (Modern Aero Dashboard) ---
st.set_page_config(page_title="AeroOptimizer Ultra | Professional Sizing", layout="wide")

st.markdown("""
    <style>
    /* Dark Mode Global */
    .main { background-color: #0B0E14; color: #E2E8F0; }
    
    /* Sidebar: High Contrast - Fixing Text Visibility */
    section[data-testid="stSidebar"] {
        background-color: #161B22 !important;
        border-right: 2px solid #58A6FF;
    }
    section[data-testid="stSidebar"] label, section[data-testid="stSidebar"] p {
        color: #58A6FF !important; /* Cyber Blue for maximum clarity */
        font-weight: 700 !important;
        text-transform: uppercase;
        font-size: 14px !important;
    }
    
    /* Metrics Styling */
    div[data-testid="stMetric"] {
        background: #161B22;
        border: 1px solid #30363D;
        border-left: 5px solid #58A6FF;
        border-radius: 8px;
        padding: 15px;
    }
    
    /* Inputs */
    .stNumberInput input {
        background-color: #0D1117 !important;
        color: #FFFFFF !important;
        border: 1px solid #30363D !important;
    }
    
    h1, h2, h3 { color: #58A6FF; font-family: 'Inter', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR: THE ENGINEERING DASHBOARD ---
st.sidebar.title("🛠️ DESIGN CONFIGURATION")

with st.sidebar:
    st.markdown("---")
    # Move WTO to Inputs as requested
    wto_input = st.number_input("DESIGN WTO (LBS)", value=48550.0, step=50.0)
    
    with st.expander("📦 PAYLOAD & CREW", expanded=True):
        pax = st.number_input("PAX COUNT", value=34)
        w_pax_total = pax * 205
        w_crew = st.number_input("CREW ASSETS (LBS)", value=615.0)
        d_val_calc = w_pax_total + w_crew # Fixed Asset D

    with st.expander("🚀 CRUISE (REF: TABLE 2.20)", expanded=True):
        rc = st.number_input("RANGE (MI)", value=1265.8)
        ld_c = st.number_input("CRUISE L/D", value=13.0)
        cp_c = st.number_input("CRUISE SFC (CP)", value=0.6)
        np_c = st.number_input("PROP ηP", value=0.85)

    with st.expander("🔄 LOITER & RESERVES", expanded=False):
        eltr = st.number_input("ENDURANCE (HRS)", value=0.75)
        ld_l = st.number_input("LOITER L/D", value=16.0)
        cp_l = st.number_input("LOITER SFC", value=0.65)
        m_res = st.number_input("RESERVES (MRES)", value=0.05)
        m_tfo = st.number_input("TFO RATIO", value=0.005)

# --- 3. AEROSPACE PHYSICS ENGINE (ACCURATE MDAO) ---
def run_sizing_solver(wto):
    # Mission Phase Fractions
    f_p = 0.990 * 0.995 * 0.995 * 0.985 # Engine start to climb
    f_c = 1 / math.exp(rc / (375 * (np_c / cp_c) * ld_c))
    f_l = 1 / math.exp(eltr / (375 * (0.80 / cp_l) * ld_l)) # ηp_loiter assumed 0.80
    f_e = 0.985 * 0.995 # Descent and Landing
    mff = f_p * f_c * f_l * f_e
    
    # Efficiency Factor (C) - Equation 2.22
    c_val = 1 - (1 + m_res) * (1 - mff) - m_tfo
    
    # Matching Logic
    wf = wto * (1 - mff)
    we_req = wto - wf - d_val_calc - (m_tfo * wto)
    we_allow = 10**((math.log10(wto) - 0.3774) / 0.9647)
    
    # Sensitivity (Table 2.20 Logic)
    # F = dWTO / dD
    num_f = -0.9647 * (wto**2) * (1 + m_res) * mff
    den_f = (c_val * wto * (1 - 0.9647)) - d_val_calc
    f_growth = num_f / den_f if den_f != 0 else 0
    
    # Sensitivity Derivatives (Eq 2.49)
    dw_dr = (f_growth * cp_c) / (375 * np_c * ld_c)
    dw_dcp = (f_growth * rc) / (375 * np_c * ld_c)
    
    # Return dictionary with explicit keys to prevent KeyError
    return {
        "mff": mff, "f_growth": f_growth, "c_val": c_val,
        "we_req": we_req, "we_allow": we_allow, "wf": wf,
        "dw_dr": dw_dr, "dw_dcp": dw_dcp, "d_val": d_val_calc
    }

res = run_sizing_solver(wto_input)

# --- 4. MAIN DASHBOARD INTERFACE ---
st.title("✈️ AeroOptimizer Ultra | Design Suite")
st.markdown("##### Precision Conceptual Sizing & Sensitivity Analysis")
st.divider()

# Core Metrics Row
c1, c2, c3, c4 = st.columns(4)
c1.metric("Mission Mff", f"{res['mff']:.4f}")
c2.metric("Growth Factor (F)", f"{res['f_growth']:,.2f}")
c3.metric("Efficiency (C)", f"{res['c_val']:.4f}")
delta_err = res['we_req'] - res['we_allow']
c4.metric("Convergence Delta", f"{delta_err:,.1f} lb", delta=delta_err, delta_color="inverse")

st.divider()

# Advanced Graphical Analysis
col_plot, col_summary = st.columns([2, 1])

with col_plot:
    st.subheader("🌐 Weight Convergence Map")
    w_range = np.linspace(35000, 75000, 100)
    sweep = [run_sizing_solver(w) for w in w_range]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=w_range, y=[x['we_req'] for x in sweep], name='Mission Required WE', line=dict(color='#58A6FF', width=4)))
    fig.add_trace(go.Scatter(x=w_range, y=[x['we_allow'] for x in sweep], name='Structural Allowable WE', line=dict(color='#F85149', width=4, dash='dot')))
    fig.add_trace(go.Scatter(x=[wto_input], y=[res['we_req']], mode='markers', marker=dict(size=14, color='#3FB950', symbol='diamond'), name='Current Design'))
    
    fig.update_layout(plot_bgcolor='#0D1117', paper_bgcolor='#0B0E14', font_color='#C9D1D9', margin=dict(l=0,r=0,t=20,b=0))
    fig.update_xaxes(showgrid=True, gridcolor='#30363D', title="Gross Weight (WTO) [lbs]")
    fig.update_yaxes(showgrid=True, gridcolor='#30363D', title="Empty Weight (WE) [lbs]")
    st.plotly_chart(fig, use_container_width=True)

with col_summary:
    st.subheader("📑 Analysis Logs")
    st.write(f"**Payload Asset (D):** {res['d_val']:,.1f} lbs")
    st.write(f"**Total Fuel (Wf):** {res['wf']:,.1f} lbs")
    st.info("Technical equilibrium occurs at the intersection of 'Required' and 'Allowable' curves.")

st.divider()

# Sensitivity Derivatives Table 2.20
st.subheader("📉 Design Sensitivity Matrix (Table 2.20)")
sc1, sc2 = st.columns(2)
sc1.metric("Range Penalty (dW/dR)", f"{res['dw_dr']:.4f} lbs/mi")
sc2.metric("SFC Penalty (dW/dCp)", f"{res['dw_dcp']:,.1f} lbs/unit")

# --- 5. THE MASTER PDF PACKAGE (EXECUTIVE FORMAT) ---
def generate_master_pdf(d):
    pdf = FPDF()
    pdf.add_page()
    
    # Aesthetic Border
    pdf.set_draw_color(88, 166, 255)
    pdf.rect(5, 5, 200, 287)
    
    # Executive Header
    pdf.set_fill_color(22, 27, 34)
    pdf.rect(5, 5, 200, 45, 'F')
    pdf.set_text_color(88, 166, 255)
    pdf.set_font("Arial", 'B', 20)
    pdf.cell(0, 25, "AIRCRAFT PRELIMINARY DESIGN PACKAGE", ln=True, align='C')
    pdf.set_font("Arial", 'I', 11)
    pdf.cell(0, 5, "Quantitative Weight Sizing & Sensitivity Matrix", ln=True, align='C')
    
    pdf.set_text_color(0, 0, 0)
    pdf.ln(25)
    
    # Section 1: Philosophy
    pdf.set_font("Arial", 'B', 14)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(0, 10, " 1. SYSTEM METHODOLOGY", ln=True, fill=True)
    pdf.set_font("Arial", '', 11)
    pdf.multi_cell(0, 7, "This report details the multidisciplinary sizing of a fixed-wing aircraft. By calculating fuel fractions for each mission segment (Cruise and Loiter) and applying structural weight log-models, we identify the design Gross Weight (WTO) that satisfies all performance constraints.")
    
    # Section 2: Input Configuration
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, " 2. CONFIGURATION MATRIX", ln=True, fill=True)
    pdf.set_font("Arial", '', 11)
    pdf.cell(95, 8, f"- Target WTO: {wto_input:,.1f} lbs", ln=0)
    pdf.cell(95, 8, f"- Mission Range: {rc} miles", ln=1)
    pdf.cell(95, 8, f"- Payload Asset (D): {d_val_calc:,.1f} lbs", ln=0)
    pdf.cell(95, 8, f"- Cruise L/D: {ld_c}", ln=1)
    
    # Section 3: Performance Analysis
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, " 3. WEIGHT CONVERGENCE & GROWTH", ln=True, fill=True)
    pdf.set_font("Arial", '', 11)
    pdf.multi_cell(0, 7, f"The Growth Factor (F = {d['f_growth']:.2f}) quantifies the sensitivity of the gross weight to internal changes. At the current design point, the mission fuel fraction (Mff) is {d['mff']:.4f}, resulting in a matching error of {d['we_req'] - d['we_allow']:,.1f} lbs.")
    
    # Section 4: Sensitivity Derivatives (Table 2.20)
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, " 4. SENSITIVITY DERIVATIVES", ln=True, fill=True)
    pdf.set_font("Arial", '', 11)
    pdf.multi_cell(0, 7, f"Based on Table 2.20 logic: \n- Range Sensitivity (dW/dR): {d['dw_dr']:.4f} lbs/mi \n- SFC Sensitivity (dW/dCp): {d['dw_dcp']:.2f} lbs/unit SFC.")

    return pdf.output(dest='S').encode('latin-1', 'ignore')

st.divider()
st.download_button("📥 DOWNLOAD MASTER DESIGN PACKAGE (PDF)", 
                   data=generate_master_pdf(res), 
                   file_name="Aero_Master_Design.pdf")
