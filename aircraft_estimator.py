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
                                 Table, TableStyle, HRFlowable, PageBreak,
                                 KeepTogether)
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Circle, Polygon
from reportlab.graphics import renderPDF

# ─── PAGE CONFIG ───
st.set_page_config(
    page_title="AeroSizer Pro",
    page_icon="✈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start': new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0], j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src= 'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f); })(window,document,'script','dataLayer','GTM-T8JSQMHD');</script>""", unsafe_allow_html=True)

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
html,body,[class*="css"]{background:var(--bg)!important;color:var(--text)!important;
  font-family:'DM Sans',sans-serif!important;}
.stApp{background:var(--bg)!important;}
.main .block-container{padding:.75rem 1.2rem 2rem!important;max-width:100%!important;}

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
[data-testid="stSidebar"]{background:var(--sur)!important;
  border-right:1px solid var(--border)!important;padding:0!important;}
[data-testid="stSidebar"]>div:first-child{padding:0!important;}
.sb-logo{padding:1.3rem 1.1rem .9rem;border-bottom:1px solid var(--border);
  background:linear-gradient(150deg,#06090f,#0c1220);position:relative;overflow:hidden;}
.sb-logo::before{content:'';position:absolute;inset:0;
  background-image:linear-gradient(rgba(72,117,194,.04) 1px,transparent 1px),
  linear-gradient(90deg,rgba(72,117,194,.04) 1px,transparent 1px);
  background-size:20px 20px;pointer-events:none;}
.sb-logo-title{font-family:'DM Serif Display',serif;font-size:1.25rem;
  color:var(--white);letter-spacing:-.03em;line-height:1;position:relative;z-index:1;}
.sb-logo-title span{background:linear-gradient(135deg,var(--gold),var(--gold2));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.sb-logo-sub{font-family:'JetBrains Mono',monospace;font-size:.52rem;
  letter-spacing:.18em;text-transform:uppercase;color:var(--text3);
  margin-top:.3rem;position:relative;z-index:1;}
.sb-stripe{height:2px;background:linear-gradient(90deg,var(--blue),var(--gold),var(--blue));
  background-size:200%;animation:stripe 4s linear infinite;}
@keyframes stripe{0%{background-position:0%;}100%{background-position:200%;}}
.sb-sec{font-family:'JetBrains Mono',monospace;font-size:.57rem;font-weight:700;
  letter-spacing:.18em;text-transform:uppercase;color:var(--gold);
  padding:.55rem 1rem .3rem;border-bottom:1px solid var(--border2);
  margin:.35rem 0 .45rem;display:flex;align-items:center;gap:.45rem;}
.sb-sec::before{content:'';width:8px;height:1px;background:var(--gold);flex-shrink:0;}
[data-testid="stSidebar"] label{font-family:'DM Sans',sans-serif!important;
  font-size:.76rem!important;font-weight:500!important;color:var(--text)!important;}
[data-testid="stSidebar"] .stNumberInput input{background:var(--pan)!important;
  border:1px solid var(--border)!important;border-radius:7px!important;
  color:var(--white)!important;font-family:'JetBrains Mono',monospace!important;
  font-size:.81rem!important;}
[data-testid="stSidebar"] .stNumberInput input:focus{border-color:var(--gold)!important;
  box-shadow:0 0 0 2px rgba(200,168,108,.18)!important;}
[data-testid="stSidebar"] div.stButton>button{
  background:linear-gradient(135deg,var(--gold),var(--gold2))!important;
  color:#07090d!important;border:none!important;border-radius:9px!important;
  font-size:.83rem!important;font-weight:700!important;padding:.65rem!important;
  width:100%!important;letter-spacing:.04em;
  box-shadow:0 4px 18px rgba(200,168,108,.28)!important;transition:all .22s!important;}
[data-testid="stSidebar"] div.stButton>button:hover{
  transform:translateY(-1px)!important;
  box-shadow:0 6px 24px rgba(200,168,108,.4)!important;}
.sb-kpi{background:var(--pan);border:1px solid var(--border);
  border-top:2px solid var(--gold);border-radius:9px;
  padding:.7rem .9rem;margin:0 .65rem .45rem;}
.sb-kpi-val{font-family:'JetBrains Mono',monospace;font-size:1.45rem;
  font-weight:700;color:var(--gold2);line-height:1.1;}
.sb-kpi-lbl{font-size:.58rem;letter-spacing:.1em;text-transform:uppercase;
  color:var(--text3);margin-top:.18rem;}
.conv-pill{display:inline-flex;align-items:center;gap:.35rem;border-radius:20px;
  padding:.22rem .78rem;font-family:'JetBrains Mono',monospace;font-size:.64rem;
  font-weight:700;letter-spacing:.05em;margin-top:.5rem;}
.conv-ok{background:rgba(63,185,80,.1);border:1px solid rgba(63,185,80,.28);color:#3fb950;}
.conv-warn{background:rgba(248,81,73,.09);border:1px solid rgba(248,81,73,.28);color:#f85149;}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"]{background:var(--sur)!important;
  border:1px solid var(--border)!important;border-radius:11px!important;
  padding:4px!important;gap:3px!important;margin-bottom:1.1rem!important;}
.stTabs [data-baseweb="tab"]{border-radius:8px!important;
  font-family:'DM Sans',sans-serif!important;font-size:.78rem!important;
  font-weight:500!important;color:var(--text2)!important;
  padding:.42rem 1rem!important;transition:all .2s!important;}
.stTabs [aria-selected="true"]{
  background:linear-gradient(135deg,var(--gold),var(--gold2))!important;
  color:#07090d!important;font-weight:700!important;
  box-shadow:0 2px 10px rgba(200,168,108,.32)!important;}

/* ── CARDS ── */
.card{background:var(--sur);border:1px solid var(--border);border-radius:12px;
  padding:1.1rem 1.25rem;margin-bottom:.9rem;position:relative;overflow:hidden;}
.card::after{content:'';position:absolute;top:0;left:0;right:0;height:1px;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,.05),transparent);
  pointer-events:none;}
.card-gold{border-left:2px solid var(--gold);}
.card-blue{border-left:2px solid var(--blue2);}
.card-green{border-left:2px solid var(--green);}
.card-amber{border-left:2px solid var(--amber);}
.card-red{border-left:2px solid var(--red);}
.card-title{font-family:'JetBrains Mono',monospace;font-size:.57rem;font-weight:700;
  letter-spacing:.16em;text-transform:uppercase;color:var(--gold);
  padding-bottom:.48rem;border-bottom:1px solid var(--border2);margin-bottom:.75rem;
  display:flex;align-items:center;gap:.45rem;}
.card-title::before{content:'';width:8px;height:1px;background:var(--gold);flex-shrink:0;}

/* ── EQUATIONS ── */
.eq-box{background:rgba(200,168,108,.06);border:1px solid rgba(200,168,108,.18);
  border-radius:8px;padding:.48rem .9rem;font-family:'JetBrains Mono',monospace;
  font-size:.79rem;color:var(--gold2);display:block;margin-bottom:.45rem;
  white-space:nowrap;overflow-x:auto;letter-spacing:.01em;}
.eq-label{font-size:.7rem;color:var(--text2);margin-bottom:.28rem;font-weight:500;}

/* ── RESULT PILLS ── */
.rpill{display:inline-flex;align-items:baseline;gap:.25rem;border-radius:7px;
  padding:.2rem .72rem;font-family:'JetBrains Mono',monospace;font-size:.84rem;
  font-weight:700;margin-right:.38rem;margin-top:.32rem;}
.rpill-gold{background:rgba(200,168,108,.1);border:1px solid rgba(200,168,108,.26);
  color:var(--gold2);}
.rpill-blue{background:rgba(72,117,194,.1);border:1px solid rgba(106,158,234,.26);
  color:var(--blue3);}
.rpill-green{background:rgba(63,185,80,.1);border:1px solid rgba(63,185,80,.26);
  color:var(--green);}
.rpill-red{background:rgba(248,81,73,.1);border:1px solid rgba(248,81,73,.26);
  color:var(--red);}
.rpill-unit{font-size:.62rem;font-weight:400;opacity:.6;}

/* ── TABLE ROWS ── */
.ph-hdr{display:grid;grid-template-columns:145px 90px 75px 75px 1fr;gap:.45rem;
  padding:.22rem 0 .38rem;font-size:.59rem;letter-spacing:.08em;text-transform:uppercase;
  color:var(--text3);border-bottom:1px solid var(--border);font-weight:700;}
.ph-row{display:grid;grid-template-columns:145px 90px 75px 75px 1fr;gap:.45rem;
  align-items:center;padding:.38rem 0;border-bottom:1px solid var(--border2);
  font-size:.79rem;transition:background .15s;border-radius:5px;}
.ph-row:last-child{border-bottom:none;}
.ph-row:hover{background:rgba(200,168,108,.04);padding-left:.3rem;padding-right:.3rem;}
.ph-name{font-weight:500;color:var(--text);}
.ph-frac{font-family:'JetBrains Mono',monospace;font-weight:700;}
.ph-frac-fixed{color:var(--blue3);}
.ph-frac-breguet{color:var(--gold2);}
.ph-badge{font-size:.59rem;font-weight:700;letter-spacing:.05em;text-transform:uppercase;
  padding:.1rem .48rem;border-radius:4px;width:fit-content;}
.ph-badge-fixed{background:rgba(72,117,194,.1);color:var(--blue3);
  border:1px solid rgba(72,117,194,.2);}
.ph-badge-breguet{background:rgba(200,168,108,.1);color:var(--gold);
  border:1px solid rgba(200,168,108,.2);}
.ph-src{font-size:.64rem;color:var(--text3);font-family:'JetBrains Mono',monospace;}

/* ── SENSITIVITY ── */
.sens-row{display:grid;grid-template-columns:210px 110px 155px 68px;gap:.45rem;
  align-items:center;padding:.36rem 0;border-bottom:1px solid var(--border2);
  transition:background .15s;border-radius:5px;}
.sens-row:hover{background:rgba(200,168,108,.04);padding-left:.3rem;padding-right:.3rem;}
.sens-row:last-child{border-bottom:none;}
.sens-partial{font-family:'JetBrains Mono',monospace;font-size:.75rem;color:var(--text);}
.sens-pos{font-family:'JetBrains Mono',monospace;font-size:.81rem;font-weight:700;
  color:var(--red);}
.sens-neg{font-family:'JetBrains Mono',monospace;font-size:.81rem;font-weight:700;
  color:var(--green);}
.sens-unit{font-size:.63rem;color:var(--text3);}
.sens-eq{font-size:.61rem;color:var(--gold);font-family:'JetBrains Mono',monospace;}

/* ── STATUS ── */
.status-ok{background:rgba(63,185,80,.06);border:1px solid rgba(63,185,80,.16);
  border-left:3px solid var(--green);border-radius:0 9px 9px 0;
  padding:.52rem 1.1rem;margin-bottom:.9rem;font-family:'JetBrains Mono',monospace;
  font-size:.75rem;color:var(--green);}
.status-err{background:rgba(248,81,73,.05);border:1px solid rgba(248,81,73,.16);
  border-left:3px solid var(--red);border-radius:0 9px 9px 0;
  padding:.52rem 1.1rem;margin-bottom:.9rem;font-family:'JetBrains Mono',monospace;
  font-size:.75rem;color:var(--red);}

/* ── KPI ── */
.kpi-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:.7rem;margin-bottom:1rem;}
.kpi-card{background:var(--sur);border:1px solid var(--border);
  border-top:2px solid var(--border);border-radius:11px;padding:.9rem 1rem;
  transition:transform .2s,border-color .2s;}
.kpi-card:hover{transform:translateY(-2px);border-color:rgba(200,168,108,.22);}
.kpi-card.primary{border-top:2px solid var(--gold);background:rgba(200,168,108,.04);}
.kpi-card.green{border-top:2px solid var(--green);}
.kpi-card.amber{border-top:2px solid var(--amber);}
.kpi-card.blue{border-top:2px solid var(--blue2);}
.kpi-val{font-family:'JetBrains Mono',monospace;font-size:1.45rem;font-weight:700;
  color:var(--white);line-height:1.1;}
.kpi-val.primary{color:var(--gold2);font-size:1.6rem;}
.kpi-unit{font-size:.63rem;font-weight:400;color:var(--text3);margin-left:2px;}
.kpi-lbl{font-size:.57rem;letter-spacing:.09em;text-transform:uppercase;
  color:var(--text3);margin-top:.26rem;font-weight:500;}

/* ── SECTION DIV ── */
.sec-div{font-family:'JetBrains Mono',monospace;font-size:.59rem;font-weight:700;
  letter-spacing:.15em;text-transform:uppercase;color:var(--gold);
  border-bottom:1px solid var(--border);padding-bottom:.38rem;
  margin:.7rem 0 .85rem;display:flex;align-items:center;gap:.45rem;}
.sec-div::before{content:'';width:8px;height:1px;background:var(--gold);flex-shrink:0;}

/* ── MAIN HEADER ── */
.main-header{background:var(--sur);border:1px solid var(--border);border-radius:12px;
  border-left:3px solid var(--gold);padding:.85rem 1.4rem;margin-bottom:1rem;
  display:flex;align-items:center;justify-content:space-between;
  flex-wrap:wrap;gap:.8rem;position:relative;overflow:hidden;}
.main-header::before{content:'';position:absolute;inset:0;
  background-image:linear-gradient(rgba(200,168,108,.025) 1px,transparent 1px),
  linear-gradient(90deg,rgba(200,168,108,.025) 1px,transparent 1px);
  background-size:32px 32px;pointer-events:none;}
.mh-title{font-family:'DM Serif Display',serif;font-size:1.35rem;
  color:var(--white);letter-spacing:-.03em;line-height:1;position:relative;z-index:1;}
.mh-title span{background:linear-gradient(135deg,var(--gold),var(--gold2));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}

/* ── DARK TABLE ── */
.dark-table{width:100%;border-collapse:collapse;font-family:'JetBrains Mono',monospace;
  font-size:.76rem;border:1px solid rgba(200,168,108,.22);
  border-radius:10px;overflow:hidden;}
.dark-table thead tr{background:linear-gradient(135deg,#0d1520,#111e2e);}
.dark-table thead th{padding:.52rem .85rem;text-align:left;font-size:.6rem;
  font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--gold);
  border-bottom:1.5px solid rgba(200,168,108,.3);white-space:nowrap;}
.dark-table tbody tr{border-bottom:1px solid rgba(255,255,255,.04);transition:background .15s;}
.dark-table tbody tr:nth-child(odd){background:#0d1520;}
.dark-table tbody tr:nth-child(even){background:#111e2e;}
.dark-table tbody tr:hover{background:rgba(200,168,108,.07);}
.dark-table tbody tr:last-child{border-bottom:none;}
.dark-table tbody td{padding:.42rem .85rem;color:var(--text);vertical-align:middle;line-height:1.5;}
.dark-table tbody td:first-child{color:var(--gold);font-weight:600;font-size:.72rem;}
.dark-table tbody td.val{color:var(--white);font-weight:700;}
.dark-table tbody td.unit{color:var(--text3);font-size:.68rem;}
.dark-table tbody td.check-ok{color:var(--green);font-weight:700;}
.dark-table tbody td.check-warn{color:var(--amber);font-weight:700;}
.dark-table-wrap{border:1px solid rgba(200,168,108,.18);border-radius:10px;
  overflow:hidden;margin-bottom:.7rem;}

/* ── DOWNLOAD ── */
div.stDownloadButton>button{background:var(--pan)!important;color:var(--gold)!important;
  border:1px solid rgba(200,168,108,.22)!important;border-radius:8px!important;
  font-size:.79rem!important;font-weight:600!important;padding:.52rem 1rem!important;
  width:100%!important;transition:all .2s!important;}
div.stDownloadButton>button:hover{border-color:var(--gold)!important;
  color:var(--white)!important;background:rgba(200,168,108,.1)!important;
  transform:translateY(-1px)!important;}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# PHYSICS  —  Raymer Ch.2 exact equations
# ═══════════════════════════════════════════════════════
def compute_mission(p):
    Wpl   = p['npax'] * (p['wpax'] + p['wbag'])
    Wcrew = (p['ncrew'] + p['natt']) * 205
    Wtfo  = p['Wto'] * p['Mtfo']
    Rc    = p['R']  * 1.15078
    Vm    = p['Vl'] * 1.15078
    W5 = 1.0 / math.exp(Rc / (375.0 * (p['npc'] / p['Cpc']) * p['LDc']))
    W6 = 1.0 / math.exp(p['El'] / (375.0 * (1.0 / Vm) * (p['npl'] / p['Cpl']) * p['LDl']))
    phases = {
        'Engine Start': (0.990, 'Fixed',   'Table 2.1'),
        'Taxi':         (0.995, 'Fixed',   'Table 2.1'),
        'Takeoff':      (0.995, 'Fixed',   'Table 2.1'),
        'Climb':        (0.985, 'Fixed',   'Fig. 2.2'),
        'Cruise':       (W5,   'Breguet', 'Eq. 2.9'),
        'Loiter':       (W6,   'Breguet', 'Eq. 2.11'),
        'Descent':      (0.985, 'Fixed',   'Fig. 2.2'),
        'Landing':      (0.995, 'Fixed',   'Table 2.1'),
    }
    Mff = 1.0
    for v, _, _ in phases.values():
        Mff *= v
    WFu  = p['Wto'] * (1.0 - Mff)
    WF   = WFu * (1.0 + p['Mr'])
    WOE  = p['Wto'] - WF - Wpl
    WE   = WOE - Wtfo - Wcrew
    WEa  = 10.0 ** ((math.log10(p['Wto']) - p['A']) / p['B'])
    return dict(
        Wpl=Wpl, Wcrew=Wcrew, Wtfo=Wtfo, Mff=Mff,
        WF=WF, WFu=WFu, WOE=WOE, WE=WE, WEa=WEa,
        diff=WEa - WE,
        phases=phases, Rc=Rc, Vm=Vm
    )


def solve_Wto(p, tol=0.5, n=500):
    pp = dict(p)
    guess = float(p.get('Wto', 48550))
    lo_b  = max(5000,   int(guess * 0.3))
    hi_b  = min(600000, int(guess * 3.5))
    step  = max(500, int((hi_b - lo_b) / 300))
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
    RR    = compute_mission({**p, 'Wto': Wto})
    Mff   = RR['Mff']; Rc = RR['Rc']; Vm = RR['Vm']
    Wpl   = RR['Wpl']; Wcrew = RR['Wcrew']
    C  = 1.0 - (1.0 + p['Mr']) * (1.0 - Mff) - p['Mtfo']
    D  = Wpl + Wcrew
    dn = C * Wto * (1.0 - p['B']) - D
    F  = (-p['B'] * Wto**2 * (1.0 + p['Mr']) * Mff) / dn if abs(dn) > 1e-6 else 0.0
    return dict(C=C, D=D, F=F,
        dCpR  =  F * Rc                       / (375.0 * p['npc']    * p['LDc']),
        dnpR  = -F * Rc  * p['Cpc']           / (375.0 * p['npc']**2 * p['LDc']),
        dLDR  = -F * Rc  * p['Cpc']           / (375.0 * p['npc']    * p['LDc']**2),
        dR    =  F        * p['Cpc']           / (375.0 * p['npc']    * p['LDc']),
        dCpE  =  F * p['El'] * Vm             / (375.0 * p['npl']    * p['LDl']),
        dnpE  = -F * p['El'] * Vm * p['Cpl']  / (375.0 * p['npl']**2 * p['LDl']),
        dLDE  = -F * p['El'] * Vm * p['Cpl']  / (375.0 * p['npl']    * p['LDl']**2),
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
    npax  = st.number_input("Passengers",                1,   400,  34,    step=1)
    wpax  = st.number_input("Pax body weight (lbs)",   100,  300,  175,   step=5)
    wbag  = st.number_input("Baggage per pax (lbs)",     0,  100,   30,   step=5)
    ncrew = st.number_input("Flight crew (pilots)",      1,    6,    2,    step=1)
    natt  = st.number_input("Cabin attendants",          0,   10,    1,    step=1)

    st.markdown('<div class="sb-sec">② Cruise Segment</div>', unsafe_allow_html=True)
    R_nm = st.number_input("Design range (nm)",        100, 6000, 1100,   step=50)
    LDc  = st.number_input("Cruise L/D",               4.0, 30.0,  13.0, step=0.5,  format="%.1f")
    Cpc  = st.number_input("Cruise SFC Cp (lbs/hp/hr)",0.20, 1.20, 0.60, step=0.01, format="%.2f")
    npc  = st.number_input("Cruise η_p",               0.30, 0.98, 0.85, step=0.01, format="%.2f")

    st.markdown('<div class="sb-sec">③ Loiter / Reserve</div>', unsafe_allow_html=True)
    El   = st.number_input("Loiter endurance E (hr)",  0.10,  6.0, 0.75, step=0.05, format="%.2f")
    Vl   = st.number_input("Loiter speed (kts)",         60,  400,  250,  step=5)
    LDl  = st.number_input("Loiter L/D",               4.0, 30.0,  16.0, step=0.5,  format="%.1f")
    Cpl  = st.number_input("Loiter SFC Cp (lbs/hp/hr)",0.20, 1.20, 0.65, step=0.01, format="%.2f")
    npl  = st.number_input("Loiter η_p",               0.30, 0.98, 0.77, step=0.01, format="%.2f")

    st.markdown('<div class="sb-sec">④ Regression Constants</div>', unsafe_allow_html=True)
    A_v  = st.number_input("A  (Table 2.15)",          0.0,  2.0,  0.3774, step=0.0001, format="%.4f")
    B_v  = st.number_input("B  (Table 2.2 / 2.15)",    0.1,  2.0,  0.9647, step=0.0001, format="%.4f")

    st.markdown('<div class="sb-sec">⑤ Fuel Allowances</div>', unsafe_allow_html=True)
    Mtfo  = st.number_input("M_tfo (trapped fuel)",    0.000, 0.05, 0.005, step=0.001, format="%.3f")
    Mres  = st.number_input("M_res (reserve fraction)",0.000, 0.10, 0.000, step=0.001, format="%.3f")
    Wto_g = st.number_input("W_TO initial guess (lbs)",5000, 500000, 48550, step=1000)

    st.markdown("<br>", unsafe_allow_html=True)
    calc  = st.button("⟳  Run Sizing", use_container_width=True)

# ─── Solve ───
P = dict(
    npax=int(npax),   wpax=float(wpax),  wbag=float(wbag),
    ncrew=int(ncrew), natt=int(natt),    Mtfo=float(Mtfo),  Mr=float(Mres),
    R=float(R_nm),    Vl=float(Vl),      LDc=float(LDc),
    Cpc=float(Cpc),   npc=float(npc),    El=float(El),
    LDl=float(LDl),   Cpl=float(Cpl),   npl=float(npl),
    A=float(A_v),     B=float(B_v),      Wto=float(Wto_g)
)
P_key = str(sorted(P.items()))
if 'res' not in st.session_state or st.session_state.get('_key') != P_key or calc:
    Wto, RR = solve_Wto(P)
    S = sensitivity(P, Wto)
    st.session_state['res'] = (Wto, RR, S)
    st.session_state['_key'] = P_key
else:
    Wto, RR, S = st.session_state['res']

conv    = abs(RR['diff']) < 1.0
WE      = RR['WE'];   WOE = RR['WOE'];  WF = RR['WF']
Wpl     = RR['Wpl'];  Wcrew = RR['Wcrew']; Wtfo_r = RR['Wtfo']

# ─── Sidebar live KPIs ───
with st.sidebar:
    st.markdown('<div class="sb-sec">◉ Live Results</div>', unsafe_allow_html=True)
    dc = '#3fb950' if conv else '#f85149'
    st.markdown(f"""
    <div style="padding:0 .65rem">
      <div class="sb-kpi">
        <div class="sb-kpi-val">{Wto:,.0f}
          <span style="font-size:.72rem;font-weight:400;color:#6e7681">lbs</span>
        </div>
        <div class="sb-kpi-lbl">W_TO · Gross Takeoff Weight</div>
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:.38rem;margin:0 0 .45rem">
        <div class="sb-kpi" style="padding:.48rem .7rem;border-top-color:var(--blue2)">
          <div style="font-family:'JetBrains Mono',monospace;font-size:.96rem;
               font-weight:700;color:var(--blue3)">{RR['Mff']:.4f}</div>
          <div class="sb-kpi-lbl">Mff</div>
        </div>
        <div class="sb-kpi" style="padding:.48rem .7rem;border-top-color:{dc}">
          <div style="font-family:'JetBrains Mono',monospace;font-size:.96rem;
               font-weight:700;color:{dc}">{RR['diff']:+.2f}</div>
          <div class="sb-kpi-lbl">ΔW_E (lbs)</div>
        </div>
      </div>
      <div class="conv-pill {'conv-ok' if conv else 'conv-warn'}">
        {'✓ CONVERGED' if conv else '⚠ NOT CONVERGED'}
      </div>
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
    <div class="mh-title">Aero<span>Sizer</span>
      <span style="font-size:.88rem;font-weight:400;color:#8b949e;
            font-family:'DM Sans',sans-serif">Pro</span>
    </div>
    <div style="font-size:.6rem;letter-spacing:.08em;text-transform:uppercase;
         color:#6e7681;margin-top:.22rem">
      Raymer (2018) Ch.2 · Propeller Aircraft Conceptual Weight Sizing
    </div>
  </div>
  <div style="display:flex;align-items:center;gap:1rem;flex-wrap:wrap;
       position:relative;z-index:1">
    <div style="text-align:right">
      <div style="font-family:'JetBrains Mono',monospace;font-size:1.38rem;
           font-weight:700;color:var(--gold2)">{Wto:,.0f}
        <span style="font-size:.7rem;color:#6e7681">lbs</span>
      </div>
      <div style="font-size:.58rem;letter-spacing:.1em;text-transform:uppercase;
           color:#6e7681">W_TO Gross</div>
    </div>
    <div style="background:{bb};color:{bc};border:1px solid {bc}44;
         font-family:'JetBrains Mono',monospace;font-size:.66rem;font-weight:700;
         padding:.28rem .85rem;border-radius:20px;letter-spacing:.06em">{bt}</div>
  </div>
</div>""", unsafe_allow_html=True)

if conv:
    st.markdown(
        f'<div class="status-ok">✓ &nbsp;W_TO = {Wto:,.1f} lbs &nbsp;·&nbsp; '
        f'Mff = {RR["Mff"]:.6f} &nbsp;·&nbsp; '
        f'W_E_tent = {WE:,.1f} lbs &nbsp;·&nbsp; '
        f'W_E_allow = {RR["WEa"]:,.1f} lbs &nbsp;·&nbsp; '
        f'ΔW_E = {RR["diff"]:+.2f} lbs</div>',
        unsafe_allow_html=True)
else:
    st.markdown(
        f'<div class="status-err">⚠ &nbsp;Not converged — ΔW_E = {RR["diff"]:+.0f} lbs. '
        f'Adjust A, B regression constants or check inputs.</div>',
        unsafe_allow_html=True)

st.markdown(f"""
<div class="kpi-grid">
  <div class="kpi-card primary">
    <div class="kpi-val primary">{Wto:,.0f}<span class="kpi-unit">lbs</span></div>
    <div class="kpi-lbl">W_TO Gross</div>
  </div>
  <div class="kpi-card blue">
    <div class="kpi-val">{RR['Mff']:.5f}</div>
    <div class="kpi-lbl">Mff Fuel Frac.</div>
  </div>
  <div class="kpi-card amber">
    <div class="kpi-val">{WF:,.0f}<span class="kpi-unit">lbs</span></div>
    <div class="kpi-lbl">W_F Total Fuel</div>
  </div>
  <div class="kpi-card green">
    <div class="kpi-val">{Wpl:,.0f}<span class="kpi-unit">lbs</span></div>
    <div class="kpi-lbl">W_PL Payload</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-val">{WE:,.0f}<span class="kpi-unit">lbs</span></div>
    <div class="kpi-lbl">W_E Empty</div>
  </div>
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


# ─────────────────────────────────────────────────────────
# TAB 1 — Sizing Steps
# ─────────────────────────────────────────────────────────
with tab1:
    cL, cR = st.columns([3, 2], gap="medium")

    with cL:
        pax_wt  = int(npax) * (int(wpax) + int(wbag))
        crew_wt = int(ncrew) * 205
        att_wt  = int(natt)  * 200
        st.markdown(f"""
        <div class="card card-gold">
          <div class="card-title">Step 1 — Payload & Crew Weights</div>
          <div class="ph-row" style="grid-template-columns:230px 110px 1fr">
            <span class="ph-name">{npax} pax × ({int(wpax)} + {int(wbag)}) lbs</span>
            <span class="ph-frac ph-frac-fixed">{pax_wt:,} lbs</span>
            <span class="ph-src">cabin payload</span>
          </div>
          <div class="ph-row" style="grid-template-columns:230px 110px 1fr">
            <span class="ph-name">{ncrew} pilots × 205 lbs</span>
            <span class="ph-frac ph-frac-fixed">{crew_wt:,} lbs</span>
            <span class="ph-src">flight crew</span>
          </div>
          <div class="ph-row" style="grid-template-columns:230px 110px 1fr">
            <span class="ph-name">{natt} attendant(s) × 205 lbs</span>
            <span class="ph-frac ph-frac-fixed">{int(natt)*205:,} lbs</span>
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
          <div class="ph-row" style="grid-template-columns:240px 120px 1fr">
            <span class="ph-name">R_cruise (statute miles)</span>
            <span class="ph-frac ph-frac-fixed">{RR['Rc']:.3f} sm</span>
            <span class="ph-src">{R_nm} nm × 1.15078</span>
          </div>
          <div class="ph-row" style="grid-template-columns:240px 120px 1fr">
            <span class="ph-name">V_loiter (mph)</span>
            <span class="ph-frac ph-frac-fixed">{RR['Vm']:.2f} mph</span>
            <span class="ph-src">{Vl} kts × 1.15078</span>
          </div>
          <div class="ph-row" style="grid-template-columns:240px 120px 1fr">
            <span class="ph-name">W_tfo = M_tfo × W_TO</span>
            <span class="ph-frac ph-frac-fixed">{Wtfo_r:,.2f} lbs</span>
            <span class="ph-src">{Mtfo:.3f} × {Wto:,.0f} lbs</span>
          </div>
        </div>""", unsafe_allow_html=True)

        st.markdown(
            '<div class="card card-blue">'
            '<div class="card-title">Step 3 — Mission Phase Weight Fractions'
            ' (Raymer Table 2.1 + Breguet)</div>',
            unsafe_allow_html=True)
        st.markdown(
            '<div class="ph-hdr">'
            '<span>Phase</span><span>Wi/Wi-1</span>'
            '<span>Type</span><span>Source</span><span>Cumulative Mff</span>'
            '</div>', unsafe_allow_html=True)
        cum = 1.0
        for ph, (fv, ft, fs) in RR['phases'].items():
            cum *= fv
            fc  = 'ph-frac-breguet' if ft == 'Breguet' else 'ph-frac-fixed'
            bc2 = 'ph-badge-breguet' if ft == 'Breguet' else 'ph-badge-fixed'
            st.markdown(
                f'<div class="ph-row">'
                f'<span class="ph-name">{ph}</span>'
                f'<span class="ph-frac {fc}">{fv:.5f}</span>'
                f'<span class="ph-badge {bc2}">{ft}</span>'
                f'<span class="ph-src">{fs}</span>'
                f'<span style="font-family:\'JetBrains Mono\',monospace;'
                f'font-size:.72rem;color:#8b949e">{cum:.5f}</span></div>',
                unsafe_allow_html=True)
        st.markdown(
            f'<div style="margin-top:.6rem;padding-top:.48rem;'
            f'border-top:1px solid var(--border2)">'
            f'<span class="rpill rpill-gold">Mff = {RR["Mff"]:.6f}</span>'
            f'<span style="font-size:.67rem;color:#6e7681;margin-left:.4rem">'
            f'product of all 8 phase fractions</span>'
            f'</div></div>', unsafe_allow_html=True)

        ok = "rpill-green" if conv else "rpill-red"
        st.markdown(f"""
        <div class="card {'card-green' if conv else 'card-red'}">
          <div class="card-title">Steps 4–6 — Weight Build-Up & Convergence Check</div>
          <div style="display:grid;grid-template-columns:240px 150px 1fr;gap:.45rem;
               font-size:.59rem;letter-spacing:.08em;text-transform:uppercase;
               color:var(--text3);padding-bottom:.32rem;
               border-bottom:1px solid var(--border);font-weight:700">
            <span>Quantity</span><span>Value</span><span>Expression</span>
          </div>
          <div class="ph-row" style="grid-template-columns:240px 150px 1fr">
            <span class="ph-name">4a — W_F (total fuel)</span>
            <span class="ph-frac ph-frac-fixed">{WF:,.1f} lbs</span>
            <span class="ph-src">W_TO·(1−Mff)·(1+M_res)</span>
          </div>
          <div class="ph-row" style="grid-template-columns:240px 150px 1fr">
            <span class="ph-name">4b — W_OE (operating empty)</span>
            <span class="ph-frac ph-frac-fixed">{WOE:,.1f} lbs</span>
            <span class="ph-src">W_TO − W_F − W_PL</span>
          </div>
          <div class="ph-row" style="grid-template-columns:240px 150px 1fr">
            <span class="ph-name">5 — W_E (tentative)</span>
            <span class="ph-frac ph-frac-fixed">{WE:,.2f} lbs</span>
            <span class="ph-src">W_OE − W_tfo − W_crew</span>
          </div>
          <div class="ph-row" style="grid-template-columns:240px 150px 1fr">
            <span class="ph-name">6 — W_E (allowable, regression)</span>
            <span class="ph-frac ph-frac-fixed">{RR['WEa']:,.2f} lbs</span>
            <span class="ph-src">10^[(log W_TO − A) / B]</span>
          </div>
          <div style="margin-top:.6rem">
            <span class="rpill {ok}">ΔW_E = {RR['diff']:+.2f} lbs</span>
            <span class="rpill {ok}">{'✓ CONVERGED' if conv else '⚠ NOT CONVERGED'}</span>
          </div>
        </div>""", unsafe_allow_html=True)

    with cR:
        st.markdown("""
        <div class="card card-gold">
          <div class="card-title">Key Equations — Raymer Ch.2</div>
          <div class="eq-label">Cruise fraction (Eq. 2.9) — Breguet Range</div>
          <div class="eq-box">W₅/W₄ = exp[ −Rc / (375·(η_p/Cp)·(L/D)) ]</div>
          <div class="eq-label" style="margin-top:.55rem">
            Loiter fraction (Eq. 2.11) — Breguet Endurance</div>
          <div class="eq-box">W₆/W₅ = exp[ −E·V / (375·(η_p/Cp)·(L/D)) ]</div>
          <div class="eq-label" style="margin-top:.55rem">
            Regression line (Table 2.2 / 2.15)</div>
          <div class="eq-box">log₁₀(W_E) = A + B · log₁₀(W_TO)</div>
          <div style="font-size:.65rem;color:#6e7681;margin-top:.45rem;line-height:1.72">
            R<sub>c</sub> in <b style="color:#8b949e">statute miles</b>
            &nbsp;·&nbsp; Cp in <b style="color:#8b949e">lbs/hp/hr</b><br>
            V in <b style="color:#8b949e">mph</b>
            &nbsp;·&nbsp; E in <b style="color:#8b949e">hours</b>
            &nbsp;·&nbsp; η_p dimensionless
          </div>
        </div>""", unsafe_allow_html=True)

        sum_rows = [
            ('W_TO',      f"{Wto:,.1f}",          'lbs'),
            ('Mff',       f"{RR['Mff']:.6f}",      '—'),
            ('W_F',       f"{WF:,.1f}",            'lbs'),
            ('W_F_used',  f"{RR['WFu']:,.1f}",     'lbs'),
            ('W_tfo',     f"{Wtfo_r:,.2f}",        'lbs'),
            ('W_OE',      f"{WOE:,.1f}",           'lbs'),
            ('W_E_tent',  f"{WE:,.2f}",            'lbs'),
            ('W_E_allow', f"{RR['WEa']:,.2f}",     'lbs'),
            ('ΔW_E',      f"{RR['diff']:+.2f}",    'lbs'),
            ('W_PL',      f"{Wpl:,.1f}",           'lbs'),
            ('W_crew',    f"{Wcrew:,.1f}",         'lbs'),
        ]
        tbl_html = (
            '<div class="dark-table-wrap"><table class="dark-table">'
            '<thead><tr><th>Symbol</th><th>Value</th><th>Unit</th></tr></thead>'
            '<tbody>')
        for sym, val, unit in sum_rows:
            tbl_html += (f'<tr><td>{sym}</td>'
                         f'<td class="val">{val}</td>'
                         f'<td class="unit">{unit}</td></tr>')
        tbl_html += '</tbody></table></div>'
        st.markdown(tbl_html, unsafe_allow_html=True)

        ratio_html = (
            '<div class="dark-table-wrap"><table class="dark-table">'
            '<thead><tr><th>Ratio</th><th>Value</th><th>Typical</th><th>✓</th></tr>'
            '</thead><tbody>')
        for nm, vr, lo_r, hi_r in [
            ('W_PL / W_TO', Wpl/Wto, 0.10, 0.25),
            ('W_F  / W_TO', WF/Wto,  0.20, 0.45),
            ('W_E  / W_TO', WE/Wto,  0.45, 0.65),
            ('W_PL / W_E',  Wpl/WE,  0.15, 0.40),
        ]:
            ok_r = lo_r <= vr <= hi_r
            chk  = '✓' if ok_r else ('▲' if vr > hi_r else '▼')
            chk_cls = 'check-ok' if ok_r else 'check-warn'
            ratio_html += (
                f'<tr><td>{nm}</td>'
                f'<td class="val">{vr:.4f}</td>'
                f'<td class="unit">{lo_r:.2f}–{hi_r:.2f}</td>'
                f'<td class="{chk_cls}">{chk}</td></tr>')
        ratio_html += '</tbody></table></div>'
        st.markdown(ratio_html, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────
# TAB 2 — Sensitivity
# ─────────────────────────────────────────────────────────
with tab2:
    s1, s2 = st.columns([1, 1], gap="medium")

    with s1:
        st.markdown(f"""
        <div class="card card-gold">
          <div class="card-title">Intermediate Factors — Eq. 2.22 – 2.44</div>
          <div class="sens-row" style="grid-template-columns:270px 1fr">
            <span class="sens-partial">C = 1−(1+M_res)(1−Mff)−M_tfo</span>
            <span style="font-family:'JetBrains Mono',monospace;font-size:.82rem;
                 font-weight:700;color:var(--gold2)">{S['C']:.5f}
              <span style="font-size:.63rem;color:#6e7681">Eq. 2.22</span>
            </span>
          </div>
          <div class="sens-row" style="grid-template-columns:270px 1fr">
            <span class="sens-partial">D = W_PL + W_crew</span>
            <span style="font-family:'JetBrains Mono',monospace;font-size:.82rem;
                 font-weight:700;color:var(--gold2)">{S['D']:,.0f} lbs
              <span style="font-size:.63rem;color:#6e7681">Eq. 2.23</span>
            </span>
          </div>
          <div class="sens-row" style="grid-template-columns:270px 1fr">
            <span class="sens-partial">C(1−B)W_TO − D  (denominator)</span>
            <span style="font-family:'JetBrains Mono',monospace;font-size:.82rem;
                 font-weight:700;color:var(--amber)">
              {S['C']*(1-float(B_v))*Wto-S['D']:,.0f} lbs
            </span>
          </div>
          <div class="sens-row" style="grid-template-columns:270px 1fr;border-bottom:none">
            <span class="sens-partial">F (sizing multiplier, Eq. 2.44)</span>
            <span style="font-family:'JetBrains Mono',monospace;font-size:.82rem;
                 font-weight:700;color:var(--pu)">{S['F']:,.0f} lbs</span>
          </div>
        </div>""", unsafe_allow_html=True)

        st.markdown(
            '<div class="card card-blue">'
            '<div class="card-title">Cruise Segment — Partial Derivatives</div>',
            unsafe_allow_html=True)
        for partial, val, unit, eq in [
            ('∂W_TO/∂Cp  (cruise)',   S['dCpR'], 'lbs / (lbs/hp/hr)', 'Eq. 2.49'),
            ('∂W_TO/∂η_p (cruise)',   S['dnpR'], 'lbs',               'Eq. 2.50'),
            ('∂W_TO/∂(L/D) cruise',  S['dLDR'], 'lbs',               'Eq. 2.51'),
            ('∂W_TO/∂R',             S['dR'],   'lbs / nm',          'Eq. 2.45'),
        ]:
            vc = 'sens-neg' if val < 0 else 'sens-pos'
            st.markdown(
                f'<div class="sens-row">'
                f'<span class="sens-partial">{partial}</span>'
                f'<span class="{vc}">{val:+,.1f}</span>'
                f'<span class="sens-unit">{unit}</span>'
                f'<span class="sens-eq">{eq}</span></div>',
                unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown(
            '<div class="card card-amber">'
            '<div class="card-title">Loiter Segment — Partial Derivatives</div>',
            unsafe_allow_html=True)
        for partial, val, unit in [
            ('∂W_TO/∂Cp  (loiter)',  S['dCpE'], 'lbs / (lbs/hp/hr)'),
            ('∂W_TO/∂η_p (loiter)', S['dnpE'], 'lbs'),
            ('∂W_TO/∂(L/D) loiter', S['dLDE'], 'lbs'),
        ]:
            vc = 'sens-neg' if val < 0 else 'sens-pos'
            st.markdown(
                f'<div class="sens-row" style="grid-template-columns:210px 110px 1fr">'
                f'<span class="sens-partial">{partial}</span>'
                f'<span class="{vc}">{val:+,.1f}</span>'
                f'<span class="sens-unit">{unit}</span></div>',
                unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with s2:
        r_lo   = max(100,  int(R_nm) - 500)
        r_hi   = min(6000, int(R_nm) + 500)
        ranges = list(range(r_lo, r_hi + 1, 40))
        wto_vals = []
        for r in ranges:
            try:
                w2, _ = solve_Wto({**P, 'R': float(r)})
                wto_vals.append(w2)
            except Exception:
                wto_vals.append(None)

        DARK = dict(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(11,15,22,.7)',
            font=dict(family='JetBrains Mono', color='#8b949e', size=9),
            margin=dict(l=8, r=8, t=42, b=8))
        AX_BASE = dict(
            gridcolor='rgba(255,255,255,.04)',
            linecolor='rgba(255,255,255,.09)')
        AX_SM = dict(**AX_BASE, tickfont=dict(size=9))

        fig_r = go.Figure()
        fig_r.add_trace(go.Scatter(
            x=ranges, y=wto_vals, mode='lines',
            line=dict(color='#c8a86c', width=2.5),
            fill='tozeroy', fillcolor='rgba(200,168,108,.06)'))
        fig_r.add_vline(
            x=R_nm, line=dict(color='rgba(63,185,80,.6)', width=1.5, dash='dash'),
            annotation_text=f'{R_nm} nm',
            annotation_font=dict(color='#3fb950', size=10, family='JetBrains Mono'))
        fig_r.update_layout(
            **DARK, height=260,
            title=dict(text='W_TO vs. Design Range (nm)',
                       font=dict(color='#c8a86c', size=12,
                                 family='DM Serif Display')),
            xaxis=dict(**AX_SM, title='Range (nm)'),
            yaxis=dict(**AX_SM, title='W_TO (lbs)'),
            showlegend=False)
        st.plotly_chart(fig_r, use_container_width=True)

        st.markdown(
            f'<div class="card card-amber">'
            f'<div class="card-title">Range Trade · ∂W_TO/∂R = {S["dR"]:+.2f} lbs/nm</div>',
            unsafe_allow_html=True)
        for dr in [-200, -100, +100, +200]:
            dw = S['dR'] * dr
            cv = '#3fb950' if dw < 0 else '#e3b341'
            st.markdown(
                f'<div style="display:flex;justify-content:space-between;'
                f'padding:.28rem 0;border-bottom:1px solid var(--border2);'
                f'font-size:.79rem">'
                f'<span style="color:#8b949e">ΔR = {dr:+d} nm</span>'
                f'<span style="font-family:JetBrains Mono,monospace;'
                f'font-weight:700;color:{cv}">{dw:+,.1f} lbs</span>'
                f'</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────
# TAB 3 — Charts  (✈ ENHANCED ANIMATED FLIGHT PATH)
# ─────────────────────────────────────────────────────────
with tab3:
    DARK3 = dict(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(11,15,22,.7)',
        font=dict(family='JetBrains Mono', color='#8b949e', size=9),
        margin=dict(l=8, r=8, t=44, b=8))
    AX3     = dict(gridcolor='rgba(255,255,255,.04)',
                   linecolor='rgba(255,255,255,.09)', tickfont=dict(size=9))
    AX3_SM8 = dict(gridcolor='rgba(255,255,255,.04)',
                   linecolor='rgba(255,255,255,.09)', tickfont=dict(size=8))
    def TITLE3(t):
        return dict(text=t, font=dict(color='#c8a86c', size=12,
                                      family='DM Serif Display'))

    # ══════════════════════════════════════════════════════════════════════
    # CHART 0 — Animated Mission Flight Path  ✈  (NEW)
    # ══════════════════════════════════════════════════════════════════════
    st.markdown(
        '<div class="sec-div">Chart 0 — Animated Mission Flight Path'
        ' &nbsp;·&nbsp; press ▶ Fly to animate the ✈</div>',
        unsafe_allow_html=True)

    # Waypoints: (dist_fraction, alt_fraction, label, text_position)
    _waypoints = [
        (0.000, 0.000, "Engine Start", "bottom center"),
        (0.040, 0.000, "Taxi",         "bottom center"),
        (0.085, 0.130, "Takeoff",      "bottom center"),
        (0.190, 1.000, "Climb",        "top center"),
        (0.660, 1.000, "Cruise",       "top center"),
        (0.760, 0.680, "Loiter",       "top center"),
        (0.890, 0.130, "Descent",      "bottom center"),
        (1.000, 0.000, "Landing",      "bottom center"),
    ]

    _CRUISE_ALT_FT = 25_000          # FL250 for regional turboprop
    _wx = np.array([w[0] for w in _waypoints])
    _wy = np.array([w[1] for w in _waypoints])

    # Cubic spline (scipy) or linear fallback
    try:
        from scipy.interpolate import CubicSpline
        _cs  = CubicSpline(_wx, _wy, bc_type='clamped')
        _t   = np.linspace(0, 1, 400)
        _ys  = np.clip(_cs(_t), 0, None)
    except ImportError:
        _t  = np.linspace(0, 1, 400)
        _ys = np.interp(_t, _wx, _wy)

    _dist_km = _t  * float(R_nm) * 1.852
    _alt_ft  = _ys * _CRUISE_ALT_FT
    _wp_dist = _wx * float(R_nm) * 1.852
    _wp_alt  = _wy * _CRUISE_ALT_FT
    _total_km = float(R_nm) * 1.852

    # ── Colour palette ────────────────────────────────────────────────────
    _GOLD    = "#c8a86c"
    _GOLD2   = "#e4c88a"
    _GOLD_F  = "rgba(200,168,108,0.13)"
    _TRAIL_C = "rgba(228,200,138,0.90)"
    _TC      = "#8b949e"
    _GREEN   = "#3fb950"
    _GRID_C  = "rgba(255,255,255,0.04)"
    _BG_C    = "rgba(11,15,22,0.85)"

    # ── Static base traces ────────────────────────────────────────────────
    _area_tr = go.Scatter(
        x=_dist_km, y=_alt_ft,
        mode="none", fill="tozeroy",
        fillcolor=_GOLD_F,
        hoverinfo="skip", showlegend=False)

    _line_tr = go.Scatter(
        x=_dist_km, y=_alt_ft,
        mode="lines",
        line=dict(color=_GOLD, width=2.2, shape="spline", smoothing=1.3),
        name="Flight path",
        hovertemplate="Dist: %{x:,.0f} km<br>Alt: %{y:,.0f} ft<extra></extra>",
        showlegend=False)

    _dot_tr = go.Scatter(
        x=_wp_dist, y=_wp_alt,
        mode="markers+text",
        marker=dict(color=_GOLD2, size=9,
                    line=dict(color="#07090d", width=1.5), symbol="circle"),
        text=[w[2] for w in _waypoints],
        textposition=[w[3] for w in _waypoints],
        textfont=dict(size=8.5, color=_TC, family="JetBrains Mono"),
        hovertemplate="%{text}<extra></extra>",
        showlegend=False)

    # ── Animation frames ──────────────────────────────────────────────────
    _N_FRAMES = 80
    _TRAIL    = 60          # tail length in data-points
    _f_idxs   = np.linspace(0, len(_t) - 1, _N_FRAMES, dtype=int)

    _frames = []
    for _fi, _idx in enumerate(_f_idxs):
        _ts = max(0, _idx - _TRAIL)
        _tx = _dist_km[_ts:_idx + 1]
        _ty = _alt_ft[_ts:_idx + 1]

        _frames.append(go.Frame(
            name=str(_fi),
            data=[
                _area_tr,
                _line_tr,
                _dot_tr,
                # Glowing golden trail
                go.Scatter(
                    x=_tx, y=_ty,
                    mode="lines",
                    line=dict(color=_TRAIL_C, width=5, shape="spline"),
                    showlegend=False, hoverinfo="skip"),
                # ✈ Airplane — large golden emoji as text marker
                go.Scatter(
                    x=[_dist_km[_idx]],
                    y=[_alt_ft[_idx]],
                    mode="markers+text",
                    marker=dict(symbol="circle", size=1,
                                color="rgba(0,0,0,0)"),
                    text=["✈"],
                    textposition="middle center",
                    textfont=dict(size=28, color=_GOLD2,
                                  family="Arial Unicode MS, Arial"),
                    showlegend=False, hoverinfo="skip"),
            ],
            traces=[0, 1, 2, 3, 4],
        ))

    # ── Assemble figure ───────────────────────────────────────────────────
    _fig_fp = go.Figure(
        data=[
            _area_tr,
            _line_tr,
            _dot_tr,
            # Initial empty trail
            go.Scatter(x=[], y=[], mode="lines",
                       line=dict(color=_TRAIL_C, width=5),
                       showlegend=False, hoverinfo="skip"),
            # Initial airplane at runway threshold
            go.Scatter(
                x=[_dist_km[0]], y=[_alt_ft[0]],
                mode="markers+text",
                marker=dict(symbol="circle", size=1, color="rgba(0,0,0,0)"),
                text=["✈"],
                textposition="middle center",
                textfont=dict(size=28, color=_GOLD2,
                              family="Arial Unicode MS, Arial"),
                showlegend=False, hoverinfo="skip"),
        ],
        frames=_frames,
    )

    _fig_fp.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=_BG_C,
        height=420,
        margin=dict(l=68, r=18, t=56, b=90),
        font=dict(family="JetBrains Mono", color=_TC, size=9),
        title=dict(
            text=(
                f"<b><span style='color:{_GOLD}'>Mission Flight Path</span></b>"
                f"<span style='color:{_TC};font-size:10px'>"
                f"  ·  {int(npax)} pax  ·  {int(R_nm)} nm  "
                f"·  FL{int(_CRUISE_ALT_FT//100):03d} cruise  "
                f"·  Mff = {RR['Mff']:.5f}</span>"
            ),
            font=dict(size=13, family="DM Serif Display, serif"),
            x=0.01, xanchor="left",
        ),
        xaxis=dict(
            title=dict(text="Distance (km)", font=dict(size=9, color=_TC)),
            gridcolor=_GRID_C,
            linecolor="rgba(255,255,255,0.09)",
            tickfont=dict(size=8, color=_TC),
            range=[-_total_km * 0.025, _total_km * 1.06],
            zeroline=False,
        ),
        yaxis=dict(
            title=dict(text="Altitude (ft)", font=dict(size=9, color=_TC)),
            gridcolor=_GRID_C,
            linecolor="rgba(255,255,255,0.09)",
            tickfont=dict(size=8, color=_TC),
            range=[-2200, _CRUISE_ALT_FT * 1.30],
            tickformat=",d",
            zeroline=True,
            zerolinecolor="rgba(255,255,255,0.10)",
            zerolinewidth=1,
        ),
        showlegend=False,
        # ── Animation controls ──────────────────────────────────────────
        updatemenus=[dict(
            type="buttons",
            showactive=False,
            x=0.0, y=-0.22,
            xanchor="left", yanchor="top",
            bgcolor="rgba(12,15,22,0.95)",
            bordercolor="rgba(200,168,108,0.40)",
            borderwidth=1,
            font=dict(size=12, color=_GOLD2, family="JetBrains Mono"),
            buttons=[
                dict(
                    label="▶  Fly",
                    method="animate",
                    args=[None, dict(
                        frame=dict(duration=28, redraw=True),
                        fromcurrent=True,
                        transition=dict(duration=0),
                        mode="immediate")]),
                dict(
                    label="  ⏸  Pause  ",
                    method="animate",
                    args=[[None], dict(
                        frame=dict(duration=0, redraw=False),
                        mode="immediate",
                        transition=dict(duration=0))]),
                dict(
                    label="  ↺  Reset  ",
                    method="animate",
                    args=[["0"], dict(
                        frame=dict(duration=0, redraw=True),
                        mode="immediate",
                        transition=dict(duration=0))]),
            ],
        )],
        sliders=[dict(
            active=0,
            pad=dict(t=14, b=0, l=0),
            len=1.0, x=0.0, y=-0.12,
            bgcolor="rgba(0,0,0,0)",
            bordercolor="rgba(200,168,108,0.20)",
            tickcolor="rgba(200,168,108,0.30)",
            currentvalue=dict(visible=False),
            font=dict(size=7, color=_TC),
            steps=[
                dict(
                    method="animate",
                    label="",
                    args=[[str(_fi)], dict(
                        frame=dict(duration=0, redraw=True),
                        mode="immediate",
                        transition=dict(duration=0))],
                )
                for _fi in range(_N_FRAMES)
            ],
        )],
    )

    # FL250 cruise altitude dashed reference
    _fig_fp.add_hline(
        y=_CRUISE_ALT_FT,
        line=dict(color="rgba(72,117,194,0.28)", width=1, dash="dot"),
        annotation_text=f"FL{int(_CRUISE_ALT_FT//100):03d}",
        annotation_font=dict(size=8, color="rgba(106,158,234,0.7)",
                             family="JetBrains Mono"),
        annotation_position="left",
    )

    # Ground line
    _fig_fp.add_hline(
        y=0,
        line=dict(color="rgba(63,185,80,0.20)", width=1),
    )

    st.plotly_chart(_fig_fp, use_container_width=True)
    st.markdown(
        f'<div style="font-size:.68rem;color:#6e7681;margin:-6px 0 18px;line-height:1.7">'
        f'<b style="color:{_GOLD2}">✈ Golden airplane</b> sweeps from takeoff to landing  '
        f'&nbsp;·&nbsp; Press <b style="color:{_GOLD2}">▶ Fly</b> to animate  '
        f'&nbsp;·&nbsp; Drag the slider to scrub through the flight  '
        f'&nbsp;·&nbsp; Cubic-spline altitude profile across 8 Raymer mission phases'
        f'</div>',
        unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════
    # Chart 1 — Phase fractions
    # ══════════════════════════════════════════════════════════════════════
    st.markdown(
        '<div class="sec-div">Chart 1 — Mission Phase Weight Fractions</div>',
        unsafe_allow_html=True)
    phases_l = list(RR['phases'].keys())
    fvals    = [v for v, _, _ in RR['phases'].values()]
    ftypes   = [t for _, t, _ in RR['phases'].values()]
    cum_p    = [1.0]
    for fv in fvals:
        cum_p.append(cum_p[-1] * fv)
    bar_col = ['#6a9eea' if t == 'Fixed' else '#c8a86c' for t in ftypes]

    fig1 = make_subplots(rows=1, cols=2, subplot_titles=[
        "Wi/Wi-1 per phase (closer to 1.0 = less fuel burned)",
        "Cumulative Mff (starts at 1.0, ends at Mff)"])
    fig1.add_trace(go.Bar(
        x=phases_l, y=fvals, marker_color=bar_col,
        marker_line=dict(width=0),
        text=[f'{v:.4f}' for v in fvals],
        textposition='outside', textfont=dict(size=8, color='#8b949e')),
        row=1, col=1)
    fig1.add_trace(go.Scatter(
        x=['Ramp'] + phases_l, y=cum_p, mode='lines+markers',
        line=dict(color='#c8a86c', width=2.5),
        marker=dict(color='#e4c88a', size=7,
                    line=dict(color='#c8a86c', width=1.5)),
        fill='tozeroy', fillcolor='rgba(200,168,108,.06)'),
        row=1, col=2)
    fig1.update_layout(**DARK3, height=340, showlegend=False)
    fig1.update_xaxes(**AX3)
    fig1.update_yaxes(**AX3)
    fig1.update_annotations(font=dict(color='#c8a86c', size=10))
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown(
        f'<div style="font-size:.7rem;color:#6e7681;margin:-6px 0 12px;line-height:1.65">'
        f'Blue bars = fixed fractions (Table 2.1) &nbsp;·&nbsp; '
        f'Gold bars = Breguet equations &nbsp;·&nbsp; '
        f'Cruise fraction = {[v for v,t,_ in RR["phases"].values() if t=="Breguet"][0]:.4f}'
        f'</div>', unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════
    # Chart 2 — Convergence
    # ══════════════════════════════════════════════════════════════════════
    st.markdown(
        '<div class="sec-div">Chart 2 — Sizing Convergence: '
        'W_E_tent = W_E_allow at the solution W_TO</div>',
        unsafe_allow_html=True)
    wto_rng  = np.linspace(Wto * 0.55, Wto * 1.5, 150)
    we_tent  = []; we_allow = []
    for w in wto_rng:
        try:
            rr2 = compute_mission({**P, 'Wto': float(w)})
            we_tent.append(rr2['WE']); we_allow.append(rr2['WEa'])
        except Exception:
            we_tent.append(None); we_allow.append(None)

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=list(wto_rng), y=we_tent, mode='lines',
        name='W_E Tentative (from mission)',
        line=dict(color='#6a9eea', width=2.5)))
    fig2.add_trace(go.Scatter(
        x=list(wto_rng), y=we_allow, mode='lines',
        name='W_E Allowable (regression)',
        line=dict(color='#c8a86c', width=2.5)))
    fig2.add_vline(x=Wto, line=dict(
        color='rgba(63,185,80,.65)', width=1.5, dash='dash'))
    fig2.add_annotation(
        x=Wto, y=WE,
        text=f'Solution<br>W_TO={Wto:,.0f} lbs',
        font=dict(color='#3fb950', size=9, family='JetBrains Mono'),
        showarrow=True, arrowcolor='rgba(63,185,80,.5)',
        ax=40, ay=-40,
        bgcolor='rgba(7,9,13,.8)',
        bordercolor='rgba(63,185,80,.3)', borderwidth=1)
    fig2.update_layout(
        **DARK3, height=310,
        title=TITLE3('Sizing Loop Convergence'),
        xaxis=dict(**AX3, title='W_TO (lbs)'),
        yaxis=dict(**AX3, title='W_E (lbs)'),
        legend=dict(font=dict(size=9, color='#8b949e'),
                    bgcolor='rgba(0,0,0,0)', x=0.02, y=0.98))
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown(
        '<div style="font-size:.7rem;color:#6e7681;margin:-6px 0 12px;line-height:1.65">'
        'Blue line = tentative W_E from mission analysis &nbsp;·&nbsp; '
        'Gold line = allowable W_E from regression &nbsp;·&nbsp; '
        'They intersect at the solution W_TO (green dot).</div>',
        unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════
    # Charts 3 & 4
    # ══════════════════════════════════════════════════════════════════════
    st.markdown(
        '<div class="sec-div">Chart 3 — Weight Composition &nbsp;&nbsp; '
        'Chart 4 — Sensitivity Tornado</div>',
        unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    with c1:
        labels = ['W_F  Fuel', 'W_PL  Payload',
                  'W_tfo  Trapped', 'W_crew  Crew', 'W_E  Empty']
        values = [WF, Wpl, Wtfo_r, Wcrew, WE]
        fig3   = go.Figure(go.Pie(
            labels=labels, values=values, hole=0.52,
            marker=dict(
                colors=['#c8a86c','#6a9eea','#e3b341','#9c72d4','#3fb950'],
                line=dict(color='#07090d', width=2)),
            textfont=dict(size=9, family='JetBrains Mono'),
            hovertemplate=(
                '<b>%{label}</b><br>'
                '%{value:,.0f} lbs<br>'
                '%{percent}<extra></extra>')))
        fig3.add_annotation(
            text=f'<b>{Wto:,.0f}</b><br>lbs W_TO',
            xref='paper', yref='paper', x=0.5, y=0.5,
            font=dict(size=10, color='#c8a86c', family='JetBrains Mono'),
            showarrow=False, align='center')
        fig3.update_layout(
            **DARK3, title=TITLE3('Weight Composition'), height=300,
            legend=dict(font=dict(size=8), bgcolor='rgba(0,0,0,0)'))
        st.plotly_chart(fig3, use_container_width=True)

    with c2:
        sp = [
            ('∂W/∂Cp cruise',  S['dCpR']),
            ('∂W/∂η_p cruise', S['dnpR']),
            ('∂W/∂(L/D) cr.',  S['dLDR']),
            ('∂W/∂R',          S['dR']),
            ('∂W/∂Cp loiter',  S['dCpE']),
            ('∂W/∂η_p loiter', S['dnpE']),
            ('∂W/∂(L/D) lt.',  S['dLDE']),
        ]
        sp_s  = sorted(sp, key=lambda x: abs(x[1]), reverse=True)
        slbl  = [x[0] for x in sp_s]
        sval  = [x[1] for x in sp_s]
        scol  = ['rgba(248,81,73,.75)' if v > 0
                 else 'rgba(63,185,80,.75)' for v in sval]
        fig4  = go.Figure(go.Bar(
            y=slbl, x=sval, orientation='h',
            marker_color=scol, marker_line=dict(width=0),
            text=[f'{v:+,.1f}' for v in sval],
            textposition='outside',
            textfont=dict(size=8, color='#8b949e')))
        fig4.add_vline(x=0, line=dict(
            color='rgba(255,255,255,.12)', width=1))
        fig4.update_layout(
            **DARK3, title=TITLE3('Sensitivity Tornado  ∂W_TO/∂X'),
            height=300,
            xaxis=dict(**AX3_SM8, title='∂W_TO (lbs / unit)'),
            yaxis=dict(**AX3_SM8))
        st.plotly_chart(fig4, use_container_width=True)


# ─────────────────────────────────────────────────────────
# TAB 4 — Export
# ─────────────────────────────────────────────────────────
with tab4:
    e1, e2 = st.columns(2, gap="medium")

    # ── CSV ──
    with e1:
        st.markdown(
            '<div class="sec-div">Full Results — CSV</div>',
            unsafe_allow_html=True)
        exp_rows = [
            ('W_TO',       round(Wto, 2),            'lbs'),
            ('Mff',        round(RR['Mff'], 6),       '—'),
            ('W_F',        round(WF, 2),              'lbs'),
            ('W_F_usable', round(RR['WFu'], 2),       'lbs'),
            ('W_tfo',      round(Wtfo_r, 3),          'lbs'),
            ('W_OE',       round(WOE, 2),             'lbs'),
            ('W_E_tent',   round(WE, 2),              'lbs'),
            ('W_E_allow',  round(RR['WEa'], 2),       'lbs'),
            ('delta_WE',   round(RR['diff'], 3),      'lbs'),
            ('W_PL',       round(Wpl, 2),             'lbs'),
            ('W_crew',     round(Wcrew, 2),           'lbs'),
            ('Rc_sm',      round(RR['Rc'], 3),        'stat.mi'),
            ('Vm_mph',     round(RR['Vm'], 3),        'mph'),
            ('F',          round(S['F'], 2),          '—'),
            ('C',          round(S['C'], 6),          '—'),
            ('D',          round(S['D'], 2),          'lbs'),
        ]
        exp_html = (
            '<div class="dark-table-wrap"><table class="dark-table">'
            '<thead><tr><th>Parameter</th><th>Value</th><th>Units</th></tr></thead>'
            '<tbody>')
        for param, val, unit in exp_rows:
            exp_html += (f'<tr><td>{param}</td>'
                         f'<td class="val">{val}</td>'
                         f'<td class="unit">{unit}</td></tr>')
        exp_html += '</tbody></table></div>'
        st.markdown(exp_html, unsafe_allow_html=True)

        df_exp = pd.DataFrame({
            'Parameter': [r[0] for r in exp_rows],
            'Value':     [r[1] for r in exp_rows],
            'Units':     [r[2] for r in exp_rows]})
        b = io.StringIO()
        df_exp.to_csv(b, index=False)
        st.download_button(
            "⬇  Download CSV", b.getvalue(),
            "aerosizer_results.csv", "text/csv",
            use_container_width=True)

    # ── PDF ──
    with e2:
        st.markdown(
            '<div class="sec-div">PDF Report — A4 · Print-Ready</div>',
            unsafe_allow_html=True)

        def make_pdf():
            buf = io.BytesIO()
            doc = SimpleDocTemplate(buf, pagesize=A4,
                leftMargin=2.0*cm, rightMargin=2.0*cm,
                topMargin=2.2*cm,  bottomMargin=2.2*cm)
            PW = 17.0*cm

            C_WHITE   = colors.HexColor('#FFFFFF')
            C_NEAR_W  = colors.HexColor('#F8F9FA')
            C_LIGHT   = colors.HexColor('#EEF1F4')
            C_BLACK   = colors.HexColor('#1A1A1A')
            C_DARK    = colors.HexColor('#2C3E50')
            C_GRAY    = colors.HexColor('#5A6A7A')
            C_LGRAY   = colors.HexColor('#8A9BAB')
            C_BORDER  = colors.HexColor('#C8D0D8')
            C_BORDER2 = colors.HexColor('#E0E5EA')
            C_GOLD    = colors.HexColor('#8B6914')
            C_BLUE    = colors.HexColor('#1A4A8A')
            C_GREEN   = colors.HexColor('#1A6B3A')
            C_RED     = colors.HexColor('#8B1A1A')
            C_HDR     = colors.HexColor('#2C3E50')
            C_HDR_TXT = colors.HexColor('#FFFFFF')
            C_PANEL   = colors.HexColor('#F2F4F7')

            sty = getSampleStyleSheet()
            def ps(nm, **kw):
                return ParagraphStyle(nm, parent=sty['Normal'], **kw)

            sH1_RULE = ps('H1R', fontSize=12, fontName='Helvetica-Bold',
                           textColor=C_HDR, spaceBefore=14, spaceAfter=5, leading=15)
            sH2      = ps('H2',  fontSize=10, fontName='Helvetica-Bold',
                           textColor=C_BLUE, spaceBefore=8, spaceAfter=3, leading=13)
            sBODY    = ps('BD',  fontSize=8.5, fontName='Helvetica',
                           textColor=C_BLACK, leading=13, spaceAfter=3)
            sNOTE    = ps('NT',  fontSize=7.5, fontName='Helvetica',
                           textColor=C_LGRAY, leading=11, spaceAfter=2)
            sFOOT    = ps('FT',  fontSize=7,  fontName='Helvetica',
                           textColor=C_LGRAY, alignment=TA_CENTER)
            sEQ_LBL  = ps('EL',  fontSize=8,  fontName='Helvetica-Oblique',
                           textColor=C_GRAY, leading=11, spaceAfter=1)
            sEQ      = ps('EQ',  fontSize=9,  fontName='Courier-Bold',
                           textColor=C_DARK, backColor=C_PANEL,
                           leading=14, spaceBefore=1, spaceAfter=6,
                           leftIndent=12, rightIndent=8, borderPad=5)
            sEQ_SUB  = ps('ES',  fontSize=7.5, fontName='Courier',
                           textColor=C_GRAY, leading=11,
                           leftIndent=12, spaceAfter=4)
            sANAL    = ps('AN',  fontSize=8.5, fontName='Helvetica',
                           textColor=C_BLACK, leading=13, spaceAfter=3)

            def build_table(data, col_widths, val_cols=None,
                             highlight_last=False, font_sz=8):
                val_cols = val_cols or []
                t = Table(data, colWidths=col_widths,
                           repeatRows=1, splitByRow=False)
                style = [
                    ('BACKGROUND',    (0,0),  (-1,0),  C_HDR),
                    ('TEXTCOLOR',     (0,0),  (-1,0),  C_HDR_TXT),
                    ('FONTNAME',      (0,0),  (-1,0),  'Helvetica-Bold'),
                    ('FONTSIZE',      (0,0),  (-1,-1), font_sz),
                    ('LEADING',       (0,0),  (-1,-1), font_sz + 3),
                    ('ALIGN',         (0,0),  (-1,0),  'CENTER'),
                    ('VALIGN',        (0,0),  (-1,-1), 'MIDDLE'),
                    ('LINEBELOW',     (0,0),  (-1,0),  1.5, C_GOLD),
                    ('FONTNAME',      (0,1),  (-1,-1), 'Helvetica'),
                    ('TEXTCOLOR',     (0,1),  (-1,-1), C_BLACK),
                    ('GRID',          (0,0),  (-1,-1), 0.4, C_BORDER),
                    ('LEFTPADDING',   (0,0),  (-1,-1), 7),
                    ('RIGHTPADDING',  (0,0),  (-1,-1), 7),
                    ('TOPPADDING',    (0,0),  (-1,-1), 4),
                    ('BOTTOMPADDING', (0,0),  (-1,-1), 4),
                    ('FONTNAME',      (0,1),  (0,-1),  'Helvetica-Bold'),
                    ('TEXTCOLOR',     (0,1),  (0,-1),  C_DARK),
                ]
                for i in range(1, len(data)):
                    bg = C_NEAR_W if i % 2 == 1 else C_WHITE
                    style.append(('BACKGROUND', (0,i), (-1,i), bg))
                for vc in val_cols:
                    style += [
                        ('FONTNAME',  (vc,1), (vc,-1), 'Courier-Bold'),
                        ('TEXTCOLOR', (vc,1), (vc,-1), C_DARK),
                        ('ALIGN',     (vc,1), (vc,-1), 'RIGHT'),
                    ]
                if highlight_last:
                    style += [
                        ('BACKGROUND', (0,-1), (-1,-1), C_LIGHT),
                        ('FONTNAME',   (0,-1), (-1,-1), 'Helvetica-Bold'),
                        ('TEXTCOLOR',  (0,-1), (-1,-1), C_DARK),
                    ]
                t.setStyle(TableStyle(style))
                return KeepTogether(t)

            def make_mission_profile(width=PW, height=5.5*cm):
                d = Drawing(width, height)
                d.add(Rect(0, 0, width, height,
                           fillColor=C_WHITE,
                           strokeColor=C_BORDER, strokeWidth=0.8))
                d.add(String(width/2, height - 13,
                             'Figure 1 — Mission Profile: Altitude vs. Distance',
                             textAnchor='middle', fontSize=8.5,
                             fontName='Helvetica-Bold', fillColor=C_DARK))
                ml, mr, mb, mt = 32, 15, 30, 22
                cw = width - ml - mr
                ch = height - mb - mt
                profile = [
                    (0.00, 0.00, 'Engine Start'),
                    (0.04, 0.00, 'Taxi'),
                    (0.08, 0.12, 'Takeoff'),
                    (0.18, 0.85, 'Climb'),
                    (0.65, 0.85, 'Cruise'),
                    (0.75, 0.62, 'Loiter'),
                    (0.88, 0.12, 'Descent'),
                    (1.00, 0.00, 'Landing'),
                ]
                pts_x = [ml + cw * p[0] for p in profile]
                pts_y = [mb + ch * p[1] for p in profile]
                fill = [ml, mb]
                for px, py in zip(pts_x, pts_y):
                    fill += [px, py]
                fill += [ml + cw, mb]
                d.add(Polygon(fill,
                              fillColor=colors.HexColor('#EEF4FA'),
                              strokeWidth=0))
                for i in range(len(profile) - 1):
                    d.add(Line(pts_x[i], pts_y[i],
                               pts_x[i+1], pts_y[i+1],
                               strokeColor=C_BLUE, strokeWidth=1.8))
                for i, (df, af, lbl) in enumerate(profile):
                    px = ml + cw * df
                    py = mb + ch * af
                    d.add(Circle(px, py, 3.2,
                                 fillColor=C_GOLD,
                                 strokeColor=C_WHITE, strokeWidth=0.8))
                    ly = py + 7 if af < 0.5 else py - 14
                    d.add(String(px, ly, lbl,
                                 textAnchor='middle', fontSize=6,
                                 fontName='Helvetica', fillColor=C_GRAY))
                d.add(Line(ml, mb, ml + cw, mb,
                           strokeColor=C_BORDER, strokeWidth=0.8))
                d.add(Line(ml, mb, ml, mb + ch,
                           strokeColor=C_BORDER, strokeWidth=0.8))
                d.add(String(ml + cw/2, 10,
                             'Distance  (nm)', textAnchor='middle',
                             fontSize=7, fontName='Helvetica', fillColor=C_GRAY))
                d.add(String(10, mb + ch/2,
                             'Altitude', textAnchor='middle',
                             fontSize=7, fontName='Helvetica', fillColor=C_GRAY))
                return d

            def make_bar(labels, values, bar_colors,
                          width=PW, height=5.0*cm, title=''):
                d = Drawing(width, height)
                d.add(Rect(0, 0, width, height,
                           fillColor=C_WHITE,
                           strokeColor=C_BORDER, strokeWidth=0.8))
                if title:
                    d.add(String(width/2, height - 13, title,
                                 textAnchor='middle', fontSize=8.5,
                                 fontName='Helvetica-Bold', fillColor=C_DARK))
                ml, mr, mb = 20, 15, 28
                cw = width - ml - mr
                ch = height - mb - 20
                n  = len(values)
                bar_w = cw / n * 0.6
                gap   = cw / n
                max_v = max(abs(v) for v in values) if values else 1
                for gi in range(5):
                    gy = mb + ch * gi / 4
                    d.add(Line(ml, gy, ml + cw, gy,
                               strokeColor=C_BORDER2, strokeWidth=0.4))
                    d.add(String(ml - 3, gy - 3,
                                 f'{max_v*gi/4:.4f}',
                                 textAnchor='end', fontSize=5.5,
                                 fontName='Courier', fillColor=C_LGRAY))
                for i, (lbl, val, col) in enumerate(
                        zip(labels, values, bar_colors)):
                    bx = ml + i * gap + gap/2 - bar_w/2
                    bh = ch * abs(val) / max_v
                    d.add(Rect(bx, mb, bar_w, bh,
                               fillColor=col, strokeWidth=0))
                    d.add(String(bx + bar_w/2, mb + bh + 2,
                                 f'{val:.4f}',
                                 textAnchor='middle', fontSize=5.5,
                                 fontName='Courier', fillColor=C_GRAY))
                    d.add(String(bx + bar_w/2, mb - 12,
                                 lbl[:7],
                                 textAnchor='middle', fontSize=5.5,
                                 fontName='Helvetica', fillColor=C_GRAY))
                return d

            def make_convergence(Wto_sol, WE_sol,
                                  width=PW, height=5.5*cm, title=''):
                d = Drawing(width, height)
                d.add(Rect(0, 0, width, height,
                           fillColor=C_WHITE,
                           strokeColor=C_BORDER, strokeWidth=0.8))
                if title:
                    d.add(String(width/2, height - 13, title,
                                 textAnchor='middle', fontSize=8.5,
                                 fontName='Helvetica-Bold', fillColor=C_DARK))
                ml, mr, mb, mt = 55, 15, 22, 22
                cw = width - ml - mr
                ch = height - mb - mt
                pts_t = []; pts_a = []
                w_vals = [Wto_sol * (0.55 + 0.95*i/39) for i in range(40)]
                for w in w_vals:
                    try:
                        rr2 = compute_mission({**P, 'Wto': float(w)})
                        pts_t.append((w, rr2['WE']))
                        pts_a.append((w, rr2['WEa']))
                    except Exception:
                        pass
                if not pts_t:
                    return d
                all_y = [y for _, y in pts_t + pts_a]
                min_w = w_vals[0]; max_w = w_vals[-1]
                min_y = min(all_y); max_y = max(all_y)
                rng_w = max_w - min_w or 1
                rng_y = max_y - min_y or 1
                def tx(w): return ml + cw*(w-min_w)/rng_w
                def ty(y): return mb + ch*(y-min_y)/rng_y
                for gi in range(5):
                    gy = mb + ch*gi/4
                    gv = min_y + rng_y*gi/4
                    d.add(Line(ml, gy, ml+cw, gy,
                               strokeColor=C_BORDER2, strokeWidth=0.3))
                    d.add(String(ml-3, gy-3, f'{gv:,.0f}',
                                 textAnchor='end', fontSize=5.5,
                                 fontName='Courier', fillColor=C_LGRAY))
                for i in range(len(pts_t)-1):
                    d.add(Line(tx(pts_t[i][0]),  ty(pts_t[i][1]),
                               tx(pts_t[i+1][0]),ty(pts_t[i+1][1]),
                               strokeColor=C_BLUE, strokeWidth=1.8))
                for i in range(len(pts_a)-1):
                    d.add(Line(tx(pts_a[i][0]),  ty(pts_a[i][1]),
                               tx(pts_a[i+1][0]),ty(pts_a[i+1][1]),
                               strokeColor=C_GOLD, strokeWidth=1.8))
                sx = tx(Wto_sol); sy = ty(WE_sol)
                d.add(Circle(sx, sy, 5,
                             fillColor=C_GREEN,
                             strokeColor=C_WHITE, strokeWidth=1.0))
                d.add(Line(sx, mb, sx, sy,
                           strokeColor=C_GREEN, strokeWidth=0.9,
                           strokeDashArray=[3,2]))
                d.add(String(sx+6, sy+2,
                             f'W_TO = {Wto_sol:,.0f} lbs',
                             fontSize=6.5, fontName='Courier-Bold',
                             fillColor=C_GREEN))
                d.add(Line(ml, height-10, ml+14, height-10,
                           strokeColor=C_BLUE, strokeWidth=1.8))
                d.add(String(ml+16, height-13,
                             'W_E Tentative',
                             fontSize=6, fontName='Helvetica', fillColor=C_GRAY))
                d.add(Line(ml+80, height-10, ml+94, height-10,
                           strokeColor=C_GOLD, strokeWidth=1.8))
                d.add(String(ml+96, height-13,
                             'W_E Allowable',
                             fontSize=6, fontName='Helvetica', fillColor=C_GRAY))
                return d

            def make_tornado(S_d, width=PW, height=6.0*cm, title=''):
                d = Drawing(width, height)
                d.add(Rect(0, 0, width, height,
                           fillColor=C_WHITE,
                           strokeColor=C_BORDER, strokeWidth=0.8))
                if title:
                    d.add(String(width/2, height - 13, title,
                                 textAnchor='middle', fontSize=8.5,
                                 fontName='Helvetica-Bold', fillColor=C_DARK))
                items = [
                    ('dW/dCp (cruise)',  S_d['dCpR']),
                    ('dW/deta_p (cr.)',  S_d['dnpR']),
                    ('dW/d(L/D) (cr.)',  S_d['dLDR']),
                    ('dW/dR',           S_d['dR']),
                    ('dW/dCp (loiter)', S_d['dCpE']),
                    ('dW/deta_p (lt.)', S_d['dnpE']),
                    ('dW/d(L/D) (lt.)', S_d['dLDE']),
                ]
                items_s = sorted(items, key=lambda x: abs(x[1]), reverse=True)
                max_abs = max(abs(v) for _, v in items_s) or 1
                ml, mr, mb, mt = 90, 55, 16, 22
                cw = width - ml - mr
                ch = height - mb - mt
                n  = len(items_s)
                bar_h = ch / n * 0.55
                gap   = ch / n
                cx_l  = ml + cw/2
                for i, (lbl, val) in enumerate(items_s):
                    bar_y = mb + ch - (i+1)*gap + gap/2 - bar_h/2
                    bw = cw/2 * abs(val) / max_abs
                    col = C_RED if val > 0 else C_GREEN
                    if val > 0:
                        d.add(Rect(cx_l, bar_y, bw, bar_h,
                                   fillColor=col, strokeWidth=0))
                        d.add(String(cx_l+bw+3, bar_y+bar_h/2-3,
                                     f'{val:+,.1f}', fontSize=6,
                                     fontName='Courier', fillColor=col))
                    else:
                        d.add(Rect(cx_l-bw, bar_y, bw, bar_h,
                                   fillColor=col, strokeWidth=0))
                        d.add(String(cx_l-bw-3, bar_y+bar_h/2-3,
                                     f'{val:+,.1f}', fontSize=6,
                                     textAnchor='end',
                                     fontName='Courier', fillColor=col))
                    d.add(String(ml-3, bar_y+bar_h/2-3, lbl,
                                 textAnchor='end', fontSize=6,
                                 fontName='Helvetica', fillColor=C_DARK))
                d.add(Line(cx_l, mb, cx_l, mb+ch,
                           strokeColor=C_GRAY, strokeWidth=0.6))
                d.add(Rect(width-mr+2, mb+ch-8, 8, 7,
                           fillColor=C_RED, strokeWidth=0))
                d.add(String(width-mr+12, mb+ch-7,
                             '+ve: raises W_TO',
                             fontSize=5.5, fontName='Helvetica', fillColor=C_GRAY))
                d.add(Rect(width-mr+2, mb+ch-18, 8, 7,
                           fillColor=C_GREEN, strokeWidth=0))
                d.add(String(width-mr+12, mb+ch-17,
                             '-ve: reduces W_TO',
                             fontSize=5.5, fontName='Helvetica', fillColor=C_GRAY))
                return d

            def make_pie(pie_lbl, pie_val, pie_col,
                          width=8*cm, height=7*cm, title=''):
                d = Drawing(width, height)
                d.add(Rect(0, 0, width, height,
                           fillColor=C_WHITE,
                           strokeColor=C_BORDER, strokeWidth=0.8))
                if title:
                    d.add(String(width/2, height-13, title,
                                 textAnchor='middle', fontSize=8,
                                 fontName='Helvetica-Bold', fillColor=C_DARK))
                cx, cy = width/2 - 5, height/2 - 8
                r      = min(width, height) * 0.27
                total  = sum(pie_val)
                start  = 90
                for lbl, val, col in zip(pie_lbl, pie_val, pie_col):
                    sweep = 360 * val / total
                    steps = max(8, int(sweep/5))
                    pts   = [cx, cy]
                    for s in range(steps+1):
                        ang = math.radians(start + sweep*s/steps)
                        pts.extend([cx + r*math.cos(ang),
                                    cy + r*math.sin(ang)])
                    d.add(Polygon(pts, fillColor=col,
                                  strokeColor=C_WHITE, strokeWidth=1.2))
                    mid = math.radians(start + sweep/2)
                    lx  = cx + (r+14)*math.cos(mid)
                    ly  = cy + (r+14)*math.sin(mid)
                    pct = val/total*100
                    d.add(String(lx, ly-3,
                                 f'{lbl.split()[0]} {pct:.1f}%',
                                 textAnchor='middle', fontSize=5.5,
                                 fontName='Helvetica', fillColor=C_DARK))
                    start += sweep
                d.add(String(cx, cy-4, f'{total:,.0f}',
                             textAnchor='middle', fontSize=8,
                             fontName='Courier-Bold', fillColor=C_DARK))
                d.add(String(cx, cy-13, 'lbs W_TO',
                             textAnchor='middle', fontSize=6,
                             fontName='Helvetica', fillColor=C_GRAY))
                return d

            # ═══════════════ STORY BUILD ═══════════════
            story = []

            # Cover
            cov = [[
                Paragraph(
                    '<font color="#2C3E50"><b>AeroSizer Pro</b></font>',
                    ps('CVT', fontSize=22, fontName='Helvetica-Bold',
                       textColor=C_DARK, leading=26)),
                Paragraph(
                    '<font color="#5A6A7A">Raymer (2018), Chapter 2</font><br/>'
                    '<font color="#8A9BAB">Propeller Aircraft — Conceptual Weight Sizing</font><br/>'
                    f'<font color="#8A9BAB">W_TO = {Wto:,.1f} lbs  |  '
                    f'Mff = {RR["Mff"]:.6f}</font>',
                    ps('CVS', fontSize=8.5, textColor=C_GRAY,
                       leading=13, alignment=TA_RIGHT))
            ]]
            cov_t = Table(cov, colWidths=[PW*0.55, PW*0.45])
            cov_t.setStyle(TableStyle([
                ('BACKGROUND',    (0,0),(-1,-1), C_WHITE),
                ('TOPPADDING',    (0,0),(-1,-1), 10),
                ('BOTTOMPADDING', (0,0),(-1,-1), 10),
                ('LEFTPADDING',   (0,0),(-1,-1), 0),
                ('RIGHTPADDING',  (0,0),(-1,-1), 0),
                ('VALIGN',        (0,0),(-1,-1), 'MIDDLE'),
            ]))
            story.append(cov_t)
            story.append(HRFlowable(width=PW, thickness=2.0,
                                     color=C_DARK, spaceBefore=2, spaceAfter=4))

            sc_hex = '#1A6B3A' if conv else '#8B1A1A'
            sc     = C_GREEN   if conv else C_RED
            cv_d   = [[Paragraph(
                f'<font color="{sc_hex}"><b>{"[OK] CONVERGED" if conv else "[!!] NOT CONVERGED"}</b></font>'
                f'<font color="#5A6A7A">  W_TO = {Wto:,.1f} lbs  |  '
                f'Mff = {RR["Mff"]:.6f}  |  '
                f'delta_W_E = {RR["diff"]:+.2f} lbs</font>',
                ps('CVB', fontSize=8.5, fontName='Helvetica-Bold',
                   textColor=sc, backColor=C_LIGHT, leading=13))
            ]]
            cv_t = Table(cv_d, colWidths=[PW])
            cv_t.setStyle(TableStyle([
                ('BACKGROUND',    (0,0),(0,0), C_LIGHT),
                ('LINEBELOW',     (0,0),(0,0), 2.0, sc),
                ('LEFTPADDING',   (0,0),(0,0), 10),
                ('TOPPADDING',    (0,0),(0,0), 7),
                ('BOTTOMPADDING', (0,0),(0,0), 7),
            ]))
            story.append(cv_t)
            story.append(Spacer(1, 0.3*cm))

            story.append(HRFlowable(width=PW, thickness=0.6, color=C_BORDER,
                                     spaceBefore=0, spaceAfter=3))
            story.append(Paragraph('0   NOMENCLATURE & SYMBOL REFERENCE', sH1_RULE))
            story.append(Paragraph(
                'All symbols, units, and abbreviations used throughout this report '
                'are defined below. Conventions follow Raymer (2018), Chapter 2.',
                sBODY))
            nom = [
                ['Symbol', 'Full Name', 'Units', 'Definition'],
                ['W_TO',   'Gross Takeoff Weight',        'lbs',   'Total aircraft weight at start of mission.'],
                ['W_E',    'Empty Weight (tentative)',     'lbs',   'Computed from mission sizing.'],
                ['W_Ea',   'Empty Weight (allowable)',     'lbs',   '10^[(log10(W_TO) - A) / B]. From regression.'],
                ['delta_WE','Convergence Error',           'lbs',   'W_Ea - W_E. Solution when |delta_WE| < 1 lb.'],
                ['W_OE',   'Operating Empty Weight',       'lbs',   'W_E + W_tfo + W_crew.'],
                ['W_F',    'Total Fuel Weight',            'lbs',   'W_F_used x (1 + M_res).'],
                ['W_F_used','Usable Fuel',                 'lbs',   'W_TO x (1 - Mff).'],
                ['W_tfo',  'Trapped Fuel & Oil',           'lbs',   'M_tfo x W_TO.'],
                ['W_PL',   'Payload Weight',               'lbs',   'N_pax x (W_pax + W_bag).'],
                ['W_crew', 'Crew Weight',                  'lbs',   '(N_pilots + N_att) x 205 lbs/person.'],
                ['Mff',    'Mission Fuel Fraction',        '--',    'Product of all 8 phase fractions.'],
                ['R',      'Design Range',                 'nm',    'Required flight distance.'],
                ['Rc',     'Cruise Range (converted)',      'stat.mi', 'Rc = R x 1.15078.'],
                ['E',      'Loiter Endurance',              'hr',    'Duration of loiter segment.'],
                ['V',      'Loiter Speed',                  'kts',   'Airspeed during loiter.'],
                ['L/D',    'Lift-to-Drag Ratio',            '--',    'Aerodynamic efficiency.'],
                ['Cp',     'Specific Fuel Consumption',     'lbs/hp/hr', 'Fuel mass flow per unit shaft power.'],
                ['eta_p',  'Propeller Efficiency',          '--',    'Ratio of thrust power to shaft power.'],
                ['A',      'Regression Intercept',           '--',   'Aircraft-class constant, Raymer Table 2.15.'],
                ['B',      'Regression Slope',               '--',   'Aircraft-class slope, Raymer Table 2.15.'],
                ['F',      'Sizing Multiplier',              'lbs',  'Scales all partial derivatives.'],
                ['C',      'Fuel Availability Factor',       '--',   '1 - (1+M_res)(1-Mff) - M_tfo.'],
                ['D',      'Fixed Weight Demand',            'lbs',  'W_PL + W_crew.'],
            ]
            story.append(build_table(nom,
                [PW*0.13, PW*0.25, PW*0.10, PW*0.52],
                val_cols=[], font_sz=7.5))
            story.append(Spacer(1, 0.4*cm))

            story.append(HRFlowable(width=PW, thickness=0.6, color=C_BORDER,
                                     spaceBefore=0, spaceAfter=3))
            story.append(Paragraph('1   MISSION INPUTS', sH1_RULE))
            t_in = build_table([
                ['Parameter', 'Value', 'Units', 'Parameter', 'Value', 'Units'],
                ['Passengers',        str(int(npax)),  'pax',         'Design Range',      str(int(R_nm)),  'nm'],
                ['Pax body weight',   str(int(wpax)),  'lbs',         'Baggage per pax',   str(int(wbag)),  'lbs'],
                ['Flight crew',       str(int(ncrew)), 'pilots',      'Cabin attendants',  str(int(natt)),  'persons'],
                ['Cruise L/D',        f'{LDc:.1f}',   '--',           'Loiter L/D',        f'{LDl:.1f}',   '--'],
                ['Cruise Cp',         f'{Cpc:.2f}',   'lbs/hp/hr',   'Loiter Cp',         f'{Cpl:.2f}',   'lbs/hp/hr'],
                ['Cruise eta_p',      f'{npc:.2f}',   '--',           'Loiter eta_p',      f'{npl:.2f}',   '--'],
                ['Loiter endurance E',f'{El:.2f}',    'hr',           'Loiter speed V',    str(int(Vl)),   'kts'],
                ['A (regression)',    f'{A_v:.4f}',   '--',           'B (regression)',    f'{B_v:.4f}',   '--'],
                ['M_tfo',             f'{Mtfo:.3f}',  '--',           'M_res',             f'{Mres:.3f}',  '--'],
            ], [PW*0.24, PW*0.10, PW*0.12, PW*0.24, PW*0.10, PW*0.10],
               val_cols=[1, 4])
            story.append(t_in)
            story.append(Spacer(1, 0.4*cm))

            story.append(HRFlowable(width=PW, thickness=0.6, color=C_BORDER,
                                     spaceBefore=0, spaceAfter=3))
            story.append(Paragraph('2   SIZING METHODOLOGY & KEY EQUATIONS', sH1_RULE))
            story.append(Paragraph(
                'This report applies the iterative weight-sizing procedure '
                'of Raymer (2018), Aircraft Design: A Conceptual Approach, Chapter 2.',
                sBODY))
            story.append(Paragraph('2.1  Breguet Cruise Range Equation  (Raymer Eq. 2.9)', sH2))
            story.append(Paragraph('W5/W4  =  exp[ -Rc / ( 375 x (eta_p / Cp) x (L/D) ) ]', sEQ))
            story.append(Paragraph('2.2  Breguet Loiter Endurance Equation  (Raymer Eq. 2.11)', sH2))
            story.append(Paragraph('W6/W5  =  exp[ -E*V / ( 375 x (eta_p / Cp) x (L/D) ) ]', sEQ))
            story.append(Paragraph('2.3  Empty Weight Regression  (Raymer Table 2.2 / 2.15)', sH2))
            story.append(Paragraph('log10(W_E)  =  A  +  B x log10(W_TO)', sEQ))
            story.append(Paragraph('2.4  Fuel Weight Build-Up', sH2))
            story.append(Paragraph('W_F_used  =  W_TO x (1 - Mff)', sEQ))
            story.append(Paragraph('W_F_total  =  W_F_used x (1 + M_res)', sEQ))
            story.append(Spacer(1, 0.4*cm))

            story.append(HRFlowable(width=PW, thickness=0.6, color=C_BORDER,
                                     spaceBefore=0, spaceAfter=3))
            story.append(Paragraph('3   MISSION PROFILE DIAGRAM', sH1_RULE))
            story.append(Paragraph(
                f'Figure 1 shows the altitude-vs-distance profile for the '
                f'{int(npax)}-passenger mission with design range {R_nm} nm.',
                sBODY))
            story.append(Spacer(1, 0.1*cm))
            story.append(make_mission_profile(width=PW, height=5.5*cm))
            story.append(Spacer(1, 0.4*cm))

            story.append(HRFlowable(width=PW, thickness=0.6, color=C_BORDER,
                                     spaceBefore=0, spaceAfter=3))
            story.append(Paragraph('4   MISSION PHASE WEIGHT FRACTIONS', sH1_RULE))
            ph_d = [['Phase', 'Wi/Wi-1', 'Type', 'Source', 'Cumulative Mff']]
            cm4  = 1.0
            for pname, (fv, ft, fs) in RR['phases'].items():
                cm4 *= fv
                ph_d.append([pname, f'{fv:.5f}', ft, fs, f'{cm4:.5f}'])
            ph_d.append(['PRODUCT  (Mff)', '--', '--', 'All 8 phases', f'{RR["Mff"]:.6f}'])
            story.append(build_table(ph_d,
                [PW*0.22, PW*0.14, PW*0.13, PW*0.13, PW*0.18],
                val_cols=[1, 4], highlight_last=True))
            story.append(Spacer(1, 0.15*cm))
            ph_labels = list(RR['phases'].keys())
            ph_fvals  = [v for v,_,_ in RR['phases'].values()]
            ph_types  = [t for _,t,_ in RR['phases'].values()]
            ph_cols   = [C_BLUE if t=='Fixed'
                         else colors.HexColor('#8B6914') for t in ph_types]
            story.append(make_bar(ph_labels, ph_fvals, ph_cols,
                                   width=PW, height=5.0*cm,
                                   title='Chart 1 — Phase Weight Fractions  (Wi / Wi-1)'))
            story.append(Spacer(1, 0.4*cm))

            story.append(HRFlowable(width=PW, thickness=0.6, color=C_BORDER,
                                     spaceBefore=0, spaceAfter=3))
            story.append(Paragraph('5   SIZING RESULTS', sH1_RULE))
            res_d = [['Quantity', 'Symbol', 'Value', 'Units', 'Expression']]
            for nm, sym, vl_r, un, ex in [
                ('Gross Takeoff Weight',     'W_TO',      f'{Wto:,.2f}',       'lbs', 'Bisection convergence solution'),
                ('Total Fuel Weight',        'W_F',       f'{WF:,.2f}',        'lbs', 'W_TO x (1 - Mff) x (1 + M_res)'),
                ('Usable Fuel Weight',       'W_F_used',  f'{RR["WFu"]:,.2f}', 'lbs', 'W_TO x (1 - Mff)'),
                ('Trapped Fuel & Oil',       'W_tfo',     f'{Wtfo_r:,.3f}',    'lbs', f'M_tfo x W_TO'),
                ('Operating Empty Weight',   'W_OE',      f'{WOE:,.2f}',       'lbs', 'W_TO - W_F - W_PL'),
                ('Empty Weight (tentative)', 'W_E',       f'{WE:,.2f}',        'lbs', 'W_OE - W_tfo - W_crew'),
                ('Empty Weight (allowable)', 'W_Ea',      f'{RR["WEa"]:,.2f}', 'lbs', '10^[(log W_TO - A) / B]'),
                ('Convergence Error',        'delta_WE',  f'{RR["diff"]:+.3f}','lbs', 'W_Ea - W_E  -->  0'),
                ('Payload Weight',           'W_PL',      f'{Wpl:,.2f}',       'lbs', f'{npax} pax x ({wpax}+{wbag}) lbs'),
                ('Crew Weight',              'W_crew',    f'{Wcrew:,.2f}',     'lbs', f'{ncrew} pilots + {natt} attendant(s) x 205 lbs'),
                ('Mission Fuel Fraction',    'Mff',       f'{RR["Mff"]:.6f}',  '--',  'Product of all 8 phase fractions'),
            ]:
                res_d.append([nm, sym, vl_r, un, ex])
            story.append(build_table(res_d,
                [PW*0.28, PW*0.12, PW*0.13, PW*0.08, PW*0.39],
                val_cols=[2]))
            story.append(Spacer(1, 0.2*cm))
            story.append(make_convergence(Wto, WE, width=PW, height=5.8*cm,
                title='Chart 2 — W_E Tentative (blue) vs W_E Allowable (gold)'))
            story.append(Spacer(1, 0.4*cm))

            story.append(HRFlowable(width=PW, thickness=0.6, color=C_BORDER,
                                     spaceBefore=0, spaceAfter=3))
            story.append(Paragraph('6   WEIGHT RATIOS — SANITY CHECK', sH1_RULE))
            rat_d = [['Ratio', 'Computed', 'Typical Range', 'Status', 'Comment']]
            for nm, vr, lo_r, hi_r, cmt in [
                ('W_PL / W_TO', Wpl/Wto, 0.10, 0.25, 'Payload fraction'),
                ('W_F  / W_TO', WF/Wto,  0.20, 0.45, 'Fuel fraction'),
                ('W_E  / W_TO', WE/Wto,  0.45, 0.65, 'Empty weight fraction'),
                ('W_PL / W_E',  Wpl/WE,  0.15, 0.40, 'Payload-to-empty ratio'),
            ]:
                ok_r = lo_r <= vr <= hi_r
                chk  = '[OK]' if ok_r else ('[HIGH]' if vr > hi_r else '[LOW]')
                rat_d.append([nm, f'{vr:.4f}', f'{lo_r:.2f} - {hi_r:.2f}', chk, cmt])
            story.append(build_table(rat_d,
                [PW*0.22, PW*0.12, PW*0.18, PW*0.10, PW*0.28],
                val_cols=[1]))

            story.append(Spacer(1, 0.2*cm))
            pie_lbl = ['W_F Fuel','W_PL Payload','W_tfo Trapped','W_crew Crew','W_E Empty']
            pie_val = [WF, Wpl, Wtfo_r, Wcrew, WE]
            pie_col = [
                colors.HexColor('#8B6914'), colors.HexColor('#1A4A8A'),
                colors.HexColor('#A05A00'), colors.HexColor('#5A1A8A'),
                colors.HexColor('#1A6B3A'),
            ]
            pie_d_draw = make_pie(pie_lbl, pie_val, pie_col,
                                   width=8*cm, height=6.5*cm,
                                   title='Weight Breakdown (% of W_TO)')
            leg_r = [['Component', 'Weight (lbs)', '% W_TO']]
            for lbl, val in zip(pie_lbl, pie_val):
                leg_r.append([lbl, f'{val:,.1f}', f'{val/Wto*100:.1f}%'])
            leg_r.append(['W_TO Total', f'{Wto:,.1f}', '100.0%'])
            leg_t = Table(leg_r, colWidths=[PW*0.24, PW*0.14, PW*0.10], splitByRow=False)
            leg_t.setStyle(TableStyle([
                ('BACKGROUND',    (0,0),  (-1,0),  C_HDR),
                ('TEXTCOLOR',     (0,0),  (-1,0),  C_HDR_TXT),
                ('FONTNAME',      (0,0),  (-1,0),  'Helvetica-Bold'),
                ('FONTSIZE',      (0,0),  (-1,-1), 7.5),
                ('LEADING',       (0,0),  (-1,-1), 10),
                ('GRID',          (0,0),  (-1,-1), 0.3, C_BORDER),
                ('BACKGROUND',    (0,-1), (-1,-1), C_LIGHT),
                ('FONTNAME',      (0,-1), (-1,-1), 'Helvetica-Bold'),
                ('TOPPADDING',    (0,0),  (-1,-1), 3),
                ('BOTTOMPADDING', (0,0),  (-1,-1), 3),
                ('LEFTPADDING',   (0,0),  (-1,-1), 5),
                ('TEXTCOLOR',     (0,1),  (-1,-1), C_BLACK),
                ('FONTNAME',      (1,1),  (-1,-1), 'Courier'),
            ]))
            combined = Table([[pie_d_draw, leg_t]],
                              colWidths=[8.2*cm, PW-8.2*cm], splitByRow=False)
            combined.setStyle(TableStyle([
                ('VALIGN',       (0,0),(-1,-1), 'TOP'),
                ('LEFTPADDING',  (0,0),(-1,-1), 0),
                ('RIGHTPADDING', (0,0),(-1,-1), 0),
                ('TOPPADDING',   (0,0),(-1,-1), 0),
            ]))
            story.append(KeepTogether(combined))
            story.append(Spacer(1, 0.4*cm))

            story.append(PageBreak())
            story.append(HRFlowable(width=PW, thickness=0.6, color=C_BORDER,
                                     spaceBefore=0, spaceAfter=3))
            story.append(Paragraph('7   SENSITIVITY ANALYSIS  (Raymer Eq. 2.44 - 2.51)', sH1_RULE))
            items_s = [
                ('Cruise SFC (Cp)',           abs(S['dCpR']), S['dCpR'], 'lbs/(lbs/hp/hr)'),
                ('Cruise prop. efficiency',   abs(S['dnpR']), S['dnpR'], 'lbs'),
                ('Cruise L/D',               abs(S['dLDR']), S['dLDR'], 'lbs'),
                ('Design range R',           abs(S['dR']),   S['dR'],   'lbs/nm'),
                ('Loiter SFC (Cp)',           abs(S['dCpE']), S['dCpE'], 'lbs/(lbs/hp/hr)'),
                ('Loiter prop. efficiency',   abs(S['dnpE']), S['dnpE'], 'lbs'),
                ('Loiter L/D',               abs(S['dLDE']), S['dLDE'], 'lbs'),
            ]
            items_s_sorted = sorted(items_s, key=lambda x: x[0], reverse=True)
            dom  = items_s_sorted[0]
            sec  = items_s_sorted[1]
            dirn = 'increases' if dom[2] > 0 else 'decreases'
            story.append(Paragraph(
                f'The sizing multiplier F = {S["F"]:,.0f} lbs propagates sensitivities. '
                f'{dom[0]} is the most influential parameter '
                f'(dW_TO/dX = {dom[2]:+,.1f} {dom[3]}). '
                f'Second most sensitive: {sec[0]} ({sec[2]:+,.1f} {sec[3]}).',
                sANAL))
            fac_d = [
                ['Factor', 'Symbol', 'Value', 'Units', 'Equation'],
                ['Fuel availability factor', 'C', f'{S["C"]:.6f}', '--', '1 - (1+M_res)(1-Mff) - M_tfo  [Eq. 2.22]'],
                ['Fixed weight demand', 'D', f'{S["D"]:,.2f}', 'lbs', 'W_PL + W_crew  [Eq. 2.23]'],
                ['Sizing multiplier', 'F', f'{S["F"]:,.2f}', 'lbs', '-B x W_TO^2 x (1+M_res) x Mff / denom  [Eq. 2.44]'],
            ]
            story.append(build_table(fac_d,
                [PW*0.28, PW*0.08, PW*0.14, PW*0.08, PW*0.42],
                val_cols=[2]))
            story.append(Spacer(1, 0.2*cm))
            sen_d = [['Partial Derivative', 'Value', 'Units', 'Eq.', 'Physical Interpretation']]
            for partial, val, unit, eq, interp in [
                ('dW_TO / dCp  (cruise)',    S['dCpR'], 'lbs/(lbs/hp/hr)', 'Eq. 2.49', '+ve: higher SFC increases fuel, raises W_TO'),
                ('dW_TO / deta_p  (cruise)', S['dnpR'], 'lbs', 'Eq. 2.50', '-ve: better prop. efficiency reduces fuel needed'),
                ('dW_TO / d(L/D)  (cruise)', S['dLDR'], 'lbs', 'Eq. 2.51', '-ve: higher aero efficiency reduces fuel'),
                ('dW_TO / dR',               S['dR'],   'lbs/nm', 'Eq. 2.45', '+ve: longer range requires more fuel'),
                ('dW_TO / dCp  (loiter)',    S['dCpE'], 'lbs/(lbs/hp/hr)', '--', '+ve: higher loiter SFC raises reserve fuel'),
                ('dW_TO / deta_p  (loiter)', S['dnpE'], 'lbs', '--', '-ve: better prop. eff. reduces reserve fuel'),
                ('dW_TO / d(L/D)  (loiter)', S['dLDE'], 'lbs', '--', '-ve: higher loiter L/D reduces reserve fuel'),
            ]:
                sen_d.append([partial, f'{val:+,.2f}', unit, eq, interp])
            sen_t = Table(sen_d,
                          colWidths=[PW*0.28, PW*0.12, PW*0.18, PW*0.08, PW*0.34],
                          repeatRows=1, splitByRow=False)
            sen_style = [
                ('BACKGROUND', (0,0), (-1,0), C_HDR),
                ('TEXTCOLOR',  (0,0), (-1,0), C_HDR_TXT),
                ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
                ('FONTSIZE',   (0,0), (-1,-1), 7.5),
                ('LEADING',    (0,0), (-1,-1), 11),
                ('GRID',       (0,0), (-1,-1), 0.4, C_BORDER),
                ('LINEBELOW',  (0,0), (-1,0),  1.5, C_GOLD),
                ('VALIGN',     (0,0), (-1,-1), 'MIDDLE'),
                ('LEFTPADDING',(0,0), (-1,-1), 6),
                ('RIGHTPADDING',(0,0),(-1,-1), 6),
                ('TOPPADDING', (0,0), (-1,-1), 3),
                ('BOTTOMPADDING',(0,0),(-1,-1),3),
                ('TEXTCOLOR',  (0,1), (-1,-1), C_BLACK),
                ('FONTNAME',   (0,1), (0,-1),  'Helvetica-Bold'),
                ('TEXTCOLOR',  (0,1), (0,-1),  C_DARK),
            ]
            for ri in range(1, len(sen_d)):
                val_num = [S['dCpR'],S['dnpR'],S['dLDR'],S['dR'],
                           S['dCpE'],S['dnpE'],S['dLDE']][ri-1]
                col = C_RED if val_num > 0 else C_GREEN
                bg  = C_NEAR_W if ri % 2 == 1 else C_WHITE
                sen_style += [
                    ('BACKGROUND', (0,ri), (-1,ri), bg),
                    ('TEXTCOLOR',  (1,ri), (1,ri),  col),
                    ('FONTNAME',   (1,ri), (1,ri),  'Courier-Bold'),
                ]
            sen_t.setStyle(TableStyle(sen_style))
            story.append(KeepTogether(sen_t))
            story.append(Spacer(1, 0.25*cm))
            story.append(make_tornado(S, width=PW, height=6.0*cm,
                title='Chart 4 — dW_TO/dX  |  Sorted by Absolute Magnitude'))

            trd_d = [['Delta Range (nm)', 'Delta W_TO (lbs)', 'New W_TO (lbs)', 'Trend']]
            for dr in [-300, -200, -100, +100, +200, +300]:
                dw = S['dR'] * dr
                nw = Wto + dw
                trd_d.append([f'{dr:+d} nm', f'{dw:+,.1f} lbs',
                               f'{nw:,.1f} lbs', 'LIGHTER' if dw < 0 else 'HEAVIER'])
            story.append(Spacer(1, 0.2*cm))
            story.append(build_table(trd_d,
                [PW*0.22, PW*0.24, PW*0.22, PW*0.16],
                val_cols=[1, 2]))

            story.append(Spacer(1, 0.5*cm))
            story.append(HRFlowable(width=PW, thickness=0.5, color=C_BORDER,
                                     spaceBefore=3, spaceAfter=4))
            story.append(Paragraph(
                f'AeroSizer Pro  —  Raymer (2018): Aircraft Design, A Conceptual Approach  —  '
                f'W_TO = {Wto:,.1f} lbs  |  Mff = {RR["Mff"]:.6f}  |  '
                f'{"CONVERGED" if conv else "NOT CONVERGED"}',
                sFOOT))

            doc.build(story)
            buf.seek(0)
            return buf.read()

        st.markdown(f"""
        <div class="card card-gold">
          <div class="card-title">PDF Report Contents — A4 Print-Ready</div>
          <div style="font-size:.77rem;color:var(--text);line-height:2.0">
            <b style="color:var(--gold2)">Sec 0</b> · Nomenclature & symbol reference<br>
            <b style="color:var(--gold2)">Sec 1</b> · Mission inputs table<br>
            <b style="color:var(--gold2)">Sec 2</b> · Methodology + equations (Eq. 2.9, 2.11, regression)<br>
            <b style="color:var(--gold2)">Sec 3</b> · Mission profile diagram (Altitude vs. Distance)<br>
            <b style="color:var(--gold2)">Sec 4</b> · Phase fractions table + Chart 1<br>
            <b style="color:var(--gold2)">Sec 5</b> · Sizing results + Chart 2 (convergence)<br>
            <b style="color:var(--gold2)">Sec 6</b> · Weight ratios sanity check + Chart 3 (pie)<br>
            <b style="color:var(--gold2)">Sec 7</b> · Sensitivity analysis + Chart 4 (Tornado) + range trade
          </div>
          <div style="margin-top:.65rem;font-size:.67rem;color:#6e7681">
            White background · Black text · Gray borders · All units labelled ·
            {'✓ Ready to export' if conv else '⚠ Check convergence before export'}
          </div>
        </div>""", unsafe_allow_html=True)

        st.download_button(
            "⬇  Generate & Download PDF (A4)",
            make_pdf(),
            "aerosizer_report.pdf",
            "application/pdf",
            use_container_width=True)
