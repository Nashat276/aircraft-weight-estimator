import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math, io
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                 Table, TableStyle, HRFlowable, KeepTogether)
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

# --- إعداد الصفحة ---
st.set_page_config(page_title="AeroSizer Pro", page_icon="✈", layout="wide")

# --- التصميم البصري (CSS) ---
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
.cn { font-size:0.74rem; color:#94A3B8; line-height:1.6; margin-top:0.5rem; }

.kpi { background:#fff; border:1px solid #E2E8F0; border-radius:10px;
  padding:0.9rem 1rem; border-top:2px solid #0EA5E9; }
.kv { font-family:'DM Mono',monospace; font-size:1.35rem; font-weight:500;
  color:#0D1B2A; line-height:1.1; }
.ku { font-size:0.7rem; color:#64748B; margin-left:0.15rem; }
.kl { font-size:0.58rem; color:#94A3B8; letter-spacing:0.09em;
  margin-top:0.28rem; text-transform:uppercase; }

.s-ok { background:#F0FDF4; border-left:3px solid #22C55E; border-radius:0 8px 8px 0;
  padding:0.55rem 1.1rem; font-family:'DM Mono',monospace; font-size:0.78rem;
  color:#15803D; margin-bottom:1.2rem; }

[data-testid="stSidebar"] { background:#fff !important; border-right:1px solid #E2E8F0 !important; }
.sb-sec { font-family:'DM Mono',monospace; font-size:0.61rem; font-weight:500;
  color:#0369A1; letter-spacing:0.15em; text-transform:uppercase;
  padding:0.4rem 0 0.32rem; border-bottom:1px solid #F1F5F9; margin:0.55rem 0 0.6rem; }

.stTabs [data-baseweb="tab-list"] { background:#fff; border-radius:9px;
  padding:3px; border:1px solid #E2E8F0; gap:2px; margin-bottom:0.9rem; }
.stTabs [data-baseweb="tab"] { border-radius:6px; font-size:0.78rem; font-weight:500;
  color:#64748B; padding:0.38rem 1rem; }
.stTabs [aria-selected="true"] { background:#0D1B2A !important; color:#fff !important; }

div.stDownloadButton > button { background:#0D1B2A !important; color:#fff !important;
  border:none !important; border-radius:8px !important; font-size:0.78rem !important;
  font-weight:500 !important; padding:0.5rem 1rem !important; width:100% !important; }
</style>
""", unsafe_allow_html=True)

# ── سمة الرسوم البيانية ──
_B = dict(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='#FAFBFC',
          font=dict(family='DM Mono', color='#475569', size=9.5),
          margin=dict(l=52,r=14,t=30,b=40))
_AX = dict(gridcolor='#F1F5F9', linecolor='#E2E8F0', zerolinecolor='#E2E8F0')

def pf(fig, h=220, xt='', yt=''):
    fig.update_layout(**_B, height=h)
    fig.update_xaxes(**_AX); fig.update_yaxes(**_AX)
    return fig

# ── محرك الحسابات (المعدل ليعمل بوزن ثابت) ──
def mission_calc(p):
    # حسابات الحمولة
    Wpl   = p['npax']*(p['wpax']+p['wbag']) + p['ncrew']*205 + p['natt']*200
    Wcrew = p['ncrew']*205 + p['natt']*200
    Wtfo  = p['Wto_input']*p['Mtfo']
    
    # Breguet Equations
    Rc    = p['R']*1.15078
    W5    = 1.0/math.exp(Rc / (375.0*(p['npc']/p['Cpc'])*p['LDc']))
    Vm    = p['Vl']*1.15078
    W6    = 1.0/math.exp(p['El'] / (375.0*(1.0/Vm)*(p['npl']/p['Cpl'])*p['LDl']))
    
    fn = ['Engine Start','Taxi','Takeoff','Climb','Cruise','Loiter','Descent','Landing']
    fv = [0.990, 0.995, 0.995, 0.985, W5, W6, 0.985, 0.995]
    
    Mff = 1.0
    for v in fv: Mff *= v
    
    # حساب الأوزان بناءً على مدخل المستخدم
    Wto = p['Wto_input']
    WFu = Wto*(1.0-Mff)
    WF  = WFu + Wto*p['Mr']*(1.0-Mff) + Wtfo
    WOE = Wto - WF - Wpl
    WE  = WOE - Wtfo - Wcrew
    WEa = 10.0**((math.log10(max(1.0, Wto))-p['A'])/p['B'])
    
    return dict(Wpl=Wpl, Wcrew=Wcrew, Wtfo=Wtfo, Mff=Mff,
                WF=WF, WFu=WFu, WOE=WOE, WE=WE, WEa=WEa,
                diff=WEa-WE, fracs=dict(zip(fn,fv)))

# ── القائمة الجانبية (المدخلات) ──
with st.sidebar:
    st.markdown('<div style="font-family:DM Mono,monospace;font-size:1rem;font-weight:500;color:#0D1B2A">AERO<span style="color:#0EA5E9">SIZER</span> PRO</div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-sec">Configuration & Weight</div>', unsafe_allow_html=True)
    
    # الوزن المطلوب وضعه بجانب المعطيات
    wto_user = st.number_input("Design Gross Weight (W_TO) lbs", 5000, 800000, 48550, step=500)
    
    st.markdown('<div class="sb-sec">Cabin & Mission</div>', unsafe_allow_html=True)
    npax = st.number_input("Passengers", 1, 400, 34)
    R_nm = st.number_input("Design range (nm)", 100, 6000, 1100)
    
    st.markdown('<div class="sb-sec">Performance Indices</div>', unsafe_allow_html=True)
    LDc  = st.number_input("Cruise L/D", 4.0, 30.0, 13.0, step=0.5)
    Cpc  = st.number_input("SFC Cp (lbs/hp/hr)", 0.2, 1.2, 0.6)
    npc  = st.number_input("Prop. eff. η_p", 0.3, 0.98, 0.85)

# تجميع المعطيات
P = dict(Wto_input=float(wto_user), npax=int(npax), wpax=175.0, wbag=30.0,
         ncrew=2, natt=1, Mtfo=0.005, Mr=0.0, R=float(R_nm), Vl=250.0, 
         LDc=float(LDc), Cpc=float(Cpc), npc=float(npc), El=0.75, 
         LDl=16.0, Cpl=0.65, npl=0.77, A=0.3774, B=0.9647)

# الحسابات
RR = mission_calc(P)
Wto = P['Wto_input']
WE, WF, Wpl = RR['WE'], RR['WF'], RR['Wpl']

# ── الواجهة الرئيسية (التصميم الذي طلبته) ──
st.markdown(f"""
<div style="background:#fff;border:1px solid #E2E8F0;border-radius:14px;
  border-top:3px solid #0EA5E9;padding:1.1rem 1.6rem;margin-bottom:1.1rem">
  <div style="display:flex;align-items:center;justify-content:space-between;gap:1rem">
    <div style="min-width:0">
      <div style="font-family:'DM Mono',monospace;font-size:1.25rem;font-weight:600;color:#0D1B2A;margin-bottom:0.22rem">
        AERO<span style="color:#0EA5E9">SIZER</span> PRO
      </div>
      <div style="font-family:'DM Mono',monospace;font-size:0.6rem;color:#64748B;text-transform:uppercase;white-space:nowrap">
        Preliminary Weight Analysis · Fixed W_TO Input Mode · Breguet Method
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
metrics = [(k1, f"{Wto:,.0f}", "lbs", "Input Gross W_TO"), 
           (k2, f"{RR['Mff']:.5f}", "", "Fuel Fraction Mff"),
           (k3, f"{WF:,.0f}", "lbs", "Total Fuel W_F"),
           (k4, f"{Wpl:,.0f}", "lbs", "Payload W_PL"),
           (k5, f"{WE:,.0f}", "lbs", "Empty Weight W_E")]

for col, val, unit, lbl in metrics:
    with col:
        st.markdown(f'<div class="kpi"><div class="kv">{val}<span class="ku">{unit}</span></div><div class="kl">{lbl}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
tab1, tab2, tab3 = st.tabs(["  ① Mission Sizing  ", "  ② Weight Breakdown  ", "  ③ Export  "])

with tab1:
    c1, c2 = st.columns([3,2], gap="medium")
    with c1:
        st.markdown('<div class="card"><div class="ct">Mission Phase Weight Fractions</div>', unsafe_allow_html=True)
        phases = list(RR['fracs'].keys()); fvals = list(RR['fracs'].values())
        fig_m = go.Figure(go.Bar(x=phases, y=fvals, marker_color='#0EA5E9', text=[f'{v:.4f}' for v in fvals], textposition='outside'))
        pf(fig_m, h=250); st.plotly_chart(fig_m, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="card"><div class="ct">Sizing Check (Raymer Regression)</div>', unsafe_allow_html=True)
        st.table(pd.DataFrame({'Parameter':['W_E Calculated','W_E Allowable','Difference'],
                               'Value':[f"{WE:,.0f} lbs", f"{RR['WEa']:,.0f} lbs", f"{RR['diff']:+.1f} lbs"]}))
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    w1, w2 = st.columns(2)
    with w1:
        st.markdown('<div class="card"><div class="ct">W_TO Composition</div>', unsafe_allow_html=True)
        fig_p = go.Figure(go.Pie(labels=['Empty','Fuel','Payload'], values=[WE, WF, Wpl], hole=0.5, marker_colors=['#0EA5E9','#38BDF8','#10B981']))
        pf(fig_p, h=300); st.plotly_chart(fig_p, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with w2:
        st.markdown('<div class="card"><div class="ct">Key Ratios</div>', unsafe_allow_html=True)
        st.table(pd.DataFrame({'Ratio':['W_PL / W_TO', 'W_F / W_TO', 'W_E / W_TO'], 
                               'Value':[f"{Wpl/Wto:.4f}", f"{WF/Wto:.4f}", f"{WE/Wto:.4f}"]}))
        st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="card"><div class="ct">Download Results</div>', unsafe_allow_html=True)
    csv = pd.DataFrame({'Component':['W_TO','W_E','W_F','W_PL'], 'Value':[Wto, WE, WF, Wpl]}).to_csv(index=False)
    st.download_button("⬇ Download CSV", csv, "results.csv", "text/csv")
    st.markdown('</div>', unsafe_allow_html=True)
