import streamlit as st
import math
import numpy as np
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import io

# --- 1. UI Setup ---
st.set_page_config(page_title="AeroDesign Interactive Controller", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #FFFFFF; }
    .stMetric { border-top: 5px solid #002D72; background-color: #F8F9FA; border-radius: 8px; padding: 20px; }
    h1, h2, h3 { color: #002D72; font-family: 'Segoe UI', sans-serif; }
    .stSlider [data-baseweb="slider"] { margin-bottom: 25px; }
    </style>
    """, unsafe_allow_html=True)

st.title("✈️ Aircraft Weight & Sensitivity Controller")
st.caption("Manual Weight Control Mode | Equations 2.22, 2.44, and 2.49 Integrated")
st.divider()

# --- 2. Sidebar & Global Inputs ---
st.sidebar.header("🕹️ Global Constants")
pax = st.sidebar.number_input("Number of Passengers", value=34)
w_pl = pax * 205
w_crew = st.sidebar.number_input("Crew Weight (lbs)", value=615.0)
d_val = w_pl + w_crew # D Factor from your equations

# --- 3. Main Variable: Take-off Weight (WTO) ---
st.subheader("⚙️ Control Panel: Variable Gross Weight")
# جعلنا WTO متغير يتحكم فيه المستخدم يدوياً
wto_var = st.slider("Adjust Take-off Weight (WTO) in lbs", 
                   min_value=30000.0, 
                   max_value=100000.0, 
                   value=48550.0, 
                   step=10.0)

# --- 4. Engineering Engine (Logic from your notes) ---
def calculate_system(wto):
    # Performance Constants
    rc, ld_c, cp_c, np_c = 1265.8, 13.0, 0.6, 0.85
    eltr, ld_l, cp_l, np_l = 0.75, 16.0, 0.65, 0.80
    m_res, m_tfo = 0.05, 0.005
    coeff_a, coeff_b = 0.3774, 0.9647

    # Phase Fractions
    f_fixed = 0.990 * 0.995 * 0.995 * 0.985
    f_cruise = 1 / math.exp(rc / (375 * (np_c / cp_c) * ld_c))
    f_loiter = 0.970 
    f_end = 0.985 * 0.995
    mff = f_fixed * f_cruise * f_loiter * f_end
    
    # Factor C (Eq 2.22)
    c_val = 1 - (1 + m_res) * (1 - mff) - m_tfo
    
    # Weight Analysis
    wf = wto * (1 - mff)
    we_calc = wto - wf - d_val - (m_tfo * wto)
    # Correct Log10 Usage for Allowable WE
    we_allow = 10**((math.log10(wto) - coeff_a) / coeff_b)
    
    # Sensitivity Factor F (Eq 2.44)
    num_f = -coeff_b * (wto**2) * (1 + m_res) * mff
    den_f = (c_val * wto * (1 - coeff_b)) - d_val
    f_factor = num_f / den_f if den_f != 0 else 0

    # Range Sensitivity (Eq 2.49 & 2.51)
    dwto_dcp = (f_factor * rc) / (375 * np_c * ld_c)
    dwto_dr = (f_factor * cp_c) / (375 * np_c * ld_c)

    return {
        "mff": mff, "wf": wf, "we_c": we_calc, "we_a": we_allow, "f": f_factor,
        "c": c_val, "dw_dcp": dwto_dcp, "dw_dr": dwto_dr
    }

# --- 5. Execution & Visual Output ---
res = calculate_system(wto_var)
error = res['we_c'] - res['we_a']

# Performance Metrics Dashboard
st.subheader("🏁 Real-Time Analysis")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Current WTO", f"{wto_var:,.0f} lb")
col2.metric("Calculated WE", f"{res['we_c']:,.1f} lb")
col3.metric("Allowable WE", f"{res['we_a']:,.1f} lb")
col4.metric("Convergence Error", f"{error:,.1f} lb", delta=error, delta_color="inverse")

# Sensitivity Results Table
st.divider()
st.subheader("📉 Sensitivity Calculations (Eq 2.44 - 2.51)")
s1, s2, s3 = st.columns(3)
s1.info(f"**Sensitivity Factor (F):**\n\n {res['f']:,.0f}")
s2.info(f"**∂WTO / ∂Cp:**\n\n {res['dw_dcp']:,.2f} lbs/unit")
s3.info(f"**∂WTO / ∂R:**\n\n {res['dw_dr']:,.2f} lbs/mile")

# Visual Explanation of the Error
st.divider()
st.subheader("📊 Convergence Graphic")
st.write("The goal is to adjust WTO until **Calculated WE** matches **Allowable WE** (Error = 0).")

w_axis = np.linspace(30000, 80000, 100)
sweep = [calculate_system(w) for w in w_axis]
df_plot = pd.DataFrame({
    "WTO": w_axis,
    "Calculated Empty Weight": [x['we_c'] for x in sweep],
    "Allowable Empty Weight": [x['we_a'] for x in sweep]
})

fig = px.line(df_plot, x="WTO", y=["Calculated Empty Weight", "Allowable Empty Weight"], 
              color_discrete_sequence=["#002D72", "#D62728"],
              title="Weight Convergence (Find the intersection point)")
# إضافة خط يوضح موقع الوزن الحالي الذي اختاره المستخدم
fig.add_vline(x=wto_var, line_dash="dash", line_color="black", annotation_text="Your Current Selection")
fig.update_layout(plot_bgcolor='white', hovermode="x unified")
st.plotly_chart(fig, use_container_width=True)

# PDF Generation
def gen_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "Aircraft Weight & Sensitivity Report", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Selected Take-off Weight: {wto_var:,.2f} lbs", ln=True)
    pdf.cell(0, 10, f"Sensitivity Factor F: {res['f']:,.2f}", ln=True)
    pdf.cell(0, 10, f"Weight/Range Sensitivity (dWTO/dR): {res['dw_dr']:,.2f} lbs/mi", ln=True)
    return pdf.output(dest='S').encode('latin-1')

pdf_data = gen_pdf()
st.download_button("📥 DOWNLOAD TECHNICAL REPORT (PDF)", data=pdf_data, file_name="Aircraft_Report.pdf")
