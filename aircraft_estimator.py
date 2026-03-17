import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import math
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="AeroNova Estimator", layout="wide")

# --- 2. المحرك الحسابي مع معالجة استثنائية ---
def calculate_weights(p):
    try:
        # Payload + Crew
        w_payload = (p['n_pax'] * 205) + (p['n_crew'] * 200) # تبسيط للحسابات
        w_tfo = p['wto_guess'] * 0.005
        
        # Breguet Range Logic
        range_m = p['range_nm'] * 1.15078
        # حماية من القسمة على صفر
        eff = (375 * (p['eta'] / p['sfc']) * p['ld'])
        if eff <= 0: return None
        
        mff = 0.97 * math.exp(-range_m / eff) * 0.99
        w_fuel = p['wto_guess'] * (1 - mff) * 1.05 # شامل الاحتياطي
        
        we_required = p['wto_guess'] - w_fuel - w_payload - w_tfo
        
        # حماية اللوغاريتم
        if p['wto_guess'] <= 100: return None
        we_allowable = 10**((math.log10(p['wto_guess']) - 0.3774) / 0.9647)
        
        return {
            "wto": p['wto_guess'],
            "we_req": we_required,
            "we_allow": we_allowable,
            "diff": we_allowable - we_required,
            "fuel": w_fuel,
            "payload": w_payload
        }
    except:
        return None

# --- 3. الواجهة الرسومية ---
st.title("✈️ AeroNova Estimator X")

with st.sidebar:
    st.header("Input Parameters")
    pax = st.slider("Passengers", 10, 100, 34)
    dist = st.slider("Range (nm)", 500, 3000, 1200)
    sfc = st.number_input("SFC (lb/hp/hr)", value=0.6)
    ld = st.slider("L/D Ratio", 10, 18, 13)

# خوارزمية البحث عن الوزن الصحيح
params = {'n_pax': pax, 'n_crew': 3, 'range_nm': dist, 'sfc': sfc, 'eta': 0.85, 'ld': ld}
best_wto = 0
final_res = None

# Bisection Method
low, high = 10000, 500000
for _ in range(50):
    mid = (low + high) / 2
    params['wto_guess'] = mid
    res = calculate_weights(params)
    if res is None: break
    if abs(res['diff']) < 1.0:
        best_wto = mid
        final_res = res
        break
    if res['diff'] > 0: high = mid
    else: low = mid

# --- 4. عرض النتائج بحذر ---
if final_res:
    col1, col2, col3 = st.columns(3)
    col1.metric("Gross Weight", f"{final_res['wto']:,.0f} lb")
    col2.metric("Empty Weight", f"{final_res['we_req']:,.0f} lb")
    col3.metric("Fuel Required", f"{final_res['fuel']:,.0f} lb")

    # رسم بياني بسيط للتأكد من عدم وجود خطأ في Plotly
    fig = go.Figure(go.Pie(labels=['Empty', 'Fuel', 'Payload'], 
                         values=[final_res['we_req'], final_res['fuel'], final_res['payload']],
                         hole=.4))
    fig.update_layout(template="plotly_dark", title="Weight Distribution")
    st.plotly_chart(fig)

    # دالة الـ PDF: تم تبسيطها لأقصى حد لتجنب الـ ValueError
    def make_pdf(data):
        buf = io.BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=letter)
        styles = getSampleStyleSheet()
        # نستخدم بيانات نصية فقط لتجنب مشاكل الـ Formatting
        tbl_data = [
            ["Category", "Value (lb)"],
            ["Takeoff Weight", f"{data['wto']:,.1f}"],
            ["Empty Weight", f"{data['we_req']:,.1f}"],
            ["Fuel Weight", f"{data['fuel']:,.1f}"],
            ["Payload", f"{data['payload']:,.1f}"]
        ]
        t = Table(tbl_data)
        t.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 1, colors.black)]))
        doc.build([Paragraph("AeroNova Estimation Report", styles['Title']), t])
        return buf.getvalue()

    if st.button("Generate Report"):
        pdf = make_pdf(final_res)
        st.download_button("Download PDF", pdf, "Report.pdf", "application/pdf")
else:
    st.warning("⚠️ لا يمكن الوصول لوزن متقارب بهذه المدخلات. جرب تقليل المسافة أو زيادة L/D.")
