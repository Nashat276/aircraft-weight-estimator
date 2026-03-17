import streamlit as st
import math
import numpy as np
import pandas as pd
import plotly.express as px

# 1. تصميم الواجهة (Neon Style)
st.set_page_config(page_title="AeroDesign Pro", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #00ffcc; }
    .stButton>button { background-color: #00ffcc; color: black; border-radius: 10px; border: 2px solid #00ffcc; box-shadow: 0 0 10px #00ffcc; }
    .stNumberInput { border: 1px solid #00ffcc; }
    h1, h2, h3 { color: #00ffcc; text-shadow: 0 0 10px #00ffcc; }
    </style>
    """, unsafe_allow_stdio=True)

st.title("⚡ AeroDesign Professional: Weight & Sensitivity")

# 2. تقسيم المدخلات (Sidebar)
st.sidebar.header("🛠️ Design Parameters")

with st.sidebar.expander("Passenger & Crew Data"):
    pax = st.number_input("Passengers", value=34)
    w_pax_total = pax * (175 + 30) # من ملفك: وزن + حقائب
    w_crew = st.number_input("Crew Weight", value=615.0)
    w_tfo = st.number_input("Trapped Fuel (Wtfo)", value=242.75)

with st.sidebar.expander("Cruise Performance"):
    rc = st.number_input("Range (statute miles)", value=1265.8)
    ld = st.number_input("L/D Cruise", value=13.0)
    cp = st.number_input("Cp (Specific Fuel Cons.)", value=0.6)
    eta = st.number_input("Propeller Efficiency (ηp)", value=0.85)

with st.sidebar.expander("Statistical Constants (A & B)"):
    # يمكنك التغيير هنا بناءً على نوع الطائرة أو المادة
    coeff_a = st.number_input("Constant A", value=0.3774, format="%.4f")
    coeff_b = st.number_input("Constant B", value=0.9647, format="%.4f")

wto_guess = st.sidebar.number_input("Initial WTO Guess (lbs)", value=48550.0)

# 3. محرك الحسابات (Detailed Calculation)
def analyze(wto):
    # كسر الوقود لكل مرحلة بناءً على ملفك
    phases = {
        "Start/Taxi/Takeoff": 0.990 * 0.995 * 0.995,
        "Climb": 0.985,
        "Cruise": 1 / math.exp(rc / (375 * (eta / cp) * ld)),
        "Loiter": 0.970,
        "Descent/Landing": 0.985 * 0.995
    }
    
    mff = np.prod(list(phases.values()))
    wf = wto * (1 - mff)
    we_calc = wto - wf - w_pax_total - w_tfo - w_crew
    we_allow = 10**((math.log10(wto) - coeff_a) / coeff_b)
    
    return mff, wf, we_calc, we_allow, phases

# 4. التنفيذ والعرض
if st.button("🚀 EXECUTE ENGINEERING ANALYSIS"):
    mff, wf, we_calc, we_allow, phases = analyze(wto_guess)
    
    # عرض العدادات (Metrics)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Fuel Fraction (Mff)", f"{mff:.4f}")
    c2.metric("Fuel Weight", f"{wf:,.1f} lb")
    c3.metric("Payload", f"{w_pax_total:,.0f} lb")
    c4.metric("Matching Error", f"{we_calc - we_allow:.2f} lb")

    # جدول المراحل (جديد)
    st.subheader("📋 Mission Profile Breakdown")
    st.table(pd.DataFrame(phases.items(), columns=["Phase", "Weight Fraction (f)"]))

    # 5. تحليل الحساسية (Sensitivity) - بناءً على معادلات ملفك
    st.divider()
    st.subheader("📉 Design Sensitivities (Breguet Derivatives)")
    
    # معادلة dR/dCp من الصفحة 2 في ملفك
    sens_range_cp = -rc / cp
    sens_range_eta = rc / eta
    
    s1, s2 = st.columns(2)
    s1.info(f"**Range Sensitivity to Cp:** {sens_range_cp:.2f} miles per unit Cp")
    s2.info(f"**Range Sensitivity to Efficiency:** {sens_range_eta:.2f} miles per unit ηp")

    # رسم بياني تفاعلي
    st.subheader("🔍 Parametric Sweep: Range vs. WTO Required")
    range_list = np.linspace(500, 2000, 20)
    # حساب تقريبي للوزن المطلوب لكل مدى
    wto_needed = [wto_guess * (math.exp(r/(375*(eta/cp)*ld)) / math.exp(rc/(375*(eta/cp)*ld))) for r in range_list]
    
    fig = px.area(x=range_list, y=wto_needed, 
                  labels={'x': 'Range (miles)', 'y': 'Required WTO (lbs)'},
                  title="Mission Capability Map")
    fig.update_traces(line_color='#00ffcc')
    st.plotly_chart(fig, use_container_width=True)

else:
    st.write("👈 Configure the mission profile in the sidebar and press Execute.")
