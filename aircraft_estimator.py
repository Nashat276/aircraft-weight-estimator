import streamlit as st
import math
import numpy as np
import pandas as pd
import plotly.express as px

# إعدادات الصفحة
st.set_page_config(page_title="Aircraft Design Pro", layout="wide")

st.title("✈️ Aircraft Design Cockpit")
st.markdown("### Engineering Analysis (Based on Homework 2.8)")

# --- Sidebar Inputs ---
st.sidebar.header("⚙️ Mission Specifications")

# بيانات الركاب بناءً على المصدر [Source 2]
passengers = st.sidebar.number_input("Passengers", value=34)
w_crew = 615 # lbs 
w_tfo = 242.75 # lbs 
w_payload = passengers * (175 + 30) # 175 lbs weight + 30 lbs baggage 

# بيانات الرحلة [Source 2]
rc_miles = st.sidebar.number_input("Range (statute miles)", value=1265.8)
ld_cruise = st.sidebar.number_input("L/D (Cruise)", value=13.0)
cp_cruise = st.sidebar.number_input("Cp (lbs/Hp/Hr)", value=0.6)
np_eff = st.sidebar.number_input("ηp (Propeller Efficiency)", value=0.85)

# الثوابت الإحصائية A و B [Source 2]
coeff_a = 0.3774
coeff_b = 0.9647

wto_guess = st.sidebar.number_input("WTO Guess (lbs)", value=48550.0)

# --- Calculation Engine ---
def run_analysis(wto):
    # Fuel Fractions (Step 3) [Source 3]
    f1, f2, f3, f4 = 0.990, 0.995, 0.995, 0.985 
    
    # Cruise Equation 2.9 [Source 3]
    f_cruise = 1 / math.exp(rc_miles / (375 * (np_eff / cp_cruise) * ld_cruise))
    
    # Loiter & Landing [Source 3]
    f6, f7, f8 = 0.970, 0.985, 0.995
    
    mff = f1 * f2 * f3 * f4 * f_cruise * f6 * f7 * f8
    wf = wto * (1 - mff)
    
    # WE Tentative (Step 5) [Source 3]
    we_calc = wto - wf - w_payload - w_tfo - w_crew
    
    # WE Allowable (Step 6) [Source 3]
    we_allow = 10**((math.log10(wto) - coeff_a) / coeff_b)
    
    return mff, wf, we_calc, we_allow

# --- Results Interface ---
if st.button("🚀 Run Analysis"):
    mff, wf, we_calc, we_allow = run_analysis(wto_guess)
    diff = we_calc - we_allow

    st.subheader("📊 Weight Summary")
    c1, c2, c3 = st.columns(3)
    c1.metric("Fuel Fraction (Mff)", f"{mff:.4f}")
    c2.metric("Fuel Weight (WF)", f"{wf:,.1f} lbs")
    c3.metric("Payload Weight", f"{w_payload:,.1f} lbs")

    st.subheader("⚖️ Weight Matching")
    res1, res2, res3 = st.columns(3)
    res1.write(f"**Calculated WE:** {we_calc:,.1f} lbs")
    res2.write(f"**Allowable WE:** {we_allow:,.1f} lbs")
    res3.metric("Difference", f"{diff:.2f} lbs", delta=diff, delta_color="inverse")

    # --- Sensitivity Analysis Chart ---
    st.divider()
    st.subheader("📈 Range Sensitivity Analysis")
    
    ranges = np.linspace(500, 2500, 50)
    # حساب الوزن الفارغ المطلوب لتغطية المدى المختلف
    we_trend = []
    for r in ranges:
        f_c = 1 / math.exp(r / (375 * (np_eff / cp_cruise) * ld_cruise))
        mff_t = (0.99*0.995*0.995*0.985) * f_c * (0.97*0.985*0.995)
        we_trend.append(wto_guess - (wto_guess * (1 - mff_t)) - w_payload - w_tfo - w_crew)

    df = pd.DataFrame({"Range (miles)": ranges, "Tentative WE (lbs)": we_trend})
    fig = px.line(df, x="Range (miles)", y="Tentative WE (lbs)", title="Empty Weight Trend vs Range")
    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("👈 اضغط Run Analysis بعد التأكد من المدخلات")
