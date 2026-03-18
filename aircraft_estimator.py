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

st.set_page_config(page_title="AeroSizer Pro", page_icon="✈", layout="wide",
                   initial_sidebar_state="expanded")

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
    Wpl   = p['npax']*(p['wpax']+p['wbag']) + p['ncrew']*205 + p['natt']*200
    Wcrew = p['ncrew']*205 + p['natt']*200
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
    WFu=p['Wto']*(1.0-Mff)
    WF =WFu+p['Wto']*p['Mr']*(1.0-Mff)+Wtfo
    WOE=p['Wto']-WF-Wpl
    WE =WOE-Wtfo-Wcrew
    WEa=10.0**((math.log10(p['Wto'])-p['A'])/p['B'])
    return dict(Wpl=Wpl,Wcrew=Wcrew,Wtfo=Wtfo,Mff=Mff,
                WF=WF,WFu=WFu,WOE=WOE,WE=WE,WEa=WEa,
                diff=WEa-WE,phases=phases,Rc=Rc,Vm=Vm)

def solve_Wto(p,tol=0.5,n=500):
    pp=dict(p); prev_d,prev_w,lo,hi=None,None,None,None
    for w in range(8000,600001,2000):
        pp['Wto']=float(w); d=compute_mission(pp)['diff']
        if prev_d is not None and prev_d*d<=0:
            lo,hi=float(prev_w),float(w); break
        prev_d,prev_w=d,w
    if lo is None:
        pp['Wto']=float(p.get('Wto',48550)); return float(p.get('Wto',48550)),compute_mission(pp)
    for _ in range(n):
        m=(lo+hi)/2.0; pp['Wto']=m; r=compute_mission(pp)
        if abs(r['diff'])<tol: return m,r
        if r['diff']>0: lo=m
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
    npax  = st.number_input("Passengers",            1,  400, 34,   step=1)
    wpax  = st.number_input("Pax body weight (lbs)", 100,300, 175,  step=5)
    wbag  = st.number_input("Baggage weight (lbs)",  0,  100, 30,   step=5)
    ncrew = st.number_input("Flight crew (pilots)",  1,  6,   2,    step=1)
    natt  = st.number_input("Cabin attendants",      0,  10,  1,    step=1)

    st.markdown('<div class="sb-sec">② Cruise Segment</div>',unsafe_allow_html=True)
    R_nm = st.number_input("Design range (nm)",         100,6000,1100,step=50)
    LDc  = st.number_input("Cruise L/D",                4.0,30.0,13.0,step=0.5,format="%.1f")
    Cpc  = st.number_input("Cruise SFC Cp (lbs/hp/hr)", 0.20,1.20,0.60,step=0.01,format="%.2f")
    npc  = st.number_input("Cruise η_p",                0.30,0.98,0.85,step=0.01,format="%.2f")

    st.markdown('<div class="sb-sec">③ Loiter / Reserve</div>',unsafe_allow_html=True)
    El   = st.number_input("Loiter endurance E (hr)",  0.10,6.0,0.75,step=0.05,format="%.2f")
    Vl   = st.number_input("Loiter speed (kts)",        60, 400,250, step=5)
    LDl  = st.number_input("Loiter L/D",               4.0,30.0,16.0,step=0.5,format="%.1f")
    Cpl  = st.number_input("Loiter SFC Cp (lbs/hp/hr)",0.20,1.20,0.65,step=0.01,format="%.2f")
    npl  = st.number_input("Loiter η_p",               0.30,0.98,0.77,step=0.01,format="%.2f")

    st.markdown('<div class="sb-sec">④ Regression Constants (T2.2)</div>',unsafe_allow_html=True)
    A_v  = st.number_input("A  (Table 2.15)",           0.0,2.0,0.3774,step=0.0001,format="%.4f")
    B_v  = st.number_input("B  (Table 2.2/2.15)",       0.1,2.0,0.9647,step=0.0001,format="%.4f")

    st.markdown('<div class="sb-sec">⑤ Fuel Allowances & W_TO Guess</div>',unsafe_allow_html=True)
    Mtfo  = st.number_input("M_tfo  (trapped fuel)",  0.000,0.05,0.005,step=0.001,format="%.3f")
    Mres  = st.number_input("M_res  (reserve ratio)", 0.000,0.10,0.000,step=0.001,format="%.3f")
    Wto_g = st.number_input("W_TO initial guess (lbs)",5000,500000,48550,step=1000)

    st.markdown("<br>",unsafe_allow_html=True)
    calc = st.button("⟳  Run Sizing",use_container_width=True)

P = dict(npax=int(npax),wpax=float(wpax),wbag=float(wbag),
         ncrew=int(ncrew),natt=int(natt),Mtfo=float(Mtfo),Mr=float(Mres),
         R=float(R_nm),Vl=float(Vl),LDc=float(LDc),Cpc=float(Cpc),npc=float(npc),
         El=float(El),LDl=float(LDl),Cpl=float(Cpl),npl=float(npl),
         A=float(A_v),B=float(B_v),Wto=float(Wto_g))

P_key=str(sorted({k:v for k,v in P.items() if k!='Wto'}.items()))
if 'res' not in st.session_state or st.session_state.get('_key')!=P_key or calc:
    Wto,RR=solve_Wto(P); S=sensitivity(P,Wto)
    st.session_state['res']=(Wto,RR,S); st.session_state['_key']=P_key
else:
    Wto,RR,S=st.session_state['res']

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
    <div class="mh-sub">Raymer Ch.2 · Breguet Range/Endurance · Propeller-Driven Aircraft · Problem 2.8</div>
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

