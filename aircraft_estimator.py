import streamlit as st
import math
import numpy as np
import plotly.graph_objects as go
from fpdf import FPDF
from datetime import date

# ==========================================
# 1. إعدادات الصفحة (Clean Workspace)
# ==========================================
st.set_page_config(page_title="Aircraft Sizing | Thesis Edition", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #FAFAFA; color: #1E1E1E; font-family: 'Arial', sans-serif; }
    h1, h2, h3 { color: #003366; }
    .stTabs [data-baseweb="tab-list"] { gap: 15px; }
    .stTabs [data-baseweb="tab"] { font-weight: bold; font-size: 16px; padding: 10px; }
    .stTabs [aria-selected="true"] { border-bottom: 3px solid #003366 !important; color: #003366 !important; }
    div[data-testid="stMetric"] { background: #FFFFFF; border: 1px solid #E0E0E0; border-left: 4px solid #003366; padding: 15px; box-shadow: 1px 1px 5px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. المحرك الحسابي (Math & Equations)
# ==========================================
def calculate_sizing_and_sensitivity(wto, pax, crew, rc, ld_c, cp_c, np_c, m_res, m_tfo):
    # 1. الأوزان الثابتة (Payload & Crew)
    w_payload = pax * 205
    d_val = w_payload + crew
    
    # 2. حساب أجزاء الوقود (Mission Fuel Fractions)
    f_p = 0.990 * 0.995 * 0.995 * 0.985 # Engine start, taxi, takeoff, climb
    f_c = math.exp(-rc / (375 * (np_c / cp_c) * ld_c)) # Cruise (Eq. 2.23 & 2.44)
    f_l = 0.990 # Loiter/Descent assumed fraction
    f_e = 0.985 * 0.995 # Landing
    
    mff = f_p * f_c * f_l * f_e # Total Mission Fuel Fraction
    
    # 3. حساب الأوزان (Weight Matching)
    wf = wto * (1 - mff) # Total Fuel Weight
    we_req = wto - wf - d_val - (m_tfo * wto) # Required Empty Weight (Eq 2.22)
    we_allow = 10**((math.log10(wto) - 0.3774) / 0.9647) # Statistical Allowable WE
    
    # 4. معاملات الحساسية (Table 2.20 & Growth Factor F)
    c_val = 1 - (1 + m_res) * (1 - mff) - m_tfo
    num_f = -0.9647 * (wto**2) * (1 + m_res) * mff
    den_f = (c_val * wto * (1 - 0.9647)) - d_val
    f_growth = num_f / den_f if den_f != 0 else 0
    
    # Derivatives (Eq 2.49 etc)
    dw_dr = (f_growth * cp_c) / (375 * np_c * ld_c)
    dw_dcp = (f_growth * rc) / (375 * np_c * ld_c)

    return {
        "wto": wto, "d_val": d_val, "wf": wf, 
        "mff": mff, "f_c": f_c, 
        "we_req": we_req, "we_allow": we_allow,
        "f_growth": f_growth, "dw_dr": dw_dr, "dw_dcp": dw_dcp,
        "m_res": m_res, "m_tfo": m_tfo
    }

# ==========================================
# 3. المدخلات (مفصلة في القائمة الجانبية)
# ==========================================
st.sidebar.title("📑 Input Parameters")

with st.sidebar.expander("1. Design Weight", expanded=True):
    wto_in = st.number_input("Design WTO (lbs)", value=48550.0, step=100.0)

with st.sidebar.expander("2. Payload & Crew", expanded=True):
    pax_in = st.number_input("Number of PAX", value=34)
    crew_in = st.number_input("Crew Weight (lbs)", value=615.0)

with st.sidebar.expander("3. Mission & Aero", expanded=True):
    rc_in = st.number_input("Range - Rc (miles)", value=1265.8)
    ld_c_in = st.number_input("Cruise L/D", value=13.0)
    cp_c_in = st.number_input("SFC - Cp", value=0.6, format="%.3f")
    np_c_in = st.number_input("Prop Efficiency - ηp", value=0.85)

with st.sidebar.expander("4. Fuel Fractions", expanded=True):
    m_res_in = st.number_input("Reserve Fuel (Mres)", value=0.05, format="%.2f")
    m_tfo_in = st.number_input("Trapped Fuel (Mtfo)", value=0.005, format="%.3f")

# التنفيذ
res = calculate_sizing_and_sensitivity(wto_in, pax_in, crew_in, rc_in, ld_c_in, cp_c_in, np_c_in, m_res_in, m_tfo_in)

# ==========================================
# 4. الواجهة الرئيسية (كل قسم لحال)
# ==========================================
st.title("✈️ Conceptual Aircraft Sizing & Sensitivity Analysis")
st.markdown("---")

# ملخص سريع أعلى الصفحة
c1, c2, c3, c4 = st.columns(4)
c1.metric("Mission Fuel Fraction (Mff)", f"{res['mff']:.4f}")
c2.metric("Required Empty Wt (WE)", f"{res['we_req']:,.1f} lbs")
c3.metric("Growth Factor (F)", f"{res['f_growth']:.3f}")
c4.metric("Convergence Delta", f"{(res['we_req'] - res['we_allow']):,.1f} lbs")

st.markdown("<br>", unsafe_allow_html=True)

# تقسيم النتائج لتبويبات (Tabs)
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 1. Weight Matching", 
    "🧮 2. Mission Breakdown", 
    "📉 3. Sensitivity (Table 2.20)", 
    "📑 4. Export Thesis PDF"
])

with tab1:
    st.subheader("Weight Convergence & Sizing")
    col_chart, col_data = st.columns([2, 1])
    
    with col_chart:
        w_axis = np.linspace(35000, 70000, 50)
        sweep = [calculate_sizing_and_sensitivity(w, pax_in, crew_in, rc_in, ld_c_in, cp_c_in, np_c_in, m_res_in, m_tfo_in) for w in w_axis]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=w_axis, y=[x['we_req'] for x in sweep], name='Req. Empty Weight', line=dict(color='#003366', width=3)))
        fig.add_trace(go.Scatter(x=w_axis, y=[x['we_allow'] for x in sweep], name='Allow. Empty Weight', line=dict(color='#CC0000', width=3, dash='dash')))
        fig.add_trace(go.Scatter(x=[wto_in], y=[res['we_req']], mode='markers+text', text=["Design Point"], textposition="top center", marker=dict(size=12, color='#009900')))
        
        fig.update_layout(template="simple_white", xaxis_title="Gross Weight (WTO) [lbs]", yaxis_title="Empty Weight (WE) [lbs]", margin=dict(t=20, b=20))
        st.plotly_chart(fig, use_container_width=True)
        
    with col_data:
        st.write("**Key Weights (lbs)**")
        st.dataframe({
            "Component": ["Payload & Crew (D)", "Total Fuel (Wf)", "Required WE", "Allowable WE"],
            "Value": [f"{res['d_val']:,.1f}", f"{res['wf']:,.1f}", f"{res['we_req']:,.1f}", f"{res['we_allow']:,.1f}"]
        }, hide_index=True)

