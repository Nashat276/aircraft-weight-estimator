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

# ─── PAGE CONFIG ───
st.set_page_config(page_title="AeroSizer Pro", page_icon="✈", layout="wide",
                   initial_sidebar_state="expanded")

st.markdown("""<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-T8JSQMHD');</script>""", unsafe_allow_html=True)

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&family=DM+Sans:wght@300;400;500;600;700&family=DM+Serif+Display:ital@0;1&display=swap');

:root {
  --bg:#07090d; --sur:#0c0f16; --pan:#111720; --pan2:#161d2a;
  --border:rgba(255,255,255,.07); --border2:rgba(255,255,255,.04);
  --gold:#c8a86c; --gold2:#e4c88a; --gold3:rgba(200,168,108,.08);
  --blue:#4875c2; --blue2:#6a9eea; --blue3:#8fb8ff;
  --green:#3fb950; --amber:#e3b341; --red:#f85149; --pu:#9c72d4;
  --text:#b0bcce; --text2:#8b949e; --text3:#6e7681; --white:#f0ede6;
}
*,*::before,*::after{box-sizing:border-box;}
html,body,[class*="css"]{background:var(--bg)!important;color:var(--text)!important;font-family:'DM Sans',sans-serif!important;}
.stApp{background:var(--bg)!important;}
.main .block-container{padding:.75rem 1.2rem 2rem!important;max-width:100%!important;}

/* Mobile */
@media(max-width:768px){
  .main .block-container{padding:.5rem .7rem 1.5rem!important;}
  .kpi-grid{grid-template-columns:1fr 1fr!important;}
  .ph-row{grid-template-columns:1fr 1fr!important;font-size:.73rem!important;}
  .ph-hdr{display:none!important;}
  .sens-row{grid-template-columns:1fr 1fr!important;}
  .main-header{flex-direction:column!important;gap:.6rem!important;}
  .eq-box{font-size:.7rem!important;}
}
@media(max-width:480px){
  .kpi-grid{grid-template-columns:1fr!important;}
  .sb-kpi-val{font-size:1.1rem!important;}
}

::-webkit-scrollbar{width:4px;height:4px;}
::-webkit-scrollbar-track{background:var(--bg);}
::-webkit-scrollbar-thumb{background:rgba(200,168,108,.3);border-radius:4px;}

