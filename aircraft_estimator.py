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
from reportlab.lib.enums import TA_CENTER, TA_LEFT

# --- إعداد الصفحة والتصميم ---
st.set_page_config(page_title="AeroSizer Pro", page_icon="✈", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500;600&display=swap');
*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] {
    background: #F5F7FA !important;
    color: #1A1D2E !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stApp { background: #F5F7FA !important; }

.card { background:#fff; border:1px solid #E2E8F0; border-radius:12px;
  padding:1.1rem 1.3rem; margin-bottom:0.9rem; }
.ct { font-family:'DM Mono',monospace; font-size:0.66rem; font-weight:500;
  color:#0369A1; letter-spacing:0.13em; text-transform:uppercase;
  padding-bottom:0.5rem; border-bottom:1px solid #F1F5F9; margin-bottom:0.8rem; }

.kpi { background:#fff; border:1px solid #E2E8F0; border-radius:10px;
  padding:0.9rem 1rem; border-top:2px solid #0EA5E9; }
.kv { font-family:'DM Mono',monospace; font-size:1.35rem; font-weight:500;
  color:#0D1B2A; line-height:1.1; }
.ku { font-size:0.7rem; color:#64748B; margin-left:0.15rem; }
.kl { font-size:0.58rem; color:#94A3B8; letter-spacing:0.09em;
  margin-top:0.28rem; text-transform:uppercase; }

[data-testid="stSidebar"] { background:#fff !important; border-right:1px solid #E2E8F0 !important; }
.sb-sec { font-family:'DM Mono',monospace; font-size:0.61rem; font-weight:500;
  color:#0369A1; letter-spacing:0.15em; text-transform:uppercase;
  padding:0.4rem 0 0.32rem; border-bottom:1px solid #F1F5F9; margin:0.55rem 0 0.6rem; }
</style>
""", unsafe_allow_html=True)

# ── Physics Engine ──
def mission(p):
    Wpl   = p['npax']*(p['wpax']+p['wbag']) + p['ncrew']*205 + p['natt']*200
    Wcrew = p['ncrew']*205 + p['natt']*200
    Wtfo  = p['Wto']*p['Mtfo']
    
    Rc    = p['R']*1.15078
    W5    = 1.0/math.exp(Rc / (375.0*(p['npc']/p['Cpc'])*p['LDc']))
    Vm    = p['Vl']*1.15078
    W6    = 1.0/math.exp(p['El'] / (375.0*(1.0/Vm)*(p['npl']/p['Cpl'])*p['LDl']))
    
    fn = ['Start','Taxi','Takeoff','Climb','Cruise','Loiter','Descent','Landing']
    fv = [0.990, 0.995, 0.995, 0.985, W5, W6, 0.985, 0.995]
    Mff = 1.0
    for v in fv: Mff *= v
    
    WFu = p['Wto']*(1.0-Mff)
    WF  = WFu + p['Wto']*p['Mr']*(1.0-Mff) + Wtfo
    WOE = p['Wto'] - WF - Wpl
    WE  = WOE - Wtfo - Wcrew
    WEa = 10.0**((math.log10(max(1.0, p['Wto']))-p['A'])/p['B'])
    
    return dict(Wpl=Wpl, Wcrew=Wcrew, Wtfo=Wtfo, Mff=Mff,
                WF=WF, WFu=WFu, WOE=WOE, WE=WE, WEa=WEa,
                diff=WEa-WE, fracs=dict(zip(fn,fv)))

# ── Sidebar Inputs ──
with st.sidebar:
    st.markdown('<div style="font-family:DM Mono,monospace;font-size:1rem;font-weight:500;color:#0D1B2A">AERO<span style="color:#0EA5E9">SIZER</span> PRO</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sb-sec">Configuration & Weight</div>', unsafe_allow_html=True)
    wto_manual = st.number_input("Design Gross Weight (W_TO) lbs", 5000, 800000, 48550)
    
    st.markdown('<div class="sb-sec">Mission Inputs</div>', unsafe_allow_html=True)
    npax = st.number_input("Passengers", 1, 400, 34)
    R_nm = st.number_input("Range (nm)", 100, 6000, 1100)
    LDc  = st.number_input("Cruise L/D", 4.0, 30.0, 13.0)
    Cpc  = st.number_input("SFC Cp", 0.2, 1.2, 0.6)
    npc  = st.number_input("Prop. eff. η_p", 0.3, 0.98, 0.85)

# الحسابات بناءً على الوزن المدخل
P = dict(Wto=float(wto_manual), npax=int(npax), wpax=175.0, wbag=30.0,
         ncrew=2, natt=1, Mtfo=0.005, Mr=0.0, R=float(R_nm), Vl=250.0, 
         LDc=float(LDc), Cpc=float(Cpc), npc=float(npc), El=0.75, 
         LDl=16.0, Cpl=0.65, npl=0.77, A=0.3774, B=0.9647)

RR = mission(P)
Wto = P['Wto']
WE, WF, Wpl = RR['WE'], RR['WF'], RR['Wpl']

# ── واجهة العرض (Header) ──
st.markdown(f"""
<div style="background:#fff;border:1px solid #E2E8F0;border-radius:14px;
  border-top:3px solid #0EA5E9;padding:1.1rem 1.6rem;margin-bottom:1.1rem">
  <div style="display:flex;align-items:center;justify-content:space-between;gap:1rem">
    <div style="min-width:0">
      <div style="font-family:'DM Mono',monospace;font-size:1.25rem;font-weight:600;color:#0D1B2A;margin-bottom:0.22rem">
        AERO<span style="color:#0EA5E9">SIZER</span> PRO
      </div>
      <div style="font-family:'DM Mono',monospace;font-size:0.6rem;color:#64748B;text-transform:uppercase;">
        Preliminary Aircraft Weight Estimation Report · Fixed Weight Input Mode
      </div>
    </div>
    <div style="text-align:right;border-left:1px solid #E2E8F0;padding-left:1.2rem;">
      <div style="font-family:'DM Mono',monospace;font-size:0.56rem;color:#94A3B8;text-transform:uppercase">User Input W_TO</div>
      <div style="font-family:'DM Mono',monospace;font-size:1.85rem;font-weight:600;color:#0369A1;">{Wto:,.0f}</div>
      <div style="font-family:'DM Mono',monospace;font-size:0.58rem;color:#94A3B8;">lbs</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# KPI Row
k1,k2,k3,k4,k5 = st.columns(5)
for col, val, unit, lbl in [(k1, f"{Wto:,.0f}", "lbs", "Gross W_TO"), 
                             (k2, f"{RR['Mff']:.5f}", "", "Mff Fraction"),
                             (k3, f"{WF:,.0f}", "lbs", "Total Fuel"),
                             (k4, f"{Wpl:,.0f}", "lbs", "Payload"),
                             (k5, f"{WE:,.0f}", "lbs", "Empty Weight")]:
    with col:
        st.markdown(f'<div class="kpi"><div class="kv">{val}<span class="ku">{unit}</span></div><div class="kl">{lbl}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
tab1, tab2, tab3 = st.tabs(["  ① Mission Sizing  ", "  ② Weight Breakdown  ", "  ③ Export PDF  "])

with tab1:
    c1, c2 = st.columns([3,2], gap="medium")
    with c1:
        st.markdown('<div class="card"><div class="ct">Phase Weight Fractions</div>', unsafe_allow_html=True)
        fig_m = go.Figure(go.Bar(x=list(RR['fracs'].keys()), y=list(RR['fracs'].values()), marker_color='#0EA5E9'))
        fig_m.update_layout(height=250, margin=dict(l=20,r=20,t=20,b=20), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='#FAFBFC')
        st.plotly_chart(fig_m, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="card"><div class="ct">Weight Check (Raymer Regression)</div>', unsafe_allow_html=True)
        st.table(pd.DataFrame({'Parameter':['Calculated WE','Allowable WE','Delta'],
                               'Value':[f"{WE:,.0f} lbs", f"{RR['WEa']:,.0f} lbs", f"{RR['diff']:+.1f} lbs"]}))
        st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    def make_pdf():
        buf = io.BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=2*cm, rightMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
        styles = getSampleStyleSheet()
        
        # --- إصلاح التداخل هنا ---
        sTITLE = ParagraphStyle('TI', parent=styles['Normal'], fontSize=22, fontName='Helvetica-Bold',
                                textColor=colors.HexColor('#0D1B2A'), spaceAfter=12, leading=26, alignment=TA_LEFT)
        sSUB   = ParagraphStyle('SU', parent=styles['Normal'], fontSize=8.5, textColor=colors.HexColor('#64748B'),
                                spaceAfter=6, leading=12)
        sH1    = ParagraphStyle('H1', parent=styles['Normal'], fontSize=11, fontName='Helvetica-Bold',
                                textColor=colors.HexColor('#0369A1'), spaceBefore=14, spaceAfter=8)
        
        story = []
        story += [Paragraph("AeroSizer Pro Analysis Report", sTITLE),
                  Paragraph("Preliminary Aircraft Weight Estimation", sSUB),
                  Paragraph("Breguet Range / Endurance Method · Propeller-Driven · Fixed Input Mode", sSUB),
                  HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0EA5E9')),
                  Spacer(1, 0.5*cm)]
        
        story.append(Paragraph("1. Primary Weight Summary", sH1))
        data = [['Component', 'lbs', 'Fraction'],
                ['Gross Weight (W_TO)', f"{Wto:,.0f}", "1.0000"],
                ['Empty Weight (W_E)', f"{WE:,.0f}", f"{WE/Wto:.4f}"],
                ['Total Fuel Weight', f"{WF:,.0f}", f"{WF/Wto:.4f}"],
                ['Payload Weight', f"{Wpl:,.0f}", f"{Wpl/Wto:.4f}"]]
        
        t = Table(data, colWidths=[7*cm, 4*cm, 4*cm])
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#0D1B2A')),
                               ('TEXTCOLOR',(0,0),(-1,0),colors.white),
                               ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                               ('FONTSIZE',(0,0),(-1,-1),8.5),
                               ('BOTTOMPADDING',(0,0),(-1,-1),5)]))
        story.append(t)
        
        doc.build(story)
        buf.seek(0)
        return buf.read()

    st.markdown('<div class="card"><div class="ct">Generate Professional Report</div>', unsafe_allow_html=True)
    st.download_button("⬇ Download Report (PDF)", make_pdf(), "aerosizer_report.pdf", "application/pdf", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
