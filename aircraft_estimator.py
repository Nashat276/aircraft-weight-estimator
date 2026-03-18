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

st.set_page_config(page_title="AeroSizer Pro — HW 2.8", page_icon="✈", layout="wide")

# ═══════════════════════════════════════════════════════════════
#  CSS  —  Engineering Calculation Sheet aesthetic
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=Inter:wght@300;400;500;600&display=swap');
*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] {
    background: #F0F2F5 !important;
    color: #0D1B2A !important;
    font-family: 'Inter', sans-serif !important;
}
.stApp { background: #F0F2F5 !important; }

/* ─ Step block ─ */
.step-block {
    background: #fff;
    border: 1px solid #D1D9E6;
    border-left: 4px solid #1B4FD8;
    border-radius: 0 8px 8px 0;
    padding: 1rem 1.25rem 0.9rem;
    margin-bottom: 0.85rem;
}
.step-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.58rem;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #1B4FD8;
    padding-bottom: 0.42rem;
    border-bottom: 1px solid #EEF1F7;
    margin-bottom: 0.7rem;
}
.eq-box {
    background: #F7F9FF;
    border: 1px solid #C7D4F0;
    border-radius: 6px;
    padding: 0.38rem 0.78rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: #1B4FD8;
    margin-bottom: 0.5rem;
    display: inline-block;
}
.result-pill {
    display: inline-flex;
    align-items: baseline;
    gap: 0.28rem;
    background: #EEF4FF;
    border: 1px solid #A5C0FF;
    border-radius: 6px;
    padding: 0.22rem 0.75rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.84rem;
    font-weight: 600;
    color: #1B3A9E;
    margin-top: 0.32rem;
}
.result-unit { font-size: 0.66rem; font-weight: 400; color: #5B7EC9; }
.result-ok   { background:#ECFDF5; border-color:#6EE7B7; color:#065F46; }
.result-warn { background:#FFF7ED; border-color:#FDBA74; color:#92400E; }

/* ─ Phase row ─ */
.ph-row {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.32rem 0;
    border-bottom: 1px solid #F1F5FB;
    font-size: 0.81rem;
}
.ph-name { flex: 0 0 130px; font-weight: 500; color: #374151; }
.ph-frac { flex: 0 0 80px; font-family: 'JetBrains Mono', monospace;
           color: #1B4FD8; font-size: 0.8rem; }
.ph-src  { flex: 0 0 90px; font-size: 0.68rem; color: #94A3B8;
           background: #F8FAFF; border: 1px solid #E2E8F0;
           border-radius: 4px; padding: 0.05rem 0.4rem; }
.ph-type-b { color: #059669; }  /* Breguet */
.ph-type-f { color: #6366F1; }  /* Fixed */

/* ─ Sensitivity row ─ */
.sens-row {
    display: grid;
    grid-template-columns: 180px 110px 160px 70px;
    gap: 0.5rem;
    padding: 0.28rem 0;
    border-bottom: 1px solid #F1F5FB;
    font-size: 0.79rem;
    align-items: center;
}
.sens-partial { font-family: 'JetBrains Mono', monospace; color: #1B4FD8; }
.sens-val-pos { font-family: 'JetBrains Mono', monospace; color: #B45309; font-weight: 600; }
.sens-val-neg { font-family: 'JetBrains Mono', monospace; color: #065F46; font-weight: 600; }
.sens-unit    { font-size: 0.67rem; color: #94A3B8; }
.sens-eq      { font-size: 0.67rem; color: #6366F1; font-family: 'JetBrains Mono', monospace; }

/* ─ Sidebar ─ */
[data-testid="stSidebar"] { background:#fff !important; border-right:1px solid #D1D9E6 !important; }
.sb-hdr {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.58rem; font-weight: 600;
    letter-spacing: 0.18em; text-transform: uppercase;
    color: #1B4FD8; padding: 0.38rem 0 0.28rem;
    border-bottom: 1px solid #EEF1F7; margin: 0.55rem 0 0.6rem;
}
/* ─ Tabs ─ */
.stTabs [data-baseweb="tab-list"] {
    background: #fff; border-radius: 8px;
    padding: 3px; border: 1px solid #D1D9E6; gap: 2px; margin-bottom: 0.9rem;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 5px; font-size: 0.77rem; font-weight: 500;
    color: #64748B; padding: 0.36rem 0.95rem;
}
.stTabs [aria-selected="true"] { background: #0D1B2A !important; color: #fff !important; }

/* ─ Download button ─ */
div.stDownloadButton > button {
    background: #0D1B2A !important; color: #fff !important;
    border: none !important; border-radius: 7px !important;
    font-size: 0.78rem !important; font-weight: 500 !important;
    padding: 0.5rem 1rem !important; width: 100% !important;
}
/* ─ Calc button ─ */
[data-testid="stSidebar"] div.stButton > button {
    background: linear-gradient(135deg,#1B4FD8,#2563EB) !important;
    color: #fff !important; border: none !important; border-radius: 8px !important;
    font-size: 0.84rem !important; font-weight: 600 !important;
    padding: 0.62rem !important; width: 100% !important;
    box-shadow: 0 2px 8px rgba(27,79,216,0.25) !important;
}
/* ─ KPI card ─ */
.kpi-grid { display: grid; grid-template-columns: repeat(5,1fr); gap: 0.7rem; margin-bottom: 1rem; }
.kpi-card {
    background: #fff; border: 1px solid #D1D9E6;
    border-top: 3px solid #1B4FD8; border-radius: 8px;
    padding: 0.88rem 1rem;
}
.kpi-val {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.55rem; font-weight: 700;
    color: #0D1B2A; line-height: 1.1;
}
.kpi-val.primary { color: #1B4FD8; }
.kpi-unit { font-size: 0.68rem; color: #94A3B8; font-weight: 400; margin-left: 2px; }
.kpi-lbl  { font-size: 0.59rem; letter-spacing: 0.1em; text-transform: uppercase;
             color: #94A3B8; margin-top: 0.32rem; font-weight: 500; }
/* ─ Status bar ─ */
.status-ok  { background:#ECFDF5; border-left:3px solid #10B981; border-radius:0 7px 7px 0;
               padding:0.5rem 1rem; font-family:'JetBrains Mono',monospace; font-size:0.78rem;
               color:#065F46; margin-bottom:1rem; }
.status-err { background:#FFF7ED; border-left:3px solid #F59E0B; border-radius:0 7px 7px 0;
               padding:0.5rem 1rem; font-family:'JetBrains Mono',monospace; font-size:0.78rem;
               color:#92400E; margin-bottom:1rem; }
/* ─ Section divider ─ */
.sec-div {
    font-family: 'JetBrains Mono', monospace; font-size: 0.62rem; font-weight: 600;
    letter-spacing: 0.14em; text-transform: uppercase;
    color: #1B4FD8; border-bottom: 1.5px solid #D1D9E6;
    padding-bottom: 0.35rem; margin: 1rem 0 0.75rem;
}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
#  PHYSICS  (Exact Raymer Ch.2 — matches HW 2.8)
# ═══════════════════════════════════════════════════════════════
def compute_mission(p):
    """Returns all intermediate and final values for HW 2.8 steps 1-6."""
    # Step 1 — Payload
    Wpl   = p['npax']*(p['wpax']+p['wbag']) + p['ncrew']*205 + p['natt']*200
    Wcrew = p['ncrew']*205 + p['natt']*200
    Wtfo  = p['Wto']*p['Mtfo']

    # Step 3 — Phase fractions
    Rc = p['R'] * 1.15078          # nm → statute miles
    Vm = p['Vl'] * 1.15078         # kts → mph (loiter speed)

    W5 = 1.0 / math.exp(Rc / (375.0 * (p['npc']/p['Cpc']) * p['LDc']))   # Eq 2.9
    W6 = 1.0 / math.exp(p['El'] / (375.0*(1.0/Vm)*(p['npl']/p['Cpl'])*p['LDl']))  # Eq 2.11

    phases = {
        'Engine Start': (0.990,  'Fixed',    'T2.1'),
        'Taxi':         (0.995,  'Fixed',    'T2.1'),
        'Takeoff':      (0.995,  'Fixed',    'T2.1'),
        'Climb':        (0.985,  'Fixed',    'Fig 2.2'),
        'Cruise':       (W5,     'Breguet',  'Eq 2.9'),
        'Loiter':       (W6,     'Breguet',  'Eq 2.11'),
        'Descent':      (0.985,  'Fixed',    'T2.1'),
        'Landing':      (0.995,  'Fixed',    'T2.1'),
    }
    Mff = 1.0
    for v,_,_ in phases.values(): Mff *= v

    # Step 4 — Fuel weight
    WFu = p['Wto'] * (1.0 - Mff)
    WF  = WFu + p['Wto']*p['Mr']*(1.0-Mff) + Wtfo

    # Step 4 — WOE tentative
    WOE = p['Wto'] - WF - Wpl

    # Step 5 — WE tentative
    WE  = WOE - Wtfo - Wcrew

    # Step 6 — WE allowable (regression)
    WEa = 10.0**((math.log10(p['Wto']) - p['A']) / p['B'])

    return dict(Wpl=Wpl, Wcrew=Wcrew, Wtfo=Wtfo, Mff=Mff,
                WF=WF, WFu=WFu, WOE=WOE, WE=WE, WEa=WEa,
                diff=WEa-WE, phases=phases, Rc=Rc, Vm=Vm)

def solve_Wto(p, tol=0.5, n=500):
    """Bisection on the WE_tent - WE_allow = 0 root."""
    pp = dict(p)
    prev_d, prev_w, lo, hi = None, None, None, None
    for w in range(8000, 600001, 2000):
        pp['Wto'] = float(w)
        d = compute_mission(pp)['diff']
        if prev_d is not None and prev_d*d <= 0:
            lo, hi = float(prev_w), float(w); break
        prev_d, prev_w = d, w
    if lo is None:
        pp['Wto'] = float(p.get('Wto', 48550))
        return float(p.get('Wto', 48550)), compute_mission(pp)
    for _ in range(n):
        m = (lo+hi)/2.0; pp['Wto'] = m; r = compute_mission(pp)
        if abs(r['diff']) < tol: return m, r
        if r['diff'] > 0: lo = m
        else: hi = m
    return m, compute_mission(pp)

def sensitivity(p, Wto):
    """Breguet partial derivatives — Raymer Table 2.20 & Eq 2.44–2.51."""
    RR   = compute_mission({**p, 'Wto': Wto})
    Mff  = RR['Mff']
    Rc   = RR['Rc']
    Vm   = RR['Vm']
    Wpl  = RR['Wpl']
    Wcrew= RR['Wcrew']

    C  = 1.0 - (1.0 + p['Mr'])*(1.0-Mff) - p['Mtfo']       # Eq 2.22
    D  = Wpl + Wcrew                                           # Eq 2.23
    dn = C*Wto*(1.0-p['B']) - D
    F  = (-p['B']*Wto**2*(1.0+p['Mr'])*Mff)/dn if abs(dn)>1e-6 else 0.0  # Eq 2.44

    E = p['El']
    return dict(
        C=C, D=D, F=F,
        # Range case
        dCpR  =  F*Rc/(375.0*p['npc']*p['LDc']),                    # Eq 2.49
        dnpR  = -F*Rc*p['Cpc']/(375.0*p['npc']**2*p['LDc']),        # Eq 2.50
        dLDR  = -F*Rc*p['Cpc']/(375.0*p['npc']*p['LDc']**2),        # Eq 2.51
        dR    =  F*p['Cpc']/(375.0*p['npc']*p['LDc']),               # Eq 2.45
        # Endurance case
        dCpE  =  F*E*Vm/(375.0*p['npl']*p['LDl']),
        dnpE  = -F*E*Vm*p['Cpl']/(375.0*p['npl']**2*p['LDl']),
        dLDE  = -F*E*Vm*p['Cpl']/(375.0*p['npl']*p['LDl']**2),
    )

# ═══════════════════════════════════════════════════════════════
#  SIDEBAR  — all inputs exactly matching HW 2.8
# ═══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(
        '<div style="font-family:JetBrains Mono,monospace;font-size:1.0rem;'
        'font-weight:700;color:#0D1B2A;margin-bottom:0.2rem">'
        'AERO<span style="color:#1B4FD8">SIZER</span></div>'
        '<div style="font-family:JetBrains Mono,monospace;font-size:0.56rem;'
        'color:#94A3B8;letter-spacing:0.16em;text-transform:uppercase;'
        'margin-bottom:1rem">Raymer Hw 2.8 — Propeller Sizing</div>',
        unsafe_allow_html=True)

    st.markdown('<div class="sb-hdr">① Cabin & Crew</div>', unsafe_allow_html=True)
    npax  = st.number_input("Passengers (#)",             1,  400, 34,   step=1)
    wpax  = st.number_input("Passenger body weight (lbs)",100, 300, 175, step=5)
    wbag  = st.number_input("Baggage weight (lbs)",       0,  100, 30,   step=5)
    ncrew = st.number_input("Flight crew (pilots)",       1,    6, 2,    step=1)
    natt  = st.number_input("Cabin attendants",           0,   10, 1,    step=1)

    st.markdown('<div class="sb-hdr">② Cruise Segment</div>', unsafe_allow_html=True)
    R_nm = st.number_input("Design range (nm)",         100, 6000, 1100, step=50)
    LDc  = st.number_input("Cruise L/D",                4.0, 30.0, 13.0, step=0.5, format="%.1f")
    Cpc  = st.number_input("Cruise SFC  Cp (lbs/hp/hr)",0.20,1.20, 0.60, step=0.01, format="%.2f")
    npc  = st.number_input("Cruise prop. eff.  η_p",   0.30, 0.98, 0.85, step=0.01, format="%.2f")

    st.markdown('<div class="sb-hdr">③ Loiter / Reserve</div>', unsafe_allow_html=True)
    El   = st.number_input("Loiter endurance E (hr)",  0.10,  6.0, 0.75, step=0.05, format="%.2f")
    Vl   = st.number_input("Loiter speed (kts)",         60,  400, 250,  step=5)
    LDl  = st.number_input("Loiter L/D",                4.0, 30.0, 16.0, step=0.5, format="%.1f")
    Cpl  = st.number_input("Loiter SFC  Cp (lbs/hp/hr)",0.20,1.20, 0.65, step=0.01, format="%.2f")
    npl  = st.number_input("Loiter prop. eff.  η_p",   0.30, 0.98, 0.77, step=0.01, format="%.2f")

    st.markdown('<div class="sb-hdr">④ Regression Constants (Raymer T2.2)</div>', unsafe_allow_html=True)
    A_v  = st.number_input("A (Table 2.15)",  0.0, 2.0, 0.3774, step=0.0001, format="%.4f")
    B_v  = st.number_input("B (Table 2.2/2.15)", 0.1, 2.0, 0.9647, step=0.0001, format="%.4f")

    st.markdown('<div class="sb-hdr">⑤ Fuel Allowances</div>', unsafe_allow_html=True)
    Mtfo = st.number_input("M_tfo (trapped fuel)",    0.0, 0.05, 0.005, step=0.001, format="%.3f")
    Mres = st.number_input("M_res (reserve ratio)",   0.0, 0.10, 0.000, step=0.001, format="%.3f")

    st.markdown("<br>", unsafe_allow_html=True)
    calc = st.button("⟳  Run Sizing", use_container_width=True)

# ─ Parameter dict ─
P = dict(npax=int(npax), wpax=float(wpax), wbag=float(wbag),
         ncrew=int(ncrew), natt=int(natt),
         Mtfo=float(Mtfo), Mr=float(Mres),
         R=float(R_nm), Vl=float(Vl),
         LDc=float(LDc), Cpc=float(Cpc), npc=float(npc),
         El=float(El), LDl=float(LDl), Cpl=float(Cpl), npl=float(npl),
         A=float(A_v), B=float(B_v), Wto=48550.0)

# ─ KEY FIX: always recalculate when any input changes ─
P_key = str(sorted({k:v for k,v in P.items() if k!='Wto'}.items()))
if 'res' not in st.session_state or st.session_state.get('_key') != P_key or calc:
    Wto, RR = solve_Wto(P)
    S = sensitivity(P, Wto)
    st.session_state['res']  = (Wto, RR, S)
    st.session_state['_key'] = P_key
else:
    Wto, RR, S = st.session_state['res']

conv   = abs(RR['diff']) < 1.0
WE     = RR['WE'];  WOE = RR['WOE']; WF  = RR['WF']
Wpl    = RR['Wpl']; Wcrew = RR['Wcrew']; Wtfo_r = RR['Wtfo']

# ═══════════════════════════════════════════════════════════════
#  HEADER
# ═══════════════════════════════════════════════════════════════
badge_col = '#ECFDF5' if conv else '#FFF7ED'
badge_tc  = '#065F46' if conv else '#92400E'
badge_txt = '✓ Converged' if conv else '⚠ Not Converged'
st.markdown(f"""
<div style="background:#fff;border:1px solid #D1D9E6;border-radius:10px;
  border-left:5px solid #1B4FD8;padding:0.75rem 1.4rem;margin-bottom:0.85rem;
  display:flex;align-items:center;justify-content:space-between;">
  <div>
    <div style="font-family:'JetBrains Mono',monospace;font-size:1.4rem;
      font-weight:700;color:#0D1B2A;line-height:1">
      AERO<span style="color:#1B4FD8">SIZER</span>
      <span style="font-size:0.85rem;font-weight:400;color:#64748B;margin-left:0.5rem">
        Raymer Ch.2 — Propeller Weight Sizing
      </span>
    </div>
    <div style="font-family:'JetBrains Mono',monospace;font-size:0.62rem;
      color:#94A3B8;margin-top:0.2rem;letter-spacing:0.06em">
      Breguet Range / Endurance Method · Eq 2.9 / 2.11 · Table 2.1 / 2.2
    </div>
  </div>
  <div style="background:{badge_col};color:{badge_tc};
    font-family:'JetBrains Mono',monospace;font-size:0.68rem;font-weight:600;
    padding:0.26rem 0.85rem;border-radius:20px;letter-spacing:0.06em">
    {badge_txt} · ΔW_E = {RR['diff']:+.1f} lbs
  </div>
</div>
""", unsafe_allow_html=True)

# ─ Status bar ─
if conv:
    st.markdown(f'<div class="status-ok">✓  W_TO = {Wto:,.1f} lbs  ·  Mff = {RR["Mff"]:.5f}  ·  W_E(tent) = {WE:,.1f} lbs  ·  W_E(allow) = {RR["WEa"]:,.1f} lbs  ·  ΔW_E = {RR["diff"]:+.2f} lbs</div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div class="status-err">⚠  Not converged — ΔW_E = {RR["diff"]:+.0f} lbs.  Try adjusting A, B constants or Wto guess.</div>', unsafe_allow_html=True)

# ─ KPI row ─
kpis = [
    (f"{Wto:,.0f}",        "lbs", "W_TO  Gross Takeoff",   True),
    (f"{RR['Mff']:.5f}",   "",    "Mff  Fuel Fraction",    False),
    (f"{WF:,.0f}",         "lbs", "W_F  Total Fuel",       False),
    (f"{Wpl:,.0f}",        "lbs", "W_PL  Payload",         False),
    (f"{WE:,.0f}",         "lbs", "W_E  Empty Weight",     False),
]
cols = st.columns(5)
for col,(val,unit,lbl,prim) in zip(cols, kpis):
    with col:
        vc = "primary" if prim else ""
        st.markdown(f"""
        <div class="kpi-card">
          <div class="kpi-val {vc}">{val}<span class="kpi-unit">{unit}</span></div>
          <div class="kpi-lbl">{lbl}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
#  TABS
# ═══════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "  ① Sizing Steps  ",
    "  ② Sensitivity  ",
    "  ③ Charts  ",
    "  ④ Export  ",
    "  ⑤ References  "
])

# ──────────────────────────────────────────
#  TAB 1  —  Step-by-step (HW 2.8 exact)
# ──────────────────────────────────────────
with tab1:
    col_l, col_r = st.columns([3, 2], gap="medium")

    with col_l:
        # ── STEP 1 ──
        pax_wt = int(npax)*(int(wpax)+int(wbag))
        crew_wt= int(ncrew)*205
        att_wt = int(natt)*200
        st.markdown(f"""
        <div class="step-block">
          <div class="step-label">Step 1 — Payload & Crew Weights</div>
          <div class="ph-row">
            <span class="ph-name">{npax} pax × ({int(wpax)}+{int(wbag)}) lbs</span>
            <span class="ph-frac">{pax_wt:,} lbs</span>
            <span class="ph-src" style="color:#6366F1">cabin payload</span>
          </div>
          <div class="ph-row">
            <span class="ph-name">{ncrew} pilots × 205 lbs</span>
            <span class="ph-frac">{crew_wt:,} lbs</span>
            <span class="ph-src" style="color:#6366F1">flight crew</span>
          </div>
          <div class="ph-row">
            <span class="ph-name">{natt} attendant × 200 lbs</span>
            <span class="ph-frac">{att_wt:,} lbs</span>
            <span class="ph-src" style="color:#6366F1">cabin crew</span>
          </div>
          <div style="margin-top:0.5rem">
            <span class="result-pill">W_PL = {Wpl:,.0f} <span class="result-unit">lbs</span></span>
            &nbsp;
            <span class="result-pill">W_crew = {Wcrew:,.0f} <span class="result-unit">lbs</span></span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # ── STEP 2 ──
        st.markdown(f"""
        <div class="step-block">
          <div class="step-label">Step 2 — Unit Conversions</div>
          <div class="ph-row">
            <span class="ph-name">R_cruise</span>
            <span class="ph-frac">{RR['Rc']:.3f} s.m.</span>
            <span class="ph-src" style="color:#0369A1">{R_nm} nm × 1.15078</span>
          </div>
          <div class="ph-row">
            <span class="ph-name">V_loiter</span>
            <span class="ph-frac">{RR['Vm']:.2f} mph</span>
            <span class="ph-src" style="color:#0369A1">{Vl} kts × 1.15078</span>
          </div>
          <div class="ph-row">
            <span class="ph-name">W_tfo  (M_tfo × W_TO)</span>
            <span class="ph-frac">{Wtfo_r:,.2f} lbs</span>
            <span class="ph-src" style="color:#0369A1">{Mtfo:.3f} × {Wto:,.0f}</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # ── STEP 3 ──
        st.markdown('<div class="step-block"><div class="step-label">Step 3 — Mission Phase Weight Fractions</div>', unsafe_allow_html=True)

        cum_mff = 1.0
        cum_list = []
        for ph,(fv,ftype,fsrc) in RR['phases'].items():
            cum_mff *= fv
            t_class = 'ph-type-b' if ftype=='Breguet' else 'ph-type-f'
            cum_list.append((ph,fv,ftype,fsrc,cum_mff))
            st.markdown(f"""
            <div class="ph-row">
              <span class="ph-name">{ph}</span>
              <span class="ph-frac">{fv:.5f}</span>
              <span class="ph-src {t_class}">{ftype}</span>
              <span style="font-size:0.67rem;color:#94A3B8;margin-left:0.3rem">{fsrc}</span>
            </div>""", unsafe_allow_html=True)

        st.markdown(f"""
          <div style="margin-top:0.55rem;padding-top:0.45rem;border-top:1.5px solid #D1D9E6;">
            <span style="font-family:'JetBrains Mono',monospace;font-size:0.82rem;
              font-weight:700;color:#0D1B2A">
              Mff = {RR['Mff']:.5f}
            </span>
            <span style="font-size:0.7rem;color:#94A3B8;margin-left:0.5rem">
              (product of all 8 fractions)
            </span>
          </div>
        </div>""", unsafe_allow_html=True)

        # ── STEPS 4-6 ──
        diff_cls = 'result-ok' if conv else 'result-warn'
        st.markdown(f"""
        <div class="step-block">
          <div class="step-label">Steps 4 – 6 — Weight Build-Up & Convergence</div>
          <div class="ph-row">
            <span class="ph-name" style="flex:0 0 220px">Step 4a — W_F (total fuel)</span>
            <span class="ph-frac">{WF:,.1f} lbs</span>
            <span class="ph-src" style="color:#0369A1">WF_used + W_tfo</span>
          </div>
          <div class="ph-row">
            <span class="ph-name" style="flex:0 0 220px">Step 4b — W_OE (tentative)</span>
            <span class="ph-frac">{WOE:,.1f} lbs</span>
            <span class="ph-src" style="color:#0369A1">W_TO − W_F − W_PL</span>
          </div>
          <div class="ph-row">
            <span class="ph-name" style="flex:0 0 220px">Step 5 — W_E (tentative)</span>
            <span class="ph-frac">{WE:,.2f} lbs</span>
            <span class="ph-src" style="color:#0369A1">W_OE − W_tfo − W_crew</span>
          </div>
          <div class="ph-row">
            <span class="ph-name" style="flex:0 0 220px">Step 6 — W_E (allowable)</span>
            <span class="ph-frac">{RR['WEa']:,.2f} lbs</span>
            <span class="ph-src" style="color:#0369A1">10^[(log W_TO − A)/B]</span>
          </div>
          <div style="margin-top:0.55rem;display:flex;gap:0.5rem;flex-wrap:wrap">
            <span class="result-pill {diff_cls}">
              ΔW_E = {RR['diff']:+.2f} <span class="result-unit">lbs</span>
            </span>
            <span class="result-pill {'result-ok' if conv else 'result-warn'}">
              {'✓ Converged' if conv else '⚠ Not converged'}
            </span>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with col_r:
        # Equation reference card
        st.markdown("""
        <div class="step-block">
          <div class="step-label">Key Equations — Raymer Ch.2</div>
          <div style="font-size:0.72rem;color:#374151;margin-bottom:0.55rem;font-weight:500">
            Cruise fraction (Eq. 2.9):
          </div>
          <div class="eq-box">W₅/W₄ = 1/exp[ Rc / (375·η_p/Cp·L/D) ]</div>
          <div style="font-size:0.72rem;color:#374151;margin:0.55rem 0 0.3rem;font-weight:500">
            Loiter fraction (Eq. 2.11):
          </div>
          <div class="eq-box">W₆/W₅ = 1/exp[ E / (375·(1/V)·η_p/Cp·L/D) ]</div>
          <div style="font-size:0.72rem;color:#374151;margin:0.55rem 0 0.3rem;font-weight:500">
            Regression (Table 2.2/2.15):
          </div>
          <div class="eq-box">log(W_E) = A + B·log(W_TO)</div>
          <div style="font-size:0.67rem;color:#94A3B8;margin-top:0.5rem;line-height:1.6">
            R in statute miles · Cp in lbs/hp/hr<br>
            V in mph · E in hours
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Numeric summary table
        st.markdown('<div class="step-block"><div class="step-label">Numeric Summary</div>', unsafe_allow_html=True)
        df_sum = pd.DataFrame({
            'Symbol': ['W_TO','Mff','W_F','W_F_used','W_tfo','W_OE','W_E_tent','W_E_allow','ΔW_E','W_PL','W_crew'],
            'Value (lbs)': [
                f"{Wto:,.2f}", f"{RR['Mff']:.6f}",
                f"{WF:,.2f}", f"{RR['WFu']:,.2f}", f"{Wtfo_r:,.2f}",
                f"{WOE:,.2f}", f"{WE:,.2f}", f"{RR['WEa']:,.2f}",
                f"{RR['diff']:+.2f}", f"{Wpl:,.2f}", f"{Wcrew:,.2f}"
            ],
        })
        st.dataframe(df_sum, hide_index=True, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Design ratios
        st.markdown('<div class="step-block"><div class="step-label">Key Design Ratios</div>', unsafe_allow_html=True)

        ratio_rows = []
        for name, val, typ_lo, typ_hi in [
            ('W_PL / W_TO', Wpl/Wto,   0.10, 0.25),
            ('W_F  / W_TO', WF/Wto,    0.20, 0.45),
            ('W_E  / W_TO', WE/Wto,    0.45, 0.65),
            ('W_PL / W_E',  Wpl/WE,    0.15, 0.40),
        ]:
            ok  = typ_lo <= val <= typ_hi
            chk = '✓' if ok else ('▲' if val > typ_hi else '▼')
            ratio_rows.append({'Ratio': name,
                                'Value': f'{val:.4f}',
                                'Typical': f'{typ_lo:.2f} – {typ_hi:.2f}',
                                'Check': chk})
        st.dataframe(pd.DataFrame(ratio_rows), hide_index=True, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ──────────────────────────────────────────
#  TAB 2  —  Sensitivity (exact HW 2.8)
# ──────────────────────────────────────────
with tab2:
    s1, s2 = st.columns([1, 1], gap="medium")

    with s1:
        st.markdown("""
        <div class="step-block">
          <div class="step-label">Intermediate Sizing Factors — Eq 2.22–2.44</div>
        """, unsafe_allow_html=True)

        for lbl, val, eq, unit in [
            ('C  = 1−(1+M_res)(1−Mff)−M_tfo', S['C'], 'Eq 2.22', ''),
            ('D  = W_PL + W_crew',              S['D'], 'Eq 2.23', 'lbs'),
            ('C(1−B)W_TO − D',                  S['C']*(1-float(B_v))*Wto - S['D'], 'denom.', 'lbs'),
            ('F  = −B·W_TO²·(1+M_res)·Mff / [C·W_TO·(1−B)−D]',
             S['F'], 'Eq 2.44', 'lbs'),
        ]:
            color = '#1B4FD8' if abs(val)>100 else '#374151'
            st.markdown(f"""
            <div class="ph-row">
              <span style="flex:0 0 260px;font-size:0.77rem;
                font-family:'JetBrains Mono',monospace;color:{color}">{lbl}</span>
              <span style="font-family:'JetBrains Mono',monospace;font-size:0.8rem;
                font-weight:600;color:#0D1B2A">{val:,.2f}</span>
              <span style="font-size:0.66rem;color:#6366F1;margin-left:0.4rem">{eq}</span>
            </div>""", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="step-block">
          <div class="step-label">Range Sensitivity — Breguet Partials (Table 2.20)</div>
        """, unsafe_allow_html=True)

        for partial, val, unit, eq in [
            ('∂W_TO/∂Cp  (cruise)', S['dCpR'],  'lbs/(lbs/hp/hr)', 'Eq 2.49'),
            ('∂W_TO/∂η_p (cruise)', S['dnpR'],  'lbs',             'Eq 2.50'),
            ('∂W_TO/∂(L/D)(cruise)',S['dLDR'],  'lbs',             'Eq 2.51'),
            ('∂W_TO/∂R',            S['dR'],    'lbs/nm',          'Eq 2.45'),
        ]:
            v_cls = 'sens-val-neg' if val < 0 else 'sens-val-pos'
            st.markdown(f"""
            <div class="sens-row">
              <span class="sens-partial">{partial}</span>
              <span class="{v_cls}">{val:+,.1f}</span>
              <span class="sens-unit">{unit}</span>
              <span class="sens-eq">{eq}</span>
            </div>""", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with s2:
        st.markdown("""
        <div class="step-block">
          <div class="step-label">Endurance Sensitivity — Breguet Partials (Table 2.20)</div>
        """, unsafe_allow_html=True)

        for partial, val, unit in [
            ('∂W_TO/∂Cp  (loiter)', S['dCpE'], 'lbs/(lbs/hp/hr)'),
            ('∂W_TO/∂η_p (loiter)', S['dnpE'], 'lbs'),
            ('∂W_TO/∂(L/D)(loiter)',S['dLDE'], 'lbs'),
        ]:
            v_cls = 'sens-val-neg' if val < 0 else 'sens-val-pos'
            st.markdown(f"""
            <div class="sens-row">
              <span class="sens-partial">{partial}</span>
              <span class="{v_cls}">{val:+,.1f}</span>
              <span class="sens-unit">{unit}</span>
              <span class="sens-eq">Table 2.20</span>
            </div>""", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div class="step-block">
          <div class="step-label">Range Trade Study — HW 2.8 Part 2</div>
          <div style="font-size:0.8rem;color:#374151;line-height:1.7;margin-bottom:0.6rem">
            Using ∂W_TO/∂R = <b>{S['dR']:+.2f} lbs/nm</b>
          </div>
        """, unsafe_allow_html=True)

        # Delta R examples matching HW
        delta_R_nm = 200  # per HW: "200 nm change"
        dWto = S['dR'] * delta_R_nm
        st.markdown(f"""
          <div class="ph-row">
            <span class="ph-name" style="flex:0 0 180px">Range −{delta_R_nm} nm</span>
            <span class="ph-frac" style="color:#065F46">{-dWto:+,.1f} lbs</span>
            <span class="ph-src">W_TO decreases</span>
          </div>
          <div class="ph-row">
            <span class="ph-name" style="flex:0 0 180px">Range +{delta_R_nm} nm</span>
            <span class="ph-frac" style="color:#B45309">{+dWto:+,.1f} lbs</span>
            <span class="ph-src">W_TO increases</span>
          </div>
          <div style="margin-top:0.5rem">
            <span style="font-size:0.7rem;color:#94A3B8">
              Custom ΔR: use slider below
            </span>
          </div>
        </div>""", unsafe_allow_html=True)

        dR_custom = st.slider("Custom ΔR (nm)", -500, 500, 0, step=25)
        dW_custom = S['dR'] * dR_custom
        if dR_custom != 0:
            direction = "increase" if dR_custom > 0 else "decrease"
            st.markdown(f"""
            <div style="background:{'#FFF7ED' if dR_custom>0 else '#ECFDF5'};
              border-left:3px solid {'#F59E0B' if dR_custom>0 else '#10B981'};
              border-radius:0 7px 7px 0;padding:0.4rem 0.9rem;
              font-family:'JetBrains Mono',monospace;font-size:0.8rem;
              color:{'#92400E' if dR_custom>0 else '#065F46'};margin-top:0.3rem">
              ΔR = {dR_custom:+d} nm  →  ΔW_TO = {dW_custom:+,.1f} lbs
              (W_TO {'increases' if dR_custom>0 else 'decreases'} to ~{Wto+dW_custom:,.0f} lbs)
            </div>""", unsafe_allow_html=True)

        # Tornado chart
        st.markdown('<br>', unsafe_allow_html=True)
        t_lbl = ['Cp·Cruise','η_p·Cruise','L/D·Cruise','ΔR(200nm)',
                 'Cp·Loiter','η_p·Loiter','L/D·Loiter']
        t_val = [S['dCpR'], S['dnpR'], S['dLDR'], S['dR']*200,
                 S['dCpE'], S['dnpE'], S['dLDE']]
        idx = sorted(range(7), key=lambda i: abs(t_val[i]))
        t_lbl = [t_lbl[i] for i in idx]
        t_val  = [t_val[i]  for i in idx]
        fig_t = go.Figure(go.Bar(
            x=t_val, y=t_lbl, orientation='h',
            marker_color=['#1B4FD8' if v >= 0 else '#10B981' for v in t_val],
            marker_line_color='#fff', marker_line_width=0.6,
            text=[f'{abs(v):,.0f} lbs' for v in t_val],
            textposition='outside', textfont=dict(size=9, color='#374151')))
        fig_t.add_vline(x=0, line_color='#CBD5E1', line_width=1)
        fig_t.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='#FAFBFF',
            height=260, showlegend=False,
            margin=dict(l=10, r=60, t=20, b=20),
            font=dict(family='JetBrains Mono', size=9, color='#475569'),
            xaxis=dict(gridcolor='#EEF1F7', linecolor='#E2E8F0', title='ΔW_TO (lbs)',
                       title_font=dict(size=8)),
            yaxis=dict(gridcolor='#EEF1F7', linecolor='#E2E8F0'))
        st.plotly_chart(fig_t, use_container_width=True)

# ──────────────────────────────────────────
#  TAB 3  —  Charts
# ──────────────────────────────────────────
with tab3:
    ch1, ch2 = st.columns(2, gap="medium")

    with ch1:
        # Chart 1: Phase fractions bar
        st.markdown('<div class="sec-div">Mission Phase Weight Fractions</div>', unsafe_allow_html=True)
        phases_l = list(RR['phases'].keys())
        fvals    = [v for v,_,_ in RR['phases'].values()]
        types    = [t for _,t,_ in RR['phases'].values()]
        clrs     = ['#1B4FD8' if t=='Fixed' else '#059669' for t in types]
        cum_p    = [1.0]
        for fv in fvals: cum_p.append(cum_p[-1]*fv)

        fig_m = make_subplots(rows=1, cols=2,
            column_widths=[0.55, 0.45],
            subplot_titles=["Wᵢ/Wᵢ₋₁ per phase", "Cumulative Mff"])
        fig_m.add_trace(go.Bar(x=phases_l, y=fvals, marker_color=clrs,
            marker_line_color='#fff', marker_line_width=0.8,
            text=[f'{v:.4f}' for v in fvals], textposition='outside',
            textfont=dict(size=7.5, color='#374151')), row=1, col=1)
        fig_m.add_trace(go.Scatter(
            x=['Start']+phases_l, y=cum_p, mode='lines+markers',
            line=dict(color='#1B4FD8', width=2),
            marker=dict(color='#0D1B2A', size=4,
                        line=dict(color='#1B4FD8', width=1.5)),
            fill='tozeroy', fillcolor='rgba(27,79,216,0.07)'), row=1, col=2)
        fig_m.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='#FAFBFF',
            height=240, showlegend=False,
            margin=dict(l=40, r=12, t=35, b=36),
            font=dict(family='JetBrains Mono', size=9, color='#475569'))
        fig_m.update_xaxes(gridcolor='#EEF1F7', linecolor='#E2E8F0')
        fig_m.update_yaxes(gridcolor='#EEF1F7', linecolor='#E2E8F0')
        fig_m.update_yaxes(range=[0.78, 1.03], row=1, col=1)
        fig_m.update_yaxes(range=[0.70, 1.05], row=1, col=2)
        fig_m.update_annotations(font_size=8.5, font_color='#475569',
                                  font_family='JetBrains Mono')
        st.plotly_chart(fig_m, use_container_width=True)
        st.markdown('<div style="font-size:0.72rem;color:#94A3B8">Blue = fixed (Raymer T2.1) · Green = Breguet (Eq 2.9 / 2.11)</div>', unsafe_allow_html=True)

        # Chart 3: W_TO vs Range
        st.markdown('<div class="sec-div">W_TO vs Design Range</div>', unsafe_allow_html=True)
        rr_arr = np.linspace(200, min(3000, float(R_nm)*2.5), 55)
        ww_arr = []
        for rv in rr_arr:
            try:
                w, r = solve_Wto({**P, 'R': float(rv)})
                ww_arr.append(w if abs(r['diff'])<50 else float('nan'))
            except:
                ww_arr.append(float('nan'))
        fig_r = go.Figure()
        fig_r.add_trace(go.Scatter(x=rr_arr, y=ww_arr, mode='lines',
            line=dict(color='#1B4FD8', width=2),
            fill='tozeroy', fillcolor='rgba(27,79,216,0.06)'))
        fig_r.add_vline(x=float(R_nm), line_dash='dash',
            line_color='#F59E0B', line_width=1.3,
            annotation_text=f'{int(R_nm)} nm',
            annotation_font_color='#92400E', annotation_font_size=8)
        fig_r.add_scatter(x=[float(R_nm)], y=[Wto], mode='markers',
            marker=dict(color='#F59E0B', size=9,
                        line=dict(color='#fff', width=1.5)), showlegend=False)
        fig_r.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='#FAFBFF',
            height=210, showlegend=False,
            margin=dict(l=50, r=14, t=16, b=42),
            font=dict(family='JetBrains Mono', size=9, color='#475569'),
            xaxis=dict(gridcolor='#EEF1F7', linecolor='#E2E8F0',
                       title='Range (nm)', title_font=dict(size=8)),
            yaxis=dict(gridcolor='#EEF1F7', linecolor='#E2E8F0',
                       title='W_TO (lbs)', title_font=dict(size=8)))
        st.plotly_chart(fig_r, use_container_width=True)

    with ch2:
        # Chart 2: Weight stack
        st.markdown('<div class="sec-div">W_TO Composition</div>', unsafe_allow_html=True)
        fig_p = go.Figure(go.Pie(
            labels=['Empty W_E', 'Usable Fuel', 'Trapped Fuel', 'Crew', 'Payload'],
            values=[WE, RR['WFu'], Wtfo_r, Wcrew, Wpl],
            hole=0.52,
            marker=dict(
                colors=['#1B4FD8','#60A5FA','#BFDBFE','#059669','#34D399'],
                line=dict(color='#fff', width=2)),
            textfont=dict(size=9, family='JetBrains Mono'),
            textinfo='label+percent', rotation=90))
        fig_p.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='JetBrains Mono', color='#475569'),
            showlegend=False, height=265,
            margin=dict(t=10, b=10, l=10, r=10),
            annotations=[dict(
                text=f'<b>{Wto:,.0f}</b><br>lbs',
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=12, color='#0D1B2A', family='JetBrains Mono'))])
        st.plotly_chart(fig_p, use_container_width=True)

        # Chart 4: Weight through mission
        st.markdown('<div class="sec-div">Weight & Fuel Burn Through Mission</div>', unsafe_allow_html=True)
        fv_list = [v for v,_,_ in RR['phases'].values()]
        pl_list = ['Ramp'] + list(RR['phases'].keys())
        cum_w   = [Wto]
        for fv in fv_list: cum_w.append(cum_w[-1]*fv)
        burn_w  = [Wto - c for c in cum_w]

        fig_w = make_subplots(rows=1, cols=2,
            subplot_titles=['Aircraft Weight (lbs)', 'Cumul. Fuel Burn (lbs)'])
        fig_w.add_trace(go.Scatter(
            x=pl_list, y=cum_w, mode='lines+markers',
            line=dict(color='#1B4FD8', width=2),
            marker=dict(color='#0D1B2A', size=4,
                        line=dict(color='#1B4FD8', width=1.5)),
            fill='tozeroy', fillcolor='rgba(27,79,216,0.07)'), row=1, col=1)
        fig_w.add_trace(go.Scatter(
            x=pl_list, y=burn_w, mode='lines+markers',
            line=dict(color='#F59E0B', width=2),
            marker=dict(color='#0D1B2A', size=4,
                        line=dict(color='#F59E0B', width=1.5)),
            fill='tozeroy', fillcolor='rgba(245,158,11,0.07)'), row=1, col=2)
        fig_w.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='#FAFBFF',
            height=210, showlegend=False,
            margin=dict(l=40, r=10, t=32, b=32),
            font=dict(family='JetBrains Mono', size=9, color='#475569'))
        fig_w.update_xaxes(gridcolor='#EEF1F7', linecolor='#E2E8F0')
        fig_w.update_yaxes(gridcolor='#EEF1F7', linecolor='#E2E8F0')
        fig_w.update_annotations(font_size=8, font_color='#475569',
                                  font_family='JetBrains Mono')
        st.plotly_chart(fig_w, use_container_width=True)

# ──────────────────────────────────────────
#  TAB 4  —  Export
# ──────────────────────────────────────────
with tab4:
    ex1, ex2 = st.columns(2, gap="medium")

    with ex1:
        st.markdown('<div class="sec-div">Download — CSV</div>', unsafe_allow_html=True)
        rows = {
            'Parameter': ['W_TO','Mff','W_F','W_F_usable','W_tfo','W_OE',
                          'W_E_tent','W_E_allow','delta_WE','W_PL','W_crew',
                          'Rc_sm','Vm_mph',
                          'dWTO_dCp_R','dWTO_dnp_R','dWTO_dLD_R','dWTO_dR',
                          'dWTO_dCp_E','dWTO_dnp_E','dWTO_dLD_E','F','C','D'],
            'Value': [
                Wto, RR['Mff'], WF, RR['WFu'], Wtfo_r, WOE,
                WE, RR['WEa'], RR['diff'], Wpl, Wcrew,
                RR['Rc'], RR['Vm'],
                S['dCpR'], S['dnpR'], S['dLDR'], S['dR'],
                S['dCpE'], S['dnpE'], S['dLDE'], S['F'], S['C'], S['D']],
            'Units': [
                'lbs','—','lbs','lbs','lbs','lbs','lbs','lbs','lbs','lbs','lbs',
                's.m.','mph',
                'lbs/(lbs/hp/hr)','lbs','lbs','lbs/nm',
                'lbs/(lbs/hp/hr)','lbs','lbs','lbs','—','lbs']
        }
        b = io.StringIO()
        pd.DataFrame(rows).to_csv(b, index=False)
        st.download_button("⬇  Full Results (CSV)", b.getvalue(),
                           "aerosizer_hw28.csv", "text/csv",
                           use_container_width=True)

        st.markdown('<br>', unsafe_allow_html=True)
        # Phase fractions CSV
        phase_names = list(RR['phases'].keys())
        phase_fracs = [f for f,_,_ in RR['phases'].values()]
        phase_types = [t for _,t,_ in RR['phases'].values()]
        phase_refs  = [r for _,_,r in RR['phases'].values()]
        b2 = io.StringIO()
        pd.DataFrame({'Phase': phase_names, 'Wi/Wi-1': phase_fracs,
                      'Type': phase_types, 'Reference': phase_refs}).to_csv(b2, index=False)
        st.download_button("⬇  Phase Fractions (CSV)", b2.getvalue(),
                           "aerosizer_phases.csv", "text/csv",
                           use_container_width=True)

    with ex2:
        st.markdown('<div class="sec-div">Generate PDF — Engineering Report (A4)</div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="font-size:0.8rem;color:#374151;line-height:1.75;margin-bottom:0.8rem">
          Report includes all HW 2.8 sections:<br>
          &nbsp; ① Mission inputs (all sidebar parameters)<br>
          &nbsp; ② Steps 1–6 weight build-up<br>
          &nbsp; ③ Phase fractions table<br>
          &nbsp; ④ Design ratios with range check<br>
          &nbsp; ⑤ Sensitivity partials (Table 2.20)<br>
          &nbsp; ⑥ References
        </div>
        """, unsafe_allow_html=True)

        def make_pdf():
            buf = io.BytesIO()
            doc = SimpleDocTemplate(buf, pagesize=A4,
                leftMargin=2.0*cm, rightMargin=2.0*cm,
                topMargin=2.2*cm, bottomMargin=2.2*cm)
            PW = 17.0*cm

            # ── Colours ──
            C_NAVY  = colors.HexColor('#0D1B2A')
            C_BLUE  = colors.HexColor('#1B4FD8')
            C_SKY   = colors.HexColor('#3B82F6')
            C_GRAY  = colors.HexColor('#475569')
            C_LGRAY = colors.HexColor('#94A3B8')
            C_RULE  = colors.HexColor('#CBD5E1')
            C_FAINT = colors.HexColor('#F8FAFF')
            C_STRIP = colors.HexColor('#EEF4FF')
            C_OK    = colors.HexColor('#065F46')
            C_WARN  = colors.HexColor('#92400E')
            C_WHITE = colors.white
            C_GREEN = colors.HexColor('#D1FAE5')
            C_AMBER = colors.HexColor('#FFF7ED')

            sty = getSampleStyleSheet()
            def ps(nm, **kw):
                return ParagraphStyle(nm, parent=sty['Normal'], **kw)

            sTITLE = ps('TI', fontSize=18, fontName='Helvetica-Bold',
                        textColor=C_NAVY, leading=24, spaceAfter=3)
            sSUB   = ps('SU', fontSize=8, textColor=C_GRAY, leading=12, spaceAfter=2)
            sH1    = ps('H1', fontSize=10, fontName='Helvetica-Bold',
                        textColor=C_BLUE, spaceBefore=10, spaceAfter=4)
            sBODY  = ps('BO', fontSize=8, textColor=C_GRAY, leading=12)
            sMONO  = ps('MO', fontSize=7.5, fontName='Helvetica',
                        textColor=C_BLUE, leading=11)
            sCAP   = ps('CA', fontSize=7, textColor=C_LGRAY, leading=10,
                        spaceBefore=2, spaceAfter=6)
            sSTAT  = ps('ST', fontSize=9, fontName='Helvetica-Bold',
                        textColor=C_OK if conv else C_WARN, spaceAfter=3)

            def tbl_style(hdr=C_NAVY):
                return TableStyle([
                    ('BACKGROUND',   (0,0), (-1,0), hdr),
                    ('TEXTCOLOR',    (0,0), (-1,0), C_WHITE),
                    ('FONTNAME',     (0,0), (-1,0), 'Helvetica-Bold'),
                    ('FONTNAME',     (0,1), (-1,-1),'Helvetica'),
                    ('FONTSIZE',     (0,0), (-1,-1), 7.5),
                    ('LEADING',      (0,0), (-1,-1), 11),
                    ('TEXTCOLOR',    (0,1), (-1,-1), C_GRAY),
                    ('ROWBACKGROUNDS',(0,1),(-1,-1),[C_WHITE, C_FAINT]),
                    ('GRID',         (0,0), (-1,-1), 0.25, C_RULE),
                    ('LINEBELOW',    (0,0), (-1,0),   0.8, C_SKY),
                    ('LEFTPADDING',  (0,0), (-1,-1), 5),
                    ('RIGHTPADDING', (0,0), (-1,-1), 5),
                    ('TOPPADDING',   (0,0), (-1,-1), 3.5),
                    ('BOTTOMPADDING',(0,0), (-1,-1), 3.5),
                    ('VALIGN',       (0,0), (-1,-1), 'MIDDLE'),
                ])

            def rule(w=PW, t=0.4, c=C_RULE):
                return HRFlowable(width=w, thickness=t, color=c,
                                  spaceBefore=3, spaceAfter=3)

            story = []

            # ── Title block ──
            hdr_data = [[
                Paragraph('<b>AEROSIZER</b>', ps('TX',
                    fontSize=17, fontName='Helvetica-Bold',
                    textColor=C_NAVY, leading=20)),
                Paragraph(
                    'DOC: ASP-HW28-001 &nbsp; REV A<br/>'
                    'CLASS: Conceptual / Preliminary<br/>'
                    'STATUS: ' + ('RELEASED ✓' if conv else 'DRAFT ⚠'),
                    ps('TX2', fontSize=7, textColor=C_LGRAY, leading=10,
                       alignment=TA_RIGHT))
            ]]
            hdr_tbl = Table(hdr_data, colWidths=[PW*0.60, PW*0.40])
            hdr_tbl.setStyle(TableStyle([
                ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                ('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),
                ('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0),
            ]))
            story.append(hdr_tbl)
            story.append(HRFlowable(width=PW, thickness=2.5, color=C_BLUE,
                                    spaceBefore=4, spaceAfter=2))
            story.append(Paragraph(
                'Preliminary Aircraft Weight Sizing — Breguet Range/Endurance · '
                'Propeller-Driven · Raymer (2018) Ch.2 — Problem 2.8',
                sSUB))
            story.append(HRFlowable(width=PW, thickness=0.4, color=C_RULE,
                                    spaceBefore=2, spaceAfter=8))

            # ── 1. Inputs ──
            story.append(Paragraph('1   Mission Inputs', sH1))
            story.append(rule())
            CW4 = [PW*0.30, PW*0.17, PW*0.30, PW*0.17]
            t_in = Table([
                ['Parameter','Value','Parameter','Value'],
                ['Passengers', str(int(npax)), 'Design range (nm)', str(int(R_nm))],
                ['Pax body wt (lbs)', str(int(wpax)), 'Loiter endurance (hr)', f'{El:.2f}'],
                ['Baggage wt (lbs)', str(int(wbag)), 'Loiter speed (kts)', str(int(Vl))],
                ['Flight crew', str(int(ncrew)), 'Cruise L/D', f'{LDc:.1f}'],
                ['Cabin attendants', str(int(natt)), 'Loiter L/D', f'{LDl:.1f}'],
                ['Reg. constant A', f'{A_v:.4f}', 'Cruise Cp (lbs/hp/hr)', f'{Cpc:.2f}'],
                ['Reg. constant B', f'{B_v:.4f}', 'Loiter Cp (lbs/hp/hr)', f'{Cpl:.2f}'],
                ['M_tfo', f'{Mtfo:.3f}', 'Cruise η_p', f'{npc:.2f}'],
                ['M_res', f'{Mres:.3f}', 'Loiter η_p', f'{npl:.2f}'],
            ], colWidths=CW4)
            t_in.setStyle(tbl_style())
            story += [t_in, Spacer(1, 0.2*cm)]

            # ── 2. Steps 1-6 ──
            story.append(Paragraph('2   Sizing Steps 1 – 6  (Raymer §2.3)', sH1))
            story.append(rule())

            # Step 1 payload
            story.append(Paragraph('Step 1 — Payload & Crew', ps('SH',
                fontSize=8.5, fontName='Helvetica-Bold',
                textColor=C_NAVY, spaceBefore=4, spaceAfter=2)))
            CWS1 = [PW*0.52, PW*0.24, PW*0.20]
            t_pl = Table([
                ['Item', 'Weight (lbs)', 'Notes'],
                [f'{npax} pax × ({int(wpax)}+{int(wbag)}) lbs', f'{int(npax)*(int(wpax)+int(wbag)):,}', 'cabin payload'],
                [f'{ncrew} pilots × 205 lbs', f'{int(ncrew)*205:,}', 'flight crew'],
                [f'{natt} attendant × 200 lbs', f'{int(natt)*200:,}', 'cabin crew'],
                ['W_PL  (total payload)', f'{Wpl:,.0f}', ''],
                ['W_crew', f'{Wcrew:,.0f}', ''],
                ['W_tfo = M_tfo × W_TO', f'{Wtfo_r:,.2f}', f'= {Mtfo:.3f} × {Wto:,.0f}'],
            ], colWidths=CWS1)
            t_pl.setStyle(tbl_style(hdr=colors.HexColor('#334155')))
            story += [t_pl, Spacer(1, 0.12*cm)]

            # Step 3 phases
            story.append(Paragraph('Step 3 — Phase Weight Fractions', ps('SH',
                fontSize=8.5, fontName='Helvetica-Bold',
                textColor=C_NAVY, spaceBefore=4, spaceAfter=2)))
            cum_ph = 1.0
            CWP = [PW*0.24, PW*0.15, PW*0.15, PW*0.18, PW*0.24]
            ph_rows = [['Phase','Wᵢ/Wᵢ₋₁','Cumul.','Type','Source']]
            for ph,(fv,ftype,fsrc) in RR['phases'].items():
                cum_ph *= fv
                ph_rows.append([ph, f'{fv:.5f}', f'{cum_ph:.5f}', ftype, fsrc])
            t_ph = Table(ph_rows, colWidths=CWP)
            t_ph.setStyle(tbl_style(hdr=colors.HexColor('#1B4FD8')))
            # Highlight Breguet rows green
            for ri, row in enumerate(ph_rows[1:], start=1):
                if row[3] == 'Breguet':
                    t_ph.setStyle(TableStyle([
                        ('BACKGROUND', (0,ri),(-1,ri), colors.HexColor('#ECFDF5')),
                        ('TEXTCOLOR',  (3,ri),(3,ri),  colors.HexColor('#065F46')),
                        ('FONTNAME',   (0,ri),(-1,ri), 'Helvetica-Bold'),
                    ]))
            story += [t_ph,
                      Paragraph(f'Mff = {RR["Mff"]:.6f}  (product of all 8 phases)',
                                 ps('MF', fontSize=8, fontName='Helvetica-Bold',
                                    textColor=C_BLUE, spaceBefore=3, spaceAfter=4))]

            # Steps 4-6
            story.append(Paragraph('Steps 4–6 — Weight Build-Up & Convergence', ps('SH',
                fontSize=8.5, fontName='Helvetica-Bold',
                textColor=C_NAVY, spaceBefore=4, spaceAfter=2)))
            CWC = [PW*0.44, PW*0.22, PW*0.28]
            t_conv = Table([
                ['Quantity','Value (lbs)','Expression'],
                ['W_F (total fuel)', f'{WF:,.2f}', 'W_Fused + W_tfo'],
                ['W_OE (tentative)', f'{WOE:,.2f}', 'W_TO − W_F − W_PL'],
                ['W_E (tentative)',  f'{WE:,.2f}',  'W_OE − W_tfo − W_crew'],
                ['W_E (allowable)',  f'{RR["WEa"]:,.2f}', '10^[(log W_TO − A)/B]'],
                ['ΔW_E  (convergence)', f'{RR["diff"]:+.2f}', 'W_E_allow − W_E_tent'],
            ], colWidths=CWC)
            t_conv.setStyle(tbl_style(hdr=colors.HexColor('#334155')))
            # Last row highlight
            last_bg = C_GREEN if conv else C_AMBER
            last_tc = C_OK   if conv else C_WARN
            t_conv.setStyle(TableStyle([
                ('BACKGROUND', (0,5),(-1,5), last_bg),
                ('TEXTCOLOR',  (1,5),(1,5),  last_tc),
                ('FONTNAME',   (0,5),(-1,5), 'Helvetica-Bold'),
            ]))
            story += [t_conv, Spacer(1, 0.12*cm),
                      Paragraph('CONVERGED ✓' if conv else 'NOT CONVERGED ⚠', sSTAT)]

            # ── 3. Design ratios ──
            story.append(Paragraph('3   Key Design Ratios', sH1))
            story.append(rule())
            CWR = [PW*0.26, PW*0.17, PW*0.25, PW*0.15, PW*0.13]
            ratio_data = [['Ratio','Value','Typical','Check','']]
            for name, val_r, lo_r, hi_r in [
                ('W_PL / W_TO', Wpl/Wto,   0.10, 0.25),
                ('W_F  / W_TO', WF/Wto,    0.20, 0.45),
                ('W_E  / W_TO', WE/Wto,    0.45, 0.65),
                ('W_PL / W_E',  Wpl/WE,    0.15, 0.40),
            ]:
                ok_r = lo_r <= val_r <= hi_r
                chk  = '✓' if ok_r else ('▲' if val_r > hi_r else '▼')
                ratio_data.append([name, f'{val_r:.4f}',
                                   f'{lo_r:.2f} – {hi_r:.2f}', chk, ''])
            t_r = Table(ratio_data, colWidths=CWR)
            t_r.setStyle(tbl_style())
            story += [t_r, Spacer(1, 0.15*cm)]

            # ── 4. Sensitivity ──
            story.append(Paragraph('4   Sensitivity Analysis  (Raymer Table 2.20)', sH1))
            story.append(rule())
            CWP2 = [PW*0.32, PW*0.16, PW*0.34, PW*0.14]

            sens_rows = [['Partial Derivative','Value','Units','Ref.']] + [
                ('∂W_TO/∂Cp  (cruise)', f'{S["dCpR"]:+,.1f}', 'lbs/(lbs/hp/hr)', 'Eq 2.49'),
                ('∂W_TO/∂η_p (cruise)', f'{S["dnpR"]:+,.1f}', 'lbs',             'Eq 2.50'),
                ('∂W_TO/∂(L/D) (cruise)',f'{S["dLDR"]:+,.1f}','lbs',             'Eq 2.51'),
                ('∂W_TO/∂R',            f'{S["dR"]:+,.2f}',   'lbs/nm',          'Eq 2.45'),
                ('∂W_TO/∂Cp  (loiter)', f'{S["dCpE"]:+,.1f}', 'lbs/(lbs/hp/hr)', 'T2.20'),
                ('∂W_TO/∂η_p (loiter)', f'{S["dnpE"]:+,.1f}', 'lbs',             'T2.20'),
                ('∂W_TO/∂(L/D) (loiter)',f'{S["dLDE"]:+,.1f}','lbs',             'T2.20'),
            ]
            t_s = Table(sens_rows, colWidths=CWP2)
            t_s.setStyle(tbl_style(hdr=colors.HexColor('#1B4FD8')))
            # Colour negative values (favourable) green
            for ri, row in enumerate(sens_rows[1:], start=1):
                try:
                    if float(row[1].replace(',','').replace('+','')) < 0:
                        t_s.setStyle(TableStyle([
                            ('TEXTCOLOR',(1,ri),(1,ri), colors.HexColor('#065F46')),
                        ]))
                except: pass
            story += [t_s, Spacer(1, 0.15*cm)]

            # ── 5. References ──
            story.append(Paragraph('5   References', sH1))
            story.append(rule())
            CWF = [PW*0.08, PW*0.92]
            refs = [
                ['[1]','Raymer, D.P. (2018). Aircraft Design: A Conceptual Approach, 6th Ed. AIAA. — Primary reference for all equations (Ch.2).'],
                ['[2]','Roskam, J. (2003). Airplane Design, Part I. DAR Corporation. — Table 2.2 regression constants cross-reference.'],
                ['[3]','Breguet, L. (1923). Calcul du Poids de Combustible. Comptes Rendus. — Original range/endurance equations.'],
            ]
            t5 = Table([['Ref.','Citation']] + refs, colWidths=CWF)
            t5.setStyle(tbl_style(hdr=colors.HexColor('#334155')))
            story.append(t5)
            story.append(Spacer(1, 0.3*cm))
            story.append(HRFlowable(width=PW, thickness=0.5, color=C_RULE))
            story.append(Paragraph(
                'NOTE: Conceptual-level sizing only. Not for regulatory or structural use. '
                'All weights in lbs (avoirdupois). Breguet Eq. 2.9/2.11 valid for propeller aircraft only.',
                ps('DIS', fontSize=6.5, textColor=C_LGRAY, leading=9.5, spaceBefore=3)))

            doc.build(story)
            buf.seek(0)
            return buf.read()

        st.download_button("⬇  Generate & Download PDF (A4)",
                           make_pdf(), "aerosizer_hw28_report.pdf",
                           "application/pdf", use_container_width=True)

# ──────────────────────────────────────────
#  TAB 5  —  References
# ──────────────────────────────────────────
with tab5:
    st.markdown('<div class="sec-div">Equations Used in This Tool</div>', unsafe_allow_html=True)
    r1, r2 = st.columns(2, gap="medium")
    with r1:
        for code, title, eq, desc in [
            ("Eq 2.9",  "Cruise Weight Fraction — Breguet Propeller",
             "W₅/W₄ = 1 / exp[ Rc / (375·η_p/Cp·L/D) ]",
             "Rc in statute miles, Cp in lbs/hp/hr, η_p = propeller efficiency."),
            ("Eq 2.11", "Loiter Weight Fraction — Breguet Endurance",
             "W₆/W₅ = 1 / exp[ E / (375·(1/V)·η_p/Cp·L/D) ]",
             "E in hours, V in mph. Reserve fuel calculation."),
            ("Eq 2.22", "C factor",
             "C = 1 − (1+M_res)(1−Mff) − M_tfo", ""),
            ("Eq 2.23", "D factor",
             "D = W_PL + W_crew", ""),
        ]:
            st.markdown(f"""<div class="step-block">
            <div class="step-label">{code} — {title}</div>
            <div class="eq-box">{eq}</div>
            <div style="font-size:0.72rem;color:#94A3B8;margin-top:0.3rem">{desc}</div>
            </div>""", unsafe_allow_html=True)
    with r2:
        for code, title, eq, desc in [
            ("Eq 2.44", "Sizing multiplier F",
             "F = −B·W_TO²·(1+M_res)·Mff / [C·W_TO·(1−B) − D]", ""),
            ("Eq 2.45", "∂W_TO / ∂R",
             "∂W_TO/∂R = F·Cp / (375·η_p·L/D)", "lbs/nm"),
            ("Eq 2.49", "∂W_TO / ∂Cp  (cruise)",
             "∂W_TO/∂Cp = F·R / (375·η_p·L/D)", "lbs/(lbs/hp/hr)"),
            ("Eq 2.50/51","∂W_TO / ∂η_p and ∂(L/D)",
             "∂/∂η_p = −F·R·Cp/(375·η_p²·L/D)   ∂/∂(L/D) = −F·R·Cp/(375·η_p·(L/D)²)",
             "Negative values = design levers that reduce W_TO (favourable)."),
        ]:
            st.markdown(f"""<div class="step-block">
            <div class="step-label">{code} — {title}</div>
            <div class="eq-box">{eq}</div>
            <div style="font-size:0.72rem;color:#94A3B8;margin-top:0.3rem">{desc}</div>
            </div>""", unsafe_allow_html=True)
