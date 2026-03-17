import streamlit as st
import math
import numpy as np
import pandas as pd
import plotly.express as px

# إعدادات الواجهة
st.set_page_config(page_title="Aircraft Design Pro", layout="wide")
st.title("✈️ Aircraft Design Weight Analysis")

# --- المدخلات الثابتة من ملف الواجب ---
# تم حسابها بناءً على Source 2 في الملف
W_pl = 6970.0      # Payload weight 
W_crew = 615.0     # Crew weight 
W_tfo = 242.75     # Trapped Fuel & Oil 
R_c = 1265.847     # Range in statute miles 
LD_cruise = 13.0   # L/D Cruise 
Cp_cruise = 0.6    # Cp cruise 
np_cruise = 0.85   # Efficiency cruise 

# الثوابت الإحصائية [Source 2]
coeff_a = 0.3774 [cite: 2]
coeff_b = 0.9647 [cite: 2]

st.sidebar.header("⚙️ User Input")
wto_guess = st.sidebar.number_input("WTO Guess (lbs)", value=48550.0)

# --- محرك الحسابات ---
def perform_analysis(wto):
    # مراحل الوقود بناءً على Step 3 في الملف 
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
    
    # حساب الوزن الفارغ المسموح إحصائياً (Allowable WE) - Step 6 
    # تم تصحيح أسماء المتغيرات هنا لحل الـ NameError
    we_allow = 10**((math.log10(wto) - coeff_a) / coeff_b) 
    
    return mff, wf, we_tent, we_allow

# --- التنفيذ وعرض النتائج ---
if st.button("🚀 Run Analysis"):
    mff, wf, we_calc, we_allow = perform_analysis(wto_guess)
    error = we_calc - we_allow

    st.subheader("📊 Calculation Results")
    col1, col2, col3 = st.columns(3)
    col1.metric("Fuel Fraction (Mff)", f"{mff:.3f}")
    col2.metric("Fuel Weight (WF)", f"{wf:,.1f} lbs")
    col3.metric("Difference (Error)", f"{error:.2f} lbs", delta=error, delta_color="inverse")

    st.markdown("---")
    st.subheader("⚖️ Weight Matching Verification")
    c1, c2 = st.columns(2)
    c1.write(f"**Tentative WE (Step 5):** {we_calc:,.2f} lbs")
    c2.write(f"**Allowable WE (Step 6):** {we_allow:,.2f} lbs")

    if abs(error) < 1.0:
        st.success("✅ الوزن متطابق! قيمة WTO صحيحة.")
    else:
        st.warning("⚠️ يرجى تعديل WTO Guess لتقليل الفرق.")

    # رسم الحساسية
    st.subheader("📈 Range Sensitivity Plot")
    ranges = np.linspace(500, 2000, 20)
    we_trend = []
    for r in ranges:
        f_c = 1 / math.exp(r / (375 * (np_cruise / Cp_cruise) * LD_cruise))
        m_tmp = (0.99*0.995*0.995*0.985) * f_c * (0.970*0.985*0.995)
        we_trend.append(wto_guess - (wto_guess*(1-m_tmp)) - W_pl - W_tfo - W_crew)
    
    df_plot = pd.DataFrame({"Range": ranges, "WE Available": we_trend})
    fig = px.line(df_plot, x="Range", y="WE Available", title="How Range impacts available Empty Weight")
    st.plotly_chart(fig, use_container_width=True)