kpis=[(f"{Wto:,.0f}","lbs","W_TO  Gross Takeoff","primary"),
      (f"{RR['Mff']:.5f}","","Mff  Fuel Fraction",""),
      (f"{WF:,.0f}","lbs","W_F  Total Fuel","amber"),
      (f"{Wpl:,.0f}","lbs","W_PL  Payload","green"),
      (f"{WE:,.0f}","lbs","W_E  Empty Weight","")]
cols=st.columns(5)
for col,(val,unit,lbl,cls) in zip(cols,kpis):
    with col:
        vc="primary" if cls=="primary" else ""
        st.markdown(f'<div class="kpi-card {cls}"><div class="kpi-val {vc}">{val}<span class="kpi-unit">{unit}</span></div><div class="kpi-lbl">{lbl}</div></div>',unsafe_allow_html=True)

st.markdown("<br>",unsafe_allow_html=True)

tab1,tab2,tab3,tab4,tab5=st.tabs([
    "  ✦ Sizing Steps  ","  ∂ Sensitivity  ","  ◎ Charts  ","  ⬇ Export  ","  ⊕ References  "
])

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

        st.markdown('<div class="card card-blue"><div class="card-title">Numeric Summary</div>',unsafe_allow_html=True)
        df_sum=pd.DataFrame({
            'Symbol':['W_TO','Mff','W_F','W_Fused','W_tfo','W_OE','W_E_tent','W_E_allow','ΔW_E','W_PL','W_crew'],
            'Value':[f"{Wto:,.1f}",f"{RR['Mff']:.6f}",f"{WF:,.1f}",f"{RR['WFu']:,.1f}",f"{Wtfo_r:,.2f}",f"{WOE:,.1f}",f"{WE:,.2f}",f"{RR['WEa']:,.2f}",f"{RR['diff']:+.2f}",f"{Wpl:,.1f}",f"{Wcrew:,.1f}"],
            'Unit':['lbs','—','lbs','lbs','lbs','lbs','lbs','lbs','lbs','lbs','lbs']})
        st.dataframe(df_sum,hide_index=True,use_container_width=True,height=390)
        st.markdown('</div>',unsafe_allow_html=True)

        st.markdown('<div class="card card-blue"><div class="card-title">Key Design Ratios</div>',unsafe_allow_html=True)
        ratio_rows=[]
        for name,val_r,lo_r,hi_r in [('W_PL/W_TO',Wpl/Wto,0.10,0.25),('W_F/W_TO',WF/Wto,0.20,0.45),('W_E/W_TO',WE/Wto,0.45,0.65),('W_PL/W_E',Wpl/WE,0.15,0.40)]:
            ok_r=lo_r<=val_r<=hi_r
            ratio_rows.append({'Ratio':name,'Value':f'{val_r:.4f}','Typical':f'{lo_r:.2f}–{hi_r:.2f}','Status':'✓' if ok_r else ('▲' if val_r>hi_r else '▼')})
        st.dataframe(pd.DataFrame(ratio_rows),hide_index=True,use_container_width=True)
        st.markdown('</div>',unsafe_allow_html=True)

