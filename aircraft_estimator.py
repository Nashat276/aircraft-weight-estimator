import streamlit as st
import math
import numpy as np
import pandas as pd
import plotly.express as px

# إعدادات الواجهة
st.set_page_config(page_title="Aircraft Design Pro", layout="wide")
st.title("✈️ Aircraft Design Weight Analysis")

# --- المدخلات من ملف الواجب ---
st.sidebar.header("⚙️ Mission Parameters")

# ثابت من Source 2 & 3
W_pl = 6970.0      # Payload 
W_crew = 615.0     # Crew weight [cite: 2]
W_tfo = 242.75     # Trapped Fuel & Oil [cite: 2]
R_c = 1265.847     # Range in statute miles [cite: 2]
LD_cruise = 13.0   # L/D Cruise [cite: 2]
Cp_cruise = 0.6    # Cp cruise [cite: 2]
np_cruise = 0.85   # Efficiency cruise [cite: 2]

# الثوابت الإحصائية [cite: 2]
coeff_A = 0.3774
coeff_B = 0.9647

wto_guess = st.sidebar.number_input("WTO Guess (lbs)", value=48550.0)

# --- محرك الحسابات الدقيق ---
def perform_analysis(wto):
    # مراحل الوقود بناءً على Step 3 
    f1 = 0.990  # Engine Start
    f2 = 0.995  # Taxi
    f3 = 0.995  # Take-off
    f4 = 0.985  # Climb
    
    # Cruise Phase (W5/W4) 
    # Equation: 1 / exp(Rc / (375 * (np/Cp) * (L/D)))
    denominator = 375 * (np_cruise / Cp_cruise) * LD_cruise
    f5 = 1 / math.exp(R_c / denominator) # النتيجة يجب أن تكون 0.833 
    
    f6 = 0.970  # Loiter 
    f7 = 0.985  # Descent 
    f8 = 0.995  # Landing 
    
    # Total Fuel Fraction (Mff)
    mff = f1 * f2 * f3 * f4 * f5 * f6 * f7 * f8 # النتيجة 0.764 
    
    wf = wto * (1 - mff) # Fuel weight
    
    # Step 5: Tentative Empty Weight 
    we_tent = wto - wf - W_pl - W_tfo - W_crew # النتيجة 29272.8 
    
    # Step 6: Allowable Empty Weight 
    # Equation: invLog[(log(Wto)-A)/B]
    we_allow = 10**((math.log10(wto) - coeff_a) / coeff_b) # النتيجة 29272.18 
    
    return mff, wf, we_tent, we_allow

# --- عرض النتائج ---
if st.button("🚀 Calculate"):
    mff, wf, we_calc, we_allow = perform_analysis(wto_guess)
    error = we_calc - we_allow

    st.subheader("📊 Calculation Results")
    col1, col2, col3 = st.columns(3)
    col1.metric("Mff (Fuel Fraction)", f"{mff:.3f}")
    col2.metric("Fuel Weight (WF)", f"{wf:,.1f} lbs")
    col3.metric("Payload (Wpl)", f"{W_pl:,.0f} lbs")

    st.markdown("---")
    st.subheader("⚖️ Weight Matching (Step 6)")
    c1, c2, c3 = st.columns(3)
    c1.write(f"**Tentative WE:** {we_calc:,.2f} lbs")
    c2.write(f"**Allowable WE:** {we_allow:,.2f} lbs")
    c3.metric("Difference", f"{error:.2f} lbs", delta=error, delta_color="inverse")

    if abs(error) < 1.0:
        st.success("✅ التقارب ممتاز! الوزن الإجمالي صحيح تماماً.")
    else:
        st.warning("⚠️ الفرق كبير، يرجى تعديل قيمة WTO Guess للوصول للتقارب.")

    # الرسم البياني للحساسية (Range Sensitivity)
    st.subheader("📈 Range Sensitivity")
    ranges = np.linspace(500, 2000, 30)
    # ملاحظة: في الرسم نثبت الـ WTO ونغير المدى لنرى تأثيره على الوزن الفارغ المتاح
    we_trend = []
    for r in ranges:
        f_c = 1 / math.exp(r / (375 * (np_cruise / Cp_cruise) * LD_cruise))
        m_tmp = (0.99*0.995*0.995*0.985) * f_c * (0.970*0.985*0.995)
        we_trend.append(wto_guess - (wto_guess*(1-m_tmp)) - W_pl - W_tfo - W_crew)
    
    df_plot = pd.DataFrame({"Range": ranges, "WE Tentative": we_trend})
    fig = px.line(df_plot, x="Range", y="WE Tentative", title="How Range affects Empty Weight Margin")
    st.plotly_chart(fig, use_container_width=True)
