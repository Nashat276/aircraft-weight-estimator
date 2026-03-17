import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math, io
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                 Table, TableStyle, HRFlowable, KeepTogether)
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_LEFT

# --- إعدادات الصفحة ---
st.set_page_config(page_title="AeroSizer Pro", page_icon="✈", layout="wide")

# --- CSS مخصص للطابع الهندسي ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=JetBrains+Mono:wght@400;500&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
        background-color: #F8FAFC !important;
    }
    .main-title {
        font-family: 'JetBrains Mono', monospace;
        font-size: 2.2rem;
        font-weight: 600;
        color: #0F172A;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 0.9rem;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 2rem;
    }
    .section-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin-bottom: 1.5rem;
    }
    .metric-label {
        font-size: 0.75rem;
        color: #64748B;
        font-weight: 600;
        text-transform: uppercase;
    }
    .metric-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.5rem;
        color: #0369A1;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# --- محرك الفيزياء (Physics Engine) ---
def calculate_mission(p):
    # حساب الأوزان الثابتة
    W_payload = p['npax'] * (p['wpax'] + p['wbag']) + p['ncrew'] * 205 + p['natt'] * 200
    W_crew = p['ncrew'] * 205 + p['natt'] * 200
    W_tfo = p['Wto_guess'] * p['Mtfo']
    
    # Breguet Equations
    R_statute = p['R'] * 1.15078
    W5_W4 = 1.0 / math.exp(R_statute / (375.0 * (p['npc'] / p['Cpc']) * p['LDc']))
    
    V_loiter_mph = p['Vl'] * 1.15078
    W6_W5 = 1.0 / math.exp(p['El'] / (375.0 * (1.0 / V_loiter_mph) * (p['npl'] / p['Cpl']) * p['LDl']))
    
    # Fractions dictionary
    fractions = {
        'Start/Taxi/Takeoff': 0.970, # التبسيط للهندسة الأولية
        'Climb': 0.985,
        'Cruise': W5_W4,
        'Loiter': W6_W5,
        'Landing': 0.995
    }
    
    Mff = 1.0
    for f in fractions.values(): Mff *= f
    
    W_fuel_used = p['Wto_guess'] * (1.0 - Mff)
    W_fuel_total = W_fuel_used / (1.0 - p['Mr']) # شامل الاحتياطي
    
    W_empty_calculated = p['Wto_guess'] - W_fuel_total - W_payload
    
    # Raymer Statistical Empty Weight
    W_empty_statistical = 10**((math.log10(p['Wto_guess']) - p['A']) / p['B'])
    
    return {
        'W_payload': W_payload,
        'W_fuel': W_fuel_total,
        'W_empty_calc': W_empty_calculated,
        'W_empty_stat': W_empty_statistical,
        'Mff': Mff,
        'diff': W_empty_statistical - W_empty_calculated,
        'fractions': fractions
    }

def solve_weight(p):
    low, high = 5000.0, 500000.0
    for _ in range(100):
        mid = (low + high) / 2
        p['Wto_guess'] = mid
        res = calculate_mission(p)
        if abs(res['diff']) < 0.1: break
        if res['diff'] > 0: low = mid
        else: high = mid
    return mid, res

# --- Sidebar Inputs ---
with st.sidebar:
    st.markdown("### ⚙️ Mission Parameters")
    
    with st.expander("Payload & Crew", expanded=True):
        npax = st.number_input("Passengers", 1, 500, 34)
        wpax = st.number_input("Pax Weight (lbs)", 100, 250, 175)
        wbag = st.number_input("Baggage (lbs)", 0, 100, 30)
        ncrew = st.number_input("Flight Crew", 1, 10, 2)
        natt = st.number_input("Cabin Attendants", 0, 20, 1)

    with st.expander("Performance Indices", expanded=True):
        R_nm = st.number_input("Range (nm)", 100, 5000, 1100)
        LDc = st.slider("Cruise L/D", 5.0, 25.0, 13.0)
        Cpc = st.number_input("Cruise SFC (lb/hp/hr)", 0.3, 1.0, 0.6)
        npc = st.slider("Prop Efficiency", 0.5, 0.95, 0.85)
        
    with st.expander("Statistical Constants", expanded=False):
        A_const = st.number_input("A (Raymer)", 0.0, 1.0, 0.3774, format="%.4f")
        B_const = st.number_input("B (Raymer)", 0.5, 1.5, 0.9647, format="%.4f")
        Mtfo = st.number_input("Trapped Fuel Fraction", 0.0, 0.05, 0.005, format="%.3f")

# --- Main Application Logic ---
params = {
    'npax': npax, 'wpax': wpax, 'wbag': wbag, 'ncrew': ncrew, 'natt': natt,
    'R': R_nm, 'LDc': LDc, 'Cpc': Cpc, 'npc': npc,
    'El': 0.75, 'Vl': 250, 'LDl': 16.0, 'Cpl': 0.65, 'npl': 0.77,
    'A': A_const, 'B': B_const, 'Mtfo': Mtfo, 'Mr': 0.05
}