# ═══ TAB 2 ═══
with tab2:
    s1,s2=st.columns([1,1],gap="medium")
    with s1:
        st.markdown(f"""<div class="card card-blue"><div class="card-title">Intermediate Factors — Eq 2.22–2.44</div>
          <div class="sens-row" style="grid-template-columns:240px 1fr"><span class="sens-partial">C = 1−(1+M_res)(1−Mff)−M_tfo</span><span style="font-family:'JetBrains Mono',monospace;font-size:0.82rem;font-weight:700;color:#58A6FF">{S['C']:.5f} <span style="font-size:0.65rem;color:#6E7681">Eq 2.22</span></span></div>
          <div class="sens-row" style="grid-template-columns:240px 1fr"><span class="sens-partial">D = W_PL + W_crew</span><span style="font-family:'JetBrains Mono',monospace;font-size:0.82rem;font-weight:700;color:#58A6FF">{S['D']:,.0f} lbs <span style="font-size:0.65rem;color:#6E7681">Eq 2.23</span></span></div>
          <div class="sens-row" style="grid-template-columns:240px 1fr"><span class="sens-partial">C(1−B)W_TO − D</span><span style="font-family:'JetBrains Mono',monospace;font-size:0.82rem;font-weight:700;color:#E3B341">{S['C']*(1-float(B_v))*Wto-S['D']:,.0f}</span></div>
          <div class="sens-row" style="grid-template-columns:240px 1fr;border-bottom:none"><span class="sens-partial">F  (sizing multiplier, Eq 2.44)</span><span style="font-family:'JetBrains Mono',monospace;font-size:0.82rem;font-weight:700;color:#BC8CFF">{S['F']:,.0f} lbs</span></div>
        </div>""",unsafe_allow_html=True)

        st.markdown('<div class="card card-amber"><div class="card-title">Range Phase — Breguet Partials (Table 2.20)</div>',unsafe_allow_html=True)
        st.markdown("""<div style="display:grid;grid-template-columns:200px 105px 155px 70px;gap:0.5rem;font-size:0.60rem;letter-spacing:0.08em;text-transform:uppercase;color:#6E7681;padding-bottom:0.35rem;border-bottom:1px solid #30363D;font-weight:600"><span>Partial</span><span>Value</span><span>Units</span><span>Ref.</span></div>""",unsafe_allow_html=True)
        for partial,val,unit,eq in [('∂W_TO/∂Cp (cruise)',S['dCpR'],'lbs/(lbs/hp/hr)','Eq 2.49'),('∂W_TO/∂η_p (cruise)',S['dnpR'],'lbs','Eq 2.50'),('∂W_TO/∂(L/D) (cruise)',S['dLDR'],'lbs','Eq 2.51'),('∂W_TO/∂R',S['dR'],'lbs/nm','Eq 2.45')]:
            vc='sens-neg' if val<0 else 'sens-pos'
            st.markdown(f'<div class="sens-row"><span class="sens-partial">{partial}</span><span class="{vc}">{val:+,.1f}</span><span class="sens-unit">{unit}</span><span class="sens-eq">{eq}</span></div>',unsafe_allow_html=True)
        st.markdown('</div>',unsafe_allow_html=True)

        st.markdown('<div class="card card-amber"><div class="card-title">Loiter Phase — Breguet Partials (Table 2.20)</div>',unsafe_allow_html=True)
        for partial,val,unit in [('∂W_TO/∂Cp (loiter)',S['dCpE'],'lbs/(lbs/hp/hr)'),('∂W_TO/∂η_p (loiter)',S['dnpE'],'lbs'),('∂W_TO/∂(L/D) (loiter)',S['dLDE'],'lbs')]:
            vc='sens-neg' if val<0 else 'sens-pos'
            st.markdown(f'<div class="sens-row"><span class="sens-partial">{partial}</span><span class="{vc}">{val:+,.1f}</span><span class="sens-unit">{unit}</span><span class="sens-eq">T2.20</span></div>',unsafe_allow_html=True)
        st.markdown('</div>',unsafe_allow_html=True)

    with s2:
        st.markdown(f'<div class="card card-amber"><div class="card-title">Range Trade Study</div><div style="font-size:0.8rem;color:#C9D1D9;line-height:1.7;margin-bottom:0.5rem">∂W_TO/∂R = <b style="color:#58A6FF">{S["dR"]:+.2f} lbs/nm</b></div>',unsafe_allow_html=True)
        for dr in [-200,-100,100,200]:
            dw=S['dR']*dr; col_v='#3FB950' if dw<0 else '#E3B341'
            st.markdown(f'<div style="display:flex;justify-content:space-between;align-items:center;padding:0.28rem 0;border-bottom:1px solid #21262D;font-size:0.8rem"><span style="color:#8B949E">ΔR = {dr:+d} nm</span><span style="font-family:JetBrains Mono,monospace;font-weight:700;color:{col_v}">{dw:+,.1f} lbs</span></div>',unsafe_allow_html=True)
        st.markdown('</div>',unsafe_allow_html=True)

        dR_c=st.slider("Custom ΔR (nm)",-600,600,0,step=25)
        if dR_c!=0:
            dW_c=S['dR']*dR_c; col2='#3FB950' if dW_c<0 else '#E3B341'
            bg2='rgba(63,185,80,.07)' if dW_c<0 else 'rgba(227,179,65,.07)'
            bd2='rgba(63,185,80,.25)' if dW_c<0 else 'rgba(227,179,65,.25)'
            st.markdown(f'<div style="background:{bg2};border:1px solid {bd2};border-radius:7px;padding:0.55rem 1rem;font-family:JetBrains Mono,monospace;font-size:0.82rem;color:{col2};margin-top:0.3rem">ΔR={dR_c:+d} nm → ΔW_TO={S["dR"]*dR_c:+,.1f} lbs → W_TO~{Wto+S["dR"]*dR_c:,.0f} lbs</div>',unsafe_allow_html=True)

        st.markdown('<div class="sec-div" style="margin-top:1rem">Tornado — Parameter Influence Ranking</div>',unsafe_allow_html=True)
        t_lbl=['Cp·Cruise','η_p·Cruise','L/D·Cruise','ΔR(200nm)','Cp·Loiter','η_p·Loiter','L/D·Loiter']
        t_val=[S['dCpR'],S['dnpR'],S['dLDR'],S['dR']*200,S['dCpE'],S['dnpE'],S['dLDE']]
        idx=sorted(range(7),key=lambda i:abs(t_val[i]))
        t_lbl=[t_lbl[i] for i in idx]; t_val=[t_val[i] for i in idx]
        fig_t=go.Figure(go.Bar(x=t_val,y=t_lbl,orientation='h',
            marker_color=['#1F6FEB' if v>=0 else '#3FB950' for v in t_val],
            marker_line_color='rgba(0,0,0,0)',
            text=[f'{abs(v):,.0f}' for v in t_val],textposition='outside',textfont=dict(size=9,color='#8B949E')))
        fig_t.add_vline(x=0,line_color='#30363D',line_width=1)
        fig_t.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',height=265,showlegend=False,margin=dict(l=8,r=55,t=10,b=10),font=dict(family='JetBrains Mono',size=9,color='#8B949E'),xaxis=dict(gridcolor='#21262D',linecolor='#30363D',title='ΔW_TO (lbs)',title_font=dict(size=8),tickfont=dict(size=8)),yaxis=dict(gridcolor='rgba(0,0,0,0)',linecolor='#30363D',tickfont=dict(size=9)))
        st.plotly_chart(fig_t,use_container_width=True)
        st.markdown('<div style="font-size:0.68rem;color:#6E7681">Blue = increases W_TO · Green = decreases W_TO (favourable)</div>',unsafe_allow_html=True)

