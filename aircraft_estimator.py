import streamlit as st
import numpy as np
import math
import plotly.graph_objects as go
from fpdf import FPDF
import pandas as pd

# --- CONFIGURATION ---
st.set_page_config(page_title="AeroNova Simulator X", layout="wide")

# --- CYBER NEON CSS ---
st.markdown("""
    <style>
    .main { background: linear-gradient(135deg, #0b0d17 0%, #1a1c2c 100%); color: #00d4ff; }
    section[data-testid="stSidebar"] { background-color: rgba(10, 15, 30, 0.9) !important; border-right: 2px solid #7000ff; }
    div[data-testid="stMetric"] { background: rgba(0, 212, 255, 0.05); border: 1px solid #00d4ff; border-radius: 10px; padding: 15px; box-shadow: 0 0 15px rgba(0, 212, 255, 0.2); }
    h1, h2, h3 { color: #7000ff; text-shadow: 0 0 10px #7000ff; }
    .stSlider [data-baseweb="slider"] { color: #7000ff; }
    </style>
    """, unsafe_allow_html=True)

# --- CORRECTED ENGINEERING ENGINE ---
def calculate_physics(wto, pax, rc, sfc, ld, eta):
    # Constants from File/Standards
    m_res = 0.05
    m_tfo = 0.005
    w_crew = 615.0
    d_val = (pax * 205) + w_crew
    
    # 1. Fuel Fractions (Eq 2.44)
    f_pre = 0.970 
    f_cruise = math.exp(-rc / (375 * (eta / sfc) * ld))
    f_post = 0.990
    mff = f_pre * f_cruise * f_post
    
    # 2. Corrected Empty Weight Calculations
    wf = wto * (1 - mff) * (1 + m_res)
    we_req = wto - wf - d_val - (m_tfo * wto)
    
    # Statistical Allowable WE (The Corrected Equation)
    # Log10(WE) = (Log10(WTO) - 0.3774) / 0.9647
    we_allow = 10**((math.log10(wto) - 0.3774) / 0.9647)
    
    # 3. Sensitivity Analysis (Table 2.20)
    c_val = 1 - (1 + m_res) * (1 - mff) - m_tfo
    f_growth = 1 / (c_val - (0.9647 * (we_allow / wto)))
    dw_dr = (f_growth * wto * (1 + m_res) * (1 / (375 * (eta / sfc) * ld))) * f_cruise

    return {
        "mff": mff, "we_req": we_req, "we_allow": we_allow,
        "f_growth": f_growth, "dw_dr": dw_dr, "wf": wf, "d_val": d_val
    }

# --- SIDEBAR INPUTS ---
st.sidebar.title("⚡ CONTROL DECK")
wto_in = st.sidebar.slider("Design WTO (lbs)", 30000, 70000, 48550)
pax_in = st.sidebar.slider("Passengers", 10, 100, 34)
range_in = st.sidebar.slider("Range (miles)", 500, 3000, 1265)
ld_in = st.sidebar.slider("L/D Ratio", 10.0, 20.0, 13.0)
sfc_in = st.sidebar.number_input("SFC (Cp)", value=0.6)

res = calculate_physics(wto_in, pax_in, range_in, sfc_in, ld_in, 0.85)

# --- MAIN INTERFACE ---
st.title("🚀 AeroNova Simulator X")
st.write("### Next-Gen Conceptual Aircraft Sizing Matrix")

# Gauges & Key Stats
c1, c2, c3, c4 = st.columns(4)
c1.metric("Required WE", f"{res['we_req']:,.1f} lb")
c2.metric("Allowable WE", f"{res['we_allow']:,.1f} lb")
diff = res['we_req'] - res['we_allow']
c3.metric("Gap Delta", f"{diff:,.1f} lb", delta=diff, delta_color="inverse")
c4.metric("Growth Factor", f"{res['f_growth']:.3f}")

st.divider()

# Interactive Plots
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("🌐 Convergence Visualization")
    
    w_range = np.linspace(30000, 75000, 100)
    sweep = [calculate_physics(w, pax_in, range_in, sfc_in, ld_in, 0.85) for w in w_range]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=w_range, y=[x['we_req'] for x in sweep], name='Required WE (Mission)', line=dict(color='#00d4ff', width=4)))
    fig.add_trace(go.Scatter(x=w_range, y=[x['we_allow'] for x in sweep], name='Allowable WE (Stat)', line=dict(color='#7000ff', width=4, dash='dot')))
    fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.subheader("📑 Sensitivity Matrix")
    st.write(f"**Range Sensitivity:** {res['dw_dr']:.4f} lb/mi")
    st.write(f"**Payload Asset (D):** {res['d_val']:,.1f} lb")
    
    # Export CSV
    df = pd.DataFrame([res])
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Export CSV Data", csv, "aeronova_data.csv", "text/csv")

# PDF Generation
def export_pdf(d):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "AeroNova Simulator X - Engineering Report", ln=True, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.ln(10)
    for k, v in d.items():
        pdf.cell(0, 10, f"{k}: {v}", ln=True)
    return pdf.output(dest='S').encode('latin-1')

st.download_button("Download Full PDF Report", data=export_pdf(res), file_name="AeroNova_Report.pdf")
