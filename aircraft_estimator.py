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
                                 Table, TableStyle, HRFlowable)
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="AeroSizer Pro", page_icon="✈", layout="wide",
                   initial_sidebar_state="expanded")

# 2. Google Tag Manager
st.markdown("""
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-T8JSQMHD');</script>
""", unsafe_allow_html=True)

# 3. CSS
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');
:root {
  --bg:#0D1117; --sur:#161B22; --pan:#1C2333;
  --border:#30363D; --border2:#21262D;
  --blue:#1F6FEB; --blue2:#388BFD; --blue3:#58A6FF;
  --green:#3FB950; --amber:#E3B341; --red:#F85149;
  --purple:#BC8CFF;
  --text:#C9D1D9; --text2:#8B949E; --text3:#6E7681;
  --white:#F0F6FC;
}
*,*::before,*::after{box-sizing:border-box;}
html,body,[class*="css"]{background:var(--bg)!important;color:var(--text)!important;font-family:'Inter',sans-serif!important;}
.stApp{background:var(--bg)!important;}
.main .block-container{padding:1rem 1.5rem 2rem!important;max-width:100%!important;}
::-webkit-scrollbar{width:5px;height:5px;}
::-webkit-scrollbar-track{background:var(--bg);}
::-webkit-scrollbar-thumb{background:var(--border);border-radius:3px;}
::-webkit-scrollbar-thumb:hover{background:var(--blue);}

