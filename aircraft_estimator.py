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
                                 Table, TableStyle, HRFlowable, Image as RLImage)
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import plotly.io as pio

# ─── PAGE CONFIG ───
st.set_page_config(page_title="AeroSizer Pro", page_icon="✈", layout="wide",
                   initial_sidebar_state="expanded")

# ─── GTM ───
st.markdown("""<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-T8JSQMHD');</script>""",
unsafe_allow_html=True)

# ─── CSS ───
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&family=DM+Sans:wght@300;400;500;600;700&family=DM+Serif+Display:ital@0;1&display=swap');

:root {
  --bg:#07090d;       --sur:#0c0f16;      --pan:#111720;      --pan2:#161d2a;
  --border:rgba(255,255,255,.07);  --border2:rgba(255,255,255,.04);
  --gold:#c8a86c;     --gold2:#e4c88a;    --gold3:rgba(200,168,108,.08);
  --blue:#4875c2;     --blue2:#6a9eea;    --blue3:#8fb8ff;
  --green:#3fb950;    --amber:#e3b341;    --red:#f85149;      --pu:#9c72d4;
  --text:#b0bcce;     --text2:#8b949e;    --text3:#6e7681;    --white:#f0ede6;
  --sh:0 8px 40px rgba(0,0,0,.6);
}

*,*::before,*::after{box-sizing:border-box;}
html,body,[class*="css"]{
  background:var(--bg)!important;
  color:var(--text)!important;
  font-family:'DM Sans',sans-serif!important;
}
.stApp{background:var(--bg)!important;}
.main .block-container{padding:1rem 1.5rem 2rem!important;max-width:100%!important;}

/* Scrollbar */
::-webkit-scrollbar{width:4px;height:4px;}
::-webkit-scrollbar-track{background:var(--bg);}
::-webkit-scrollbar-thumb{background:rgba(200,168,108,.3);border-radius:4px;}
::-webkit-scrollbar-thumb:hover{background:var(--gold);}

/* ── SIDEBAR ── */
[data-testid="stSidebar"]{
  background:var(--sur)!important;
  border-right:1px solid var(--border)!important;
  padding:0!important;
}
[data-testid="stSidebar"]>div:first-child{padding:0!important;}

.sb-logo{
  padding:1.4rem 1.2rem 1rem;
  border-bottom:1px solid var(--border);
  background:linear-gradient(150deg,#06090f,#0c1220);
  position:relative;overflow:hidden;
}
.sb-logo::before{
  content:'';position:absolute;inset:0;
  background-image:linear-gradient(rgba(72,117,194,.04) 1px,transparent 1px),
    linear-gradient(90deg,rgba(72,117,194,.04) 1px,transparent 1px);
  background-size:20px 20px;pointer-events:none;
}
.sb-logo-title{
  font-family:'DM Serif Display',serif;font-size:1.3rem;font-weight:400;
  color:var(--white);letter-spacing:-.03em;line-height:1;position:relative;z-index:1;
}
.sb-logo-title span{
  background:linear-gradient(135deg,var(--gold),var(--gold2));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}
.sb-logo-sub{
  font-family:'JetBrains Mono',monospace;font-size:.55rem;letter-spacing:.18em;
  text-transform:uppercase;color:var(--text3);margin-top:.35rem;position:relative;z-index:1;
}
.sb-stripe{height:2px;background:linear-gradient(90deg,var(--blue),var(--gold),var(--blue));
  background-size:200%;animation:stripeMove 4s linear infinite;}
@keyframes stripeMove{0%{background-position:0%;}100%{background-position:200%;}}

.sb-sec{
  font-family:'JetBrains Mono',monospace;font-size:.58rem;font-weight:600;
  letter-spacing:.18em;text-transform:uppercase;color:var(--gold);
  padding:.6rem 1.1rem .35rem;border-bottom:1px solid var(--border2);
  margin:.4rem 0 .5rem;display:flex;align-items:center;gap:.45rem;
}
.sb-sec::before{content:'';width:10px;height:1px;background:var(--gold);flex-shrink:0;}

[data-testid="stSidebar"] label{
  font-family:'DM Sans',sans-serif!important;
  font-size:.77rem!important;font-weight:500!important;color:var(--text)!important;
}
[data-testid="stSidebar"] .stNumberInput input{
  background:var(--pan)!important;border:1px solid var(--border)!important;
  border-radius:7px!important;color:var(--white)!important;
  font-family:'JetBrains Mono',monospace!important;font-size:.82rem!important;
}
[data-testid="stSidebar"] .stNumberInput input:focus{
  border-color:var(--gold)!important;
  box-shadow:0 0 0 2px rgba(200,168,108,.2)!important;
}
[data-testid="stSidebar"] div.stButton>button{
  background:linear-gradient(135deg,var(--gold),var(--gold2))!important;
  color:#07090d!important;border:none!important;border-radius:9px!important;
  font-size:.83rem!important;font-weight:700!important;padding:.65rem!important;
  width:100%!important;letter-spacing:.04em;
  box-shadow:0 4px 18px rgba(200,168,108,.3)!important;
  transition:all .22s!important;
}
[data-testid="stSidebar"] div.stButton>button:hover{
  transform:translateY(-1px)!important;
  box-shadow:0 6px 22px rgba(200,168,108,.4)!important;
}

/* Sidebar KPI */
.sb-kpi{
  background:var(--pan);border:1px solid var(--border);border-radius:9px;
  padding:.75rem 1rem;margin:0 .7rem .5rem;
  border-top:2px solid var(--gold);
}
.sb-kpi-val{
  font-family:'JetBrains Mono',monospace;font-size:1.5rem;font-weight:700;
  color:var(--gold2);line-height:1.1;
}
.sb-kpi-lbl{font-size:.6rem;letter-spacing:.1em;text-transform:uppercase;color:var(--text3);margin-top:.2rem;}
.conv-pill{
  display:inline-flex;align-items:center;gap:.38rem;border-radius:20px;
  padding:.24rem .8rem;font-family:'JetBrains Mono',monospace;
  font-size:.65rem;font-weight:700;letter-spacing:.05em;margin-top:.55rem;
}
.conv-ok{background:rgba(63,185,80,.12);border:1px solid rgba(63,185,80,.3);color:#3fb950;}
.conv-warn{background:rgba(248,81,73,.1);border:1px solid rgba(248,81,73,.3);color:#f85149;}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"]{
  background:var(--sur)!important;border:1px solid var(--border)!important;
  border-radius:11px!important;padding:4px!important;gap:3px!important;
  margin-bottom:1.2rem!important;
}
.stTabs [data-baseweb="tab"]{
  border-radius:8px!important;font-family:'DM Sans',sans-serif!important;
  font-size:.8rem!important;font-weight:500!important;color:var(--text2)!important;
  padding:.44rem 1.2rem!important;transition:all .2s!important;
}
.stTabs [aria-selected="true"]{
  background:linear-gradient(135deg,var(--gold),var(--gold2))!important;
  color:#07090d!important;font-weight:700!important;
  box-shadow:0 2px 12px rgba(200,168,108,.35)!important;
}

/* ── CARDS ── */
.card{
  background:var(--sur);border:1px solid var(--border);
  border-radius:12px;padding:1.15rem 1.3rem;margin-bottom:1rem;
  position:relative;overflow:hidden;
}
.card::before{
  content:'';position:absolute;top:0;left:0;right:0;height:1px;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,.06),transparent);
  pointer-events:none;
}
.card-blue{border-left:2px solid var(--blue2);}
.card-gold{border-left:2px solid var(--gold);}
.card-green{border-left:2px solid var(--green);}
.card-amber{border-left:2px solid var(--amber);}
.card-red{border-left:2px solid var(--red);}

.card-title{
  font-family:'JetBrains Mono',monospace;font-size:.58rem;font-weight:700;
  letter-spacing:.16em;text-transform:uppercase;color:var(--gold);
  padding-bottom:.5rem;border-bottom:1px solid var(--border2);
  margin-bottom:.8rem;display:flex;align-items:center;gap:.5rem;
}
.card-title::before{content:'';width:8px;height:1px;background:var(--gold);flex-shrink:0;}

/* ── EQUATIONS ── */
.eq-box{
  background:rgba(200,168,108,.07);border:1px solid rgba(200,168,108,.2);
  border-radius:8px;padding:.5rem 1rem;
  font-family:'JetBrains Mono',monospace;font-size:.8rem;color:var(--gold2);
  display:block;margin-bottom:.5rem;white-space:nowrap;overflow-x:auto;
  letter-spacing:.01em;
}
.eq-label{font-size:.72rem;color:var(--text2);margin-bottom:.3rem;font-weight:500;}

