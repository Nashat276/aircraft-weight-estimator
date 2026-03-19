# app.py (modified per request: remove Charts tab, improve tables & PDF)
import streamlit as st
import numpy as np
import pandas as pd
import math, io
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                 Table, TableStyle, HRFlowable)
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER
import plotly.graph_objects as go

# Page config
st.set_page_config(page_title="AeroSizer Pro", page_icon="✈", layout="wide",
                   initial_sidebar_state="expanded")

# Keep original CSS (unchanged)
CSS = """..."""  # Use your original CSS block here (too long to repeat)
st.markdown(CSS, unsafe_allow_html=True)

# Physics functions (unchanged)
def compute_mission(p):
    Wpl   = p['npax'] * (p['wpax'] + p['wbag'])
    Wcrew = (p['ncrew'] + p['natt']) * 205
    Wtfo  = p['Wto'] * p['Mtfo']
    Rc    = p['R']   * 1.15078
    Vm    = p['Vl']  * 1.15078
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

# Sidebar inputs (unchanged)
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

# Compute
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

# Sidebar live results (unchanged display)
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

# Main header (unchanged)
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

if conv:
    st.markdown(f'<div class="status-ok">✓ &nbsp;W_TO = {Wto:,.1f} lbs &nbsp;·&nbsp; Mff = {RR["Mff"]:.6f} &nbsp;·&nbsp; W_E_tent = {WE:,.1f} lbs &nbsp;·&nbsp; W_E_allow = {RR["WEa"]:,.1f} lbs &nbsp;·&nbsp; ΔW_E = {RR["diff"]:+.2f} lbs</div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div class="status-err">⚠ &nbsp;Not converged — ΔW_E = {RR["diff"]:+.0f} lbs. Adjust A, B constants or inputs.</div>', unsafe_allow_html=True)

# KPI row (unchanged)
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

# Tabs: remove Charts tab; keep Sizing, Sensitivity (no heavy plots), Export, References
tab1, tab2, tab4, tab5 = st.tabs([
    " ✦ Sizing Steps ",
    " ∂ Sensitivity ",
    " ⬇ Export ",
    " ⊕ References "
])

# TAB 1 — Sizing Steps (improve weight build-up table)
with tab1:
    col_l, col_r = st.columns([3, 2], gap="medium")

    with col_l:
        # Steps 1..3 same as original (omitted here for brevity) — keep your existing HTML blocks
        # ...
        # After Steps content, present improved Weight Build-Up table (clear units + totals)
        st.markdown('<div class="card card-green"><div class="card-title">Weight Build-Up</div>', unsafe_allow_html=True)
        # Compose breakdown consistent with RR
        breakdown = {
            'W_TO (solution)': Wto,
            'W_F (total fuel)': WF,
            'W_F_usable': RR['WFu'],
            'W_tfo (trapped fuel)': Wtfo_r,
            'W_PL (payload)': Wpl,
            'W_crew': Wcrew,
            'W_OE (operating empty)': WOE,
            'W_E (tentative empty)': WE,
            'W_E (allowable)': RR['WEa'],
        }
        df_w = pd.DataFrame([
            {'Component': k, 'Weight (lbs)': float(v)} for k, v in breakdown.items()
        ])
        df_w['Weight (lbs)'] = df_w['Weight (lbs)'].map(lambda x: f'{x:,.2f}')
        st.dataframe(df_w, hide_index=True, use_container_width=True, height=320)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_r:
        # Equations and summary table kept (same as original)
        # recreate df_sum as before and display
        df_sum = pd.DataFrame({
            'Symbol': ['W_TO','Mff','W_F','W_F_used','W_tfo','W_OE','W_E_tent','W_E_allow','ΔW_E','W_PL','W_crew'],
            'Value':  [f"{Wto:,.1f}", f"{RR['Mff']:.6f}", f"{WF:,.1f}", f"{RR['WFu']:,.1f}",
                       f"{Wtfo_r:,.2f}", f"{WOE:,.1f}", f"{WE:,.2f}", f"{RR['WEa']:,.2f}",
                       f"{RR['diff']:+.2f}", f"{Wpl:,.1f}", f"{Wcrew:,.1f}"],
            'Unit':   ['lbs','—','lbs','lbs','lbs','lbs','lbs','lbs','lbs','lbs','lbs']})
        st.dataframe(df_sum, hide_index=True, use_container_width=True, height=410)

