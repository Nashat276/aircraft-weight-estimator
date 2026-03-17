import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import math, io
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                 Table, TableStyle, HRFlowable)
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER

# --- 1. إعدادات الصفحة والتصميم ---
st.set_page_config(page_title="AeroSizer Pro", page_icon="✈", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;500&family=Inter:wght@400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
        background-color: #FDFDFD !important;
    }

    /* العنوان الرئيسي - بسيط واحترافي */
    .app-header {
        font-family: 'Roboto Mono', monospace;
        font-size: 2.8rem;
        font-weight: 700;
        color: #1E293B;
        text-align: center;
        margin-bottom: 2rem;
        padding-top: 1rem;
    }

    /* بطاقات النتائج */
    .card-box {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-bottom: 1.2rem;
    }
    .card-label {
        font-size: 0.8rem;
        color: #64748B;
        text-transform: uppercase;
        font-weight: 600;
        margin-bottom: 0.4rem;
    }
    .card-value {
        font-family: 'Roboto Mono', monospace;
        font-size: 1.8rem;
        color: #0F172A;
        font-weight: 600;
    }
    .card-unit { font-size: 0.9rem; color: #94A3B8; margin-left: 0.2rem; }
</style>
""", unsafe_allow_html=True)

# --- 2. محرك الحسابات (Breguet Equations) ---
def run_sizing(p):
    # حسابات الحمولة والطاقم
    W_pl = p['npax'] * (p['wpax'] + p['wbag']) + p['ncrew'] * 205 + p['natt'] * 200
    W_crew = p['ncrew'] * 205 + p['natt'] * 200
    
    # معامل الوزن للمرحلة الرابعة (Cruise) باستخدام معادلة Breguet للطائرات المروحية
    R_statute = p['R'] * 1.15078
    Wc = 1.0 / math.exp(R_statute / (375.0 * (p['npc'] / p['Cpc']) * p['LDc']))
    
    # معامل الوزن للمرحلة الخامسة (Loiter)
    V_mph = p['Vl'] * 1.15078
    Wl = 1.0 / math.exp(p['El'] / (375.0 * (1.0 / V_mph) * (p['npl'] / p['Cpl']) * p['LDl']))
    
    # إجمالي معاملات الوزن (Mff) بناءً على Raymer
    Mff = 0.990 * 0.995 * 0.995 * 0.985 * Wc * Wl * 0.985 * 0.995
    
    # استخدام الوزن الذي أدخله المستخدم
    Wto = p['Wto_user']
    Wtfo = Wto * p['Mtfo']
    W_fuel_usable = Wto * (1.0 - Mff)
    W_fuel_total = W_fuel_usable * (1.0 + p['Mr']) + Wtfo
    
    W_oe = Wto - W_fuel_total - W_pl
    W_empty = W_oe - Wtfo - W_crew
    
    # حساب الوزن الفارغ المسموح به إحصائياً للمقارنة (Raymer Table 2.2)
    WE_allow = 10.0**((math.log10(max(1.0, Wto)) - p['A']) / p['B'])
    
    return {
        'Wto': Wto, 'W_pl': W_pl, 'W_fuel': W_fuel_total, 'W_empty': W_empty,
        'W_oe': W_oe, 'Mff': Mff, 'WE_allow': WE_allow
    }

# --- 3. القائمة الجانبية (Inputs) ---
with st.sidebar:
    st.header("⚙️ معطيات التصميم")
    wto_manual = st.number_input("الوزن الإجمالي للتصميم (W_TO) lbs", 5000, 800000, 48550)
    
    st.subheader("متطلبات المهمة")
    r_nm = st.number_input("المدى Design Range (nm)", 100, 6000, 1100)
    pax = st.number_input("عدد الركاب", 0, 500, 34)
    
    st.subheader("معايير الأداء")
    ld_c = st.slider("نسبة الرفع للسحب L/D", 4.0, 25.0, 13.0)
    cp_c = st.number_input("استهلاك الوقود SFC (lb/hp/hr)", 0.3, 1.1, 0.6)
    eta_c = st.slider("كفاءة المروحة Prop Efficiency", 0.4, 0.95, 0.85)

# --- 4. تشغيل الحسابات وعرض النتائج ---
params = {
    'Wto_user': float(wto_manual), 'npax': pax, 'wpax': 175.0, 'wbag': 30.0,
    'ncrew': 2, 'natt': 1, 'R': float(r_nm), 'LDc': ld_c, 'Cpc': cp_c, 'npc': eta_c,
    'El': 0.75, 'Vl': 250.0, 'LDl': 16.0, 'Cpl': 0.65, 'npl': 0.77,
    'A': 0.3774, 'B': 0.9647, 'Mtfo': 0.005, 'Mr': 0.05
}
res = run_sizing(params)

# عرض اسم الأداة فقط في الواجهة
st.markdown('<div class="app-header">AeroSizer Pro</div>', unsafe_allow_html=True)

# عرض النتائج الأساسية في بطاقات علوية
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f'<div class="card-box"><div class="card-label">الوزن الإجمالي المدخل</div><div class="card-value">{res["Wto"]:,.0f}<span class="card-unit">lbs</span></div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="card-box"><div class="card-label">الوزن الفارغ المحسوب</div><div class="card-value">{res["W_empty"]:,.0f}<span class="card-unit">lbs</span></div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="card-box"><div class="card-label">إجمالي وزن الوقود</div><div class="card-value">{res["W_fuel"]:,.0f}<span class="card-unit">lbs</span></div></div>', unsafe_allow_html=True)

st.divider()

# عرض الجداول (المعطيات والنتائج التفصيلية)
col_a, col_b = st.columns([3, 2])

with col_a:
    st.subheader("📊 تفاصيل توزيع الوزن")
    df_weight = pd.DataFrame({
        "المكون": ["الحمولة (Payload)", "إجمالي الوقود", "الوزن الفارغ التشغيلي (OEW)", "الوزن الفارغ (Empty Weight)"],
        "الوزن (lbs)": [f"{res['W_pl']:,.0f}", f"{res['W_fuel']:,.0f}", f"{res['W_oe']:,.0f}", f"{res['W_empty']:,.0f}"],
        "النسبة من الإجمالي": [f"{(res['W_pl']/res['Wto'])*100:.1f}%", f"{(res['W_fuel']/res['Wto'])*100:.1f}%", f"{(res['W_oe']/res['Wto'])*100:.1f}%", f"{(res['W_empty']/res['Wto'])*100:.1f}%"]
    })
    st.table(df_weight)

with col_b:
    st.subheader("📝 المعطيات الحالية")
    df_inputs = pd.DataFrame({
        "المتغير": ["المدى (Range)", "عدد الركاب", "نسبة L/D", "كفاءة المروحة", "استهلاك الوقود"],
        "القيمة": [f"{r_nm} nm", f"{pax}", f"{ld_c}", f"{eta_c}", f"{cp_c}"]
    })
    st.table(df_inputs)

# --- 5. تصدير التقرير PDF (مع إصلاح التداخل) ---
def make_pdf():
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, topMargin=2.5*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    
    # تنسيقات مخصصة لمنع التداخل
    pdf_title = ParagraphStyle('T', parent=styles['Heading1'], fontSize=26, alignment=TA_CENTER, spaceAfter=40, leading=32)
    pdf_h1 = ParagraphStyle('H1', parent=styles['Heading2'], fontSize=16, spaceBefore=30, spaceAfter=15, leading=20)
    
    story = []
    story.append(Paragraph("AeroSizer Pro Analysis Report", pdf_title))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.black, spaceAfter=20))
    
    story.append(Paragraph("1. Weight Summary", pdf_h1))
    data = [
        ["Parameter", "Weight (lbs)", "Note"],
        ["Gross Weight (W_TO)", f"{res['Wto']:,.0f}", "User Specified"],
        ["Empty Weight (W_E)", f"{res['W_empty']:,.0f}", "Calculated"],
        ["Fuel Weight (W_F)", f"{res['W_fuel']:,.0f}", "Incl. Reserves"]
    ]
    t = Table(data, colWidths=[6*cm, 5*cm, 5*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.black),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t)
    
    story.append(Paragraph("2. Design Inputs", pdf_h1))
    inp_data = [["Variable", "Value"]] + [[row['المتغير'], row['القيمة']] for _, row in df_inputs.iterrows()]
    ti = Table(inp_data, colWidths=[8*cm, 7*cm])
    ti.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(ti)
    
    doc.build(story)
    buf.seek(0)
    return buf.read()

st.sidebar.markdown("---")
st.sidebar.download_button("📥 تحميل التقرير بصيغة PDF", make_pdf(), "aerosizer_report.pdf", "application/pdf")