/* ── RESULT PILLS ── */
.rpill{
  display:inline-flex;align-items:baseline;gap:.28rem;border-radius:7px;
  padding:.22rem .75rem;font-family:'JetBrains Mono',monospace;
  font-size:.86rem;font-weight:700;margin-right:.4rem;margin-top:.35rem;
}
.rpill-blue{background:rgba(72,117,194,.12);border:1px solid rgba(106,158,234,.28);color:var(--blue3);}
.rpill-gold{background:rgba(200,168,108,.1);border:1px solid rgba(200,168,108,.28);color:var(--gold2);}
.rpill-green{background:rgba(63,185,80,.1);border:1px solid rgba(63,185,80,.28);color:var(--green);}
.rpill-warn{background:rgba(227,179,65,.1);border:1px solid rgba(227,179,65,.28);color:var(--amber);}
.rpill-red{background:rgba(248,81,73,.1);border:1px solid rgba(248,81,73,.28);color:var(--red);}
.rpill-unit{font-size:.63rem;font-weight:400;opacity:.6;}

/* ── PHASE TABLE ROWS ── */
.ph-hdr{
  display:grid;grid-template-columns:150px 95px 80px 80px 1fr;
  gap:.5rem;padding:.25rem 0 .4rem;
  font-size:.6rem;letter-spacing:.08em;text-transform:uppercase;
  color:var(--text3);border-bottom:1px solid var(--border);font-weight:600;
}
.ph-row{
  display:grid;grid-template-columns:150px 95px 80px 80px 1fr;
  gap:.5rem;align-items:center;padding:.4rem 0;
  border-bottom:1px solid var(--border2);font-size:.8rem;
  transition:background .15s;
}
.ph-row:last-child{border-bottom:none;}
.ph-row:hover{background:rgba(200,168,108,.03);border-radius:6px;}
.ph-name{font-weight:500;color:var(--text);}
.ph-frac{font-family:'JetBrains Mono',monospace;font-weight:700;}
.ph-frac-fixed{color:var(--blue3);}
.ph-frac-breguet{color:var(--gold2);}
.ph-badge{
  font-size:.6rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;
  padding:.1rem .5rem;border-radius:4px;width:fit-content;
}
.ph-badge-fixed{background:rgba(72,117,194,.1);color:var(--blue3);border:1px solid rgba(72,117,194,.2);}
.ph-badge-breguet{background:rgba(200,168,108,.1);color:var(--gold);border:1px solid rgba(200,168,108,.2);}
.ph-src{font-size:.66rem;color:var(--text3);font-family:'JetBrains Mono',monospace;}

/* ── SENSITIVITY ── */
.sens-row{
  display:grid;grid-template-columns:210px 115px 160px 70px;
  gap:.5rem;align-items:center;padding:.38rem 0;
  border-bottom:1px solid var(--border2);transition:background .15s;
}
.sens-row:hover{background:rgba(200,168,108,.03);border-radius:6px;}
.sens-row:last-child{border-bottom:none;}
.sens-partial{font-family:'JetBrains Mono',monospace;font-size:.77rem;color:var(--text);}
.sens-pos{font-family:'JetBrains Mono',monospace;font-size:.82rem;font-weight:700;color:var(--red);}
.sens-neg{font-family:'JetBrains Mono',monospace;font-size:.82rem;font-weight:700;color:var(--green);}
.sens-unit{font-size:.65rem;color:var(--text3);}
.sens-eq{font-size:.63rem;color:var(--gold);font-family:'JetBrains Mono',monospace;}

/* ── STATUS BAR ── */
.status-ok{
  background:rgba(63,185,80,.07);border:1px solid rgba(63,185,80,.18);
  border-left:3px solid var(--green);border-radius:0 9px 9px 0;
  padding:.55rem 1.2rem;margin-bottom:1rem;
  font-family:'JetBrains Mono',monospace;font-size:.77rem;color:var(--green);
}
.status-err{
  background:rgba(248,81,73,.06);border:1px solid rgba(248,81,73,.18);
  border-left:3px solid var(--red);border-radius:0 9px 9px 0;
  padding:.55rem 1.2rem;margin-bottom:1rem;
  font-family:'JetBrains Mono',monospace;font-size:.77rem;color:var(--red);
}

/* ── KPI CARDS ── */
.kpi-card{
  background:var(--sur);border:1px solid var(--border);
  border-radius:11px;padding:1rem 1.1rem;
  border-top:2px solid var(--border);
  transition:transform .2s,border-color .2s;
}
.kpi-card:hover{transform:translateY(-2px);border-color:rgba(200,168,108,.25);}
.kpi-card.primary{border-top:2px solid var(--gold);background:rgba(200,168,108,.05);}
.kpi-card.green{border-top:2px solid var(--green);}
.kpi-card.amber{border-top:2px solid var(--amber);}
.kpi-card.blue{border-top:2px solid var(--blue2);}
.kpi-val{
  font-family:'JetBrains Mono',monospace;font-size:1.5rem;
  font-weight:700;color:var(--white);line-height:1.1;
}
.kpi-val.primary{color:var(--gold2);font-size:1.65rem;}
.kpi-unit{font-size:.65rem;font-weight:400;color:var(--text3);margin-left:2px;}
.kpi-lbl{font-size:.58rem;letter-spacing:.1em;text-transform:uppercase;color:var(--text3);margin-top:.3rem;font-weight:500;}

/* ── SECTION DIV ── */
.sec-div{
  font-family:'JetBrains Mono',monospace;font-size:.6rem;font-weight:700;
  letter-spacing:.16em;text-transform:uppercase;color:var(--gold);
  border-bottom:1px solid var(--border);padding-bottom:.4rem;
  margin:.8rem 0 .9rem;display:flex;align-items:center;gap:.5rem;
}
.sec-div::before{content:'';width:10px;height:1px;background:var(--gold);flex-shrink:0;}

/* ── MAIN HEADER ── */
.main-header{
  background:var(--sur);border:1px solid var(--border);
  border-radius:12px;border-left:3px solid var(--gold);
  padding:.9rem 1.5rem;margin-bottom:1.1rem;
  display:flex;align-items:center;justify-content:space-between;
  position:relative;overflow:hidden;
}
.main-header::before{
  content:'';position:absolute;inset:0;
  background-image:linear-gradient(rgba(200,168,108,.03) 1px,transparent 1px),
    linear-gradient(90deg,rgba(200,168,108,.03) 1px,transparent 1px);
  background-size:32px 32px;pointer-events:none;
}
.mh-title{
  font-family:'DM Serif Display',serif;font-size:1.4rem;font-weight:400;
  color:var(--white);letter-spacing:-.03em;line-height:1;position:relative;z-index:1;
}
.mh-title span{
  background:linear-gradient(135deg,var(--gold),var(--gold2));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}

/* ── DATAFRAME ── */
[data-testid="stDataFrame"]{
  border:1px solid var(--border)!important;border-radius:10px!important;
  overflow:hidden!important;
}
[data-testid="stDataFrame"] table{border-collapse:collapse!important;}
[data-testid="stDataFrame"] thead tr th{
  background:var(--pan2)!important;color:var(--gold)!important;
  font-family:'JetBrains Mono',monospace!important;font-size:.68rem!important;
  font-weight:700!important;letter-spacing:.1em!important;text-transform:uppercase!important;
  border-bottom:1.5px solid rgba(200,168,108,.3)!important;
  padding:.5rem .8rem!important;
}
[data-testid="stDataFrame"] tbody td{
  font-family:'JetBrains Mono',monospace!important;font-size:.78rem!important;
  color:var(--text)!important;border-color:var(--border2)!important;
  padding:.42rem .8rem!important;line-height:1.4!important;
}
[data-testid="stDataFrame"] tbody tr:nth-child(odd) td{
  background:rgba(255,255,255,.015)!important;
}
[data-testid="stDataFrame"] tbody tr:hover td{
  background:rgba(200,168,108,.06)!important;color:var(--white)!important;
}
/* Number cells — right align */
[data-testid="stDataFrame"] tbody td[data-type="number"]{
  text-align:right!important;color:var(--gold2)!important;
}
/* First column — label style */
[data-testid="stDataFrame"] tbody td:first-child{
  color:var(--text2)!important;font-size:.73rem!important;
}
/* Scrollbar inside table */
[data-testid="stDataFrame"] ::-webkit-scrollbar{height:3px;}
[data-testid="stDataFrame"] ::-webkit-scrollbar-thumb{background:rgba(200,168,108,.25);}

