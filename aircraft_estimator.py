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
                                 Table, TableStyle, HRFlowable, PageBreak)
from reportlab.lib.units import cm

st.set_page_config(
    page_title="AeroSizer Pro — Aircraft Weight Estimation",
    page_icon="✈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] {
    background: #F5F6FA !important;
    color: #1A1D2E !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stApp { background: #F5F6FA !important; }

/* ─── TOP HERO BANNER ─── */
.hero {
    background: linear-gradient(135deg, #0D1B2A 0%, #1B2B4B 60%, #0D1B2A 100%);
    border-radius: 16px;
    padding: 2rem 2.4rem;
    margin-bottom: 1.6rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(56,189,248,0.12) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-grid { display: grid; grid-template-columns: 1fr auto; gap: 2rem; align-items: center; }
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 2rem; font-weight: 800;
    color: #fff; letter-spacing: -0.02em; line-height: 1;
    margin-bottom: 0.4rem;
}
.hero-title span { color: #38BDF8; }
.hero-subtitle {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem; color: #94A3B8;
    letter-spacing: 0.14em; text-transform: uppercase;
    margin-bottom: 0.9rem;
}
.hero-desc {
    font-size: 0.88rem; color: #CBD5E1;
    line-height: 1.65; max-width: 640px;
}
.hero-meta {
    display: flex; flex-direction: column; gap: 8px; align-items: flex-end;
}
.hero-badge {
    background: rgba(56,189,248,0.12);
    border: 1px solid rgba(56,189,248,0.25);
    color: #7DD3FC;
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem; letter-spacing: 0.1em;
    padding: 0.35rem 0.85rem;
    border-radius: 6px;
    white-space: nowrap;
}
.hero-stat {
    text-align: right;
}
.hero-stat-v {
    font-family: 'DM Mono', monospace;
    font-size: 1.6rem; font-weight: 500;
    color: #38BDF8; line-height: 1;
}
.hero-stat-l {
    font-size: 0.65rem; color: #64748B;
    letter-spacing: 0.1em; text-transform: uppercase;
    margin-top: 0.15rem;
}

/* ─── STATUS ─── */
.status-ok {
    background: #F0FDF4;
    border-left: 3px solid #22C55E;
    border-radius: 0 10px 10px 0;
    padding: 0.6rem 1.2rem;
    font-family: 'DM Mono', monospace;
    font-size: 0.79rem; color: #15803D;
    margin-bottom: 1.3rem;
}
.status-err {
    background: #FFF7ED;
    border-left: 3px solid #F97316;
    border-radius: 0 10px 10px 0;
    padding: 0.6rem 1.2rem;
    font-family: 'DM Mono', monospace;
    font-size: 0.79rem; color: #C2410C;
    margin-bottom: 1.3rem;
}

/* ─── KPI CARDS ─── */
.kpi-grid { display: grid; grid-template-columns: repeat(5,1fr); gap: 12px; margin-bottom: 1.4rem; }
.kpi-card {
    background: #fff;
    border: 1px solid #E8EBF4;
    border-radius: 12px;
    padding: 1rem 1.15rem;
    position: relative;
    overflow: hidden;
}
.kpi-card::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #38BDF8, #0EA5E9);
    border-radius: 12px 12px 0 0;
}
.kpi-v {
    font-family: 'DM Mono', monospace;
    font-size: 1.4rem; font-weight: 500;
    color: #0D1B2A; line-height: 1.1;
}
.kpi-u { font-size: 0.72rem; color: #64748B; margin-left: 0.18rem; }
.kpi-l {
    font-size: 0.6rem; color: #94A3B8;
    letter-spacing: 0.09em; margin-top: 0.3rem;
    text-transform: uppercase; font-family: 'DM Mono', monospace;
}

/* ─── CARDS ─── */
.card {
    background: #fff;
    border: 1px solid #E8EBF4;
    border-radius: 12px;
    padding: 1.1rem 1.3rem;
    margin-bottom: 1rem;
}
.card-title {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem; font-weight: 500;
    color: #0EA5E9; letter-spacing: 0.14em;
    text-transform: uppercase;
    padding-bottom: 0.55rem;
    border-bottom: 1px solid #F1F5F9;
    margin-bottom: 0.85rem;
}
.card-note {
    font-size: 0.75rem; color: #94A3B8;
    line-height: 1.6; margin-top: 0.6rem;
    font-family: 'DM Sans', sans-serif;
}

/* ─── SECTION LABEL ─── */
.sec-lbl {
    font-family: 'Syne', sans-serif;
    font-size: 1.05rem; font-weight: 700;
    color: #0D1B2A; letter-spacing: -0.01em;
    margin-bottom: 0.9rem;
}

/* ─── REFERENCES ─── */
.ref-item {
    padding: 0.7rem 0.9rem;
    border-left: 3px solid #38BDF8;
    background: #F8FAFE;
    border-radius: 0 8px 8px 0;
    margin-bottom: 0.6rem;
}
.ref-code {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem; color: #0EA5E9;
    font-weight: 500; margin-bottom: 0.2rem;
}
.ref-title { font-size: 0.82rem; color: #1A1D2E; font-weight: 500; margin-bottom: 0.15rem; }
.ref-desc { font-size: 0.75rem; color: #64748B; line-height: 1.5; }

/* ─── SIDEBAR ─── */
[data-testid="stSidebar"] {
    background: #fff !important;
    border-right: 1px solid #E8EBF4 !important;
}
.sb-brand {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem; font-weight: 800;
    color: #0D1B2A; letter-spacing: -0.01em;
}
.sb-brand span { color: #38BDF8; }
.sb-tag {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem; color: #94A3B8;
    letter-spacing: 0.14em; text-transform: uppercase;
    margin-bottom: 1.1rem;
}
.sb-sec {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem; font-weight: 500;
    color: #38BDF8; letter-spacing: 0.16em;
    text-transform: uppercase;
    padding: 0.45rem 0 0.35rem;
    border-bottom: 1px solid #F1F5F9;
    margin: 0.6rem 0 0.7rem;
}

/* ─── TABS ─── */
.stTabs [data-baseweb="tab-list"] {
    background: #fff; border-radius: 10px;
    padding: 3px; border: 1px solid #E8EBF4;
    gap: 2px; margin-bottom: 1rem;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 7px;
    font-size: 0.8rem; font-weight: 500;
    color: #64748B; padding: 0.4rem 1.1rem;
    font-family: 'DM Sans', sans-serif;
}
.stTabs [aria-selected="true"] {
    background: #0D1B2A !important;
    color: #fff !important;
}

/* ─── DOWNLOAD BTN ─── */
div.stDownloadButton > button {
    background: #0D1B2A !important;
    color: #fff !important; border: none !important;
    border-radius: 9px !important;
    font-size: 0.8rem !important; font-weight: 500 !important;
    padding: 0.55rem 1.1rem !important; width: 100% !important;
    font-family: 'DM Sans', sans-serif !important;
    letter-spacing: 0.01em !important;
    transition: background 0.2s !important;
}
div.stDownloadButton > button:hover { background: #1B2B4B !important; }

/* ─── NUMBER INPUT ─── */
[data-testid="stNumberInput"] input {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.85rem !important;
    border-radius: 8px !important;
}

/* ─── CALCULATE BUTTON ─── */
[data-testid="stSidebar"] div.stButton > button {
    background: linear-gradient(135deg, #0369A1, #0EA5E9) !important;
    color: #fff !important; border: none !important;
    border-radius: 9px !important;
    font-size: 0.85rem !important; font-weight: 600 !important;
    padding: 0.65rem 1rem !important; width: 100% !important;
    letter-spacing: 0.04em !important;
    box-shadow: 0 2px 8px rgba(14,165,233,0.35) !important;
}
[data-testid="stSidebar"] div.stButton > button:hover {
    background: linear-gradient(135deg, #0284C7, #38BDF8) !important;
}
.insight {
    background: linear-gradient(135deg, #EFF8FF, #F0FDF4);
    border: 1px solid #BAE6FD;
    border-radius: 10px;
    padding: 0.85rem 1.1rem;
    margin-top: 0.7rem;
}
.insight-title {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem; color: #0284C7;
    letter-spacing: 0.12em; text-transform: uppercase;
    margin-bottom: 0.3rem;
}
.insight-text { font-size: 0.8rem; color: #1E40AF; line-height: 1.55; }
</style>
""", unsafe_allow_html=True)

# ═══════════════ PLOTLY THEME ═══════════════
_B = dict(
    paper_bgcolor='rgba(255,255,255,0)',
    plot_bgcolor='#FAFBFC',
    font=dict(family='DM Mono', color='#475569', size=9.5),
    margin=dict(l=54, r=14, t=32, b=42),
    hoverlabel=dict(bgcolor='#0D1B2A', font_color='#fff',
                    font_size=10, font_family='DM Mono'),
)
_AX = dict(gridcolor='#F1F5F9', linecolor='#E8EBF4', zerolinecolor='#E8EBF4')

def pf(fig, title='', h=220, xt='', yt='', yr=None, xr=None):
    kw = dict(_B); kw['height'] = h
    if title:
        kw['title'] = dict(text=title,
                           font=dict(color='#0D1B2A', size=10.5,
                                     family='DM Mono'), x=0.01)
    fig.update_layout(**kw)
    fig.update_xaxes(**_AX)
    fig.update_yaxes(**_AX)
    if xt: fig.update_xaxes(title_text=xt, title_font=dict(size=8.5, color='#94A3B8'))
    if yt: fig.update_yaxes(title_text=yt, title_font=dict(size=8.5, color='#94A3B8'))
    if yr: fig.update_yaxes(range=yr)
    if xr: fig.update_xaxes(range=xr)
    return fig

# ═══════════════ PHYSICS ═══════════════
def mission(p):
    Wpl   = p['npax']*(p['wpax']+p['wbag']) + p['ncrew']*205 + p['natt']*200
    Wcrew = p['ncrew']*205 + p['natt']*200
    Wtfo  = p['Wto']*p['Mtfo']
    Rc    = p['R']*1.15078
    W5    = 1/math.exp(Rc/(375*(p['npc']/p['Cpc'])*p['LDc']))
    Vm    = p['Vl']*1.15078
    W6    = 1/math.exp(p['El']/(375*(1/Vm)*(p['npl']/p['Cpl'])*p['LDl']))
    fn    = ['Engine Start','Taxi','Takeoff','Climb','Cruise','Loiter','Descent','Landing']
    fv    = [0.990,0.995,0.995,0.985,W5,W6,0.985,0.995]
    Mff   = 1.0
    for v in fv: Mff *= v
    WFu = p['Wto']*(1-Mff)
    WF  = WFu + p['Wto']*p['Mr']*(1-Mff) + Wtfo
    WOE = p['Wto'] - WF - Wpl
    WE  = WOE - Wtfo - Wcrew
    WEa = 10**((math.log10(p['Wto'])-p['A'])/p['B'])
    return dict(Wpl=Wpl,Wcrew=Wcrew,Wtfo=Wtfo,Mff=Mff,
                WF=WF,WFu=WFu,WOE=WOE,WE=WE,WEa=WEa,
                diff=WEa-WE,fracs=dict(zip(fn,fv)))

def solve(p, tol=0.2, n=400):
    pp = dict(p)
    prev_d, prev_w, lo, hi = None, None, None, None
    for w in range(8000, 500000, 3000):
        pp['Wto'] = float(w); d = mission(pp)['diff']
        if prev_d is not None and prev_d*d <= 0:
            lo, hi = float(prev_w), float(w); break
        prev_d, prev_w = d, w
    if lo is None:
        pp['Wto'] = 48550.0; return 48550.0, mission(pp)
    for _ in range(n):
        m = (lo+hi)/2.0; pp['Wto'] = m; r = mission(pp)
        if abs(r['diff']) < tol: return m, r
        if r['diff'] > 0: lo = m
        else: hi = m
    return m, mission(pp)

def sens(p, Wto):
    Rc=p['R']*1.15078; Vm=p['Vl']*1.15078
    Mff=mission({**p,'Wto':Wto})['Mff']
    Wpl=p['npax']*(p['wpax']+p['wbag'])+p['ncrew']*205+p['natt']*200
    Wcrew=p['ncrew']*205+p['natt']*200
    C=1-(1+p['Mr'])*(1-Mff)-p['Mtfo']
    D=Wpl+Wcrew
    dn=C*Wto*(1-p['B'])-D
    F=(-p['B']*Wto**2*(1+p['Mr'])*Mff)/dn if abs(dn)>1e-6 else 0
    E=p['El']
    return dict(
        dCpR= F*Rc/(375*p['npc']*p['LDc']),
        dnpR=-F*Rc*p['Cpc']/(375*p['npc']**2*p['LDc']),
        dLDR=-F*Rc*p['Cpc']/(375*p['npc']*p['LDc']**2),
        dR=   F*p['Cpc']/(375*p['npc']*p['LDc']),
        dCpE= F*E*Vm/(375*p['npl']*p['LDl']),
        dnpE=-F*E*Vm*p['Cpl']/(375*p['npl']**2*p['LDl']),
        dLDE=-F*E*Vm*p['Cpl']/(375*p['npl']*p['LDl']**2),
    )

# ═══════════════ DEFAULTS ═══════════════
D = dict(npax=34,wpax=175,wbag=30,ncrew=2,natt=1,Mtfo=0.005,Mr=0.0,
         R=1100,Vl=250,LDc=13,Cpc=0.60,npc=0.85,
         El=0.75,LDl=16,Cpl=0.65,npl=0.77,A=0.3774,B=0.9647,Wto_init=48550)

# ═══════════════ SIDEBAR ═══════════════
with st.sidebar:
    st.markdown('<div class="sb-brand">AERO<span>SIZER</span> PRO</div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-tag">Aircraft Weight Estimation Tool</div>', unsafe_allow_html=True)

    st.markdown('<div class="sb-sec">Cabin & Crew</div>', unsafe_allow_html=True)
    npax  = st.number_input("Passengers",           min_value=1,   max_value=400, value=D['npax'],  step=1)
    wpax  = st.number_input("Passenger weight (lbs)",min_value=100,max_value=300, value=D['wpax'],  step=5)
    wbag  = st.number_input("Baggage weight (lbs)", min_value=0,   max_value=100, value=D['wbag'],  step=5)
    ncrew = st.number_input("Flight crew",           min_value=1,   max_value=6,   value=D['ncrew'], step=1)
    natt  = st.number_input("Cabin attendants",      min_value=0,   max_value=10,  value=D['natt'],  step=1)

    st.markdown('<div class="sb-sec">Cruise Segment</div>', unsafe_allow_html=True)
    R_nm = st.number_input("Design range (nm)",     min_value=100, max_value=6000, value=D['R'],    step=50)
    LDc  = st.number_input("Cruise L/D ratio",      min_value=4.0, max_value=30.0, value=float(D['LDc']), step=0.5, format="%.1f")
    Cpc  = st.number_input("Cruise SFC Cp (lbs/hp/hr)", min_value=0.20, max_value=1.20, value=D['Cpc'], step=0.01, format="%.2f")
    npc  = st.number_input("Cruise prop. efficiency η", min_value=0.30, max_value=0.98, value=D['npc'], step=0.01, format="%.2f")

    st.markdown('<div class="sb-sec">Loiter / Reserve</div>', unsafe_allow_html=True)
    El   = st.number_input("Loiter endurance (hr)", min_value=0.1, max_value=6.0, value=D['El'],   step=0.05, format="%.2f")
    Vl   = st.number_input("Loiter speed (kts)",    min_value=60,  max_value=400,  value=D['Vl'],   step=5)
    LDl  = st.number_input("Loiter L/D ratio",      min_value=4.0, max_value=30.0, value=float(D['LDl']), step=0.5, format="%.1f")
    Cpl  = st.number_input("Loiter SFC Cp (lbs/hp/hr)", min_value=0.20, max_value=1.20, value=D['Cpl'], step=0.01, format="%.2f")
    npl  = st.number_input("Loiter prop. efficiency η", min_value=0.30, max_value=0.98, value=D['npl'], step=0.01, format="%.2f")

    st.markdown('<div class="sb-sec">Sizing Constants</div>', unsafe_allow_html=True)
    st.caption("Raymer Table 2.2 — turboprop transport category")
    A_v   = st.number_input("Regression constant A", min_value=0.0, max_value=2.0, value=D['A'], step=0.001, format="%.4f")
    B_v   = st.number_input("Regression constant B", min_value=0.1, max_value=2.0, value=D['B'], step=0.001, format="%.4f")
    Mtfo  = st.number_input("Trapped fuel fraction M_tfo", min_value=0.0, max_value=0.05, value=D['Mtfo'], step=0.001, format="%.3f")

    st.markdown("<br>", unsafe_allow_html=True)
    calculate = st.button("⟳  Calculate", use_container_width=True, type="primary")

P = dict(npax=int(npax),wpax=float(wpax),wbag=float(wbag),
         ncrew=int(ncrew),natt=int(natt),
         Mtfo=float(Mtfo),Mr=0.0,R=float(R_nm),
         Vl=float(Vl),LDc=float(LDc),Cpc=float(Cpc),npc=float(npc),
         El=float(El),LDl=float(LDl),Cpl=float(Cpl),npl=float(npl),
         A=float(A_v),B=float(B_v),Wto=48550)

# Use session_state to cache results — only recalculate when button pressed
if 'results' not in st.session_state or calculate:
    Wto, RR = solve(P)
    S = sens(P, Wto)
    st.session_state['results'] = (Wto, RR, S)
else:
    Wto, RR, S = st.session_state['results']
conv = abs(RR['diff']) < 5
WE=RR['WE']; WOE=RR['WOE']; WF=RR['WF']
Wpl=RR['Wpl']; Wcrew=RR['Wcrew']; Wtfo=RR['Wtfo']

# ═══════════════ HERO BANNER ═══════════════
st.markdown(f"""
<div class="hero">
  <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:1.5rem;flex-wrap:wrap">
    <div>
      <div class="hero-title">AERO<span>SIZER</span> PRO</div>
      <div class="hero-subtitle" style="margin-bottom:0.7rem">Preliminary Aircraft Weight Estimation · Breguet Method · Propeller-Driven Aircraft</div>
      <div style="display:flex;gap:8px;flex-wrap:wrap">
        <div class="hero-badge">Raymer (2018)</div>
        <div class="hero-badge">Roskam Pt. I</div>
        <div class="hero-badge">Breguet Eq. 2.9 / 2.11</div>
        <div class="hero-badge">Propeller Aircraft</div>
      </div>
    </div>
    <div style="text-align:right;flex-shrink:0">
      <div style="font-family:'DM Mono',monospace;font-size:0.65rem;color:#64748B;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:0.3rem">Current W_TO</div>
      <div style="font-family:'DM Mono',monospace;font-size:2rem;font-weight:600;color:#38BDF8;line-height:1">{Wto:,.0f}</div>
      <div style="font-family:'DM Mono',monospace;font-size:0.65rem;color:#64748B;letter-spacing:0.1em">lbs</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

if conv:
    st.markdown(f'<div class="status-ok">✓  Solution converged  ·  W_TO = {Wto:,.0f} lbs  ·  Mff = {RR["Mff"]:.5f}  ·  ΔWE = {RR["diff"]:+.1f} lbs</div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div class="status-err">⚠  Not converged  ·  ΔWE = {RR["diff"]:+.0f} lbs  ·  Try increasing range of W_TO guess or check regression constants A, B</div>', unsafe_allow_html=True)

# KPIs
k1,k2,k3,k4,k5 = st.columns(5)
for col,val,unit,lbl in [
    (k1,f"{Wto:,.0f}","lbs","Gross Takeoff  W_TO"),
    (k2,f"{RR['Mff']:.5f}","","Fuel Fraction  Mff"),
    (k3,f"{WF:,.0f}","lbs","Total Fuel  W_F"),
    (k4,f"{Wpl:,.0f}","lbs","Payload  W_PL"),
    (k5,f"{WE:,.0f}","lbs","Empty Weight  W_E"),
]:
    with col:
        st.markdown(f'<div class="kpi-card"><div class="kpi-v">{val}<span class="kpi-u">{unit}</span></div><div class="kpi-l">{lbl}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

tab1,tab2,tab3,tab4,tab5 = st.tabs([
    "  ① Mission Sizing  ",
    "  ② Sensitivity  ",
    "  ③ Weight Breakdown  ",
    "  ④ Export  ",
    "  ⑤ References  "
])

# ═══════════════════════════════════════════════════
# TAB 1 — MISSION SIZING
# ═══════════════════════════════════════════════════
with tab1:
    c1, c2 = st.columns([3,2], gap="medium")

    with c1:
        # Phase fractions + cumulative subplot
        st.markdown('<div class="card"><div class="card-title">Mission Phase Weight Fractions  —  Wi / Wi-1</div>', unsafe_allow_html=True)
        phases = list(RR['fracs'].keys())
        fvals  = list(RR['fracs'].values())
        cum    = [1.0]
        for f in fvals: cum.append(cum[-1]*f)

        fig_m = make_subplots(rows=1,cols=2,
            column_widths=[0.58,0.42],
            subplot_titles=["Wi / Wi-1  per phase","Cumulative fraction"])
        clr=['#38BDF8' if p not in ('Cruise','Loiter') else '#10B981' for p in phases]
        fig_m.add_trace(go.Bar(
            x=phases,y=fvals,marker_color=clr,
            marker_line_color='#fff',marker_line_width=0.8,
            text=[f'{v:.4f}' for v in fvals],
            textposition='outside',textfont=dict(size=8),
            name='Wi/Wi-1'),row=1,col=1)
        fig_m.add_trace(go.Scatter(
            x=['Start']+phases,y=cum,mode='lines+markers',
            line=dict(color='#0EA5E9',width=2),
            marker=dict(color='#0D1B2A',size=5,line=dict(color='#0EA5E9',width=1.5)),
            fill='tozeroy',fillcolor='rgba(14,165,233,0.07)',
            name='Cumulative'),row=1,col=2)
        fig_m.update_layout(
            paper_bgcolor='rgba(255,255,255,0)',plot_bgcolor='#FAFBFC',
            height=240,showlegend=False,
            margin=dict(l=40,r=10,t=34,b=36))
        fig_m.update_xaxes(**_AX)
        fig_m.update_yaxes(**_AX)
        fig_m.update_yaxes(range=[0.78,1.03],row=1,col=1)
        fig_m.update_yaxes(range=[0.70,1.05],row=1,col=2)
        fig_m.update_annotations(font_size=9,font_color='#475569',font_family='DM Mono')
        st.plotly_chart(fig_m,use_container_width=True)
        st.markdown("""<div class="card-note">
        <b>Blue bars</b> = fixed fractions from historical data (Raymer Table 2.1) &nbsp;·&nbsp;
        <b>Green bars</b> = variable fractions computed from Breguet equations (Eq. 2.9 &amp; 2.11).
        The cumulative product gives <b>Mff</b>.
        </div></div>""", unsafe_allow_html=True)

        # Range sweep
        st.markdown('<div class="card"><div class="card-title">Parametric Study  —  W_TO vs Design Range</div>', unsafe_allow_html=True)
        rr_arr=np.linspace(200,min(2500,R_nm*2.5),60); ww_arr=[]
        for rv in rr_arr:
            try: w,_=solve({**P,'R':float(rv)}); ww_arr.append(w if w<500000 else float('nan'))
            except: ww_arr.append(float('nan'))
        fig_r=go.Figure()
        fig_r.add_trace(go.Scatter(
            x=rr_arr,y=ww_arr,mode='lines',
            line=dict(color='#38BDF8',width=2),
            fill='tozeroy',fillcolor='rgba(56,189,248,0.07)',name='W_TO'))
        fig_r.add_vline(x=R_nm,line_dash='dash',line_color='#F59E0B',line_width=1.2,
                        annotation_text=f'Design: {R_nm} nm',
                        annotation_font_color='#B45309',annotation_font_size=8.5)
        fig_r.add_scatter(x=[R_nm],y=[Wto],mode='markers',
                          marker=dict(color='#F59E0B',size=9,
                                      line=dict(color='#fff',width=1.5)),showlegend=False)
        pf(fig_r,h=200,xt='Range (nm)',yt='W_TO (lbs)')
        st.plotly_chart(fig_r,use_container_width=True)
        st.markdown("""<div class="card-note">
        Shows how gross weight grows nonlinearly with range — the fuel fraction increases with distance,
        requiring more fuel which itself adds weight (Breguet penalty). Design point marked in amber.
        </div></div>""", unsafe_allow_html=True)

    with c2:
        # Convergence
        st.markdown('<div class="card"><div class="card-title">Sizing Convergence</div>', unsafe_allow_html=True)
        st.dataframe(pd.DataFrame({
            'Parameter':['W_E Tentative','W_E Allowable','ΔWE (diff)','Mff','Converged?'],
            'Value':[f"{RR['WE']:,.0f} lbs",f"{RR['WEa']:,.0f} lbs",
                     f"{RR['diff']:+.1f} lbs",f"{RR['Mff']:.5f}",
                     '✓  Yes' if conv else '✗  No'],
        }),hide_index=True,use_container_width=True)
        st.markdown("""<div class="card-note">
        Convergence means W_E (calculated from geometry) equals W_E (from regression).
        ΔWE &lt; 0.5 lbs is accepted.
        </div></div>""", unsafe_allow_html=True)

        # Phase table
        st.markdown('<div class="card"><div class="card-title">Phase Fractions Detail</div>', unsafe_allow_html=True)
        src_map={'Engine Start':'T2.1','Taxi':'T2.1','Takeoff':'T2.1','Climb':'Fig2.2',
                 'Cruise':'Eq2.9','Loiter':'Eq2.11','Descent':'T2.1','Landing':'T2.1'}
        st.dataframe(pd.DataFrame({
            'Phase':list(RR['fracs'].keys()),
            'Wi/Wi-1':[f"{v:.4f}" for v in RR['fracs'].values()],
            'Ref.':[src_map[p] for p in RR['fracs'].keys()],
        }),hide_index=True,use_container_width=True)
        st.markdown(f'<div style="font-family:DM Mono,monospace;font-size:.8rem;color:#374151;margin-top:.45rem;padding:.5rem .9rem;background:#F8FAFE;border-radius:8px">Mff = ∏(Wi/Wi-1) = <b style="color:#0EA5E9">{RR["Mff"]:.6f}</b></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Payload breakdown
        st.markdown('<div class="card"><div class="card-title">Payload Breakdown</div>', unsafe_allow_html=True)
        pld = int(npax)*(int(wpax)+int(wbag))
        st.dataframe(pd.DataFrame({
            'Item':[f'{npax} pax × ({wpax}+{wbag})','Crew ({ncrew}×205 lbs)'.format(ncrew=ncrew),
                    f'Attendants ({natt}×200 lbs)','Total W_PL'],
            'lbs':[f"{pld:,.0f}",f"{ncrew*205:,.0f}",
                   f"{natt*200:,.0f}",f"{Wpl:,.0f}"],
        }),hide_index=True,use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════
# TAB 2 — SENSITIVITY
# ═══════════════════════════════════════════════════
with tab2:

    st.markdown('<div class="card"><div class="card-title">About Sensitivity Analysis</div>', unsafe_allow_html=True)
    st.markdown("""<div style="font-size:.82rem;color:#374151;line-height:1.7">
    <b>What does this mean?</b> Each partial derivative (∂W_TO/∂y) tells you: <i>if parameter y changes by one unit,
    how many pounds does the gross weight change?</i><br>
    A large positive value means the parameter <b>strongly increases</b> weight.
    A large negative value means it <b>strongly reduces</b> weight — these are your design levers.
    The tornado chart ranks parameters from least to most influential.
    </div></div>""", unsafe_allow_html=True)

    s1,s2 = st.columns(2,gap="medium")
    with s1:
        st.markdown('<div class="card"><div class="card-title">Cruise Phase — Breguet Partials  (Eq. 2.49–2.51)</div>', unsafe_allow_html=True)
        sdr={'Partial':['∂W_TO/∂Cp (cruise)','∂W_TO/∂η_p (cruise)',
                         '∂W_TO/∂(L/D) (cruise)','∂W_TO/∂R'],
             'Value':[f"{S['dCpR']:+,.0f}",f"{S['dnpR']:+,.0f}",
                      f"{S['dLDR']:+,.0f}",f"{S['dR']:+,.1f}"],
             'Units':['lbs/(lbs/hp/hr)','lbs','lbs','lbs/nm'],
             'Eq.':['2.49','2.50','2.51','2.45']}
        st.dataframe(pd.DataFrame(sdr),hide_index=True,use_container_width=True)
        st.markdown('</div>',unsafe_allow_html=True)
    with s2:
        st.markdown('<div class="card"><div class="card-title">Loiter Phase — Breguet Partials</div>', unsafe_allow_html=True)
        sdl={'Partial':['∂W_TO/∂Cp (loiter)','∂W_TO/∂η_p (loiter)',
                         '∂W_TO/∂(L/D) (loiter)'],
             'Value':[f"{S['dCpE']:+,.0f}",f"{S['dnpE']:+,.0f}",f"{S['dLDE']:+,.0f}"],
             'Units':['lbs/(lbs/hp/hr)','lbs','lbs'],
             'Eq.':['—','—','—']}
        st.dataframe(pd.DataFrame(sdl),hide_index=True,use_container_width=True)
        st.markdown('</div>',unsafe_allow_html=True)

    st.markdown('<div class="card"><div class="card-title">Tornado Chart — Design Parameter Influence Ranking</div>', unsafe_allow_html=True)
    tlbl=['Cp · Cruise','η_p · Cruise','L/D · Cruise','Range R',
          'Cp · Loiter','η_p · Loiter','L/D · Loiter']
    tval=[S['dCpR'],S['dnpR'],S['dLDR'],S['dR']*R_nm*0.1,
          S['dCpE'],S['dnpE'],S['dLDE']]
    idx=sorted(range(7),key=lambda i:abs(tval[i]))
    tlbl=[tlbl[i] for i in idx]; tval=[tval[i] for i in idx]
    clr_t=['#38BDF8' if v>=0 else '#F87171' for v in tval]
    fig_t=go.Figure(go.Bar(
        x=tval,y=tlbl,orientation='h',
        marker_color=clr_t,marker_line_color='#fff',marker_line_width=0.5,
        text=[f'{abs(v):,.0f} lbs' for v in tval],
        textposition='outside',textfont=dict(size=9)))
    fig_t.add_vline(x=0,line_color='#CBD5E1',line_width=1)
    pf(fig_t,h=280,xt='ΔW_TO (lbs) per unit parameter change')
    st.plotly_chart(fig_t,use_container_width=True)
    st.markdown("""<div class="card-note">
    <b>Blue</b> = increasing this parameter increases W_TO (bad) &nbsp;·&nbsp;
    <b>Red</b> = increasing this parameter decreases W_TO (good, e.g. better L/D).
    Note: Range R sensitivity shown for 10% change, all others per unit change.
    </div></div>""", unsafe_allow_html=True)

    # 3D surface
    st.markdown('<div class="card"><div class="card-title">3D Parametric Surface  —  W_TO = f(SFC, L/D)  at Cruise</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:.78rem;color:#94A3B8;margin-bottom:.6rem;font-family:DM Mono,monospace">Rotate with mouse · All other parameters fixed at sidebar values</div>', unsafe_allow_html=True)
    cpa=np.linspace(0.35,0.90,22); lda=np.linspace(8,22,22)
    Z=np.zeros((len(cpa),len(lda)))
    for i,cp in enumerate(cpa):
        for j,ld in enumerate(lda):
            try:
                w,r=solve({**P,'Cpc':float(cp),'LDc':float(ld)})
                Z[i,j]=w if abs(r['diff'])<50 else float('nan')
            except: Z[i,j]=float('nan')
    fig4=go.Figure(go.Surface(
        x=lda,y=cpa,z=Z,
        colorscale=[[0,'#EFF8FF'],[0.4,'#38BDF8'],[0.75,'#0369A1'],[1,'#1E3A5F']],
        opacity=0.92,showscale=True,
        contours=dict(z=dict(show=True,color='rgba(0,0,0,0.06)',width=1)),
        colorbar=dict(len=0.65,thickness=10,
                      tickfont=dict(size=8,color='#475569',family='DM Mono'))))
    fig4.update_layout(
        paper_bgcolor='rgba(255,255,255,0)',
        font=dict(family='DM Mono',color='#475569',size=9),
        scene=dict(
            xaxis=dict(title='L/D (cruise)',backgroundcolor='#F8FAFC',
                       gridcolor='#E8EBF4',linecolor='#E8EBF4'),
            yaxis=dict(title='Cp (lbs/hp/hr)',backgroundcolor='#F8FAFC',
                       gridcolor='#E8EBF4',linecolor='#E8EBF4'),
            zaxis=dict(title='W_TO (lbs)',backgroundcolor='#F8FAFC',
                       gridcolor='#E8EBF4',linecolor='#E8EBF4'),
            bgcolor='#FAFBFC',
            camera=dict(eye=dict(x=1.5,y=-1.5,z=0.85))),
        margin=dict(l=0,r=0,t=8,b=0),height=400)
    st.plotly_chart(fig4,use_container_width=True)
    st.markdown("""<div class="card-note">
    Low Cp (efficient engine) + high L/D (efficient wing) = minimum W_TO in the bottom-left corner.
    The steep cliff shows the design space boundary where no converged solution exists.
    </div></div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════
# TAB 3 — WEIGHT BREAKDOWN
# ═══════════════════════════════════════════════════
with tab3:
    w1,w2 = st.columns([5,4],gap="medium")

    with w1:
        st.markdown('<div class="card"><div class="card-title">Complete Weight Statement</div>', unsafe_allow_html=True)
        summary=pd.DataFrame({
            'Component':[
                'W_TO  — Gross takeoff weight',
                'W_E   — Empty weight',
                'W_OE  — Operating empty weight',
                'W_F   — Total fuel (incl. trapped)',
                'W_F   — Usable fuel',
                'W_tfo — Trapped fuel & oil',
                'W_crew — Flight & cabin crew',
                'W_PL  — Payload',
            ],
            'lbs':[f"{Wto:,.0f}",f"{WE:,.0f}",f"{WOE:,.0f}",
                   f"{WF:,.0f}",f"{RR['WFu']:,.0f}",
                   f"{Wtfo:,.0f}",f"{Wcrew:,.0f}",f"{Wpl:,.0f}"],
            'Fraction':[
                "1.00000",f"{WE/Wto:.5f}",f"{WOE/Wto:.5f}",
                f"{WF/Wto:.5f}",f"{RR['WFu']/Wto:.5f}",
                f"{Wtfo/Wto:.5f}",f"{Wcrew/Wto:.5f}",f"{Wpl/Wto:.5f}"],
            '% W_TO':[
                "100.00%",f"{WE/Wto*100:.2f}%",f"{WOE/Wto*100:.2f}%",
                f"{WF/Wto*100:.2f}%",f"{RR['WFu']/Wto*100:.2f}%",
                f"{Wtfo/Wto*100:.3f}%",f"{Wcrew/Wto*100:.3f}%",
                f"{Wpl/Wto*100:.2f}%"],
        })
        st.dataframe(summary,hide_index=True,use_container_width=True)
        st.markdown('</div>',unsafe_allow_html=True)

        # Mission weight + fuel burn dual chart
        st.markdown('<div class="card"><div class="card-title">Aircraft Weight & Fuel Burn Through Mission</div>', unsafe_allow_html=True)
        fv=list(RR['fracs'].values()); pl=['Ramp']+list(RR['fracs'].keys())
        cum=[Wto]
        for f in fv: cum.append(cum[-1]*f)
        fuel_burn=[cum[0]-c for c in cum]
        fig_w=make_subplots(rows=1,cols=2,subplot_titles=['Gross weight (lbs)','Cumulative fuel burned (lbs)'])
        fig_w.add_trace(go.Scatter(
            x=pl,y=cum,mode='lines+markers',
            line=dict(color='#38BDF8',width=2),
            marker=dict(color='#0D1B2A',size=5,line=dict(color='#38BDF8',width=1.5)),
            fill='tozeroy',fillcolor='rgba(56,189,248,0.06)',name='Weight'),row=1,col=1)
        fig_w.add_trace(go.Scatter(
            x=pl,y=fuel_burn,mode='lines+markers',
            line=dict(color='#F59E0B',width=2),
            marker=dict(color='#0D1B2A',size=5,line=dict(color='#F59E0B',width=1.5)),
            fill='tozeroy',fillcolor='rgba(245,158,11,0.06)',name='Fuel burned'),row=1,col=2)
        fig_w.update_layout(
            paper_bgcolor='rgba(255,255,255,0)',plot_bgcolor='#FAFBFC',
            height=210,showlegend=False,margin=dict(l=40,r=10,t=32,b=34))
        fig_w.update_xaxes(**_AX); fig_w.update_yaxes(**_AX)
        fig_w.update_annotations(font_size=9,font_color='#475569',font_family='DM Mono')
        st.plotly_chart(fig_w,use_container_width=True)
        st.markdown("""<div class="card-note">
        The cruise and loiter phases consume most fuel. Fuel burn is monotonically increasing.
        The step-wise weight drop shows discrete fuel consumption per phase.
        </div></div>""", unsafe_allow_html=True)

    with w2:
        # Donut
        st.markdown('<div class="card"><div class="card-title">W_TO Composition</div>', unsafe_allow_html=True)
        fig_p=go.Figure(go.Pie(
            labels=['Empty Weight','Usable Fuel','Trapped Fuel','Crew','Payload'],
            values=[WE,RR['WFu'],Wtfo,Wcrew,Wpl],hole=0.56,
            marker=dict(colors=['#0EA5E9','#38BDF8','#7DD3FC','#10B981','#34D399'],
                        line=dict(color='#fff',width=2)),
            textfont=dict(size=9.5,family='DM Mono'),textinfo='label+percent',rotation=90))
        fig_p.update_layout(
            paper_bgcolor='rgba(255,255,255,0)',
            font=dict(family='DM Mono',color='#475569'),
            showlegend=False,height=270,margin=dict(t=10,b=10,l=10,r=10),
            annotations=[dict(text=f'<b>{Wto:,.0f}</b><br><span style="font-size:10px">lbs</span>',
                x=0.5,y=0.5,showarrow=False,
                font=dict(size=13,color='#0D1B2A',family='DM Mono'))])
        st.plotly_chart(fig_p,use_container_width=True)
        st.markdown("""<div class="card-note">
        The fuel fraction Mff determines how much of W_TO is fuel.
        A typical turboprop transport has 20–35% fuel weight.
        </div></div>""", unsafe_allow_html=True)

        # Key ratios
        st.markdown('<div class="card"><div class="card-title">Key Design Ratios</div>', unsafe_allow_html=True)
        st.dataframe(pd.DataFrame({
            'Ratio':['W_PL / W_TO (payload efficiency)',
                     'W_F / W_TO (fuel fraction)',
                     'W_E / W_TO (empty fraction)',
                     'W_OE / W_TO (operating empty)',
                     'W_PL / W_E (commercial efficiency)'],
            'Value':[f"{Wpl/Wto:.4f}",f"{WF/Wto:.4f}",f"{WE/Wto:.4f}",
                     f"{WOE/Wto:.4f}",f"{Wpl/WE:.4f}"],
        }),hide_index=True,use_container_width=True)
        st.markdown("""<div class="card-note">
        <b>W_PL/W_E &gt; 0.25</b> is typically required for a commercially viable aircraft.
        W_PL/W_TO &gt; 0.15 indicates an efficient design.
        </div></div>""", unsafe_allow_html=True)

        # W_TO vs pax
        st.markdown('<div class="card"><div class="card-title">W_TO vs Passenger Count</div>', unsafe_allow_html=True)
        pxa=np.arange(5,int(npax)+30,2); wxr=[]
        for n_ in pxa:
            try:
                w,r=solve({**P,'npax':int(n_)})
                wxr.append(w if abs(r['diff'])<50 else float('nan'))
            except: wxr.append(float('nan'))
        fig_px=go.Figure()
        fig_px.add_trace(go.Scatter(
            x=pxa,y=wxr,mode='lines',
            line=dict(color='#10B981',width=2),
            fill='tozeroy',fillcolor='rgba(16,185,129,0.06)'))
        fig_px.add_vline(x=npax,line_dash='dot',line_color='#F59E0B',line_width=1.2,
                         annotation_text=f'{npax} pax',
                         annotation_font_color='#B45309',annotation_font_size=8.5)
        pf(fig_px,h=190,xt='Passengers',yt='W_TO (lbs)')
        st.plotly_chart(fig_px,use_container_width=True)
        st.markdown('</div>',unsafe_allow_html=True)


# ═══════════════════════════════════════════════════
# TAB 4 — EXPORT
# ═══════════════════════════════════════════════════
with tab4:
    e1,e2 = st.columns([1,1],gap="medium")

    with e1:
        st.markdown('<div class="card"><div class="card-title">Export — Spreadsheet Data (CSV)</div>', unsafe_allow_html=True)
        rows={
            'Parameter':['W_TO','Mff','W_F_total','W_F_usable','W_payload','W_empty',
                          'W_OE','W_crew','W_tfo','WE_allowable','delta_WE',
                          'dWTO_dCp_cruise','dWTO_dnp_cruise','dWTO_dLD_cruise','dWTO_dR',
                          'dWTO_dCp_loiter','dWTO_dnp_loiter','dWTO_dLD_loiter'],
            'Value':[Wto,RR['Mff'],WF,RR['WFu'],Wpl,WE,WOE,Wcrew,Wtfo,
                     RR['WEa'],RR['diff'],
                     S['dCpR'],S['dnpR'],S['dLDR'],S['dR'],
                     S['dCpE'],S['dnpE'],S['dLDE']],
            'Units':['lbs','—','lbs','lbs','lbs','lbs','lbs','lbs','lbs','lbs','lbs',
                     'lbs/(lbs/hp/hr)','lbs','lbs','lbs/nm',
                     'lbs/(lbs/hp/hr)','lbs','lbs'],
        }
        b=io.StringIO(); pd.DataFrame(rows).to_csv(b,index=False)
        st.download_button("⬇  Download Full Results (CSV)",b.getvalue(),
                           "aerosizer_results.csv","text/csv",use_container_width=True)
        st.markdown("<br>",unsafe_allow_html=True)
        b2=io.StringIO()
        pd.DataFrame({'Phase':list(RR['fracs'].keys()),
                       'Wi/Wi-1':list(RR['fracs'].values()),
                       'Ref':['T2.1','T2.1','T2.1','Fig2.2','Eq2.9','Eq2.11','T2.1','T2.1']
                       }).to_csv(b2,index=False)
        st.download_button("⬇  Download Phase Fractions (CSV)",b2.getvalue(),
                           "aerosizer_fractions.csv","text/csv",use_container_width=True)
        st.markdown('</div>',unsafe_allow_html=True)

        st.markdown('<div class="card"><div class="card-title">Active Configuration Snapshot</div>', unsafe_allow_html=True)
        st.dataframe(pd.DataFrame({
            'Parameter':list(P.keys()),
            'Value':[str(v) for v in P.values()]}),
            hide_index=True,use_container_width=True)
        st.markdown('</div>',unsafe_allow_html=True)

    with e2:
        st.markdown('<div class="card"><div class="card-title">Export — Formal Engineering Report (PDF / A4)</div>', unsafe_allow_html=True)
        st.markdown("""
<div style="font-size:.82rem;color:#374151;line-height:1.8">
The PDF report includes:<br>
&nbsp;① &nbsp;Tool description &amp; methodology summary<br>
&nbsp;② &nbsp;All mission inputs and configuration<br>
&nbsp;③ &nbsp;Sizing convergence verification<br>
&nbsp;④ &nbsp;Complete weight statement (8 components)<br>
&nbsp;⑤ &nbsp;Phase weight fractions with equation references<br>
&nbsp;⑥ &nbsp;Breguet sensitivity partials (Table 2.20)<br>
&nbsp;⑦ &nbsp;Key design ratios<br>
&nbsp;⑧ &nbsp;Bibliography &amp; references
</div><br>
""",unsafe_allow_html=True)
        def make_pdf():
            buf=io.BytesIO()
            doc=SimpleDocTemplate(buf,pagesize=A4,
                leftMargin=2*cm,rightMargin=2*cm,topMargin=2*cm,bottomMargin=2*cm)
            PAGE_W = 17*cm  # usable width on A4
            sty=getSampleStyleSheet()
            def ps(nm,**kw): return ParagraphStyle(nm,parent=sty['Normal'],**kw)
            sT  =ps('T',fontSize=18,fontName='Helvetica-Bold',
                      textColor=colors.HexColor('#0D1B2A'),spaceAfter=2)
            sSub=ps('S',fontSize=8,textColor=colors.HexColor('#64748B'),spaceAfter=10)
            sH  =ps('H',fontSize=10,fontName='Helvetica-Bold',
                      textColor=colors.HexColor('#0369A1'),spaceBefore=12,spaceAfter=4)
            sB  =ps('B',fontSize=8,leading=12,textColor=colors.HexColor('#374151'))
            ts=TableStyle([
                ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#0D1B2A')),
                ('TEXTCOLOR',(0,0),(-1,0),colors.white),
                ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
                ('FONTNAME',(0,1),(-1,-1),'Helvetica'),
                ('FONTSIZE',(0,0),(-1,-1),7.5),
                ('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#CBD5E1')),
                ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#F8FAFC')]),
                ('LEFTPADDING',(0,0),(-1,-1),4),
                ('RIGHTPADDING',(0,0),(-1,-1),4),
                ('TOPPADDING',(0,0),(-1,-1),3),
                ('BOTTOMPADDING',(0,0),(-1,-1),3),
            ])
            story=[
                Paragraph("AeroSizer Pro — Mission Report",sT),
                Paragraph("Preliminary Aircraft Weight Estimation · Breguet Method · Propeller-Driven Aircraft",sSub),
                HRFlowable(width="100%",thickness=1.5,color=colors.HexColor('#38BDF8')),
                Spacer(1,.25*cm),
                Paragraph("1. Methodology",sH),
                Paragraph("Iterative Breguet weight fraction method (Raymer 2018, Ch.2). "
                          "W_TO is found by bisection where W_E_tentative = W_E_regression. "
                          "Mff = product of all phase fractions Wi/Wi-1. "
                          "Cruise (Eq.2.9) and loiter (Eq.2.11) fractions are computed from inputs. "
                          "Other phases use fixed values (Raymer Table 2.1). "
                          "Regression: log10(WE) = A + B*log10(WTO) (Raymer Table 2.2).",sB),
                Spacer(1,.15*cm),
                Paragraph("2. Mission Inputs",sH),
            ]
            # 4-column inputs table with equal widths
            CW4 = [4.0*cm, 2.5*cm, 4.0*cm, 2.5*cm]
            t1=Table([
                ['Parameter','Value','Parameter','Value'],
                ['Passengers',str(int(npax)),'Range (nm)',str(int(R_nm))],
                ['Pax wt (lbs)',str(int(wpax)),'Loiter endur. (hr)',f'{float(El):.2f}'],
                ['Baggage (lbs)',str(int(wbag)),'Cruise L/D',f'{float(LDc):.1f}'],
                ['Flight crew',str(int(ncrew)),'Loiter L/D',f'{float(LDl):.1f}'],
                ['Cabin att.',str(int(natt)),'Cruise Cp',f'{float(Cpc):.2f}'],
                ['A',f'{float(A_v):.4f}','Loiter Cp',f'{float(Cpl):.2f}'],
                ['B',f'{float(B_v):.4f}','Cruise eta_p',f'{float(npc):.2f}'],
                ['M_tfo',f'{float(Mtfo):.3f}','Loiter eta_p',f'{float(npl):.2f}']],
                colWidths=CW4)
            t1.setStyle(ts)
            story+=[t1,Spacer(1,.15*cm)]

            story.append(Paragraph("3. Sizing Result",sH))
            status_str='CONVERGED' if conv else 'NOT CONVERGED'
            story.append(Paragraph(
                f"W_TO = {Wto:,.0f} lbs   |   Mff = {RR['Mff']:.5f}   |   "
                f"dWE = {RR['diff']:+.1f} lbs   |   {status_str}",sB))
            story+=[Spacer(1,.12*cm)]

            story.append(Paragraph("4. Weight Statement",sH))
            CW4b = [8.0*cm, 2.5*cm, 2.5*cm, 2.5*cm]
            t2=Table([['Component','lbs','Fraction','% W_TO']]+
                list(zip(summary['Component'],summary['lbs'],
                          summary['Fraction'],summary['% W_TO'])),
                colWidths=CW4b)
            t2.setStyle(ts)
            story+=[t2,Spacer(1,.12*cm)]

            story.append(Paragraph("5. Phase Weight Fractions",sH))
            CW3 = [5.5*cm, 3*cm, 5*cm]
            t3=Table([['Phase','Wi / Wi-1','Reference']]+
                list(zip(list(RR['fracs'].keys()),
                          [f"{v:.5f}" for v in RR['fracs'].values()],
                          ['Raymer T2.1','Raymer T2.1','Raymer T2.1',
                           'Raymer Fig2.2','Breguet Eq2.9','Breguet Eq2.11',
                           'Raymer T2.1','Raymer T2.1'])),
                colWidths=CW3)
            t3.setStyle(ts)
            story+=[t3,Spacer(1,.12*cm)]

            story.append(Paragraph("6. Key Design Ratios",sH))
            CW3b = [7*cm, 3*cm, 4.5*cm]
            t_r=Table([['Ratio','Value','Typical Range'],
                ['W_PL / W_TO',f"{Wpl/Wto:.4f}",'0.10 – 0.25'],
                ['W_F / W_TO', f"{WF/Wto:.4f}", '0.20 – 0.45'],
                ['W_E / W_TO', f"{WE/Wto:.4f}", '0.45 – 0.65'],
                ['W_PL / W_E', f"{Wpl/WE:.4f}", '0.15 – 0.40']],
                colWidths=CW3b)
            t_r.setStyle(ts)
            story+=[t_r,Spacer(1,.12*cm)]

            story.append(Paragraph("7. Sensitivity Partials",sH))
            all_p=(list(zip(sdr['Partial'],sdr['Value'],sdr['Units'],sdr['Eq.']))+
                   list(zip(sdl['Partial'],sdl['Value'],sdl['Units'],sdl['Eq.'])))
            CW4c = [5*cm, 2.5*cm, 5*cm, 1.5*cm]
            t4=Table([['Partial','Value','Units','Eq.']]+all_p, colWidths=CW4c)
            t4.setStyle(ts)
            story+=[t4,Spacer(1,.12*cm)]

            story.append(Paragraph("8. References",sH))
            CW2 = [1.2*cm, PAGE_W-1.2*cm]
            refs_data=[
                ['[1]','Raymer, D.P. (2018). Aircraft Design: A Conceptual Approach, 6th Ed. AIAA.'],
                ['[2]','Roskam, J. (2003). Airplane Design, Part I. DAR Corporation.'],
                ['[3]','Breguet, L. (1923). Calcul du Poids de Combustible. Comptes Rendus.'],
                ['[4]','Nicolai & Carichner (2010). Fundamentals of Aircraft Design. AIAA.'],
            ]
            t5=Table([['Ref.','Citation']]+refs_data, colWidths=CW2)
            t5.setStyle(ts)
            story.append(t5)
            doc.build(story); buf.seek(0); return buf.read()
        st.download_button("⬇  Generate & Download PDF Report (A4)",
            make_pdf(),"aerosizer_pro_report.pdf","application/pdf",use_container_width=True)
        st.markdown('</div>',unsafe_allow_html=True)


# ═══════════════════════════════════════════════════
# TAB 5 — REFERENCES
# ═══════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="sec-lbl">Equations Used in This Tool</div>', unsafe_allow_html=True)

    eq_col1, eq_col2 = st.columns(2, gap="medium")
    with eq_col1:
        for code, title, eq, desc in [
            ("Eq. 2.9","Cruise Weight Fraction (Breguet Propeller)",
             "W5/W4 = 1 / exp[ R·Cp / (375·η_p·(L/D)) ]",
             "R in statute miles, Cp in lbs/hp/hr, η_p = propeller efficiency. "
             "This is the propeller-aircraft form of the Breguet range equation. "
             "Source: Raymer (2018) Eq. 2.9"),
            ("Eq. 2.11","Loiter Weight Fraction (Breguet Propeller Endurance)",
             "W6/W5 = 1 / exp[ E·Cp / (375·(1/V)·η_p·(L/D)) ]",
             "E in hours, V in mph, Cp in lbs/hp/hr. "
             "Computes fuel burned during the loiter/reserve segment. "
             "Source: Raymer (2018) Eq. 2.11"),
            ("Eq. 2.45","W_TO Range Sensitivity",
             "∂W_TO/∂R = F · Cp / (375·η_p·(L/D))",
             "Sensitivity of gross weight to design range change. "
             "F is the sizing multiplier (Eq. 2.44). "
             "Source: Raymer (2018) Eq. 2.45"),
        ]:
            st.markdown(f"""<div class="ref-item">
            <div class="ref-code">{code}</div>
            <div class="ref-title">{title}</div>
            <div style="font-family:DM Mono,monospace;font-size:.75rem;color:#1E40AF;
              background:#EFF8FF;padding:.35rem .7rem;border-radius:6px;margin:.3rem 0">{eq}</div>
            <div class="ref-desc">{desc}</div>
            </div>""", unsafe_allow_html=True)

    with eq_col2:
        for code, title, eq, desc in [
            ("Eq. 2.49","∂W_TO / ∂Cp (Cruise)",
             "∂W_TO/∂Cp = F·R / (375·η_p·(L/D))",
             "Sensitivity of W_TO to specific fuel consumption at cruise. "
             "Positive: increasing Cp increases gross weight. "
             "Source: Raymer (2018) Table 2.20 / Eq. 2.49"),
            ("Eq. 2.50","∂W_TO / ∂η_p (Cruise)",
             "∂W_TO/∂η_p = −F·R·Cp / (375·η_p²·(L/D))",
             "Sensitivity to propeller efficiency. Negative: better η_p reduces W_TO. "
             "This is why propeller design is critical in preliminary sizing. "
             "Source: Raymer (2018) Table 2.20 / Eq. 2.50"),
            ("Eq. 2.51","∂W_TO / ∂(L/D) (Cruise)",
             "∂W_TO/∂(L/D) = −F·R·Cp / (375·η_p·(L/D)²)",
             "Sensitivity to aerodynamic efficiency. Negative and usually the largest "
             "driver — improving L/D is the most effective way to reduce gross weight. "
             "Source: Raymer (2018) Table 2.20 / Eq. 2.51"),
        ]:
            st.markdown(f"""<div class="ref-item">
            <div class="ref-code">{code}</div>
            <div class="ref-title">{title}</div>
            <div style="font-family:DM Mono,monospace;font-size:.75rem;color:#1E40AF;
              background:#EFF8FF;padding:.35rem .7rem;border-radius:6px;margin:.3rem 0">{eq}</div>
            <div class="ref-desc">{desc}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sec-lbl">Bibliography</div>', unsafe_allow_html=True)

    for num, title, detail in [
        ("[1]","Raymer, D.P. — Aircraft Design: A Conceptual Approach, 6th Edition (2018)",
         "AIAA Education Series · Primary reference for all equations, weight fractions, "
         "and regression constants used in this tool. Ch. 2: Sizing from a Conceptual Sketch."),
        ("[2]","Roskam, J. — Airplane Design, Part I: Preliminary Sizing (2003)",
         "DAR Corporation, Lawrence, KS · Alternative methodology for empty-weight regression "
         "and mission analysis. Used for validation of regression constants."),
        ("[3]","Breguet, L. — Calcul du Poids de Combustible Consommé par un Avion (1923)",
         "Comptes Rendus de l'Académie des Sciences · Original derivation of the Breguet range "
         "and endurance equations. Foundation of modern aircraft fuel estimation."),
        ("[4]","Nicolai, L.M. & Carichner, G.E. — Fundamentals of Aircraft and Airship Design (2010)",
         "AIAA Education Series · Additional reference for preliminary sizing methods "
         "and validation of weight fraction estimates for transport aircraft."),
        ("[5]","MIL-HDBK-516C — Airworthiness Certification Criteria (2014)",
         "U.S. Department of Defense · Reference for weight definitions (W_OE, W_TO) "
         "and terminology used in this tool, consistent with FAA/EASA certification standards."),
    ]:
        st.markdown(f"""<div class="ref-item">
        <div class="ref-code">{num}</div>
        <div class="ref-title">{title}</div>
        <div class="ref-desc">{detail}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sec-lbl">Assumptions & Limitations</div>', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    limitations = [
        ("Propeller-driven aircraft only","The Breguet equations (Eq. 2.9, 2.11) in this form apply to propeller-driven aircraft only. For jet aircraft, use the specific range form with TSFC."),
        ("Historical regression constants","A and B are statistical fits to historical aircraft data. They are most accurate for turboprop transports in the 10,000–150,000 lbs range."),
        ("No structural / aerodynamic iteration","This tool performs only conceptual-level sizing. It does not compute structural weights, drag polars, or propulsion matching."),
        ("Fixed phase fractions","Engine start, taxi, takeoff, climb, descent, and landing use fixed values from Raymer Table 2.1. Real values depend on specific aircraft and operating conditions."),
        ("Reserve policy","Loiter segment represents FAR/ICAO reserve fuel. Actual reserve calculation may include divert distance not modeled here."),
    ]
    for title, desc in limitations:
        st.markdown(f"""
        <div style="margin-bottom:.7rem">
          <span style="font-family:DM Mono,monospace;font-size:.72rem;font-weight:500;
            color:#0369A1">▸ {title}</span>
          <div style="font-size:.78rem;color:#475569;margin-top:.2rem;line-height:1.6">{desc}</div>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