W_to, final_res = solve_weight(params)

# --- UI Layout ---
st.markdown('<div class="main-title">AeroSizer Pro</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Preliminary Aircraft Sizing & Weight Estimation</div>', unsafe_allow_html=True)

# 1. قسم النتائج الرئيسية (Gross Weight)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f'<div class="section-card"><div class="metric-label">Gross Takeoff Weight</div><div class="metric-value">{W_to:,.0f} <span style="font-size:0.8rem">lbs</span></div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="section-card"><div class="metric-label">Empty Weight</div><div class="metric-value">{final_res["W_empty_calc"]:,.0f} <span style="font-size:0.8rem">lbs</span></div></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="section-card"><div class="metric-label">Total Fuel</div><div class="metric-value">{final_res["W_fuel"]:,.0f} <span style="font-size:0.8rem">lbs</span></div></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="section-card"><div class="metric-label">Payload</div><div class="metric-value">{final_res["W_payload"]:,.0f} <span style="font-size:0.8rem">lbs</span></div></div>', unsafe_allow_html=True)

# 2. تقسيم الأوزان والمعطيات في صف واحد
c_left, c_right = st.columns([1, 1])

with c_left:
    st.subheader("📊 Weight Composition")
    fig = go.Figure(data=[go.Pie(
        labels=['Empty Weight', 'Fuel Weight', 'Payload'],
        values=[final_res['W_empty_calc'], final_res['W_fuel'], final_res['W_payload']],
        hole=.4,
        marker_colors=['#0369A1', '#0EA5E9', '#7DD3FC']
    )])
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=300, showlegend=True)
    st.plotly_chart(fig, use_container_width=True)

with c_right:
    st.subheader("📝 Active Configuration")
    input_data = {
        "Requirement": ["Range", "Passengers", "Cruise L/D", "Prop Efficiency"],
        "Value": [f"{R_nm} nm", f"{npax}", f"{LDc}", f"{npc}"]
    }
    st.table(pd.DataFrame(input_data))

# --- PDF Generation (Fixed Version) ---
def generate_professional_pdf():
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, topMargin=2.5*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    
    # تعريف الستايلات المحسنة لتجنب التداخل
    title_style = ParagraphStyle(
        'Title', parent=styles['Heading1'], fontSize=24, textColor=colors.HexColor('#0F172A'),
        spaceAfter=15, leading=28  # زيادة الـ leading لمنع التداخل
    )
    h2_style = ParagraphStyle(
        'H2', parent=styles['Heading2'], fontSize=16, color=colors.HexColor('#0369A1'),
        spaceBefore=20, spaceAfter=12, leading=20
    )
    body_style = ParagraphStyle(
        'Body', parent=styles['Normal'], fontSize=10, leading=14, spaceAfter=10
    )
    
    story = []
    
    # العنوان
    story.append(Paragraph("AeroSizer Pro: Estimation Report", title_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.grey))
    story.append(Spacer(1, 15))
    
    # قسم الأوزان
    story.append(Paragraph("1. Final Sizing Results", h2_style))
    weight_data = [
        ["Parameter", "Value (lbs)", "Fraction of W_TO"],
        ["Gross Takeoff Weight (W_TO)", f"{W_to:,.2f}", "100%"],
        ["Empty Weight (W_E)", f"{final_res['W_empty_calc']:,.2f}", f"{(final_res['W_empty_calc']/W_to)*100:.1f}%"],
        ["Total Fuel Weight (W_F)", f"{final_res['W_fuel']:,.2f}", f"{(final_res['W_fuel']/W_to)*100:.1f}%"],
        ["Payload Weight (W_PL)", f"{final_res['W_payload']:,.2f}", f"{(final_res['W_payload']/W_to)*100:.1f}%"]
    ]
    t = Table(weight_data, colWidths=[7*cm, 4*cm, 4*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t)
    
    # قسم المعطيات
    story.append(Paragraph("2. Design Inputs", h2_style))
    input_table = [["Parameter", "Value"]] + [[k, str(v)] for k, v in params.items() if k != 'Wto_guess']
    it = Table(input_table, colWidths=[8*cm, 7*cm])
    it.setStyle(TableStyle([
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.grey),
        ('BOX', (0,0), (-1,-1), 0.25, colors.grey),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    # استخدام KeepTogether لمنع انفصال الجدول عن عنوانه
    story.append(KeepTogether(it))
    
    doc.build(story)
    buf.seek(0)
    return buf

st.sidebar.markdown("---")
if st.sidebar.button("📄 Export Engineering Report"):
    pdf_buf = generate_professional_pdf()
    st.sidebar.download_button("Download PDF", pdf_buf, "AeroSizer_Report.pdf", "application/pdf")
