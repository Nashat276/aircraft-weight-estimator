import streamlit as st
import math
import numpy as np
import plotly.graph_objects as go
from fpdf import FPDF

# --- 1. UI & COLOR OPTIMIZATION ---
st.set_page_config(page_title="AeroOptimizer Pro v4.0", layout="wide")

# تحسين ألوان القائمة الجانبية لتتناسب مع النص
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background-color: #1E293B; /* Slate Dark Blue */
        color: #F8FAFC;
    }
    [data-testid="stSidebar"] .stMarkdown p {
        color: #E2E8F0 !important;
        font-size: 14px;
    }
    .main { background-color: #F1F5F9; }
    div[data-testid="stMetric"] { 
        background-color: #FFFFFF; 
        border-radius: 10px; 
        padding: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR: EXTENDED INPUTS (Table 2.15 & 2.20 Specs) ---
st.sidebar.title("🚀 Design Parameters")
st.sidebar.markdown("Full Configuration Suite")

# Main Variable
wto_input = st.sidebar.number_input("Gross Take-off Weight (WTO) - lbs", value=48550.0, step=50.0)

with st.sidebar.expander("👤 Payload & Crew Assets", expanded=True):
    pax = st.number_input("Passengers", value=34)
    w_pl = pax * 205
    w_crew = st.number_input("Crew Weight", value=615.0)
    d_val = w_pl + w_crew

with st.sidebar.expander("✈️ Phase 1: Cruise (Table 2.20 Parameters)", expanded=True):
    rc = st.number_input("Range (Rc) - miles", value=1265.8)
    ld_c = st.number_input("L/D Cruise", value=13.0)
    cp_c = st.number_input("SFC (Cp) Cruise", value=0.6)
    np_c = st.number_input("ηp Cruise", value=0.85)

with st.sidebar.expander("🔄 Phase 2: Loiter Phase", expanded=True):
    eltr = st.number_input("Endurance (E) - hrs", value=0.75)
    ld_l = st.number_input("L/D Loiter", value=16.0)
    cp_l = st.number_input("SFC (Cp) Loiter", value=0.65)
    np_l = st.number_input("ηp Loiter", value=0.80)

with st.sidebar.expander("🛡️ Fuel & Structure Constants", expanded=False):
    m_res = st.number_input("Reserve Ratio", value=0.05)
    m_tfo = st.number_input("TFO Ratio", value=0.005)
    coeff_a = 0.3774
    coeff_b = 0.9647

# --- 3. AEROSPACE CALCULATION ENGINE ---
def run_analysis(wto):
    # Step 1: Fuel Fractions (Mission Profile)
    f_fixed = 0.990 * 0.995 * 0.995 * 0.985 # Start to Climb
    f_cruise = 1 / math.exp(rc / (375 * (np_c / cp_c) * ld_c))
    f_loiter = 1 / math.exp(eltr / (375 * (np_l / cp_l) * ld_l)) # Using Eq for Loiter
    f_land = 0.985 * 0.995
    mff = f_fixed * f_cruise * f_loiter * f_land
    
    # Step 2: Factors C and D (Eq 2.22)
    c_val = 1 - (1 + m_res) * (1 - mff) - m_tfo
    
    # Step 3: WE Matching
    wf = wto * (1 - mff)
    we_req = wto - wf - d_val - (m_tfo * wto)
    we_allow = 10**((math.log10(wto) - coeff_a) / coeff_b)
    
    # Step 4: Sensitivity Equations (Reference Table 2.20)
    # F factor calculates how much WTO grows per 1lb of added fixed weight
    f_growth = (-coeff_b * (wto**2) * (1 + m_res) * mff) / ((c_val * wto * (1 - coeff_b)) - d_val)
    
    # Derivatives for Range and SFC
    dw_dr = (f_growth * cp_c) / (375 * np_c * ld_c)
    dw_dcp = (f_growth * rc) / (375 * np_c * ld_c)
    
    return locals()

res = run_analysis(wto_input)

# --- 4. MAIN INTERFACE ---
st.title("AeroSystems Sizing & Sensitivity Matrix")
st.markdown("Professional Multidisciplinary Analysis based on **JUST Engineering Framework**.")

# Dashboard Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Mission Mff", f"{res['mff']:.4f}")
col2.metric("Growth Factor (F)", f"{res['f_growth']:,.2f}")
col3.metric("Efficiency (C)", f"{res['c_val']:.4f}")
error = res['we_req'] - res['we_allow']
col4.metric("Matching Error", f"{error:,.1f} lb", delta=error, delta_color="inverse")

# High-Precision Graphic
st.subheader("Weight Equilibrium Chart (Convergence Mapping)")

w_range = np.linspace(35000, 75000, 100)
sweep = [run_analysis(w) for w in w_range]

fig = go.Figure()
fig.add_trace(go.Scatter(x=w_range, y=[x['we_req'] for x in sweep], name='Required WE (Mission)', line=dict(color='#3B82F6', width=3)))
fig.add_trace(go.Scatter(x=w_range, y=[x['we_allow'] for x in sweep], name='Allowable WE (Structure)', line=dict(color='#EF4444', width=3, dash='dot')))
fig.add_trace(go.Scatter(x=[wto_input], y=[res['we_req']], mode='markers', marker=dict(size=12, color='#10B981'), name='Design Point'))

fig.update_layout(plot_bgcolor='white', margin=dict(l=0, r=0, t=30, b=0), legend=dict(orientation="h", y=1.1))
st.plotly_chart(fig, use_container_width=True)

# Sensitivity Section (Table 2.20 Logic)
st.subheader("📉 Design Sensitivity Derivatives")
st.write("Quantitative analysis of WTO response to mission parameter variations.")
s_col1, s_col2 = st.columns(2)
s_col1.info(f"**∂WTO / ∂Range:** {res['dw_dr']:.4f} lbs/mi")
s_col2.info(f"**∂WTO / ∂Cp (Cruise):** {res['dw_dcp']:.2f} lbs per unit SFC")

# --- 5. ENHANCED PDF MASTER REPORT ---
def generate_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    
    # Layout Frame
    pdf.set_draw_color(30, 41, 59)
    pdf.rect(5, 5, 200, 287)
    
    # Header Section
    pdf.set_fill_color(30, 41, 59)
    pdf.rect(5, 5, 200, 40, 'F')
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", 'B', 18)
    pdf.cell(0, 20, "AIRCRAFT TECHNICAL SPECIFICATION REPORT", ln=True, align='C')
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(0, 5, "Generated for Senior Design Analysis | Boeing/Airbus Standard", ln=True, align='C')
    
    pdf.set_text_color(0, 0, 0)
    pdf.ln(25)
    
    # Section 1: Methodology
    pdf.set_font("Arial", 'B', 13)
    pdf.set_fill_color(241, 245, 249)
    pdf.cell(0, 10, " 1. ENGINEERING METHODOLOGY", ln=True, fill=True)
    pdf.set_font("Arial", '', 10)
    pdf.multi_cell(0, 6, "This analysis utilizes the iterative sizing method to determine the design Gross Weight (WTO). By calculating fuel fractions across Cruise and Loiter phases and matching them against statistical structural models (Eq 2.22), we identify the feasibility of the airframe.")
    
    # Section 2: Input Matrix
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 13)
    pdf.cell(0, 10, " 2. DESIGN INPUT PARAMETERS", ln=True, fill=True)
    pdf.set_font("Arial", '', 10)
    pdf.cell(95, 7, f"- Target WTO: {wto_input:,.1f} lbs", ln=0)
    pdf.cell(95, 7, f"- Payload (D Factor): {d_val:,.1f} lbs", ln=1)
    pdf.cell(95, 7, f"- Cruise Range: {rc} miles", ln=0)
    pdf.cell(95, 7, f"- Cruise L/D: {ld_c}", ln=1)
    pdf.cell(95, 7, f"- Loiter Endurance: {eltr} hrs", ln=0)
    pdf.cell(95, 7, f"- Loiter L/D: {ld_l}", ln=1)
    
    # Section 3: Performance & Sensitivity
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 13)
    pdf.cell(0, 10, " 3. PERFORMANCE & SENSITIVITY (TABLE 2.20)", ln=True, fill=True)
    pdf.set_font("Arial", '', 10)
    pdf.multi_cell(0, 6, f"The Growth Factor (F) is calculated at {data['f_growth']:.2f}. This means for every 1 lb added to the fixed weight, the aircraft must grow by {data['f_growth']:.2f} lbs to maintain performance. The range sensitivity (dW/dR) shows a penalty of {data['dw_dr']:.4f} lbs per mile added.")
    
    # Final Confirmation
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, f"Current Convergence Delta: {error:,.2f} lbs", ln=True, align='R')
    
    return pdf.output(dest='S').encode('latin-1', 'ignore')

st.divider()
st.download_button("📥 DOWNLOAD MASTER DESIGN PACKAGE (PDF)", 
                   data=generate_pdf(res), 
                   file_name="Aircraft_Technical_Package.pdf")
