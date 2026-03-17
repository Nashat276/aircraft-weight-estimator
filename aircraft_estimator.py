import streamlit as st
import math
import numpy as np
import pandas as pd
import plotly.express as px

# ------------------ 1. التصميم الإبداعي (Custom Neon CSS) ------------------
st.set_page_config(page_title="AeroDesign Pro", layout="wide")

# كود CSS مخصص لجعل الواجهة داكنة مع حدود مضيئة (Neon Cyan)
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #00ffcc; font-family: 'Courier New', Courier, monospace; }
    .stNumberInput, .stButton>button { border: 2px solid #00ffcc; border-radius: 10px; box-shadow: 0 0 10px #00ffcc; }
    .stButton>button:hover { background-color: #00ffcc; color: black; font-weight: bold; }
    h1, h2, h3 { color: #00ffcc; text-shadow: 0 0 15px #00ffcc; }
    /* تنسيق خاص للعدادات (Metrics) لتظهر كصناديق مضيئة */
    [data-testid="stMetricValue"] { color: #00ffcc; }
    [data-testid="stMetricDelta"] { color: #ff0055; }
    .css-1r6slb0 { border: 1px solid #00ffcc; padding: 15px; border-radius: 15px; background-color: rgba(0, 255, 204, 0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ AeroDesign Pro: Integrated Weight & Sensitivity Analysis")
st.markdown("---")

# ------------------ 2. المدخلات الهندسية (Sidebar Modules) ------------------
st.sidebar.header("🕹️ Mission Control Dashboard")

# وحدة الحمولة والطاقم بناءً على أرقام الملف (Source 2)
with st.sidebar.expander("👤 Payload & Crew", expanded=True):
    pax = st.number_input("Passengers", value=34)
    w_pl = pax * (175 + 30) # 34 * 205 = 6970 lbs (من ملفك)
    w_crew = st.number_input("Crew Weight", value=615.0)
    w_tfo = st.number_input("Trapped Fuel (Wtfo)", value=242.75)

# وحدة الأداء بناءً على أرقام الملف (Source 2)
with st.sidebar.expander("🚀 Cruise Performance", expanded=True):
    rc = st.number_input("Range (statute miles)", value=1265.8)
    ld = st.number_input("L/D Cruise", value=13.0)
    cp = st.number_input("Cp (Specific Fuel Cons.)", value=0.6)
    eta = st.number_input("ηp (Propeller Efficiency)", value=0.85)

# الثوابت الإحصائية (قابلية التغيير لسيناريوهات أخرى)
coeff_a = 0.3774 # Aluminum / Transport [cite: 2]
coeff_b = 0.9647 # Aluminum / Transport [cite: 2]

wto_guess = st.sidebar.number_input("Initial WTO Guess (lbs)", value=48550.0)

# ------------------ 3. المحرك الحسابي المتكامل ------------------
def perform_analysis(wto):
    # حساب كسر الوقود بناءً على المراحل الثمانية في "Step 3" في ملفك
    # تم جمع المراحل الثابتة وتبسيطها
    f_fixed = 0.990 * 0.995 * 0.995 * 0.985 # Start, Taxi, Takeoff, Climb
    
    # Cruise Phase (Eq 2.9)
    denominator = 375 * (eta / cp) * ld
    f_cruise = 1 / math.exp(rc / denominator) # النتيجة المتوقعة 0.833
    
    f_end = 0.970 * 0.985 * 0.995 # Loiter, Descent, Landing
    
    # Total Fuel Fraction (Mff)
    mff = f_fixed * f_cruise * f_end
    wf = wto * (1 - mff)
    
    # تقارب الوزن الفارغ (Weight Matching) - Step 6
    we_tent = wto - wf - w_pl - w_tfo - w_crew
    we_allow = 10**((math.log10(wto) - coeff_a) / coeff_b) # النتيجة المتوقعة 29272.18
    
    # حساب الحساسية بناءً على الصفحة 2 من ملفك (Sensitivity Derivatives)
    # ∂R / ∂Cp = -R / Cp
    sens_range_cp = -rc / cp
    # ∂R / ∂(L/D) = R / (L/D)
    sens_range_ld = rc / ld
    
    return mff, wf, we_tent, we_allow, sens_range_cp, sens_range_ld

# ------------------ 4. واجهة العرض (Engineering Dashboard) ------------------
if st.button("🚀 EXECUTE DESIGN ANALYSIS"):
    mff, wf, we_calc, we_allow, s_cp, s_ld = perform_analysis(wto_guess)
    error = we_calc - we_allow

    st.subheader("📊 Weight Performance Metrics")
    c1, c2, c3, c4 = st.columns(4)
    # استخدام العدادات (Metrics) لإظهار الفرق (Delta)
    c1.metric("Fuel Fraction (Mff)", f"{mff:.4f}")
    c2.metric("Fuel Weight (WF)", f"{wf:,.1f} lbs")
    c3.metric("Payload (Wpl)", f"{w_pl:,.0f} lbs")
    c4.metric("Matching Error", f"{error:.2f} lbs", delta=error, delta_color="inverse")

    # verify convergence (Step 6 Verification)
    if abs(error) < 1.0:
        st.success("✅ Weight Convergence Achieved! Design points match.")
    else:
        st.warning("⚠️ Error exceeds threshold. Please adjust WTO Guess to find equilibrium.")

    # ------------------ 5. تحليل الحساسية (Sensitivity - Part II) ------------------
    st.divider()
    st.subheader("📉 Design Sensitivities (Partials)")
    s1, s2 = st.columns(2)
    s1.info(f"**∂R / ∂Cp:** {s_cp:.2f} miles per unit Cp (مدى/استهلاك)")
    s2.info(f"**∂R / ∂(L/D):** {s_ld:.2f} miles per unit L/D (مدى/كفاءة)")

    # ------------------ 6. الرسومات التفاعلية (Interactive Plots) ------------------
    st.subheader("🔍 Parametric Sweep: Range vs WTO Capacity")
    
    # إنشاء مصفوفة من المدى المختلف لحساب الوزن الفارغ المتاح
    ranges = np.linspace(500, 2000, 30)
    we_available = []
    for r in ranges:
        f_c = 1 / math.exp(r / (375 * (eta / cp) * ld))
        m_tmp = (0.990*0.995*0.995*0.985) * f_c * (0.970*0.985*0.995)
        we_available.append(wto_guess - (wto_guess*(1-m_tmp)) - w_pl - w_tfo - w_crew)
    
    df_plot = pd.DataFrame({"Range (miles)": ranges, "Available WE (lbs)": we_available})
    
    # رسم بياني احترافي (Area Chart) باستخدام Plotly
    fig = px.area(df_plot, x="Range (miles)", y="Available WE (lbs)", title="How Range impacts Available Empty Weight")
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color="#00ffcc")
    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("👈 اضبط المعطيات في اللوحة الجانبية ثم اضغط 'Execute' لبدء التحليل الهندسي.")