# ═══ TAB 3 — CHARTS ═══
with tab3:
    PL=dict(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='#161B22',font=dict(family='JetBrains Mono',color='#8B949E',size=9),margin=dict(l=52,r=16,t=38,b=44),hoverlabel=dict(bgcolor='#1C2333',font_color='#F0F6FC',font_size=10,bordercolor='#30363D'))
    AX=dict(gridcolor='#21262D',linecolor='#30363D',zerolinecolor='#30363D',tickfont=dict(size=8))

    ch1,ch2=st.columns(2,gap="medium")
    with ch1:
        st.markdown('<div class="sec-div">Mission Phase Weight Fractions</div>',unsafe_allow_html=True)
        phases_l=list(RR['phases'].keys())
        fvals=[v for v,_,_ in RR['phases'].values()]
        types=[t for _,t,_ in RR['phases'].values()]
        cum_p=[1.0]
        for fv in fvals: cum_p.append(cum_p[-1]*fv)
        fig_m=make_subplots(rows=1,cols=2,column_widths=[0.55,0.45],subplot_titles=["Wᵢ/Wᵢ₋₁ per phase","Cumulative Mff"],horizontal_spacing=0.12)
        fig_m.add_trace(go.Bar(x=phases_l,y=fvals,marker_color=['#3FB950' if t=='Breguet' else '#388BFD' for t in types],marker_line_color='rgba(0,0,0,0)',text=[f'{v:.4f}' for v in fvals],textposition='outside',textfont=dict(size=7.5,color='#C9D1D9'),hovertemplate='<b>%{x}</b><br>%{y:.5f}<extra></extra>'),row=1,col=1)
        fig_m.add_trace(go.Scatter(x=['Ramp']+phases_l,y=cum_p,mode='lines+markers',line=dict(color='#388BFD',width=2.5),marker=dict(color='#F0F6FC',size=5,line=dict(color='#388BFD',width=2)),fill='tozeroy',fillcolor='rgba(56,139,253,.08)',hovertemplate='<b>%{x}</b><br>Cumul.=%{y:.5f}<extra></extra>'),row=1,col=2)
        fig_m.add_hline(y=RR['Mff'],line_dash='dot',line_color='#3FB950',line_width=1.2,annotation_text=f'Mff={RR["Mff"]:.4f}',annotation_font_color='#3FB950',annotation_font_size=8,row=1,col=2)
        fig_m.update_layout(**PL,height=265,showlegend=False)
        fig_m.update_xaxes(**AX); fig_m.update_yaxes(**AX)
        fig_m.update_yaxes(range=[0.75,1.04],row=1,col=1)
        fig_m.update_yaxes(range=[0.65,1.06],row=1,col=2)
        fig_m.update_annotations(font_size=9,font_color='#8B949E',font_family='JetBrains Mono')
        st.plotly_chart(fig_m,use_container_width=True)
        st.markdown('<div style="font-size:0.68rem;color:#6E7681;margin-top:-0.4rem">Blue=fixed (T2.1) · Green=Breguet variable (Eq2.9/2.11) · Dashed=final Mff</div>',unsafe_allow_html=True)

        st.markdown('<div class="sec-div">W_TO vs Design Range</div>',unsafe_allow_html=True)
        rr_arr=np.linspace(200,min(3200,float(R_nm)*2.8),55); ww_arr=[]
        for rv in rr_arr:
            try:
                w,r=solve_Wto({**P,'R':float(rv)}); ww_arr.append(w if abs(r['diff'])<80 else float('nan'))
            except: ww_arr.append(float('nan'))
        fig_r=go.Figure()
        fig_r.add_trace(go.Scatter(x=rr_arr,y=ww_arr,mode='lines',line=dict(color='#388BFD',width=2.2),fill='tozeroy',fillcolor='rgba(56,139,253,.06)',hovertemplate='Range:%{x:.0f}nm<br>W_TO:%{y:,.0f}lbs<extra></extra>'))
        fig_r.add_vline(x=float(R_nm),line_dash='dash',line_color='#E3B341',line_width=1.4,annotation_text=f'  {int(R_nm)} nm',annotation_font_color='#E3B341',annotation_font_size=8.5)
        fig_r.add_scatter(x=[float(R_nm)],y=[Wto],mode='markers',marker=dict(color='#E3B341',size=11,line=dict(color='#161B22',width=2),symbol='diamond'),showlegend=False)
        fig_r.update_layout(**PL,height=225,showlegend=False,xaxis=dict(**AX,title='Range (nm)',title_font=dict(size=8.5,color='#8B949E')),yaxis=dict(**AX,title='W_TO (lbs)',title_font=dict(size=8.5,color='#8B949E')))
        st.plotly_chart(fig_r,use_container_width=True)

        st.markdown('<div class="sec-div">W_TO vs Passengers</div>',unsafe_allow_html=True)
        pxa=np.arange(max(5,int(npax)-20),int(npax)+30,2); wxr=[]
        for n_ in pxa:
            try:
                w,r=solve_Wto({**P,'npax':int(n_)}); wxr.append(w if abs(r['diff'])<80 else float('nan'))
            except: wxr.append(float('nan'))
        fig_px=go.Figure()
        fig_px.add_trace(go.Scatter(x=pxa,y=wxr,mode='lines',line=dict(color='#3FB950',width=2.2),fill='tozeroy',fillcolor='rgba(63,185,80,.06)',hovertemplate='Pax:%{x}<br>W_TO:%{y:,.0f}lbs<extra></extra>'))
        fig_px.add_vline(x=int(npax),line_dash='dash',line_color='#E3B341',line_width=1.3,annotation_text=f'  {int(npax)} pax',annotation_font_color='#E3B341',annotation_font_size=8.5)
        fig_px.add_scatter(x=[int(npax)],y=[Wto],mode='markers',marker=dict(color='#E3B341',size=10,line=dict(color='#161B22',width=2),symbol='diamond'),showlegend=False)
        fig_px.update_layout(**PL,height=215,showlegend=False,xaxis=dict(**AX,title='Passengers',title_font=dict(size=8.5,color='#8B949E')),yaxis=dict(**AX,title='W_TO (lbs)',title_font=dict(size=8.5,color='#8B949E')))
        st.plotly_chart(fig_px,use_container_width=True)

    with ch2:
        st.markdown('<div class="sec-div">W_TO Composition — Weight Breakdown</div>',unsafe_allow_html=True)
        fig_p=go.Figure(go.Pie(
            labels=['Empty W_E','Usable Fuel','Trapped Fuel','Crew','Payload'],
            values=[WE,RR['WFu'],Wtfo_r,Wcrew,Wpl],hole=0.56,
            marker=dict(colors=['#388BFD','#58A6FF','#79C0FF','#3FB950','#56D364'],line=dict(color='#161B22',width=2.5)),
            textfont=dict(size=9.5,family='JetBrains Mono',color='#F0F6FC'),
            textinfo='label+percent',rotation=105,
            hovertemplate='<b>%{label}</b><br>%{value:,.0f} lbs<br>%{percent}<extra></extra>'))
        fig_p.update_layout(paper_bgcolor='rgba(0,0,0,0)',font=dict(family='JetBrains Mono',color='#8B949E'),showlegend=True,legend=dict(orientation='v',x=1.02,y=0.5,font=dict(size=8.5,color='#C9D1D9'),bgcolor='rgba(0,0,0,0)'),height=290,margin=dict(t=10,b=10,l=10,r=120),annotations=[dict(text=f'<b>{Wto:,.0f}</b><br>lbs',x=0.44,y=0.5,showarrow=False,font=dict(size=13,color='#F0F6FC',family='JetBrains Mono'))])
        st.plotly_chart(fig_p,use_container_width=True)

        st.markdown('<div class="sec-div">Weight Progression & Fuel Burn Through Mission</div>',unsafe_allow_html=True)
        fv_list=[v for v,_,_ in RR['phases'].values()]
        pl_list=['Ramp']+list(RR['phases'].keys())
        cum_w=[Wto]
        for fv in fv_list: cum_w.append(cum_w[-1]*fv)
        burn_w=[Wto-c for c in cum_w]
        fig_w=make_subplots(rows=2,cols=1,subplot_titles=['Aircraft Weight (lbs)','Cumul. Fuel Burn (lbs)'],vertical_spacing=0.12,shared_xaxes=True)
        fig_w.add_trace(go.Scatter(x=pl_list,y=cum_w,mode='lines+markers',line=dict(color='#388BFD',width=2.2),marker=dict(color='#F0F6FC',size=6,line=dict(color='#388BFD',width=2)),fill='tozeroy',fillcolor='rgba(56,139,253,.07)',hovertemplate='%{x}<br>%{y:,.0f} lbs<extra></extra>'),row=1,col=1)
        # Highlight cruise
        cidx=pl_list.index('Cruise')
        fig_w.add_trace(go.Scatter(x=[pl_list[cidx],pl_list[cidx+1]],y=[cum_w[cidx],cum_w[cidx+1]],mode='lines',line=dict(color='#3FB950',width=3.5),showlegend=False),row=1,col=1)
        fig_w.add_trace(go.Scatter(x=pl_list,y=burn_w,mode='lines+markers',line=dict(color='#E3B341',width=2.2),marker=dict(color='#F0F6FC',size=6,line=dict(color='#E3B341',width=2)),fill='tozeroy',fillcolor='rgba(227,179,65,.07)',hovertemplate='%{x}<br>%{y:,.0f} lbs<extra></extra>'),row=2,col=1)
        fig_w.update_layout(**PL,height=410,showlegend=False)
        fig_w.update_xaxes(**AX); fig_w.update_yaxes(**AX)
        fig_w.update_annotations(font_size=9,font_color='#8B949E',font_family='JetBrains Mono')
        st.plotly_chart(fig_w,use_container_width=True)
        st.markdown('<div style="font-size:0.68rem;color:#6E7681;margin-top:-0.4rem">Green=Cruise (Breguet) · Amber=Cumul. fuel · Diamond=design point</div>',unsafe_allow_html=True)

        st.markdown('<div class="sec-div">3D Surface — W_TO = f(L/D, Cp) at Cruise</div>',unsafe_allow_html=True)
        cpa=np.linspace(0.35,0.90,16); lda=np.linspace(8,22,16)
        Z=np.zeros((len(cpa),len(lda)))
        for i,cp in enumerate(cpa):
            for j,ld in enumerate(lda):
                try:
                    w,r=solve_Wto({**P,'Cpc':float(cp),'LDc':float(ld)}); Z[i,j]=w if abs(r['diff'])<80 else float('nan')
                except: Z[i,j]=float('nan')
        fig4=go.Figure(go.Surface(x=lda,y=cpa,z=Z,colorscale=[[0,'#0D1117'],[0.25,'#1F6FEB'],[0.6,'#388BFD'],[0.85,'#E3B341'],[1,'#F85149']],opacity=0.88,showscale=True,colorbar=dict(len=0.65,thickness=10,tickfont=dict(size=8,color='#8B949E'),title=dict(text='W_TO(lbs)',font=dict(size=8,color='#8B949E'))),hovertemplate='L/D:%{x:.1f}<br>Cp:%{y:.2f}<br>W_TO:%{z:,.0f}lbs<extra></extra>'))
        fig4.add_scatter3d(x=[float(LDc)],y=[float(Cpc)],z=[Wto],mode='markers',marker=dict(color='#E3B341',size=7,symbol='diamond'),showlegend=False)
        fig4.update_layout(paper_bgcolor='rgba(0,0,0,0)',font=dict(family='JetBrains Mono',color='#8B949E',size=9),scene=dict(xaxis=dict(title='L/D',backgroundcolor='#161B22',gridcolor='#21262D',linecolor='#30363D'),yaxis=dict(title='Cp',backgroundcolor='#161B22',gridcolor='#21262D',linecolor='#30363D'),zaxis=dict(title='W_TO(lbs)',backgroundcolor='#0D1117',gridcolor='#21262D',linecolor='#30363D'),bgcolor='#161B22',camera=dict(eye=dict(x=1.4,y=-1.6,z=0.7))),margin=dict(l=0,r=0,t=8,b=0),height=330)
        st.plotly_chart(fig4,use_container_width=True)
        st.markdown('<div style="font-size:0.68rem;color:#6E7681;margin-top:-0.4rem">Low Cp + High L/D = min W_TO. Amber diamond = design point. Cliff = no solution.</div>',unsafe_allow_html=True)

