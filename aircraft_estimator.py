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
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Circle, Polygon
from reportlab.graphics.charts.barcharts import HorizontalBarChart, VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics import renderPDF

# ─── PAGE CONFIG ───
st.set_page_config(page_title="AeroSizer Pro", page_icon="✈", layout="wide",
                   initial_sidebar_state="expanded")

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
[data-testid="stDataFrame"]{border:1px solid rgba(200,168,108,.22)!important;border-radius:10px!important;overflow:hidden!important;background:var(--sur)!important;}
[data-testid="stDataFrame"]>div{background:var(--sur)!important;}
[data-testid="stDataFrame"] *{background-color:var(--sur)!important;color:var(--text)!important;}
[data-testid="stDataFrame"] canvas{filter:invert(0)!important;}
[data-testid="stDataFrame"] [style*="background"]{background:#0c0f16!important;}
[data-testid="stDataFrame"] [style*="color: rgb(49"]{color:#b0bcce!important;}
[data-testid="stDataFrame"] [style*="color: white"]{color:#b0bcce!important;}
[data-testid="stDataFrame"] ::-webkit-scrollbar{height:3px!important;width:3px!important;}
[data-testid="stDataFrame"] ::-webkit-scrollbar-thumb{background:rgba(200,168,108,.3)!important;}

/* ── CUSTOM HTML TABLE ── */
.dark-table{width:100%;border-collapse:collapse;font-family:'JetBrains Mono',monospace;font-size:.76rem;border:1px solid rgba(200,168,108,.22);border-radius:10px;overflow:hidden;}
.dark-table thead tr{background:linear-gradient(135deg,#0d1520,#111e2e);}
.dark-table thead th{padding:.52rem .85rem;text-align:left;font-size:.6rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--gold);border-bottom:1.5px solid rgba(200,168,108,.3);white-space:nowrap;}
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
.dark-table-wrap{border:1px solid rgba(200,168,108,.18);border-radius:10px;overflow:hidden;margin-bottom:.7rem;}

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
    Wpl   = p['npax'] * (p['wpax'] + p['wbag'])
    Wcrew = (p['ncrew'] + p['natt']) * 205
    Wtfo  = p['Wto'] * p['Mtfo']

    Rc = p['R']  * 1.15078
    Vm = p['Vl'] * 1.15078

    W5 = 1.0 / math.exp(Rc / (375.0 * (p['npc'] / p['Cpc']) * p['LDc']))
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
        st.markdown("""<div class="ph-hdr"><span>Phase</span><span>Wi/Wi-1</span><span>Type</span><span>Source</span><span>Cumulative Mff</span></div>""", unsafe_allow_html=True)
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
          <div class="eq-box">W5/W4 = 1 / exp[ Rc / (375·eta_p/Cp·L/D) ]</div>
          <div class="eq-label" style="margin-top:.55rem">Loiter fraction (Eq. 2.11) — Breguet</div>
          <div class="eq-box">W6/W5 = 1 / exp[ E·V / (375·eta_p/Cp·L/D) ]</div>
          <div class="eq-label" style="margin-top:.55rem">Regression line (Table 2.2 / 2.15)</div>
          <div class="eq-box">log10(W_E) = A + B · log10(W_TO)</div>
          <div style="font-size:.65rem;color:#6e7681;margin-top:.45rem;line-height:1.72">
            R in <b style="color:#8b949e">statute miles</b> &nbsp;·&nbsp;
            Cp in <b style="color:#8b949e">lbs/hp/hr</b><br>
            V in <b style="color:#8b949e">mph</b> &nbsp;·&nbsp;
            E in <b style="color:#8b949e">hours</b> &nbsp;·&nbsp;
            eta_p dimensionless
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
        tbl_html = '<div class="dark-table-wrap"><table class="dark-table"><thead><tr><th>Symbol</th><th>Value</th><th>Unit</th></tr></thead><tbody>'
        for sym, val, unit in sum_rows:
            tbl_html += f'<tr><td>{sym}</td><td class="val">{val}</td><td class="unit">{unit}</td></tr>'
        tbl_html += '</tbody></table></div>'
        st.markdown(tbl_html, unsafe_allow_html=True)

        ratio_html = '<div class="dark-table-wrap"><table class="dark-table"><thead><tr><th>Ratio</th><th>Value</th><th>Typical</th><th>✓</th></tr></thead><tbody>'
        for nm, vr, lo_r, hi_r in [
            ('W_PL / W_TO', Wpl/Wto, 0.10, 0.25),
            ('W_F  / W_TO', WF/Wto,  0.20, 0.45),
            ('W_E  / W_TO', WE/Wto,  0.45, 0.65),
            ('W_PL / W_E',  Wpl/WE,  0.15, 0.40)]:
            ok_r = lo_r <= vr <= hi_r
            chk  = '✓' if ok_r else ('▲' if vr > hi_r else '▼')
            chk_cls = 'check-ok' if ok_r else 'check-warn'
            ratio_html += (f'<tr><td>{nm}</td><td class="val">{vr:.4f}</td>'
                           f'<td class="unit">{lo_r:.2f}–{hi_r:.2f}</td>'
                           f'<td class="{chk_cls}">{chk}</td></tr>')
        ratio_html += '</tbody></table></div>'
        st.markdown(ratio_html, unsafe_allow_html=True)

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
            ('dW_TO/dCp (cruise)',  S['dCpR'], 'lbs per lbs/hp/hr', 'Eq 2.49'),
            ('dW_TO/dn_p (cruise)', S['dnpR'], 'lbs',               'Eq 2.50'),
            ('dW_TO/d(L/D) cruise', S['dLDR'], 'lbs',               'Eq 2.51'),
            ('dW_TO/dR',           S['dR'],   'lbs/nm',            'Eq 2.45')]:
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
            ('dW_TO/dCp (loiter)',  S['dCpE'], 'lbs per lbs/hp/hr'),
            ('dW_TO/dn_p (loiter)', S['dnpE'], 'lbs'),
            ('dW_TO/d(L/D) loiter', S['dLDE'], 'lbs')]:
            vc = 'sens-neg' if val < 0 else 'sens-pos'
            st.markdown(
                f'<div class="sens-row" style="grid-template-columns:210px 110px 1fr">'
                f'<span class="sens-partial">{partial}</span>'
                f'<span class="{vc}">{val:+,.1f}</span>'
                f'<span class="sens-unit">{unit}</span></div>',
                unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with s2:
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
          <div class="card-title">Range Trade · dW_TO/dR = {S['dR']:+.2f} lbs/nm</div>""",
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
    DARK3 = dict(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(11,15,22,.7)',
                font=dict(family='JetBrains Mono', color='#8b949e', size=9),
                margin=dict(l=8, r=8, t=44, b=8))
    AX3      = dict(gridcolor='rgba(255,255,255,.04)', linecolor='rgba(255,255,255,.09)', tickfont=dict(size=9))
    AX3_SM8  = dict(gridcolor='rgba(255,255,255,.04)', linecolor='rgba(255,255,255,.09)', tickfont=dict(size=8))
    TITLE3   = lambda t: dict(text=t, font=dict(color='#c8a86c', size=12, family='DM Serif Display'))

    st.markdown('<div class="sec-div">Chart 1 — Mission Phase Weight Fractions: How fuel is consumed each phase</div>', unsafe_allow_html=True)
    phases_l = list(RR['phases'].keys())
    fvals    = [v for v, _, _ in RR['phases'].values()]
    ftypes   = [t for _, t, _ in RR['phases'].values()]
    cum_p    = [1.0]
    for fv in fvals: cum_p.append(cum_p[-1] * fv)
    bar_col = ['#6a9eea' if t == 'Fixed' else '#c8a86c' for t in ftypes]

    fig1 = make_subplots(rows=1, cols=2,
        subplot_titles=["Wi/Wi-1 per phase (closer to 1.0 = less fuel burned)",
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
        f'Blue bars = fixed fractions (Table 2.1) &nbsp;·&nbsp; Gold bars = Breguet equations · '
        f'Cruise burns the most fuel (fraction = {[v for v,t,_ in RR["phases"].values() if t=="Breguet"][0]:.4f})</div>',
        unsafe_allow_html=True)

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
    fig2.add_annotation(x=Wto, y=WE, text=f'Solution\nW_TO={Wto:,.0f} lbs',
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
        sp = [
            ('dW/dCp cruise',  S['dCpR']),
            ('dW/dn_p cruise', S['dnpR']),
            ('dW/d(L/D) cr.',  S['dLDR']),
            ('dW/dR',         S['dR']),
            ('dW/dCp loiter', S['dCpE']),
            ('dW/dn_p loiter',S['dnpE']),
            ('dW/d(L/D) lt.', S['dLDE']),
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
            yaxis=dict(**AX3_SM8))
        st.plotly_chart(fig4, use_container_width=True)

# ───────────────────────────────────────────────────────
# TAB 4 — Export
# ───────────────────────────────────────────────────────
with tab4:
    e1, e2 = st.columns(2, gap="medium")

    with e1:
        st.markdown('<div class="sec-div">Full Results — CSV</div>', unsafe_allow_html=True)
        exp_rows = [
            ('W_TO',       round(Wto,2),           'lbs'),
            ('Mff',        round(RR['Mff'],6),      '—'),
            ('W_F',        round(WF,2),             'lbs'),
            ('W_F_usable', round(RR['WFu'],2),      'lbs'),
            ('W_tfo',      round(Wtfo_r,3),         'lbs'),
            ('W_OE',       round(WOE,2),            'lbs'),
            ('W_E_tent',   round(WE,2),             'lbs'),
            ('W_E_allow',  round(RR['WEa'],2),      'lbs'),
            ('delta_WE',   round(RR['diff'],3),     'lbs'),
            ('W_PL',       round(Wpl,2),            'lbs'),
            ('W_crew',     round(Wcrew,2),          'lbs'),
            ('Rc_sm',      round(RR['Rc'],3),       's.mi'),
            ('Vm_mph',     round(RR['Vm'],3),       'mph'),
            ('F',          round(S['F'],2),         '—'),
            ('C',          round(S['C'],6),         '—'),
            ('D',          round(S['D'],2),         'lbs'),
        ]
        exp_html = '<div class="dark-table-wrap"><table class="dark-table"><thead><tr><th>Parameter</th><th>Value</th><th>Units</th></tr></thead><tbody>'
        for param, val, unit in exp_rows:
            exp_html += f'<tr><td>{param}</td><td class="val">{val}</td><td class="unit">{unit}</td></tr>'
        exp_html += '</tbody></table></div>'
        st.markdown(exp_html, unsafe_allow_html=True)

        df_exp = pd.DataFrame({
            'Parameter': [r[0] for r in exp_rows],
            'Value':     [r[1] for r in exp_rows],
            'Units':     [r[2] for r in exp_rows]})
        b = io.StringIO(); df_exp.to_csv(b, index=False)
        st.download_button("Download CSV", b.getvalue(),
                           "aerosizer_results.csv", "text/csv",
                           use_container_width=True)

    with e2:
        st.markdown('<div class="sec-div">PDF Report — A4</div>', unsafe_allow_html=True)

        # ════════════════════════════════════════════════════
        # IMPROVED make_pdf() — enhanced colors, typography,
        # symbol reference table, and chart visualizations
        # ════════════════════════════════════════════════════
        def make_pdf():
            buf = io.BytesIO()
            doc = SimpleDocTemplate(buf, pagesize=A4,
                leftMargin=1.8*cm, rightMargin=1.8*cm,
                topMargin=2.0*cm,  bottomMargin=2.0*cm)
            PW = 17.4*cm  # usable width

            # ── Refined color palette (eye-friendly, high contrast) ──
            C_BG      = colors.HexColor('#0D1B2A')   # deep navy background
            C_BG2     = colors.HexColor('#0F2236')   # slightly lighter navy
            C_PANEL   = colors.HexColor('#132639')   # panel background
            C_PANEL2  = colors.HexColor('#1A3048')   # alt row
            C_GOLD    = colors.HexColor('#D4AA70')   # warm gold — primary accent
            C_GOLD2   = colors.HexColor('#EDD192')   # light gold — headings
            C_BLUE    = colors.HexColor('#4E85C5')   # steel blue
            C_BLUE2   = colors.HexColor('#7AADEA')   # sky blue — values
            C_GREEN   = colors.HexColor('#4EC94E')   # emerald green
            C_RED     = colors.HexColor('#F06464')   # soft red
            C_AMBER   = colors.HexColor('#E8B84B')   # amber
            C_PURPLE  = colors.HexColor('#A57FD4')   # purple
            C_LGRAY   = colors.HexColor('#A0AEBB')   # light gray — body text
            C_MGRAY   = colors.HexColor('#6E8494')   # medium gray
            C_DGRAY   = colors.HexColor('#3A5068')   # dark gray — borders
            C_WHITE   = colors.HexColor('#EEF2F7')   # near-white
            C_ROW1    = colors.HexColor('#0D1E30')   # odd row
            C_ROW2    = colors.HexColor('#122438')   # even row
            C_HDR     = colors.HexColor('#091828')   # table header bg
            C_BORDER  = colors.HexColor('#1E3A52')   # table border

            sty = getSampleStyleSheet()

            def ps(nm, **kw):
                return ParagraphStyle(nm, parent=sty['Normal'], **kw)

            # Typography — larger, clearer fonts
            sCOVER  = ps('CV',  fontSize=20, fontName='Helvetica-Bold',
                          textColor=C_GOLD2, alignment=TA_LEFT, leading=24)
            sSUBHD  = ps('SH',  fontSize=9,  fontName='Helvetica',
                          textColor=C_LGRAY, alignment=TA_LEFT, leading=13)
            sH1     = ps('H1',  fontSize=11, fontName='Helvetica-Bold',
                          textColor=C_GOLD, spaceBefore=14, spaceAfter=5, leading=14)
            sH2     = ps('H2',  fontSize=9,  fontName='Helvetica-Bold',
                          textColor=C_BLUE2, spaceBefore=7,  spaceAfter=3, leading=12)
            sH3     = ps('H3',  fontSize=8,  fontName='Helvetica-Bold',
                          textColor=C_GOLD, spaceBefore=5,  spaceAfter=2, leading=11)
            sBODY   = ps('BD',  fontSize=8,  fontName='Helvetica',
                          textColor=C_LGRAY, leading=12, spaceAfter=2)
            sNOTE   = ps('NT',  fontSize=7,  fontName='Helvetica',
                          textColor=C_MGRAY, leading=10, spaceAfter=2)
            sEQ     = ps('EQ',  fontSize=8.5,fontName='Courier-Bold',
                          textColor=C_BLUE2, leading=12,
                          backColor=colors.HexColor('#091828'),
                          leftIndent=10, rightIndent=10,
                          spaceBefore=2, spaceAfter=5,
                          borderPad=4)
            sEQLBL  = ps('EL',  fontSize=7.5,fontName='Helvetica',
                          textColor=C_GOLD, leading=10, spaceAfter=1)
            sFOOT   = ps('FT',  fontSize=6.5,fontName='Helvetica',
                          textColor=C_MGRAY, alignment=TA_CENTER)
            sCENTER = ps('CT',  fontSize=8,  fontName='Helvetica',
                          textColor=C_LGRAY, alignment=TA_CENTER, leading=11)
            sVAL    = ps('VL',  fontSize=8,  fontName='Courier-Bold',
                          textColor=C_WHITE, leading=11)
            sVAL_G  = ps('VG',  fontSize=8,  fontName='Courier-Bold',
                          textColor=C_GOLD2, leading=11)
            sVAL_B  = ps('VB',  fontSize=8,  fontName='Courier-Bold',
                          textColor=C_BLUE2, leading=11)
            sVAL_GR = ps('VGR', fontSize=8,  fontName='Courier-Bold',
                          textColor=C_GREEN, leading=11)
            sVAL_R  = ps('VR',  fontSize=8,  fontName='Courier-Bold',
                          textColor=C_RED,   leading=11)

            # ── Table builder helper ──
            def dark_table(data, col_widths, hdr_bg=None, val_cols=None,
                           gold_col0=True, alt_rows=True, font_sz=8):
                hdr_bg = hdr_bg or C_HDR
                val_cols = val_cols or []
                t = Table(data, colWidths=col_widths, repeatRows=1)
                row_bgs = [C_ROW1, C_ROW2] if alt_rows else [C_PANEL]
                style = [
                    # Header
                    ('BACKGROUND',    (0,0), (-1,0),  hdr_bg),
                    ('TEXTCOLOR',     (0,0), (-1,0),  C_GOLD),
                    ('FONTNAME',      (0,0), (-1,0),  'Helvetica-Bold'),
                    ('FONTSIZE',      (0,0), (-1,0),  font_sz - 0.5),
                    ('LEADING',       (0,0), (-1,0),  font_sz + 3),
                    ('LETTERSPACE',   (0,0), (-1,0),  0.5),
                    # Body
                    ('FONTNAME',      (0,1), (-1,-1), 'Courier'),
                    ('FONTSIZE',      (0,1), (-1,-1), font_sz),
                    ('LEADING',       (0,1), (-1,-1), font_sz + 3),
                    ('TEXTCOLOR',     (0,1), (-1,-1), C_LGRAY),
                    # Alternating rows
                    ('ROWBACKGROUNDS', (0,1), (-1,-1), row_bgs),
                    # Grid
                    ('GRID',          (0,0), (-1,-1), 0.25, C_BORDER),
                    ('LINEBELOW',     (0,0), (-1,0),  1.5,  C_GOLD),
                    ('LINEAFTER',     (0,0), (-1,-1), 0.25, C_BORDER),
                    # Padding
                    ('LEFTPADDING',   (0,0), (-1,-1), 7),
                    ('RIGHTPADDING',  (0,0), (-1,-1), 7),
                    ('TOPPADDING',    (0,0), (-1,-1), 4),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                    ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
                ]
                if gold_col0:
                    style += [
                        ('TEXTCOLOR',  (0,1), (0,-1), C_GOLD2),
                        ('FONTNAME',   (0,1), (0,-1), 'Helvetica-Bold'),
                    ]
                for vc in val_cols:
                    style += [
                        ('TEXTCOLOR',  (vc,1), (vc,-1), C_WHITE),
                        ('FONTNAME',   (vc,1), (vc,-1), 'Courier-Bold'),
                    ]
                t.setStyle(TableStyle(style))
                return t

            # ── Inline bar chart using ReportLab Drawing ──
            def make_bar_chart_drawing(labels, values, colors_list,
                                       width=PW, height=5.5*cm,
                                       title='', y_label=''):
                d = Drawing(width, height)
                # Background
                d.add(Rect(0, 0, width, height,
                           fillColor=colors.HexColor('#091828'),
                           strokeColor=C_BORDER, strokeWidth=0.5))
                # Title
                if title:
                    d.add(String(width/2, height - 14,
                                 title, textAnchor='middle',
                                 fontSize=9, fontName='Helvetica-Bold',
                                 fillColor=C_GOLD))
                margin_l, margin_r = 20, 15
                margin_b, margin_t = 30, 25
                chart_w = width - margin_l - margin_r
                chart_h = height - margin_b - margin_t
                n = len(values)
                bar_w = chart_w / n * 0.6
                gap   = chart_w / n
                max_v = max(abs(v) for v in values) if values else 1
                # Grid lines
                for gi in range(5):
                    gy = margin_b + chart_h * gi / 4
                    gv = max_v * gi / 4
                    d.add(Line(margin_l, gy, margin_l + chart_w, gy,
                               strokeColor=C_BORDER, strokeWidth=0.3))
                    d.add(String(margin_l - 3, gy - 3,
                                 f'{gv:,.0f}', textAnchor='end',
                                 fontSize=6, fontName='Helvetica',
                                 fillColor=C_MGRAY))
                # Bars
                for i, (lbl, val, col) in enumerate(zip(labels, values, colors_list)):
                    bx = margin_l + i * gap + gap/2 - bar_w/2
                    bh = chart_h * abs(val) / max_v if max_v > 0 else 0
                    d.add(Rect(bx, margin_b, bar_w, bh,
                               fillColor=col, strokeWidth=0))
                    d.add(String(bx + bar_w/2, margin_b + bh + 2,
                                 f'{val:.4f}', textAnchor='middle',
                                 fontSize=6, fontName='Courier',
                                 fillColor=C_LGRAY))
                    # X label (rotated not possible, so abbreviate)
                    short_lbl = lbl[:8]
                    d.add(String(bx + bar_w/2, margin_b - 12,
                                 short_lbl, textAnchor='middle',
                                 fontSize=6, fontName='Helvetica',
                                 fillColor=C_MGRAY))
                return d

            def make_pie_drawing(labels, values, colors_list,
                                  width=8*cm, height=7*cm, title=''):
                """Simple pie chart using ReportLab graphics."""
                d = Drawing(width, height)
                d.add(Rect(0, 0, width, height,
                           fillColor=colors.HexColor('#091828'),
                           strokeColor=C_BORDER, strokeWidth=0.5))
                if title:
                    d.add(String(width/2, height - 14, title,
                                 textAnchor='middle', fontSize=9,
                                 fontName='Helvetica-Bold', fillColor=C_GOLD))
                # Draw pie manually
                cx, cy = width/2 - 10, height/2 - 5
                r = min(width, height) * 0.28
                total = sum(values)
                start = 90  # start at top
                for i, (lbl, val, col) in enumerate(zip(labels, values, colors_list)):
                    sweep = 360 * val / total
                    # Draw arc segment approximation as wedge
                    import math as _math
                    steps = max(8, int(sweep / 5))
                    pts = [cx, cy]
                    for s in range(steps + 1):
                        ang = _math.radians(start + sweep * s / steps)
                        pts.extend([cx + r * _math.cos(ang),
                                    cy + r * _math.sin(ang)])
                    d.add(Polygon(pts, fillColor=col,
                                  strokeColor=colors.HexColor('#091828'),
                                  strokeWidth=1.0))
                    # Label line
                    mid_ang = _math.radians(start + sweep / 2)
                    lx = cx + (r + 12) * _math.cos(mid_ang)
                    ly = cy + (r + 12) * _math.sin(mid_ang)
                    pct = val / total * 100
                    short = lbl.split()[0]
                    d.add(String(lx, ly - 3, f'{short} {pct:.1f}%',
                                 textAnchor='middle', fontSize=5.5,
                                 fontName='Helvetica', fillColor=C_LGRAY))
                    start += sweep
                # Center text
                d.add(String(cx, cy - 5, f'{total:,.0f}',
                             textAnchor='middle', fontSize=8,
                             fontName='Courier-Bold', fillColor=C_GOLD2))
                d.add(String(cx, cy - 14, 'lbs W_TO',
                             textAnchor='middle', fontSize=6,
                             fontName='Helvetica', fillColor=C_MGRAY))
                return d

            def make_convergence_drawing(Wto, P, WE_sol, width=PW, height=5.5*cm, title=''):
                """Line chart showing W_E_tent vs W_E_allow convergence."""
                d = Drawing(width, height)
                d.add(Rect(0, 0, width, height,
                           fillColor=colors.HexColor('#091828'),
                           strokeColor=C_BORDER, strokeWidth=0.5))
                if title:
                    d.add(String(width/2, height - 14, title,
                                 textAnchor='middle', fontSize=9,
                                 fontName='Helvetica-Bold', fillColor=C_GOLD))
                margin_l, margin_r = 55, 15
                margin_b, margin_t = 22, 22
                cw = width - margin_l - margin_r
                ch = height - margin_b - margin_t

                pts_tent = []; pts_allow = []
                w_vals = [Wto * (0.55 + 0.95 * i / 39) for i in range(40)]
                for w in w_vals:
                    try:
                        rr2 = compute_mission({**P, 'Wto': float(w)})
                        pts_tent.append((w, rr2['WE']))
                        pts_allow.append((w, rr2['WEa']))
                    except Exception:
                        pass

                if not pts_tent:
                    return d

                all_y = [y for _, y in pts_tent + pts_allow]
                min_w = w_vals[0]; max_w = w_vals[-1]
                min_y = min(all_y); max_y = max(all_y)
                rng_w = max_w - min_w or 1
                rng_y = max_y - min_y or 1

                def tx(w): return margin_l + cw * (w - min_w) / rng_w
                def ty(y): return margin_b + ch * (y - min_y) / rng_y

                # Grid
                for gi in range(5):
                    gy = margin_b + ch * gi / 4
                    gv = min_y + rng_y * gi / 4
                    d.add(Line(margin_l, gy, margin_l + cw, gy,
                               strokeColor=C_BORDER, strokeWidth=0.3))
                    d.add(String(margin_l - 3, gy - 3,
                                 f'{gv:,.0f}', textAnchor='end',
                                 fontSize=5.5, fontName='Courier',
                                 fillColor=C_MGRAY))

                # Lines — W_E tentative (blue)
                for i in range(len(pts_tent) - 1):
                    d.add(Line(tx(pts_tent[i][0]), ty(pts_tent[i][1]),
                               tx(pts_tent[i+1][0]), ty(pts_tent[i+1][1]),
                               strokeColor=C_BLUE2, strokeWidth=1.5))

                # Lines — W_E allowable (gold)
                for i in range(len(pts_allow) - 1):
                    d.add(Line(tx(pts_allow[i][0]), ty(pts_allow[i][1]),
                               tx(pts_allow[i+1][0]), ty(pts_allow[i+1][1]),
                               strokeColor=C_GOLD, strokeWidth=1.5))

                # Solution point
                sx = tx(Wto); sy = ty(WE_sol)
                d.add(Circle(sx, sy, 4, fillColor=C_GREEN, strokeWidth=0))
                d.add(Line(sx, margin_b, sx, sy,
                           strokeColor=C_GREEN, strokeWidth=0.8,
                           strokeDashArray=[3, 2]))
                d.add(String(sx + 5, sy + 2, f'W_TO={Wto:,.0f}',
                             fontSize=6, fontName='Courier-Bold',
                             fillColor=C_GREEN))

                # Legend
                d.add(Line(margin_l, margin_b + ch + 8, margin_l + 15, margin_b + ch + 8,
                           strokeColor=C_BLUE2, strokeWidth=1.5))
                d.add(String(margin_l + 17, margin_b + ch + 5, 'W_E Tentative',
                             fontSize=6, fontName='Helvetica', fillColor=C_BLUE2))
                d.add(Line(margin_l + 80, margin_b + ch + 8, margin_l + 95, margin_b + ch + 8,
                           strokeColor=C_GOLD, strokeWidth=1.5))
                d.add(String(margin_l + 97, margin_b + ch + 5, 'W_E Allowable',
                             fontSize=6, fontName='Helvetica', fillColor=C_GOLD))
                return d

            def make_tornado_drawing(S, width=PW, height=6*cm, title=''):
                """Horizontal bar chart for sensitivity tornado."""
                d = Drawing(width, height)
                d.add(Rect(0, 0, width, height,
                           fillColor=colors.HexColor('#091828'),
                           strokeColor=C_BORDER, strokeWidth=0.5))
                if title:
                    d.add(String(width/2, height - 14, title,
                                 textAnchor='middle', fontSize=9,
                                 fontName='Helvetica-Bold', fillColor=C_GOLD))
                items = [
                    ('dW/dCp cruise',  S['dCpR']),
                    ('dW/dn_p cruise', S['dnpR']),
                    ('dW/d(L/D) cr.', S['dLDR']),
                    ('dW/dR',         S['dR']),
                    ('dW/dCp loiter', S['dCpE']),
                    ('dW/dn_p loiter',S['dnpE']),
                    ('dW/d(L/D) lt.', S['dLDE']),
                ]
                items_s = sorted(items, key=lambda x: abs(x[1]), reverse=True)
                max_abs = max(abs(v) for _, v in items_s) or 1

                margin_l, margin_r = 80, 45
                margin_b, margin_t = 15, 22
                cw = width - margin_l - margin_r
                ch = height - margin_b - margin_t
                n = len(items_s)
                bar_h = ch / n * 0.55
                gap = ch / n

                for i, (lbl, val) in enumerate(items_s):
                    bar_y = margin_b + ch - (i + 1) * gap + gap/2 - bar_h/2
                    bw = cw/2 * abs(val) / max_abs
                    cx_line = margin_l + cw/2
                    col = C_RED if val > 0 else C_GREEN
                    if val > 0:
                        d.add(Rect(cx_line, bar_y, bw, bar_h,
                                   fillColor=col, strokeWidth=0))
                        d.add(String(cx_line + bw + 3, bar_y + bar_h/2 - 3,
                                     f'{val:+,.1f}', fontSize=6,
                                     fontName='Courier', fillColor=col))
                    else:
                        d.add(Rect(cx_line - bw, bar_y, bw, bar_h,
                                   fillColor=col, strokeWidth=0))
                        d.add(String(cx_line - bw - 3, bar_y + bar_h/2 - 3,
                                     f'{val:+,.1f}', fontSize=6,
                                     textAnchor='end', fontName='Courier',
                                     fillColor=col))
                    d.add(String(margin_l - 3, bar_y + bar_h/2 - 3,
                                 lbl, textAnchor='end', fontSize=6,
                                 fontName='Helvetica', fillColor=C_LGRAY))

                # Center line
                cx_line = margin_l + cw/2
                d.add(Line(cx_line, margin_b, cx_line, margin_b + ch,
                           strokeColor=C_MGRAY, strokeWidth=0.5))
                d.add(String(cx_line, margin_b - 10, '0',
                             textAnchor='middle', fontSize=6,
                             fontName='Helvetica', fillColor=C_MGRAY))
                return d

            # ════════════════════════════════════════════════════
            # BUILD STORY
            # ════════════════════════════════════════════════════
            story = []

            # ── Cover block ──────────────────────────────────────
            cover_data = [[
                Paragraph('<font color="#D4AA70"><b>AEROSIZER PRO</b></font>',
                    ps('HDR', fontSize=20, fontName='Helvetica-Bold',
                       textColor=C_GOLD2, leading=24)),
                Paragraph(
                    f'<font color="#6E8494">Raymer (2018) Chapter 2</font><br/>'
                    f'<font color="#A0AEBB">Propeller Aircraft Conceptual Weight Sizing</font>',
                    ps('SUB', fontSize=8, textColor=C_LGRAY, leading=12, alignment=TA_RIGHT))
            ]]
            cover_tbl = Table(cover_data, colWidths=[PW*0.55, PW*0.45])
            cover_tbl.setStyle(TableStyle([
                ('BACKGROUND',    (0,0), (-1,-1), C_BG),
                ('TOPPADDING',    (0,0), (-1,-1), 12),
                ('BOTTOMPADDING', (0,0), (-1,-1), 12),
                ('LEFTPADDING',   (0,0), (-1,-1), 12),
                ('RIGHTPADDING',  (0,0), (-1,-1), 12),
                ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
            ]))
            story.append(cover_tbl)
            story.append(HRFlowable(width=PW, thickness=2.5, color=C_GOLD,
                                     spaceBefore=0, spaceAfter=5))

            # Convergence status banner
            sc = C_GREEN if conv else C_RED
            sc_hex = '#4EC94E' if conv else '#F06464'
            cv_lbl = 'CONVERGED' if conv else 'NOT CONVERGED'
            cv_sym = 'OK' if conv else '!!'
            cv_data = [[Paragraph(
                f'<font color="{sc_hex}"><b>[{cv_sym}] {cv_lbl}</b></font>'
                f'<font color="#6E8494">  —  </font>'
                f'<font color="#A0AEBB">W_TO = {Wto:,.1f} lbs  |  '
                f'Mff = {RR["Mff"]:.6f}  |  '
                f'delta_W_E = {RR["diff"]:+.2f} lbs</font>',
                ps('CV2', fontSize=8.5, fontName='Helvetica-Bold',
                   textColor=sc, backColor=C_HDR, leading=12))
            ]]
            cv_tbl = Table(cv_data, colWidths=[PW])
            cv_tbl.setStyle(TableStyle([
                ('BACKGROUND',    (0,0), (0,0), C_HDR),
                ('LINEBELOW',     (0,0), (0,0), 2.0, sc),
                ('LEFTPADDING',   (0,0), (0,0), 10),
                ('TOPPADDING',    (0,0), (0,0), 7),
                ('BOTTOMPADDING', (0,0), (0,0), 7),
            ]))
            story.append(cv_tbl)
            story.append(Spacer(1, 0.3*cm))

            # ── KPI summary row ──────────────────────────────────
            story.append(Paragraph('KEY PERFORMANCE INDICATORS', sH1))
            kpi_data = [
                ['W_TO', 'Mff', 'W_F', 'W_PL', 'W_E'],
                [f'{Wto:,.0f} lbs', f'{RR["Mff"]:.5f}',
                 f'{WF:,.0f} lbs', f'{Wpl:,.0f} lbs', f'{WE:,.0f} lbs'],
                ['Gross Takeoff', 'Fuel Fraction', 'Total Fuel', 'Payload', 'Empty Weight'],
            ]
            kpi_tbl = Table(kpi_data, colWidths=[PW/5]*5)
            kpi_tbl.setStyle(TableStyle([
                ('BACKGROUND',    (0,0), (-1,0), C_HDR),
                ('BACKGROUND',    (0,1), (-1,1), C_BG2),
                ('BACKGROUND',    (0,2), (-1,2), C_BG),
                ('TEXTCOLOR',     (0,0), (-1,0), C_GOLD),
                ('TEXTCOLOR',     (0,1), (-1,1), C_WHITE),
                ('TEXTCOLOR',     (0,2), (-1,2), C_MGRAY),
                ('FONTNAME',      (0,0), (-1,0), 'Helvetica-Bold'),
                ('FONTNAME',      (0,1), (-1,1), 'Courier-Bold'),
                ('FONTNAME',      (0,2), (-1,2), 'Helvetica'),
                ('FONTSIZE',      (0,0), (-1,0), 8),
                ('FONTSIZE',      (0,1), (-1,1), 9.5),
                ('FONTSIZE',      (0,2), (-1,2), 7),
                ('ALIGN',         (0,0), (-1,-1), 'CENTER'),
                ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
                ('TOPPADDING',    (0,0), (-1,-1), 5),
                ('BOTTOMPADDING', (0,0), (-1,-1), 5),
                ('GRID',          (0,0), (-1,-1), 0.3, C_BORDER),
                ('LINEABOVE',     (0,0), (-1,0),  1.5, C_GOLD),
                ('LINEBELOW',     (0,2), (-1,2),  1.5, C_GOLD),
                # Highlight W_TO gold
                ('TEXTCOLOR',     (0,1), (0,1), C_GOLD2),
                ('FONTSIZE',      (0,1), (0,1), 11),
            ]))
            story.append(kpi_tbl)
            story.append(Spacer(1, 0.4*cm))

            # ── Section 1: Mission Inputs ────────────────────────
            story.append(Paragraph('1   MISSION INPUTS', sH1))
            t_in = dark_table([
                ['Parameter', 'Value', 'Parameter', 'Value'],
                ['Passengers', str(int(npax)), 'Design Range (nm)', str(int(R_nm))],
                ['Pax weight (lbs)', str(int(wpax)), 'Baggage (lbs)', str(int(wbag))],
                ['Flight crew', str(int(ncrew)), 'Cabin attendants', str(int(natt))],
                ['Cruise L/D', f'{LDc:.1f}', 'Loiter L/D', f'{LDl:.1f}'],
                ['Cruise Cp (lbs/hp/hr)', f'{Cpc:.2f}', 'Loiter Cp', f'{Cpl:.2f}'],
                ['Cruise eta_p', f'{npc:.2f}', 'Loiter eta_p', f'{npl:.2f}'],
                ['Loiter E (hr)', f'{El:.2f}', 'Loiter V (kts)', str(int(Vl))],
                ['A (regression)', f'{A_v:.4f}', 'B (regression)', f'{B_v:.4f}'],
                ['M_tfo', f'{Mtfo:.3f}', 'M_res', f'{Mres:.3f}'],
            ], [PW*0.30, PW*0.20, PW*0.30, PW*0.20],
            val_cols=[1, 3], gold_col0=True)
            story.append(t_in)
            story.append(Spacer(1, 0.4*cm))

            # ── Section 2: Key Equations ─────────────────────────
            story.append(Paragraph('2   KEY EQUATIONS  (Raymer 2018, Chapter 2)', sH1))

            story.append(Paragraph('2.1  Cruise Weight Fraction — Breguet Range Equation (Eq. 2.9)', sH2))
            story.append(Paragraph('W5/W4 = 1 / exp[ Rc / (375 * (eta_p/Cp) * (L/D)) ]', sEQ))

            story.append(Paragraph('2.2  Loiter Weight Fraction — Breguet Endurance Equation (Eq. 2.11)', sH2))
            story.append(Paragraph('W6/W5 = 1 / exp[ E / (375 * (1/V) * (eta_p/Cp) * (L/D)) ]', sEQ))

            story.append(Paragraph('2.3  Empty Weight Regression (Table 2.2 / 2.15)', sH2))
            story.append(Paragraph('log10(W_E) = A  +  B * log10(W_TO)', sEQ))

            story.append(Paragraph('2.4  Fuel Weight Build-Up', sH2))
            story.append(Paragraph('W_F_used = W_TO * (1 - Mff)', sEQ))
            story.append(Paragraph('W_F_total = W_F_used * (1 + M_res)', sEQ))

            story.append(Paragraph(
                'Units: Rc in statute miles (= nm x 1.15078)  |  '
                'Cp in lbs/hp/hr  |  V in mph  |  E in hours  |  eta_p dimensionless',
                sBODY))
            story.append(Spacer(1, 0.3*cm))

            # Computed values table
            story.append(Paragraph('2.5  Computed Equation Inputs (converted units)', sH2))
            eq_vals = dark_table([
                ['Converted Quantity', 'Value', 'Source'],
                ['Rc — cruise range (statute miles)', f'{RR["Rc"]:.3f}', f'{R_nm} nm x 1.15078'],
                ['Vm — loiter speed (mph)',           f'{RR["Vm"]:.2f}', f'{Vl} kts x 1.15078'],
                ['W5/W4 cruise fraction',             f'{[v for v,t,_ in RR["phases"].values() if t=="Breguet"][0]:.6f}', 'Eq. 2.9'],
                ['W6/W5 loiter fraction',             f'{[v for v,t,_ in RR["phases"].values() if t=="Breguet"][1]:.6f}', 'Eq. 2.11'],
                ['Mff — mission fuel fraction',       f'{RR["Mff"]:.6f}', 'Product of 8 phases'],
            ], [PW*0.48, PW*0.24, PW*0.28], val_cols=[1])
            story.append(eq_vals)
            story.append(Spacer(1, 0.4*cm))

            # ── Section 3: Phase Weight Fractions ───────────────
            story.append(Paragraph('3   MISSION PHASE WEIGHT FRACTIONS', sH1))
            ph_data = [['Phase', 'Wi/Wi-1', 'Type', 'Source', 'Cum. Mff']]
            cm3 = 1.0
            for pname, (fv, ft, fs) in RR['phases'].items():
                cm3 *= fv
                ph_data.append([pname, f'{fv:.5f}', ft, fs, f'{cm3:.5f}'])
            ph_data.append(['PRODUCT (Mff)', '—', '—', 'All phases', f'{RR["Mff"]:.6f}'])
            ph_tbl = dark_table(ph_data,
                [PW*0.22, PW*0.14, PW*0.13, PW*0.13, PW*0.15],
                val_cols=[1, 4])
            ph_tbl.setStyle(TableStyle([
                ('TEXTCOLOR', (-1,1), (-1,-2), C_BLUE2),
                ('TEXTCOLOR', (1,1),  (1,-1),  C_GOLD2),
                ('BACKGROUND', (0,-1), (-1,-1), C_PANEL2),
                ('TEXTCOLOR',  (0,-1), (-1,-1), C_GOLD),
                ('FONTNAME',   (0,-1), (-1,-1), 'Helvetica-Bold'),
            ]))
            story.append(ph_tbl)
            story.append(Spacer(1, 0.3*cm))

            # ── Chart 1: Phase fractions bar chart ──────────────
            story.append(Paragraph('CHART 1 — Mission Phase Weight Fractions', sH2))
            story.append(Paragraph(
                'Each bar shows the weight fraction Wi/Wi-1 for that mission phase. '
                'Values closer to 1.0 indicate less fuel consumption. '
                'Fixed fractions (blue) come from Raymer Table 2.1; '
                'Breguet fractions (gold) are computed from the range/endurance equations.',
                sBODY))
            ph_labels = list(RR['phases'].keys())
            ph_fvals  = [v for v, _, _ in RR['phases'].values()]
            ph_types  = [t for _, t, _ in RR['phases'].values()]
            ph_colors = [C_BLUE2 if t == 'Fixed' else C_GOLD for t in ph_types]
            bar_d = make_bar_chart_drawing(
                ph_labels, ph_fvals, ph_colors,
                width=PW, height=5.5*cm,
                title='Phase Weight Fractions  (Wi / Wi-1)')
            story.append(bar_d)
            story.append(Spacer(1, 0.15*cm))

            # Cumulative Mff note
            cum_note = [['Ramp=1.0']]
            cv = 1.0
            for ph, (fv, _, _) in RR['phases'].items():
                cv *= fv
                cum_note[0].append(f'{ph[:6]}={cv:.4f}')
            note_tbl = Table(cum_note, colWidths=[PW/9]*9 if len(cum_note[0])==9 else [PW/len(cum_note[0])]*len(cum_note[0]))
            note_tbl.setStyle(TableStyle([
                ('TEXTCOLOR',  (0,0), (-1,-1), C_MGRAY),
                ('FONTNAME',   (0,0), (-1,-1), 'Courier'),
                ('FONTSIZE',   (0,0), (-1,-1), 6),
                ('ALIGN',      (0,0), (-1,-1), 'CENTER'),
                ('TOPPADDING', (0,0), (-1,-1), 2),
                ('BOTTOMPADDING',(0,0),(-1,-1),2),
            ]))
            story.append(note_tbl)
            story.append(Spacer(1, 0.4*cm))

            # ── Section 4: Sizing Results ────────────────────────
            story.append(Paragraph('4   SIZING RESULTS', sH1))
            res_data = [['Quantity', 'Value (lbs)', 'Expression']]
            for nm, vl_r, ex in [
                ('W_TO   Gross Takeoff Weight',  f'{Wto:,.2f}',       'Bisection convergence solution'),
                ('W_F    Total Fuel Weight',      f'{WF:,.2f}',        'W_TO x (1 - Mff) x (1 + M_res)'),
                ('W_F_used  Usable Fuel',         f'{RR["WFu"]:,.2f}', 'W_TO x (1 - Mff)'),
                ('W_tfo  Trapped Fuel & Oil',     f'{Wtfo_r:,.3f}',    f'M_tfo x W_TO = {Mtfo:.3f} x {Wto:,.0f}'),
                ('W_OE   Operating Empty',        f'{WOE:,.2f}',       'W_TO - W_F - W_PL'),
                ('W_E    Empty Weight (tent.)',    f'{WE:,.2f}',        'W_OE - W_tfo - W_crew'),
                ('W_Ea   Empty Weight (allow.)',   f'{RR["WEa"]:,.2f}', '10^[(log W_TO - A)/B]'),
                ('delta_WE  Convergence error',   f'{RR["diff"]:+.3f}', 'W_Ea - W_E  ->  0'),
                ('W_PL   Payload',                f'{Wpl:,.2f}',       f'{npax} pax x ({wpax}+{wbag}) lbs'),
                ('W_crew  Crew Weight',           f'{Wcrew:,.2f}',     f'{ncrew} pilots + {natt} attendants'),
                ('Mff    Mission Fuel Fraction',  f'{RR["Mff"]:.6f}',  'Product of all 8 phase fractions'),
            ]:
                res_data.append([nm, vl_r, ex])
            res_tbl = dark_table(res_data,
                [PW*0.33, PW*0.20, PW*0.47], val_cols=[1])
            story.append(res_tbl)
            story.append(Spacer(1, 0.4*cm))

            # ── Chart 2: Convergence diagram ─────────────────────
            story.append(Paragraph('CHART 2 — Sizing Loop Convergence', sH2))
            story.append(Paragraph(
                'The blue line shows W_E (tentative) computed from the mission weight build-up. '
                'The gold line shows W_E (allowable) from the statistical regression. '
                'The green dot marks the solution W_TO where both lines intersect (convergence).',
                sBODY))
            conv_d = make_convergence_drawing(Wto, P, WE,
                width=PW, height=5.8*cm,
                title='W_E Tentative (blue) vs W_E Allowable (gold) — Solution at green dot')
            story.append(conv_d)
            story.append(Spacer(1, 0.4*cm))

            # ── Section 5: Weight Ratios ─────────────────────────
            story.append(Paragraph('5   WEIGHT RATIOS — SANITY CHECK', sH1))
            rat_data = [['Ratio', 'Computed', 'Typical Range', 'Status', 'Comment']]
            for nm, vr, lo_r, hi_r, cmt in [
                ('W_PL / W_TO', Wpl/Wto, 0.10, 0.25, 'Payload fraction'),
                ('W_F  / W_TO', WF/Wto,  0.20, 0.45, 'Fuel fraction'),
                ('W_E  / W_TO', WE/Wto,  0.45, 0.65, 'Empty weight fraction'),
                ('W_PL / W_E',  Wpl/WE,  0.15, 0.40, 'Payload to empty ratio')]:
                ok_r = lo_r <= vr <= hi_r
                chk = '[OK]' if ok_r else ('[HIGH]' if vr > hi_r else '[LOW]')
                rat_data.append([nm, f'{vr:.4f}',
                                  f'{lo_r:.2f} - {hi_r:.2f}', chk, cmt])
            rat_tbl = dark_table(rat_data,
                [PW*0.24, PW*0.14, PW*0.20, PW*0.12, PW*0.30], val_cols=[1])
            rat_tbl.setStyle(TableStyle([
                ('TEXTCOLOR', (3,1), (3,-1), C_GREEN),
            ]))
            story.append(rat_tbl)
            story.append(Spacer(1, 0.4*cm))

            # ── Chart 3: Weight composition pie ──────────────────
            story.append(Paragraph('CHART 3 — Weight Composition at Solution W_TO', sH2))
            story.append(Paragraph(
                'Distribution of W_TO among major weight groups: '
                'fuel (gold), payload (blue), trapped fuel (amber), '
                'crew (purple), and empty structure (green).',
                sBODY))

            pie_labels  = ['W_F Fuel', 'W_PL Payload', 'W_tfo Trapped', 'W_crew Crew', 'W_E Empty']
            pie_values  = [WF, Wpl, Wtfo_r, Wcrew, WE]
            pie_colors  = [C_GOLD, C_BLUE2, C_AMBER, C_PURPLE, C_GREEN]

            # Pie + legend side by side
            pie_d = make_pie_drawing(pie_labels, pie_values, pie_colors,
                                      width=8*cm, height=6.5*cm,
                                      title='Weight Breakdown (% of W_TO)')
            legend_rows = [['Component', 'Weight (lbs)', '% of W_TO']]
            for lbl, val in zip(pie_labels, pie_values):
                legend_rows.append([lbl, f'{val:,.1f}', f'{val/Wto*100:.1f}%'])
            legend_rows.append(['W_TO Total', f'{Wto:,.1f}', '100.0%'])
            leg_tbl = dark_table(legend_rows,
                [PW*0.38, PW*0.22, PW*0.18], val_cols=[1, 2])
            leg_tbl.setStyle(TableStyle([
                ('BACKGROUND', (0,-1), (-1,-1), C_PANEL2),
                ('TEXTCOLOR',  (0,-1), (-1,-1), C_GOLD),
                ('FONTNAME',   (0,-1), (-1,-1), 'Helvetica-Bold'),
            ]))

            combined = Table([[pie_d, leg_tbl]], colWidths=[8.2*cm, PW - 8.2*cm])
            combined.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ]))
            story.append(combined)
            story.append(Spacer(1, 0.4*cm))

            # ── Section 6: Sensitivity Analysis ─────────────────
            story.append(PageBreak())
            story.append(Paragraph('6   SENSITIVITY ANALYSIS  (Raymer Eq. 2.44 – 2.51)', sH1))

            story.append(Paragraph('6.1  Intermediate Sizing Factors', sH2))
            fac_data = [
                ['Factor', 'Symbol', 'Value', 'Equation'],
                ['Fuel availability factor',    'C',
                 f'{S["C"]:.6f}', '1 - (1+M_res)(1-Mff) - M_tfo  [Eq 2.22]'],
                ['Fixed payload + crew',        'D',
                 f'{S["D"]:,.2f} lbs', 'W_PL + W_crew  [Eq 2.23]'],
                ['Denominator C(1-B)W_TO - D',  'denom',
                 f'{S["C"]*(1-float(B_v))*Wto - S["D"]:,.2f}', 'see Eq 2.44'],
                ['Sizing multiplier',           'F',
                 f'{S["F"]:,.2f} lbs', '-B * W_TO^2 * (1+M_res) * Mff / denom  [Eq 2.44]'],
            ]
            story.append(dark_table(fac_data,
                [PW*0.28, PW*0.08, PW*0.18, PW*0.46], val_cols=[2]))
            story.append(Spacer(1, 0.25*cm))

            story.append(Paragraph('6.2  Partial Derivatives dW_TO/dX', sH2))
            sen_data = [['Partial Derivative', 'Value', 'Units', 'Eq.', 'Interpretation']]
            for partial, val, unit, eq, interp in [
                ('dW_TO / dCp (cruise)',  S['dCpR'], 'lbs/(lbs/hp/hr)', 'Eq 2.49',
                 '+ve: higher SFC increases W_TO'),
                ('dW_TO / dn_p (cruise)', S['dnpR'], 'lbs',             'Eq 2.50',
                 '-ve: better prop eff. reduces W_TO'),
                ('dW_TO / d(L/D) cruise', S['dLDR'], 'lbs',             'Eq 2.51',
                 '-ve: higher L/D reduces W_TO'),
                ('dW_TO / dR',            S['dR'],   'lbs/nm',          'Eq 2.45',
                 '+ve: longer range increases W_TO'),
                ('dW_TO / dCp (loiter)',  S['dCpE'], 'lbs/(lbs/hp/hr)', '—',
                 '+ve: higher SFC increases W_TO'),
                ('dW_TO / dn_p (loiter)', S['dnpE'], 'lbs',             '—',
                 '-ve: better prop eff. reduces W_TO'),
                ('dW_TO / d(L/D) loiter', S['dLDE'], 'lbs',             '—',
                 '-ve: higher L/D reduces W_TO')]:
                sen_data.append([partial, f'{val:+,.2f}', unit, eq, interp])
            sen_tbl = dark_table(sen_data,
                [PW*0.28, PW*0.14, PW*0.20, PW*0.09, PW*0.29], val_cols=[1])
            # Color +/- values
            for row_i in range(1, len(sen_data)):
                val = [S['dCpR'], S['dnpR'], S['dLDR'], S['dR'],
                       S['dCpE'], S['dnpE'], S['dLDE']][row_i-1]
                col = C_RED if val > 0 else C_GREEN
                sen_tbl.setStyle(TableStyle([
                    ('TEXTCOLOR', (1,row_i), (1,row_i), col)]))
            story.append(sen_tbl)
            story.append(Spacer(1, 0.3*cm))

            # ── Chart 4: Sensitivity Tornado ──────────────────────
            story.append(Paragraph('CHART 4 — Sensitivity Tornado Diagram', sH2))
            story.append(Paragraph(
                'Shows the magnitude of dW_TO/dX for each design parameter. '
                'Red bars (positive): increasing X increases W_TO. '
                'Green bars (negative): increasing X decreases W_TO. '
                'Sorted by absolute magnitude — longest bar = most critical parameter.',
                sBODY))
            tornado_d = make_tornado_drawing(S, width=PW, height=6.0*cm,
                title='dW_TO/dX — Sensitivity of Gross Weight to Design Parameters')
            story.append(tornado_d)
            story.append(Spacer(1, 0.4*cm))

            # ── Range Trade table ────────────────────────────────
            story.append(Paragraph('6.3  Range Trade Study  (dW_TO/dR = {:.2f} lbs/nm)'.format(S['dR']), sH2))
            trade_data = [['Delta Range (nm)', 'Delta W_TO (lbs)', 'New W_TO (lbs)', 'Change']]
            for dr in [-300, -200, -100, +100, +200, +300]:
                dw = S['dR'] * dr
                nw = Wto + dw
                chg = 'LIGHTER' if dw < 0 else 'HEAVIER'
                trade_data.append([f'{dr:+d}', f'{dw:+,.1f}', f'{nw:,.1f}', chg])
            story.append(dark_table(trade_data,
                [PW*0.22, PW*0.25, PW*0.25, PW*0.20], val_cols=[1, 2]))
            story.append(Spacer(1, 0.5*cm))

            # ══════════════════════════════════════════════════════
            # SECTION 7: SYMBOL REFERENCE TABLE
            # ══════════════════════════════════════════════════════
            story.append(PageBreak())
            story.append(Paragraph('7   SYMBOL & NOTATION REFERENCE', sH1))
            story.append(Paragraph(
                'Complete reference for all symbols, abbreviations, and notation '
                'used in AeroSizer Pro. Based on Raymer (2018) Chapter 2 conventions.',
                sBODY))
            story.append(Spacer(1, 0.2*cm))

            # Weight symbols
            story.append(Paragraph('7.1  Weight Symbols', sH2))
            wsym_data = [
                ['Symbol', 'Full Name', 'Units', 'Definition'],
                ['W_TO',   'Gross Takeoff Weight',    'lbs',
                 'Total weight at start of mission. Primary sizing target.'],
                ['W_E',    'Empty Weight',            'lbs',
                 'Structural + systems + propulsion weight. No fuel, crew, or payload.'],
                ['W_OE',   'Operating Empty Weight',  'lbs',
                 'W_E + trapped fuel + crew. Aircraft empty but ready to fly.'],
                ['W_F',    'Total Fuel Weight',       'lbs',
                 'Usable fuel + fuel reserve = W_F_used x (1 + M_res).'],
                ['W_F_used','Usable Fuel Weight',     'lbs',
                 'Fuel burned during mission = W_TO x (1 - Mff).'],
                ['W_tfo',  'Trapped Fuel & Oil',      'lbs',
                 'Undrainable fuel in lines/tanks = M_tfo x W_TO.'],
                ['W_PL',   'Payload Weight',          'lbs',
                 'Passengers + baggage. Does not include crew.'],
                ['W_crew', 'Crew Weight',             'lbs',
                 'Flight crew (pilots) + cabin attendants. Assumed 205 lbs/person.'],
                ['W_E_tent','Empty Weight (Tentative)','lbs',
                 'Computed from mission sizing: W_OE - W_tfo - W_crew.'],
                ['W_Ea',   'Empty Weight (Allowable)','lbs',
                 'From regression: 10^[(log10(W_TO) - A) / B].'],
                ['delta_WE','Convergence Error',      'lbs',
                 'W_Ea - W_E_tent. Solution found when |delta_WE| < 1 lb.'],
            ]
            story.append(dark_table(wsym_data,
                [PW*0.14, PW*0.24, PW*0.10, PW*0.52], val_cols=[]))
            story.append(Spacer(1, 0.25*cm))

            # Mission parameters
            story.append(Paragraph('7.2  Mission & Aerodynamic Parameters', sH2))
            msym_data = [
                ['Symbol', 'Full Name', 'Units', 'Definition'],
                ['R',      'Design Range',            'nm',
                 'Required flight distance (nautical miles). Converted to statute miles for Raymer eq.'],
                ['Rc',     'Cruise Range (converted)', 'stat. mi',
                 'Rc = R x 1.15078. Used directly in Breguet cruise equation.'],
                ['V',      'Loiter Speed',            'kts',
                 'Airspeed during loiter/reserve segment (knots).'],
                ['Vm',     'Loiter Speed (converted)', 'mph',
                 'Vm = V x 1.15078. Used directly in Breguet endurance equation.'],
                ['E',      'Loiter Endurance',        'hr',
                 'Duration of loiter/reserve segment in hours.'],
                ['L/D',    'Lift-to-Drag Ratio',      '—',
                 'Aerodynamic efficiency. Higher is better. Subscript c=cruise, l=loiter.'],
                ['L/Dc',   'Cruise L/D',              '—',
                 'Lift-to-drag ratio at cruise condition. Typical turboprop: 10-16.'],
                ['L/Dl',   'Loiter L/D',              '—',
                 'Lift-to-drag ratio at loiter condition. Often higher than cruise L/D.'],
            ]
            story.append(dark_table(msym_data,
                [PW*0.12, PW*0.26, PW*0.12, PW*0.50], val_cols=[]))
            story.append(Spacer(1, 0.25*cm))

            # Propulsion parameters
            story.append(Paragraph('7.3  Propulsion Parameters', sH2))
            psym_data = [
                ['Symbol', 'Full Name', 'Units', 'Definition'],
                ['Cp',     'Specific Fuel Consumption', 'lbs/hp/hr',
                 'Fuel burned per unit power per unit time. Lower = more efficient engine. Typical turboprop: 0.4-0.7.'],
                ['Cpc',    'Cruise SFC',              'lbs/hp/hr',
                 'Specific fuel consumption at cruise power setting.'],
                ['Cpl',    'Loiter SFC',              'lbs/hp/hr',
                 'Specific fuel consumption at loiter/reserve power setting.'],
                ['eta_p',  'Propeller Efficiency',    '—',
                 'Ratio of thrust power to shaft power (0 to 1). Typical: 0.75-0.90.'],
                ['eta_pc', 'Cruise Prop. Efficiency', '—',
                 'Propeller efficiency at cruise condition.'],
                ['eta_pl', 'Loiter Prop. Efficiency', '—',
                 'Propeller efficiency at loiter condition. Often lower than cruise.'],
            ]
            story.append(dark_table(psym_data,
                [PW*0.12, PW*0.26, PW*0.12, PW*0.50], val_cols=[]))
            story.append(Spacer(1, 0.25*cm))

            # Fuel fractions
            story.append(Paragraph('7.4  Fuel Fraction Symbols', sH2))
            fsym_data = [
                ['Symbol', 'Full Name', 'Definition'],
                ['Mff',    'Mission Fuel Fraction',
                 'Product of all 8 phase weight fractions. = W_final / W_initial.'],
                ['Wi/Wi-1','Phase Weight Fraction',
                 'Weight at end of phase i divided by weight at start. Values < 1.0 indicate fuel burned.'],
                ['M_tfo',  'Trapped Fuel & Oil Fraction',
                 'Fraction of W_TO reserved for undrainable fuel. Typical: 0.001-0.005.'],
                ['M_res',  'Reserve Fuel Fraction',
                 'Additional fuel fraction beyond mission requirement. FAR 135 requires 30-45 min reserve.'],
                ['W5/W4',  'Cruise Phase Fraction',
                 'Breguet cruise weight fraction (end of cruise / start of cruise).'],
                ['W6/W5',  'Loiter Phase Fraction',
                 'Breguet loiter weight fraction (end of loiter / start of loiter).'],
            ]
            story.append(dark_table(fsym_data,
                [PW*0.12, PW*0.25, PW*0.63], val_cols=[]))
            story.append(Spacer(1, 0.25*cm))

            # Regression parameters
            story.append(Paragraph('7.5  Regression & Convergence Parameters', sH2))
            rsym_data = [
                ['Symbol', 'Full Name', 'Definition'],
                ['A',      'Regression Intercept',
                 'Aircraft-type specific constant from Raymer Table 2.15. '
                 'For turboprop transports, typical value 0.3774.'],
                ['B',      'Regression Slope',
                 'Aircraft-type specific slope from Raymer Table 2.2/2.15. '
                 'For turboprop transports, typical value 0.9647.'],
                ['C',      'Fuel Availability Factor',
                 'C = 1 - (1+M_res)(1-Mff) - M_tfo. Internal sizing factor (Eq 2.22).'],
                ['D',      'Fixed Weight Demand',
                 'D = W_PL + W_crew. Total non-fuel, non-structural weight (Eq 2.23).'],
                ['F',      'Sizing Multiplier',
                 'F = -B*W_TO^2*(1+M_res)*Mff / [C(1-B)W_TO - D]. '
                 'Scales all partial derivatives (Eq 2.44).'],
            ]
            story.append(dark_table(rsym_data,
                [PW*0.10, PW*0.24, PW*0.66], val_cols=[]))
            story.append(Spacer(1, 0.25*cm))

            # Sensitivity derivatives
            story.append(Paragraph('7.6  Sensitivity Partial Derivatives', sH2))
            ssym_data = [
                ['Symbol', 'Meaning', 'Equation'],
                ['dW_TO/dCp',   'Change in W_TO per unit SFC change',    'Eq 2.49 (cruise) / analogous (loiter)'],
                ['dW_TO/dn_p',  'Change in W_TO per unit prop efficiency','Eq 2.50 (cruise) / analogous (loiter)'],
                ['dW_TO/d(L/D)','Change in W_TO per unit L/D change',    'Eq 2.51 (cruise) / analogous (loiter)'],
                ['dW_TO/dR',    'Change in W_TO per nm of range added',   'Eq 2.45'],
                ['dW_TO/dW_PL', 'Change in W_TO per lb of payload added', 'Eq 2.46 (not shown in UI)'],
            ]
            story.append(dark_table(ssym_data,
                [PW*0.20, PW*0.42, PW*0.38], val_cols=[]))
            story.append(Spacer(1, 0.25*cm))

            # Mission phases
            story.append(Paragraph('7.7  Mission Phase Descriptions', sH2))
            mph_data = [
                ['Phase', 'Type', 'Fraction', 'Description'],
                ['Engine Start', 'Fixed',   '0.990', 'APU/engine start fuel consumption. From Raymer Table 2.1.'],
                ['Taxi',         'Fixed',   '0.995', 'Ground taxi to runway. Fixed fraction from Table 2.1.'],
                ['Takeoff',      'Fixed',   '0.995', 'Takeoff roll and initial climb. Table 2.1.'],
                ['Climb',        'Fixed',   '0.985', 'Climb to cruise altitude. Approximate from Fig. 2.2.'],
                ['Cruise',       'Breguet', 'Eq 2.9','Cruise to destination. Computed via Breguet range equation.'],
                ['Loiter',       'Breguet', 'Eq 2.11','Reserve/holding pattern. Breguet endurance equation.'],
                ['Descent',      'Fixed',   '0.985', 'Descent from cruise altitude. Approx. from Fig. 2.2.'],
                ['Landing',      'Fixed',   '0.995', 'Final approach, touchdown, and taxi-in. Table 2.1.'],
            ]
            story.append(dark_table(mph_data,
                [PW*0.18, PW*0.12, PW*0.12, PW*0.58], val_cols=[]))
            story.append(Spacer(1, 0.3*cm))

            # Unit conversions reference
            story.append(Paragraph('7.8  Unit Conversion Reference', sH2))
            uc_data = [
                ['From', 'To', 'Factor', 'Usage in AeroSizer'],
                ['Nautical miles (nm)',  'Statute miles (sm)', '× 1.15078', 'Range R for Breguet cruise eq.'],
                ['Knots (kts)',          'Miles/hour (mph)',   '× 1.15078', 'Loiter speed V for Breguet endurance eq.'],
                ['lbs/hp/hr',            'lbs/hp/hr',          '× 1.0',    'SFC Cp — no conversion needed'],
                ['Hours (hr)',           'Hours (hr)',          '× 1.0',    'Endurance E — no conversion needed'],
            ]
            story.append(dark_table(uc_data,
                [PW*0.25, PW*0.22, PW*0.15, PW*0.38], val_cols=[2]))
            story.append(Spacer(1, 0.4*cm))

            # ── Footer / signature ───────────────────────────────
            story.append(HRFlowable(width=PW, thickness=0.6, color=C_GOLD,
                                     spaceBefore=5, spaceAfter=5))
            story.append(Paragraph(
                f'AeroSizer Pro  |  Raymer (2018): Aircraft Design — A Conceptual Approach  |  '
                f'W_TO = {Wto:,.1f} lbs  |  Mff = {RR["Mff"]:.6f}  |  '
                f'{"CONVERGED" if conv else "NOT CONVERGED"}  |  '
                f'Sections: Inputs / Equations / Phase Fractions / Results / Ratios / Sensitivity / Symbol Ref.',
                sFOOT))

            doc.build(story)
            buf.seek(0)
            return buf.read()

        st.markdown(f"""
        <div class="card card-gold">
          <div class="card-title">PDF Report Contents</div>
          <div style="font-size:.77rem;color:var(--text);line-height:2.0">
            <b style="color:var(--gold2)">1</b> · Mission inputs table<br>
            <b style="color:var(--gold2)">2</b> · Key equations (Raymer Ch.2) + computed values<br>
            <b style="color:var(--gold2)">3</b> · Mission phase weight fractions + Chart 1 (bar chart)<br>
            <b style="color:var(--gold2)">4</b> · Full sizing results + Chart 2 (convergence diagram)<br>
            <b style="color:var(--gold2)">5</b> · Weight ratios sanity check + Chart 3 (pie chart)<br>
            <b style="color:var(--gold2)">6</b> · Sensitivity analysis + Chart 4 (tornado) + range trade<br>
            <b style="color:var(--gold2)">7</b> · Symbol & notation reference (all symbols explained)
          </div>
          <div style="margin-top:.65rem;font-size:.67rem;color:#6e7681">
            Dark theme · A4 format · {'✓ Converged' if conv else '⚠ Check convergence before export'}
          </div>
        </div>""", unsafe_allow_html=True)

        st.download_button(
            "⬇  Generate & Download PDF (A4)", make_pdf(),
            "aerosizer_report.pdf", "application/pdf",
            use_container_width=True)