with tab2:
    st.subheader("Mission Fuel Fractions")
    st.write("Detailed breakdown of fuel consumption across the mission profile.")
    st.dataframe({
        "Parameter": ["Total Mission Fraction (Mff)", "Cruise Fraction (fc)", "Reserve Ratio (Mres)", "Trapped Ratio (Mtfo)"],
        "Value": [f"{res['mff']:.4f}", f"{res['f_c']:.4f}", f"{res['m_res']:.3f}", f"{res['m_tfo']:.3f}"]
    }, hide_index=True)

with tab3:
    st.subheader("Sensitivity Derivatives (Ref: Table 2.20)")
    st.write("Measures the impact of aerodynamic and propulsive changes on the Design Gross Weight.")
    st.dataframe({
        "Derivative": ["Growth Factor (F = dWTO/dD)", "Range Penalty (dWTO/dR)", "SFC Penalty (dWTO/dCp)"],
        "Calculated Value": [f"{res['f_growth']:.3f}", f"{res['dw_dr']:.4f} lbs/mile", f"{res['dw_dcp']:,.2f} lbs/unit"]
    }, hide_index=True)

with tab4:
    st.subheader("Generate Official PDF Report")
    st.write("Export the results in a formal academic format suitable for graduation project documentation.")
    
    def generate_thesis_pdf(data):
        pdf = FPDF()
        pdf.add_page()
        
        # --- Cover Page Style Header ---
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 8, "JORDAN UNIVERSITY OF SCIENCE AND TECHNOLOGY (JUST)", ln=True, align='C')
        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 6, "Aeronautical Engineering Department", ln=True, align='C')
        pdf.ln(10)
        
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "AIRCRAFT CONCEPTUAL SIZING & SENSITIVITY REPORT", ln=True, align='C')
        pdf.set_font("Arial", 'I', 11)
        pdf.cell(0, 6, f"Date: {date.today().strftime('%B %d, %Y')}", ln=True, align='C')
        pdf.cell(0, 6, "Prepared by: Eng. Nashat Al-Dhoun", ln=True, align='C')
        pdf.line(10, 55, 200, 55)
        pdf.ln(15)
        
        # --- Section 1: Inputs ---
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 8, "1. INITIAL DESIGN PARAMETERS", ln=True)
        pdf.set_font("Arial", '', 11)
        pdf.cell(0, 6, f"   - Design Gross Weight (WTO): {data['wto']:,.1f} lbs", ln=True)
        pdf.cell(0, 6, f"   - Payload & Crew (D): {data['d_val']:,.1f} lbs", ln=True)
        pdf.cell(0, 6, f"   - Mission Range (Rc): {rc_in} miles", ln=True)
        pdf.ln(5)
        
        # --- Section 2: Weight Convergence ---
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 8, "2. WEIGHT MATCHING RESULTS", ln=True)
        pdf.set_font("Arial", '', 11)
        pdf.cell(0, 6, f"   - Mission Fuel Fraction (Mff): {data['mff']:.4f}", ln=True)
        pdf.cell(0, 6, f"   - Total Fuel Weight (Wf): {data['wf']:,.1f} lbs", ln=True)
        pdf.cell(0, 6, f"   - Required Empty Weight: {data['we_req']:,.1f} lbs", ln=True)
        pdf.cell(0, 6, f"   - Allowable Empty Weight: {data['we_allow']:,.1f} lbs", ln=True)
        delta = data['we_req'] - data['we_allow']
        pdf.cell(0, 6, f"   - Convergence Delta: {delta:,.1f} lbs", ln=True)
        pdf.ln(5)
        
        # --- Section 3: Sensitivity Analysis ---
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 8, "3. SENSITIVITY DERIVATIVES (TABLE 2.20)", ln=True)
        pdf.set_font("Arial", '', 11)
        pdf.cell(0, 6, f"   - Growth Factor (F): {data['f_growth']:.3f}", ln=True)
        pdf.cell(0, 6, f"   - Range Sensitivity (dWTO/dR): {data['dw_dr']:.4f} lbs/mi", ln=True)
        pdf.cell(0, 6, f"   - SFC Sensitivity (dWTO/dCp): {data['dw_dcp']:,.2f} lbs/unit", ln=True)
        
        return pdf.output(dest='S').encode('latin-1')

    st.download_button(
        label="📥 Download Thesis Report (PDF)",
        data=generate_thesis_pdf(res),
        file_name="Nashat_AlDhoun_Sizing_Report.pdf",
        mime="application/pdf"
        )