# ═══ TAB 4 ═══
with tab4:
    ex1,ex2=st.columns([1,1],gap="medium")
    with ex1:
        st.markdown('<div class="card card-blue"><div class="card-title">Download — CSV</div>',unsafe_allow_html=True)
        rows={'Parameter':['W_TO','Mff','W_F','W_F_usable','W_tfo','W_OE','W_E_tent','W_E_allow','delta_WE','W_PL','W_crew','Rc_sm','Vm_mph','dWTO_dCp_R','dWTO_dnp_R','dWTO_dLD_R','dWTO_dR','dWTO_dCp_E','dWTO_dnp_E','dWTO_dLD_E','F','C','D'],
              'Value':[Wto,RR['Mff'],WF,RR['WFu'],Wtfo_r,WOE,WE,RR['WEa'],RR['diff'],Wpl,Wcrew,RR['Rc'],RR['Vm'],S['dCpR'],S['dnpR'],S['dLDR'],S['dR'],S['dCpE'],S['dnpE'],S['dLDE'],S['F'],S['C'],S['D']],
              'Units':['lbs','—','lbs','lbs','lbs','lbs','lbs','lbs','lbs','lbs','lbs','s.m.','mph','lbs/(lbs/hp/hr)','lbs','lbs','lbs/nm','lbs/(lbs/hp/hr)','lbs','lbs','lbs','—','lbs']}
        b=io.StringIO(); pd.DataFrame(rows).to_csv(b,index=False)
        st.download_button("⬇  Full Results (CSV)",b.getvalue(),"aerosizer_hw28.csv","text/csv",use_container_width=True)
        st.markdown('<br>',unsafe_allow_html=True)
        b2=io.StringIO()
        pd.DataFrame({'Phase':list(RR['phases'].keys()),'Wi/Wi-1':[f for f,_,_ in RR['phases'].values()],'Type':[t for _,t,_ in RR['phases'].values()],'Ref':[r for _,_,r in RR['phases'].values()]}).to_csv(b2,index=False)
        st.download_button("⬇  Phase Fractions (CSV)",b2.getvalue(),"phases.csv","text/csv",use_container_width=True)
        st.markdown('</div>',unsafe_allow_html=True)
        st.markdown('<div class="card card-blue"><div class="card-title">Active Configuration</div>',unsafe_allow_html=True)
        st.dataframe(pd.DataFrame({'Parameter':list(P.keys()),'Value':[str(v) for v in P.values()]}),hide_index=True,use_container_width=True)
        st.markdown('</div>',unsafe_allow_html=True)

    with ex2:
        st.markdown('<div class="card card-blue"><div class="card-title">PDF Report — A4 Engineering Format</div>',unsafe_allow_html=True)
        st.markdown('<div style="font-size:0.8rem;color:#8B949E;line-height:1.8;margin-bottom:0.8rem">① Title block · ② All inputs · ③ Steps 1–6 · ④ Phase fractions (Breguet highlighted) · ⑤ Design ratios · ⑥ Sensitivity partials · ⑦ References</div>',unsafe_allow_html=True)
        def make_pdf():
            buf=io.BytesIO()
            doc=SimpleDocTemplate(buf,pagesize=A4,leftMargin=2.0*cm,rightMargin=2.0*cm,topMargin=2.2*cm,bottomMargin=2.2*cm)
            PW=17.0*cm
            CN=colors.HexColor('#0D1B2A'); CB=colors.HexColor('#1F6FEB'); CS=colors.HexColor('#388BFD')
            CG=colors.HexColor('#475569'); CL=colors.HexColor('#94A3B8'); CR=colors.HexColor('#CBD5E1')
            CF=colors.HexColor('#F8FAFF'); CW=colors.white
            CGR=colors.HexColor('#D1FAE5'); CA=colors.HexColor('#FEF3C7')
            CO=colors.HexColor('#065F46'); CWN=colors.HexColor('#92400E')
            sty=getSampleStyleSheet()
            def ps(nm,**kw): return ParagraphStyle(nm,parent=sty['Normal'],**kw)
            sH1=ps('H1',fontSize=10,fontName='Helvetica-Bold',textColor=CB,spaceBefore=10,spaceAfter=4)
            sBODY=ps('BO',fontSize=8,textColor=CG,leading=12)
            sSUB=ps('SU',fontSize=8,textColor=CG,leading=12,spaceAfter=2)
            sSTAT=ps('ST',fontSize=9,fontName='Helvetica-Bold',textColor=CO if conv else CWN,spaceAfter=3)
            sCAP=ps('CA',fontSize=7,textColor=CL,leading=10,spaceBefore=2,spaceAfter=6)
            def ts(hdr=CN):
                return TableStyle([('BACKGROUND',(0,0),(-1,0),hdr),('TEXTCOLOR',(0,0),(-1,0),CW),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTNAME',(0,1),(-1,-1),'Helvetica'),('FONTSIZE',(0,0),(-1,-1),7.5),('LEADING',(0,0),(-1,-1),11),('TEXTCOLOR',(0,1),(-1,-1),CG),('ROWBACKGROUNDS',(0,1),(-1,-1),[CW,CF]),('GRID',(0,0),(-1,-1),0.25,CR),('LINEBELOW',(0,0),(-1,0),0.8,CS),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),3.5),('BOTTOMPADDING',(0,0),(-1,-1),3.5),('VALIGN',(0,0),(-1,-1),'MIDDLE')])
            def rule(): return HRFlowable(width=PW,thickness=0.4,color=CR,spaceBefore=3,spaceAfter=3)
            story=[]
            hd=Table([[Paragraph('<b>AEROSIZER PRO</b>',ps('TX',fontSize=16,fontName='Helvetica-Bold',textColor=CN,leading=20)),Paragraph('DOC: ASP-HW28 REV A<br/>CLASS: Conceptual<br/>STATUS: '+('RELEASED' if conv else 'DRAFT'),ps('TX2',fontSize=7,textColor=CL,leading=10,alignment=TA_RIGHT))]],colWidths=[PW*0.60,PW*0.40])
            hd.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0)]))
            story.append(hd)
            story.append(HRFlowable(width=PW,thickness=2.5,color=CB,spaceBefore=4,spaceAfter=2))
            story.append(Paragraph('Preliminary Aircraft Weight Sizing — Breguet Range/Endurance · Propeller-Driven · Raymer (2018) Ch.2 — Problem 2.8',sSUB))
            story.append(HRFlowable(width=PW,thickness=0.4,color=CR,spaceBefore=2,spaceAfter=8))
            story.append(Paragraph('1   Mission Inputs',sH1)); story.append(rule())
            CW4=[PW*0.30,PW*0.17,PW*0.30,PW*0.17]
            t_in=Table([['Parameter','Value','Parameter','Value'],['Passengers',str(int(npax)),'Design range (nm)',str(int(R_nm))],['Pax body wt (lbs)',str(int(wpax)),'Loiter endurance (hr)',f'{El:.2f}'],['Baggage wt (lbs)',str(int(wbag)),'Loiter speed (kts)',str(int(Vl))],['Flight crew',str(int(ncrew)),'Cruise L/D',f'{LDc:.1f}'],['Cabin attendants',str(int(natt)),'Loiter L/D',f'{LDl:.1f}'],['Reg. A',f'{A_v:.4f}','Cruise Cp',f'{Cpc:.2f}'],['Reg. B',f'{B_v:.4f}','Loiter Cp',f'{Cpl:.2f}'],['M_tfo',f'{Mtfo:.3f}','Cruise η_p',f'{npc:.2f}'],['M_res',f'{Mres:.3f}','Loiter η_p',f'{npl:.2f}']],colWidths=CW4)
            t_in.setStyle(ts()); story+=[t_in,Spacer(1,0.2*cm)]
            story.append(Paragraph('2   Sizing Steps 1–6',sH1)); story.append(rule())
            t_pl=Table([['Item','Weight (lbs)','Notes'],[f'{npax} pax×({int(wpax)}+{int(wbag)})',f'{int(npax)*(int(wpax)+int(wbag)):,}','cabin'],[f'{ncrew} pilots×205',f'{int(ncrew)*205:,}','crew'],[f'{natt} att×200',f'{int(natt)*200:,}','cabin crew'],['W_PL',f'{Wpl:,.0f}',''],['W_crew',f'{Wcrew:,.0f}',''],['W_tfo',f'{Wtfo_r:,.2f}','trapped fuel']],colWidths=[PW*0.52,PW*0.24,PW*0.20])
            t_pl.setStyle(ts(hdr=colors.HexColor('#334155'))); story+=[t_pl,Spacer(1,0.1*cm)]
            cum_ph=1.0; ph_rows=[['Phase','Wᵢ/Wᵢ₋₁','Cumul.','Type','Source']]
            for ph,(fv,ftype,fsrc) in RR['phases'].items():
                cum_ph*=fv; ph_rows.append([ph,f'{fv:.5f}',f'{cum_ph:.5f}',ftype,fsrc])
            t_ph=Table(ph_rows,colWidths=[PW*0.22,PW*0.14,PW*0.14,PW*0.18,PW*0.28])
            t_ph.setStyle(ts(hdr=CB))
            for ri,row in enumerate(ph_rows[1:],start=1):
                if row[3]=='Breguet': t_ph.setStyle(TableStyle([('BACKGROUND',(0,ri),(-1,ri),colors.HexColor('#ECFDF5')),('TEXTCOLOR',(3,ri),(3,ri),CO),('FONTNAME',(0,ri),(-1,ri),'Helvetica-Bold')]))
            story+=[t_ph,Paragraph(f'Final Mff={RR["Mff"]:.6f}',ps('MF',fontSize=8,fontName='Helvetica-Bold',textColor=CB,spaceBefore=3,spaceAfter=4))]
            t_cv=Table([['Quantity','Value (lbs)','Expression'],['W_F (total)',f'{WF:,.2f}','W_Fused+W_tfo'],['W_OE (tent.)',f'{WOE:,.2f}','W_TO−W_F−W_PL'],['W_E (tent.)',f'{WE:,.2f}','W_OE−W_tfo−W_crew'],['W_E (allow.)',f'{RR["WEa"]:,.2f}','10^[(logW_TO−A)/B]'],['ΔW_E',f'{RR["diff"]:+.2f}','W_E_allow−W_E_tent']],colWidths=[PW*0.44,PW*0.22,PW*0.30])
            t_cv.setStyle(ts(hdr=colors.HexColor('#334155')))
            t_cv.setStyle(TableStyle([('BACKGROUND',(0,5),(-1,5),CGR if conv else CA),('TEXTCOLOR',(1,5),(1,5),CO if conv else CWN),('FONTNAME',(0,5),(-1,5),'Helvetica-Bold')]))
            story+=[t_cv,Spacer(1,0.1*cm),Paragraph('CONVERGED ✓' if conv else 'NOT CONVERGED ⚠',sSTAT)]
            story.append(Paragraph('3   Design Ratios',sH1)); story.append(rule())
            rr_data=[['Ratio','Value','Typical','Check']]
            for nm,vl,lo,hi in [('W_PL/W_TO',Wpl/Wto,0.10,0.25),('W_F/W_TO',WF/Wto,0.20,0.45),('W_E/W_TO',WE/Wto,0.45,0.65),('W_PL/W_E',Wpl/WE,0.15,0.40)]:
                ok_r=lo<=vl<=hi; rr_data.append([nm,f'{vl:.4f}',f'{lo:.2f}–{hi:.2f}','✓' if ok_r else ('▲' if vl>hi else '▼')])
            t_r=Table(rr_data,colWidths=[PW*0.28,PW*0.18,PW*0.28,PW*0.22]); t_r.setStyle(ts()); story+=[t_r,Spacer(1,0.15*cm)]
            story.append(Paragraph('4   Sensitivity Partials (Raymer Table 2.20)',sH1)); story.append(rule())
            s_rows=[['Partial','Value','Units','Ref.'],('∂W_TO/∂Cp(cruise)',f'{S["dCpR"]:+,.1f}','lbs/(lbs/hp/hr)','Eq2.49'),('∂W_TO/∂η_p(cruise)',f'{S["dnpR"]:+,.1f}','lbs','Eq2.50'),('∂W_TO/∂(L/D)(cruise)',f'{S["dLDR"]:+,.1f}','lbs','Eq2.51'),('∂W_TO/∂R',f'{S["dR"]:+,.2f}','lbs/nm','Eq2.45'),('∂W_TO/∂Cp(loiter)',f'{S["dCpE"]:+,.1f}','lbs/(lbs/hp/hr)','T2.20'),('∂W_TO/∂η_p(loiter)',f'{S["dnpE"]:+,.1f}','lbs','T2.20'),('∂W_TO/∂(L/D)(loiter)',f'{S["dLDE"]:+,.1f}','lbs','T2.20')]
            t_s=Table(s_rows,colWidths=[PW*0.34,PW*0.16,PW*0.34,PW*0.12]); t_s.setStyle(ts(hdr=CB))
            for ri,row in enumerate(s_rows[1:],start=1):
                try:
                    if float(row[1].replace(',','').replace('+',''))<0: t_s.setStyle(TableStyle([('TEXTCOLOR',(1,ri),(1,ri),CO)]))
                except: pass
            story+=[t_s,Spacer(1,0.15*cm)]
            story.append(Paragraph('5   References',sH1)); story.append(rule())
            refs=[['[1]','Raymer,D.P.(2018).Aircraft Design:A Conceptual Approach,6th Ed.AIAA.'],['[2]','Roskam,J.(2003).Airplane Design,Part I.DAR Corp.'],['[3]','Breguet,L.(1923).Calcul du Poids de Combustible.Comptes Rendus.']]
            t5=Table([['Ref.','Citation']]+refs,colWidths=[PW*0.08,PW*0.92]); t5.setStyle(ts(hdr=colors.HexColor('#334155'))); story.append(t5)
            story+=[Spacer(1,0.3*cm),HRFlowable(width=PW,thickness=0.5,color=CR),Paragraph('Conceptual-level sizing only. Not for regulatory/structural use. Breguet Eq.2.9/2.11 for propeller aircraft only.',ps('DIS',fontSize=6.5,textColor=CL,leading=9.5,spaceBefore=3))]
            doc.build(story); buf.seek(0); return buf.read()

        st.download_button("⬇  Generate & Download PDF (A4)",make_pdf(),"aerosizer_hw28_report.pdf","application/pdf",use_container_width=True)
        st.markdown('</div>',unsafe_allow_html=True)

