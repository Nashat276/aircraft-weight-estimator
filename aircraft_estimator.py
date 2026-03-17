import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import math, io
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.units import inch, cm

st.set_page_config(
    page_title="AeroSizer Pro — Aircraft Weight Estimation",
    page_icon="✈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"] {
    background: #F0F2F5 !important;
    color: #0A0E1A !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
}
.stApp { background: #F0F2F5 !important; }

/* ── TOP HEADER BAR ── */
.header-bar {
    background: #0A1628;
    border-radius: 12px;
    padding: 1rem 1.6rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.4rem;
}
.header-logo {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.25rem;
    font-weight: 600;
    color: #FFFFFF;
    letter-spacing: .06em;
}
.header-logo span { color: #3B82F6; }
.header-sub {
    font-size: .72rem;
    color: #94A3B8;
    letter-spacing: .14em;
    text-transform: uppercase;
    margin-top: .15rem;
    font-family: 'IBM Plex Mono', monospace;
}
.header-badge {
    background: #1E3A5F;
    color: #60A5FA;
    font-size: .68rem;
    font-family: 'IBM Plex Mono', monospace;
    letter-spacing: .1em;
    padding: .35rem .8rem;
    border-radius: 6px;
    border: 1px solid #2563EB40;
}

/* ── STATUS BANNERS ── */
.ok-bar {
    background: #F0FDF4;
    border: 1px solid #16A34A50;
    border-left: 4px solid #16A34A;
    border-radius: 8px;
    padding: .6rem 1.1rem;
    font-family: 'IBM Plex Mono', monospace;
    font-size: .8rem;
    color: #15803D;
    margin-bottom: 1.2rem;
}
.warn-bar {
    background: #FFF7ED;
    border: 1px solid #EA580C50;
    border-left: 4px solid #EA580C;
    border-radius: 8px;
    padding: .6rem 1.1rem;
    font-family: 'IBM Plex Mono', monospace;
    font-size: .8rem;
    color: #C2410C;
    margin-bottom: 1.2rem;
}

/* ── KPI CARDS ── */
.kpi-row { display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; margin-bottom: 1.4rem; }
.kpi {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    padding: 1rem 1.1rem;
    border-top: 3px solid #3B82F6;
}
.kpi-v {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.45rem;
    font-weight: 600;
    color: #0A1628;
    line-height: 1.1;
}
.kpi-u { font-size: .75rem; color: #64748B; margin-left: .2rem; font-weight: 400; }
.kpi-l { font-size: .65rem; color: #94A3B8; letter-spacing: .1em; margin-top: .3rem; text-transform: uppercase; }

/* ── SECTION CARDS ── */
.sec-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1rem;
}
.sec-title {
    font-size: .72rem;
    font-weight: 600;
    color: #3B82F6;
    letter-spacing: .14em;
    text-transform: uppercase;
    padding-bottom: .6rem;
    border-bottom: 1px solid #F1F5F9;
    margin-bottom: .9rem;
    font-family: 'IBM Plex Mono', monospace;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: #FFFFFF !important;
    border-right: 1px solid #E2E8F0 !important;
}
[data-testid="stSidebar"] .stSlider > label {
    font-size: .78rem !important;
    color: #374151 !important;
    font-weight: 500 !important;
}
.sidebar-section {
    font-size: .65rem;
    font-weight: 600;
    color: #3B82F6;
    letter-spacing: .16em;
    text-transform: uppercase;
    padding: .5rem 0 .4rem 0;
    border-bottom: 1px solid #E2E8F0;
    margin: .6rem 0 .7rem 0;
    font-family: 'IBM Plex Mono', monospace;
}
.sidebar-logo {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.05rem;
    font-weight: 600;
    color: #0A1628;
    letter-spacing: .05em;
    padding-bottom: .3rem;
}
.sidebar-logo span { color: #3B82F6; }
.sidebar-tag {
    font-size: .62rem;
    color: #94A3B8;
    letter-spacing: .15em;
    text-transform: uppercase;
    font-family: 'IBM Plex Mono', monospace;
    margin-bottom: 1rem;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: #FFFFFF;
    border-radius: 8px;
    padding: 3px;
    border: 1px solid #E2E8F0;
    gap: 2px;
    margin-bottom: 1rem;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 6px;
    font-size: .78rem;
    font-weight: 500;
    color: #64748B;
    padding: .4rem 1.1rem;
    font-family: 'IBM Plex Sans', sans-serif;
}
.stTabs [aria-selected="true"] {
    background: #0A1628 !important;
    color: #FFFFFF !important;
}

/* ── DATAFRAME ── */
[data-testid="stDataFrame"] { border-radius: 8px; overflow: hidden; }

/* ── DOWNLOAD BUTTON ── */
div.stDownloadButton > button {
    background: #0A1628 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
    font-size: .8rem !important;
    font-weight: 500 !important;
    padding: .55rem 1rem !important;
    width: 100% !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
    letter-spacing: .02em !important;
}
div.stDownloadButton > button:hover {
    background: #1E3A5F !important;
}

/* ── DIVIDER ── */
.div-line { height: 1px; background: #E2E8F0; margin: .8rem 0; }

/* ── PHASE TAG ── */
.phase-tag {
    display: inline-block;
    background: #EFF6FF;
    color: #1D4ED8;
    font-size: .65rem;
    font-family: 'IBM Plex Mono', monospace;
    padding: .15rem .5rem;
    border-radius: 4px;
    border: 1px solid #BFDBFE;
    margin: 1px;
}
</style>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════
# PLOTLY THEME — LIGHT PROFESSIONAL
# ZERO xaxis/yaxis in update_layout
# ════════════════════════════════════════════════
_BASE = dict(
    paper_bgcolor='rgba(255,255,255,0)',
    plot_bgcolor='#FAFBFC',
    font=dict(family='IBM Plex Mono', color='#374151', size=10),
    margin=dict(l=52, r=16, t=38, b=42),
    hoverlabel=dict(bgcolor='#0A1628', font_color='#FFFFFF', font_size=11,
                    font_family='IBM Plex Mono', bordercolor='#0A1628'),
)
_AX = dict(gridcolor='#F1F5F9', linecolor='#E2E8F0',
           zerolinecolor='#E2E8F0', showgrid=True)

def pset(fig, title='', h=300, xt='', yt='', yr=None):
    kw = dict(_BASE)
    if title:
        kw['title'] = dict(text=title,
                           font=dict(color='#0A1628', size=11,
                                     family='IBM Plex Mono'),
                           x=0.01, pad=dict(l=2))
    kw['height'] = h
    fig.update_layout(**kw)
    fig.update_xaxes(**_AX)
    fig.update_yaxes(**_AX)
    if xt: fig.update_xaxes(title_text=xt, title_font=dict(size=9, color='#64748B'))
    if yt: fig.update_yaxes(title_text=yt, title_font=dict(size=9, color='#64748B'))
    if yr: fig.update_yaxes(range=yr)
    return fig


# ════════════════════════════════════════════════
# PHYSICS ENGINE
# ════════════════════════════════════════════════
def mission(p):
    Wpl   = p['npax']*(p['wpax']+p['wbag']) + p['ncrew']*205 + p['natt']*200
    Wcrew = p['ncrew']*205 + p['natt']*200
    Wtfo  = p['Wto']*p['Mtfo']
    Rc    = p['R']*1.15078
    W5    = 1/math.exp(Rc / (375*(p['npc']/p['Cpc'])*p['LDc']))
    Vm    = p['Vl']*1.15078
    W6    = 1/math.exp(p['El'] / (375*(1/Vm)*(p['npl']/p['Cpl'])*p['LDl']))
    fnames = ['Engine Start','Taxi','Takeoff','Climb','Cruise','Loiter','Descent','Landing']
    fvals  = [0.990, 0.995, 0.995, 0.985, W5, W6, 0.985, 0.995]
    Mff = 1.0
    for v in fvals: Mff *= v
    WFu  = p['Wto']*(1-Mff)
    WF   = WFu + p['Wto']*p['Mr']*(1-Mff) + Wtfo
    WOE  = p['Wto'] - WF - Wpl
    WE   = WOE - Wtfo - Wcrew
    WEa  = 10**((math.log10(p['Wto'])-p['A'])/p['B'])
    return dict(Wpl=Wpl, Wcrew=Wcrew, Wtfo=Wtfo, Mff=Mff,
                WF=WF, WFu=WFu, WOE=WOE, WE=WE,
                WEa=WEa, diff=WEa-WE, fracs=dict(zip(fnames,fvals)))

def solve(p, tol=0.5, n=400):
    pp = dict(p)
    lo, hi = 5000.0, 500000.0
    # Find a bracket where sign changes
    pp['Wto']=lo; rlo=mission(pp)
    pp['Wto']=hi; rhi=mission(pp)
    if rlo['diff']*rhi['diff'] > 0:
        for w0 in [15000,25000,40000,60000,80000,120000,200000,350000]:
            pp['Wto']=w0; r0=mission(pp)
            if r0['diff']*rhi['diff'] < 0:
                lo=w0; rlo=r0; break
    r = {}
    for _ in range(n):
        m = (lo+hi)/2; pp['Wto']=m; r=mission(pp)
        if abs(r['diff']) < tol: break
        if r['diff'] > 0: hi=m
        else: lo=m
    return m, r

def sensitivity(p, Wto):
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


# ════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════
D = dict(npax=34, wpax=175, wbag=30, ncrew=2, natt=1, Mtfo=0.005, Mr=0.0,
         R=1100, Vl=250, LDc=13, Cpc=0.60, npc=0.85,
         El=0.75, LDl=16, Cpl=0.65, npl=0.77, A=0.3774, B=0.9647)

with st.sidebar:
    st.markdown('<div class="sidebar-logo">AERO<span>SIZER</span> PRO</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-tag">Aircraft Weight Estimation Tool</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">Cabin & Crew</div>', unsafe_allow_html=True)
    npax  = st.slider("Passengers",         10, 150, D['npax'])
    wpax  = st.slider("Passenger wt (lbs)", 140, 230, D['wpax'])
    wbag  = st.slider("Baggage wt (lbs)",   10,  70, D['wbag'])
    ncrew = st.slider("Flight crew",          1,   4, D['ncrew'])
    natt  = st.slider("Cabin attendants",     0,   6, D['natt'])

    st.markdown('<div class="sidebar-section">Cruise Segment</div>', unsafe_allow_html=True)
    R_nm = st.slider("Design range (nm)",  200, 4000, D['R'], step=50)
    LDc  = st.slider("L/D ratio",            8,   24, D['LDc'])
    Cpc  = st.slider("SFC Cp (lbs/hp/hr)", 0.3,  1.0, D['Cpc'], step=0.01)
    npc  = st.slider("Prop efficiency η",  0.50, 0.95, D['npc'], step=0.01)

    st.markdown('<div class="sidebar-section">Loiter / Reserve</div>', unsafe_allow_html=True)
    El   = st.slider("Endurance (hr)",     0.1,  4.0, D['El'], step=0.05)
    Vl   = st.slider("Loiter speed (kts)", 100,  350, D['Vl'])
    LDl  = st.slider("L/D ratio",           8,   26, D['LDl'])
    Cpl  = st.slider("SFC Cp (lbs/hp/hr)", 0.3,  1.0, D['Cpl'], step=0.01)
    npl  = st.slider("Prop efficiency η",  0.50, 0.95, D['npl'], step=0.01)

    st.markdown('<div class="sidebar-section">Regression Constants</div>', unsafe_allow_html=True)
    st.caption("From historical weight data (Raymer Table 2.2)")
    A_v  = st.number_input("A",      value=D['A'],    step=0.001, format="%.4f")
    B_v  = st.number_input("B",      value=D['B'],    step=0.001, format="%.4f")
    Mtfo = st.number_input("M_tfo",  value=D['Mtfo'], step=0.001, format="%.4f")

P = dict(npax=npax, wpax=wpax, wbag=wbag, ncrew=ncrew, natt=natt,
         Mtfo=Mtfo, Mr=0.0, R=R_nm, Vl=Vl, LDc=LDc, Cpc=Cpc, npc=npc,
         El=El, LDl=LDl, Cpl=Cpl, npl=npl, A=A_v, B=B_v, Wto=48550)

Wto, RR = solve(P)
S = sensitivity(P, Wto)

# ════════════════════════════════════════════════
# MAIN CONTENT
# ════════════════════════════════════════════════

# Header bar
st.markdown(f"""
<div class="header-bar">
  <div>
    <div class="header-logo">AERO<span>SIZER</span> PRO</div>
    <div class="header-sub">Preliminary Aircraft Weight Estimation · Breguet Method · Propeller-Driven</div>
  </div>
  <div class="header-badge">Rev. 2025 · Raymer / Roskam Methodology</div>
</div>
""", unsafe_allow_html=True)

# Status
converged = abs(RR['diff']) < 5
if converged:
    st.markdown(f'<div class="ok-bar">✓  Solution converged  ·  W_TO = {Wto:,.0f} lbs  ·  ΔWE = {RR["diff"]:+.2f} lbs  ·  Mff = {RR["Mff"]:.5f}</div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div class="warn-bar">⚠  Solution did not converge  ·  ΔWE = {RR["diff"]:.1f} lbs  ·  Review inputs</div>', unsafe_allow_html=True)

# KPI row
WE=RR['WE']; WOE=RR['WOE']; WF=RR['WF']
Wpl=RR['Wpl']; Wcrew=RR['Wcrew']; Wtfo=RR['Wtfo']

k1,k2,k3,k4,k5 = st.columns(5)
for col,val,unit,lbl in [
    (k1, f"{Wto:,.0f}",       "lbs", "Gross Takeoff Weight"),
    (k2, f"{RR['Mff']:.5f}",  "",    "Mission Fuel Fraction"),
    (k3, f"{WF:,.0f}",        "lbs", "Total Fuel Required"),
    (k4, f"{Wpl:,.0f}",       "lbs", "Payload Weight"),
    (k5, f"{WE:,.0f}",        "lbs", "Empty Weight W_E"),
]:
    with col:
        st.markdown(f'<div class="kpi"><div class="kpi-v">{val}<span class="kpi-u">{unit}</span></div><div class="kpi-l">{lbl}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "  ① Mission Sizing  ",
    "  ② Sensitivity Analysis  ",
    "  ③ Weight Breakdown  ",
    "  ④ Export Report  "
])


# ════════════════════════════════════════════════
# TAB 1 — MISSION SIZING
# ════════════════════════════════════════════════
with tab1:
    L, R_col = st.columns([3, 2], gap="large")

    with L:
        # Phase fractions chart
        st.markdown('<div class="sec-card"><div class="sec-title">Mission Phase Weight Fractions</div>', unsafe_allow_html=True)
        phases = list(RR['fracs'].keys())
        fvals  = list(RR['fracs'].values())
        C_BLUE   = '#3B82F6'
        C_GREEN  = '#10B981'
        bar_clrs = [C_BLUE,C_BLUE,C_BLUE,C_BLUE,C_GREEN,C_GREEN,C_BLUE,C_BLUE]
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=phases, y=fvals,
            marker_color=bar_clrs,
            marker_line_color='#FFFFFF', marker_line_width=1,
            text=[f'{v:.4f}' for v in fvals],
            textposition='outside',
            textfont=dict(size=9, color='#374151'),
        ))
        pset(fig, 'Wi / Wi-1  per phase  (green = variable, blue = fixed)', 280, yr=[0.80, 1.02])
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Range sweep
        st.markdown('<div class="sec-card"><div class="sec-title">Parametric Study — W_TO vs Design Range</div>', unsafe_allow_html=True)
        rr = np.linspace(200, 4000, 55); ww=[]
        for rv in rr:
            try: w,_=solve({**P,'R':float(rv)}); ww.append(w)
            except: ww.append(float('nan'))
        fig3=go.Figure()
        fig3.add_trace(go.Scatter(
            x=rr, y=ww, mode='lines',
            line=dict(color='#3B82F6', width=2.5),
            fill='tozeroy', fillcolor='rgba(59,130,246,0.06)',
            name='W_TO',
        ))
        fig3.add_vline(x=R_nm, line_dash='dash', line_color='#F59E0B', line_width=1.5,
                       annotation_text=f'Design point: {R_nm} nm',
                       annotation_font_color='#92400E', annotation_font_size=9)
        pset(fig3, '', 240, xt='Range (nautical miles)', yt='Gross Takeoff Weight (lbs)')
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with R_col:
        # Gauge
        st.markdown('<div class="sec-card"><div class="sec-title">W_TO Sizing Gauge</div>', unsafe_allow_html=True)
        fig2 = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=Wto,
            delta={'reference': 48550, 'relative': False,
                   'increasing': {'color': '#EF4444'},
                   'decreasing': {'color': '#10B981'},
                   'font': {'size': 13}},
            number={'suffix': ' lbs', 'font': {'color': '#0A1628', 'size': 17,
                                                'family': 'IBM Plex Mono'}},
            gauge={
                'axis': {'range': [0, 120000], 'tickfont': {'size': 8},
                         'tickcolor': '#94A3B8'},
                'bar': {'color': '#3B82F6', 'thickness': 0.22},
                'bgcolor': '#FAFBFC', 'borderwidth': 1, 'bordercolor': '#E2E8F0',
                'steps': [
                    {'range': [0,     40000], 'color': '#F0FDF4'},
                    {'range': [40000, 80000], 'color': '#EFF6FF'},
                    {'range': [80000,120000], 'color': '#FFF7ED'},
                ],
                'threshold': {'line': {'color': '#EF4444', 'width': 2},
                              'thickness': 0.75, 'value': Wto},
            },
            title={'text': 'Gross Takeoff Weight',
                   'font': {'color': '#64748B', 'size': 9, 'family': 'IBM Plex Mono'}},
        ))
        fig2.update_layout(
            paper_bgcolor='rgba(255,255,255,0)',
            font=dict(family='IBM Plex Mono', color='#374151'),
            height=255, margin=dict(t=30, b=5, l=10, r=10))
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Convergence
        st.markdown('<div class="sec-card"><div class="sec-title">Sizing Convergence</div>', unsafe_allow_html=True)
        conv_df = pd.DataFrame({
            'Parameter': ['WE Tentative', 'WE Allowable', 'Difference ΔWE'],
            'Value': [f"{RR['WE']:,.1f} lbs",
                      f"{RR['WEa']:,.1f} lbs",
                      f"{RR['diff']:+.2f} lbs"],
            'Status': ['—', '—',
                       '✓ OK' if converged else '✗ Retry'],
        })
        st.dataframe(conv_df, hide_index=True, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Fraction table
        st.markdown('<div class="sec-card"><div class="sec-title">Phase Weight Fractions</div>', unsafe_allow_html=True)
        phase_df = pd.DataFrame({
            'Phase': list(RR['fracs'].keys()),
            'Wi / Wi-1': [f"{v:.4f}" for v in RR['fracs'].values()],
            'Type': ['Fixed','Fixed','Fixed','Fixed','Variable','Variable','Fixed','Fixed'],
        })
        st.dataframe(phase_df, hide_index=True, use_container_width=True)
        st.markdown(f'<div style="margin-top:.6rem;font-family:IBM Plex Mono;font-size:.8rem;color:#374151">Overall Mff = <b style="color:#3B82F6">{RR["Mff"]:.5f}</b></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════
# TAB 2 — SENSITIVITY
# ════════════════════════════════════════════════
with tab2:
    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown('<div class="sec-card"><div class="sec-title">Range Phase — Breguet Partials (Eq. 2.49–2.51)</div>', unsafe_allow_html=True)
        sdr = {
            'Partial':  ['∂W_TO/∂Cp',  '∂W_TO/∂ηp', '∂W_TO/∂(L/D)', '∂W_TO/∂R'],
            'Value':    [f"{S['dCpR']:+,.1f}", f"{S['dnpR']:+,.1f}",
                         f"{S['dLDR']:+,.1f}", f"{S['dR']:+,.2f}"],
            'Units':    ['lbs / (lbs/hp/hr)', 'lbs', 'lbs', 'lbs / nm'],
            'Equation': ['Eq. 2.49', 'Eq. 2.50', 'Eq. 2.51', 'Eq. 2.45'],
        }
        st.dataframe(pd.DataFrame(sdr), hide_index=True, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="sec-card"><div class="sec-title">Loiter Phase — Breguet Partials</div>', unsafe_allow_html=True)
        sdl = {
            'Partial':  ['∂W_TO/∂Cp',  '∂W_TO/∂ηp', '∂W_TO/∂(L/D)'],
            'Value':    [f"{S['dCpE']:+,.1f}", f"{S['dnpE']:+,.1f}", f"{S['dLDE']:+,.1f}"],
            'Units':    ['lbs / (lbs/hp/hr)', 'lbs', 'lbs'],
            'Equation': ['—', '—', '—'],
        }
        st.dataframe(pd.DataFrame(sdl), hide_index=True, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-card"><div class="sec-title">Tornado Chart — ΔW_TO per Unit Parameter Change</div>', unsafe_allow_html=True)
    tlbl = ['Cp (Range)','ηp (Range)','L/D (Range)','Range R',
            'Cp (Loiter)','ηp (Loiter)','L/D (Loiter)']
    tval = [S['dCpR'], S['dnpR'], S['dLDR'], S['dR']*R_nm*0.1,
            S['dCpE'], S['dnpE'], S['dLDE']]
    idx  = sorted(range(7), key=lambda i: abs(tval[i]))
    tlbl = [tlbl[i] for i in idx]; tval=[tval[i] for i in idx]
    fig_t = go.Figure(go.Bar(
        x=tval, y=tlbl, orientation='h',
        marker_color=['#3B82F6' if v>=0 else '#EF4444' for v in tval],
        marker_line_color='#FFFFFF', marker_line_width=0.5,
        text=[f'{v:+,.0f} lbs' for v in tval],
        textposition='outside', textfont=dict(size=9),
    ))
    fig_t.add_vline(x=0, line_color='#CBD5E1', line_width=1.5)
    pset(fig_t, '', 340, xt='ΔW_TO (lbs)  —  blue = increases W_TO,  red = decreases W_TO')
    st.plotly_chart(fig_t, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-card"><div class="sec-title">3D Parametric Surface — W_TO as a Function of Cp and L/D (Cruise)</div>', unsafe_allow_html=True)
    cpa=np.linspace(0.40,0.90,20); lda=np.linspace(9.0,20.0,20)
    Z=np.zeros((len(cpa),len(lda)))
    for i,cp in enumerate(cpa):
        for j,ld in enumerate(lda):
            try: w,_=solve({**P,'Cpc':float(cp),'LDc':float(ld)}); Z[i,j]=w
            except: Z[i,j]=float('nan')
    fig4=go.Figure(go.Surface(
        x=lda,y=cpa,z=Z,
        colorscale=[[0,'#EFF6FF'],[0.4,'#93C5FD'],[0.75,'#3B82F6'],[1,'#1D4ED8']],
        opacity=0.93,showscale=True,
        colorbar=dict(tickfont=dict(size=8,color='#374151'),len=0.65,thickness=12,
                      title=dict(text='W_TO (lbs)',font=dict(size=9)))))
    fig4.update_layout(
        paper_bgcolor='rgba(255,255,255,0)',
        font=dict(family='IBM Plex Mono',color='#374151',size=9),
        title=dict(text='W_TO surface over SFC (Cp) and Aerodynamic Efficiency (L/D)',
                   font=dict(color='#0A1628',size=11,family='IBM Plex Mono'),x=0.01),
        scene=dict(
            xaxis=dict(title='L/D (cruise)',backgroundcolor='#FAFBFC',
                       gridcolor='#E2E8F0',linecolor='#E2E8F0'),
            yaxis=dict(title='Cp (lbs/hp/hr)',backgroundcolor='#FAFBFC',
                       gridcolor='#E2E8F0',linecolor='#E2E8F0'),
            zaxis=dict(title='W_TO (lbs)',backgroundcolor='#FAFBFC',
                       gridcolor='#E2E8F0',linecolor='#E2E8F0'),
            bgcolor='#F8FAFC',
        ),
        margin=dict(l=0,r=0,t=44,b=0),height=470)
    st.plotly_chart(fig4,use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════
# TAB 3 — WEIGHT BREAKDOWN
# ════════════════════════════════════════════════
with tab3:
    pa, pb = st.columns(2, gap="large")
    with pa:
        st.markdown('<div class="sec-card"><div class="sec-title">W_TO Component Breakdown</div>', unsafe_allow_html=True)
        fig_p = go.Figure(go.Pie(
            labels=['Empty Weight (WE)', 'Usable Fuel', 'Trapped Fuel + Oil',
                    'Crew Weight', 'Payload'],
            values=[WE, RR['WFu'], Wtfo, Wcrew, Wpl],
            hole=0.54,
            marker=dict(
                colors=['#1D4ED8','#3B82F6','#93C5FD','#10B981','#34D399'],
                line=dict(color='#FFFFFF', width=2),
            ),
            textfont=dict(size=10, family='IBM Plex Mono'),
            textinfo='label+percent',
        ))
        fig_p.update_layout(
            paper_bgcolor='rgba(255,255,255,0)',
            font=dict(family='IBM Plex Mono', color='#374151'),
            showlegend=False, height=310,
            margin=dict(t=10, b=10, l=10, r=10),
            annotations=[dict(
                text=f'<b>{Wto:,.0f}</b><br>lbs',
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=13, color='#0A1628', family='IBM Plex Mono')
            )],
        )
        st.plotly_chart(fig_p, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with pb:
        st.markdown('<div class="sec-card"><div class="sec-title">Aircraft Weight Through Mission Phases</div>', unsafe_allow_html=True)
        fv = list(RR['fracs'].values())
        pl = list(RR['fracs'].keys()) + ['End of mission']
        cum = [Wto]
        for f in fv: cum.append(cum[-1]*f)
        fig_w = go.Figure()
        fig_w.add_trace(go.Scatter(
            x=pl, y=cum, mode='lines+markers',
            line=dict(color='#3B82F6', width=2.5),
            marker=dict(color='#1D4ED8', size=7,
                        line=dict(color='#FFFFFF', width=1.5)),
            fill='tozeroy', fillcolor='rgba(59,130,246,0.07)',
            name='Aircraft Weight',
        ))
        pset(fig_w, '', 310, xt='Mission Phase', yt='Aircraft Weight (lbs)')
        st.plotly_chart(fig_w, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-card"><div class="sec-title">Detailed Weight Statement</div>', unsafe_allow_html=True)
    summary = pd.DataFrame({
        'Weight Component': [
            'W_TO  —  Gross Takeoff Weight',
            'W_E   —  Empty Weight',
            'W_OE  —  Operating Empty Weight',
            'W_F   —  Total Fuel (incl. trapped)',
            'W_F   —  Usable Fuel',
            'W_tfo —  Trapped Fuel & Oil',
            'W_crew—  Flight & Cabin Crew',
            'W_PL  —  Payload',
        ],
        'Weight (lbs)': [
            f"{Wto:,.0f}", f"{WE:,.0f}", f"{WOE:,.0f}",
            f"{WF:,.0f}", f"{RR['WFu']:,.0f}",
            f"{Wtfo:,.0f}", f"{Wcrew:,.0f}", f"{Wpl:,.0f}",
        ],
        'Fraction of W_TO': [
            "1.0000",
            f"{WE/Wto:.4f}", f"{WOE/Wto:.4f}",
            f"{WF/Wto:.4f}", f"{RR['WFu']/Wto:.4f}",
            f"{Wtfo/Wto:.4f}", f"{Wcrew/Wto:.4f}", f"{Wpl/Wto:.4f}",
        ],
        '% of W_TO': [
            "100.00%",
            f"{WE/Wto*100:.2f}%", f"{WOE/Wto*100:.2f}%",
            f"{WF/Wto*100:.2f}%", f"{RR['WFu']/Wto*100:.2f}%",
            f"{Wtfo/Wto*100:.3f}%", f"{Wcrew/Wto*100:.3f}%",
            f"{Wpl/Wto*100:.2f}%",
        ],
    })
    st.dataframe(summary, hide_index=True, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-card"><div class="sec-title">Parametric Study — W_TO vs Passenger Count</div>', unsafe_allow_html=True)
    pxa=np.arange(5,npax+25,2); wxr=[]
    for n_ in pxa:
        try: w,_=solve({**P,'npax':int(n_)}); wxr.append(w)
        except: wxr.append(float('nan'))
    fig_px=go.Figure()
    fig_px.add_trace(go.Scatter(
        x=pxa, y=wxr, mode='lines+markers',
        line=dict(color='#10B981', width=2.5),
        marker=dict(size=5, color='#059669'),
        fill='tozeroy', fillcolor='rgba(16,185,129,0.06)',
    ))
    fig_px.add_vline(x=npax, line_dash='dash', line_color='#F59E0B', line_width=1.5,
                     annotation_text=f'Design: {npax} pax',
                     annotation_font_color='#92400E', annotation_font_size=9)
    pset(fig_px, '', 260, xt='Number of Passengers', yt='Gross Takeoff Weight (lbs)')
    st.plotly_chart(fig_px, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════
# TAB 4 — EXPORT
# ════════════════════════════════════════════════
with tab4:
    e1, e2 = st.columns([1, 1], gap="large")

    with e1:
        st.markdown('<div class="sec-card"><div class="sec-title">Export Data — CSV</div>', unsafe_allow_html=True)
        rows = {
            'Parameter': ['W_TO','Mff','W_F_total','W_F_usable','W_payload',
                          'W_empty','W_OE','W_crew','W_tfo','WE_allowable','Convergence_delta',
                          'dWTO_dCp_cruise','dWTO_dnp_cruise','dWTO_dLD_cruise','dWTO_dRange',
                          'dWTO_dCp_loiter','dWTO_dnp_loiter','dWTO_dLD_loiter'],
            'Value': [Wto, RR['Mff'], WF, RR['WFu'], Wpl, WE, WOE, Wcrew, Wtfo,
                      RR['WEa'], RR['diff'],
                      S['dCpR'], S['dnpR'], S['dLDR'], S['dR'],
                      S['dCpE'], S['dnpE'], S['dLDE']],
            'Units': ['lbs','—','lbs','lbs','lbs','lbs','lbs','lbs','lbs','lbs','lbs',
                      'lbs/(lbs/hp/hr)','lbs','lbs','lbs/nm',
                      'lbs/(lbs/hp/hr)','lbs','lbs'],
        }
        b=io.StringIO(); pd.DataFrame(rows).to_csv(b,index=False)
        st.download_button("⬇  Download Full Results  (CSV)", b.getvalue(),
                           "aerosizer_results.csv", "text/csv", use_container_width=True)
        st.markdown("<br>", unsafe_allow_html=True)
        b2=io.StringIO()
        pd.DataFrame({'Phase':list(RR['fracs'].keys()),
                       'Wi/Wi-1':list(RR['fracs'].values())}).to_csv(b2,index=False)
        st.download_button("⬇  Download Phase Fractions  (CSV)", b2.getvalue(),
                           "aerosizer_fractions.csv", "text/csv", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="sec-card"><div class="sec-title">Current Configuration</div>', unsafe_allow_html=True)
        st.dataframe(pd.DataFrame({'Parameter': list(P.keys()),
                                    'Value': [str(v) for v in P.values()]}),
                     hide_index=True, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with e2:
        st.markdown('<div class="sec-card"><div class="sec-title">Export Formal Report — PDF</div>', unsafe_allow_html=True)
        st.markdown("""
<div style="font-size:.82rem;color:#374151;line-height:1.7;margin-bottom:1rem">
The PDF report includes:<br>
&nbsp;· Mission inputs &amp; configuration<br>
&nbsp;· Full weight statement (all components)<br>
&nbsp;· Phase weight fractions (Mff)<br>
&nbsp;· Breguet sensitivity partials (Table 2.20)<br>
&nbsp;· Convergence verification
</div>
""", unsafe_allow_html=True)

        def make_pdf():
            buf=io.BytesIO()
            doc=SimpleDocTemplate(buf, pagesize=A4,
                leftMargin=2*cm, rightMargin=2*cm,
                topMargin=2*cm, bottomMargin=2*cm)
            sty=getSampleStyleSheet()
            def ps(name,**kw):
                return ParagraphStyle(name,parent=sty['Normal'],**kw)
            sTITLE = ps('T', fontSize=20, fontName='Helvetica-Bold',
                         textColor=colors.HexColor('#0A1628'), spaceAfter=4)
            sSUB   = ps('S', fontSize=9,  textColor=colors.HexColor('#64748B'),
                         spaceAfter=16)
            sH2    = ps('H2', fontSize=11, fontName='Helvetica-Bold',
                         textColor=colors.HexColor('#1D4ED8'),
                         spaceBefore=14, spaceAfter=5)
            sB     = ps('B', fontSize=9, leading=14,
                         textColor=colors.HexColor('#374151'))
            ts = TableStyle([
                ('BACKGROUND',    (0,0), (-1,0), colors.HexColor('#0A1628')),
                ('TEXTCOLOR',     (0,0), (-1,0), colors.white),
                ('FONTNAME',      (0,0), (-1,0), 'Helvetica-Bold'),
                ('FONTSIZE',      (0,0), (-1,-1), 8.5),
                ('FONTNAME',      (0,1), (-1,-1), 'Helvetica'),
                ('GRID',          (0,0), (-1,-1), 0.4, colors.HexColor('#CBD5E1')),
                ('ROWBACKGROUNDS',(0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
                ('LEFTPADDING',   (0,0), (-1,-1), 6),
                ('RIGHTPADDING',  (0,0), (-1,-1), 6),
                ('TOPPADDING',    (0,0), (-1,-1), 4),
                ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ])
            story=[
                Paragraph("AeroSizer Pro", sTITLE),
                Paragraph("Preliminary Aircraft Weight Estimation Report · Breguet Method · Propeller-Driven Aircraft", sSUB),
                HRFlowable(width="100%", thickness=1, color=colors.HexColor('#3B82F6')),
                Spacer(1,.25*inch),
                Paragraph("1. Mission Inputs", sH2),
            ]
            t1=Table([['Parameter','Value','Parameter','Value'],
                       ['Passengers', str(npax), 'Design range (nm)', str(R_nm)],
                       ['Pax weight (lbs)', str(wpax), 'Loiter endurance (hr)', str(El)],
                       ['Baggage (lbs)', str(wbag), 'Cruise L/D', str(LDc)],
                       ['Flight crew', str(ncrew), 'Loiter L/D', str(LDl)],
                       ['Cabin attendants', str(natt), 'SFC Cp cruise', str(Cpc)],
                       ['A (regression)', f'{A_v:.4f}', 'SFC Cp loiter', str(Cpl)],
                       ['B (regression)', f'{B_v:.4f}', 'M_tfo', str(Mtfo)]],
                      colWidths=[4.5*cm,3*cm,4.5*cm,3*cm])
            t1.setStyle(ts); story+=[t1,Spacer(1,.15*inch)]
            story.append(Paragraph("2. Gross Takeoff Weight", sH2))
            story.append(Paragraph(
                f"Converged W_TO = <b>{Wto:,.0f} lbs</b> | Mff = {RR['Mff']:.5f} | ΔWE = {RR['diff']:+.2f} lbs",
                sB))
            story+=[Spacer(1,.1*inch),Paragraph("3. Weight Statement", sH2)]
            t2=Table([['Component','Weight (lbs)','Fraction','% W_TO']]+
                list(zip(summary['Weight Component'],
                         summary['Weight (lbs)'],
                         summary['Fraction of W_TO'],
                         summary['% of W_TO'])),
                colWidths=[7*cm,3*cm,2.8*cm,2.8*cm])
            t2.setStyle(ts); story+=[t2,Spacer(1,.12*inch)]
            story.append(Paragraph("4. Phase Weight Fractions", sH2))
            t3=Table([['Phase','Wi / Wi-1','Type']]+
                list(zip(phase_df['Phase'],phase_df['Wi / Wi-1'],phase_df['Type'])),
                colWidths=[5*cm,3.5*cm,3*cm])
            t3.setStyle(ts); story+=[t3,Spacer(1,.12*inch)]
            story.append(Paragraph("5. Sensitivity Partials (Breguet — Table 2.20)", sH2))
            t4=Table([['Partial','Value','Units','Eq.']]+
                list(zip(sdr['Partial'],sdr['Value'],sdr['Units'],sdr['Equation']))+
                list(zip(sdl['Partial'],sdl['Value'],sdl['Units'],sdl['Equation'])),
                colWidths=[4.5*cm,3*cm,4*cm,2*cm])
            t4.setStyle(ts); story.append(t4)
            doc.build(story); buf.seek(0); return buf.read()

        st.download_button(
            "⬇  Generate & Download PDF Report",
            make_pdf(), "aerosizer_report.pdf",
            "application/pdf", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
