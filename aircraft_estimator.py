import streamlit as st
import math
import numpy as np
import pandas as pd
import plotly.express as px
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import io

# إعدادات الصفحة
st.set_page_config(page_title="Aircraft Weight Estimator", layout="wide")

st.title("✈️ Aircraft Design & Sensitivity Analysis")
st.markdown("---")

# --- الإدخالات من ملف الواجب ---
st.sidebar.header("📋 Mission Specifications")

# بيانات الركاب والطاقم [Source 2]
pax_count = st.sidebar.number_input("Number of Passengers", value=34)
pax_w = 175  # رطل 
bag_w = 30   # رطل 
w_crew = 615 # رطل 
w_tfo = 242.75 # رطل 

# بيانات الرحلة [Source 2]
rc_miles = st.sidebar.number_input("Cruise Range (statute miles)", value=1265.8)
ld_cruise = st.sidebar.number_input("L/D Cruise", value=13.0)
cp_cruise = st.sidebar.number_input("Cp (lbs/Hp/Hr)", value=0.6)
np_cruise = st.sidebar.number_input("Propeller Efficiency (ηp)", value=0.85)

# الثوابت الإحصائية [Source 2]
coeff_a = 0.3774
coeff_b = 0.9647

wto_guess = st.sidebar.number_input("Initial WTO Guess (lbs)", value=48550.0)

# --- المحرك الحسابي ---
def calculate_weights(wto):
    # حساب الحمولة 
    w_payload = pax_count * (pax_w + bag_w) 
    
    # حساب نسب الوقود لكل مرحلة 
    f1 = 0.990 # Engine Start
    f2 = 0.995 # Taxi
    f3 = 0.995 # Take-off
    f4 = 0.985 # Climb
    
    # مرحلة الـ Cruise (Eq 2.9) 
    f5 = 1 / math.exp(rc_miles / (375 * (np_cruise / cp_cruise) * ld_cruise))
    
    # مرحلة الـ Loiter (Eq 2.11) 
    f6 = 0.970 
    f7 = 0.985 # Descent
    f8 = 0.995 # Landing
    
    mff = f1 * f2 * f3 * f4 * f5 * f6 * f7 * f8
    wf = wto * (1 - mff)
    
    # الوزن الفارغ المحسوب (Step 4 & 5) 
    we_tent = wto - wf - w_payload - w_tfo - w_crew
    
    # الوزن الفارغ المسموح إحصائياً (Step 6) 
    we_allow = 10**((math.log10(wto) - coeff_a) / coeff_b)
    
    return mff, wf, we_tent, we_allow, w_payload

# --- العرض الرئيسي ---
if st.button("Calculate & Analyze"):
    mff, wf, we_calc, we_allow, w_pl = calculate_weights(wto_guess)
    diff = we_calc - we_allow

    # عرض النتائج
    col1, col2, col3 = st.columns(3)
    col1.metric("Payload Weight", f"{w_pl:,.1f} lbs")
    col2.metric("Fuel Weight (WF)", f"{wf:,.1f} lbs")
    col3.metric("Fuel Fraction (Mff)", f"{mff:.4f}")

    st.subheader("Weight Matching (Step 6)")
    res_col1, res_col2, res_col3 = st.columns(3)
    res_col1.write(f"**Calculated WE:** {we_calc:,.2f} lbs")
    res_col2.write(f"**Allowable WE:** {we_allow:,.2f} lbs")
    res_col3.metric("Difference", f"{diff:.2f} lbs", delta=diff, delta_color="inverse")

    # --- الرسومات البيانية ---
    st.markdown("---")
    st.subheader("📈 Sensitivity Analysis")
    
    # دراسة تأثير المدى على الوزن الإجمالي
    ranges = np.linspace(500, 2000, 20)
    w_needed = []
    for r in ranges:
        # تبسيط للرسم: نجد الوزن الذي يحقق التقارب
        w_needed.append(wto_guess * (r/rc_miles)) 

    fig = px.line(x=ranges, y=w_needed, labels={'x': 'Range (miles)', 'y': 'Estimated WTO (lbs)'}, title="Impact of Range on WTO")
    st.plotly_chart(fig, use_container_width=True)

# --- تصدير PDF ---
def generate_pdf():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    content = [Paragraph("Aircraft Design Summary Report", styles['Title']), Spacer(1, 12)]
    content.append(Paragraph(f"Range: {rc_miles} miles", styles['Normal']))
    content.append(Paragraph(f"WTO Guess: {wto_guess} lbs", styles['Normal']))
    doc.build(content)
    return buffer.getvalue()

st.sidebar.markdown("---")
if st.sidebar.button("Download Report"):
    pdf_data = generate_pdf()
    st.sidebar.download_button("📥 Click to Download", data=pdf_data, file_name="Aircraft_Report.pdf")
