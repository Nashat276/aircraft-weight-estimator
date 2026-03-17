import streamlit as st
import numpy as np
import pandas as pd
import math, io
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                 Table, TableStyle, HRFlowable)
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER

# --- 1. إعدادات الصفحة والتنسيق البصري ---
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
        border-bottom: 2px solid #E2E8F0;
        padding-bottom: 1rem;
    }

    /* بطاقات النتائج الرقمية */
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

# --- 2. محرك الحسابات (معادلات Breguet) ---
def run_sizing(p):
    # حساب الحمولة والطاقم
    W_pl = p['npax'] * (p['wpax'] + p['wbag']) + p['ncrew'] * 205 + p['natt'] * 200
    W_crew = p['ncrew'] * 205 + p['natt'] * 200
    
    # معامل الوزن للرحلة (Cruise) - Breguet propeller range
    R_statute = p['R'] * 1.15078
    Wc = 1.0 / math.exp(R_statute / (375.0 * (p['npc'] / p['Cpc']) * p['LDc']))
    
    # معامل الوزن للانتظار (Loiter)
    V_mph = p['Vl'] * 1.15078
    Wl = 1.0 / math.exp(p['El'] / (375.0 * (1.0 / V_mph) * (p['npl'] / p['Cpl']) * p['LDl']))
    
    # إجمالي معاملات الوزن للمهمة
    Mff = 0.990 * 0.995 * 0.995 * 0.985 * Wc * Wl * 0.985 * 0.995
    
    # الحسابات بناءً على الوزن المدخل
    Wto = p['Wto_user']
    Wtfo = Wto * p['Mtfo']
    W_fuel_usable = Wto * (1.0 - Mff)
    W_fuel_total = W_fuel_usable * (1.0 + p['Mr']) + Wtfo
    W_oe = Wto - W_fuel_total - W_pl
    W_empty = W_oe - Wtfo - W_crew
    
    return {
        'Wto': Wto, 'W_pl': W_pl, 'W_fuel': W_fuel_total, 'W_empty': W_empty,
        'W_oe': W_oe, 'Mff': Mff
    }

# --- 3. القائمة الجانبية: المدخلات ---
with st.sidebar:
    st.header("⚙️ معطيات التصميم")
    
    # إدخال الوزن بجانب بقية المعطيات كما طلبت
    wto_manual = st.number_input("الوزن عند الإقلاع (W_TO) lbs", 5000, 800000, 48550)
    
    st.markdown("---")
    st.subheader("متطلبات المهمة")
    r_nm = st.number_input("المدى Design Range (nm)", 100, 6000, 1100)
    pax = st.number_input("عدد الركاب", 0, 500, 34)
    
    st.subheader("معايير الأداء")
    ld_c = st.slider("نسبة الرفع للسحب L/D", 4.0, 25.0, 13.0)
    cp_c = st.number_input("SFC (lb/hp/hr)", 0.3, 1.1, 0.6)
    eta_p = st.slider("كفاءة المروحة Efficiency", 0.4, 0.95, 0.85)

# --- 4. العرض الرئيسي للنتائج ---
st.markdown('<div class="app-header">AeroSizer Pro</div>', unsafe_allow_html=True)

params = {
    'Wto_user': float(wto_manual), 'npax': pax, 'wpax': 175.0, 'wbag': 30.0,
    'ncrew': 2, 'natt': 1, 'R': float(r_nm), 'LDc': ld_c, 'Cpc': cp_c, 'npc': eta_p,
    'El': 0.75, 'Vl': 250.0, 'LDl': 16.0, 'Cpl': 0.65, 'npl': 0.77,
    'Mtfo': 0.005, 'Mr': 0.05
}
res = run_sizing(params)

# عرض النتائج الأساسية أولاً بأول
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f'<div class="card-box"><div class="card-label">الوزن المدخل W_TO</div><div class="card-value">{res["Wto"]:,.0f}<span class="card-unit">lbs</span></div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="card-box"><div class="card-label">الوزن الفارغ W_E</div><div class="card-value">{res["W_empty"]:,.0f}<span class="card-unit">lbs</span></div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="card-box"><div class="card-label">إجمالي الوقود W_F</div><div class="card-value">{res["W_fuel"]:,.0f}<span class="card-unit">lbs</span></div></div>', unsafe_allow_html=True)

st.divider()

# عرض تفصيلي للمعطيات والنتائج
col_left, col_right = st.columns([3, 2])

with col_left:
    st.subheader("📊 تفصيل توزيع الوزن")
    df_weight = pd.DataFrame({
        "المكون": ["الحمولة (Payload)", "إجمالي الوقود", "الوزن الفارغ التشغيلي (OEW)", "الوزن الفارغ (Empty Weight)"],
        "الوزن (lbs)": [f"{res['W_pl']:,.0f}", f"{res['W_fuel']:,.0f}", f"{res['W_oe']:,.0f}", f"{res['W_empty']:,.0f}"],
        "النسبة": [f"{(res['W_pl']/res['Wto'])*100:.1f}%", f"{(res['W_fuel']/res['Wto'])*100:.1f}%", f"{(res['W_oe']/res['Wto'])*100:.1f}%", f"{(res['W_empty']/res['Wto'])*100:.1f}%"]
    })
    st.table(df_weight)

with col_right:
    st.subheader("📝 المعطيات الحالية")
    df_inputs = pd.DataFrame({
        "المتغير": ["المدى (Range)", "عدد الركاب", "نسبة L/D", "كفاءة المروحة"],
        "القيمة": [f"{r_nm} nm", f"{pax}", f"{ld_c}", f"{eta_p}"]
    })
    st.table(df_inputs)

# --- 5. تصدير ملف PDF ---
def make_pdf():
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, topMargin=2.5*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    
    # تنسيق لمنع التداخل
    pdf_title = ParagraphStyle('T', parent=styles['Heading1'], fontSize=26, alignment=TA_CENTER, spaceAfter=40, leading=32)
    pdf_h1 = ParagraphStyle('H1', parent=styles['Heading2'], fontSize=16, spaceBefore=30, spaceAfter=15, leading=20)
    
    story = []
    story.append(Paragraph("AeroSizer Pro Report", pdf_title))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.black, spaceAfter=20))
    
    story.append(Paragraph("Weight Summary", pdf_h1))
    data = [["Parameter", "Weight (lbs)"], ["Gross Weight", f"{res['Wto']:,.0f}"], ["Empty Weight", f"{res['W_empty']:,.0f}"], ["Fuel Weight", f"{res['W_fuel']:,.0f}"]]
    t = Table(data, colWidths=[8*cm, 7*cm])
    t.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.black), ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke), ('GRID', (0,0), (-1,-1), 0.5, colors.grey), ('BOTTOMPADDING', (0,0), (-1,-1), 10)]))
    story.append(t)
    
    doc.build(story)
    buf.seek(0)
    return buf.read()

st.sidebar.markdown("---")
st.sidebar.download_button("📥 تحميل التقرير (PDF)", make_pdf(), "report.pdf", "application/pdf", use_container_width=True)
