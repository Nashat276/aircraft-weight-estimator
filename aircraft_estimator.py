import streamlit as st
import math
import numpy as np
import pandas as pd
import plotly.express as px

# إعدادات الصفحة
st.set_page_config(page_title="Aircraft Weight Estimator", layout="wide")

st.title("✈️ Aircraft Design Weight Analysis")
st.markdown("---")

# --- الثوابت من ملف الواجب ---
# بيانات الركاب والطاقم [cite: 2]
W_pl = 6970.0      # Payload weight 
W_crew = 615.0     # Crew weight [cite: 2]
W_tfo = 242.75     # Trapped Fuel & Oil [cite: 2]
R_c = 1265.847     # Range in statute miles [cite: 2]
LD_cruise = 13.0   # L/D Cruise [cite: 2]
Cp_cruise = 0.6    # Cp cruise [cite: 2]
np_cruise = 0.85   # Efficiency cruise [cite: 2]

# الثوابت الإحصائية [cite: 2]
coeff_a = 0.3774 
coeff_b = 0.9647

# --- الواجهة الجانبية ---
st.sidebar.header("⚙️ Inputs")
wto_guess = st.sidebar.number_input("WTO Guess (lbs)", value=48550.0)

# --- المحرك الحسابي ---
def perform_analysis(wto):
    # مراحل الوقود 
    f1, f2, f3, f4 = 0.990, 0.995, 0.995, 0.985 
    
    # مرحلة Cruise (W5/W4) - Equation 2.9 
    denominator = 375 * (np_cruise / Cp_cruise) * LD_cruise
    f5 = 1 / math.exp(R_c / denominator) 
    
    # مراحل Loiter, Descent, Landing 
    f6, f7, f8 = 0.970, 0.985, 0.995
    
    # Total Fuel Fraction (Mff) 
    mff = f1 * f2 * f3 * f4 * f5 * f6 * f7 * f8
    wf = wto * (1 - mff)
    
    # حساب الوزن الفارغ الفعلي (Tentative WE) 
    we_tent = wto - wf - W_pl - W_tfo - W_crew
    
    # حساب الوزن الفارغ المسموح إحصائياً (Allowable WE) 
    we_allow = 10**((math.log10(wto) - coeff_a) / coeff_b) 
    
    return mff, wf, we_tent, we_allow

# --- عرض النتائج ---
if st.button("🚀 Run Analysis"):
    mff, wf, we_calc, we_allow = perform_analysis(wto_guess)
    error = we_calc - we_allow

    st.subheader("📊 Results Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Fuel Fraction (Mff)", f"{mff:.3f}")
    col2.metric("Fuel Weight (WF)", f"{wf:,.1f} lbs")
    col3.metric("Weight Gap", f"{error:.2f} lbs", delta=error, delta_color="inverse")

    st.markdown("---")
    st.subheader("⚖️ Weight Matching Verification")
    c1, c2 = st.columns(2)
    c1.info(f"**Tentative WE:** {we_calc:,.2f} lbs")
    c2.success(f"**Allowable WE:** {we_allow:,.2f} lbs")

    # رسم الحساسية
    st.subheader("📈 Sensitivity Analysis")
    ranges = np.linspace(500, 2000, 20)
    we_trend = []
    for r in ranges:
        f_cruise_tmp = 1 / math.exp(r / (375 * (np_cruise / Cp_cruise) * LD_cruise))
        m_tmp = (0.99*0.995*0.995*0.985) * f_cruise_tmp * (0.970*0.985*0.995)
        we_trend.append(wto_guess - (wto_guess*(1-m_tmp)) - W_pl - W_tfo - W_crew)
    
    df_plot = pd.DataFrame({"Range (miles)": ranges, "Available WE (lbs)": we_trend})
    fig = px.line(df_plot, x="Range (miles)", y="Available WE (lbs)", title="Empty Weight Capacity vs Range")
    st.plotly_chart(fig, use_container_width=True)