/* ── DOWNLOAD ── */
div.stDownloadButton>button{
  background:var(--pan)!important;color:var(--gold)!important;
  border:1px solid rgba(200,168,108,.25)!important;border-radius:8px!important;
  font-size:.8rem!important;font-weight:600!important;padding:.55rem 1rem!important;width:100%!important;
  transition:all .2s!important;
}
div.stDownloadButton>button:hover{
  border-color:var(--gold)!important;color:var(--white)!important;
  background:rgba(200,168,108,.1)!important;transform:translateY(-1px)!important;
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────
# PHYSICS — unchanged, exact Raymer Ch.2 equations
# ─────────────────────────────────────────────────────
def compute_mission(p):
    Wpl   = p['npax'] * (p['wpax'] + p['wbag'])
    Wcrew = (p['ncrew'] + p['natt']) * 205
    Wtfo  = p['Wto'] * p['Mtfo']
    Rc    = p['R']   * 1.15078              # nm → statute miles
    Vm    = p['Vl']  * 1.15078              # kts → mph
    # Eq 2.9 cruise fraction
    W5 = 1.0 / math.exp(Rc / (375.0 * (p['npc'] / p['Cpc']) * p['LDc']))
    # Eq 2.11 loiter fraction
    W6 = 1.0 / math.exp(p['El'] / (375.0 * (1.0 / Vm) * (p['npl'] / p['Cpl']) * p['LDl']))
    phases = {
        'Engine Start': (0.990, 'Fixed',   'T2.1'),
        'Taxi':         (0.995, 'Fixed',   'T2.1'),
        'Takeoff':      (0.995, 'Fixed',   'T2.1'),
        'Climb':        (0.985, 'Fixed',   'Fig2.2'),
        'Cruise':       (W5,   'Breguet', 'Eq 2.9'),
        'Loiter':       (W6,   'Breguet', 'Eq 2.11'),
        'Descent':      (0.985, 'Fixed',   'T2.1'),
        'Landing':      (0.995, 'Fixed',   'T2.1'),
    }
    Mff = 1.0
    for v, _, _ in phases.values():
        Mff *= v
    WFu  = p['Wto'] * (1.0 - Mff)
    WF   = WFu + p['Wto'] * p['Mr'] * (1.0 - Mff)
    WOE  = p['Wto'] - WF - Wpl
    WE   = WOE - Wtfo - Wcrew
    WEa  = 10.0 ** ((math.log10(p['Wto']) - p['A']) / p['B'])
    return dict(Wpl=Wpl, Wcrew=Wcrew, Wtfo=Wtfo, Mff=Mff,
                WF=WF, WFu=WFu, WOE=WOE, WE=WE, WEa=WEa,
                diff=WEa - WE, phases=phases, Rc=Rc, Vm=Vm)

def solve_Wto(p, tol=0.5, n=500):
    pp = dict(p)
    guess = float(p.get('Wto', 48550))
    lo_b = max(5000, int(guess * 0.3))
    hi_b = min(600000, int(guess * 3.5))
    step = max(500, int((hi_b - lo_b) / 300))
    lo = hi = None
    prev_d = prev_w = None
    for w in range(lo_b, hi_b + step, step):
        pp['Wto'] = float(w)
        d = compute_mission(pp)['diff']
        if prev_d is not None and prev_d * d <= 0:
            lo, hi = float(prev_w), float(w); break
        prev_d, prev_w = d, w
    if lo is None:
        prev_d = prev_w = None
        for w in range(5000, 600001, 1000):
            pp['Wto'] = float(w)
            d = compute_mission(pp)['diff']
            if prev_d is not None and prev_d * d <= 0:
                lo, hi = float(prev_w), float(w); break
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
        else: hi = m
    return m, compute_mission(pp)

def sensitivity(p, Wto):
    RR  = compute_mission({**p, 'Wto': Wto})
    Mff = RR['Mff']; Rc = RR['Rc']; Vm = RR['Vm']
    Wpl = RR['Wpl']; Wcrew = RR['Wcrew']
    C = 1.0 - (1.0 + p['Mr']) * (1.0 - Mff) - p['Mtfo']
    D = Wpl + Wcrew
    dn = C * Wto * (1.0 - p['B']) - D
    F  = (-p['B'] * Wto**2 * (1.0 + p['Mr']) * Mff) / dn if abs(dn) > 1e-6 else 0.0
    E  = p['El']
    return dict(C=C, D=D, F=F,
        dCpR  = F * Rc / (375.0 * p['npc'] * p['LDc']),
        dnpR  = -F * Rc * p['Cpc'] / (375.0 * p['npc']**2 * p['LDc']),
        dLDR  = -F * Rc * p['Cpc'] / (375.0 * p['npc'] * p['LDc']**2),
        dR    = F * p['Cpc'] / (375.0 * p['npc'] * p['LDc']),
        dCpE  = F * E * Vm / (375.0 * p['npl'] * p['LDl']),
        dnpE  = -F * E * Vm * p['Cpl'] / (375.0 * p['npl']**2 * p['LDl']),
        dLDE  = -F * E * Vm * p['Cpl'] / (375.0 * p['npl'] * p['LDl']**2))

# ─────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        '<div class="sb-logo">'
        '<div class="sb-logo-title">Aero<span>Sizer</span></div>'
        '<div class="sb-logo-sub">Raymer Ch.2 — Propeller Weight Estimation</div>'
        '</div>'
        '<div class="sb-stripe"></div>',
        unsafe_allow_html=True)

    st.markdown('<div class="sb-sec">① Cabin & Crew</div>', unsafe_allow_html=True)
    npax  = st.number_input("Passengers",           1,   400,  34,  step=1)
    wpax  = st.number_input("Pax body weight (lbs)",100, 300,  175, step=5)
    wbag  = st.number_input("Baggage weight (lbs)", 0,   100,  30,  step=5)
    ncrew = st.number_input("Flight crew (pilots)", 1,   6,    2,   step=1)
    natt  = st.number_input("Cabin attendants",     0,   10,   1,   step=1)

    st.markdown('<div class="sb-sec">② Cruise Segment</div>', unsafe_allow_html=True)
    R_nm = st.number_input("Design range (nm)",            100, 6000, 1100, step=50)
    LDc  = st.number_input("Cruise L/D",                   4.0, 30.0, 13.0, step=0.5, format="%.1f")
    Cpc  = st.number_input("Cruise SFC Cp (lbs/hp/hr)",    0.20,1.20, 0.60, step=0.01,format="%.2f")
    npc  = st.number_input("Cruise η_p",                   0.30,0.98, 0.85, step=0.01,format="%.2f")

    st.markdown('<div class="sb-sec">③ Loiter / Reserve</div>', unsafe_allow_html=True)
    El   = st.number_input("Loiter endurance E (hr)",      0.10,6.0,  0.75, step=0.05,format="%.2f")
    Vl   = st.number_input("Loiter speed (kts)",           60,  400,  250,  step=5)
    LDl  = st.number_input("Loiter L/D",                   4.0, 30.0, 16.0, step=0.5, format="%.1f")
    Cpl  = st.number_input("Loiter SFC Cp (lbs/hp/hr)",    0.20,1.20, 0.65, step=0.01,format="%.2f")
    npl  = st.number_input("Loiter η_p",                   0.30,0.98, 0.77, step=0.01,format="%.2f")

    st.markdown('<div class="sb-sec">④ Regression Constants (T2.2)</div>', unsafe_allow_html=True)
    A_v  = st.number_input("A (Table 2.15)",               0.0, 2.0,  0.3774,step=0.0001,format="%.4f")
    B_v  = st.number_input("B (Table 2.2/2.15)",           0.1, 2.0,  0.9647,step=0.0001,format="%.4f")

    st.markdown('<div class="sb-sec">⑤ Fuel Allowances & W_TO Guess</div>', unsafe_allow_html=True)
    Mtfo  = st.number_input("M_tfo (trapped fuel)",        0.000,0.05, 0.005,step=0.001,format="%.3f")
    Mres  = st.number_input("M_res (reserve ratio)",       0.000,0.10, 0.000,step=0.001,format="%.3f")
    Wto_g = st.number_input("W_TO initial guess (lbs)",    5000,500000,48550,step=1000)

    st.markdown("<br>", unsafe_allow_html=True)
    calc  = st.button("⟳  Run Sizing", use_container_width=True)

# ─── solve ───
P = dict(npax=int(npax), wpax=float(wpax), wbag=float(wbag),
         ncrew=int(ncrew), natt=int(natt), Mtfo=float(Mtfo), Mr=float(Mres),
         R=float(R_nm), Vl=float(Vl), LDc=float(LDc), Cpc=float(Cpc), npc=float(npc),
         El=float(El), LDl=float(LDl), Cpl=float(Cpl), npl=float(npl),
         A=float(A_v), B=float(B_v), Wto=float(Wto_g))
P_key = str(sorted(P.items()))
if 'res' not in st.session_state or st.session_state.get('_key') != P_key or calc:
    Wto, RR = solve_Wto(P)
    S = sensitivity(P, Wto)
    st.session_state['res'] = (Wto, RR, S)
    st.session_state['_key'] = P_key
else:
    Wto, RR, S = st.session_state['res']

conv     = abs(RR['diff']) < 1.0
WE       = RR['WE'];  WOE = RR['WOE']; WF = RR['WF']
Wpl      = RR['Wpl']; Wcrew = RR['Wcrew']; Wtfo_r = RR['Wtfo']

