import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import math
import io
from reportlab.lib.pagesizes import letter
from reportlab.lib imporimport streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
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

html, body, [class*="css"] { background-color: #050A14 !important; color: #C8D8F0 !important; }
.stApp { background: linear-gradient(135deg, #050A14 0%, #0A1628 50%, #050A14 100%); }
h1, h2, h3 { font-family: 'Orbitron', monospace !important; }

.main-title {
    font-family: 'Orbitron', monospace;
    font-size: 2.4rem; font-weight: 900;
    background: linear-gradient(90deg, #00D4FF, #8A2BE2, #00D4FF);
    background-size: 200%;
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    animation: shimmer 3s infinite;
    text-align: center; letter-spacing: 0.15em; margin-bottom: 0;
}
@keyframes shimmer { 0%{background-position:0%} 100%{background-position:200%} }

.subtitle {
    font-family: 'Share Tech Mono', monospace; color: #4FC3F7;
    text-align: center; font-size: 0.85rem; letter-spacing: 0.3em;
    margin-top: 0.2rem; margin-bottom: 1.5rem;
}
.metric-card {
    background: linear-gradient(135deg, #0D1F35, #0A1628);
    border: 1px solid #00D4FF33; border-radius: 12px;
    padding: 1.2rem 1.5rem; text-align: center;
    box-shadow: 0 0 20px #00D4FF15; margin-bottom: 0.5rem;
}
.metric-value {
    font-family: 'Orbitron', monospace; font-size: 1.8rem; font-weight: 700;
    color: #00D4FF; text-shadow: 0 0 10px #00D4FF80;
}
.metric-label {
    font-family: 'Share Tech Mono', monospace; font-size: 0.7rem;
    color: #7B9CC8; letter-spacing: 0.15em; margin-top: 0.3rem;
}
.metric-unit { font-size: 0.9rem; color: #4FC3F7; }
.section-header {
    font-family: 'Orbitron', monospace; font-size: 0.9rem; font-weight: 700;
    color: #8A2BE2; letter-spacing: 0.2em;
    border-bottom: 1px solid #8A2BE230; padding-bottom: 0.4rem;
    margin-bottom: 1rem; text-transform: uppercase;
}
.status-ok {
    background: #00FF8820; border: 1px solid #00FF8860; border-radius: 8px;
    padding: 0.5rem 1rem; font-family: 'Share Tech Mono', monospace;
    font-size: 0.85rem; color: #00FF88;
}
.status-warn {
    background: #FF880020; border: 1px solid #FF880060; border-radius: 8px;
    padding: 0.5rem 1rem; font-family: 'Share Tech Mono', monospace;
    font-size: 0.85rem; color: #FF8800;
}
.stButton > button {
    font-family: 'Orbitron', monospace !important;
    background: linear-gradient(90deg, #00D4FF20, #8A2BE220) !important;
    border: 1px solid #00D4FF60 !important; color: #00D4FF !important;
    border-radius: 8px !important; letter-spacing: 0.1em !important;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #07111F, #0A1628) !important;
    border-right: 1px solid #00D4FF20 !important;
}
.scan-line {
    background: repeating-linear-gradient(0deg, transparent, transparent 2px, #00D4FF04 2px, #00D4FF04 4px);
    pointer-events: none; position: fixed; top:0; left:0; width:100%; height:100%; z-index: 9999;
}
</style>
<div class="scan-line"></div>
""", unsafe_allow_html=True)


# ─── PHYSICS ENGINE ───────────────────────────────────────────────────────────

def compute_mission(params):
    p = params
    Wpl   = p['n_pax'] * (p['w_pax'] + p['w_bag']) + p['n_crew'] * 205 + p['n_att'] * 200
    Wcrew = p['n_crew'] * 205 + p['n_att'] * 200
    Wtfo  = p['Wto_guess'] * p['Mtfo']

    W1_Wto = 0.990
    W2_W1  = 0.995
    W3_W2  = 0.995
    W4_W3  = 0.985

    Rc_sm  = p['range_nm'] * 1.15078
    W5_W4  = 1.0 / math.exp(Rc_sm / (375.0 * (p['np_cruise'] / p['Cp_cruise']) * p['LD_cruise']))

    V_mph  = p['V_loiter_kts'] * 1.15078
    W6_W5  = 1.0 / math.exp(p['E_loiter'] / (375.0 * (1.0 / V_mph) * (p['np_loiter'] / p['Cp_loiter']) * p['LD_loiter']))

    W7_W6  = 0.985
    W8_W7  = 0.995

    Mff     = W1_Wto * W2_W1 * W3_W2 * W4_W3 * W5_W4 * W6_W5 * W7_W6 * W8_W7
    WF_used = p['Wto_guess'] * (1.0 - Mff)
    WF_res  = p['Wto_guess'] * p['Mres'] * (1.0 - Mff)
    WF      = WF_used + WF_res + Wtfo

    WOE_tent = p['Wto_guess'] - WF - Wpl
    WE_tent  = WOE_tent - Wtfo - Wcrew

    log_Wto  = math.log10(p['Wto_guess'])
    WE_allow = 10.0 ** ((log_Wto - p['A']) / p['B'])
    diff     = WE_allow - WE_tent

    fractions = {
        'Engine Start': W1_Wto, 'Taxi': W2_W1, 'Takeoff': W3_W2,
        'Climb': W4_W3, 'Cruise': W5_W4, 'Loiter': W6_W5,
        'Descent': W7_W6, 'Landing': W8_W7,
    }
    return {
        'Wpl': Wpl, 'Wcrew': Wcrew, 'Wtfo': Wtfo,
        'Mff': Mff, 'WF': WF, 'WOE': WOE_tent, 'WE': WE_tent,
        'WE_allow': WE_allow, 'diff': diff, 'fractions': fractions,
        'WF_used': WF_used,
    }


def solve_wto(params, tol=1.0, max_iter=200):
    p = dict(params)
    lo, hi = 5000.0, 500000.0
    mid = (lo + hi) / 2.0
    r = {}
    for _ in range(max_iter):
        mid = (lo + hi) / 2.0
        p['Wto_guess'] = mid
        r = compute_mission(p)
        if abs(r['diff']) < tol:
            break
        if r['diff'] > 0:
            hi = mid
        else:
            lo = mid
    return mid, r


def Wpl_from(p):
    return p['n_pax'] * (p['w_pax'] + p['w_bag']) + p['n_crew'] * 205 + p['n_att'] * 200


def sensitivity(params, Wto):
    p    = params
    Rc_sm = p['range_nm'] * 1.15078
    V_mph = p['V_loiter_kts'] * 1.15078
    Mff   = compute_mission({**p, 'Wto_guess': Wto})['Mff']

    C = 1.0 - (1.0 + p['Mres']) * (1.0 - Mff) - p['Mtfo']
    D = Wpl_from(p) + p['n_crew'] * 205 + p['n_att'] * 200
    B = p['B']

    numer = -B * Wto**2 * (1.0 + p['Mres']) * Mff
    denom = C * Wto * (1.0 - B) - D
    F     = numer / denom if abs(denom) > 1e-6 else 0.0

    dCp_R  =  F * Rc_sm / (375.0 * p['np_cruise'] * p['LD_cruise'])
    dnp_R  = -F * Rc_sm * p['Cp_cruise'] / (375.0 * p['np_cruise']**2 * p['LD_cruise'])
    dLD_R  = -F * Rc_sm * p['Cp_cruise'] / (375.0 * p['np_cruise'] * p['LD_cruise']**2)
    dR     =  F * p['Cp_cruise'] / (375.0 * p['np_cruise'] * p['LD_cruise'])

    E = p['E_loiter']
    dCp_E  =  F * E * V_mph / (375.0 * p['np_loiter'] * p['LD_loiter'])
    dnp_E  = -F * E * V_mph * p['Cp_loiter'] / (375.0 * p['np_loiter']**2 * p['LD_loiter'])
    dLD_E  = -F * E * V_mph * p['Cp_loiter'] / (375.0 * p['np_loiter'] * p['LD_loiter']**2)

    return {
        'F': F,
        'Range':  {'dCp': dCp_R,  'dnp': dnp_R,  'dLD': dLD_R,  'dR': dR},
        'Loiter': {'dCp': dCp_E,  'dnp': dnp_E,  'dLD': dLD_E},
    }


# ─── PLOTLY HELPERS ───────────────────────────────────────────────────────────
# Base layout dict — NO xaxis/yaxis keys here to avoid conflicts when
# per-chart axis options are passed separately via update_xaxes / update_yaxes.

BASE_LAYOUT = dict(
    paper_bgcolor='rgba(5,10,20,0)',
    plot_bgcolor='rgba(10,22,40,0.7)',
    font=dict(family='Share Tech Mono', color='#C8D8F0', size=11),
    margin=dict(l=55, r=20, t=45, b=45),
)

AXIS_STYLE = dict(gridcolor='#00D4FF12', linecolor='#00D4FF30', tickfont=dict(color='#4FC3F7'))


def apply_base(fig, title_text='', height=None, extra=None):
    """Apply BASE_LAYOUT plus optional title/height to a figure."""
    kw = dict(BASE_LAYOUT)
    if title_text:
        kw['title'] = dict(text=title_text, font=dict(color='#4FC3F7', size=13))
    if height:
        kw['height'] = height
    if extra:
        kw.update(extra)
    fig.update_layout(**kw)
    fig.update_xaxes(**AXIS_STYLE)
    fig.update_yaxes(**AXIS_STYLE)
    return fig


# ─── DEFAULTS ─────────────────────────────────────────────────────────────────

DEFAULTS = dict(
    n_pax=34, w_pax=175, w_bag=30, n_crew=2, n_att=1,
    Mtfo=0.005, Mres=0.0, range_nm=1100,
    V_cruise_kts=250, LD_cruise=13, Cp_cruise=0.60, np_cruise=0.85,
    E_loiter=0.75, V_loiter_kts=250, LD_loiter=16, Cp_loiter=0.65, np_loiter=0.77,
    A=0.3774, B=0.9647, Wto_guess=48550,
)


# ─── SIDEBAR ──────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown('<div class="main-title" style="font-size:1.1rem">⚙ PARAMETERS</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle" style="font-size:0.65rem">MISSION CONFIGURATION</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">PAYLOAD</div>', unsafe_allow_html=True)
    n_pax  = st.slider("Passengers",        10,  100, DEFAULTS['n_pax'])
    w_pax  = st.slider("Pax weight (lbs)", 140,  220, DEFAULTS['w_pax'])
    w_bag  = st.slider("Baggage (lbs)",     10,   60, DEFAULTS['w_bag'])
    n_crew = st.slider("Pilots",             1,    4, DEFAULTS['n_crew'])
    n_att  = st.slider("Attendants",         0,    4, DEFAULTS['n_att'])

    st.markdown('<div class="section-header">CRUISE PHASE</div>', unsafe_allow_html=True)
    range_nm  = st.slider("Range (nm)",            200, 3000, DEFAULTS['range_nm'], step=50)
    V_cruise  = st.slider("Cruise speed (kts)",    150,  400, DEFAULTS['V_cruise_kts'])
    LD_cruise = st.slider("Cruise L/D",              8,   22, DEFAULTS['LD_cruise'])
    Cp_cruise = st.slider("Cp cruise",             0.3,  1.0, DEFAULTS['Cp_cruise'], step=0.01)
    np_cruise = st.slider("η_p cruise",            0.5, 0.95, DEFAULTS['np_cruise'], step=0.01)

    st.markdown('<div class="section-header">LOITER PHASE</div>', unsafe_allow_html=True)
    E_loiter  = st.slider("Endurance (hr)",        0.1,  3.0, DEFAULTS['E_loiter'], step=0.05)
    V_loiter  = st.slider("Loiter speed (kts)",    100,  350, DEFAULTS['V_loiter_kts'])
    LD_loiter = st.slider("Loiter L/D",              8,   24, DEFAULTS['LD_loiter'])
    Cp_loiter = st.slider("Cp loiter",             0.3,  1.0, DEFAULTS['Cp_loiter'], step=0.01)
    np_loiter = st.slider("η_p loiter",            0.5, 0.95, DEFAULTS['np_loiter'], step=0.01)

    st.markdown('<div class="section-header">REGRESSION CONSTANTS</div>', unsafe_allow_html=True)
    A_coef = st.number_input("A (Table 2.2)", value=DEFAULTS['A'],    step=0.001, format="%.4f")
    B_coef = st.number_input("B (Table 2.2)", value=DEFAULTS['B'],    step=0.001, format="%.4f")
    Mtfo   = st.number_input("M_tfo",         value=DEFAULTS['Mtfo'], step=0.001, format="%.4f")


params = dict(
    n_pax=n_pax, w_pax=w_pax, w_bag=w_bag, n_crew=n_crew, n_att=n_att,
    Mtfo=Mtfo, Mres=0.0, range_nm=range_nm,
    V_cruise_kts=V_cruise, LD_cruise=LD_cruise, Cp_cruise=Cp_cruise, np_cruise=np_cruise,
    E_loiter=E_loiter, V_loiter_kts=V_loiter, LD_loiter=LD_loiter,
    Cp_loiter=Cp_loiter, np_loiter=np_loiter,
    A=A_coef, B=B_coef, Wto_guess=DEFAULTS['Wto_guess'],
)

Wto, result = solve_wto(params)
sens   = sensitivity(params, Wto)
sens_r = sens['Range']
sens_l = sens['Loiter']


# ─── HEADER ───────────────────────────────────────────────────────────────────

st.markdown('<h1 class="main-title">✈ AERONOVA SIMULATOR X</h1>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">PROPELLER-DRIVEN AIRCRAFT PRELIMINARY SIZING · BREGUET RANGE / ENDURANCE</div>', unsafe_allow_html=True)

if abs(result['diff']) < 5:
    st.markdown(f'<div class="status-ok">✔ CONVERGED — ΔWE = {result["diff"]:.2f} lbs &nbsp;|&nbsp; W_TO = {Wto:,.0f} lbs</div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div class="status-warn">⚠ CONVERGENCE DELTA: {result["diff"]:.1f} lbs</div>', unsafe_allow_html=True)

st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(["⬡ MISSION SIZING", "⬡ SENSITIVITY", "⬡ WEIGHT BREAKDOWN", "⬡ EXPORT"])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — MISSION SIZING
# ══════════════════════════════════════════════════════════════════════════════

with tab1:
    c1, c2, c3, c4 = st.columns(4)
    for col, val, unit, label in [
        (c1, f"{Wto:,.0f}",              "lbs", "GROSS WEIGHT W_TO"),
        (c2, f"{result['Mff']:.4f}",     "",    "FUEL FRACTION M_FF"),
        (c3, f"{result['WF']:,.0f}",     "lbs", "TOTAL FUEL W_F"),
        (c4, f"{result['Wpl']:,.0f}",    "lbs", "PAYLOAD W_PL"),
    ]:
        with col:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{val} <span class="metric-unit">{unit}</span></div><div class="metric-label">{label}</div></div>', unsafe_allow_html=True)

    st.markdown("&nbsp;")
    col_a, col_b = st.columns([1.1, 0.9])

    with col_a:
        st.markdown('<div class="section-header">MISSION WEIGHT FRACTIONS</div>', unsafe_allow_html=True)
        phases = list(result['fractions'].keys())
        fracs  = list(result['fractions'].values())

        # Use explicit per-bar colors (list of hex) — avoids colorscale+line conflict
        bar_colors = ['#8A2BE2','#7B6FD4','#6BB4C6','#00D4FF','#00C4EE','#00FF88','#00D070','#00B060']

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=phases, y=fracs,
            marker_color=bar_colors,
            name='Wi / Wi-1',
            text=[f'{v:.4f}' for v in fracs],
            textposition='outside',
            textfont=dict(size=10, color='#C8D8F0'),
        ))
        apply_base(fig, title_text='Phase Weight Fractions', height=340)
        fig.update_yaxes(range=[0.80, 1.02])
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
                'axis': {'range': [10000, 150000], 'tickcolor': '#4FC3F7',
                         'tickfont': {'size': 9}},
                'bar':  {'color': '#00D4FF', 'thickness': 0.25},
                'bgcolor': '#0A1628', 'borderwidth': 1, 'bordercolor': '#00D4FF30',
                'steps': [
                    {'range': [10000,  50000], 'color': '#00FF8810'},
                    {'range': [50000, 100000], 'color': '#00D4FF10'},
                    {'range': [100000,150000], 'color': '#FF3CAC10'},
                ],
                'threshold': {'line': {'color': '#FF3CAC', 'width': 2},
                              'thickness': 0.75, 'value': Wto},
            },
            title={'text': 'W_TO', 'font': {'color': '#7B9CC8', 'size': 12, 'family': 'Orbitron'}},
        ))
        fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                           font=dict(family='Share Tech Mono', color='#C8D8F0'),
                           height=280, margin=dict(t=30, b=10, l=20, r=20))
        st.plotly_chart(fig2, use_container_width=True)

        st.markdown('<div class="section-header">WE CONVERGENCE CHECK</div>', unsafe_allow_html=True)
        we_df = pd.DataFrame({
            'Parameter': ['WE Tentative', 'WE Allowable', 'Delta'],
            'Value (lbs)': [f"{result['WE']:,.1f}", f"{result['WE_allow']:,.1f}",
                            f"{result['diff']:+.2f}"],
        })
        st.dataframe(we_df, hide_index=True, use_container_width=True)

    # Range sweep
    st.markdown('<div class="section-header">W_TO vs RANGE SWEEP</div>', unsafe_allow_html=True)
    sweep_ranges = np.linspace(200, 3000, 60)
    sweep_wtos   = []
    for r_val in sweep_ranges:
        try:
            w, _ = solve_wto({**params, 'range_nm': float(r_val)})
            sweep_wtos.append(w)
        except Exception:
            sweep_wtos.append(float('nan'))

    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=sweep_ranges, y=sweep_wtos,
        mode='lines',
        line=dict(color='#00D4FF', width=2.5),
        fill='tozeroy', fillcolor='rgba(0,212,255,0.05)',
        name='W_TO',
    ))
    fig3.add_vline(x=range_nm, line_dash='dash', line_color='#FF3CAC', line_width=1.5,
                   annotation_text=f'Current: {range_nm} nm',
                   annotation_font_color='#FF3CAC')
    apply_base(fig3, title_text='Gross Takeoff Weight vs Range', height=320)
    fig3.update_xaxes(title_text='Range (nm)')
    fig3.update_yaxes(title_text='W_TO (lbs)')
    st.plotly_chart(fig3, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — SENSITIVITY
# ══════════════════════════════════════════════════════════════════════════════

with tab2:
    st.markdown('<div class="section-header">BREGUET SENSITIVITY PARTIALS (TABLE 2.20)</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Range phase**")
        s_data_r = {
            'Partial': ['∂WTO/∂Cp', '∂WTO/∂ηp', '∂WTO/∂(L/D)', '∂WTO/∂R'],
            'Value':   [f"{sens_r['dCp']:+,.1f}", f"{sens_r['dnp']:+,.1f}",
                        f"{sens_r['dLD']:+,.1f}", f"{sens_r['dR']:+,.2f}"],
            'Units':   ['lbs/(lbs/hp/hr)', 'lbs', 'lbs', 'lbs/nm'],
        }
        st.dataframe(pd.DataFrame(s_data_r), hide_index=True, use_container_width=True)

    with col2:
        st.markdown("**Loiter phase**")
        s_data_l = {
            'Partial': ['∂WTO/∂Cp', '∂WTO/∂ηp', '∂WTO/∂(L/D)'],
            'Value':   [f"{sens_l['dCp']:+,.1f}", f"{sens_l['dnp']:+,.1f}",
                        f"{sens_l['dLD']:+,.1f}"],
            'Units':   ['lbs/(lbs/hp/hr)', 'lbs', 'lbs'],
        }
        st.dataframe(pd.DataFrame(s_data_l), hide_index=True, use_container_width=True)

    # Tornado
    st.markdown('<div class="section-header">TORNADO DIAGRAM — W_TO SENSITIVITY</div>', unsafe_allow_html=True)

    t_labels = ['Cp (range)', 'ηp (range)', 'L/D (range)', 'R (range)',
                'Cp (loiter)', 'ηp (loiter)', 'L/D (loiter)']
    t_values = [sens_r['dCp'], sens_r['dnp'], sens_r['dLD'], sens_r['dR'] * range_nm * 0.1,
                sens_l['dCp'], sens_l['dnp'], sens_l['dLD']]

    order    = sorted(range(len(t_values)), key=lambda i: abs(t_values[i]))
    t_labels = [t_labels[i] for i in order]
    t_values = [t_values[i] for i in order]
    t_colors = ['#00D4FF' if v >= 0 else '#FF3CAC' for v in t_values]

    fig_t = go.Figure(go.Bar(
        x=t_values, y=t_labels,
        orientation='h',
        marker_color=t_colors,
        text=[f'{v:+,.0f}' for v in t_values],
        textposition='outside',
        textfont=dict(size=10),
    ))
    fig_t.add_vline(x=0, line_color='#C8D8F080', line_width=1)
    apply_base(fig_t, title_text='Tornado: ΔW_TO per unit change in parameter', height=380)
    fig_t.update_xaxes(title_text='ΔW_TO (lbs)')
    st.plotly_chart(fig_t, use_container_width=True)

    # 3D surface
    st.markdown('<div class="section-header">3D SURFACE — W_TO vs Cp × L/D (CRUISE)</div>', unsafe_allow_html=True)
    cp_arr = np.linspace(0.40, 0.90, 22)
    ld_arr = np.linspace(9.0, 20.0, 22)
    Z = np.zeros((len(cp_arr), len(ld_arr)))
    for i, cp in enumerate(cp_arr):
        for j, ld in enumerate(ld_arr):
            try:
                w, _ = solve_wto({**params, 'Cp_cruise': float(cp), 'LD_cruise': float(ld)})
                Z[i, j] = w
            except Exception:
                Z[i, j] = float('nan')

    fig4 = go.Figure(go.Surface(
        x=ld_arr, y=cp_arr, z=Z,
        colorscale=[[0,'#050A14'],[0.35,'#0A1628'],[0.65,'#00D4FF'],[1,'#8A2BE2']],
        opacity=0.90,
        contours=dict(z=dict(show=True, color='rgba(0,212,255,0.2)', width=1)),
        showscale=True,
        colorbar=dict(title=dict(text='W_TO (lbs)', font=dict(color='#4FC3F7', size=10)),
                      tickfont=dict(color='#C8D8F0', size=9)),
    ))
    fig4.update_layout(
        paper_bgcolor='rgba(5,10,20,0)',
        font=dict(family='Share Tech Mono', color='#C8D8F0', size=10),
        title=dict(text='3D: W_TO surface over Cp and L/D', font=dict(color='#4FC3F7', size=13)),
        scene=dict(
            xaxis=dict(title='L/D',        backgroundcolor='rgba(10,22,40,0.8)',
                       gridcolor='#00D4FF20', linecolor='#00D4FF40'),
            yaxis=dict(title='Cp',         backgroundcolor='rgba(10,22,40,0.8)',
                       gridcolor='#00D4FF20', linecolor='#00D4FF40'),
            zaxis=dict(title='W_TO (lbs)', backgroundcolor='rgba(10,22,40,0.8)',
                       gridcolor='#00D4FF20', linecolor='#00D4FF40'),
            bgcolor='rgba(5,10,20,0.95)',
        ),
        margin=dict(l=0, r=0, t=50, b=0),
        height=500,
    )
    st.plotly_chart(fig4, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — WEIGHT BREAKDOWN
# ══════════════════════════════════════════════════════════════════════════════

with tab3:
    st.markdown('<div class="section-header">FULL WEIGHT STACK</div>', unsafe_allow_html=True)

    WE    = result['WE']
    WOE   = result['WOE']
    WF    = result['WF']
    Wpl   = result['Wpl']
    Wcrew = result['Wcrew']
    Wtfo  = result['Wtfo']

    col_pie, col_bar = st.columns(2)

    with col_pie:
        fig_pie = go.Figure(go.Pie(
            labels=['Empty Weight', 'Fuel (usable)', 'Trapped Fuel/Oil', 'Crew', 'Payload'],
            values=[WE, result['WF_used'], Wtfo, Wcrew, Wpl],
            hole=0.5,
            marker=dict(
                colors=['#8A2BE2','#00D4FF','#FF6B35','#00FF88','#FFD700'],
                line=dict(color='#050A14', width=2),
            ),
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
            annotations=[dict(text=f'{Wto:,.0f}<br>lbs', x=0.5, y=0.5,
                               showarrow=False,
                               font=dict(size=14, color='#00D4FF', family='Orbitron'))],
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_bar:
        frac_vals  = list(result['fractions'].values())
        phase_labs = list(result['fractions'].keys()) + ['Landing (final)']
        cum = [Wto]
        for f in frac_vals:
            cum.append(cum[-1] * f)

        fig_w = go.Figure()
        fig_w.add_trace(go.Scatter(
            x=phase_labs, y=cum,
            mode='lines+markers',
            line=dict(color='#00D4FF', width=2.5),
            marker=dict(color='#8A2BE2', size=8,
                        line=dict(color='#00D4FF', width=1.5)),
        ))
        apply_base(fig_w, title_text='Weight Through Mission Phases', height=320)
        fig_w.update_xaxes(title_text='Phase')
        fig_w.update_yaxes(title_text='Aircraft Weight (lbs)')
        st.plotly_chart(fig_w, use_container_width=True)

    # Summary table
    st.markdown('<div class="section-header">WEIGHT SUMMARY TABLE</div>', unsafe_allow_html=True)
    summary = pd.DataFrame({
        'Weight Component': ['W_TO (Gross)', 'W_E (Empty)', 'W_OE (Op. Empty)',
                              'W_F (Total Fuel)', 'W_F (Usable)', 'W_tfo', 'W_crew', 'W_payload'],
        'Value (lbs)':      [f"{Wto:,.1f}", f"{WE:,.1f}", f"{WOE:,.1f}",
                              f"{WF:,.1f}", f"{result['WF_used']:,.1f}",
                              f"{Wtfo:,.2f}", f"{Wcrew:,.0f}", f"{Wpl:,.0f}"],
        '% of W_TO':        [f"{100:.1f}%",
                              f"{WE/Wto*100:.1f}%",    f"{WOE/Wto*100:.1f}%",
                              f"{WF/Wto*100:.1f}%",    f"{result['WF_used']/Wto*100:.1f}%",
                              f"{Wtfo/Wto*100:.2f}%",  f"{Wcrew/Wto*100:.2f}%",
                              f"{Wpl/Wto*100:.1f}%"],
    })
    st.dataframe(summary, hide_index=True, use_container_width=True)

    # Payload–Range
    st.markdown('<div class="section-header">W_TO vs PASSENGER COUNT</div>', unsafe_allow_html=True)
    pax_arr  = np.arange(5, n_pax + 20, 2)
    wtos_pax = []
    for np_ in pax_arr:
        try:
            w, _ = solve_wto({**params, 'n_pax': int(np_)})
            wtos_pax.append(w)
        except Exception:
            wtos_pax.append(float('nan'))

    fig_pr = go.Figure()
    fig_pr.add_trace(go.Scatter(
        x=pax_arr, y=wtos_pax,
        mode='lines+markers',
        line=dict(color='#00FF88', width=2),
        marker=dict(size=5),
        fill='tozeroy', fillcolor='rgba(0,255,136,0.04)',
    ))
    fig_pr.add_vline(x=n_pax, line_dash='dot', line_color='#FFD700', line_width=1.5,
                     annotation_text=f'{n_pax} pax', annotation_font_color='#FFD700')
    apply_base(fig_pr, title_text='W_TO vs Passenger Count', height=300)
    fig_pr.update_xaxes(title_text='Passengers')
    fig_pr.update_yaxes(title_text='W_TO (lbs)')
    st.plotly_chart(fig_pr, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — EXPORT
# ══════════════════════════════════════════════════════════════════════════════

with tab4:
    st.markdown('<div class="section-header">EXPORT RESULTS</div>', unsafe_allow_html=True)
    col_e1, col_e2 = st.columns(2)

    with col_e1:
        st.markdown("**CSV — Full Results**")
        export_rows = {
            'Parameter': ['W_TO','Mff','W_F','W_payload','W_empty','W_OE',
                           'W_crew','W_tfo','WE_allow','Convergence_delta',
                           'dWTO_dCp_range','dWTO_dnp_range','dWTO_dLD_range','dWTO_dR',
                           'dWTO_dCp_loiter','dWTO_dnp_loiter','dWTO_dLD_loiter'],
            'Value':     [Wto, result['Mff'], WF, Wpl, WE, WOE, Wcrew, Wtfo,
                           result['WE_allow'], result['diff'],
                           sens_r['dCp'], sens_r['dnp'], sens_r['dLD'], sens_r['dR'],
                           sens_l['dCp'], sens_l['dnp'], sens_l['dLD']],
            'Units':     ['lbs','–','lbs','lbs','lbs','lbs','lbs','lbs','lbs','lbs',
                           'lbs/(lbs/hp/hr)','lbs','lbs','lbs/nm',
                           'lbs/(lbs/hp/hr)','lbs','lbs'],
        }
        buf_csv = io.StringIO()
        pd.DataFrame(export_rows).to_csv(buf_csv, index=False)
        st.download_button("⬇ DOWNLOAD CSV", buf_csv.getvalue(),
                           "aeronova_results.csv", "text/csv", use_container_width=True)

        st.markdown("**Weight fractions CSV**")
        buf_frac = io.StringIO()
        pd.DataFrame({'Phase': list(result['fractions'].keys()),
                       'Wi/Wi-1': list(result['fractions'].values())}).to_csv(buf_frac, index=False)
        st.download_button("⬇ DOWNLOAD FRACTIONS CSV", buf_frac.getvalue(),
                           "aeronova_fractions.csv", "text/csv", use_container_width=True)

    with col_e2:
        st.markdown("**PDF — Mission Report**")

        def generate_pdf():
            buf = io.BytesIO()
            doc = SimpleDocTemplate(buf, pagesize=letter,
                                    leftMargin=0.75*inch, rightMargin=0.75*inch,
                                    topMargin=0.75*inch, bottomMargin=0.75*inch)
            styles    = getSampleStyleSheet()
            sty_title = ParagraphStyle('T', parent=styles['Title'], fontSize=18,
                                        textColor=colors.HexColor('#00D4FF'), spaceAfter=6)
            sty_h2    = ParagraphStyle('H', parent=styles['Heading2'], fontSize=12,
                                        textColor=colors.HexColor('#8A2BE2'),
                                        spaceBefore=12, spaceAfter=4)
            sty_body  = ParagraphStyle('B', parent=styles['Normal'], fontSize=9, leading=13)

            tbl_style = TableStyle([
                ('BACKGROUND',    (0,0), (-1,0), colors.HexColor('#0A1628')),
                ('TEXTCOLOR',     (0,0), (-1,0), colors.HexColor('#00D4FF')),
                ('FONTSIZE',      (0,0), (-1,-1), 9),
                ('GRID',          (0,0), (-1,-1), 0.5, colors.HexColor('#334466')),
                ('ROWBACKGROUNDS',(0,1), (-1,-1), [colors.white, colors.HexColor('#F5F8FF')]),
            ])

            story = [
                Paragraph("AeroNova Simulator X — Mission Report", sty_title),
                Paragraph("Propeller-Driven Aircraft Preliminary Sizing (Breguet Method)", sty_body),
                Spacer(1, 0.2*inch),
                Paragraph("Mission Parameters", sty_h2),
            ]

            mp = Table([['Parameter','Value'],
                         ['Passengers', str(n_pax)], ['Crew', str(n_crew)],
                         ['Range (nm)', str(range_nm)], ['Cruise L/D', str(LD_cruise)],
                         ['Loiter endurance (hr)', str(E_loiter)]],
                        colWidths=[3*inch, 3*inch])
            mp.setStyle(tbl_style)
            story += [mp, Spacer(1, 0.15*inch), Paragraph("Weight Summary", sty_h2)]

            ws = Table([['Component', 'Value (lbs)', '% W_TO']] +
                        list(zip(summary['Weight Component'],
                                  summary['Value (lbs)'],
                                  summary['% of W_TO'])),
                        colWidths=[3*inch, 1.5*inch, 1.5*inch])
            ws.setStyle(tbl_style)
            story += [ws, Spacer(1, 0.15*inch), Paragraph("Sensitivity Partials", sty_h2)]

            sp = Table([['Partial','Value','Units']] +
                        list(zip(s_data_r['Partial'], s_data_r['Value'], s_data_r['Units'])) +
                        list(zip(s_data_l['Partial'], s_data_l['Value'], s_data_l['Units'])),
                        colWidths=[2.5*inch, 2*inch, 1.5*inch])
            sp.setStyle(tbl_style)
            story.append(sp)

            doc.build(story)
            buf.seek(0)
            return buf.read()

        st.download_button("⬇ DOWNLOAD PDF REPORT", generate_pdf(),
                           "aeronova_report.pdf", "application/pdf", use_container_width=True)

    st.markdown("---")
    st.markdown('<div class="section-header">CURRENT CONFIGURATION SNAPSHOT</div>', unsafe_allow_html=True)
    st.dataframe(pd.DataFrame({'Param': list(params.keys()),
                                'Value': [str(v) for v in params.values()]}),
                 hide_index=True, use_container_width=True)t colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch

# --- 1. CONFIGURATION & STYLES ---
st.set_page_config(page_title="AeroNova Simulator X", layout="wide")

# تعريف التنسيق الصحيح للمحاور (تم حذف المفاتيح المسببة للأخطاء)
AXIS_STYLE = dict(
    showgrid=True,
    gridcolor='#1f2937',
    zeroline=False,
    tickfont=dict(color='#C8D8F0', size=10),
    title_font=dict(color='#00D4FF', size=12)
)

def apply_base(fig, title_text='', height=340):
    """دالة تنسيق الرسوم البيانية - مصححة لتجنب ValueError"""
    fig.update_layout(
        title=dict(text=title_text, font=dict(color='#00D4FF', size=16)),
        height=height,
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=40, r=20, t=60, b=40)
    )
    # استخدام التحديث بشكل منفصل لكل محور لضمان الاستقرار
    fig.update_xaxes(**AXIS_STYLE)
    fig.update_yaxes(**AXIS_STYLE)

# --- 2. PHYSICS ENGINE ---
def compute_mission(p):
    try:
        Wpl = (p['n_pax'] * (p['w_pax'] + p['w_bag'])) + p['n_crew'] * 205 + (p['n_att'] * 200)
        Wcrew = p['n_crew'] * 205 + p['n_att'] * 200
        Wtfo = p['Wto_guess'] * p['Mtfo']

        Rc_sm = p['range_nm'] * 1.15078
        denom = (375 * (p['np_cruise'] / p['Cp_cruise']) * p['LD_cruise'])
        if denom <= 0: return None
        
        f_cruise = math.exp(-Rc_sm / denom)
        mff = 0.970 * f_cruise * 0.990 
        
        wf = p['Wto_guess'] * (1 - mff) * (1 + p['Mres'])
        we_tent = p['Wto_guess'] - wf - Wpl - Wtfo - Wcrew
        
        # حماية اللوغاريتم
        wto_safe = max(100, p['Wto_guess'])
        we_allow = 10 ** ((math.log10(wto_safe) - p['A']) / p['B'])
        
        return {
            'Wpl': Wpl, 'WF': wf, 'WE': we_tent, 'WE_allow': we_allow, 
            'diff': we_allow - we_tent, 'Mff': mff,
            'fractions': {'Start': 0.99, 'Climb': 0.98, 'Cruise': round(f_cruise, 3), 'Landing': 0.99}
        }
    except: return None

def solve_wto(params):
    lo, hi = 5000, 800000
    for _ in range(50):
        mid = (lo + hi) / 2
        params['Wto_guess'] = mid
        res = compute_mission(params)
        if res is None: break
        if abs(res['diff']) < 1.0: return mid, res
        if res['diff'] > 0: hi = mid
        else: lo = mid
    return mid, res

# --- 3. UI & DISPLAY ---
st.markdown("<h1 style='text-align: center; color: #00D4FF;'>AERONOVA ESTIMATOR X</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.header("Parameters")
    pax = st.slider("Passengers", 10, 100, 34)
    dist = st.slider("Range (nm)", 200, 3000, 1200)
    sfc = st.number_input("SFC", value=0.6)

params = {
    'n_pax': pax, 'w_pax': 175, 'w_bag': 30, 'n_crew': 2, 'n_att': 1,
    'Mtfo': 0.005, 'Mres': 0.05, 'range_nm': dist, 'np_cruise': 0.85,
    'Cp_cruise': sfc, 'LD_cruise': 13, 'A': 0.3774, 'B': 0.9647
}

wto_final, result = solve_wto(params)

if result:
    c1, c2, c3 = st.columns(3)
    c1.metric("Gross Weight", f"{wto_final:,.0f} lb")
    c2.metric("Empty Weight", f"{result['WE']:,.0f} lb")
    c3.metric("Fuel Weight", f"{result['WF']:,.0f} lb")

    # --- رسم بياني باستخدام دالة apply_base المصححة ---
    st.write("### Mission Weight Fractions")
    fig = go.Figure(go.Bar(
        x=list(result['fractions'].keys()), 
        y=list(result['fractions'].values()),
        marker_color='#00D4FF'
    ))
    
    # استدعاء الدالة (هنا كان الخطأ 333)
    apply_base(fig, title_text='Phase Weight Fractions', height=340)
    fig.update_yaxes(range=[0.80, 1.02]) # تعيين المدى بشكل آمن
    
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("⚠️ يرجى مراجعة المدخلات، لم يتم الوصول لنقطة تقارب.")
