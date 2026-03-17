import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import math
import io
import warnings

# محاولة استيراد reportlab — إذا فشل → PDF معطل
PDF_AVAILABLE = False
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.units import inch
    PDF_AVAILABLE = True
except ImportError:
    pass

st.set_page_config(page_title="AeroNova Simulator X", page_icon="✈️", layout="wide")

# ────────────────────────────────────────────────
#                Futuristic CSS Theme
# ────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap');

html, body, [class*="css"] {
    background-color: #050A14 !important;
    color: #C8D8F0 !important;
}
.stApp {
    background: linear-gradient(135deg, #050A14 0%, #0A1628 50%, #050A14 100%);
}
.main-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 2.4rem;
    font-weight: 900;
    background: linear-gradient(90deg, #00D4FF, #8A2BE2, #00D4FF);
    background-size: 200%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shimmer 4s infinite;
    text-align: center;
    letter-spacing: 0.15em;
}
@keyframes shimmer {
    0% { background-position: 0% }
    100% { background-position: 200% }
}
.subtitle {
    font-family: 'Share Tech Mono', monospace;
    color: #4FC3F7;
    text-align: center;
    font-size: 1rem;
    letter-spacing: 0.3em;
    margin: 1rem 0 2rem;
}
.metric-card {
    background: linear-gradient(135deg, #0D1F35, #0A1628);
    border: 1px solid #00D4FF33;
    border-radius: 12px;
    padding: 1.4rem;
    text-align: center;
    margin: 0.5rem 0;
}
.metric-value { font-family: 'Orbitron'; font-size: 1.9rem; font-weight: 700; color: #00D4FF; }
.metric-unit { font-size: 0.9rem; color: #4FC3F7; }
.metric-label { font-family: 'Share Tech Mono'; font-size: 0.75rem; color: #7B9CC8; letter-spacing: 0.15em; margin-top: 0.4rem; }
.sec-hdr {
    font-family: 'Orbitron';
    font-size: 1.1rem;
    font-weight: 700;
    color: #8A2BE2;
    letter-spacing: 0.2em;
    border-bottom: 1px solid #8A2BE230;
    padding-bottom: 0.5rem;
    margin: 1.5rem 0 1rem;
    text-transform: uppercase;
}
.status-ok  { background:#00FF8820; border:1px solid #00FF8860; border-radius:8px; padding:0.6rem 1.2rem; color:#00FF88; font-family:'Share Tech Mono'; }
.status-warn { background:#FF880020; border:1px solid #FF880060; border-radius:8px; padding:0.6rem 1.2rem; color:#FF8800; font-family:'Share Tech Mono'; }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #07111F, #0A1628) !important; }
</style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
#                Layout Helper
# ────────────────────────────────────────────────
def mk_layout(title='', height=380, xt='', yt='', yrange=None):
    ax = dict(
        gridcolor='#00D4FF15',
        linecolor='#00D4FF40',
        title=dict(text=xt) if xt else None
    )
    ay = dict(
        gridcolor='#00D4FF15',
        linecolor='#00D4FF40',
        title=dict(text=yt) if yt else None
    )
    if yrange:
        ay['range'] = yrange
        ay['fixedrange'] = True  # يمنع الزوم اليدوي خارج النطاق

    d = dict(
        paper_bgcolor='rgba(5,10,20,0.0)',
        plot_bgcolor='rgba(10,22,40,0.65)',
        font=dict(family='Share Tech Mono', color='#C8D8F0', size=12),
        margin=dict(l=60, r=30, t=60, b=60),
        xaxis=ax,
        yaxis=ay,
        height=height
    )
    if title:
        d['title'] = dict(text=title, font=dict(color='#4FC3F7', size=15))
    return d

# ────────────────────────────────────────────────
#                Core Calculations
# ────────────────────────────────────────────────
@st.cache_data
def compute_mission(p):
    try:
        Wpl   = p['n_pax'] * (p['w_pax'] + p['w_bag']) + p['n_crew']*205 + p['n_att']*200
        Wcrew = p['n_crew']*205 + p['n_att']*200
        Wtfo  = p['Wto_guess'] * p['Mtfo']
        Rc    = p['range_nm'] * 1.15078
        W5    = math.exp( -Rc / (375 * (p['np_c']/p['Cp_c']) * p['LD_c']) )
        Vm    = p['V_lkts'] * 1.15078
        W6    = math.exp( -p['E_l'] / (375 * (1/Vm) * (p['np_l']/p['Cp_l']) * p['LD_l']) )

        fracs = {
            'Engine Start': 0.990,
            'Taxi':         0.995,
            'Takeoff':      0.995,
            'Climb':        0.985,
            'Cruise':       W5,
            'Loiter':       W6,
            'Descent':      0.985,
            'Landing':      0.995
        }

        Mff = 1.0
        for v in fracs.values():
            Mff *= v

        WF_used = p['Wto_guess'] * (1 - Mff)
        WF = WF_used + p['Wto_guess'] * p['Mres'] * (1 - Mff) + Wtfo

        WOE = p['Wto_guess'] - WF - Wpl
        WE  = WOE - Wtfo - Wcrew

        WE_all = 10 ** ((math.log10(p['Wto_guess']) - p['A']) / p['B'])

        return {
            'Wpl': Wpl, 'Wcrew': Wcrew, 'Wtfo': Wtfo, 'Mff': Mff,
            'WF': WF, 'WF_used': WF_used, 'WOE': WOE, 'WE': WE,
            'WE_all': WE_all, 'diff': WE_all - WE, 'fracs': fracs
        }
    except Exception as e:
        st.error(f"خطأ في الحسابات: {str(e)}")
        return None

@st.cache_data
def solve_wto(p, tol=1.0, max_iter=300):
    pp = dict(p)
    lo, hi = 5000.0, 600000.0
    for i in range(max_iter):
        mid = (lo + hi) / 2
        pp['Wto_guess'] = mid
        r = compute_mission(pp)
        if r is None:
            return None, None
        diff = r['diff']
        if abs(diff) < tol:
            return mid, r
        if diff > 0:
            hi = mid
        else:
            lo = mid
    st.warning(f"لم يتقارب بعد {max_iter} تكرار (delta = {diff:.1f} lbs)")
    return mid, r

@st.cache_data
def sens_calc(p, Wto):
    try:
        Rc = p['range_nm'] * 1.15078
        Vm = p['V_lkts'] * 1.15078
        Mff = compute_mission({**p, 'Wto_guess': Wto})['Mff']
        D = p['n_pax']*(p['w_pax']+p['w_bag']) + p['n_crew']*205*2 + p['n_att']*200
        C = 1 - (1 + p['Mres'])*(1 - Mff) - p['Mtfo']
        dn = C * Wto * (1 - p['B']) - D
        F = (-p['B'] * Wto**2 * (1 + p['Mres']) * Mff) / dn if abs(dn) > 1e-6 else 0

        return {
            'dCp_R':  F * Rc / (375 * p['np_c'] * p['LD_c']),
            'dnp_R': -F * Rc * p['Cp_c'] / (375 * p['np_c']**2 * p['LD_c']),
            'dLD_R': -F * Rc * p['Cp_c'] / (375 * p['np_c'] * p['LD_c']**2),
            'dR':     F * p['Cp_c'] / (375 * p['np_c'] * p['LD_c']),
            'dCp_E':  F * p['E_l'] * Vm / (375 * p['np_l'] * p['LD_l']),
            'dnp_E': -F * p['E_l'] * Vm * p['Cp_l'] / (375 * p['np_l']**2 * p['LD_l']),
            'dLD_E': -F * p['E_l'] * Vm * p['Cp_l'] / (375 * p['np_l'] * p['LD_l']**2),
        }
    except:
        return {k: 0.0 for k in ['dCp_R','dnp_R','dLD_R','dR','dCp_E','dnp_E','dLD_E']}

# ────────────────────────────────────────────────
#                Default Values
# ────────────────────────────────────────────────
DEF = {
    'n_pax':34, 'w_pax':175, 'w_bag':30, 'n_crew':2, 'n_att':1,
    'Mtfo':0.005, 'Mres':0.0, 'range_nm':1100, 'V_lkts':250,
    'LD_c':13, 'Cp_c':0.60, 'np_c':0.85,
    'E_l':0.75, 'LD_l':16, 'Cp_l':0.65, 'np_l':0.77,
    'A':0.3774, 'B':0.9647
}

# ────────────────────────────────────────────────
#                Sidebar Inputs
# ────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="main-title" style="font-size:1.2rem">PARAMETERS</div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-hdr">PAYLOAD</div>', unsafe_allow_html=True)
    n_pax   = st.slider("Passengers",       10, 120, DEF['n_pax'])
    w_pax   = st.slider("Pax weight (lbs)", 140, 220, DEF['w_pax'])
    w_bag   = st.slider("Baggage (lbs)",     10,  60, DEF['w_bag'])
    n_crew  = st.slider("Pilots",             1,   5, DEF['n_crew'])
    n_att   = st.slider("Attendants",         0,   5, DEF['n_att'])

    st.markdown('<div class="sec-hdr">CRUISE</div>', unsafe_allow_html=True)
    range_nm = st.slider("Range (nm)",  200, 4000, DEF['range_nm'], step=50)
    LD_c     = st.slider("Cruise L/D",    8,   22, DEF['LD_c'])
    Cp_c     = st.slider("Cp cruise",   0.3,  1.0, DEF['Cp_c'], step=0.01)
    np_c     = st.slider("np cruise",  0.50,0.95, DEF['np_c'], step=0.01)

    st.markdown('<div class="sec-hdr">LOITER</div>', unsafe_allow_html=True)
    E_l      = st.slider("Endurance (hr)", 0.1, 3.0, DEF['E_l'], step=0.05)
    V_lkts   = st.slider("Loiter speed (kts)", 100, 400, DEF['V_lkts'])
    LD_l     = st.slider("Loiter L/D",     8,   24, DEF['LD_l'])
    Cp_l     = st.slider("Cp loiter",    0.3,  1.0, DEF['Cp_l'], step=0.01)
    np_l     = st.slider("np loiter",   0.50,0.95, DEF['np_l'], step=0.01)

    st.markdown('<div class="sec-hdr">REGRESSION</div>', unsafe_allow_html=True)
    A_val = st.number_input("A", value=DEF['A'], step=0.0001, format="%.4f")
    B_val = st.number_input("B", value=DEF['B'], step=0.0001, format="%.4f")
    Mtfo  = st.number_input("M_tfo", value=DEF['Mtfo'], step=0.0001, format="%.4f")

# ────────────────────────────────────────────────
#                Computation
# ────────────────────────────────────────────────
P = {
    'n_pax':n_pax, 'w_pax':w_pax, 'w_bag':w_bag, 'n_crew':n_crew, 'n_att':n_att,
    'Mtfo':Mtfo, 'Mres':0.0, 'range_nm':range_nm, 'V_lkts':V_lkts,
    'LD_c':LD_c, 'Cp_c':Cp_c, 'np_c':np_c,
    'E_l':E_l, 'LD_l':LD_l, 'Cp_l':Cp_l, 'np_l':np_l,
    'A':A_val, 'B':B_val, 'Wto_guess': 52000
}

Wto, R = solve_wto(P)
S = sens_calc(P, Wto) if Wto is not None else {}

# ────────────────────────────────────────────────
#                Main Page
# ────────────────────────────────────────────────
st.markdown('<h1 class="main-title">AERONOVA SIMULATOR X</h1>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">PROPELLER-DRIVEN AIRCRAFT PRELIMINARY SIZING – BREGUET</div>', unsafe_allow_html=True)

if Wto is None or R is None:
    st.error("حدث خطأ في الحسابات الأساسية. تحقق من المدخلات.")
else:
    delta = R['diff']
    if abs(delta) < 10:
        st.markdown(f'<div class="status-ok">CONVERGED | W_TO = {Wto:,.0f} lbs | Δ = {delta:.1f} lbs</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="status-warn">Δ = {delta:.1f} lbs (قد يحتاج تعديل الـ guess أو المدخلات)</div>', unsafe_allow_html=True)

    # باقي الـ tabs والرسوم البيانية كما في الكود الأصلي (لكن مع تحسينات صغيرة في الـ layout)
    # ... (يمكنك لصق باقي الكود من tab1 إلى tab4 من النسخة الأصلية هنا)

    # مثال على تحسين واحد للـ bar chart:
    with st.container():
        phases = list(R['fracs'].keys())
        fracs  = list(R['fracs'].values())
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=phases, y=fracs,
            marker_color=['#8A2BE2','#7B6FD4','#6BB4C6','#00D4FF','#00C4EE','#00FF88','#00D070','#00B060'],
            text=[f'{v:.4f}' for v in fracs],
            textposition='outside',
            textfont=dict(size=11, color='#E0F0FF')
        ))
        fig.update_layout(**mk_layout('Phase Weight Fractions', 380, yrange=[0.96, 1.005]))
        fig.update_yaxes(tickformat='.4f')
        st.plotly_chart(fig, use_container_width=True)

# إذا أردت باقي الـ tabs كاملة، أخبرني وسأكملها بنفس الأسلوب (لأن الرسالة طويلة جداً)

st.markdown("---")
st.caption("AeroNova Simulator X v1.0 – Stable version – March 2026")
