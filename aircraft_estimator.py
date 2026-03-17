import streamlit as st
import math
import numpy as np
import pandas as pd
import plotly.express as px

# 1. إعداد الواجهة بتصميم Neon (تصحيح الخطأ السابق)
st.set_page_config(page_title="AeroDesign Pro", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #00ffcc; }
    .stMetric { border: 1px solid #00ffcc; padding: 10px; border-radius: 10px; box-shadow: 0 0 5px #00ffcc; }
    h1, h2, h3 { color: #00ffcc; text-shadow: 0 0 10px #00ffcc; }
    </style>
    """, unsafe_allow_html=True) # تم تصحيح المعامل هنا من stdio إلى html

st.title("⚡ AeroDesign Professional: Weight & Sensitivity")

# 2. المدخلات بناءً على أرقام الملف (Homework 1)
st.sidebar.header("🛠️ Mission Specifications")

with st.sidebar.expander("Weights & Payload", expanded=True):
    pax_count = st.number_input("Number of Passengers", value=34)
    w_pl = pax_count * (175 + 30) # 34 * 205 = 6970 lbs
    w_crew = 615.0
    w_tfo = 242.75

with st.sidebar.expander("Cruise & Performance", expanded=True):
    rc_miles = st.number_input("Cruise Range (miles)", value=1265.8)
    ld_cruise = st.number_input("L/D Cruise", value=13.0)
    cp_cruise = st.number_input("Cp (lbs/Hp/Hr)", value=0.6)
    np_eff = st.number_input("Propeller Efficiency (ηp)", value=0.85)

# الثوابت الإحصائية من الجدول 2.15 في ملفك
coeff_a = 0.3774
coeff_b = 0.9647

wto_guess = st.sidebar.number_input("Initial WTO Guess (lbs)", value=48550.0)

# 3. محرك الحسابات التفصيلي
def run_full_analysis(wto):
    # مراحل الوقود (Step 3)
    f_fixed = 0.990 * 0.995 * 0.995 * 0.985 # Start to Climb
    f_cruise = 1 / math.exp(rc_miles / (375 * (np_eff / cp_cruise) * ld_cruise))
    f_end = 0.970 * 0.985 * 0.995 # Loiter to Landing
    
    mff = f_fixed * f_cruise * f_end
    wf = wto * (1 - mff)
    
    # التقارب (Weight Matching)
    we_tentative = wto - wf - w_pl - w_tfo - w_crew
    we_allowable = 10**((math.log10(wto) - coeff_a) / coeff_b)
    
    return mff, wf, we_tentative, we_allowable

# 4. واجهة النتائج والرسومات
if st.button("🚀 RUN ENGINEERING ANALYSIS"):
    mff, wf, we_calc, we_allow = run_full_analysis(wto_guess)
    diff = we_calc - we_allow

    # النتائج الأساسية
    st.subheader("📊 Weight Performance Summary")
    c1, c2, c3 = st.columns(3)
    c1.metric("Fuel Fraction (Mff)", f"{mff:.4f}")
    c2.metric("Total Fuel Weight", f"{wf:,.1f} lbs")
    c3.metric("Weight Gap", f"{diff:.2f} lbs", delta=diff, delta_color="inverse")

    # جزء الحساسية (بناءً على الصفحة 2 من ملفك)
    st.divider()
    st.subheader("📉 Design Sensitivity Derivatives")
    col_s1, col_s2 = st.columns(2)
    
    # مشتقات بريجيت (Breguet Derivatives) من جدول ملفك
    # dR/dCp = -R/Cp
    dr_dcp = -rc_miles / cp_cruise
    # dR/d(eta) = R/eta
    dr_deta = rc_miles / np_eff
    
    col_s1.info(f"**∂R / ∂Cp:** {dr_dcp:.2f} (ميل لكل وحدة استهلاك)")
    col_s2.info(f"**∂R / ∂ηp:** {dr_deta:.2f} (ميل لكل وحدة كفاءة)")

    # الرسم البياني للتقارب
    st.subheader("🔍 Weight Convergence Map")
    wto_range = np.linspace(40000, 60000, 20)
    we_calcs = [run_full_analysis(w)[2] for w in wto_range]
    we_allows = [run_full_analysis(w)[3] for w in wto_range]
    
    df_plot = pd.DataFrame({
        "WTO": wto_range,
        "Tentative WE": we_calcs,
        "Allowable WE": we_allows
    })
    
    fig = px.line(df_plot, x="WTO", y=["Tentative WE", "Allowable WE"], 
                  title="Finding the Equilibrium Point (Where lines cross)")
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color="#00ffcc")
    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("قم بتعديل المعطيات من اليسار ثم اضغط على Execute")