# ─── sidebar live results ───
with st.sidebar:
    st.markdown('<div class="sb-sec">◉ Live Results</div>', unsafe_allow_html=True)
    c_cls = "conv-ok" if conv else "conv-warn"
    c_txt = "✓ CONVERGED" if conv else "⚠ NOT CONVERGED"
    delta_c = '#3fb950' if conv else '#f85149'
    st.markdown(f"""
    <div style="padding:0 .7rem">
      <div class="sb-kpi">
        <div class="sb-kpi-val">{Wto:,.0f} <span style="font-size:.75rem;font-weight:400;color:#6e7681">lbs</span></div>
        <div class="sb-kpi-lbl">W_TO · Gross Takeoff Weight</div>
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:.4rem;margin:0 0 .5rem">
        <div class="sb-kpi" style="padding:.5rem .7rem;border-top-color:var(--blue2)">
          <div style="font-family:'JetBrains Mono',monospace;font-size:.98rem;font-weight:700;color:#8fb8ff">{RR['Mff']:.4f}</div>
          <div class="sb-kpi-lbl">Mff</div>
        </div>
        <div class="sb-kpi" style="padding:.5rem .7rem;border-top-color:{delta_c}">
          <div style="font-family:'JetBrains Mono',monospace;font-size:.98rem;font-weight:700;color:{delta_c}">{RR['diff']:+.2f}</div>
          <div class="sb-kpi-lbl">ΔW_E (lbs)</div>
        </div>
      </div>
      <div class="conv-pill {c_cls}">{c_txt}</div>
    </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────
# MAIN AREA — Header
# ─────────────────────────────────────────────────────
badge_c = '#3fb950' if conv else '#f85149'
badge_b = 'rgba(63,185,80,.1)' if conv else 'rgba(248,81,73,.08)'
badge_t = '✓ Converged' if conv else '⚠ Not Converged'

st.markdown(f"""
<div class="main-header">
  <div style="position:relative;z-index:1">
    <div class="mh-title">Aero<span>Sizer</span> <span style="font-size:.9rem;font-weight:400;color:#8b949e;font-family:'DM Sans',sans-serif">Pro</span></div>
    <div style="font-size:.62rem;letter-spacing:.08em;text-transform:uppercase;color:#6e7681;margin-top:.25rem">Raymer (2018) Ch.2 · Propeller Aircraft Weight Estimation</div>
  </div>
  <div style="display:flex;align-items:center;gap:1.2rem;position:relative;z-index:1">
    <div style="text-align:right">
      <div style="font-family:'JetBrains Mono',monospace;font-size:1.4rem;font-weight:700;color:var(--gold2)">{Wto:,.0f} <span style="font-size:.72rem;color:#6e7681">lbs</span></div>
      <div style="font-size:.6rem;letter-spacing:.1em;text-transform:uppercase;color:#6e7681">W_TO Gross</div>
    </div>
    <div style="background:{badge_b};color:{badge_c};border:1px solid {badge_c}44;font-family:'JetBrains Mono',monospace;font-size:.68rem;font-weight:700;padding:.3rem .9rem;border-radius:20px;letter-spacing:.06em">{badge_t}</div>
  </div>
</div>""", unsafe_allow_html=True)

# Status bar
if conv:
    st.markdown(f'<div class="status-ok">✓ &nbsp;W_TO = {Wto:,.1f} lbs &nbsp;·&nbsp; Mff = {RR["Mff"]:.6f} &nbsp;·&nbsp; W_E_tent = {WE:,.1f} lbs &nbsp;·&nbsp; W_E_allow = {RR["WEa"]:,.1f} lbs &nbsp;·&nbsp; ΔW_E = {RR["diff"]:+.2f} lbs</div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div class="status-err">⚠ &nbsp;Not converged — ΔW_E = {RR["diff"]:+.0f} lbs. Adjust A, B constants or inputs.</div>', unsafe_allow_html=True)

# KPI row
kpis = [
    (f"{Wto:,.0f}",        "lbs", "W_TO Gross Takeoff", "primary"),
    (f"{RR['Mff']:.5f}",   "",    "Mff Fuel Fraction",   "blue"),
    (f"{WF:,.0f}",         "lbs", "W_F Total Fuel",      "amber"),
    (f"{Wpl:,.0f}",        "lbs", "W_PL Payload",        "green"),
    (f"{WE:,.0f}",         "lbs", "W_E Empty Weight",    ""),
]
cols = st.columns(5)
for col, (val, unit, lbl, cls) in zip(cols, kpis):
    with col:
        vc = "primary" if cls == "primary" else ""
        st.markdown(
            f'<div class="kpi-card {cls}">'
            f'<div class="kpi-val {vc}">{val}<span class="kpi-unit">{unit}</span></div>'
            f'<div class="kpi-lbl">{lbl}</div>'
            f'</div>',
            unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    " ✦ Sizing Steps ",
    " ∂ Sensitivity ",
    " ◎ Charts ",
    " ⬇ Export ",
    " ⊕ References "
])

# ═══════════════════════════════════════════════════
# TAB 1 — SIZING STEPS
# ═══════════════════════════════════════════════════
with tab1:
    col_l, col_r = st.columns([3, 2], gap="medium")

    with col_l:
        # Step 1
        pax_wt  = int(npax) * (int(wpax) + int(wbag))
        crew_wt = int(ncrew) * 205
        att_wt  = int(natt)  * 200
        st.markdown(f"""
        <div class="card card-gold">
          <div class="card-title">Step 1 — Payload & Crew Weights</div>
          <div class="ph-row" style="grid-template-columns:200px 100px 1fr">
            <span class="ph-name">{npax} pax × ({int(wpax)} + {int(wbag)}) lbs</span>
            <span class="ph-frac ph-frac-fixed">{pax_wt:,} lbs</span>
            <span class="ph-src">cabin payload</span>
          </div>
          <div class="ph-row" style="grid-template-columns:200px 100px 1fr">
            <span class="ph-name">{ncrew} pilots × 205 lbs</span>
            <span class="ph-frac ph-frac-fixed">{crew_wt:,} lbs</span>
            <span class="ph-src">flight crew</span>
          </div>
          <div class="ph-row" style="grid-template-columns:200px 100px 1fr">
            <span class="ph-name">{natt} attendant × 200 lbs</span>
            <span class="ph-frac ph-frac-fixed">{att_wt:,} lbs</span>
            <span class="ph-src">cabin crew</span>
          </div>
          <div style="margin-top:.65rem">
            <span class="rpill rpill-gold">W_PL = {Wpl:,.0f} <span class="rpill-unit">lbs</span></span>
            <span class="rpill rpill-blue">W_crew = {Wcrew:,.0f} <span class="rpill-unit">lbs</span></span>
          </div>
        </div>""", unsafe_allow_html=True)

        # Step 2
        st.markdown(f"""
        <div class="card card-blue">
          <div class="card-title">Step 2 — Unit Conversions</div>
          <div class="ph-row" style="grid-template-columns:220px 120px 1fr">
            <span class="ph-name">R_cruise (statute miles)</span>
            <span class="ph-frac ph-frac-fixed">{RR['Rc']:.3f}</span>
            <span class="ph-src">{R_nm} nm × 1.15078</span>
          </div>
          <div class="ph-row" style="grid-template-columns:220px 120px 1fr">
            <span class="ph-name">V_loiter (mph)</span>
            <span class="ph-frac ph-frac-fixed">{RR['Vm']:.2f}</span>
            <span class="ph-src">{Vl} kts × 1.15078</span>
          </div>
          <div class="ph-row" style="grid-template-columns:220px 120px 1fr">
            <span class="ph-name">W_tfo = M_tfo × W_TO</span>
            <span class="ph-frac ph-frac-fixed">{Wtfo_r:,.2f} lbs</span>
            <span class="ph-src">{Mtfo:.3f} × {Wto:,.0f}</span>
          </div>
        </div>""", unsafe_allow_html=True)

        # Step 3 — Mission Phase Fractions
        st.markdown('<div class="card card-blue"><div class="card-title">Step 3 — Mission Phase Weight Fractions</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="ph-hdr">
          <span>Phase</span><span>Wᵢ/Wᵢ₋₁</span><span>Type</span><span>Source</span><span>Cum. Mff</span>
        </div>""", unsafe_allow_html=True)
        cum_mff = 1.0
        for ph, (fv, ftype, fsrc) in RR['phases'].items():
            cum_mff *= fv
            fc = 'ph-frac-breguet' if ftype == 'Breguet' else 'ph-frac-fixed'
            bc = 'ph-badge-breguet' if ftype == 'Breguet' else 'ph-badge-fixed'
            st.markdown(
                f'<div class="ph-row">'
                f'<span class="ph-name">{ph}</span>'
                f'<span class="ph-frac {fc}">{fv:.5f}</span>'
                f'<span class="ph-badge {bc}">{ftype}</span>'
                f'<span class="ph-src">{fsrc}</span>'
                f'<span style="font-family:\'JetBrains Mono\',monospace;font-size:.73rem;color:#8b949e">{cum_mff:.5f}</span>'
                f'</div>',
                unsafe_allow_html=True)
        st.markdown(
            f'<div style="margin-top:.65rem;padding-top:.5rem;border-top:1px solid var(--border2)">'
            f'<span class="rpill rpill-gold">Mff = {RR["Mff"]:.6f}</span>'
            f'<span style="font-size:.68rem;color:#6e7681;margin-left:.4rem">product of all 8 phase fractions</span>'
            f'</div></div>',
            unsafe_allow_html=True)

        # Steps 4–6
        ok_cls = "rpill-green" if conv else "rpill-red"
        st.markdown(f"""
        <div class="card {'card-green' if conv else 'card-red'}">
          <div class="card-title">Steps 4–6 — Weight Build-Up & Convergence</div>
          <div style="display:grid;grid-template-columns:230px 140px 1fr;gap:.5rem;font-size:.6rem;letter-spacing:.08em;text-transform:uppercase;color:var(--text3);padding-bottom:.35rem;border-bottom:1px solid var(--border);font-weight:600">
            <span>Quantity</span><span>Value</span><span>Expression</span>
          </div>
          <div class="ph-row" style="grid-template-columns:230px 140px 1fr"><span class="ph-name">4a — W_F (total fuel)</span><span class="ph-frac ph-frac-fixed">{WF:,.1f} lbs</span><span class="ph-src">W_Fused + W_tfo</span></div>
          <div class="ph-row" style="grid-template-columns:230px 140px 1fr"><span class="ph-name">4b — W_OE (tentative)</span><span class="ph-frac ph-frac-fixed">{WOE:,.1f} lbs</span><span class="ph-src">W_TO − W_F − W_PL</span></div>
          <div class="ph-row" style="grid-template-columns:230px 140px 1fr"><span class="ph-name">5 — W_E (tentative)</span><span class="ph-frac ph-frac-fixed">{WE:,.2f} lbs</span><span class="ph-src">W_OE − W_tfo − W_crew</span></div>
          <div class="ph-row" style="grid-template-columns:230px 140px 1fr"><span class="ph-name">6 — W_E (allowable)</span><span class="ph-frac ph-frac-fixed">{RR['WEa']:,.2f} lbs</span><span class="ph-src">10^[(log W_TO − A) / B]</span></div>
          <div style="margin-top:.65rem">
            <span class="rpill {ok_cls}">ΔW_E = {RR['diff']:+.2f} <span class="rpill-unit">lbs</span></span>
            <span class="rpill {ok_cls}">{'✓ CONVERGED' if conv else '⚠ NOT CONVERGED'}</span>
          </div>
        </div>""", unsafe_allow_html=True)

    with col_r:
        # Equations card
        st.markdown("""
        <div class="card card-gold">
          <div class="card-title">Key Equations — Raymer Ch.2</div>
          <div class="eq-label">Cruise fraction (Eq. 2.9)</div>
          <div class="eq-box">W₅/W₄ = 1 / exp[ Rc / (375·η_p/Cp·L/D) ]</div>
          <div class="eq-label" style="margin-top:.6rem">Loiter fraction (Eq. 2.11)</div>
          <div class="eq-box">W₆/W₅ = 1 / exp[ E / (375·(1/V)·η_p/Cp·L/D) ]</div>
          <div class="eq-label" style="margin-top:.6rem">Regression (Table 2.2 / 2.15)</div>
          <div class="eq-box">log₁₀(W_E) = A + B · log₁₀(W_TO)</div>
          <div style="font-size:.67rem;color:#6e7681;margin-top:.5rem;line-height:1.7">
            R in statute miles &nbsp;·&nbsp; Cp in lbs/hp/hr<br>
            V in mph &nbsp;·&nbsp; E in hours
          </div>
        </div>""", unsafe_allow_html=True)

        # Summary table
        df_sum = pd.DataFrame({
            'Symbol': ['W_TO','Mff','W_F','W_F_used','W_tfo','W_OE','W_E_tent','W_E_allow','ΔW_E','W_PL','W_crew'],
            'Value':  [f"{Wto:,.1f}", f"{RR['Mff']:.6f}", f"{WF:,.1f}", f"{RR['WFu']:,.1f}",
                       f"{Wtfo_r:,.2f}", f"{WOE:,.1f}", f"{WE:,.2f}", f"{RR['WEa']:,.2f}",
                       f"{RR['diff']:+.2f}", f"{Wpl:,.1f}", f"{Wcrew:,.1f}"],
            'Unit':   ['lbs','—','lbs','lbs','lbs','lbs','lbs','lbs','lbs','lbs','lbs']})
        st.dataframe(df_sum, hide_index=True, use_container_width=True, height=410,
            column_config={
                'Symbol': st.column_config.TextColumn('Symbol', width='small'),
                'Value':  st.column_config.TextColumn('Value',  width='medium'),
                'Unit':   st.column_config.TextColumn('Unit',   width='small'),
            })

        # Weight ratios
        ratio_rows = []
        for name, val_r, lo_r, hi_r in [
            ('W_PL/W_TO', Wpl/Wto, 0.10, 0.25),
            ('W_F/W_TO',  WF/Wto,  0.20, 0.45),
            ('W_E/W_TO',  WE/Wto,  0.45, 0.65),
            ('W_PL/W_E',  Wpl/WE,  0.15, 0.40)]:
            ok_r = lo_r <= val_r <= hi_r
            ratio_rows.append({
                'Ratio': name, 'Value': f'{val_r:.4f}',
                'Typical': f'{lo_r:.2f}–{hi_r:.2f}',
                'Status': '✓' if ok_r else ('▲' if val_r > hi_r else '▼')})
        st.dataframe(pd.DataFrame(ratio_rows), hide_index=True, use_container_width=True,
            column_config={
                'Ratio':   st.column_config.TextColumn('Ratio',   width='small'),
                'Value':   st.column_config.TextColumn('Value',   width='small'),
                'Typical': st.column_config.TextColumn('Typical', width='small'),
                'Status':  st.column_config.TextColumn('Status',  width='small'),
            })

