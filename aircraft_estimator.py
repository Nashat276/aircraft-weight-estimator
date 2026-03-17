import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import math, io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch

st.set_page_config(page_title="AeroWeight Pro", page_icon="✈", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;600;700&family=Space+Mono&display=swap');
*{box-sizing:border-box}
html,body,[class*="css"]{background:#0F1117!important;color:#E8EAF0!important;font-family:'Space Grotesk',sans-serif!important}
.stApp{background:radial-gradient(ellipse at top,#1a1f2e 0%,#0F1117 60%)}
.brand{font-family:'Space Mono',monospace;font-size:1.9rem;font-weight:700;
  letter-spacing:.08em;text-align:center;color:#fff;margin-bottom:.2rem}
.brand span{color:#6C63FF}
.tagline{font-family:'Space Mono',monospace;font-size:.72rem;color:#6B7280;
  text-align:center;letter-spacing:.22em;margin-bottom:1.8rem}
.kpi-wrap{background:linear-gradient(135deg,#1C2030,#161B27);border:1px solid #2A2F45;
  border-radius:16px;padding:1.1rem 1.4rem;text-align:center;transition:.2s}
.kpi-wrap:hover{border-color:#6C63FF55;box-shadow:0 0 18px #6C63FF18}
.kpi-val{font-family:'Space Mono',monospace;font-size:1.65rem;font-weight:700;color:#6C63FF;line-height:1}
.kpi-unit{font-size:.8rem;color:#9CA3AF;margin-left:.3rem}
.kpi-lbl{font-size:.62rem;color:#6B7280;letter-spacing:.12em;margin-top:.4rem;text-transform:uppercase}
.blk{background:#161B27;border:1px solid #252B3B;border-radius:14px;padding:1.2rem 1.4rem;margin-bottom:1rem}
.blk-title{font-family:'Space Mono',monospace;font-size:.78rem;color:#6C63FF;
  letter-spacing:.15em;text-transform:uppercase;margin-bottom:.9rem;
  border-bottom:1px solid #252B3B;padding-bottom:.4rem}
.ok-banner{background:#0D2818;border:1px solid #16A34A55;border-radius:10px;
  padding:.55rem 1.1rem;font-family:'Space Mono',monospace;font-size:.82rem;color:#4ADE80}
.warn-banner{background:#2D1A0E;border:1px solid #EA580C55;border-radius:10px;
  padding:.55rem 1.1rem;font-family:'Space Mono',monospace;font-size:.82rem;color:#FB923C}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#0D1020,#0F1117)!important;
  border-right:1px solid #1E2230!important}
div[data-testid="stSidebar"] .stSlider>div>div{background:#1C2030!important}
.stTabs [data-baseweb="tab-list"]{background:#161B27;border-radius:10px;padding:3px}
.stTabs [data-baseweb="tab"]{border-radius:8px;font-family:'Space Mono',monospace;
  font-size:.72rem;letter-spacing:.08em;color:#6B7280}
.stTabs [aria-selected="true"]{background:#6C63FF!important;color:#fff!important}
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════
# PLOTLY SAFE WRAPPER
# Rule: update_layout gets ZERO xaxis/yaxis keys.
# Axes styled exclusively via update_xaxes / update_yaxes.
# ═══════════════════════════════════════════════════════════════════
_BASE = dict(
    paper_bgcolor='rgba(15,17,23,0)',
    plot_bgcolor='rgba(22,27,39,0.85)',
    font=dict(family='Space Mono', color='#9CA3AF', size=10),
    margin=dict(l=50, r=16, t=40, b=42),
    hoverlabel=dict(bgcolor='#1C2030', font_size=11),
)
_AX = dict(gridcolor='#252B3B', linecolor='#2A2F45', zerolinecolor='#2A2F45')

def _fig(fig, title='', h=340, xt='', yt='', yr=None):
    kw = dict(_BASE)
    if title: kw['title'] = dict(text=title, font=dict(color='#A5B4FC', size=12), x=0.01)
    kw['height'] = h
    fig.update_layout(**kw)
    fig.update_xaxes(**_AX)
    fig.update_yaxes(**_AX)
    if xt: fig.update_xaxes(title_text=xt, title_font=dict(size=10))
    if yt: fig.update_yaxes(title_text=yt, title_font=dict(size=10))
    if yr: fig.update_yaxes(range=yr)
    return fig


# ═══════════════════════════════════════════════════════════════════
# PHYSICS
# ═══════════════════════════════════════════════════════════════════
def mission(p):
    Wpl   = p['npax']*(p['wpax']+p['wbag']) + p['ncrew']*205 + p['natt']*200
    Wcrew = p['ncrew']*205 + p['natt']*200
    Wtfo  = p['Wto']*p['Mtfo']
    Rc    = p['R']*1.15078
    W5    = 1/math.exp(Rc/(375*(p['npc']/p['Cpc'])*p['LDc']))
    Vm    = p['Vl']*1.15078
    W6    = 1/math.exp(p['El']/(375*(1/Vm)*(p['npl']/p['Cpl'])*p['LDl']))
    fnames = ['Engine Start','Taxi','Takeoff','Climb','Cruise','Loiter','Descent','Landing']
    fvals  = [0.990, 0.995, 0.995, 0.985, W5, W6, 0.985, 0.995]
    fracs  = dict(zip(fnames, fvals))
    Mff = 1.0
    for v in fvals: Mff *= v
    WFu  = p['Wto']*(1-Mff)
    WF   = WFu + p['Wto']*p['Mr']*(1-Mff) + Wtfo
    WOE  = p['Wto'] - WF - Wpl
    WE   = WOE - Wtfo - Wcrew
    WEa  = 10**((math.log10(p['Wto'])-p['A'])/p['B'])
    return dict(Wpl=Wpl,Wcrew=Wcrew,Wtfo=Wtfo,Mff=Mff,WF=WF,WFu=WFu,
                WOE=WOE,WE=WE,WEa=WEa,diff=WEa-WE,fracs=fracs)

def solve(p, tol=0.5, n=300):
    pp=dict(p); lo,hi=4000.,600000.; r={}
    for _ in range(n):
        m=(lo+hi)/2; pp['Wto']=m; r=mission(pp)
        if abs(r['diff'])<tol: break
        if r['diff']>0: hi=m
        else: lo=m
    return m,r

def sens(p, Wto):
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


# ═══════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════
D = dict(npax=34,wpax=175,wbag=30,ncrew=2,natt=1,Mtfo=0.005,Mr=0.0,
         R=1100,Vl=250,LDc=13,Cpc=0.60,npc=0.85,
         El=0.75,LDl=16,Cpl=0.65,npl=0.77,A=0.3774,B=0.9647)

with st.sidebar:
    st.markdown('<div class="brand">AERO<span>WEIGHT</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="tagline">PRELIMINARY SIZING TOOL</div>', unsafe_allow_html=True)

    with st.expander("PAYLOAD", expanded=True):
        npax  = st.slider("Passengers",       10,100,D['npax'])
        wpax  = st.slider("Pax weight (lbs)",140,220,D['wpax'])
        wbag  = st.slider("Baggage (lbs)",    10, 60,D['wbag'])
        ncrew = st.slider("Pilots",            1,  4,D['ncrew'])
        natt  = st.slider("Attendants",        0,  4,D['natt'])

    with st.expander("CRUISE", expanded=True):
        R_nm = st.slider("Range (nm)",      200,3000,D['R'],step=50)
        LDc  = st.slider("L/D cruise",        8,  22,D['LDc'])
        Cpc  = st.slider("Cp cruise",        0.3, 1.0,D['Cpc'],step=0.01)
        npc  = st.slider("np cruise",        0.5,0.95,D['npc'],step=0.01)

    with st.expander("LOITER", expanded=False):
        El   = st.slider("Endurance (hr)",  0.1, 3.0,D['El'],step=0.05)
        Vl   = st.slider("Loiter spd (kts)",100, 350,D['Vl'])
        LDl  = st.slider("L/D loiter",        8,  24,D['LDl'])
        Cpl  = st.slider("Cp loiter",        0.3, 1.0,D['Cpl'],step=0.01)
        npl  = st.slider("np loiter",        0.5,0.95,D['npl'],step=0.01)

    with st.expander("REGRESSION CONSTANTS", expanded=False):
        A_v  = st.number_input("A",    value=D['A'],   step=0.001,format="%.4f")
        B_v  = st.number_input("B",    value=D['B'],   step=0.001,format="%.4f")
        Mtfo = st.number_input("M_tfo",value=D['Mtfo'],step=0.001,format="%.4f")

P = dict(npax=npax,wpax=wpax,wbag=wbag,ncrew=ncrew,natt=natt,
         Mtfo=Mtfo,Mr=0.0,R=R_nm,Vl=Vl,LDc=LDc,Cpc=Cpc,npc=npc,
         El=El,LDl=LDl,Cpl=Cpl,npl=npl,A=A_v,B=B_v,Wto=48550)

Wto, RR = solve(P)
S = sens(P, Wto)


# ═══════════════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════════════
st.markdown('<div class="brand" style="font-size:2rem">AERO<span>WEIGHT</span> PRO</div>', unsafe_allow_html=True)
st.markdown('<div class="tagline">BREGUET RANGE / ENDURANCE · PROPELLER AIRCRAFT SIZING</div>', unsafe_allow_html=True)

if abs(RR['diff']) < 5:
    st.markdown(f'<div class="ok-banner">✓ CONVERGED — W_TO = {Wto:,.0f} lbs &nbsp;|&nbsp; ΔWE = {RR["diff"]:.2f} lbs</div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div class="warn-banner">⚠ NOT CONVERGED — ΔWE = {RR["diff"]:.1f} lbs</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# KPI row
k1,k2,k3,k4,k5 = st.columns(5)
for col,val,unit,lbl in [
    (k1, f"{Wto:,.0f}",         "lbs", "Gross Weight W_TO"),
    (k2, f"{RR['Mff']:.4f}",    "",    "Fuel Fraction Mff"),
    (k3, f"{RR['WF']:,.0f}",    "lbs", "Total Fuel"),
    (k4, f"{RR['Wpl']:,.0f}",   "lbs", "Payload"),
    (k5, f"{RR['WE']:,.0f}",    "lbs", "Empty Weight"),
]:
    with col:
        st.markdown(f'<div class="kpi-wrap"><div class="kpi-val">{val}<span class="kpi-unit">{unit}</span></div><div class="kpi-lbl">{lbl}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["  MISSION  ", "  SENSITIVITY  ", "  WEIGHTS  ", "  EXPORT  "])


# ═══════════════════════════════════════════════════════════════════
# TAB 1 — MISSION
# ═══════════════════════════════════════════════════════════════════
with tab1:
    colA, colB = st.columns([3, 2])

    with colA:
        st.markdown('<div class="blk"><div class="blk-title">Phase Weight Fractions</div>', unsafe_allow_html=True)
        phases = list(RR['fracs'].keys())
        fvals  = list(RR['fracs'].values())
        COLORS = ['#6C63FF','#7C73FF','#4ECDC4','#45B7D1','#96E6A1','#D4EDDA','#A8DADC','#457B9D']
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=phases, y=fvals,
            marker_color=COLORS,
            text=[f'{v:.4f}' for v in fvals],
            textposition='outside',
            textfont=dict(size=9),
        ))
        _fig(fig, h=300, yr=[0.80, 1.02])
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="blk"><div class="blk-title">W_TO vs Range Sweep</div>', unsafe_allow_html=True)
        rr = np.linspace(200, 3000, 55)
        ww = []
        for rv in rr:
            try: w,_ = solve({**P,'R':float(rv)}); ww.append(w)
            except: ww.append(float('nan'))
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(
            x=rr, y=ww, mode='lines',
            line=dict(color='#6C63FF', width=2.5),
            fill='tozeroy', fillcolor='rgba(108,99,255,0.07)',
        ))
        fig3.add_vline(x=R_nm, line_dash='dot', line_color='#4ECDC4', line_width=1.5,
                       annotation_text=f'{R_nm} nm', annotation_font_color='#4ECDC4',
                       annotation_font_size=10)
        _fig(fig3, h=260, xt='Range (nm)', yt='W_TO (lbs)')
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with colB:
        st.markdown('<div class="blk"><div class="blk-title">W_TO Gauge</div>', unsafe_allow_html=True)
        fig2 = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=Wto,
            delta={'reference': 48550, 'relative': False,
                   'increasing': {'color': '#FB923C'},
                   'decreasing': {'color': '#4ADE80'}},
            number={'suffix': ' lbs', 'font': {'color': '#6C63FF', 'size': 18, 'family': 'Space Mono'}},
            gauge={
                'axis': {'range': [10000, 150000], 'tickfont': {'size': 8}},
                'bar': {'color': '#6C63FF', 'thickness': 0.22},
                'bgcolor': '#161B27',
                'borderwidth': 1, 'bordercolor': '#2A2F45',
                'steps': [
                    {'range': [10000,  50000], 'color': '#0D2818'},
                    {'range': [50000, 100000], 'color': '#161B27'},
                    {'range': [100000,150000], 'color': '#2D1A0E'},
                ],
                'threshold': {'line': {'color': '#FB923C', 'width': 2},
                              'thickness': 0.75, 'value': Wto},
            },
            title={'text': 'Gross Takeoff Weight',
                   'font': {'color': '#6B7280', 'size': 10, 'family': 'Space Mono'}},
        ))
        fig2.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Space Mono', color='#9CA3AF'),
            height=270, margin=dict(t=35, b=10, l=15, r=15),
        )
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="blk"><div class="blk-title">Convergence Check</div>', unsafe_allow_html=True)
        st.dataframe(pd.DataFrame({
            'Item': ['WE Tentative', 'WE Allowable', 'Delta'],
            'Value (lbs)': [f"{RR['WE']:,.1f}", f"{RR['WEa']:,.1f}", f"{RR['diff']:+.2f}"],
        }), hide_index=True, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="blk"><div class="blk-title">Mission Phases</div>', unsafe_allow_html=True)
        phase_df = pd.DataFrame({
            'Phase': list(RR['fracs'].keys()),
            'Wi / Wi-1': [f"{v:.4f}" for v in RR['fracs'].values()],
        })
        st.dataframe(phase_df, hide_index=True, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════
# TAB 2 — SENSITIVITY
# ═══════════════════════════════════════════════════════════════════
with tab2:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="blk"><div class="blk-title">Range Partials</div>', unsafe_allow_html=True)
        sdr = {'Partial': ['dWTO/dCp', 'dWTO/dnp', 'dWTO/d(L/D)', 'dWTO/dR'],
               'Value':   [f"{S['dCpR']:+,.1f}", f"{S['dnpR']:+,.1f}",
                           f"{S['dLDR']:+,.1f}", f"{S['dR']:+,.2f}"],
               'Units':   ['lbs/(lbs/hp/hr)', 'lbs', 'lbs', 'lbs/nm']}
        st.dataframe(pd.DataFrame(sdr), hide_index=True, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="blk"><div class="blk-title">Loiter Partials</div>', unsafe_allow_html=True)
        sdl = {'Partial': ['dWTO/dCp', 'dWTO/dnp', 'dWTO/d(L/D)'],
               'Value':   [f"{S['dCpE']:+,.1f}", f"{S['dnpE']:+,.1f}", f"{S['dLDE']:+,.1f}"],
               'Units':   ['lbs/(lbs/hp/hr)', 'lbs', 'lbs']}
        st.dataframe(pd.DataFrame(sdl), hide_index=True, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="blk"><div class="blk-title">Tornado Diagram</div>', unsafe_allow_html=True)
    tlbl = ['Cp(R)', 'np(R)', 'L/D(R)', 'R', 'Cp(E)', 'np(E)', 'L/D(E)']
    tval = [S['dCpR'], S['dnpR'], S['dLDR'], S['dR']*R_nm*0.1,
            S['dCpE'], S['dnpE'], S['dLDE']]
    idx  = sorted(range(7), key=lambda i: abs(tval[i]))
    tlbl = [tlbl[i] for i in idx]
    tval = [tval[i] for i in idx]
    fig_t = go.Figure(go.Bar(
        x=tval, y=tlbl, orientation='h',
        marker_color=['#6C63FF' if v >= 0 else '#FB923C' for v in tval],
        text=[f'{v:+,.0f}' for v in tval],
        textposition='outside',
        textfont=dict(size=9),
    ))
    fig_t.add_vline(x=0, line_color='#2A2F45', line_width=1.5)
    _fig(fig_t, h=360, xt='ΔW_TO (lbs)')
    st.plotly_chart(fig_t, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="blk"><div class="blk-title">3D Surface: W_TO over Cp × L/D</div>', unsafe_allow_html=True)
    cpa = np.linspace(0.40, 0.90, 20)
    lda = np.linspace(9.0, 20.0, 20)
    Z   = np.zeros((len(cpa), len(lda)))
    for i, cp in enumerate(cpa):
        for j, ld in enumerate(lda):
            try: w,_ = solve({**P,'Cpc':float(cp),'LDc':float(ld)}); Z[i,j] = w
            except: Z[i,j] = float('nan')
    fig4 = go.Figure(go.Surface(
        x=lda, y=cpa, z=Z,
        colorscale=[[0,'#0F1117'],[0.3,'#1C2030'],[0.65,'#6C63FF'],[1,'#4ECDC4']],
        opacity=0.92, showscale=True,
        colorbar=dict(tickfont=dict(size=9), len=0.7),
    ))
    fig4.update_layout(
        paper_bgcolor='rgba(15,17,23,0)',
        font=dict(family='Space Mono', color='#9CA3AF', size=9),
        title=dict(text='W_TO surface over Cp and L/D',
                   font=dict(color='#A5B4FC', size=12), x=0.01),
        scene=dict(
            xaxis=dict(title='L/D'),
            yaxis=dict(title='Cp'),
            zaxis=dict(title='W_TO (lbs)'),
        ),
        margin=dict(l=0, r=0, t=45, b=0),
        height=480,
    )
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════
# TAB 3 — WEIGHTS
# ═══════════════════════════════════════════════════════════════════
with tab3:
    WE=RR['WE']; WOE=RR['WOE']; WF=RR['WF']
    Wpl=RR['Wpl']; Wcrew=RR['Wcrew']; Wtfo=RR['Wtfo']

    pa, pb = st.columns(2)
    with pa:
        st.markdown('<div class="blk"><div class="blk-title">W_TO Breakdown</div>', unsafe_allow_html=True)
        fig_p = go.Figure(go.Pie(
            labels=['Empty', 'Fuel (usable)', 'Trapped fuel', 'Crew', 'Payload'],
            values=[WE, RR['WFu'], Wtfo, Wcrew, Wpl],
            hole=0.52,
            marker=dict(
                colors=['#6C63FF','#4ECDC4','#45B7D1','#96E6A1','#A8DADC'],
                line=dict(color='#0F1117', width=2),
            ),
            textfont=dict(size=10),
            textinfo='label+percent',
        ))
        fig_p.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Space Mono', color='#9CA3AF'),
            showlegend=False,
            height=300,
            margin=dict(t=20, b=10, l=10, r=10),
            annotations=[dict(text=f'{Wto:,.0f}<br>lbs', x=0.5, y=0.5,
                               showarrow=False, font=dict(size=12, color='#6C63FF',
                                                           family='Space Mono'))],
        )
        st.plotly_chart(fig_p, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with pb:
        st.markdown('<div class="blk"><div class="blk-title">Weight Through Mission</div>', unsafe_allow_html=True)
        fv = list(RR['fracs'].values())
        pl = list(RR['fracs'].keys()) + ['End']
        cum = [Wto]
        for f in fv: cum.append(cum[-1]*f)
        fig_w = go.Figure()
        fig_w.add_trace(go.Scatter(
            x=pl, y=cum, mode='lines+markers',
            line=dict(color='#6C63FF', width=2.5),
            marker=dict(color='#4ECDC4', size=7, line=dict(color='#6C63FF', width=1.5)),
            fill='tozeroy', fillcolor='rgba(108,99,255,0.06)',
        ))
        _fig(fig_w, h=300, xt='Phase', yt='Weight (lbs)')
        st.plotly_chart(fig_w, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="blk"><div class="blk-title">Weight Summary Table</div>', unsafe_allow_html=True)
    summary = pd.DataFrame({
        'Component': ['W_TO', 'W_E (Empty)', 'W_OE (Op. Empty)',
                      'W_F Total', 'W_F Usable', 'W_tfo', 'W_crew', 'W_payload'],
        'Value (lbs)': [f"{Wto:,.1f}", f"{WE:,.1f}", f"{WOE:,.1f}",
                         f"{WF:,.1f}", f"{RR['WFu']:,.1f}",
                         f"{Wtfo:,.2f}", f"{Wcrew:,.0f}", f"{Wpl:,.0f}"],
        '% of W_TO':  [f"{100:.1f}%", f"{WE/Wto*100:.1f}%", f"{WOE/Wto*100:.1f}%",
                        f"{WF/Wto*100:.1f}%", f"{RR['WFu']/Wto*100:.1f}%",
                        f"{Wtfo/Wto*100:.2f}%", f"{Wcrew/Wto*100:.2f}%",
                        f"{Wpl/Wto*100:.1f}%"],
    })
    st.dataframe(summary, hide_index=True, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="blk"><div class="blk-title">W_TO vs Passenger Count</div>', unsafe_allow_html=True)
    pxa = np.arange(5, npax+22, 2); wxr = []
    for n_ in pxa:
        try: w,_ = solve({**P,'npax':int(n_)}); wxr.append(w)
        except: wxr.append(float('nan'))
    fig_px = go.Figure()
    fig_px.add_trace(go.Scatter(
        x=pxa, y=wxr, mode='lines+markers',
        line=dict(color='#4ECDC4', width=2),
        marker=dict(size=5),
        fill='tozeroy', fillcolor='rgba(78,205,196,0.06)',
    ))
    fig_px.add_vline(x=npax, line_dash='dot', line_color='#96E6A1', line_width=1.5,
                     annotation_text=f'{npax} pax', annotation_font_color='#96E6A1',
                     annotation_font_size=10)
    _fig(fig_px, h=280, xt='Passengers', yt='W_TO (lbs)')
    st.plotly_chart(fig_px, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════
# TAB 4 — EXPORT
# ═══════════════════════════════════════════════════════════════════
with tab4:
    e1, e2 = st.columns(2)

    with e1:
        st.markdown('<div class="blk"><div class="blk-title">Download CSV</div>', unsafe_allow_html=True)
        rows = {
            'Parameter': ['W_TO','Mff','W_F','W_payload','W_empty','W_OE',
                          'W_crew','W_tfo','WE_allow','Conv_delta',
                          'dWTO_dCp_R','dWTO_dnp_R','dWTO_dLD_R','dWTO_dR',
                          'dWTO_dCp_E','dWTO_dnp_E','dWTO_dLD_E'],
            'Value': [Wto, RR['Mff'], WF, Wpl, WE, WOE, Wcrew, Wtfo,
                      RR['WEa'], RR['diff'],
                      S['dCpR'], S['dnpR'], S['dLDR'], S['dR'],
                      S['dCpE'], S['dnpE'], S['dLDE']],
            'Units': ['lbs','','lbs','lbs','lbs','lbs','lbs','lbs','lbs','lbs',
                      'lbs/(lbs/hp/hr)','lbs','lbs','lbs/nm',
                      'lbs/(lbs/hp/hr)','lbs','lbs'],
        }
        b = io.StringIO(); pd.DataFrame(rows).to_csv(b, index=False)
        st.download_button("⬇ DOWNLOAD RESULTS CSV", b.getvalue(),
                           "aeroweight_results.csv", "text/csv", use_container_width=True)
        b2 = io.StringIO()
        pd.DataFrame({'Phase': list(RR['fracs'].keys()),
                       'Wi/Wi-1': list(RR['fracs'].values())}).to_csv(b2, index=False)
        st.download_button("⬇ DOWNLOAD FRACTIONS CSV", b2.getvalue(),
                           "aeroweight_fractions.csv", "text/csv", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with e2:
        st.markdown('<div class="blk"><div class="blk-title">Download PDF Report</div>', unsafe_allow_html=True)
        def make_pdf():
            buf = io.BytesIO()
            doc = SimpleDocTemplate(buf, pagesize=letter,
                                    leftMargin=0.75*inch, rightMargin=0.75*inch,
                                    topMargin=0.75*inch, bottomMargin=0.75*inch)
            sty = getSampleStyleSheet()
            sT = ParagraphStyle('T', parent=sty['Title'], fontSize=18,
                                 textColor=colors.HexColor('#6C63FF'), spaceAfter=6)
            sH = ParagraphStyle('H', parent=sty['Heading2'], fontSize=11,
                                 textColor=colors.HexColor('#4ECDC4'),
                                 spaceBefore=10, spaceAfter=4)
            sB = ParagraphStyle('B', parent=sty['Normal'], fontSize=9, leading=13)
            ts = TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1C2030')),
                ('TEXTCOLOR',  (0,0), (-1,0), colors.HexColor('#6C63FF')),
                ('FONTSIZE',   (0,0), (-1,-1), 9),
                ('GRID',       (0,0), (-1,-1), 0.5, colors.HexColor('#2A2F45')),
                ('ROWBACKGROUNDS', (0,1), (-1,-1),
                 [colors.white, colors.HexColor('#F8F9FF')]),
            ])
            story = [
                Paragraph("AeroWeight Pro — Mission Report", sT),
                Paragraph("Propeller-Driven Aircraft · Breguet Method", sB),
                Spacer(1, 0.2*inch),
                Paragraph("Mission Parameters", sH),
            ]
            t1 = Table([['Parameter','Value'],
                         ['Passengers', str(npax)], ['Crew', str(ncrew)],
                         ['Range (nm)', str(R_nm)], ['Cruise L/D', str(LDc)],
                         ['Loiter endurance (hr)', str(El)]],
                        colWidths=[3*inch, 3*inch])
            t1.setStyle(ts)
            story += [t1, Spacer(1, 0.15*inch), Paragraph("Weight Summary", sH)]
            t2 = Table(
                [['Component','Value (lbs)','% W_TO']] +
                list(zip(summary['Component'], summary['Value (lbs)'], summary['% of W_TO'])),
                colWidths=[3*inch, 1.5*inch, 1.5*inch])
            t2.setStyle(ts)
            story += [t2, Spacer(1, 0.15*inch), Paragraph("Sensitivity Partials", sH)]
            t3 = Table(
                [['Partial','Value','Units']] +
                list(zip(sdr['Partial'], sdr['Value'], sdr['Units'])) +
                list(zip(sdl['Partial'], sdl['Value'], sdl['Units'])),
                colWidths=[2.5*inch, 2*inch, 1.5*inch])
            t3.setStyle(ts)
            story.append(t3)
            doc.build(story)
            buf.seek(0); return buf.read()

        st.download_button("⬇ DOWNLOAD PDF REPORT", make_pdf(),
                           "aeroweight_report.pdf", "application/pdf",
                           use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="blk"><div class="blk-title">Configuration Snapshot</div>', unsafe_allow_html=True)
    st.dataframe(pd.DataFrame({'Param': list(P.keys()),
                                'Value': [str(v) for v in P.values()]}),
                 hide_index=True, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
