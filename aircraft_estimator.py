import streamlit as st
import math
import numpy as np
import plotly.graph_objects as go
from fpdf import FPDF

# --- 1. إعدادات هندسية نظيفة ---
st.set_page_config(page_title="AeroOptimizer Pro", layout="wide")
st.markdown("<style>.main {background-color: #f9f9f9;}</style>", unsafe_allow_html=True)

# --- 2. المحرك الحسابي المدقق ---
def aircraft_sizing_engine(wto, pax, crew, rc, ld_c, cp_c, np_c):
    # أ- الثوابت (Standard Factors)
    m_res = 0.05   # 5% Reserve
    m_tfo = 0.005  # 0.5% Trapped Fuel & Oil
    
    # ب- حساب الحمولة (D-Factor)
    w_payload = pax * 205
    d_val = w_payload + crew
    
    # ج- حساب أجزاء الوقود (Mission Fractions)
    # f1*f2*f3*f4 (Takeoff & Climb) = 0.970 (Typical for Turboprop/Regional)
    f_pre_cruise = 0.970 
    # Cruise Fraction (Eq. 2.44)
    f_cruise = math.exp(-rc / (375 * (np_c / cp_c) * ld_c))
    # f_landing/descent = 0.990
    f_post_cruise = 0.990
    
    mff = f_pre_cruise * f_cruise * f_post_cruise
    
    # د- حساب الأوزان (The Core Logic)
    wf = wto * (1 - mff) * (1 + m_res) # الوقود مع الاحتياطي
    
    # 1. Required Empty Weight (من معادلة التوازن)
    # WE_req = WTO - W_fuel - W_payload - W_crew - W_tfo
    we_req = wto - wf - d_val - (m_tfo * wto)
    
    # 2. Allowable Empty Weight (المعادلة الإحصائية لـ JUST)
    # Log10(WE) = (Log10(WTO) - A) / B
    # للأوزان المتوسطة (Turboprop): A = 0.3774, B = 0.9647
    we_allow = 10**((math.log10(wto) - 0.3774) / 0.9647)
    
    # هـ- معاملات الحساسية (F & Derivatives)
    c_val = 1 - (1 + m_res) * (1 - mff) - m_tfo
    # F = dWTO / dD (Growth Factor)
    # المشتقة الإحصائية للهيكل هي 0.9647
    f_growth = 1 / (c_val - (0.9647 * (we_allow / wto)))
    
    dw_dr = (f_growth * wto * (1 + m_res) * (1 / (375 * (np_c / cp_c) * ld_c))) * f_cruise
    
    return {
        "mff": mff, "wf": wf, "we_req": we_req, "we_allow": we_allow,
        "f_growth": f_growth, "dw_dr": dw_dr, "d_val": d_val
    }

# --- 3. واجهة المستخدم ---
st.sidebar.header("🛠️ Input Parameters")
wto_in = st.sidebar.number_input("Design WTO (lbs)", value=48550.0)
pax_in = st.sidebar.number_input("Passengers", value=34)
rc_in = st.sidebar.number_input("Range (mi)", value=1265.8)
cp_in = st.sidebar.number_input("SFC (Cp)", value=0.6)
ld_in = st.sidebar.number_input("L/D", value=13.0)

# تنفيذ الحسابات
res = aircraft_sizing_engine(wto_in, pax_in, 615.0, rc_in, ld_in, cp_in, 0.85)

# --- 4. عرض النتائج بترتيب منطقي ---
st.title("🛡️ Aircraft Sizing Verification")
st.info("تم تدقيق معادلات الوزن الفارغ (Required vs Allowable) بناءً على المعايير الإحصائية.")

# عرض الأرقام الكبرى
c1, c2, c3 = st.columns(3)
c1.metric("Required WE (Mission)", f"{res['we_req']:,.1f} lbs")
c2.metric("Allowable WE (Stat)", f"{res['we_allow']:,.1f} lbs")
diff = res['we_req'] - res['we_allow']
c3.metric("Gap (Difference)", f"{diff:,.1f} lbs", delta=diff, delta_color="inverse")

st.divider()

# التبويبات لتنظيم المخرجات
t1, t2 = st.tabs(["📈 Convergence Map", "📄 Technical Report"])

with t1:
    
    w_range = np.linspace(35000, 75000, 100)
    sweep = [aircraft_sizing_engine(w, pax_in, 615.0, rc_in, ld_in, cp_in, 0.85) for w in w_range]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=w_range, y=[x['we_req'] for x in sweep], name='Required WE', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=w_range, y=[x['we_allow'] for x in sweep], name='Allowable WE', line=dict(color='red', dash='dash')))
    fig.update_layout(title="Weight Matching (Sizing Chart)", template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

with t2:
    st.subheader("Summary Table")
    st.table({
        "Parameter": ["Total Fuel (Inc. Reserves)", "Payload Factor (D)", "Growth Factor (F)", "Range Sensitivity (dW/dR)"],
        "Value": [f"{res['wf']:,.1f} lbs", f"{res['d_val']:,.1f} lbs", f"{res['f_growth']:.3f}", f"{res['dw_dr']:.4f} lb/mi"]
    })