# TAB 2 — Sensitivity (no heavy plots, numeric tables only)
with tab2:
    s1, s2 = st.columns([1,1], gap="medium")
    with s1:
        st.markdown('<div class="card card-gold"><div class="card-title">Intermediate Factors</div>', unsafe_allow_html=True)
        st.markdown(f"<div style='padding:.5rem 0'><b>C</b> = {S['C']:.5f} &nbsp;&nbsp; <b>D</b> = {S['D']:.0f} lbs &nbsp;&nbsp; <b>F</b> = {S['F']:+.2f}</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card card-blue"><div class="card-title">Cruise Sensitivities</div>', unsafe_allow_html=True)
        sens_table = pd.DataFrame([
            ['∂W_TO/∂Cp (cruise)', S['dCpR'], 'lbs/(lbs/hp/hr)', 'Eq 2.49'],
            ['∂W_TO/∂η_p (cruise)',S['dnpR'], 'lbs', 'Eq 2.50'],
            ['∂W_TO/∂(L/D) cruise',S['dLDR'], 'lbs', 'Eq 2.51'],
            ['∂W_TO/∂R', S['dR'], 'lbs/nm', 'Eq 2.45'],
        ], columns=['Partial','Value','Units','Eq'])
        sens_table['Value'] = sens_table['Value'].map(lambda x: f'{x:+,.2f}')
        st.dataframe(sens_table, hide_index=True, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with s2:
        st.markdown('<div class="card card-amber"><div class="card-title">Loiter Sensitivities</div>', unsafe_allow_html=True)
        sens_table2 = pd.DataFrame([
            ['∂W_TO/∂Cp (loiter)',  S['dCpE'], 'lbs/(lbs/hp/hr)', 'Eq 2.49'],
            ['∂W_TO/∂η_p (loiter)', S['dnpE'], 'lbs', 'Eq 2.50'],
            ['∂W_TO/∂(L/D) loiter',S['dLDE'], 'lbs', 'Eq 2.51'],
        ], columns=['Partial','Value','Units','Eq'])
        sens_table2['Value'] = sens_table2['Value'].map(lambda x: f'{x:+,.2f}')
        st.dataframe(sens_table2, hide_index=True, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# TAB 4 — EXPORT (improved PDF generation and CSV)
with tab4:
    ex1, ex2 = st.columns([1,1], gap="medium")
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
        st.dataframe(df_export, hide_index=True, use_container_width=True)
        b = io.StringIO()
        df_export.to_csv(b, index=False)
        st.download_button("⬇  Full Results (CSV)", b.getvalue(),
                           "aerosizer_results.csv", "text/csv",
                           use_container_width=True)

    with ex2:
        st.markdown('<div class="sec-div">PDF Report</div>', unsafe_allow_html=True)

        def make_pdf_bytes():
            buf = io.BytesIO()
            doc = SimpleDocTemplate(buf, pagesize=A4,
                leftMargin=2.0*cm, rightMargin=2.0*cm,
                topMargin=2.2*cm,  bottomMargin=2.2*cm)
            PW = 17.0*cm
            sty = getSampleStyleSheet()
            def ps(nm, **kw):
                return ParagraphStyle(nm, parent=sty['Normal'], **kw)

            sH1  = ps('H1',  fontSize=11, fontName='Helvetica-Bold', textColor=colors.HexColor('#c8a86c'), spaceBefore=8, spaceAfter=4)
            sSUB = ps('SU',  fontSize=8,  textColor=colors.HexColor('#94A3B8'), leading=12, spaceAfter=2)
            sEQ  = ps('EQ',  fontSize=8,  fontName='Courier', textColor=colors.HexColor('#6a9eea'), leading=12, spaceAfter=3)

            def ts(hdr=colors.HexColor('#0D1B2A'), alt=colors.white):
                return TableStyle([
                    ('BACKGROUND',  (0,0), (-1,0),  hdr),
                    ('TEXTCOLOR',   (0,0), (-1,0),  colors.white),
                    ('FONTNAME',    (0,0), (-1,0),  'Helvetica-Bold'),
                    ('FONTNAME',    (0,1), (-1,-1), 'Helvetica'),
                    ('FONTSIZE',    (0,0), (-1,-1), 8),
                    ('LEADING',     (0,0), (-1,-1), 11),
                    ('TEXTCOLOR',   (0,1), (-1,-1), colors.HexColor('#475569')),
                    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, alt]),
                    ('GRID',        (0,0), (-1,-1), 0.25, colors.HexColor('#E2E8F0')),
                    ('LEFTPADDING', (0,0), (-1,-1), 6),
                    ('RIGHTPADDING',(0,0), (-1,-1), 6),
                    ('TOPPADDING',  (0,0), (-1,-1), 4),
                    ('BOTTOMPADDING',(0,0),(-1,-1), 4),
                    ('VALIGN',      (0,0), (-1,-1), 'MIDDLE'),
                ])

            story = []
            # Header
            story.append(Paragraph('AeroSizer Pro — Raymer Ch.2', sH1))
            story.append(Paragraph(f'STATUS: {"CONVERGED" if conv else "DRAFT"} · W_TO = {Wto:,.1f} lbs', sSUB))
            story.append(Spacer(1, 6))

            # Inputs table
            story.append(Paragraph('Mission Inputs', ps('h', fontSize=9, fontName='Helvetica-Bold')))
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
            t_in.setStyle(ts()); story.append(t_in)
            story.append(Spacer(1, 8))

            # Sizing results table (clear ordering)
            story.append(Paragraph('Sizing Results', ps('h', fontSize=9, fontName='Helvetica-Bold')))
            t_res = Table([
                ['Quantity', 'Value (lbs)', 'Notes'],
                ['W_TO (Gross Takeoff)', f'{Wto:,.2f}', 'Sizing solution'],
                ['W_F (Total Fuel)',     f'{WF:,.2f}',  'W_Fused + W_tfo'],
                ['W_F_used',            f'{RR["WFu"]:,.2f}', 'W_TO(1−Mff)'],
                ['W_tfo (Trapped)',      f'{Wtfo_r:,.2f}', f'M_tfo × W_TO'],
                ['W_OE (Operating)',     f'{WOE:,.2f}', 'W_TO − W_F − W_PL'],
                ['W_E (Tentative)',      f'{WE:,.2f}',  'W_OE − W_tfo − W_crew'],
                ['W_E (Allowable)',      f'{RR["WEa"]:,.2f}', '10^[(log W_TO − A)/B]'],
                ['ΔW_E (Convergence)',   f'{RR["diff"]:+.2f}', 'W_E_allow − W_E_tent'],
            ], colWidths=[PW*0.35, PW*0.2, PW*0.45])
            t_res.setStyle(ts()); story.append(t_res)
            story.append(Spacer(1, 8))

            # Sensitivity small table
            story.append(Paragraph('Sensitivity — Key Partials', ps('h', fontSize=9, fontName='Helvetica-Bold')))
            sens_data = [['Partial','Value','Units'],
                         ['∂W_TO/∂Cp (cruise)', f'{S["dCpR"]:+,.2f}', 'lbs/(lbs/hp/hr)'],
                         ['∂W_TO/∂η_p (cruise)', f'{S["dnpR"]:+,.2f}', 'lbs'],
                         ['∂W_TO/∂(L/D) cruise', f'{S["dLDR"]:+,.2f}', 'lbs'],
                         ['∂W_TO/∂R', f'{S["dR"]:+,.2f}', 'lbs/nm']]
            t_sen = Table(sens_data, colWidths=[PW*0.45, PW*0.25, PW*0.25])
            t_sen.setStyle(ts()); story.append(t_sen)

            # Footer
            story.append(Spacer(1, 10))
            story.append(HRFlowable(width=PW, thickness=0.4, color=colors.HexColor('#c8a86c')))
            story.append(Paragraph('Generated by AeroSizer Pro · Raymer (2018)', ps('f', fontSize=7, textColor=colors.HexColor('#94A3B8'), alignment=TA_CENTER)))
            doc.build(story)
            buf.seek(0)
            return buf.read()

        st.download_button(
            "⬇  Generate & Download PDF (A4)", make_pdf_bytes(),
            "aerosizer_report.pdf", "application/pdf",
            use_container_width=True)

# TAB 5 — REFERENCES (kept)
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