/* ── SIDEBAR ── */
[data-testid="stSidebar"]{background:var(--sur)!important;border-right:1px solid var(--border)!important;padding:0!important;}
[data-testid="stSidebar"]>div:first-child{padding:0!important;}
.sb-logo{padding:1.3rem 1.1rem .9rem;border-bottom:1px solid var(--border);background:linear-gradient(150deg,#06090f,#0c1220);position:relative;overflow:hidden;}
.sb-logo::before{content:'';position:absolute;inset:0;background-image:linear-gradient(rgba(72,117,194,.04) 1px,transparent 1px),linear-gradient(90deg,rgba(72,117,194,.04) 1px,transparent 1px);background-size:20px 20px;pointer-events:none;}
.sb-logo-title{font-family:'DM Serif Display',serif;font-size:1.25rem;color:var(--white);letter-spacing:-.03em;line-height:1;position:relative;z-index:1;}
.sb-logo-title span{background:linear-gradient(135deg,var(--gold),var(--gold2));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.sb-logo-sub{font-family:'JetBrains Mono',monospace;font-size:.52rem;letter-spacing:.18em;text-transform:uppercase;color:var(--text3);margin-top:.3rem;position:relative;z-index:1;}
.sb-stripe{height:2px;background:linear-gradient(90deg,var(--blue),var(--gold),var(--blue));background-size:200%;animation:stripe 4s linear infinite;}
@keyframes stripe{0%{background-position:0%;}100%{background-position:200%;}}
.sb-sec{font-family:'JetBrains Mono',monospace;font-size:.57rem;font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:var(--gold);padding:.55rem 1rem .3rem;border-bottom:1px solid var(--border2);margin:.35rem 0 .45rem;display:flex;align-items:center;gap:.45rem;}
.sb-sec::before{content:'';width:8px;height:1px;background:var(--gold);flex-shrink:0;}
[data-testid="stSidebar"] label{font-family:'DM Sans',sans-serif!important;font-size:.76rem!important;font-weight:500!important;color:var(--text)!important;}
[data-testid="stSidebar"] .stNumberInput input{background:var(--pan)!important;border:1px solid var(--border)!important;border-radius:7px!important;color:var(--white)!important;font-family:'JetBrains Mono',monospace!important;font-size:.81rem!important;}
[data-testid="stSidebar"] .stNumberInput input:focus{border-color:var(--gold)!important;box-shadow:0 0 0 2px rgba(200,168,108,.18)!important;}
[data-testid="stSidebar"] div.stButton>button{background:linear-gradient(135deg,var(--gold),var(--gold2))!important;color:#07090d!important;border:none!important;border-radius:9px!important;font-size:.83rem!important;font-weight:700!important;padding:.65rem!important;width:100%!important;letter-spacing:.04em;box-shadow:0 4px 18px rgba(200,168,108,.28)!important;transition:all .22s!important;}
[data-testid="stSidebar"] div.stButton>button:hover{transform:translateY(-1px)!important;box-shadow:0 6px 24px rgba(200,168,108,.4)!important;}
.sb-kpi{background:var(--pan);border:1px solid var(--border);border-top:2px solid var(--gold);border-radius:9px;padding:.7rem .9rem;margin:0 .65rem .45rem;}
.sb-kpi-val{font-family:'JetBrains Mono',monospace;font-size:1.45rem;font-weight:700;color:var(--gold2);line-height:1.1;}
.sb-kpi-lbl{font-size:.58rem;letter-spacing:.1em;text-transform:uppercase;color:var(--text3);margin-top:.18rem;}
.conv-pill{display:inline-flex;align-items:center;gap:.35rem;border-radius:20px;padding:.22rem .78rem;font-family:'JetBrains Mono',monospace;font-size:.64rem;font-weight:700;letter-spacing:.05em;margin-top:.5rem;}
.conv-ok{background:rgba(63,185,80,.1);border:1px solid rgba(63,185,80,.28);color:#3fb950;}
.conv-warn{background:rgba(248,81,73,.09);border:1px solid rgba(248,81,73,.28);color:#f85149;}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"]{background:var(--sur)!important;border:1px solid var(--border)!important;border-radius:11px!important;padding:4px!important;gap:3px!important;margin-bottom:1.1rem!important;}
.stTabs [data-baseweb="tab"]{border-radius:8px!important;font-family:'DM Sans',sans-serif!important;font-size:.78rem!important;font-weight:500!important;color:var(--text2)!important;padding:.42rem 1rem!important;transition:all .2s!important;}
.stTabs [aria-selected="true"]{background:linear-gradient(135deg,var(--gold),var(--gold2))!important;color:#07090d!important;font-weight:700!important;box-shadow:0 2px 10px rgba(200,168,108,.32)!important;}

/* ── CARDS ── */
.card{background:var(--sur);border:1px solid var(--border);border-radius:12px;padding:1.1rem 1.25rem;margin-bottom:.9rem;position:relative;overflow:hidden;}
.card::after{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(255,255,255,.05),transparent);pointer-events:none;}
.card-gold{border-left:2px solid var(--gold);}
.card-blue{border-left:2px solid var(--blue2);}
.card-green{border-left:2px solid var(--green);}
.card-amber{border-left:2px solid var(--amber);}
.card-red{border-left:2px solid var(--red);}
.card-title{font-family:'JetBrains Mono',monospace;font-size:.57rem;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--gold);padding-bottom:.48rem;border-bottom:1px solid var(--border2);margin-bottom:.75rem;display:flex;align-items:center;gap:.45rem;}
.card-title::before{content:'';width:8px;height:1px;background:var(--gold);flex-shrink:0;}

/* ── EQUATIONS ── */
.eq-box{background:rgba(200,168,108,.06);border:1px solid rgba(200,168,108,.18);border-radius:8px;padding:.48rem .9rem;font-family:'JetBrains Mono',monospace;font-size:.79rem;color:var(--gold2);display:block;margin-bottom:.45rem;white-space:nowrap;overflow-x:auto;letter-spacing:.01em;}
.eq-label{font-size:.7rem;color:var(--text2);margin-bottom:.28rem;font-weight:500;}

/* ── RESULT PILLS ── */
.rpill{display:inline-flex;align-items:baseline;gap:.25rem;border-radius:7px;padding:.2rem .72rem;font-family:'JetBrains Mono',monospace;font-size:.84rem;font-weight:700;margin-right:.38rem;margin-top:.32rem;}
.rpill-gold{background:rgba(200,168,108,.1);border:1px solid rgba(200,168,108,.26);color:var(--gold2);}
.rpill-blue{background:rgba(72,117,194,.1);border:1px solid rgba(106,158,234,.26);color:var(--blue3);}
.rpill-green{background:rgba(63,185,80,.1);border:1px solid rgba(63,185,80,.26);color:var(--green);}
.rpill-red{background:rgba(248,81,73,.1);border:1px solid rgba(248,81,73,.26);color:var(--red);}
.rpill-unit{font-size:.62rem;font-weight:400;opacity:.6;}

/* ── TABLE ROWS ── */
.ph-hdr{display:grid;grid-template-columns:145px 90px 75px 75px 1fr;gap:.45rem;padding:.22rem 0 .38rem;font-size:.59rem;letter-spacing:.08em;text-transform:uppercase;color:var(--text3);border-bottom:1px solid var(--border);font-weight:700;}
.ph-row{display:grid;grid-template-columns:145px 90px 75px 75px 1fr;gap:.45rem;align-items:center;padding:.38rem 0;border-bottom:1px solid var(--border2);font-size:.79rem;transition:background .15s;border-radius:5px;}
.ph-row:last-child{border-bottom:none;}
.ph-row:hover{background:rgba(200,168,108,.04);padding-left:.3rem;padding-right:.3rem;}
.ph-name{font-weight:500;color:var(--text);}
.ph-frac{font-family:'JetBrains Mono',monospace;font-weight:700;}
.ph-frac-fixed{color:var(--blue3);}
.ph-frac-breguet{color:var(--gold2);}
.ph-badge{font-size:.59rem;font-weight:700;letter-spacing:.05em;text-transform:uppercase;padding:.1rem .48rem;border-radius:4px;width:fit-content;}
.ph-badge-fixed{background:rgba(72,117,194,.1);color:var(--blue3);border:1px solid rgba(72,117,194,.2);}
.ph-badge-breguet{background:rgba(200,168,108,.1);color:var(--gold);border:1px solid rgba(200,168,108,.2);}
.ph-src{font-size:.64rem;color:var(--text3);font-family:'JetBrains Mono',monospace;}

/* ── SENSITIVITY ── */
.sens-row{display:grid;grid-template-columns:210px 110px 155px 68px;gap:.45rem;align-items:center;padding:.36rem 0;border-bottom:1px solid var(--border2);transition:background .15s;border-radius:5px;}
.sens-row:hover{background:rgba(200,168,108,.04);padding-left:.3rem;padding-right:.3rem;}
.sens-row:last-child{border-bottom:none;}
.sens-partial{font-family:'JetBrains Mono',monospace;font-size:.75rem;color:var(--text);}
.sens-pos{font-family:'JetBrains Mono',monospace;font-size:.81rem;font-weight:700;color:var(--red);}
.sens-neg{font-family:'JetBrains Mono',monospace;font-size:.81rem;font-weight:700;color:var(--green);}
.sens-unit{font-size:.63rem;color:var(--text3);}
.sens-eq{font-size:.61rem;color:var(--gold);font-family:'JetBrains Mono',monospace;}

/* ── STATUS ── */
.status-ok{background:rgba(63,185,80,.06);border:1px solid rgba(63,185,80,.16);border-left:3px solid var(--green);border-radius:0 9px 9px 0;padding:.52rem 1.1rem;margin-bottom:.9rem;font-family:'JetBrains Mono',monospace;font-size:.75rem;color:var(--green);}
.status-err{background:rgba(248,81,73,.05);border:1px solid rgba(248,81,73,.16);border-left:3px solid var(--red);border-radius:0 9px 9px 0;padding:.52rem 1.1rem;margin-bottom:.9rem;font-family:'JetBrains Mono',monospace;font-size:.75rem;color:var(--red);}

/* ── KPI ── */
.kpi-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:.7rem;margin-bottom:1rem;}
.kpi-card{background:var(--sur);border:1px solid var(--border);border-top:2px solid var(--border);border-radius:11px;padding:.9rem 1rem;transition:transform .2s,border-color .2s;}
.kpi-card:hover{transform:translateY(-2px);border-color:rgba(200,168,108,.22);}
.kpi-card.primary{border-top:2px solid var(--gold);background:rgba(200,168,108,.04);}
.kpi-card.green{border-top:2px solid var(--green);}
.kpi-card.amber{border-top:2px solid var(--amber);}
.kpi-card.blue{border-top:2px solid var(--blue2);}
.kpi-val{font-family:'JetBrains Mono',monospace;font-size:1.45rem;font-weight:700;color:var(--white);line-height:1.1;}
.kpi-val.primary{color:var(--gold2);font-size:1.6rem;}
.kpi-unit{font-size:.63rem;font-weight:400;color:var(--text3);margin-left:2px;}
.kpi-lbl{font-size:.57rem;letter-spacing:.09em;text-transform:uppercase;color:var(--text3);margin-top:.26rem;font-weight:500;}

/* ── SECTION DIV ── */
.sec-div{font-family:'JetBrains Mono',monospace;font-size:.59rem;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:var(--gold);border-bottom:1px solid var(--border);padding-bottom:.38rem;margin:.7rem 0 .85rem;display:flex;align-items:center;gap:.45rem;}
.sec-div::before{content:'';width:8px;height:1px;background:var(--gold);flex-shrink:0;}

/* ── MAIN HEADER ── */
.main-header{background:var(--sur);border:1px solid var(--border);border-radius:12px;border-left:3px solid var(--gold);padding:.85rem 1.4rem;margin-bottom:1rem;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:.8rem;position:relative;overflow:hidden;}
.main-header::before{content:'';position:absolute;inset:0;background-image:linear-gradient(rgba(200,168,108,.025) 1px,transparent 1px),linear-gradient(90deg,rgba(200,168,108,.025) 1px,transparent 1px);background-size:32px 32px;pointer-events:none;}
.mh-title{font-family:'DM Serif Display',serif;font-size:1.35rem;color:var(--white);letter-spacing:-.03em;line-height:1;position:relative;z-index:1;}
.mh-title span{background:linear-gradient(135deg,var(--gold),var(--gold2));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}

/* ── DATAFRAME ── */
[data-testid="stDataFrame"]{border:1px solid var(--border)!important;border-radius:10px!important;overflow:hidden!important;}
[data-testid="stDataFrame"] *{background-color:transparent!important;}
[data-testid="stDataFrame"] table{border-collapse:collapse!important;width:100%!important;}
[data-testid="stDataFrame"] thead tr th{background:var(--pan2)!important;color:var(--gold)!important;font-family:'JetBrains Mono',monospace!important;font-size:.66rem!important;font-weight:700!important;letter-spacing:.1em!important;text-transform:uppercase!important;border-bottom:1.5px solid rgba(200,168,108,.28)!important;padding:.48rem .75rem!important;}
[data-testid="stDataFrame"] tbody td{font-family:'JetBrains Mono',monospace!important;font-size:.77rem!important;color:var(--text)!important;border-color:var(--border2)!important;padding:.38rem .75rem!important;line-height:1.4!important;}
[data-testid="stDataFrame"] tbody tr:nth-child(odd) td{background:rgba(255,255,255,.012)!important;}
[data-testid="stDataFrame"] tbody tr:nth-child(even) td{background:rgba(255,255,255,.024)!important;}
[data-testid="stDataFrame"] tbody tr:hover td{background:rgba(200,168,108,.06)!important;color:var(--white)!important;}
[data-testid="stDataFrame"] tbody td:first-child{color:var(--text2)!important;font-size:.72rem!important;}
[data-testid="stDataFrame"] ::-webkit-scrollbar{height:3px!important;}
[data-testid="stDataFrame"] ::-webkit-scrollbar-thumb{background:rgba(200,168,108,.22)!important;}

/* ── DOWNLOAD ── */
div.stDownloadButton>button{background:var(--pan)!important;color:var(--gold)!important;border:1px solid rgba(200,168,108,.22)!important;border-radius:8px!important;font-size:.79rem!important;font-weight:600!important;padding:.52rem 1rem!important;width:100%!important;transition:all .2s!important;}
div.stDownloadButton>button:hover{border-color:var(--gold)!important;color:var(--white)!important;background:rgba(200,168,108,.1)!important;transform:translateY(-1px)!important;}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# PHYSICS — Exact Raymer Ch.2, verified equations
# ═══════════════════════════════════════════════════════
def compute_mission(p):
    """
    Raymer (2018) Ch.2 fuel-fraction weight sizing for propeller aircraft.
    All units as specified: R in nm (converted internally), V in kts,
    Cp in lbs/hp/hr, E in hours.
    """
    Wpl   = p['npax'] * (p['wpax'] + p['wbag'])
    Wcrew = (p['ncrew'] + p['natt']) * 205
    Wtfo  = p['Wto'] * p['Mtfo']

    # Unit conversions required by Raymer equations
    Rc = p['R']  * 1.15078    # nm → statute miles
    Vm = p['Vl'] * 1.15078    # knots → mph

    # Eq. 2.9 — Breguet cruise weight fraction (propeller)
    W5 = 1.0 / math.exp(Rc / (375.0 * (p['npc'] / p['Cpc']) * p['LDc']))

    # Eq. 2.11 — Breguet loiter weight fraction (propeller)
    W6 = 1.0 / math.exp(p['El'] / (375.0 * (1.0 / Vm) * (p['npl'] / p['Cpl']) * p['LDl']))

    # Table 2.1 — Fixed phase fractions
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

    # Fuel weights
    WFu  = p['Wto'] * (1.0 - Mff)
    WF   = WFu * (1.0 + p['Mr'])

    WOE  = p['Wto'] - WF - Wpl
    WE   = WOE - Wtfo - Wcrew

    # Regression: log10(W_E) = A + B*log10(W_TO)
    WEa  = 10.0 ** ((math.log10(p['Wto']) - p['A']) / p['B'])

    return dict(
        Wpl=Wpl, Wcrew=Wcrew, Wtfo=Wtfo, Mff=Mff,
        WF=WF, WFu=WFu, WOE=WOE, WE=WE, WEa=WEa,
        diff=WEa - WE,
        phases=phases, Rc=Rc, Vm=Vm
    )


def solve_Wto(p, tol=0.5, n=500):
    """Bisection solver: find W_TO where W_E_tent = W_E_allow (diff=0)."""
    pp = dict(p)
    guess = float(p.get('Wto', 48550))
    lo_b = max(5000,   int(guess * 0.3))
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
    """
    Raymer Eq. 2.22–2.51 partial derivatives ∂W_TO/∂X.
    F is the central sizing multiplier (Eq. 2.44).
    """
    RR  = compute_mission({**p, 'Wto': Wto})
    Mff = RR['Mff']; Rc = RR['Rc']; Vm = RR['Vm']
    Wpl = RR['Wpl']; Wcrew = RR['Wcrew']

    C  = 1.0 - (1.0 + p['Mr']) * (1.0 - Mff) - p['Mtfo']
    D  = Wpl + Wcrew
    dn = C * Wto * (1.0 - p['B']) - D
    F  = (-p['B'] * Wto**2 * (1.0 + p['Mr']) * Mff) / dn if abs(dn) > 1e-6 else 0.0

    return dict(C=C, D=D, F=F,
        dCpR  =  F * Rc                          / (375.0 * p['npc']               * p['LDc']),
        dnpR  = -F * Rc  * p['Cpc']              / (375.0 * p['npc']**2            * p['LDc']),
        dLDR  = -F * Rc  * p['Cpc']              / (375.0 * p['npc']               * p['LDc']**2),
        dR    =  F        * p['Cpc']              / (375.0 * p['npc']               * p['LDc']),
        dCpE  =  F * p['El'] * Vm                / (375.0 * p['npl']               * p['LDl']),
        dnpE  = -F * p['El'] * Vm * p['Cpl']     / (375.0 * p['npl']**2            * p['LDl']),
        dLDE  = -F * p['El'] * Vm * p['Cpl']     / (375.0 * p['npl']               * p['LDl']**2),
    )

# ═══════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(
        '<div class="sb-logo">'
        '<div class="sb-logo-title">Aero<span>Sizer</span></div>'
        '<div class="sb-logo-sub">Raymer Ch.2 · Propeller Weight Estimation</div>'
        '</div><div class="sb-stripe"></div>',
        unsafe_allow_html=True)

    st.markdown('<div class="sb-sec">① Cabin & Crew</div>', unsafe_allow_html=True)
    npax  = st.number_input("Passengers",            1,   400,  34,     step=1)
    wpax  = st.number_input("Pax body weight (lbs)", 100, 300,  175,    step=5)
    wbag  = st.number_input("Baggage (lbs)",         0,   100,  30,     step=5)
    ncrew = st.number_input("Flight crew (pilots)",  1,   6,    2,      step=1)
    natt  = st.number_input("Cabin attendants",      0,   10,   1,      step=1)

    st.markdown('<div class="sb-sec">② Cruise Segment</div>', unsafe_allow_html=True)
    R_nm = st.number_input("Design range (nm)",           100, 6000, 1100, step=50)
    LDc  = st.number_input("Cruise L/D",                  4.0, 30.0, 13.0, step=0.5, format="%.1f")
    Cpc  = st.number_input("Cruise SFC Cp (lbs/hp/hr)",   0.20,1.20, 0.60, step=0.01,format="%.2f")
    npc  = st.number_input("Cruise η_p",                  0.30,0.98, 0.85, step=0.01,format="%.2f")

    st.markdown('<div class="sb-sec">③ Loiter / Reserve</div>', unsafe_allow_html=True)
    El   = st.number_input("Loiter endurance E (hr)",     0.10,6.0,  0.75, step=0.05,format="%.2f")
    Vl   = st.number_input("Loiter speed (kts)",          60,  400,  250,  step=5)
    LDl  = st.number_input("Loiter L/D",                  4.0, 30.0, 16.0, step=0.5, format="%.1f")
    Cpl  = st.number_input("Loiter SFC Cp (lbs/hp/hr)",   0.20,1.20, 0.65, step=0.01,format="%.2f")
    npl  = st.number_input("Loiter η_p",                  0.30,0.98, 0.77, step=0.01,format="%.2f")

    st.markdown('<div class="sb-sec">④ Regression Constants</div>', unsafe_allow_html=True)
    A_v  = st.number_input("A  (Table 2.15)",             0.0, 2.0,  0.3774,step=0.0001,format="%.4f")
    B_v  = st.number_input("B  (Table 2.2 / 2.15)",       0.1, 2.0,  0.9647,step=0.0001,format="%.4f")

    st.markdown('<div class="sb-sec">⑤ Fuel Allowances</div>', unsafe_allow_html=True)
    Mtfo  = st.number_input("M_tfo (trapped fuel)",       0.000,0.05, 0.005,step=0.001,format="%.3f")
    Mres  = st.number_input("M_res (reserve fraction)",   0.000,0.10, 0.000,step=0.001,format="%.3f")
    Wto_g = st.number_input("W_TO initial guess (lbs)",   5000,500000,48550,step=1000)

    st.markdown("<br>", unsafe_allow_html=True)
    calc = st.button("⟳  Run Sizing", use_container_width=True)

# ─── Solve ───
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

conv   = abs(RR['diff']) < 1.0
WE     = RR['WE'];  WOE = RR['WOE']; WF = RR['WF']
Wpl    = RR['Wpl']; Wcrew = RR['Wcrew']; Wtfo_r = RR['Wtfo']

# ─── Sidebar live KPIs ───
with st.sidebar:
    st.markdown('<div class="sb-sec">◉ Live Results</div>', unsafe_allow_html=True)
    dc = '#3fb950' if conv else '#f85149'
    st.markdown(f"""
    <div style="padding:0 .65rem">
      <div class="sb-kpi">
        <div class="sb-kpi-val">{Wto:,.0f} <span style="font-size:.72rem;font-weight:400;color:#6e7681">lbs</span></div>
        <div class="sb-kpi-lbl">W_TO · Gross Takeoff Weight</div>
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:.38rem;margin:0 0 .45rem">
        <div class="sb-kpi" style="padding:.48rem .7rem;border-top-color:var(--blue2)">
          <div style="font-family:'JetBrains Mono',monospace;font-size:.96rem;font-weight:700;color:var(--blue3)">{RR['Mff']:.4f}</div>
          <div class="sb-kpi-lbl">Mff</div>
        </div>
        <div class="sb-kpi" style="padding:.48rem .7rem;border-top-color:{dc}">
          <div style="font-family:'JetBrains Mono',monospace;font-size:.96rem;font-weight:700;color:{dc}">{RR['diff']:+.2f}</div>
          <div class="sb-kpi-lbl">ΔW_E (lbs)</div>
        </div>
      </div>
      <div class="conv-pill {'conv-ok' if conv else 'conv-warn'}">{'✓ CONVERGED' if conv else '⚠ NOT CONVERGED'}</div>
    </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# MAIN AREA
# ═══════════════════════════════════════════════════════
bc = '#3fb950' if conv else '#f85149'
bb = 'rgba(63,185,80,.08)' if conv else 'rgba(248,81,73,.07)'
bt = '✓ Converged' if conv else '⚠ Not Converged'

st.markdown(f"""
<div class="main-header">
  <div style="position:relative;z-index:1">
    <div class="mh-title">Aero<span>Sizer</span> <span style="font-size:.88rem;font-weight:400;color:#8b949e;font-family:'DM Sans',sans-serif">Pro</span></div>
    <div style="font-size:.6rem;letter-spacing:.08em;text-transform:uppercase;color:#6e7681;margin-top:.22rem">Raymer (2018) Ch.2 · Propeller Aircraft Conceptual Weight Sizing</div>
  </div>
  <div style="display:flex;align-items:center;gap:1rem;flex-wrap:wrap;position:relative;z-index:1">
    <div style="text-align:right">
      <div style="font-family:'JetBrains Mono',monospace;font-size:1.38rem;font-weight:700;color:var(--gold2)">{Wto:,.0f} <span style="font-size:.7rem;color:#6e7681">lbs</span></div>
      <div style="font-size:.58rem;letter-spacing:.1em;text-transform:uppercase;color:#6e7681">W_TO Gross</div>
    </div>
    <div style="background:{bb};color:{bc};border:1px solid {bc}44;font-family:'JetBrains Mono',monospace;font-size:.66rem;font-weight:700;padding:.28rem .85rem;border-radius:20px;letter-spacing:.06em">{bt}</div>
  </div>
</div>""", unsafe_allow_html=True)

if conv:
    st.markdown(f'<div class="status-ok">✓ &nbsp;W_TO = {Wto:,.1f} lbs &nbsp;·&nbsp; Mff = {RR["Mff"]:.6f} &nbsp;·&nbsp; W_E_tent = {WE:,.1f} lbs &nbsp;·&nbsp; W_E_allow = {RR["WEa"]:,.1f} lbs &nbsp;·&nbsp; ΔW_E = {RR["diff"]:+.2f} lbs</div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div class="status-err">⚠ &nbsp;Not converged — ΔW_E = {RR["diff"]:+.0f} lbs. Adjust A, B regression constants or check inputs.</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="kpi-grid">
  <div class="kpi-card primary"><div class="kpi-val primary">{Wto:,.0f}<span class="kpi-unit">lbs</span></div><div class="kpi-lbl">W_TO Gross</div></div>
  <div class="kpi-card blue"><div class="kpi-val">{RR['Mff']:.5f}</div><div class="kpi-lbl">Mff Fuel Frac.</div></div>
  <div class="kpi-card amber"><div class="kpi-val">{WF:,.0f}<span class="kpi-unit">lbs</span></div><div class="kpi-lbl">W_F Total Fuel</div></div>
  <div class="kpi-card green"><div class="kpi-val">{Wpl:,.0f}<span class="kpi-unit">lbs</span></div><div class="kpi-lbl">W_PL Payload</div></div>
  <div class="kpi-card"><div class="kpi-val">{WE:,.0f}<span class="kpi-unit">lbs</span></div><div class="kpi-lbl">W_E Empty</div></div>
</div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# TABS
# ═══════════════════════════════════════════════════════
tab1, tab2, tab3, tab4 = st.tabs([
    " ✦ Sizing Steps ",
    " ∂ Sensitivity ",
    " ◎ Charts ",
    " ⬇ Export PDF / CSV ",
])

# ───────────────────────────────────────────────────────
# TAB 1 — Sizing Steps
# ───────────────────────────────────────────────────────
with tab1:
    cL, cR = st.columns([3, 2], gap="medium")

    with cL:
        pax_wt  = int(npax) * (int(wpax) + int(wbag))
        crew_wt = int(ncrew) * 205
        att_wt  = int(natt)  * 200
        st.markdown(f"""
        <div class="card card-gold">
          <div class="card-title">Step 1 — Payload & Crew Weights</div>
          <div class="ph-row" style="grid-template-columns:210px 100px 1fr">
            <span class="ph-name">{npax} pax × ({int(wpax)} + {int(wbag)}) lbs</span>
            <span class="ph-frac ph-frac-fixed">{pax_wt:,} lbs</span>
            <span class="ph-src">cabin payload</span>
          </div>
          <div class="ph-row" style="grid-template-columns:210px 100px 1fr">
            <span class="ph-name">{ncrew} pilots × 205 lbs</span>
            <span class="ph-frac ph-frac-fixed">{crew_wt:,} lbs</span>
            <span class="ph-src">flight crew</span>
          </div>
          <div class="ph-row" style="grid-template-columns:210px 100px 1fr">
            <span class="ph-name">{natt} attendant(s) × 200 lbs</span>
            <span class="ph-frac ph-frac-fixed">{att_wt:,} lbs</span>
            <span class="ph-src">cabin crew</span>
          </div>
          <div style="margin-top:.6rem">
            <span class="rpill rpill-gold">W_PL = {Wpl:,.0f} <span class="rpill-unit">lbs</span></span>
            <span class="rpill rpill-blue">W_crew = {Wcrew:,.0f} <span class="rpill-unit">lbs</span></span>
          </div>
        </div>""", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="card card-blue">
          <div class="card-title">Step 2 — Unit Conversions (Raymer uses statute miles & mph)</div>
          <div class="ph-row" style="grid-template-columns:220px 115px 1fr">
            <span class="ph-name">R_cruise (statute miles)</span>
            <span class="ph-frac ph-frac-fixed">{RR['Rc']:.3f}</span>
            <span class="ph-src">{R_nm} nm × 1.15078</span>
          </div>
          <div class="ph-row" style="grid-template-columns:220px 115px 1fr">
            <span class="ph-name">V_loiter (mph)</span>
            <span class="ph-frac ph-frac-fixed">{RR['Vm']:.2f}</span>
            <span class="ph-src">{Vl} kts × 1.15078</span>
          </div>
          <div class="ph-row" style="grid-template-columns:220px 115px 1fr">
            <span class="ph-name">W_tfo = M_tfo × W_TO</span>
            <span class="ph-frac ph-frac-fixed">{Wtfo_r:,.2f} lbs</span>
            <span class="ph-src">{Mtfo:.3f} × {Wto:,.0f}</span>
          </div>
        </div>""", unsafe_allow_html=True)

        st.markdown('<div class="card card-blue"><div class="card-title">Step 3 — Mission Phase Weight Fractions (Raymer Table 2.1 + Breguet)</div>', unsafe_allow_html=True)
        st.markdown("""<div class="ph-hdr"><span>Phase</span><span>Wᵢ/Wᵢ₋₁</span><span>Type</span><span>Source</span><span>Cumulative Mff</span></div>""", unsafe_allow_html=True)
        cum = 1.0
        for ph, (fv, ft, fs) in RR['phases'].items():
            cum *= fv
            fc  = 'ph-frac-breguet' if ft == 'Breguet' else 'ph-frac-fixed'
            bc2 = 'ph-badge-breguet' if ft == 'Breguet' else 'ph-badge-fixed'
            st.markdown(
                f'<div class="ph-row"><span class="ph-name">{ph}</span>'
                f'<span class="ph-frac {fc}">{fv:.5f}</span>'
                f'<span class="ph-badge {bc2}">{ft}</span>'
                f'<span class="ph-src">{fs}</span>'
                f'<span style="font-family:\'JetBrains Mono\',monospace;font-size:.72rem;color:#8b949e">{cum:.5f}</span></div>',
                unsafe_allow_html=True)
        st.markdown(
            f'<div style="margin-top:.6rem;padding-top:.48rem;border-top:1px solid var(--border2)">'
            f'<span class="rpill rpill-gold">Mff = {RR["Mff"]:.6f}</span>'
            f'<span style="font-size:.67rem;color:#6e7681;margin-left:.4rem">product of all 8 phase fractions</span>'
            f'</div></div>', unsafe_allow_html=True)

        ok = "rpill-green" if conv else "rpill-red"
        st.markdown(f"""
        <div class="card {'card-green' if conv else 'card-red'}">
          <div class="card-title">Steps 4–6 — Weight Build-Up & Convergence Check</div>
          <div style="display:grid;grid-template-columns:235px 140px 1fr;gap:.45rem;font-size:.59rem;letter-spacing:.08em;text-transform:uppercase;color:var(--text3);padding-bottom:.32rem;border-bottom:1px solid var(--border);font-weight:700"><span>Quantity</span><span>Value</span><span>Expression</span></div>
          <div class="ph-row" style="grid-template-columns:235px 140px 1fr"><span class="ph-name">4a — W_F (total fuel)</span><span class="ph-frac ph-frac-fixed">{WF:,.1f} lbs</span><span class="ph-src">W_TO·(1−Mff)·(1+M_res)</span></div>
          <div class="ph-row" style="grid-template-columns:235px 140px 1fr"><span class="ph-name">4b — W_OE (operating empty)</span><span class="ph-frac ph-frac-fixed">{WOE:,.1f} lbs</span><span class="ph-src">W_TO − W_F − W_PL</span></div>
          <div class="ph-row" style="grid-template-columns:235px 140px 1fr"><span class="ph-name">5 — W_E (tentative)</span><span class="ph-frac ph-frac-fixed">{WE:,.2f} lbs</span><span class="ph-src">W_OE − W_tfo − W_crew</span></div>
          <div class="ph-row" style="grid-template-columns:235px 140px 1fr"><span class="ph-name">6 — W_E (allowable, regression)</span><span class="ph-frac ph-frac-fixed">{RR['WEa']:,.2f} lbs</span><span class="ph-src">10^[(log W_TO − A) / B]</span></div>
          <div style="margin-top:.6rem">
            <span class="rpill {ok}">ΔW_E = {RR['diff']:+.2f} <span class="rpill-unit">lbs</span></span>
            <span class="rpill {ok}">{'✓ CONVERGED' if conv else '⚠ NOT CONVERGED'}</span>
          </div>
        </div>""", unsafe_allow_html=True)

    with cR:
        st.markdown("""
        <div class="card card-gold">
          <div class="card-title">Key Equations — Raymer Ch.2</div>
          <div class="eq-label">Cruise fraction (Eq. 2.9) — Breguet</div>
          <div class="eq-box">W₅/W₄ = 1 / exp[ Rc / (375·η_p/Cp·L/D) ]</div>
          <div class="eq-label" style="margin-top:.55rem">Loiter fraction (Eq. 2.11) — Breguet</div>
          <div class="eq-box">W₆/W₅ = 1 / exp[ E·V / (375·η_p/Cp·L/D) ]</div>
          <div class="eq-label" style="margin-top:.55rem">Regression line (Table 2.2 / 2.15)</div>
          <div class="eq-box">log₁₀(W_E) = A + B · log₁₀(W_TO)</div>
          <div style="font-size:.65rem;color:#6e7681;margin-top:.45rem;line-height:1.72">
            R in <b style="color:#8b949e">statute miles</b> &nbsp;·&nbsp;
            Cp in <b style="color:#8b949e">lbs/hp/hr</b><br>
            V in <b style="color:#8b949e">mph</b> &nbsp;·&nbsp;
            E in <b style="color:#8b949e">hours</b> &nbsp;·&nbsp;
            η_p dimensionless
          </div>
        </div>""", unsafe_allow_html=True)

        df_sum = pd.DataFrame({
            'Symbol':  ['W_TO','Mff','W_F','W_F_used','W_tfo','W_OE','W_E_tent','W_E_allow','ΔW_E','W_PL','W_crew'],
            'Value':   [f"{Wto:,.1f}", f"{RR['Mff']:.6f}", f"{WF:,.1f}", f"{RR['WFu']:,.1f}",
                        f"{Wtfo_r:,.2f}", f"{WOE:,.1f}", f"{WE:,.2f}", f"{RR['WEa']:,.2f}",
                        f"{RR['diff']:+.2f}", f"{Wpl:,.1f}", f"{Wcrew:,.1f}"],
            'Unit':    ['lbs','—','lbs','lbs','lbs','lbs','lbs','lbs','lbs','lbs','lbs']})
        st.dataframe(df_sum, hide_index=True, use_container_width=True, height=405,
            column_config={
                'Symbol': st.column_config.TextColumn('Symbol', width='small'),
                'Value':  st.column_config.TextColumn('Value',  width='medium'),
                'Unit':   st.column_config.TextColumn('Unit',   width='small'),
            })

        ratio_rows = []
        for nm, vr, lo_r, hi_r in [
            ('W_PL / W_TO', Wpl/Wto, 0.10, 0.25),
            ('W_F  / W_TO', WF/Wto,  0.20, 0.45),
            ('W_E  / W_TO', WE/Wto,  0.45, 0.65),
            ('W_PL / W_E',  Wpl/WE,  0.15, 0.40)]:
            ok_r = lo_r <= vr <= hi_r
            ratio_rows.append({'Ratio': nm, 'Value': f'{vr:.4f}',
                'Range': f'{lo_r:.2f}–{hi_r:.2f}',
                'Check': '✓' if ok_r else ('▲' if vr > hi_r else '▼')})
        st.dataframe(pd.DataFrame(ratio_rows), hide_index=True, use_container_width=True,
            column_config={
                'Ratio': st.column_config.TextColumn('Ratio', width='small'),
                'Value': st.column_config.TextColumn('Value', width='small'),
                'Range': st.column_config.TextColumn('Typical', width='small'),
                'Check': st.column_config.TextColumn('✓', width='small'),
            })

# ───────────────────────────────────────────────────────
# TAB 2 — Sensitivity
# ───────────────────────────────────────────────────────
with tab2:
    s1, s2 = st.columns([1, 1], gap="medium")

    with s1:
        st.markdown(f"""
        <div class="card card-gold">
          <div class="card-title">Intermediate Factors — Eq 2.22–2.44</div>
          <div class="sens-row" style="grid-template-columns:255px 1fr">
            <span class="sens-partial">C = 1−(1+M_res)(1−Mff)−M_tfo</span>
            <span style="font-family:'JetBrains Mono',monospace;font-size:.82rem;font-weight:700;color:var(--gold2)">{S['C']:.5f} <span style="font-size:.63rem;color:#6e7681">Eq 2.22</span></span>
          </div>
          <div class="sens-row" style="grid-template-columns:255px 1fr">
            <span class="sens-partial">D = W_PL + W_crew</span>
            <span style="font-family:'JetBrains Mono',monospace;font-size:.82rem;font-weight:700;color:var(--gold2)">{S['D']:,.0f} lbs <span style="font-size:.63rem;color:#6e7681">Eq 2.23</span></span>
          </div>
          <div class="sens-row" style="grid-template-columns:255px 1fr">
            <span class="sens-partial">C(1−B)W_TO − D  (denominator)</span>
            <span style="font-family:'JetBrains Mono',monospace;font-size:.82rem;font-weight:700;color:var(--amber)">{S['C']*(1-float(B_v))*Wto-S['D']:,.0f}</span>
          </div>
          <div class="sens-row" style="grid-template-columns:255px 1fr;border-bottom:none">
            <span class="sens-partial">F (sizing multiplier, Eq 2.44)</span>
            <span style="font-family:'JetBrains Mono',monospace;font-size:.82rem;font-weight:700;color:var(--pu)">{S['F']:,.0f} lbs</span>
          </div>
        </div>""", unsafe_allow_html=True)

        st.markdown('<div class="card card-blue"><div class="card-title">Cruise Segment Partial Derivatives</div>', unsafe_allow_html=True)
        for partial, val, unit, eq in [
            ('∂W_TO/∂Cp (cruise)',  S['dCpR'], 'lbs per lbs/hp/hr', 'Eq 2.49'),
            ('∂W_TO/∂η_p (cruise)', S['dnpR'], 'lbs',               'Eq 2.50'),
            ('∂W_TO/∂(L/D) cruise', S['dLDR'], 'lbs',               'Eq 2.51'),
            ('∂W_TO/∂R',           S['dR'],   'lbs/nm',            'Eq 2.45')]:
            vc = 'sens-neg' if val < 0 else 'sens-pos'
            st.markdown(
                f'<div class="sens-row"><span class="sens-partial">{partial}</span>'
                f'<span class="{vc}">{val:+,.1f}</span>'
                f'<span class="sens-unit">{unit}</span>'
                f'<span class="sens-eq">{eq}</span></div>',
                unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card card-amber"><div class="card-title">Loiter Segment Partial Derivatives</div>', unsafe_allow_html=True)
        for partial, val, unit in [
            ('∂W_TO/∂Cp (loiter)',  S['dCpE'], 'lbs per lbs/hp/hr'),
            ('∂W_TO/∂η_p (loiter)', S['dnpE'], 'lbs'),
            ('∂W_TO/∂(L/D) loiter', S['dLDE'], 'lbs')]:
            vc = 'sens-neg' if val < 0 else 'sens-pos'
            st.markdown(
                f'<div class="sens-row" style="grid-template-columns:210px 110px 1fr">'
                f'<span class="sens-partial">{partial}</span>'
                f'<span class="{vc}">{val:+,.1f}</span>'
                f'<span class="sens-unit">{unit}</span></div>',
                unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with s2:
        # Range trade chart
        r_lo = max(100, int(R_nm) - 500)
        r_hi = min(6000, int(R_nm) + 500)
        ranges = list(range(r_lo, r_hi + 1, 40))
        wto_vals = []
        for r in ranges:
            try:
                w2, _ = solve_Wto({**P, 'R': float(r)})
                wto_vals.append(w2)
            except Exception:
                wto_vals.append(None)

        # ── FIX: define AX_BASE without tickfont to avoid duplicate key error ──
        DARK = dict(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(11,15,22,.7)',
                    font=dict(family='JetBrains Mono', color='#8b949e', size=9),
                    margin=dict(l=8, r=8, t=42, b=8))
        AX_BASE = dict(gridcolor='rgba(255,255,255,.04)', linecolor='rgba(255,255,255,.09)')
        AX_SM   = dict(**AX_BASE, tickfont=dict(size=9))

        fig_r = go.Figure()
        fig_r.add_trace(go.Scatter(x=ranges, y=wto_vals,
            mode='lines', line=dict(color='#c8a86c', width=2.5),
            fill='tozeroy', fillcolor='rgba(200,168,108,.06)'))
        fig_r.add_vline(x=R_nm, line=dict(color='rgba(63,185,80,.6)', width=1.5, dash='dash'),
            annotation_text=f'{R_nm} nm',
            annotation_font=dict(color='#3fb950', size=10, family='JetBrains Mono'))
        fig_r.update_layout(**DARK, height=260,
            title=dict(text='W_TO vs Design Range', font=dict(color='#c8a86c', size=12, family='DM Serif Display')),
            xaxis=dict(**AX_SM, title='Range (nm)'),
            yaxis=dict(**AX_SM, title='W_TO (lbs)'),
            showlegend=False)
        st.plotly_chart(fig_r, use_container_width=True)

        st.markdown(f"""<div class="card card-amber">
          <div class="card-title">Range Trade · ∂W_TO/∂R = {S['dR']:+.2f} lbs/nm</div>""",
          unsafe_allow_html=True)
        for dr in [-200, -100, +100, +200]:
            dw = S['dR'] * dr
            cv = '#3fb950' if dw < 0 else '#e3b341'
            st.markdown(
                f'<div style="display:flex;justify-content:space-between;padding:.28rem 0;'
                f'border-bottom:1px solid var(--border2);font-size:.79rem">'
                f'<span style="color:#8b949e">ΔR = {dr:+d} nm</span>'
                f'<span style="font-family:JetBrains Mono,monospace;font-weight:700;color:{cv}">{dw:+,.1f} lbs</span>'
                f'</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ───────────────────────────────────────────────────────
# TAB 3 — Charts
# ───────────────────────────────────────────────────────
with tab3:
    # ── FIX: separate DARK and AX definitions with no tickfont conflict ──
    DARK3 = dict(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(11,15,22,.7)',
                font=dict(family='JetBrains Mono', color='#8b949e', size=9),
                margin=dict(l=8, r=8, t=44, b=8))
    AX3      = dict(gridcolor='rgba(255,255,255,.04)', linecolor='rgba(255,255,255,.09)', tickfont=dict(size=9))
    AX3_SM8  = dict(gridcolor='rgba(255,255,255,.04)', linecolor='rgba(255,255,255,.09)', tickfont=dict(size=8))
    TITLE3   = lambda t: dict(text=t, font=dict(color='#c8a86c', size=12, family='DM Serif Display'))

    # ── Chart 1: Phase fractions + cumulative Mff ──
    st.markdown('<div class="sec-div">Chart 1 — Mission Phase Weight Fractions: How fuel is consumed each phase</div>', unsafe_allow_html=True)
    phases_l = list(RR['phases'].keys())
    fvals    = [v for v, _, _ in RR['phases'].values()]
    ftypes   = [t for _, t, _ in RR['phases'].values()]
    cum_p    = [1.0]
    for fv in fvals: cum_p.append(cum_p[-1] * fv)
    bar_col = ['#6a9eea' if t == 'Fixed' else '#c8a86c' for t in ftypes]

    fig1 = make_subplots(rows=1, cols=2,
        subplot_titles=["Wᵢ/Wᵢ₋₁ per phase (closer to 1.0 = less fuel burned)",
                        "Cumulative Mff (starts at 1.0, ends at Mff)"])
    fig1.add_trace(go.Bar(x=phases_l, y=fvals, marker_color=bar_col,
        marker_line=dict(width=0), text=[f'{v:.4f}' for v in fvals],
        textposition='outside', textfont=dict(size=8, color='#8b949e')), row=1, col=1)
    fig1.add_trace(go.Scatter(x=['Ramp'] + phases_l, y=cum_p,
        mode='lines+markers', line=dict(color='#c8a86c', width=2.5),
        marker=dict(color='#e4c88a', size=7, line=dict(color='#c8a86c', width=1.5)),
        fill='tozeroy', fillcolor='rgba(200,168,108,.06)'), row=1, col=2)
    fig1.update_layout(**DARK3, height=340, showlegend=False)
    fig1.update_xaxes(**AX3)
    fig1.update_yaxes(**AX3)
    fig1.update_annotations(font=dict(color='#c8a86c', size=10))
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown(
        f'<div style="font-size:.7rem;color:#6e7681;margin:-6px 0 12px;line-height:1.65">'
        f'🔵 Blue bars = fixed fractions (Table 2.1) &nbsp;·&nbsp; 🟡 Gold bars = Breguet equations · '
        f'Cruise burns the most fuel (fraction = {[v for v,t,_ in RR["phases"].values() if t=="Breguet"][0]:.4f})</div>',
        unsafe_allow_html=True)

    # ── Chart 2: Convergence ──
    st.markdown('<div class="sec-div">Chart 2 — Sizing Convergence: Where W_E_tent = W_E_allow is the solution</div>', unsafe_allow_html=True)
    wto_rng = np.linspace(Wto * 0.55, Wto * 1.5, 150)
    we_tent = []; we_allow = []
    for w in wto_rng:
        try:
            rr2 = compute_mission({**P, 'Wto': float(w)})
            we_tent.append(rr2['WE']); we_allow.append(rr2['WEa'])
        except Exception:
            we_tent.append(None); we_allow.append(None)

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=list(wto_rng), y=we_tent, mode='lines',
        name='W_E Tentative (from mission)',
        line=dict(color='#6a9eea', width=2.5)))
    fig2.add_trace(go.Scatter(x=list(wto_rng), y=we_allow, mode='lines',
        name='W_E Allowable (regression)',
        line=dict(color='#c8a86c', width=2.5)))
    fig2.add_vline(x=Wto, line=dict(color='rgba(63,185,80,.65)', width=1.5, dash='dash'))
    fig2.add_annotation(x=Wto, y=WE, text=f'✓ Solution\nW_TO={Wto:,.0f} lbs',
        font=dict(color='#3fb950', size=9, family='JetBrains Mono'),
        showarrow=True, arrowcolor='rgba(63,185,80,.5)', ax=40, ay=-40,
        bgcolor='rgba(7,9,13,.8)', bordercolor='rgba(63,185,80,.3)', borderwidth=1)
    fig2.update_layout(**DARK3, height=310, title=TITLE3('Sizing Loop Convergence'),
        xaxis=dict(**AX3, title='W_TO (lbs)'),
        yaxis=dict(**AX3, title='W_E (lbs)'),
        legend=dict(font=dict(size=9, color='#8b949e'), bgcolor='rgba(0,0,0,0)',
                    x=0.02, y=0.98))
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown(
        '<div style="font-size:.7rem;color:#6e7681;margin:-6px 0 12px;line-height:1.65">'
        'Blue line = tentative W_E computed from mission analysis &nbsp;·&nbsp; '
        'Gold line = allowable W_E from regression · '
        'They intersect at the solution W_TO.</div>', unsafe_allow_html=True)

    # ── Chart 3: Weight breakdown donut ──
    st.markdown('<div class="sec-div">Chart 3 — Weight Composition at Solution W_TO</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        labels = ['W_F  Fuel', 'W_PL  Payload', 'W_tfo  Trapped', 'W_crew  Crew', 'W_E  Empty']
        values = [WF, Wpl, Wtfo_r, Wcrew, WE]
        fig3 = go.Figure(go.Pie(labels=labels, values=values, hole=0.52,
            marker=dict(colors=['#c8a86c','#6a9eea','#e3b341','#9c72d4','#3fb950'],
                        line=dict(color='#07090d', width=2)),
            textfont=dict(size=9, family='JetBrains Mono'),
            hovertemplate='<b>%{label}</b><br>%{value:,.0f} lbs<br>%{percent}<extra></extra>'))
        fig3.add_annotation(text=f'<b>{Wto:,.0f}</b><br>lbs W_TO',
            xref='paper', yref='paper', x=0.5, y=0.5,
            font=dict(size=10, color='#c8a86c', family='JetBrains Mono'),
            showarrow=False, align='center')
        fig3.update_layout(**DARK3, title=TITLE3('Weight Composition'), height=300,
            legend=dict(font=dict(size=8), bgcolor='rgba(0,0,0,0)'))
        st.plotly_chart(fig3, use_container_width=True)

    with c2:
        # ── FIX: Sensitivity tornado — use AX3_SM8 (size=8 tickfont) separately ──
        sp = [
            ('∂W_TO/∂Cp cruise',  S['dCpR']),
            ('∂W_TO/∂η_p cruise', S['dnpR']),
            ('∂W_TO/∂L/D cruise', S['dLDR']),
            ('∂W_TO/∂R',         S['dR']),
            ('∂W_TO/∂Cp loiter', S['dCpE']),
            ('∂W_TO/∂η_p loiter',S['dnpE']),
            ('∂W_TO/∂L/D loiter',S['dLDE']),
        ]
        sp_s = sorted(sp, key=lambda x: abs(x[1]), reverse=True)
        slbl = [x[0] for x in sp_s]; sval = [x[1] for x in sp_s]
        scol = ['rgba(248,81,73,.75)' if v > 0 else 'rgba(63,185,80,.75)' for v in sval]
        fig4 = go.Figure(go.Bar(y=slbl, x=sval, orientation='h',
            marker_color=scol, marker_line=dict(width=0),
            text=[f'{v:+,.1f}' for v in sval],
            textposition='outside', textfont=dict(size=8, color='#8b949e')))
        fig4.add_vline(x=0, line=dict(color='rgba(255,255,255,.12)', width=1))
        fig4.update_layout(**DARK3, title=TITLE3('Sensitivity Tornado'), height=300,
            xaxis=dict(**AX3_SM8, title='dW_TO (lbs/unit)'),
            yaxis=dict(**AX3_SM8))   # ← FIX: no duplicate tickfont
        st.plotly_chart(fig4, use_container_width=True)

# ───────────────────────────────────────────────────────
# TAB 4 — Export
# ───────────────────────────────────────────────────────
with tab4:
    e1, e2 = st.columns(2, gap="medium")

    with e1:
        st.markdown('<div class="sec-div">Full Results — CSV</div>', unsafe_allow_html=True)
        df_exp = pd.DataFrame({
            'Parameter': ['W_TO','Mff','W_F','W_F_usable','W_tfo','W_OE',
                          'W_E_tent','W_E_allow','delta_WE','W_PL','W_crew',
                          'Rc_sm','Vm_mph','F','C','D'],
            'Value':     [round(Wto,2), round(RR['Mff'],6), round(WF,2),
                          round(RR['WFu'],2), round(Wtfo_r,3), round(WOE,2),
                          round(WE,2), round(RR['WEa'],2), round(RR['diff'],3),
                          round(Wpl,2), round(Wcrew,2), round(RR['Rc'],3),
                          round(RR['Vm'],3), round(S['F'],2), round(S['C'],6), round(S['D'],2)],
            'Units':     ['lbs','—','lbs','lbs','lbs','lbs','lbs','lbs','lbs',
                          'lbs','lbs','s.mi','mph','—','—','lbs']})
        st.dataframe(df_exp, hide_index=True, use_container_width=True, height=540,
            column_config={
                'Parameter': st.column_config.TextColumn('Parameter', width='medium'),
                'Value':     st.column_config.TextColumn('Value',     width='medium'),
                'Units':     st.column_config.TextColumn('Units',     width='small'),
            })
        b = io.StringIO(); df_exp.to_csv(b, index=False)
        st.download_button("⬇  Download CSV", b.getvalue(),
                           "aerosizer_results.csv", "text/csv",
                           use_container_width=True)

    with e2:
        st.markdown('<div class="sec-div">PDF Report — A4</div>', unsafe_allow_html=True)

        def make_pdf():
            buf = io.BytesIO()
            doc = SimpleDocTemplate(buf, pagesize=A4,
                leftMargin=2.0*cm, rightMargin=2.0*cm,
                topMargin=2.2*cm,  bottomMargin=2.2*cm)
            PW = 17.0*cm

            C_DARK  = colors.HexColor('#0D1B2A')
            C_GOLD  = colors.HexColor('#c8a86c')
            C_BLUE  = colors.HexColor('#4875c2')
            C_BLUE2 = colors.HexColor('#6a9eea')
            C_GREEN = colors.HexColor('#3fb950')
            C_RED   = colors.HexColor('#f85149')
            C_NAVY  = colors.HexColor('#0a1628')
            C_PANEL = colors.HexColor('#111720')
            C_GRAY  = colors.HexColor('#475569')
            C_LGRAY = colors.HexColor('#8b949e')
            C_ROW1  = colors.HexColor('#0d1520')
            C_ROW2  = colors.HexColor('#111e2e')
            C_WHITE = colors.white

            sty = getSampleStyleSheet()
            def ps(nm, **kw):
                return ParagraphStyle(nm, parent=sty['Normal'], **kw)

            sH1   = ps('H1',  fontSize=10,  fontName='Helvetica-Bold', textColor=C_GOLD, spaceBefore=14, spaceAfter=5)
            sH2   = ps('H2',  fontSize=8.5, fontName='Helvetica-Bold', textColor=C_BLUE2, spaceBefore=8,  spaceAfter=3)
            sBODY = ps('BD',  fontSize=8,   textColor=C_LGRAY, leading=12, spaceAfter=2)
            sEQ   = ps('EQ',  fontSize=8,   fontName='Courier', textColor=C_BLUE2, leading=12,
                        backColor=colors.HexColor('#0a1422'), leftIndent=8, rightIndent=8,
                        spaceBefore=2, spaceAfter=4)
            sFOOT = ps('FT',  fontSize=6.5, textColor=C_LGRAY, alignment=TA_CENTER)

            def dark_table(data, col_widths, hdr_color=C_NAVY):
                t = Table(data, colWidths=col_widths)
                style = [
                    ('BACKGROUND',   (0,0), (-1,0),  hdr_color),
                    ('TEXTCOLOR',    (0,0), (-1,0),  C_GOLD),
                    ('FONTNAME',     (0,0), (-1,0),  'Helvetica-Bold'),
                    ('FONTNAME',     (0,1), (-1,-1), 'Courier'),
                    ('FONTSIZE',     (0,0), (-1,-1), 7.5),
                    ('LEADING',      (0,0), (-1,-1), 11),
                    ('TEXTCOLOR',    (0,1), (-1,-1), C_LGRAY),
                    ('ROWBACKGROUNDS',(0,1),(-1,-1),  [C_ROW1, C_ROW2]),
                    ('GRID',         (0,0), (-1,-1), 0.2, colors.HexColor('#1e2d40')),
                    ('LINEBELOW',    (0,0), (-1,0),  1.0, C_GOLD),
                    ('LEFTPADDING',  (0,0), (-1,-1), 6),
                    ('RIGHTPADDING', (0,0), (-1,-1), 6),
                    ('TOPPADDING',   (0,0), (-1,-1), 3.5),
                    ('BOTTOMPADDING',(0,0), (-1,-1), 3.5),
                    ('VALIGN',       (0,0), (-1,-1), 'MIDDLE'),
                ]
                t.setStyle(TableStyle(style))
                return t

            story = []

            # Cover block
            hdr = Table([[
                Paragraph('<font color="#c8a86c"><b>AEROSIZER PRO</b></font>',
                    ps('HDR', fontSize=18, fontName='Helvetica-Bold', textColor=C_GOLD, leading=22)),
                Paragraph(
                    f'<font color="#6e7681">Raymer (2018) Ch.2 · Propeller Sizing</font><br/>'
                    f'<font color="#8b949e">W_TO = {Wto:,.1f} lbs &nbsp;·&nbsp; Mff = {RR["Mff"]:.6f}</font>',
                    ps('SUB', fontSize=8, textColor=C_LGRAY, leading=12, alignment=TA_RIGHT))
            ]], colWidths=[PW*0.58, PW*0.42])
            hdr.setStyle(TableStyle([
                ('BACKGROUND', (0,0),(-1,-1), C_DARK),
                ('TOPPADDING', (0,0),(-1,-1), 10),
                ('BOTTOMPADDING',(0,0),(-1,-1),10),
                ('LEFTPADDING',(0,0),(-1,-1),10),
                ('RIGHTPADDING',(0,0),(-1,-1),10),
            ]))
            story.append(hdr)
            story.append(HRFlowable(width=PW, thickness=2, color=C_GOLD, spaceBefore=0, spaceAfter=6))

            sc = C_GREEN if conv else C_RED
            cv_row = Table([[Paragraph(
                f'{"✓  CONVERGED" if conv else "⚠  NOT CONVERGED"}  —  '
                f'ΔW_E = {RR["diff"]:+.2f} lbs  ·  Mff = {RR["Mff"]:.6f}  ·  W_TO = {Wto:,.1f} lbs',
                ps('CV', fontSize=8.5, fontName='Helvetica-Bold',
                   textColor=sc, backColor=colors.HexColor('#0d1520')))
            ]], colWidths=[PW])
            cv_row.setStyle(TableStyle([
                ('BACKGROUND',(0,0),(0,0), colors.HexColor('#0d1520')),
                ('LINEBELOW',(0,0),(0,0),1.5,sc),
                ('LEFTPADDING',(0,0),(-1,-1),10),
                ('TOPPADDING',(0,0),(-1,-1),6),
                ('BOTTOMPADDING',(0,0),(-1,-1),6),
            ]))
            story.append(cv_row)
            story.append(Spacer(1, 0.35*cm))

            story.append(Paragraph('1  Mission Inputs', sH1))
            t_in = dark_table([
                ['Parameter','Value','Parameter','Value'],
                ['Passengers', str(int(npax)), 'Design range (nm)', str(int(R_nm))],
                ['Pax weight (lbs)', str(int(wpax)), 'Baggage (lbs)', str(int(wbag))],
                ['Flight crew', str(int(ncrew)), 'Cabin attendants', str(int(natt))],
                ['Cruise L/D', f'{LDc:.1f}', 'Loiter L/D', f'{LDl:.1f}'],
                ['Cruise Cp (lbs/hp/hr)', f'{Cpc:.2f}', 'Loiter Cp', f'{Cpl:.2f}'],
                ['Cruise η_p', f'{npc:.2f}', 'Loiter η_p', f'{npl:.2f}'],
                ['Loiter E (hr)', f'{El:.2f}', 'Loiter V (kts)', str(int(Vl))],
                ['A (regression)', f'{A_v:.4f}', 'B (regression)', f'{B_v:.4f}'],
                ['M_tfo', f'{Mtfo:.3f}', 'M_res', f'{Mres:.3f}'],
            ], [PW*0.3, PW*0.2, PW*0.3, PW*0.2])
            story.append(t_in)
            story.append(Spacer(1, 0.35*cm))

            story.append(Paragraph('2  Key Equations  (Raymer 2018, Chapter 2)', sH1))
            story.append(Paragraph('Cruise fraction — Breguet range equation, Eq. 2.9:', sH2))
            story.append(Paragraph('W5/W4  =  1 / exp[ Rc / (375 * (eta_p/Cp) * (L/D)) ]', sEQ))
            story.append(Paragraph('Loiter fraction — Breguet endurance equation, Eq. 2.11:', sH2))
            story.append(Paragraph('W6/W5  =  1 / exp[ E / (375 * (1/V) * (eta_p/Cp) * (L/D)) ]', sEQ))
            story.append(Paragraph('Empty weight regression, Table 2.2 / 2.15:', sH2))
            story.append(Paragraph('log10(W_E)  =  A  +  B * log10(W_TO)', sEQ))
            story.append(Paragraph(
                'Units: R in statute miles · Cp in lbs/hp/hr · V in mph · E in hours · eta_p dimensionless',
                sBODY))
            story.append(Spacer(1, 0.35*cm))

            story.append(Paragraph('3  Mission Phase Weight Fractions', sH1))
            ph_data = [['Phase', 'Wᵢ/Wᵢ₋₁', 'Type', 'Source', 'Cum. Mff']]
            cm3 = 1.0
            for pname, (fv, ft, fs) in RR['phases'].items():
                cm3 *= fv
                ph_data.append([pname, f'{fv:.5f}', ft, fs, f'{cm3:.5f}'])
            ph_data.append(['PRODUCT', '—', '—', 'Mff', f'{RR["Mff"]:.6f}'])
            story.append(dark_table(ph_data, [PW*0.22,PW*0.13,PW*0.13,PW*0.13,PW*0.15]))
            story.append(Spacer(1, 0.35*cm))

            story.append(Paragraph('4  Sizing Results', sH1))
            res_data = [['Quantity', 'Value (lbs)', 'Expression']]
            for nm, vl, ex in [
                ('W_TO Gross',          f'{Wto:,.2f}',          'Bisection solution'),
                ('W_F Total fuel',      f'{WF:,.2f}',           'W_TO·(1−Mff)·(1+M_res)'),
                ('W_F_used Usable',     f'{RR["WFu"]:,.2f}',    'W_TO·(1−Mff)'),
                ('W_tfo Trapped',       f'{Wtfo_r:,.3f}',       f'M_tfo×W_TO = {Mtfo:.3f}×'),
                ('W_OE Operating',      f'{WOE:,.2f}',          'W_TO − W_F − W_PL'),
                ('W_E Tentative',       f'{WE:,.2f}',           'W_OE − W_tfo − W_crew'),
                ('W_E Allowable',       f'{RR["WEa"]:,.2f}',    '10^[(log W_TO − A)/B]'),
                ('ΔW_E Convergence',    f'{RR["diff"]:+.3f}',   'W_E_allow − W_E_tent → 0'),
                ('W_PL Payload',        f'{Wpl:,.2f}',          f'{npax} pax × ({wpax}+{wbag}) lbs'),
                ('W_crew',              f'{Wcrew:,.2f}',        f'{ncrew} pilots + {natt} att.'),
                ('Mff Fuel fraction',   f'{RR["Mff"]:.6f}',     'Product of 8 phases'),
            ]:
                res_data.append([nm, vl, ex])
            story.append(dark_table(res_data, [PW*0.32, PW*0.2, PW*0.48]))
            story.append(Spacer(1, 0.35*cm))

            story.append(Paragraph('5  Weight Ratios — Sanity Check', sH1))
            rat_data = [['Ratio', 'Computed', 'Typical Range', 'Status']]
            for nm, vr, lo_r, hi_r in [
                ('W_PL / W_TO', Wpl/Wto, 0.10, 0.25),
                ('W_F  / W_TO', WF/Wto,  0.20, 0.45),
                ('W_E  / W_TO', WE/Wto,  0.45, 0.65),
                ('W_PL / W_E',  Wpl/WE,  0.15, 0.40)]:
                ok_r = lo_r <= vr <= hi_r
                rat_data.append([nm, f'{vr:.4f}', f'{lo_r:.2f} – {hi_r:.2f}',
                    '✓ OK' if ok_r else ('▲ High' if vr > hi_r else '▼ Low')])
            story.append(dark_table(rat_data, [PW*0.28,PW*0.17,PW*0.27,PW*0.18]))
            story.append(Spacer(1, 0.35*cm))

            story.append(Paragraph('6  Sensitivity Analysis (Raymer Eq. 2.44–2.51)', sH1))
            sen_data = [['Partial Derivative', 'Value', 'Units', 'Eq.']]
            for partial, val, unit, eq in [
                ('∂W_TO / ∂Cp (cruise)',  S['dCpR'], 'lbs/(lbs/hp/hr)', 'Eq 2.49'),
                ('∂W_TO / ∂η_p (cruise)', S['dnpR'], 'lbs',             'Eq 2.50'),
                ('∂W_TO / ∂(L/D) cruise', S['dLDR'], 'lbs',             'Eq 2.51'),
                ('∂W_TO / ∂R',            S['dR'],   'lbs/nm',          'Eq 2.45'),
                ('∂W_TO / ∂Cp (loiter)',  S['dCpE'], 'lbs/(lbs/hp/hr)', '—'),
                ('∂W_TO / ∂η_p (loiter)', S['dnpE'], 'lbs',             '—'),
                ('∂W_TO / ∂(L/D) loiter', S['dLDE'], 'lbs',             '—')]:
                sen_data.append([partial, f'{val:+,.2f}', unit, eq])
            story.append(dark_table(sen_data, [PW*0.38,PW*0.16,PW*0.28,PW*0.14]))
            story.append(Spacer(1, 0.45*cm))

            story.append(HRFlowable(width=PW, thickness=0.5, color=C_GOLD, spaceBefore=3, spaceAfter=4))
            story.append(Paragraph(
                f'AeroSizer Pro  ·  Raymer (2018) Aircraft Design: A Conceptual Approach  ·  '
                f'W_TO = {Wto:,.1f} lbs  ·  Mff = {RR["Mff"]:.6f}  ·  '
                f'{"CONVERGED" if conv else "NOT CONVERGED"}', sFOOT))

            doc.build(story); buf.seek(0); return buf.read()

        st.markdown(f"""
        <div class="card card-gold">
          <div class="card-title">PDF Report Contents</div>
          <div style="font-size:.77rem;color:var(--text);line-height:1.85">
            1 · Mission inputs table<br>
            2 · Key equations (Raymer Ch.2)<br>
            3 · Mission phase weight fractions<br>
            4 · Full sizing results<br>
            5 · Weight ratios sanity check<br>
            6 · Sensitivity analysis ∂W_TO/∂X
          </div>
          <div style="margin-top:.65rem;font-size:.67rem;color:#6e7681">
            Dark theme · A4 format · {'✓ Converged' if conv else '⚠ Check convergence before export'}
          </div>
        </div>""", unsafe_allow_html=True)

        st.download_button(
            "⬇  Generate & Download PDF (A4)", make_pdf(),
            "aerosizer_report.pdf", "application/pdf",
            use_container_width=True)
