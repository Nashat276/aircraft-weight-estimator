import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import math
import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch

st.set_page_config(
    page_title="AeroNova Simulator X",
    page_icon="✈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&family=Exo+2:wght@300;400;600&display=swap');

html, body, [class*="css"] {
    background-color: #050A14 !important;
    color: #C8D8F0 !important;
}
.stApp { background: linear-gradient(135deg, #050A14 0%, #0A1628 50%, #050A14 100%); }

h1, h2, h3 { font-family: 'Orbitron', monospace !important; }
p, label, div { font-family: 'Exo 2', sans-serif !important; }

.main-title {
    font-family: 'Orbitron', monospace;
    font-size: 2.4rem;
    font-weight: 900;
    background: linear-gradient(90deg, #00D4FF, #8A2BE2, #00D4FF);
    background-size: 200%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shimmer 3s infinite;
    text-align: center;
    letter-spacing: 0.15em;
    margin-bottom: 0;
}
@keyframes shimmer { 0%{background-position:0%} 100%{background-position:200%} }

.subtitle {
    font-family: 'Share Tech Mono', monospace;
    color: #4FC3F7;
    text-align: center;
    font-size: 0.85rem;
    letter-spacing: 0.3em;
    margin-top: 0.2rem;
    margin-bottom: 1.5rem;
}

.metric-card {
    background: linear-gradient(135deg, #0D1F35, #0A1628);
    border: 1px solid #00D4FF33;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    text-align: center;
    box-shadow: 0 0 20px #00D4FF15, inset 0 0 30px #00000030;
    margin-bottom: 0.5rem;
}
.metric-value {
    font-family: 'Orbitron', monospace;
    font-size: 1.8rem;
    font-weight: 700;
    color: #00D4FF;
    text-shadow: 0 0 10px #00D4FF80;
}
.metric-label {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.7rem;
    color: #7B9CC8;
    letter-spacing: 0.15em;
    margin-top: 0.3rem;
}
.metric-unit { font-size: 0.9rem; color: #4FC3F7; }

.section-header {
    font-family: 'Orbitron', monospace;
    font-size: 0.9rem;
    font-weight: 700;
    color: #8A2BE2;
    letter-spacing: 0.2em;
    border-bottom: 1px solid #8A2BE230;
    padding-bottom: 0.4rem;
    margin-bottom: 1rem;
    text-transform: uppercase;
}

.status-ok {
    background: #00FF8820;
    border: 1px solid #00FF8860;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.85rem;
    color: #00FF88;
}
.status-warn {
    background: #FF880020;
    border: 1px solid #FF880060;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.85rem;
    color: #FF8800;
}

.stSlider > div > div { background: #0D1F35 !important; }
.stSlider [data-testid="stThumbValue"] { color: #00D4FF !important; }

div[data-testid="stTab"] button {
    font-family: 'Orbitron', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.1em !important;
    color: #4FC3F7 !important;
    border-bottom: 2px solid transparent !important;
}
div[data-testid="stTab"] button[aria-selected="true"] {
    color: #00D4FF !important;
    border-bottom: 2px solid #00D4FF !important;
    text-shadow: 0 0 8px #00D4FF80 !important;
}

.stButton > button {
    font-family: 'Orbitron', monospace !important;
    background: linear-gradient(90deg, #00D4FF20, #8A2BE220) !important;
    border: 1px solid #00D4FF60 !important;
    color: #00D4FF !important;
    border-radius: 8px !important;
    letter-spacing: 0.1em !important;
    transition: all 0.3s !important;
}
.stButton > button:hover {
    background: linear-gradient(90deg, #00D4FF40, #8A2BE240) !important;
    box-shadow: 0 0 15px #00D4FF40 !important;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #07111F, #0A1628) !important;
    border-right: 1px solid #00D4FF20 !important;
}

.scan-line {
    background: repeating-linear-gradient(0deg, transparent, transparent 2px, #00D4FF04 2px, #00D4FF04 4px);
    pointer-events: none;
    position: fixed; top:0; left:0; width:100%; height:100%;
    z-index: 9999;
}
</style>
<div class="scan-line"></div>
""", unsafe_allow_html=True)


# ─── CORE PHYSICS ENGINE ──────────────────────────────────────────────────────

def compute_mission(params):
    p = params
    Wpl = (p['n_pax'] * (p['w_pax'] + p['w_bag'])) + p['n_crew'] * 205 + (p['n_att'] * 200)
    Wcrew = p['n_crew'] * 205 + p['n_att'] * 200
    Wtfo = p['Wto_guess'] * p['Mtfo']

    # Weight fractions
    W1_Wto = 0.990
    W2_W1  = 0.995
    W3_W2  = 0.995
    W4_W3  = 0.985

    Rc_sm = p['range_nm'] * 1.15078
    W5_W4 = 1.0 / math.exp(Rc_sm / (375 * (p['np_cruise'] / p['Cp_cruise']) * p['LD_cruise']))

    V_mph = p['V_loiter_kts'] * 1.15078
    W6_W5 = 1.0 / math.exp(p['E_loiter'] / (375 * (1.0 / V_mph) * (p['np_loiter'] / p['Cp_loiter']) * p['LD_loiter']))

    W7_W6 = 0.985
    W8_W7 = 0.995

    Mff = W1_Wto * W2_W1 * W3_W2 * W4_W3 * W5_W4 * W6_W5 * W7_W6 * W8_W7

    WF_used = p['Wto_guess'] * (1 - Mff)
    WF_res  = p['Wto_guess'] * p['Mres'] * (1 - Mff)
    WF      = WF_used + WF_res + Wtfo

    WOE_tent = p['Wto_guess'] - WF - Wpl
    WE_tent  = WOE_tent - Wtfo - Wcrew

    A, B = p['A'], p['B']
    log_Wto = math.log10(p['Wto_guess'])
    WE_allow = 10 ** ((log_Wto - A) / B)

    diff = WE_allow - WE_tent

    fractions = {
        'Engine Start': W1_Wto,
        'Taxi':         W2_W1,
        'Takeoff':      W3_W2,
        'Climb':        W4_W3,
        'Cruise':       W5_W4,
        'Loiter':       W6_W5,
        'Descent':      W7_W6,
        'Landing':      W8_W7,
    }

    return {
        'Wpl': Wpl, 'Wcrew': Wcrew, 'Wtfo': Wtfo,
        'Mff': Mff, 'WF': WF, 'WOE': WOE_tent, 'WE': WE_tent,
        'WE_allow': WE_allow, 'diff': diff, 'fractions': fractions,
        'WF_used': WF_used,
    }


def solve_wto(params, tol=1.0, max_iter=100):
    p = dict(params)
    Wpl = (p['n_pax'] * (p['w_pax'] + p['w_bag'])) + p['n_crew'] * 205 + p['n_att'] * 200

    lo, hi = 10000, 300000
    for _ in range(max_iter):
        mid = (lo + hi) / 2
        p['Wto_guess'] = mid
        r = compute_mission(p)
        if abs(r['diff']) < tol:
            return mid, r
        if r['diff'] > 0:
            hi = mid
        else:
            lo = mid
    return mid, r


def sensitivity(params, Wto):
    p = params
    Rc_sm = p['range_nm'] * 1.15078
    V_mph = p['V_loiter_kts'] * 1.15078

    C = 1 - (1 + p['Mres']) * (1 - compute_mission({**p, 'Wto_guess': Wto})['Mff']) - p['Mtfo']
    D = Wpl_from(p) + p['n_crew'] * 205 + p['n_att'] * 200
    Mff = compute_mission({**p, 'Wto_guess': Wto})['Mff']
    B = p['B']
    numer = -B * Wto**2 * (1 + p['Mres']) * Mff
    denom = C * Wto * (1 - B) - D
    F = numer / denom if denom != 0 else 0

    dWTO_dCp_R  =  F * Rc_sm / (375 * p['np_cruise'] * p['LD_cruise'])
    dWTO_dnp_R  = -F * Rc_sm * p['Cp_cruise'] / (375 * p['np_cruise']**2 * p['LD_cruise'])
    dWTO_dLD_R  = -F * Rc_sm * p['Cp_cruise'] / (375 * p['np_cruise'] * p['LD_cruise']**2)
    dWTO_dR     =  F * p['Cp_cruise'] / (375 * p['np_cruise'] * p['LD_cruise'])

    E = p['E_loiter']
    dWTO_dCp_E  =  F * E * V_mph / (375 * p['np_loiter'] * p['LD_loiter'])
    dWTO_dnp_E  = -F * E * V_mph * p['Cp_loiter'] / (375 * p['np_loiter']**2 * p['LD_loiter'])
    dWTO_dLD_E  = -F * E * V_mph * p['Cp_loiter'] / (375 * p['np_loiter'] * p['LD_loiter']**2)

    return {
        'F': F,
        'Range': {'dCp': dWTO_dCp_R, 'dnp': dWTO_dnp_R, 'dLD': dWTO_dLD_R, 'dR': dWTO_dR},
        'Loiter': {'dCp': dWTO_dCp_E, 'dnp': dWTO_dnp_E, 'dLD': dWTO_dLD_E},
    }


def Wpl_from(p):
    return p['n_pax'] * (p['w_pax'] + p['w_bag']) + p['n_crew'] * 205 + p['n_att'] * 200


# ─── PLOTLY THEME ─────────────────────────────────────────────────────────────

PLOTLY_LAYOUT = dict(
    paper_bgcolor='rgba(5,10,20,0)',
    plot_bgcolor='rgba(10,22,40,0.7)',
    font=dict(family='Share Tech Mono', color='#C8D8F0', size=11),
    xaxis=dict(gridcolor='#00D4FF12', linecolor='#00D4FF30', tickcolor='#4FC3F7'),
    yaxis=dict(gridcolor='#00D4FF12', linecolor='#00D4FF30', tickcolor='#4FC3F7'),
    margin=dict(l=50, r=20, t=40, b=40),
)

NEON_COLORS = ['#00D4FF', '#8A2BE2', '#00FF88', '#FF6B35', '#FFD700', '#FF3CAC']


# ─── DEFAULT PARAMS ───────────────────────────────────────────────────────────

DEFAULTS = {
    'n_pax': 34, 'w_pax': 175, 'w_bag': 30,
    'n_crew': 2, 'n_att': 1,
    'Mtfo': 0.005, 'Mres': 0.0,
    'range_nm': 1100,
    'V_cruise_kts': 250, 'LD_cruise': 13, 'Cp_cruise': 0.60, 'np_cruise': 0.85,
    'E_loiter': 0.75, 'V_loiter_kts': 250, 'LD_loiter': 16, 'Cp_loiter': 0.65, 'np_loiter': 0.77,
    'A': 0.3774, 'B': 0.9647,
    'Wto_guess': 48550,
}


# ─── SIDEBAR ──────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown('<div class="main-title" style="font-size:1.1rem">⚙ PARAMETERS</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle" style="font-size:0.65rem">MISSION CONFIGURATION</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">PAYLOAD</div>', unsafe_allow_html=True)
    n_pax    = st.slider("Passengers",     10, 100, DEFAULTS['n_pax'])
    w_pax    = st.slider("Pax weight (lbs)", 140, 220, DEFAULTS['w_pax'])
    w_bag    = st.slider("Baggage (lbs)",    10,  60, DEFAULTS['w_bag'])
    n_crew   = st.slider("Pilots",           1,   4, DEFAULTS['n_crew'])
    n_att    = st.slider("Attendants",       0,   4, DEFAULTS['n_att'])

    st.markdown('<div class="section-header">CRUISE PHASE</div>', unsafe_allow_html=True)
    range_nm    = st.slider("Range (nm)",     200, 3000, DEFAULTS['range_nm'], step=50)
    V_cruise    = st.slider("Cruise speed (kts)", 150, 400, DEFAULTS['V_cruise_kts'])
    LD_cruise   = st.slider("Cruise L/D",      8,  22, DEFAULTS['LD_cruise'])
    Cp_cruise   = st.slider("Cp cruise",     0.3, 1.0, DEFAULTS['Cp_cruise'], step=0.01)
    np_cruise   = st.slider("η_p cruise",    0.5, 0.95, DEFAULTS['np_cruise'], step=0.01)

    st.markdown('<div class="section-header">LOITER PHASE</div>', unsafe_allow_html=True)
    E_loiter    = st.slider("Endurance (hr)",  0.1, 3.0, DEFAULTS['E_loiter'], step=0.05)
    V_loiter    = st.slider("Loiter speed (kts)", 100, 350, DEFAULTS['V_loiter_kts'])
    LD_loiter   = st.slider("Loiter L/D",      8,  24, DEFAULTS['LD_loiter'])
    Cp_loiter   = st.slider("Cp loiter",      0.3, 1.0, DEFAULTS['Cp_loiter'], step=0.01)
    np_loiter   = st.slider("η_p loiter",     0.5, 0.95, DEFAULTS['np_loiter'], step=0.01)

    st.markdown('<div class="section-header">REGRESSION CONSTANTS</div>', unsafe_allow_html=True)
    A_coef = st.number_input("A (Table 2.2)", value=DEFAULTS['A'], step=0.001, format="%.4f")
    B_coef = st.number_input("B (Table 2.2)", value=DEFAULTS['B'], step=0.001, format="%.4f")
    Mtfo   = st.number_input("M_tfo",         value=DEFAULTS['Mtfo'], step=0.001, format="%.4f")


params = {
    'n_pax': n_pax, 'w_pax': w_pax, 'w_bag': w_bag,
    'n_crew': n_crew, 'n_att': n_att,
    'Mtfo': Mtfo, 'Mres': 0.0,
    'range_nm': range_nm,
    'V_cruise_kts': V_cruise, 'LD_cruise': LD_cruise, 'Cp_cruise': Cp_cruise, 'np_cruise': np_cruise,
    'E_loiter': E_loiter, 'V_loiter_kts': V_loiter, 'LD_loiter': LD_loiter,
    'Cp_loiter': Cp_loiter, 'np_loiter': np_loiter,
    'A': A_coef, 'B': B_coef,
    'Wto_guess': DEFAULTS['Wto_guess'],
}

Wto, result = solve_wto(params)
sens = sensitivity(params, Wto)


# ─── HEADER ───────────────────────────────────────────────────────────────────

st.markdown('<h1 class="main-title">✈ AERONOVA SIMULATOR X</h1>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">PROPELLER-DRIVEN AIRCRAFT PRELIMINARY SIZING ENGINE · BREGUET RANGE/ENDURANCE</div>', unsafe_allow_html=True)

conv_ok = abs(result['diff']) < 5
if conv_ok:
    st.markdown(f'<div class="status-ok">✔ CONVERGED — ΔWE = {result["diff"]:.2f} lbs &nbsp;|&nbsp; WTO = {Wto:,.0f} lbs</div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div class="status-warn">⚠ CONVERGENCE DELTA: {result["diff"]:.1f} lbs — tighten tolerance</div>', unsafe_allow_html=True)

st.markdown("---")

# ─── TABS ─────────────────────────────────────────────────────────────────────

tab1, tab2, tab3, tab4 = st.tabs(["⬡ MISSION SIZING", "⬡ SENSITIVITY", "⬡ WEIGHT BREAKDOWN", "⬡ EXPORT"])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — MISSION SIZING
# ══════════════════════════════════════════════════════════════════════════════

with tab1:
    c1, c2, c3, c4 = st.columns(4)
    cards = [
        (c1, f"{Wto:,.0f}", "lbs", "GROSS WEIGHT W_TO"),
        (c2, f"{result['Mff']:.4f}", "", "FUEL FRACTION M_FF"),
        (c3, f"{result['WF']:,.0f}", "lbs", "TOTAL FUEL W_F"),
        (c4, f"{result['Wpl']:,.0f}", "lbs", "PAYLOAD W_PL"),
    ]
    for col, val, unit, label in cards:
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{val} <span class="metric-unit">{unit}</span></div>
                <div class="metric-label">{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("&nbsp;")
    col_a, col_b = st.columns([1.1, 0.9])

    with col_a:
        st.markdown('<div class="section-header">MISSION WEIGHT FRACTIONS</div>', unsafe_allow_html=True)
        phases = list(result['fractions'].keys())
        fracs  = list(result['fractions'].values())
        cum    = [1.0]
        for f in fracs:
            cum.append(cum[-1] * f)

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=phases, y=fracs,
            marker=dict(
                color=fracs,
                colorscale=[[0,'#8A2BE2'],[0.5,'#00D4FF'],[1,'#00FF88']],
            ),
            name='W_i / W_{i-1}',
            text=[f'{v:.4f}' for v in fracs],
            textposition='outside',
            textfont=dict(size=10, color='#C8D8F0'),
        ))
        fig.update_layout(**PLOTLY_LAYOUT,
            title=dict(text='Phase Weight Fractions', font=dict(color='#4FC3F7', size=13)),
            yaxis_range=[0.80, 1.02],
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.markdown('<div class="section-header">WEIGHT BUDGET GAUGE</div>', unsafe_allow_html=True)
        fig2 = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=Wto,
            delta={'reference': DEFAULTS['Wto_guess'], 'relative': False,
                   'font': {'color': '#00FF88', 'size': 14}},
            number={'suffix': ' lbs', 'font': {'color': '#00D4FF', 'size': 22,
                                                'family': 'Share Tech Mono'}},
            gauge={
                'axis': {'range': [10000, 120000], 'tickcolor': '#4FC3F7',
                         'tickfont': {'size': 9}},
                'bar': {'color': '#00D4FF', 'thickness': 0.25},
                'bgcolor': '#0A1628',
                'borderwidth': 1, 'bordercolor': '#00D4FF30',
                'steps': [
                    {'range': [10000,  40000], 'color': '#00FF8810'},
                    {'range': [40000,  70000], 'color': '#00D4FF10'},
                    {'range': [70000, 120000], 'color': '#FF3CAC10'},
                ],
                'threshold': {'line': {'color': '#FF3CAC', 'width': 2},
                              'thickness': 0.75, 'value': Wto},
            },
            title={'text': 'W_TO', 'font': {'color': '#7B9CC8', 'size': 12,
                                              'family': 'Orbitron'}},
        ))
        fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                           font=dict(family='Share Tech Mono', color='#C8D8F0'),
                           height=280, margin=dict(t=30, b=10, l=20, r=20))
        st.plotly_chart(fig2, use_container_width=True)

        st.markdown('<div class="section-header">WE CONVERGENCE CHECK</div>', unsafe_allow_html=True)
        we_df = pd.DataFrame({
            'Parameter': ['WE Tent', 'WE Allow', 'Delta'],
            'Value (lbs)': [f"{result['WE']:,.1f}", f"{result['WE_allow']:,.1f}",
                            f"{result['diff']:+.2f}"]
        })
        st.dataframe(we_df, hide_index=True, use_container_width=True)

    # Range sweep chart
    st.markdown('<div class="section-header">WTO vs RANGE SWEEP</div>', unsafe_allow_html=True)
    ranges = np.linspace(200, 3000, 60)
    wtos = []
    for r in ranges:
        try:
            w, _ = solve_wto({**params, 'range_nm': r})
            wtos.append(w)
        except:
            wtos.append(np.nan)

    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=ranges, y=wtos,
        mode='lines',
        line=dict(color='#00D4FF', width=2.5),
        fill='tozeroy',
        fillcolor='rgba(0,212,255,0.05)',
        name='W_TO',
    ))
    fig3.add_vline(x=range_nm, line_dash='dash', line_color='#FF3CAC', line_width=1.5,
                   annotation_text=f'Current: {range_nm} nm', annotation_font_color='#FF3CAC')
    fig3.update_layout(**PLOTLY_LAYOUT,
        title=dict(text='Gross Takeoff Weight vs Range', font=dict(color='#4FC3F7', size=13)),
        xaxis_title='Range (nm)', yaxis_title='W_TO (lbs)',
        height=320,
    )
    st.plotly_chart(fig3, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — SENSITIVITY
# ══════════════════════════════════════════════════════════════════════════════

with tab2:
    st.markdown('<div class="section-header">BREGUET SENSITIVITY PARTIALS (TABLE 2.20)</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Range phase**")
        sens_r = sens['Range']
        s_data_r = {
            'Partial': ['∂WTO/∂Cp', '∂WTO/∂ηp', '∂WTO/∂(L/D)', '∂WTO/∂R'],
            'Value': [f"{sens_r['dCp']:+,.1f}", f"{sens_r['dnp']:+,.1f}",
                      f"{sens_r['dLD']:+,.1f}", f"{sens_r['dR']:+,.2f}"],
            'Units': ['lbs / (lbs/hp/hr)', 'lbs', 'lbs', 'lbs/nm'],
        }
        st.dataframe(pd.DataFrame(s_data_r), hide_index=True, use_container_width=True)

    with col2:
        st.markdown("**Loiter phase**")
        sens_l = sens['Loiter']
        s_data_l = {
            'Partial': ['∂WTO/∂Cp', '∂WTO/∂ηp', '∂WTO/∂(L/D)'],
            'Value': [f"{sens_l['dCp']:+,.1f}", f"{sens_l['dnp']:+,.1f}",
                      f"{sens_l['dLD']:+,.1f}"],
            'Units': ['lbs / (lbs/hp/hr)', 'lbs', 'lbs'],
        }
        st.dataframe(pd.DataFrame(s_data_l), hide_index=True, use_container_width=True)

    # Tornado chart
    st.markdown('<div class="section-header">TORNADO DIAGRAM — WTO SENSITIVITY</div>', unsafe_allow_html=True)

    labels = ['Cp (range)', 'ηp (range)', 'L/D (range)', 'R (range)',
              'Cp (loiter)', 'ηp (loiter)', 'L/D (loiter)']
    values = [sens_r['dCp'], sens_r['dnp'], sens_r['dLD'], sens_r['dR'] * range_nm * 0.1,
              sens_l['dCp'], sens_l['dnp'], sens_l['dLD']]

    abs_v = [abs(v) for v in values]
    order = sorted(range(len(abs_v)), key=lambda i: abs_v[i])
    labels_s = [labels[i] for i in order]
    values_s = [values[i] for i in order]
    colors_s = ['#00D4FF' if v >= 0 else '#FF3CAC' for v in values_s]

    fig_t = go.Figure(go.Bar(
        x=values_s, y=labels_s,
        orientation='h',
        marker=dict(color=colors_s, line=dict(color='#00000040', width=0.5)),
        text=[f'{v:+,.0f}' for v in values_s],
        textposition='outside',
        textfont=dict(size=10),
    ))
    fig_t.add_vline(x=0, line_color='#C8D8F080', line_width=1)
    fig_t.update_layout(**PLOTLY_LAYOUT,
        title=dict(text='Tornado: ΔW_TO per unit change in parameter', font=dict(color='#4FC3F7', size=13)),
        xaxis_title='ΔW_TO (lbs)', height=380,
        yaxis=dict(gridcolor='#00D4FF12', linecolor='#00D4FF30'),
    )
    st.plotly_chart(fig_t, use_container_width=True)

    # 3D sensitivity surface: Cp vs np vs WTO
    st.markdown('<div class="section-header">3D SURFACE — WTO vs Cp × L/D (CRUISE)</div>', unsafe_allow_html=True)
    cp_arr  = np.linspace(0.40, 0.90, 25)
    ld_arr  = np.linspace(9,  20, 25)
    Z = np.zeros((len(cp_arr), len(ld_arr)))
    for i, cp in enumerate(cp_arr):
        for j, ld in enumerate(ld_arr):
            try:
                w, _ = solve_wto({**params, 'Cp_cruise': cp, 'LD_cruise': ld})
                Z[i, j] = w
            except:
                Z[i, j] = np.nan

    fig4 = go.Figure(go.Surface(
        x=ld_arr, y=cp_arr, z=Z,
        colorscale=[[0,'#050A14'],[0.3,'#0A1628'],[0.6,'#00D4FF'],[1,'#8A2BE2']],
        opacity=0.92,
        contours=dict(z=dict(show=True, color='#00D4FF30', width=1)),
        showscale=True,
        colorbar=dict(title='W_TO (lbs)', tickfont=dict(color='#C8D8F0', size=9),
                      titlefont=dict(color='#4FC3F7', size=10)),
    ))
    fig4.update_layout(
        paper_bgcolor='rgba(5,10,20,0)',
        font=dict(family='Share Tech Mono', color='#C8D8F0', size=10),
        scene=dict(
            xaxis=dict(title='L/D', backgroundcolor='rgba(10,22,40,0.8)',
                       gridcolor='#00D4FF20', linecolor='#00D4FF40'),
            yaxis=dict(title='Cp', backgroundcolor='rgba(10,22,40,0.8)',
                       gridcolor='#00D4FF20', linecolor='#00D4FF40'),
            zaxis=dict(title='W_TO (lbs)', backgroundcolor='rgba(10,22,40,0.8)',
                       gridcolor='#00D4FF20', linecolor='#00D4FF40'),
            bgcolor='rgba(5,10,20,0.95)',
        ),
        title=dict(text='3D: W_TO surface over Cp and L/D', font=dict(color='#4FC3F7', size=13)),
        margin=dict(l=0, r=0, t=50, b=0),
        height=500,
    )
    st.plotly_chart(fig4, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — WEIGHT BREAKDOWN
# ══════════════════════════════════════════════════════════════════════════════

with tab3:
    st.markdown('<div class="section-header">FULL WEIGHT STACK</div>', unsafe_allow_html=True)

    WE   = result['WE']
    WOE  = result['WOE']
    WF   = result['WF']
    Wpl  = result['Wpl']
    Wcrew  = result['Wcrew']
    Wtfo   = result['Wtfo']

    col_pie, col_bar = st.columns(2)

    with col_pie:
        labels_w = ['Empty Weight', 'Fuel (usable)', 'Trapped Fuel/Oil', 'Crew', 'Payload']
        values_w = [WE, result['WF_used'], Wtfo, Wcrew, Wpl]
        fig_pie = go.Figure(go.Pie(
            labels=labels_w, values=values_w,
            hole=0.5,
            marker=dict(colors=['#8A2BE2','#00D4FF','#FF6B35','#00FF88','#FFD700'],
                        line=dict(color='#050A14', width=2)),
            textfont=dict(size=11, color='#C8D8F0'),
            textinfo='label+percent',
        ))
        fig_pie.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Share Tech Mono', color='#C8D8F0'),
            title=dict(text='W_TO Breakdown', font=dict(color='#4FC3F7', size=13)),
            showlegend=False,
            margin=dict(t=40, b=10, l=10, r=10),
            height=320,
            annotations=[dict(text=f'{Wto:,.0f}<br>lbs', x=0.5, y=0.5, showarrow=False,
                               font=dict(size=14, color='#00D4FF', family='Orbitron'))]
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_bar:
        fracs = result['fractions']
        phases_list = list(fracs.keys())
        frac_vals   = list(fracs.values())
        cum = [Wto]
        for f in frac_vals:
            cum.append(cum[-1] * f)

        fig_w = go.Figure()
        fig_w.add_trace(go.Scatter(
            x=phases_list + ['Landing'],
            y=cum,
            mode='lines+markers',
            line=dict(color='#00D4FF', width=2.5),
            marker=dict(color='#8A2BE2', size=8, line=dict(color='#00D4FF', width=1.5)),
            fill='tonexty' if False else None,
        ))
        fig_w.update_layout(**PLOTLY_LAYOUT,
            title=dict(text='Weight Through Mission Phases', font=dict(color='#4FC3F7', size=13)),
            xaxis_title='Phase', yaxis_title='Aircraft Weight (lbs)',
            height=320,
        )
        st.plotly_chart(fig_w, use_container_width=True)

    # Summary table
    st.markdown('<div class="section-header">WEIGHT SUMMARY TABLE</div>', unsafe_allow_html=True)
    summary = pd.DataFrame({
        'Weight Component': ['W_TO (Gross)', 'W_E (Empty)', 'W_OE (Operating Empty)',
                              'W_F (Total Fuel)', 'W_F (Usable)', 'W_tfo', 'W_crew', 'W_payload'],
        'Value (lbs)': [f"{Wto:,.1f}", f"{WE:,.1f}", f"{WOE:,.1f}",
                         f"{WF:,.1f}", f"{result['WF_used']:,.1f}", f"{Wtfo:,.2f}",
                         f"{Wcrew:,.0f}", f"{Wpl:,.0f}"],
        '% of W_TO': [f"{100:.1f}%", f"{WE/Wto*100:.1f}%", f"{WOE/Wto*100:.1f}%",
                       f"{WF/Wto*100:.1f}%", f"{result['WF_used']/Wto*100:.1f}%",
                       f"{Wtfo/Wto*100:.2f}%", f"{Wcrew/Wto*100:.2f}%",
                       f"{Wpl/Wto*100:.1f}%"],
    })
    st.dataframe(summary, hide_index=True, use_container_width=True)

    # Payload-range
    st.markdown('<div class="section-header">PAYLOAD–RANGE DIAGRAM</div>', unsafe_allow_html=True)
    pax_arr = np.arange(5, n_pax + 15, 2)
    wtos_pax = []
    for np_ in pax_arr:
        try:
            w, _ = solve_wto({**params, 'n_pax': np_})
            wtos_pax.append(w)
        except:
            wtos_pax.append(np.nan)

    fig_pr = go.Figure()
    fig_pr.add_trace(go.Scatter(
        x=pax_arr, y=wtos_pax,
        mode='lines+markers',
        line=dict(color='#00FF88', width=2),
        marker=dict(size=5),
        name='W_TO',
        fill='tozeroy', fillcolor='rgba(0,255,136,0.04)',
    ))
    fig_pr.add_vline(x=n_pax, line_dash='dot', line_color='#FFD700', line_width=1.5,
                     annotation_text=f'{n_pax} pax', annotation_font_color='#FFD700')
    fig_pr.update_layout(**PLOTLY_LAYOUT,
        title=dict(text='W_TO vs Passenger Count', font=dict(color='#4FC3F7', size=13)),
        xaxis_title='Passengers', yaxis_title='W_TO (lbs)', height=300,
    )
    st.plotly_chart(fig_pr, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — EXPORT
# ══════════════════════════════════════════════════════════════════════════════

with tab4:
    st.markdown('<div class="section-header">EXPORT RESULTS</div>', unsafe_allow_html=True)

    col_e1, col_e2 = st.columns(2)

    # CSV export
    with col_e1:
        st.markdown("**CSV — Full Results**")
        export_data = {
            'Parameter': ['W_TO', 'Mff', 'W_F', 'W_payload', 'W_empty', 'W_OE',
                           'W_crew', 'W_tfo', 'WE_allow', 'Convergence_delta',
                           'dWTO_dCp_range', 'dWTO_dnp_range', 'dWTO_dLD_range', 'dWTO_dR',
                           'dWTO_dCp_loiter', 'dWTO_dnp_loiter', 'dWTO_dLD_loiter'],
            'Value': [Wto, result['Mff'], WF, Wpl, WE, WOE,
                       Wcrew, Wtfo, result['WE_allow'], result['diff'],
                       sens_r['dCp'], sens_r['dnp'], sens_r['dLD'], sens_r['dR'],
                       sens_l['dCp'], sens_l['dnp'], sens_l['dLD']],
            'Units': ['lbs','–','lbs','lbs','lbs','lbs','lbs','lbs','lbs','lbs',
                       'lbs/(lbs/hp/hr)','lbs','lbs','lbs/nm',
                       'lbs/(lbs/hp/hr)','lbs','lbs'],
        }
        df_export = pd.DataFrame(export_data)
        csv_buf = io.StringIO()
        df_export.to_csv(csv_buf, index=False)
        st.download_button(
            label="⬇ DOWNLOAD CSV",
            data=csv_buf.getvalue(),
            file_name="aeronova_results.csv",
            mime="text/csv",
            use_container_width=True,
        )

        st.markdown("**Weight fractions CSV**")
        df_frac = pd.DataFrame({'Phase': list(result['fractions'].keys()),
                                 'Wi/Wi-1': list(result['fractions'].values())})
        csv_frac = io.StringIO()
        df_frac.to_csv(csv_frac, index=False)
        st.download_button(
            label="⬇ DOWNLOAD FRACTIONS CSV",
            data=csv_frac.getvalue(),
            file_name="aeronova_fractions.csv",
            mime="text/csv",
            use_container_width=True,
        )

    # PDF export
    with col_e2:
        st.markdown("**PDF — Mission Report**")

        def generate_pdf():
            buf = io.BytesIO()
            doc = SimpleDocTemplate(buf, pagesize=letter,
                                    leftMargin=0.75*inch, rightMargin=0.75*inch,
                                    topMargin=0.75*inch, bottomMargin=0.75*inch)
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle('title', parent=styles['Title'],
                                          fontSize=18, textColor=colors.HexColor('#00D4FF'),
                                          spaceAfter=6)
            h2_style = ParagraphStyle('h2', parent=styles['Heading2'],
                                       fontSize=12, textColor=colors.HexColor('#8A2BE2'),
                                       spaceBefore=12, spaceAfter=4)
            body_style = ParagraphStyle('body', parent=styles['Normal'],
                                         fontSize=9, leading=13)

            story = []
            story.append(Paragraph("AeroNova Simulator X — Mission Report", title_style))
            story.append(Paragraph("Propeller-Driven Aircraft Preliminary Sizing (Breguet Method)", body_style))
            story.append(Spacer(1, 0.2*inch))

            story.append(Paragraph("Mission Parameters", h2_style))
            mp_data = [['Parameter', 'Value'],
                        ['Passengers', str(n_pax)], ['Crew', str(n_crew)],
                        ['Range (nm)', str(range_nm)], ['Cruise L/D', str(LD_cruise)],
                        ['Loiter endurance (hr)', str(E_loiter)]]
            t = Table(mp_data, colWidths=[3*inch, 3*inch])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0A1628')),
                ('TEXTCOLOR',  (0,0), (-1,0), colors.HexColor('#00D4FF')),
                ('FONTSIZE',   (0,0), (-1,-1), 9),
                ('GRID',       (0,0), (-1,-1), 0.5, colors.HexColor('#00D4FF40')),
                ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F5F8FF')]),
            ]))
            story.append(t)
            story.append(Spacer(1, 0.15*inch))

            story.append(Paragraph("Weight Summary", h2_style))
            ws_data = [['Component', 'Value (lbs)', '% W_TO']] + [
                [r['Parameter'], r['Value (lbs)'], r['% of W_TO']] for _, r in summary.iterrows()
            ]
            t2 = Table(ws_data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
            t2.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0A1628')),
                ('TEXTCOLOR',  (0,0), (-1,0), colors.HexColor('#00D4FF')),
                ('FONTSIZE',   (0,0), (-1,-1), 9),
                ('GRID',       (0,0), (-1,-1), 0.5, colors.HexColor('#00D4FF40')),
                ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F5F8FF')]),
            ]))
            story.append(t2)
            story.append(Spacer(1, 0.15*inch))

            story.append(Paragraph("Sensitivity Partials", h2_style))
            sp_data = [['Partial', 'Value', 'Units']] + [
                [r['Partial'], r['Value'], r['Units']] for _, r in pd.DataFrame(s_data_r).iterrows()
            ] + [
                [r['Partial'], r['Value'], r['Units']] for _, r in pd.DataFrame(s_data_l).iterrows()
            ]
            t3 = Table(sp_data, colWidths=[2.5*inch, 2*inch, 1.5*inch])
            t3.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0A1628')),
                ('TEXTCOLOR',  (0,0), (-1,0), colors.HexColor('#00D4FF')),
                ('FONTSIZE',   (0,0), (-1,-1), 9),
                ('GRID',       (0,0), (-1,-1), 0.5, colors.HexColor('#00D4FF40')),
                ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F5F8FF')]),
            ]))
            story.append(t3)

            doc.build(story)
            buf.seek(0)
            return buf.read()

        pdf_bytes = generate_pdf()
        st.download_button(
            label="⬇ DOWNLOAD PDF REPORT",
            data=pdf_bytes,
            file_name="aeronova_report.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

    st.markdown("---")
    st.markdown('<div class="section-header">CURRENT CONFIGURATION SNAPSHOT</div>', unsafe_allow_html=True)
    snap = pd.DataFrame({
        'Param': list(params.keys()),
        'Value': [str(v) for v in params.values()],
    })
    st.dataframe(snap, hide_index=True, use_container_width=True)
