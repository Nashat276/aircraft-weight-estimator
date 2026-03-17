import streamlit as st
import math
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from fpdf import FPDF

# --- 1. الهوية البصرية (Professional Design) ---
st.set_page_config(page_title="Aircraft Design Analysis - JUST Edition", layout="wide")
st.markdown("""
    <style>
    .report-box { border: 1px solid #E0E0E0; padding: 20px; border-radius: 5px; background-color: #FFFFFF; }
    .metric-label { font-weight: bold; color: #1E3A8A; }
    h1, h2, h3 { color: #1E3A8A; border-bottom: 2px solid #1E3A8A; padding-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("✈️ Conceptual Aircraft Design & Sensitivity Analysis")
st.info("هذا البرنامج يتبع تسلسل الحسابات في ملف Homework 1 & 2 خطوة بخطوة.")

# --- 2. مدخلات التصميم (المعطيات - Page 1) ---
st.header("1️⃣ Design Inputs (المعطيات)")
col_in1, col_in2, col_in3 = st.columns(3)

with col_in1:
    st.subheader("Payload & Crew")
    pax = st.number_input("Number of Passengers", value=34)
    w_pax_unit = 205 # 175 + 30 baggage
    w_pl = pax * w_pax_unit
    w_crew = st.number_input("Crew Weight (Wcrew)", value=615.0)
    st.caption(f"Total D (Fixed Weight): {w_pl + w_crew} lbs")

with col_in2:
    st.subheader("Mission Profile")
    rc = st.number_input("Range (Rc) - miles", value=1265.8)
    eltr = st.number_input("Endurance (E) - hrs", value=0.75)
    m_res = st.number_input("Reserve Ratio (Mres)", value=0.05)
    m_tfo = st.number_input("TFO Ratio (Mtfo)", value=0.005)

with col_in3:
    st.subheader("Performance Specs")
    ld_c = st.number_input("L/D Cruise", value=13.0)
    cp_c = st.number_input("Cp Cruise", value=0.6)
    np_c = st.number_input("ηp Cruise", value=0.85)

# --- 3. المتغير الأساسي (Control Section) ---
st.header("2️⃣ Gross Weight Control (Variable WTO)")
st.write("قم بتغيير الوزن الإجمالي لرؤية أثره على الحسابات (كما في الجدول اليدوي):")
wto_input = st.number_input("Set Take-off Weight (WTO) - lbs", value=48550.0, step=100.0)

# --- 4. محرك الحسابات (Step-by-Step Logic) ---
def calculate_mission(wto):
    # المرحلة 1: حساب كسر الوقود (Mff)
    f_fixed = 0.990 * 0.995 * 0.995 * 0.985
    f_cruise = 1 / math.exp(rc / (375 * (np_c / cp_c) * ld_c))
    f_loiter = 0.970 # القيمة المعتمدة في ملفك
    f_land = 0.985 * 0.995
    mff = f_fixed * f_cruise * f_loiter * f_land
    
    # المرحلة 2: حساب المعاملات (C and D) - Eq 2.22
    c_val = 1 - (1 + m_res) * (1 - mff) - m_tfo
    d_val = w_pl + w_crew
    
    # المرحلة 3: مقارنة الأوزان (Matching)
    wf = wto * (1 - mff)
    we_required = wto - wf - d_val - (m_tfo * wto)
    # Allowable WE using Log10 (Step 6 in your file)
    coeff_a, coeff_b = 0.3774, 0.9647
    we_structural = 10**((math.log10(wto) - coeff_a) / coeff_b)
    
    # المرحلة 4: معامل الحساسية (F) - Eq 2.44
    num_f = -coeff_b * (wto**2) * (1 + m_res) * mff
    den_f = (c_val * wto * (1 - coeff_b)) - d_val
    f_factor = num_f / den_f if den_f != 0 else 0
    
    # المرحلة 5: مشتقات الحساسية (Sensitivity) - Page 2
    dw_dr = (f_factor * cp_c) / (375 * np_c * ld_c)
    dw_dcp = (f_factor * rc) / (375 * np_c * ld_c)
    
    return locals()

res = calculate_mission(wto_input)

# --- 5. عرض النتائج بترتيب الملف (Output Display) ---
st.header("3️⃣ Results & Verification (النتائج والتحقق)")
col_res1, col_res2 = st.columns(2)

with col_res1:
    st.markdown("**Intermediate Factors:**")
    st.write(f"Fuel Fraction (Mff): `{res['mff']:.4f}`")
    st.write(f"C Factor (Efficiency): `{res['c_val']:.4f}`")
    st.write(f"Sensitivity F Factor: `{res['f_factor']:,.2f}`")

with col_res2:
    st.markdown("**Weight Matching (The Balance):**")
    st.write(f"Required WE (from Mission): `{res['we_required']:,.1f} lbs`")
    st.write(f"Allowable WE (from Structure): `{res['we_structural']:,.1f} lbs`")
    diff = res['we_required'] - res['we_structural']
    st.warning(f"Difference (Error): {diff:,.1f} lbs")

# --- 6. الرسوم البيانية (Excel-Style Charts) ---
st.header("4️⃣ Graphical Analysis (العلاقات الهندسية)")

w_range = np.linspace(30000, 80000, 50)
sweep = [calculate_mission(w) for w in w_range]

fig = go.Figure()
fig.add_trace(go.Scatter(x=w_range, y=[x['we_required'] for x in sweep], name='Required WE', line=dict(color='blue', width=2)))
fig.add_trace(go.Scatter(x=w_range, y=[x['we_structural'] for x in sweep], name='Allowable WE', line=dict(color='red', width=2)))
fig.add_vline(x=wto_input, line_dash="dash", line_color="black", annotation_text="Your WTO")
fig.update_layout(title="Finding the Equilibrium Point (Intersection)", xaxis_title="Gross Weight (WTO)", yaxis_title="Empty Weight (WE)", plot_bgcolor='white')
st.plotly_chart(fig, use_container_width=True)

# --- 7. تحليل الحساسية (Page 2) ---
st.header("5️⃣ Sensitivity Analysis (تحليل الحساسية)")
st.write("هذه الأرقام توضح كيف سيتغير وزن الطائرة الإجمالي إذا تغيرت مدخلات التصميم:")
col_s1, col_s2 = st.columns(2)
col_s1.info(f"**∂WTO / ∂Range (dW/dR):** {res['dw_dr']:.2f} lbs/mile")
col_s2.info(f"**∂WTO / ∂Cp (dW/dCp):** {res['dw_dcp']:.2f} lbs/unit")

# --- 8. التقرير المفصل (PDF Explanation) ---
def generate_detailed_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Engineering Report: Aircraft Design & Sensitivity", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "1. Objective and Process", ln=True)
    pdf.set_font("Arial", '', 11)
    process = (
        "This study aims to find the equilibrium Take-off Weight (WTO). "
        "We use a variable WTO to calculate the fuel needed for the mission. "
        "The intersection of Required Weight and Allowable Structural Weight gives us the feasible design point."
    )
    pdf.multi_cell(0, 7, process)
    
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "2. Sensitivity Logic (Factor F)", ln=True)
    pdf.set_font("Arial", '', 11)
    f_logic = (
        f"The Sensitivity Factor F ({res['f_factor']:,.2f}) is the growth multiplier. "
        "It indicates that for every unit of weight added, the total aircraft grows by this factor "
        "due to the additional fuel and wing area needed to lift it."
    )
    pdf.multi_cell(0, 7, f_logic)
    
    return pdf.output(dest='S').encode('latin-1', 'ignore')

st.divider()
st.download_button("📥 Download Comprehensive Engineering Report (PDF)", 
                   data=generate_detailed_pdf(), 
                   file_name="Aircraft_Technical_Analysis.pdf")