# ═══════════════════════════════════════════════════
# TAB 2 — SENSITIVITY
# ═══════════════════════════════════════════════════
with tab2:
    s1, s2 = st.columns([1, 1], gap="medium")

    with s1:
        st.markdown(f"""
        <div class="card card-gold">
          <div class="card-title">Intermediate Factors — Eq 2.22–2.44</div>
          <div class="sens-row" style="grid-template-columns:250px 1fr">
            <span class="sens-partial">C = 1−(1+M_res)(1−Mff)−M_tfo</span>
            <span style="font-family:'JetBrains Mono',monospace;font-size:.82rem;font-weight:700;color:var(--gold2)">{S['C']:.5f} <span style="font-size:.64rem;color:#6e7681">Eq 2.22</span></span>
          </div>
          <div class="sens-row" style="grid-template-columns:250px 1fr">
            <span class="sens-partial">D = W_PL + W_crew</span>
            <span style="font-family:'JetBrains Mono',monospace;font-size:.82rem;font-weight:700;color:var(--gold2)">{S['D']:,.0f} lbs <span style="font-size:.64rem;color:#6e7681">Eq 2.23</span></span>
          </div>
          <div class="sens-row" style="grid-template-columns:250px 1fr">
            <span class="sens-partial">C(1−B)W_TO − D</span>
            <span style="font-family:'JetBrains Mono',monospace;font-size:.82rem;font-weight:700;color:var(--amber)">{S['C']*(1-float(B_v))*Wto-S['D']:,.0f}</span>
          </div>
          <div class="sens-row" style="grid-template-columns:250px 1fr;border-bottom:none">
            <span class="sens-partial">F (sizing multiplier, Eq 2.44)</span>
            <span style="font-family:'JetBrains Mono',monospace;font-size:.82rem;font-weight:700;color:var(--pu)">{S['F']:,.0f} lbs</span>
          </div>
        </div>""", unsafe_allow_html=True)

        st.markdown('<div class="card card-blue"><div class="card-title">Cruise Segment Sensitivities</div>', unsafe_allow_html=True)
        for partial, val, unit, eq in [
            ('∂W_TO/∂Cp (cruise)', S['dCpR'], 'lbs/(lbs/hp/hr)', 'Eq 2.49'),
            ('∂W_TO/∂η_p (cruise)',S['dnpR'], 'lbs',             'Eq 2.50'),
            ('∂W_TO/∂(L/D) cruise',S['dLDR'], 'lbs',             'Eq 2.51'),
            ('∂W_TO/∂R',          S['dR'],   'lbs/nm',          'Eq 2.45')]:
            vc = 'sens-neg' if val < 0 else 'sens-pos'
            st.markdown(
                f'<div class="sens-row">'
                f'<span class="sens-partial">{partial}</span>'
                f'<span class="{vc}">{val:+,.1f}</span>'
                f'<span class="sens-unit">{unit}</span>'
                f'<span class="sens-eq">{eq}</span>'
                f'</div>',
                unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with s2:
        # Range trade chart
        ranges = list(range(int(R_nm) - 400, int(R_nm) + 401, 50))
        wto_vals = []
        for r in ranges:
            pp2 = {**P, 'R': float(r)}
            w2, _ = solve_Wto(pp2)
            wto_vals.append(w2)

        fig_r = go.Figure()
        fig_r.add_trace(go.Scatter(
            x=ranges, y=wto_vals,
            mode='lines+markers',
            line=dict(color='#c8a86c', width=2.5),
            marker=dict(color='#e4c88a', size=5,
                        line=dict(color='#c8a86c', width=1)),
            fill='tozeroy',
            fillcolor='rgba(200,168,108,.06)',
            name='W_TO'
        ))
        fig_r.add_vline(x=R_nm, line=dict(color='rgba(200,168,108,.5)', width=1.5, dash='dash'))
        fig_r.add_annotation(x=R_nm, y=max(wto_vals)*0.85,
            text=f"Current: {R_nm} nm",
            font=dict(color='#c8a86c', size=11, family='JetBrains Mono'),
            showarrow=False, bgcolor='rgba(7,9,13,.8)',
            bordercolor='rgba(200,168,108,.3)', borderwidth=1)
        fig_r.update_layout(
            title=dict(text="W_TO vs Design Range", font=dict(color='#c8a86c', size=13, family='DM Serif Display')),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(12,15,22,0.6)',
            font=dict(family='JetBrains Mono', color='#8b949e', size=10),
            xaxis=dict(title='Range (nm)', gridcolor='rgba(255,255,255,.04)',
                       linecolor='rgba(255,255,255,.1)', tickfont=dict(size=9)),
            yaxis=dict(title='W_TO (lbs)', gridcolor='rgba(255,255,255,.04)',
                       linecolor='rgba(255,255,255,.1)', tickfont=dict(size=9)),
            margin=dict(l=10, r=10, t=40, b=10), height=320,
            showlegend=False
        )
        st.plotly_chart(fig_r, use_container_width=True)

        st.markdown(f"""
        <div class="card card-amber">
          <div class="card-title">Range Trade Study · ∂W_TO/∂R = {S['dR']:+.2f} lbs/nm</div>""",
          unsafe_allow_html=True)
        for dr in [-200, -100, +100, +200]:
            dw = S['dR'] * dr
            col_v = '#3fb950' if dw < 0 else '#e3b341'
            st.markdown(
                f'<div style="display:flex;justify-content:space-between;align-items:center;'
                f'padding:.3rem 0;border-bottom:1px solid var(--border2);font-size:.8rem">'
                f'<span style="color:#8b949e">ΔR = {dr:+d} nm</span>'
                f'<span style="font-family:JetBrains Mono,monospace;font-weight:700;color:{col_v}">{dw:+,.1f} lbs</span>'
                f'</div>',
                unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════
# TAB 3 — CHARTS
# ═══════════════════════════════════════════════════
with tab3:
    DARK_LAYOUT = dict(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(12,15,22,0.6)',
        font=dict(family='JetBrains Mono', color='#8b949e', size=10),
        margin=dict(l=10, r=10, t=45, b=10),
    )
    AXIS = dict(gridcolor='rgba(255,255,255,.04)', linecolor='rgba(255,255,255,.1)',
                tickfont=dict(size=9))

    # ── Chart 1: Phase fractions + cumulative ──
    st.markdown('<div class="sec-div">Mission Phase Weight Fractions</div>', unsafe_allow_html=True)
    phases_l = list(RR['phases'].keys())
    fvals    = [v for v, _, _ in RR['phases'].values()]
    ftypes   = [t for _, t, _ in RR['phases'].values()]
    cum_p    = [1.0]
    for fv in fvals:
        cum_p.append(cum_p[-1] * fv)

    bar_colors = ['#6a9eea' if t == 'Fixed' else '#c8a86c' for t in ftypes]
    fig1 = make_subplots(rows=1, cols=2, subplot_titles=["Wᵢ/Wᵢ₋₁ per Phase", "Cumulative Mff"])
    fig1.add_trace(go.Bar(
        x=phases_l, y=fvals, marker_color=bar_colors,
        marker_line=dict(width=0), name='Phase fraction',
        text=[f'{v:.4f}' for v in fvals], textposition='outside',
        textfont=dict(size=9, color='#8b949e')), row=1, col=1)
    fig1.add_trace(go.Scatter(
        x=['Ramp'] + phases_l, y=cum_p,
        mode='lines+markers',
        line=dict(color='#c8a86c', width=2.5),
        marker=dict(color='#e4c88a', size=7, line=dict(color='#c8a86c', width=1.5)),
        fill='tozeroy', fillcolor='rgba(200,168,108,.07)',
        name='Cum. Mff'), row=1, col=2)
    fig1.update_layout(**DARK_LAYOUT, height=360, showlegend=False)
    fig1.update_xaxes(**AXIS); fig1.update_yaxes(**AXIS)
    fig1.update_annotations(font=dict(color='#c8a86c', size=11, family='DM Serif Display'))
    st.plotly_chart(fig1, use_container_width=True)

    # ── Chart 2: Weight breakdown waterfall ──
    st.markdown('<div class="sec-div">Weight Breakdown</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        fig2 = go.Figure(go.Waterfall(
            orientation='v',
            measure=['absolute','relative','relative','relative','relative'],
            x=['W_TO', '− W_F', '− W_PL', '− W_tfo', '− W_crew'],
            y=[Wto, -WF, -Wpl, -Wtfo_r, -Wcrew],
            text=[f'{Wto:,.0f}', f'{WF:,.0f}', f'{Wpl:,.0f}', f'{Wtfo_r:,.0f}', f'{Wcrew:,.0f}'],
            textposition='outside', textfont=dict(size=9, color='#8b949e'),
            connector=dict(line=dict(color='rgba(200,168,108,.3)', width=1)),
            increasing=dict(marker=dict(color='rgba(200,168,108,.7)')),
            decreasing=dict(marker=dict(color='rgba(106,158,234,.7)')),
            totals=dict(marker=dict(color='rgba(63,185,80,.7)'))))
        fig2.update_layout(**DARK_LAYOUT, title=dict(text='Takeoff Weight Breakdown',
            font=dict(color='#c8a86c', size=12, family='DM Serif Display')),
            height=360, yaxis=dict(**AXIS, title='Weight (lbs)'), xaxis=dict(**AXIS))
        st.plotly_chart(fig2, use_container_width=True)

    with c2:
        labels = ['W_F (Fuel)', 'W_PL (Payload)', 'W_tfo (Trapped)', 'W_crew', 'W_E (Empty)']
        values = [WF, Wpl, Wtfo_r, Wcrew, WE]
        fig3 = go.Figure(go.Pie(
            labels=labels, values=values,
            hole=0.55,
            marker=dict(colors=['#c8a86c','#6a9eea','#e3b341','#9c72d4','#3fb950'],
                        line=dict(color='#07090d', width=2)),
            textfont=dict(size=10, family='JetBrains Mono'),
            hovertemplate='<b>%{label}</b><br>%{value:,.0f} lbs<br>%{percent}<extra></extra>'))
        fig3.add_annotation(text=f'<b>{Wto:,.0f}</b><br>lbs W_TO',
            xref='paper', yref='paper', x=0.5, y=0.5,
            font=dict(size=11, color='#c8a86c', family='JetBrains Mono'),
            showarrow=False, align='center')
        fig3.update_layout(**DARK_LAYOUT, title=dict(text='Weight Composition',
            font=dict(color='#c8a86c', size=12, family='DM Serif Display')),
            height=360, showlegend=True,
            legend=dict(font=dict(size=9, color='#8b949e'),
                        bgcolor='rgba(0,0,0,0)'))
        st.plotly_chart(fig3, use_container_width=True)

    # ── Chart 3: Sensitivity tornado ──
    st.markdown('<div class="sec-div">Sensitivity Analysis — Tornado Chart</div>', unsafe_allow_html=True)
    sens_params = [
        ('∂W_TO/∂Cp cruise',  S['dCpR'],  'lbs/(lbs/hp/hr)'),
        ('∂W_TO/∂η_p cruise', S['dnpR'],  'lbs'),
        ('∂W_TO/∂(L/D) cr.',  S['dLDR'],  'lbs'),
        ('∂W_TO/∂R',          S['dR'],    'lbs/nm'),
        ('∂W_TO/∂Cp loiter',  S['dCpE'],  'lbs/(lbs/hp/hr)'),
        ('∂W_TO/∂η_p loiter', S['dnpE'],  'lbs'),
        ('∂W_TO/∂(L/D) loit.',S['dLDE'],  'lbs'),
    ]
    sorted_s = sorted(sens_params, key=lambda x: abs(x[1]), reverse=True)
    labels_s = [x[0] for x in sorted_s]
    vals_s   = [x[1] for x in sorted_s]
    colors_s = ['rgba(248,81,73,.75)' if v > 0 else 'rgba(63,185,80,.75)' for v in vals_s]

    fig4 = go.Figure(go.Bar(
        y=labels_s, x=vals_s, orientation='h',
        marker_color=colors_s, marker_line=dict(width=0),
        text=[f'{v:+,.1f}' for v in vals_s],
        textposition='outside',
        textfont=dict(size=9, color='#8b949e')))
    fig4.add_vline(x=0, line=dict(color='rgba(255,255,255,.15)', width=1))
    fig4.update_layout(**DARK_LAYOUT, title=dict(text='Sensitivity Tornado — dW_TO/dX',
        font=dict(color='#c8a86c', size=12, family='DM Serif Display')),
        height=340, xaxis=dict(**AXIS, title='dW_TO (lbs per unit change)'),
        yaxis=dict(**AXIS))
    st.plotly_chart(fig4, use_container_width=True)

    # ── Chart 4: Convergence visualization ──
    st.markdown('<div class="sec-div">Convergence — W_E Tent. vs W_E Allow.</div>', unsafe_allow_html=True)
    wto_range = np.linspace(Wto * 0.6, Wto * 1.4, 120)
    we_tent   = []
    we_allow  = []
    for w in wto_range:
        try:
            rr_tmp = compute_mission({**P, 'Wto': float(w)})
            we_tent.append(rr_tmp['WE'])
            we_allow.append(rr_tmp['WEa'])
        except:
            we_tent.append(None)
            we_allow.append(None)

    fig5 = go.Figure()
    fig5.add_trace(go.Scatter(x=list(wto_range), y=we_tent,
        mode='lines', name='W_E Tentative',
        line=dict(color='#6a9eea', width=2.5)))
    fig5.add_trace(go.Scatter(x=list(wto_range), y=we_allow,
        mode='lines', name='W_E Allowable',
        line=dict(color='#c8a86c', width=2.5)))
    fig5.add_vline(x=Wto, line=dict(color='rgba(63,185,80,.6)', width=1.5, dash='dash'),
        annotation_text=f'W_TO = {Wto:,.0f} lbs',
        annotation_font=dict(color='#3fb950', size=10, family='JetBrains Mono'))
    fig5.update_layout(**DARK_LAYOUT, title=dict(text='Sizing Convergence — Intersection = Solution',
        font=dict(color='#c8a86c', size=12, family='DM Serif Display')),
        height=340,
        xaxis=dict(**AXIS, title='W_TO (lbs)'),
        yaxis=dict(**AXIS, title='W_E (lbs)'),
        legend=dict(font=dict(size=10, color='#8b949e'), bgcolor='rgba(0,0,0,0)'))
    st.plotly_chart(fig5, use_container_width=True)

# ═══════════════════════════════════════════════════
# TAB 4 — EXPORT
# ═══════════════════════════════════════════════════
with tab4:
    ex1, ex2 = st.columns([1, 1], gap="medium")

    with ex1:
        st.markdown('<div class="sec-div">CSV Export</div>', unsafe_allow_html=True)
        rows = {
            'Parameter': ['W_TO','Mff','W_F','W_F_usable','W_tfo','W_OE','W_E_tent','W_E_allow',
                          'delta_WE','W_PL','W_crew','Rc_sm','Vm_mph','F','C','D'],
            'Value':     [Wto, RR['Mff'], WF, RR['WFu'], Wtfo_r, WOE, WE, RR['WEa'],
                          RR['diff'], Wpl, Wcrew, RR['Rc'], RR['Vm'], S['F'], S['C'], S['D']],
            'Units':     ['lbs','—','lbs','lbs','lbs','lbs','lbs','lbs','lbs','lbs','lbs',
                          's.m.','mph','—','—','lbs']}
        df_export = pd.DataFrame(rows)
        st.dataframe(df_export, hide_index=True, use_container_width=True,
            column_config={
                'Parameter': st.column_config.TextColumn('Parameter', width='medium'),
                'Value':     st.column_config.NumberColumn('Value', format='%.4f'),
                'Units':     st.column_config.TextColumn('Units', width='small'),
            })
        b = io.StringIO()
        df_export.to_csv(b, index=False)
        st.download_button("⬇  Full Results (CSV)", b.getvalue(),
                           "aerosizer_results.csv", "text/csv",
                           use_container_width=True)

    with ex2:
        st.markdown('<div class="sec-div">PDF Report</div>', unsafe_allow_html=True)

        def make_pdf():
            buf = io.BytesIO()
            doc = SimpleDocTemplate(buf, pagesize=A4,
                leftMargin=2.0*cm, rightMargin=2.0*cm,
                topMargin=2.2*cm,  bottomMargin=2.2*cm)
            PW = 17.0*cm

            # Colors matching the app palette
            CN  = colors.HexColor('#0D1B2A')
            CG  = colors.HexColor('#c8a86c')   # gold
            CB  = colors.HexColor('#4875c2')   # blue
            CS  = colors.HexColor('#6a9eea')   # blue2
            CGr = colors.HexColor('#475569')
            CL  = colors.HexColor('#94A3B8')
            CR  = colors.HexColor('#E2E8F0')
            CF  = colors.HexColor('#F8FAFF')
            CW  = colors.white
            CGreen = colors.HexColor('#3fb950')
            CAmber = colors.HexColor('#e3b341')
            CRed   = colors.HexColor('#f85149')

            sty = getSampleStyleSheet()
            def ps(nm, **kw):
                return ParagraphStyle(nm, parent=sty['Normal'], **kw)

            sH1  = ps('H1',  fontSize=10, fontName='Helvetica-Bold', textColor=CG,  spaceBefore=12, spaceAfter=4)
            sH2  = ps('H2',  fontSize=8,  fontName='Helvetica-Bold', textColor=CB,  spaceBefore=8,  spaceAfter=3)
            sSUB = ps('SU',  fontSize=8,  textColor=CGr, leading=12, spaceAfter=2)
            sEQ  = ps('EQ',  fontSize=8,  fontName='Courier', textColor=CS, leading=12, spaceAfter=3,
                       backColor=colors.HexColor('#0D1B2A'), leftIndent=8, rightIndent=8,
                       spaceBefore=2)

            def ts(hdr=CN, alt=CF):
                return TableStyle([
                    ('BACKGROUND',  (0,0), (-1,0),  hdr),
                    ('TEXTCOLOR',   (0,0), (-1,0),  CW),
                    ('FONTNAME',    (0,0), (-1,0),  'Helvetica-Bold'),
                    ('FONTNAME',    (0,1), (-1,-1), 'Helvetica'),
                    ('FONTSIZE',    (0,0), (-1,-1), 7.5),
                    ('LEADING',     (0,0), (-1,-1), 11),
                    ('TEXTCOLOR',   (0,1), (-1,-1), CGr),
                    ('ROWBACKGROUNDS', (0,1), (-1,-1), [CW, alt]),
                    ('GRID',        (0,0), (-1,-1), 0.25, CR),
                    ('LINEBELOW',   (0,0), (-1,0),  0.8,  CG),
                    ('LEFTPADDING', (0,0), (-1,-1), 6),
                    ('RIGHTPADDING',(0,0), (-1,-1), 6),
                    ('TOPPADDING',  (0,0), (-1,-1), 3.5),
                    ('BOTTOMPADDING',(0,0),(-1,-1), 3.5),
                    ('VALIGN',      (0,0), (-1,-1), 'MIDDLE'),
                ])

            story = []

            # ── Header ──
            hd = Table([[
                Paragraph('<b>AEROSIZER PRO</b>',
                    ps('TX', fontSize=17, fontName='Helvetica-Bold', textColor=CN, leading=22)),
                Paragraph(f'STATUS: {"CONVERGED" if conv else "DRAFT"}<br/>W_TO = {Wto:,.1f} lbs',
                    ps('TX2', fontSize=7.5, textColor=CL, leading=11, alignment=TA_RIGHT))
            ]], colWidths=[PW*0.60, PW*0.40])
            story.append(hd)
            story.append(HRFlowable(width=PW, thickness=2.5, color=CG, spaceBefore=5, spaceAfter=3))
            story.append(Paragraph('Preliminary Aircraft Weight Sizing — Raymer (2018) Ch.2', sSUB))
            story.append(Spacer(1, 0.3*cm))

            # ── Convergence status ──
            sc = CGreen if conv else CRed
            cv_tbl = Table([[Paragraph(
                f'{"✓ CONVERGED" if conv else "⚠ NOT CONVERGED"} — '
                f'ΔW_E = {RR["diff"]:+.2f} lbs | Mff = {RR["Mff"]:.6f}',
                ps('CV', fontSize=8, fontName='Helvetica-Bold', textColor=sc))]],
                colWidths=[PW])
            cv_tbl.setStyle(TableStyle([
                ('BACKGROUND',(0,0),(0,0), colors.HexColor('#0f2010' if conv else '#200f0f')),
                ('LINEBELOW',(0,0),(0,0),1.5,sc),
                ('LEFTPADDING',(0,0),(-1,-1),8),
                ('TOPPADDING',(0,0),(-1,-1),5),
                ('BOTTOMPADDING',(0,0),(-1,-1),5),
            ]))
            story.append(cv_tbl)
            story.append(Spacer(1, 0.3*cm))

            # ── Section 1: Inputs ──
            story.append(Paragraph('1  Mission Inputs', sH1))
            t_in = Table([
                ['Parameter','Value','Parameter','Value'],
                ['Passengers', str(int(npax)), 'Design range (nm)', str(int(R_nm))],
                ['Pax weight (lbs)', str(int(wpax)), 'Baggage (lbs)', str(int(wbag))],
                ['Flight crew', str(int(ncrew)), 'Cabin attendants', str(int(natt))],
                ['Cruise L/D', f'{LDc:.1f}', 'Loiter L/D', f'{LDl:.1f}'],
                ['Cruise Cp', f'{Cpc:.2f}', 'Loiter Cp', f'{Cpl:.2f}'],
                ['Cruise η_p', f'{npc:.2f}', 'Loiter η_p', f'{npl:.2f}'],
                ['Loiter E (hr)', f'{El:.2f}', 'Loiter V (kts)', str(int(Vl))],
                ['A (regression)', f'{A_v:.4f}', 'B (regression)', f'{B_v:.4f}'],
                ['M_tfo', f'{Mtfo:.3f}', 'M_res', f'{Mres:.3f}'],
            ], colWidths=[PW*0.3, PW*0.2, PW*0.3, PW*0.2])
            t_in.setStyle(ts(hdr=CN)); story.append(t_in)
            story.append(Spacer(1, 0.3*cm))

            # ── Section 2: Key Equations ──
            story.append(Paragraph('2  Key Equations (Raymer Ch.2)', sH1))
            story.append(Paragraph('Cruise fraction (Eq. 2.9):', sH2))
            story.append(Paragraph('W5/W4 = 1 / exp[ Rc / (375 * np/Cp * L/D) ]', sEQ))
            story.append(Paragraph('Loiter fraction (Eq. 2.11):', sH2))
            story.append(Paragraph('W6/W5 = 1 / exp[ E / (375 * (1/V) * np/Cp * L/D) ]', sEQ))
            story.append(Paragraph('Regression line (Table 2.2/2.15):', sH2))
            story.append(Paragraph('log10(W_E) = A + B * log10(W_TO)', sEQ))
            story.append(Spacer(1, 0.3*cm))

            # ── Section 3: Mission phases ──
            story.append(Paragraph('3  Mission Phase Weight Fractions', sH1))
            ph_data = [['Phase', 'Wᵢ/Wᵢ₋₁', 'Type', 'Source', 'Cum. Mff']]
            cm2 = 1.0
            for ph_name, (fv, ftype, fsrc) in RR['phases'].items():
                cm2 *= fv
                ph_data.append([ph_name, f'{fv:.5f}', ftype, fsrc, f'{cm2:.5f}'])
            ph_data.append(['—', '—', '—', 'Mff Product', f'{RR["Mff"]:.6f}'])
            t_ph = Table(ph_data, colWidths=[PW*0.22, PW*0.14, PW*0.14, PW*0.14, PW*0.16])
            t_ph.setStyle(ts(hdr=CN)); story.append(t_ph)
            story.append(Spacer(1, 0.3*cm))

            # ── Section 4: Sizing results ──
            story.append(Paragraph('4  Sizing Results', sH1))
            t_res = Table([
                ['Quantity', 'Value (lbs)', 'Expression'],
                ['W_TO (Gross Takeoff)', f'{Wto:,.2f}', 'Sizing solution'],
                ['W_F (Total Fuel)',     f'{WF:,.2f}',  'W_Fused + W_tfo'],
                ['W_F_used',            f'{RR["WFu"]:,.2f}', 'W_TO(1−Mff)'],
                ['W_tfo (Trapped)',      f'{Wtfo_r:,.2f}', f'M_tfo × W_TO = {Mtfo:.3f}×'],
                ['W_OE (Operating)',     f'{WOE:,.2f}', 'W_TO − W_F − W_PL'],
                ['W_E (Tentative)',      f'{WE:,.2f}',  'W_OE − W_tfo − W_crew'],
                ['W_E (Allowable)',      f'{RR["WEa"]:,.2f}', '10^[(log W_TO − A)/B]'],
                ['ΔW_E (Convergence)',   f'{RR["diff"]:+.2f}', 'W_E_allow − W_E_tent'],
                ['W_PL (Payload)',       f'{Wpl:,.2f}', f'{npax} pax × ({wpax}+{wbag}) lbs'],
                ['W_crew',              f'{Wcrew:,.2f}', f'{ncrew} pilots + {natt} att.'],
            ], colWidths=[PW*0.35, PW*0.2, PW*0.45])
            t_res.setStyle(ts(hdr=colors.HexColor('#0a1628'))); story.append(t_res)
            story.append(Spacer(1, 0.3*cm))

            # ── Section 5: Weight ratios ──
            story.append(Paragraph('5  Weight Ratios & Sanity Check', sH1))
            ratio_data = [['Ratio', 'Value', 'Typical Range', 'Status']]
            for nm, vr, lo_r, hi_r in [
                ('W_PL/W_TO', Wpl/Wto, 0.10, 0.25),
                ('W_F/W_TO',  WF/Wto,  0.20, 0.45),
                ('W_E/W_TO',  WE/Wto,  0.45, 0.65),
                ('W_PL/W_E',  Wpl/WE,  0.15, 0.40)]:
                ok_r = lo_r <= vr <= hi_r
                ratio_data.append([nm, f'{vr:.4f}', f'{lo_r:.2f}–{hi_r:.2f}',
                                   '✓ OK' if ok_r else ('▲ High' if vr > hi_r else '▼ Low')])
            t_rat = Table(ratio_data, colWidths=[PW*0.3, PW*0.2, PW*0.25, PW*0.25])
            t_rat.setStyle(ts(hdr=colors.HexColor('#0a1628'))); story.append(t_rat)
            story.append(Spacer(1, 0.3*cm))

            # ── Section 6: Sensitivity ──
            story.append(Paragraph('6  Sensitivity Analysis', sH1))
            sens_data = [['Partial Derivative', 'Value', 'Units', 'Equation']]
            for partial, val, unit, eq in [
                ('∂W_TO/∂Cp (cruise)',  S['dCpR'], 'lbs/(lbs/hp/hr)', 'Eq 2.49'),
                ('∂W_TO/∂η_p (cruise)', S['dnpR'], 'lbs',             'Eq 2.50'),
                ('∂W_TO/∂(L/D) cruise', S['dLDR'], 'lbs',             'Eq 2.51'),
                ('∂W_TO/∂R',           S['dR'],   'lbs/nm',          'Eq 2.45'),
                ('∂W_TO/∂Cp (loiter)', S['dCpE'], 'lbs/(lbs/hp/hr)', 'Eq 2.49'),
                ('∂W_TO/∂η_p (loiter)',S['dnpE'], 'lbs',             'Eq 2.50'),
                ('∂W_TO/∂(L/D) loiter',S['dLDE'], 'lbs',             'Eq 2.51')]:
                sens_data.append([partial, f'{val:+,.2f}', unit, eq])
            t_sen = Table(sens_data, colWidths=[PW*0.38, PW*0.18, PW*0.26, PW*0.18])
            t_sen.setStyle(ts(hdr=colors.HexColor('#0a1628'))); story.append(t_sen)

            # ── Footer ──
            story.append(Spacer(1, 0.4*cm))
            story.append(HRFlowable(width=PW, thickness=0.5, color=CG, spaceBefore=4, spaceAfter=4))
            story.append(Paragraph(
                f'AeroSizer Pro &nbsp;·&nbsp; Raymer (2018) Aircraft Design: A Conceptual Approach &nbsp;·&nbsp; '
                f'W_TO = {Wto:,.1f} lbs &nbsp;·&nbsp; Mff = {RR["Mff"]:.6f}',
                ps('FT', fontSize=6.5, textColor=CL, alignment=TA_CENTER)))

            doc.build(story)
            buf.seek(0)
            return buf.read()

        st.download_button(
            "⬇  Generate & Download PDF (A4)", make_pdf(),
            "aerosizer_report.pdf", "application/pdf",
            use_container_width=True)

# ═══════════════════════════════════════════════════
# TAB 5 — REFERENCES
# ═══════════════════════════════════════════════════
with tab5:
    refs = [
        ("Eq 2.9",  "Cruise Phase — Breguet Range Equation",
         "W₅/W₄ = 1 / exp[ Rc / (375·η_p/Cp·L/D) ]",
         "R in statute miles, Cp in lbs/hp/hr, propeller efficiency η_p dimensionless"),
        ("Eq 2.11", "Loiter Phase — Breguet Endurance Equation",
         "W₆/W₅ = 1 / exp[ E / (375·(1/V)·η_p/Cp·L/D) ]",
         "E in hours, V in mph, other units same as cruise"),
        ("T2.1",    "Fixed Phase Weight Fractions (Table 2.1)",
         "Engine Start=0.990, Taxi=0.995, T/O=0.995, Climb=0.985, Descent=0.985, Landing=0.995",
         "Typical values for propeller-driven transport aircraft"),
        ("T2.2/2.15","Regression Constants — Empty Weight Fraction",
         "log₁₀(W_E) = A + B · log₁₀(W_TO)",
         "A, B from Table 2.2 (Raymer 2018) — aircraft-class specific"),
        ("Eq 2.22", "Fuel fraction coefficient C",
         "C = 1 − (1 + M_res)(1 − Mff) − M_tfo",
         "Captures reserve fuel and trapped fuel allowances"),
        ("Eq 2.44", "Sizing multiplier F",
         "F = −B·W_TO²·(1+M_res)·Mff / [C·(1−B)·W_TO − D]",
         "Central factor linking all sensitivity derivatives"),
    ]
    r1, r2 = st.columns(2)
    for i, (code, title, eq, note) in enumerate(refs):
        col = r1 if i % 2 == 0 else r2
        with col:
            st.markdown(f"""
            <div class="card card-gold">
              <div class="card-title">{code} — {title}</div>
              <div class="eq-box">{eq}</div>
              <div style="font-size:.7rem;color:#6e7681;margin-top:.35rem;line-height:1.65">{note}</div>
            </div>""", unsafe_allow_html=True)