/* SIDEBAR */
[data-testid="stSidebar"]{background:var(--sur)!important;border-right:1px solid var(--border)!important;padding:0!important;}
[data-testid="stSidebar"]>div:first-child{padding:0!important;}
.sb-logo{padding:1.2rem 1.1rem 0.9rem;border-bottom:1px solid var(--border);background:linear-gradient(135deg,#0D1117,#161B22);margin-bottom:0;}
.sb-logo-title{font-family:'JetBrains Mono',monospace;font-size:1.1rem;font-weight:700;color:var(--white);letter-spacing:-0.02em;line-height:1;}
.sb-logo-title span{color:var(--blue2);}
.sb-logo-sub{font-family:'JetBrains Mono',monospace;font-size:0.56rem;letter-spacing:0.16em;text-transform:uppercase;color:var(--text3);margin-top:0.3rem;}
.sb-sec{font-family:'JetBrains Mono',monospace;font-size:0.60rem;font-weight:600;letter-spacing:0.16em;text-transform:uppercase;color:var(--blue3);padding:0.55rem 1.1rem 0.35rem;border-bottom:1px solid var(--border2);margin:0.35rem 0 0.45rem;display:flex;align-items:center;gap:0.45rem;}
.sb-sec::before{content:'';width:8px;height:1px;background:var(--blue2);flex-shrink:0;}
[data-testid="stSidebar"] label{font-family:'Inter',sans-serif!important;font-size:0.78rem!important;font-weight:500!important;color:var(--text)!important;}
[data-testid="stSidebar"] .stNumberInput input{background:var(--pan)!important;border:1px solid var(--border)!important;border-radius:6px!important;color:var(--white)!important;font-family:'JetBrains Mono',monospace!important;font-size:0.82rem!important;}
[data-testid="stSidebar"] .stNumberInput input:focus{border-color:var(--blue2)!important;box-shadow:0 0 0 2px rgba(31,111,235,0.25)!important;}
[data-testid="stSidebar"] div.stButton>button{background:linear-gradient(135deg,#1F6FEB,#388BFD)!important;color:#fff!important;border:none!important;border-radius:8px!important;font-size:0.82rem!important;font-weight:600!important;padding:0.6rem!important;width:100%!important;box-shadow:0 2px 10px rgba(31,111,235,0.35)!important;}
.sb-kpi{background:var(--pan);border:1px solid var(--border);border-radius:8px;padding:0.7rem 0.9rem;margin:0 0.65rem 0.5rem;}
.sb-kpi-val{font-family:'JetBrains Mono',monospace;font-size:1.45rem;font-weight:700;color:var(--blue3);line-height:1.1;}
.sb-kpi-lbl{font-size:0.62rem;letter-spacing:0.1em;text-transform:uppercase;color:var(--text3);margin-top:0.2rem;}
.conv-pill{display:inline-flex;align-items:center;gap:0.38rem;border-radius:20px;padding:0.22rem 0.72rem;font-family:'JetBrains Mono',monospace;font-size:0.65rem;font-weight:600;letter-spacing:0.05em;margin-top:0.5rem;}
.conv-ok{background:rgba(63,185,80,.15);border:1px solid rgba(63,185,80,.3);color:#3FB950;}
.conv-warn{background:rgba(248,81,73,.12);border:1px solid rgba(248,81,73,.3);color:#F85149;}

/* TABS */
.stTabs [data-baseweb="tab-list"]{background:var(--sur)!important;border:1px solid var(--border)!important;border-radius:10px!important;padding:4px!important;gap:3px!important;margin-bottom:1.1rem!important;}
.stTabs [data-baseweb="tab"]{border-radius:7px!important;font-family:'Inter',sans-serif!important;font-size:0.80rem!important;font-weight:500!important;color:var(--text2)!important;padding:0.42rem 1.1rem!important;transition:all 0.2s!important;}
.stTabs [aria-selected="true"]{background:linear-gradient(135deg,#1F6FEB,#388BFD)!important;color:#fff!important;font-weight:600!important;box-shadow:0 2px 8px rgba(31,111,235,0.4)!important;}

/* CARDS */
.card{background:var(--sur);border:1px solid var(--border);border-radius:10px;padding:1.1rem 1.25rem;margin-bottom:1rem;}
.card-blue{border-left:3px solid var(--blue2);border-radius:0 10px 10px 0;}
.card-green{border-left:3px solid var(--green);border-radius:0 10px 10px 0;}
.card-amber{border-left:3px solid var(--amber);border-radius:0 10px 10px 0;}
.card-red{border-left:3px solid var(--red);border-radius:0 10px 10px 0;}
.card-title{font-family:'JetBrains Mono',monospace;font-size:0.60rem;font-weight:600;letter-spacing:0.15em;text-transform:uppercase;color:var(--blue3);padding-bottom:0.5rem;border-bottom:1px solid var(--border2);margin-bottom:0.75rem;display:flex;align-items:center;gap:0.5rem;}
.card-title::before{content:'';width:8px;height:1px;background:var(--blue2);flex-shrink:0;}

/* EQUATION */
.eq-box{background:rgba(31,111,235,.08);border:1px solid rgba(31,111,235,.22);border-radius:7px;padding:0.42rem 0.9rem;font-family:'JetBrains Mono',monospace;font-size:0.79rem;color:var(--blue3);display:block;margin-bottom:0.45rem;white-space:nowrap;overflow-x:auto;}

/* PILLS */
.rpill{display:inline-flex;align-items:baseline;gap:0.25rem;border-radius:6px;padding:0.2rem 0.7rem;font-family:'JetBrains Mono',monospace;font-size:0.85rem;font-weight:700;margin-right:0.4rem;margin-top:0.3rem;}
.rpill-blue{background:rgba(31,111,235,.12);border:1px solid rgba(56,139,253,.3);color:var(--blue3);}
.rpill-green{background:rgba(63,185,80,.1);border:1px solid rgba(63,185,80,.28);color:var(--green);}
.rpill-warn{background:rgba(227,179,65,.1);border:1px solid rgba(227,179,65,.28);color:var(--amber);}
.rpill-red{background:rgba(248,81,73,.1);border:1px solid rgba(248,81,73,.28);color:var(--red);}
.rpill-unit{font-size:0.64rem;font-weight:400;opacity:0.65;}

/* PHASE ROWS */
.ph-row{display:grid;grid-template-columns:140px 90px 70px 90px 1fr;gap:0.5rem;align-items:center;padding:0.38rem 0;border-bottom:1px solid var(--border2);font-size:0.80rem;}
.ph-row:last-child{border-bottom:none;}
.ph-name{font-weight:500;color:var(--text);}
.ph-frac{font-family:'JetBrains Mono',monospace;font-weight:600;}
.ph-frac-fixed{color:var(--blue3);}
.ph-frac-breguet{color:var(--green);}
.ph-badge{font-size:0.62rem;font-weight:600;letter-spacing:0.06em;text-transform:uppercase;padding:0.1rem 0.48rem;border-radius:4px;width:fit-content;}
.ph-badge-fixed{background:rgba(31,111,235,.1);color:var(--blue3);border:1px solid rgba(31,111,235,.22);}
.ph-badge-breguet{background:rgba(63,185,80,.1);color:var(--green);border:1px solid rgba(63,185,80,.22);}
.ph-src{font-size:0.67rem;color:var(--text3);font-family:'JetBrains Mono',monospace;}

/* SENSITIVITY */
.sens-row{display:grid;grid-template-columns:200px 105px 150px 65px;gap:0.5rem;align-items:center;padding:0.35rem 0;border-bottom:1px solid var(--border2);}
.sens-row:last-child{border-bottom:none;}
.sens-partial{font-family:'JetBrains Mono',monospace;font-size:0.78rem;color:var(--text);}
.sens-pos{font-family:'JetBrains Mono',monospace;font-size:0.82rem;font-weight:700;color:var(--red);}
.sens-neg{font-family:'JetBrains Mono',monospace;font-size:0.82rem;font-weight:700;color:var(--green);}
.sens-unit{font-size:0.66rem;color:var(--text3);}
.sens-eq{font-size:0.64rem;color:var(--blue3);font-family:'JetBrains Mono',monospace;}

/* STATUS */
.status-ok{background:rgba(63,185,80,.08);border:1px solid rgba(63,185,80,.2);border-left:3px solid var(--green);border-radius:0 8px 8px 0;padding:0.52rem 1.1rem;margin-bottom:1rem;font-family:'JetBrains Mono',monospace;font-size:0.78rem;color:var(--green);}
.status-err{background:rgba(248,81,73,.07);border:1px solid rgba(248,81,73,.2);border-left:3px solid var(--red);border-radius:0 8px 8px 0;padding:0.52rem 1.1rem;margin-bottom:1rem;font-family:'JetBrains Mono',monospace;font-size:0.78rem;color:var(--red);}

/* DATAFRAME */
[data-testid="stDataFrame"]{border:1px solid var(--border)!important;border-radius:8px!important;}
[data-testid="stDataFrame"] thead th{background:var(--pan)!important;color:var(--blue3)!important;font-family:'JetBrains Mono',monospace!important;font-size:0.72rem!important;font-weight:600!important;letter-spacing:0.06em!important;border-bottom:1px solid var(--blue2)!important;}
[data-testid="stDataFrame"] tbody td{font-family:'JetBrains Mono',monospace!important;font-size:0.78rem!important;color:var(--text)!important;border-color:var(--border2)!important;padding:0.42rem 0.7rem!important;}
[data-testid="stDataFrame"] tbody tr:nth-child(even) td{background:rgba(255,255,255,.02)!important;}
[data-testid="stDataFrame"] tbody tr:hover td{background:rgba(31,111,235,.06)!important;}

/* DOWNLOAD */
div.stDownloadButton>button{background:var(--pan)!important;color:var(--blue3)!important;border:1px solid var(--border)!important;border-radius:7px!important;font-size:0.79rem!important;font-weight:500!important;padding:0.5rem 1rem!important;width:100%!important;}
div.stDownloadButton>button:hover{border-color:var(--blue2)!important;color:var(--white)!important;background:rgba(31,111,235,.12)!important;}

/* KPI */
.kpi-card{background:var(--sur);border:1px solid var(--border);border-radius:10px;padding:0.95rem 1rem;border-top:2px solid var(--blue2);}
.kpi-card.primary{border-top-color:var(--blue3);background:rgba(31,111,235,.06);}
.kpi-card.green{border-top-color:var(--green);}
.kpi-card.amber{border-top-color:var(--amber);}
.kpi-val{font-family:'JetBrains Mono',monospace;font-size:1.5rem;font-weight:700;color:var(--white);line-height:1.1;}
.kpi-val.primary{color:var(--blue3);font-size:1.65rem;}
.kpi-unit{font-size:0.66rem;font-weight:400;color:var(--text3);margin-left:2px;}
.kpi-lbl{font-size:0.60rem;letter-spacing:0.09em;text-transform:uppercase;color:var(--text3);margin-top:0.28rem;font-weight:500;}

/* SECTION DIVIDER */
.sec-div{font-family:'JetBrains Mono',monospace;font-size:0.62rem;font-weight:600;letter-spacing:0.14em;text-transform:uppercase;color:var(--blue3);border-bottom:1px solid var(--border);padding-bottom:0.4rem;margin:0.6rem 0 0.75rem;display:flex;align-items:center;gap:0.5rem;}
.sec-div::before{content:'';width:8px;height:1px;background:var(--blue2);flex-shrink:0;}

/* HEADER */
.main-header{background:var(--sur);border:1px solid var(--border);border-radius:10px;border-left:4px solid var(--blue2);padding:0.8rem 1.4rem;margin-bottom:1rem;display:flex;align-items:center;justify-content:space-between;}
.mh-title{font-family:'JetBrains Mono',monospace;font-size:1.35rem;font-weight:700;color:var(--white);letter-spacing:-0.02em;line-height:1;}
.mh-title span{color:var(--blue3);}
.mh-sub{font-size:0.68rem;color:var(--text3);margin-top:0.2rem;letter-spacing:0.04em;}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ── PHYSICS ──
def compute_mission(p):
    Wpl   = p['npax']*(p['wpax']+p['wbag'])
    Wcrew = (p['ncrew'] + p['natt']) * 205
    Wtfo  = p['Wto']*p['Mtfo']
    Rc    = p['R']*1.15078
    Vm    = p['Vl']*1.15078
    W5    = 1.0/math.exp(Rc/(375.0*(p['npc']/p['Cpc'])*p['LDc']))
    W6    = 1.0/math.exp(p['El']/(375.0*(1.0/Vm)*(p['npl']/p['Cpl'])*p['LDl']))
    phases = {
        'Engine Start':(0.990,'Fixed','T2.1'),
        'Taxi':        (0.995,'Fixed','T2.1'),
        'Takeoff':     (0.995,'Fixed','T2.1'),
        'Climb':       (0.985,'Fixed','Fig2.2'),
        'Cruise':      (W5,'Breguet','Eq2.9'),
        'Loiter':      (W6,'Breguet','Eq2.11'),
        'Descent':     (0.985,'Fixed','T2.1'),
        'Landing':     (0.995,'Fixed','T2.1'),
    }
    Mff=1.0
    for v,_,_ in phases.values(): Mff*=v
    WFu  = p['Wto']*(1.0-Mff)
    WF   = WFu + p['Wto']*p['Mr']*(1.0-Mff)
    WOE  = p['Wto'] - WF - Wpl
    WE   = WOE - Wtfo - Wcrew
    WEa  = 10.0**((math.log10(p['Wto'])-p['A'])/p['B'])
    return dict(Wpl=Wpl,Wcrew=Wcrew,Wtfo=Wtfo,Mff=Mff,
                WF=WF,WFu=WFu,WOE=WOE,WE=WE,WEa=WEa,
                diff=WEa-WE,phases=phases,Rc=Rc,Vm=Vm)

def solve_Wto(p, tol=0.5, n=500):
    pp = dict(p)
    guess = float(p.get('Wto', 48550))
    lo_bound = max(5000, int(guess * 0.3))
    hi_bound = min(600000, int(guess * 3.5))
    step = max(500, int((hi_bound - lo_bound) / 300))
    lo, hi = None, None
    prev_d, prev_w = None, None
    for w in range(lo_bound, hi_bound + step, step):
        pp['Wto'] = float(w)
        d = compute_mission(pp)['diff']
        if prev_d is not None and prev_d * d <= 0:
            lo, hi = float(prev_w), float(w)
            break
        prev_d, prev_w = d, w
    if lo is None:
        prev_d, prev_w = None, None
        for w in range(5000, 600001, 1000):
            pp['Wto'] = float(w)
            d = compute_mission(pp)['diff']
            if prev_d is not None and prev_d * d <= 0:
                lo, hi = float(prev_w), float(w)
                break
            prev_d, prev_w = d, w
    if lo is None:
        pp['Wto'] = guess
        return guess, compute_mission(pp)
    for _ in range(n):
        m = (lo + hi) / 2.0
        pp['Wto'] = m
        r = compute_mission(pp)
        if abs(r['diff']) < tol: return m, r
        if r['diff'] > 0: lo = m
        else: hi=m
    return m,compute_mission(pp)

def sensitivity(p,Wto):
    RR=compute_mission({**p,'Wto':Wto})
    Mff=RR['Mff']; Rc=RR['Rc']; Vm=RR['Vm']
    Wpl=RR['Wpl']; Wcrew=RR['Wcrew']
    C=1.0-(1.0+p['Mr'])*(1.0-Mff)-p['Mtfo']
    D=Wpl+Wcrew
    dn=C*Wto*(1.0-p['B'])-D
    F=(-p['B']*Wto**2*(1.0+p['Mr'])*Mff)/dn if abs(dn)>1e-6 else 0.0
    E=p['El']
    return dict(C=C,D=D,F=F,
        dCpR=F*Rc/(375.0*p['npc']*p['LDc']),
        dnpR=-F*Rc*p['Cpc']/(375.0*p['npc']**2*p['LDc']),
        dLDR=-F*Rc*p['Cpc']/(375.0*p['npc']*p['LDc']**2),
        dR=F*p['Cpc']/(375.0*p['npc']*p['LDc']),
        dCpE=F*E*Vm/(375.0*p['npl']*p['LDl']),
        dnpE=-F*E*Vm*p['Cpl']/(375.0*p['npl']**2*p['LDl']),
        dLDE=-F*E*Vm*p['Cpl']/(375.0*p['npl']*p['LDl']**2))

# ── SIDEBAR ──
with st.sidebar:
    st.markdown('<div class="sb-logo"><div class="sb-logo-title">AERO<span>SIZER</span></div><div class="sb-logo-sub">Raymer Ch.2 — Propeller Weight Estimation</div></div>',unsafe_allow_html=True)
    st.markdown('<div class="sb-sec">① Cabin & Crew</div>',unsafe_allow_html=True)
    npax = st.number_input("Passengers", 1, 400, 34, step=1)
    wpax = st.number_input("Pax body weight (lbs)", 100,300, 175, step=5)
    wbag = st.number_input("Baggage weight (lbs)", 0, 100, 30, step=5)
    ncrew = st.number_input("Flight crew (pilots)", 1, 6, 2, step=1)
    natt = st.number_input("Cabin attendants", 0, 10, 1, step=1)
    st.markdown('<div class="sb-sec">② Cruise Segment</div>',unsafe_allow_html=True)
    R_nm = st.number_input("Design range (nm)", 100,6000,1100,step=50)
    LDc = st.number_input("Cruise L/D", 4.0,30.0,13.0,step=0.5,format="%.1f")
    Cpc = st.number_input("Cruise SFC Cp (lbs/hp/hr)", 0.20,1.20,0.60,step=0.01,format="%.2f")
    npc = st.number_input("Cruise η_p", 0.30,0.98,0.85,step=0.01,format="%.2f")
    st.markdown('<div class="sb-sec">③ Loiter / Reserve</div>',unsafe_allow_html=True)
    El = st.number_input("Loiter endurance E (hr)", 0.10,6.0,0.75,step=0.05,format="%.2f")
    Vl = st.number_input("Loiter speed (kts)", 60, 400,250, step=5)
    LDl = st.number_input("Loiter L/D", 4.0,30.0,16.0,step=0.5,format="%.1f")
    Cpl = st.number_input("Loiter SFC Cp (lbs/hp/hr)",0.20,1.20,0.65,step=0.01,format="%.2f")
    npl = st.number_input("Loiter η_p", 0.30,0.98,0.77,step=0.01,format="%.2f")
    st.markdown('<div class="sb-sec">④ Regression Constants (T2.2)</div>',unsafe_allow_html=True)
    A_v = st.number_input("A (Table 2.15)", 0.0,2.0,0.3774,step=0.0001,format="%.4f")
    B_v = st.number_input("B (Table 2.2/2.15)", 0.1,2.0,0.9647,step=0.0001,format="%.4f")
    st.markdown('<div class="sb-sec">⑤ Fuel Allowances & W_TO Guess</div>',unsafe_allow_html=True)
    Mtfo = st.number_input("M_tfo (trapped fuel)", 0.000,0.05,0.005,step=0.001,format="%.3f")
    Mres = st.number_input("M_res (reserve ratio)", 0.000,0.10,0.000,step=0.001,format="%.3f")
    Wto_g = st.number_input("W_TO initial guess (lbs)",5000,500000,48550,step=1000)
    st.markdown("<br>",unsafe_allow_html=True)
    calc = st.button("⟳ Run Sizing",use_container_width=True)

P = dict(npax=int(npax),wpax=float(wpax),wbag=float(wbag),
         ncrew=int(ncrew),natt=int(natt),Mtfo=float(Mtfo),Mr=float(Mres),
         R=float(R_nm),Vl=float(Vl),LDc=float(LDc),Cpc=float(Cpc),npc=float(npc),
         El=float(El),LDl=float(LDl),Cpl=float(Cpl),npl=float(npl),
         A=float(A_v),B=float(B_v),Wto=float(Wto_g))

P_key = str(sorted(P.items()))
if 'res' not in st.session_state or st.session_state.get('_key') != P_key or calc:
    Wto, RR = solve_Wto(P)
    S = sensitivity(P, Wto)
    st.session_state['res'] = (Wto, RR, S)
    st.session_state['_key'] = P_key
else:
    Wto, RR, S = st.session_state['res']

conv=abs(RR['diff'])<1.0
WE=RR['WE']; WOE=RR['WOE']; WF=RR['WF']
Wpl=RR['Wpl']; Wcrew=RR['Wcrew']; Wtfo_r=RR['Wtfo']

with st.sidebar:
    st.markdown('<div class="sb-sec">◉ Live Results</div>',unsafe_allow_html=True)
    c_cls="conv-ok" if conv else "conv-warn"
    c_txt="✓ CONVERGED" if conv else "⚠ NOT CONVERGED"
    delta_c='#3FB950' if conv else '#F85149'
    st.markdown(f"""
    <div style="padding:0 0.65rem">
      <div class="sb-kpi">
        <div class="sb-kpi-val">{Wto:,.0f} <span style="font-size:0.75rem;font-weight:400;color:#6E7681">lbs</span></div>
        <div class="sb-kpi-lbl">W_TO · Gross Takeoff Weight</div>
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.4rem;margin:0 0 0.5rem">
        <div class="sb-kpi" style="padding:0.5rem 0.7rem">
          <div style="font-family:'JetBrains Mono',monospace;font-size:1.0rem;font-weight:700;color:#C9D1D9">{RR['Mff']:.4f}</div>
          <div class="sb-kpi-lbl">Mff</div>
        </div>
        <div class="sb-kpi" style="padding:0.5rem 0.7rem">
          <div style="font-family:'JetBrains Mono',monospace;font-size:1.0rem;font-weight:700;color:{delta_c}">{RR['diff']:+.2f}</div>
          <div class="sb-kpi-lbl">ΔW_E (lbs)</div>
        </div>
      </div>
      <div class="conv-pill {c_cls}">{c_txt}</div>
    </div>""",unsafe_allow_html=True)

# ── HEADER ──
badge_c='#3FB950' if conv else '#F85149'
badge_b='rgba(63,185,80,.12)' if conv else 'rgba(248,81,73,.1)'
badge_t='✓ Converged' if conv else '⚠ Not Converged'
st.markdown(f"""
<div class="main-header">
  <div>
    <div class="mh-title">AERO<span>SIZER</span> <span style="font-size:0.9rem;font-weight:400;color:#8B949E">Pro</span></div>
    <div class="mh-sub">&nbsp;</div>
  </div>
  <div style="display:flex;align-items:center;gap:1rem">
    <div style="text-align:right">
      <div style="font-family:'JetBrains Mono',monospace;font-size:1.35rem;font-weight:700;color:#58A6FF">{Wto:,.0f} <span style="font-size:0.72rem;color:#6E7681">lbs</span></div>
      <div style="font-size:0.62rem;letter-spacing:0.08em;text-transform:uppercase;color:#6E7681">W_TO</div>
    </div>
    <div style="background:{badge_b};color:{badge_c};border:1px solid {badge_c}44;font-family:'JetBrains Mono',monospace;font-size:0.68rem;font-weight:600;padding:0.28rem 0.88rem;border-radius:20px;letter-spacing:0.06em">{badge_t}</div>
  </div>
</div>""",unsafe_allow_html=True)

if conv:
    st.markdown(f'<div class="status-ok">✓ &nbsp; W_TO={Wto:,.1f} lbs &nbsp;·&nbsp; Mff={RR["Mff"]:.6f} &nbsp;·&nbsp; W_E_tent={WE:,.1f} lbs &nbsp;·&nbsp; W_E_allow={RR["WEa"]:,.1f} lbs &nbsp;·&nbsp; ΔW_E={RR["diff"]:+.2f} lbs</div>',unsafe_allow_html=True)
else:
    st.markdown(f'<div class="status-err">⚠ &nbsp; Not converged — ΔW_E={RR["diff"]:+.0f} lbs. Adjust A, B constants or inputs.</div>',unsafe_allow_html=True)

kpis=[(f"{Wto:,.0f}","lbs","W_TO Gross Takeoff","primary"),
      (f"{RR['Mff']:.5f}","","Mff Fuel Fraction",""),
      (f"{WF:,.0f}","lbs","W_F Total Fuel","amber"),
      (f"{Wpl:,.0f}","lbs","W_PL Payload","green"),
      (f"{WE:,.0f}","lbs","W_E Empty Weight","")]
cols=st.columns(5)
for col,(val,unit,lbl,cls) in zip(cols,kpis):
    with col:
        vc="primary" if cls=="primary" else ""
        st.markdown(f'<div class="kpi-card {cls}"><div class="kpi-val {vc}">{val}<span class="kpi-unit">{unit}</span></div><div class="kpi-lbl">{lbl}</div></div>',unsafe_allow_html=True)

st.markdown("<br>",unsafe_allow_html=True)
tab1,tab2,tab3,tab4,tab5=st.tabs([" ✦ Sizing Steps "," ∂ Sensitivity "," ◎ Charts "," ⬇ Export "," ⊕ References "])

# ═══ TAB 1 ═══
with tab1:
    col_l,col_r=st.columns([3,2],gap="medium")
    with col_l:
        pax_wt=int(npax)*(int(wpax)+int(wbag))
        crew_wt=int(ncrew)*205; att_wt=int(natt)*200
        st.markdown(f"""
        <div class="card card-blue">
          <div class="card-title">Step 1 — Payload & Crew Weights</div>
          <div class="ph-row" style="grid-template-columns:180px 95px 1fr">
            <span class="ph-name">{npax} pax × ({int(wpax)}+{int(wbag)}) lbs</span>
            <span class="ph-frac ph-frac-fixed">{pax_wt:,} lbs</span>
            <span class="ph-src">cabin payload</span>
          </div>
          <div class="ph-row" style="grid-template-columns:180px 95px 1fr">
            <span class="ph-name">{ncrew} pilots × 205 lbs</span>
            <span class="ph-frac ph-frac-fixed">{crew_wt:,} lbs</span>
            <span class="ph-src">flight crew</span>
          </div>
          <div class="ph-row" style="grid-template-columns:180px 95px 1fr">
            <span class="ph-name">{natt} attendant × 200 lbs</span>
            <span class="ph-frac ph-frac-fixed">{att_wt:,} lbs</span>
            <span class="ph-src">cabin crew</span>
          </div>
          <div style="margin-top:0.6rem">
            <span class="rpill rpill-blue">W_PL = {Wpl:,.0f} <span class="rpill-unit">lbs</span></span>
            <span class="rpill rpill-blue">W_crew = {Wcrew:,.0f} <span class="rpill-unit">lbs</span></span>
          </div>
        </div>""",unsafe_allow_html=True)
        st.markdown(f"""
        <div class="card card-blue">
          <div class="card-title">Step 2 — Unit Conversions</div>
          <div class="ph-row" style="grid-template-columns:200px 110px 1fr">
            <span class="ph-name">R_cruise (statute miles)</span>
            <span class="ph-frac ph-frac-fixed">{RR['Rc']:.3f}</span>
            <span class="ph-src">{R_nm} nm × 1.15078</span>
          </div>
          <div class="ph-row" style="grid-template-columns:200px 110px 1fr">
            <span class="ph-name">V_loiter (mph)</span>
            <span class="ph-frac ph-frac-fixed">{RR['Vm']:.2f}</span>
            <span class="ph-src">{Vl} kts × 1.15078</span>
          </div>
          <div class="ph-row" style="grid-template-columns:200px 110px 1fr">
            <span class="ph-name">W_tfo = M_tfo × W_TO</span>
            <span class="ph-frac ph-frac-fixed">{Wtfo_r:,.2f} lbs</span>
            <span class="ph-src">{Mtfo:.3f} × {Wto:,.0f}</span>
          </div>
        </div>""",unsafe_allow_html=True)
        st.markdown('<div class="card card-blue"><div class="card-title">Step 3 — Mission Phase Weight Fractions</div>',unsafe_allow_html=True)
        st.markdown("""<div style="display:grid;grid-template-columns:140px 90px 70px 90px 1fr;gap:0.5rem;padding:0.2rem 0 0.4rem;font-size:0.62rem;letter-spacing:0.08em;text-transform:uppercase;color:#6E7681;border-bottom:1px solid #30363D;font-weight:600"><span>Phase</span><span>Wᵢ/Wᵢ₋₁</span><span>Type</span><span>Source</span><span>Cumul. Mff</span></div>""",unsafe_allow_html=True)
        cum_mff=1.0
        for ph,(fv,ftype,fsrc) in RR['phases'].items():
            cum_mff*=fv
            fc='ph-frac-breguet' if ftype=='Breguet' else 'ph-frac-fixed'
            bc='ph-badge-breguet' if ftype=='Breguet' else 'ph-badge-fixed'
            st.markdown(f"""<div class="ph-row"><span class="ph-name">{ph}</span><span class="ph-frac {fc}">{fv:.5f}</span><span class="ph-badge {bc}">{ftype}</span><span class="ph-src">{fsrc}</span><span style="font-family:'JetBrains Mono',monospace;font-size:0.74rem;color:#8B949E">{cum_mff:.5f}</span></div>""",unsafe_allow_html=True)
        st.markdown(f"""<div style="margin-top:0.6rem;padding-top:0.5rem;border-top:1px solid #21262D"><span class="rpill rpill-green">Mff = {RR['Mff']:.6f}</span><span style="font-size:0.69rem;color:#6E7681;margin-left:0.4rem">(product of all 8 phase fractions)</span></div></div>""",unsafe_allow_html=True)
        ok_cls="rpill-green" if conv else "rpill-red"
        st.markdown(f"""
        <div class="card {'card-green' if conv else 'card-red'}">
          <div class="card-title">Steps 4–6 — Weight Build-Up & Convergence</div>
          <div style="display:grid;grid-template-columns:220px 130px 1fr;gap:0.5rem;font-size:0.62rem;letter-spacing:0.08em;text-transform:uppercase;color:#6E7681;padding-bottom:0.38rem;border-bottom:1px solid #30363D;font-weight:600"><span>Quantity</span><span>Value</span><span>Expression</span></div>
          <div class="ph-row" style="grid-template-columns:220px 130px 1fr"><span class="ph-name">Step 4a — W_F (total fuel)</span><span class="ph-frac ph-frac-fixed">{WF:,.1f} lbs</span><span class="ph-src">W_Fused + W_tfo</span></div>
          <div class="ph-row" style="grid-template-columns:220px 130px 1fr"><span class="ph-name">Step 4b — W_OE (tentative)</span><span class="ph-frac ph-frac-fixed">{WOE:,.1f} lbs</span><span class="ph-src">W_TO − W_F − W_PL</span></div>
          <div class="ph-row" style="grid-template-columns:220px 130px 1fr"><span class="ph-name">Step 5 — W_E (tentative)</span><span class="ph-frac ph-frac-fixed">{WE:,.2f} lbs</span><span class="ph-src">W_OE − W_tfo − W_crew</span></div>
          <div class="ph-row" style="grid-template-columns:220px 130px 1fr"><span class="ph-name">Step 6 — W_E (allowable)</span><span class="ph-frac ph-frac-fixed">{RR['WEa']:,.2f} lbs</span><span class="ph-src">10^[(log W_TO − A) / B]</span></div>
          <div style="margin-top:0.6rem">
            <span class="rpill {ok_cls}">ΔW_E = {RR['diff']:+.2f} <span class="rpill-unit">lbs</span></span>
            <span class="rpill {ok_cls}">{'✓ CONVERGED' if conv else '⚠ NOT CONVERGED'}</span>
          </div>
        </div>""",unsafe_allow_html=True)

    with col_r:
        st.markdown("""<div class="card card-blue"><div class="card-title">Key Equations — Raymer Ch.2</div><div style="font-size:0.73rem;color:#8B949E;margin-bottom:0.3rem;font-weight:500">Cruise fraction (Eq. 2.9)</div><div class="eq-box">W₅/W₄ = 1 / exp[ Rc / (375·η_p/Cp·L/D) ]</div><div style="font-size:0.73rem;color:#8B949E;margin:0.5rem 0 0.3rem;font-weight:500">Loiter fraction (Eq. 2.11)</div><div class="eq-box">W₆/W₅ = 1 / exp[ E / (375·(1/V)·η_p/Cp·L/D) ]</div><div style="font-size:0.73rem;color:#8B949E;margin:0.5rem 0 0.3rem;font-weight:500">Regression (Table 2.2 / 2.15)</div><div class="eq-box">log₁₀(W_E) = A + B · log₁₀(W_TO)</div><div style="font-size:0.67rem;color:#6E7681;margin-top:0.4rem;line-height:1.65">R in statute miles · Cp in lbs/hp/hr<br>V in mph · E in hours</div></div>""",unsafe_allow_html=True)
        df_sum=pd.DataFrame({
            'Symbol':['W_TO','Mff','W_F','W_Fused','W_tfo','W_OE','W_E_tent','W_E_allow','ΔW_E','W_PL','W_crew'],
            'Value':[f"{Wto:,.1f}",f"{RR['Mff']:.6f}",f"{WF:,.1f}",f"{RR['WFu']:,.1f}",f"{Wtfo_r:,.2f}",f"{WOE:,.1f}",f"{WE:,.2f}",f"{RR['WEa']:,.2f}",f"{RR['diff']:+.2f}",f"{Wpl:,.1f}",f"{Wcrew:,.1f}"],
            'Unit':['lbs','—','lbs','lbs','lbs','lbs','lbs','lbs','lbs','lbs','lbs']})
        st.dataframe(df_sum,hide_index=True,use_container_width=True,height=390)
        ratio_rows=[]
        for name,val_r,lo_r,hi_r in [('W_PL/W_TO',Wpl/Wto,0.10,0.25),('W_F/W_TO',WF/Wto,0.20,0.45),('W_E/W_TO',WE/Wto,0.45,0.65),('W_PL/W_E',Wpl/WE,0.15,0.40)]:
            ok_r=lo_r<=val_r<=hi_r
            ratio_rows.append({'Ratio':name,'Value':f'{val_r:.4f}','Typical':f'{lo_r:.2f}–{hi_r:.2f}','Status':'✓' if ok_r else ('▲' if val_r>hi_r else '▼')})
        st.dataframe(pd.DataFrame(ratio_rows),hide_index=True,use_container_width=True)

# ═══ TAB 2 ═══
with tab2:
    s1,s2=st.columns([1,1],gap="medium")
    with s1:
        st.markdown(f"""<div class="card card-blue"><div class="card-title">Intermediate Factors — Eq 2.22–2.44</div>
          <div class="sens-row" style="grid-template-columns:240px 1fr"><span class="sens-partial">C = 1−(1+M_res)(1−Mff)−M_tfo</span><span style="font-family:'JetBrains Mono',monospace;font-size:0.82rem;font-weight:700;color:#58A6FF">{S['C']:.5f} <span style="font-size:0.65rem;color:#6E7681">Eq 2.22</span></span></div>
          <div class="sens-row" style="grid-template-columns:240px 1fr"><span class="sens-partial">D = W_PL + W_crew</span><span style="font-family:'JetBrains Mono',monospace;font-size:0.82rem;font-weight:700;color:#58A6FF">{S['D']:,.0f} lbs <span style="font-size:0.65rem;color:#6E7681">Eq 2.23</span></span></div>
          <div class="sens-row" style="grid-template-columns:240px 1fr"><span class="sens-partial">C(1−B)W_TO − D</span><span style="font-family:'JetBrains Mono',monospace;font-size:0.82rem;font-weight:700;color:#E3B341">{S['C']*(1-float(B_v))*Wto-S['D']:,.0f}</span></div>
          <div class="sens-row" style="grid-template-columns:240px 1fr;border-bottom:none"><span class="sens-partial">F (sizing multiplier, Eq 2.44)</span><span style="font-family:'JetBrains Mono',monospace;font-size:0.82rem;font-weight:700;color:#BC8CFF">{S['F']:,.0f} lbs</span></div>
        </div>""",unsafe_allow_html=True)
        for partial,val,unit,eq in [('∂W_TO/∂Cp (cruise)',S['dCpR'],'lbs/(lbs/hp/hr)','Eq 2.49'),('∂W_TO/∂η_p (cruise)',S['dnpR'],'lbs','Eq 2.50'),('∂W_TO/∂(L/D) (cruise)',S['dLDR'],'lbs','Eq 2.51'),('∂W_TO/∂R',S['dR'],'lbs/nm','Eq 2.45')]:
            vc='sens-neg' if val<0 else 'sens-pos'
            st.markdown(f'<div class="sens-row"><span class="sens-partial">{partial}</span><span class="{vc}">{val:+,.1f}</span><span class="sens-unit">{unit}</span><span class="sens-eq">{eq}</span></div>',unsafe_allow_html=True)
    with s2:
        st.markdown(f'<div class="card card-amber"><div class="card-title">Range Trade Study</div><div style="font-size:0.8rem;color:#C9D1D9;line-height:1.7;margin-bottom:0.5rem">∂W_TO/∂R = <b style="color:#58A6FF">{S["dR"]:+.2f} lbs/nm</b></div>',unsafe_allow_html=True)
        for dr in [-200,-100,100,200]:
            dw=S['dR']*dr; col_v='#3FB950' if dw<0 else '#E3B341'
            st.markdown(f'<div style="display:flex;justify-content:space-between;align-items:center;padding:0.28rem 0;border-bottom:1px solid #21262D;font-size:0.8rem"><span style="color:#8B949E">ΔR = {dr:+d} nm</span><span style="font-family:JetBrains Mono,monospace;font-weight:700;color:{col_v}">{dw:+,.1f} lbs</span></div>',unsafe_allow_html=True)

# ═══ TAB 3 ═══
with tab3:
    st.markdown('<div class="sec-div">Mission Phase Weight Fractions</div>',unsafe_allow_html=True)
    phases_l=list(RR['phases'].keys())
    fvals=[v for v,_,_ in RR['phases'].values()]
    cum_p=[1.0]
    for fv in fvals: cum_p.append(cum_p[-1]*fv)
    fig_m=make_subplots(rows=1,cols=2,subplot_titles=["Wᵢ/Wᵢ₋₁ per phase","Cumulative Mff"])
    fig_m.add_trace(go.Bar(x=phases_l,y=fvals,marker_color='#388BFD'),row=1,col=1)
    fig_m.add_trace(go.Scatter(x=['Ramp']+phases_l,y=cum_p,mode='lines+markers',line=dict(color='#388BFD')),row=1,col=2)
    st.plotly_chart(fig_m,use_container_width=True)

# ═══ TAB 4 ═══
with tab4:
    ex1,ex2=st.columns([1,1],gap="medium")
    with ex1:
        rows={'Parameter':['W_TO','Mff','W_F','W_F_usable','W_tfo','W_OE','W_E_tent','W_E_allow','delta_WE','W_PL','W_crew','Rc_sm','Vm_mph','F','C','D'],
              'Value':[Wto,RR['Mff'],WF,RR['WFu'],Wtfo_r,WOE,WE,RR['WEa'],RR['diff'],Wpl,Wcrew,RR['Rc'],RR['Vm'],S['F'],S['C'],S['D']],
              'Units':['lbs','—','lbs','lbs','lbs','lbs','lbs','lbs','lbs','lbs','lbs','s.m.','mph','—','—','lbs']}
        b=io.StringIO(); pd.DataFrame(rows).to_csv(b,index=False)
        st.download_button("⬇ Full Results (CSV)",b.getvalue(),"aerosizer_hw28.csv","text/csv",use_container_width=True)
    with ex2:
        def make_pdf():
            buf=io.BytesIO()
            doc=SimpleDocTemplate(buf,pagesize=A4,leftMargin=2.0*cm,rightMargin=2.0*cm,topMargin=2.2*cm,bottomMargin=2.2*cm)
            PW=17.0*cm
            CN=colors.HexColor('#0D1B2A'); CB=colors.HexColor('#1F6FEB'); CS=colors.HexColor('#388BFD')
            CG=colors.HexColor('#475569'); CL=colors.HexColor('#94A3B8'); CR=colors.HexColor('#CBD5E1')
            CF=colors.HexColor('#F8FAFF'); CW=colors.white
            sty=getSampleStyleSheet()
            def ps(nm,**kw): return ParagraphStyle(nm,parent=sty['Normal'],**kw)
            sH1=ps('H1',fontSize=10,fontName='Helvetica-Bold',textColor=CB,spaceBefore=10,spaceAfter=4)
            sSUB=ps('SU',fontSize=8,textColor=CG,leading=12,spaceAfter=2)
            def ts(hdr=CN):
                return TableStyle([
                    ('BACKGROUND',(0,0),(-1,0),hdr),
                    ('TEXTCOLOR',(0,0),(-1,0),CW),
                    ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
                    ('FONTNAME',(0,1),(-1,-1),'Helvetica'),
                    ('FONTSIZE',(0,0),(-1,-1),7.5),
                    ('LEADING',(0,0),(-1,-1),11),
                    ('TEXTCOLOR',(0,1),(-1,-1),CG),
                    ('ROWBACKGROUNDS',(0,1),(-1,-1),[CW,CF]),
                    ('GRID',(0,0),(-1,-1),0.25,CR),
                    ('LINEBELOW',(0,0),(-1,0),0.8,CS),
                    ('LEFTPADDING',(0,0),(-1,-1),5),
                    ('RIGHTPADDING',(0,0),(-1,-1),5),
                    ('TOPPADDING',(0,0),(-1,-1),3.5),
                    ('BOTTOMPADDING',(0,0),(-1,-1),3.5),
                    ('VALIGN',(0,0),(-1,-1),'MIDDLE')
                ])
            story=[]
            hd=Table([[Paragraph('<b>AEROSIZER PRO</b>',ps('TX',fontSize=16,fontName='Helvetica-Bold',textColor=CN,leading=20)),
                       Paragraph('DOC: ASP-HW28 REV A<br/>STATUS: '+('RELEASED' if conv else 'DRAFT'),ps('TX2',fontSize=7,textColor=CL,leading=10,alignment=TA_RIGHT))]],colWidths=[PW*0.60,PW*0.40])
            story.append(hd)
            story.append(HRFlowable(width=PW,thickness=2.5,color=CB,spaceBefore=4,spaceAfter=2))
            story.append(Paragraph('Preliminary Aircraft Weight Sizing — Raymer (2018) Ch.2',sSUB))
            story.append(Paragraph('1 Mission Inputs',sH1))
            t_in=Table([['Parameter','Value','Parameter','Value'],['Passengers',str(int(npax)),'Design range (nm)',str(int(R_nm))],['Cruise L/D',f'{LDc:.1f}','Loiter L/D',f'{LDl:.1f}']],colWidths=[PW*0.3,PW*0.2,PW*0.3,PW*0.2])
            t_in.setStyle(ts()); story.append(t_in)
            story.append(Paragraph('2 Sizing Results',sH1))
            t_cv=Table([['Quantity','Value (lbs)'],['W_TO (Gross)',f'{Wto:,.2f}'],['W_F (Total)',f'{WF:,.2f}'],['W_E (Empty)',f'{WE:,.2f}']],colWidths=[PW*0.6,PW*0.4])
            t_cv.setStyle(ts(hdr=colors.HexColor('#334155'))); story.append(t_cv)
            doc.build(story); buf.seek(0); return buf.read()
        st.download_button("⬇ Generate & Download PDF (A4)",make_pdf(),"aerosizer_hw28_report.pdf","application/pdf",use_container_width=True)

# ═══ TAB 5 ═══
with tab5:
    for code,title,eq in [("Eq 2.9","Cruise — Breguet","W₅/W₄ = 1/exp[ Rc/(375·η_p/Cp·L/D) ]"),("Eq 2.11","Loiter — Breguet","W₆/W₅ = 1/exp[ E/(375·(1/V)·η_p/Cp·L/D) ]")]:
        st.markdown(f'<div class="card card-blue"><div class="card-title">{code} — {title}</div><div class="eq-box">{eq}</div></div>',unsafe_allow_html=True)
