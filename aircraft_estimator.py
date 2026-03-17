import streamlit as st
import math
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from fpdf import FPDF
import io

# --- 1. UI & Branding ---
st.set_page_config(page_title="AeroSystems Analysis Suite", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #FFFFFF; }
    .stMetric { border: 1px solid #E5E7EB; background-color: #F9FAFB; border-radius: 4px; padding: 10px; }
    h1, h2, h3 { color: #1E3A8A; font-family: 'Arial', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Aircraft Design & Sensitivity Control Center")
st.caption("Professional Engineering Dashboard | Manual WTO Control Mode")

# --- 2. Input Data Sheet ---
st.sidebar.header("📋 Input Specifications")
with st.sidebar.expander("Mission & Payload", expanded=True):
    rc = st.number_input("Range (Rc) - miles", value=1265.8)
    pax = st.number_input("Passengers", value=34)
    w_pl = pax * 205
    w_crew = st.number_input("Crew Weight (lbs)", value=615.0)

with st.sidebar.expander("Aerodynamic Ratios", expanded=True):
    ld_c = st.number_input("L/D Cruise", value=13.0)
    cp_c = st.number_input("Cp Cruise", value=0.6)
    np_c = st.number_input("Prop Efficiency (ηp)", value=0.85)
    m_res = st.number_input("Mres (Reserves)", value=0.05)
    m_tfo = st.number_input("Mtfo (Trapped Fuel)", value=0.005)

# --- 3. Variable WTO Input (The Driver) ---
st.subheader("⚙️ Control Panel: Gross Weight Adjustment")
wto_input = st.number_input("Set Take-off Weight (WTO) - lbs", value=48550.0, step=100.0)

# --- 4. Engineering Logic Engine ---
def run_analysis(wto):
    coeff_a, coeff_b = 0.3774, 0.9647
    
    # 1. Fuel Fractions (Step-by-step)
    f_start_climb = 0.990 * 0.995 * 0.995 * 0.985
    f_cruise = 1 / math.exp(rc / (375 * (np_c / cp_c) * ld_c))
    f_loiter = 0.970 
    f_des_land = 0.985 * 0.995
    mff = f_start_climb * f_cruise * f_loiter * f_des_land
    
    # 2. Factor C & D (Eq 2.22)
    c_val = 1 - (1 + m_res) * (1 - mff) - m_tfo
    d_val = w_pl + w_crew
    
    # 3. Weight Matching
    wf = wto * (1 - mff)
    we_calc = wto - wf - d_val - (m_tfo * wto)
    we_allow = 10**((math.log10(wto) - coeff_a) / coeff_b)
    
    # 4. Sensitivity F (Eq 2.44)
    num_f = -coeff_b * (wto**2) * (1 + m_res) * mff
    den_f = (c_val * wto * (1 - coeff_b)) - d_val
    f_factor = num_f / den_f if den_f != 0 else 0
    
    # 5. Derivatives (Eq 2.49 - 2.51)
    dw_dr = (f_factor * cp_c) / (375 * np_c * ld_c)
    dw_dcp = (f_factor * rc) / (375 * np_c * ld_c)
    
    return locals()

data = run_analysis(wto_input)

# --- 5. Dashboard Output ---
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("🔢 Computed Results")
    st.metric("Factor C", f"{data['c_val']:.4f}")
    st.metric("Sensitivity Factor (F)", f"{data['f_factor']:,.0f}")
    st.write("---")
    st.write(f"**Calculated WE:** {data['we_calc']:,.1f} lb")
    st.write(f"**Allowable WE:** {data['we_allow']:,.1f} lb")
    error = data['we_calc'] - data['we_allow']
    st.write(f"**Matching Error:** {error:,.1f} lb")

with col2:
    # High-End Excel Style Plot
    w_axis = np.linspace(30000, 80000, 100)
    sweep = [run_analysis(w) for w in w_axis]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=w_axis, y=[x['we_calc'] for x in sweep], name='Tentative WE (Required)', line=dict(color='#1E3A8A', width=3)))
    fig.add_trace(go.Scatter(x=w_axis, y=[x['we_allow'] for x in sweep], name='Allowable WE (Structural)', line=dict(color='#DC2626', width=3)))
    fig.add_vline(x=wto_input, line_dash="dot", line_color="#4B5563", annotation_text="Selected WTO")
    fig.update_layout(title="Weight Equilibrium Chart", xaxis_title="WTO (lbs)", yaxis_title="Empty Weight (lbs)", plot_bgcolor='white')
    fig.update_xaxes(showgrid=True, gridcolor='#F3F4F6')
    fig.update_yaxes(showgrid=True, gridcolor='#F3F4F6')
    st.plotly_chart(fig, use_container_width=True)

# --- 6. The "Why & How" PDF Generator (Fixed Encoding) ---
def generate_pdf():
    # استخدام 'latin-1' وتجنب الرموز الغريبة لحل مشكلة Unicode
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Aeronautical Design & Sensitivity Report", ln=True, align='C')
    pdf.ln(10)
    
    # Explanation Section
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "1. Design Methodology (Why we do this?)", ln=True)
    pdf.set_font("Arial", '', 11)
    msg = (
        "In conceptual design, we must match the aircraft's 'Structural Capability' "
        "(Allowable WE) with its 'Mission Requirement' (Calculated WE). "
        "The Selected WTO is the driver for all these calculations."
    )
    pdf.multi_cell(0, 7, msg)
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "2. Sensitivity Analysis (The meaning of F)", ln=True)
    pdf.set_font("Arial", '', 11)
    f_msg = (
        f"Sensitivity Factor F ({data['f_factor']:,.0f}) represents the growth factor. "
        "A high F value indicates that any weight added to the payload or structure "
        "will cause a massive spiral increase in the total Gross Weight."
    )
    pdf.multi_cell(0, 7, f_msg)
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "3. Key Numerical Outputs", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 8, f"- Selected Take-off Weight: {wto_input:,.2f} lbs", ln=True)
    pdf.cell(0, 8, f"- C Factor (Efficiency): {data['c_val']:.4f}", ln=True)
    pdf.cell(0, 8, f"- Weight impact per mile (dWTO/dR): {data['dw_dr']:.2f} lbs/mi", ln=True)
    
    # استخراج البيانات كـ bytes بطريقة متوافقة
    return pdf.output(dest='S').encode('latin-1', 'ignore')

st.divider()
st.subheader("📄 Engineering Report")
st.write("Click below to generate a detailed PDF explaining the logic behind the C factor, F factor, and why the WTO must converge for a successful design.")

btn = st.download_button(
    label="📥 Download Detailed PDF Report",
    data=generate_detailed_pdf() if 'generate_detailed_pdf' in locals() else generate_pdf(),
    file_name="Aircraft_Technical_Analysis.pdf",
    mime="application/pdf"
)