# ═══ TAB 5 ═══
with tab5:
    r1,r2=st.columns(2,gap="medium")
    with r1:
        for code,title,eq,desc in [("Eq 2.9","Cruise — Breguet","W₅/W₄ = 1/exp[ Rc/(375·η_p/Cp·L/D) ]","Rc in s.m. · Cp in lbs/hp/hr"),("Eq 2.11","Loiter — Breguet","W₆/W₅ = 1/exp[ E/(375·(1/V)·η_p/Cp·L/D) ]","E in hr · V in mph"),("Eq 2.22","C factor","C = 1−(1+M_res)(1−Mff)−M_tfo",""),("Eq 2.23","D factor","D = W_PL + W_crew","")]:
            st.markdown(f'<div class="card card-blue"><div class="card-title">{code} — {title}</div><div class="eq-box">{eq}</div><div style="font-size:0.72rem;color:#6E7681;margin-top:0.3rem">{desc}</div></div>',unsafe_allow_html=True)
    with r2:
        for code,title,eq,desc in [("Eq 2.44","F sizing multiplier","F = −B·W_TO²·(1+M_res)·Mff / [C·W_TO·(1−B)−D]",""),("Eq 2.45","∂W_TO/∂R","∂W_TO/∂R = F·Cp/(375·η_p·L/D)","lbs/nm"),("Eq 2.49","∂W_TO/∂Cp","∂W_TO/∂Cp = F·R/(375·η_p·L/D)","lbs/(lbs/hp/hr)"),("Eq 2.50/51","∂W_TO/∂η_p & ∂(L/D)","∂/∂η_p = −F·R·Cp/(375·η_p²·L/D)","Negative = reduces W_TO (green)")]:
            st.markdown(f'<div class="card card-blue"><div class="card-title">{code} — {title}</div><div class="eq-box">{eq}</div><div style="font-size:0.72rem;color:#6E7681;margin-top:0.3rem">{desc}</div></div>',unsafe_allow_html=True)
