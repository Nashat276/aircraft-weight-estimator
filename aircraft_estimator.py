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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');
html,body,[class*="css"]{background:#0B0F1A!important;color:#E2E8F0!important;font-family:'Inter',sans-serif!important}
.stApp{background:#0B0F1A}
.hdr{text-align:center;padding:1.2rem 0 .4rem}
.hdr-title{font-size:2rem;font-weight:700;color:#fff;letter-spacing:-.02em}
.hdr-title em{font-style:normal;color:#818CF8}
.hdr-sub{font-family:'JetBrains Mono',monospace;font-size:.7rem;color:#475569;
  letter-spacing:.25em;margin-top:.3rem}
.ok{background:#052e16;border:1px solid #166534;border-radius:10px;
  padding:.6rem 1.2rem;font-family:'JetBrains Mono',monospace;font-size:.82rem;color:#4ade80;
  display:flex;align-items:center;gap:.6rem}
.warn{background:#1c0a00;border:1px solid #9a3412;border-radius:10px;
  padding:.6rem 1.2rem;font-family:'JetBrains Mono',monospace;font-size:.82rem;color:#fb923c;
  display:flex;align-items:center;gap:.6rem}
.kpi{background:#131929;border:1px solid #1e2a3a;border-radius:14px;
  padding:1rem 1.2rem;text-align:center}
.kpi:hover{border-color:#818CF855;transition:.2s}
.kpi-n{font-family:'JetBrains Mono',monospace;font-size:1.55rem;font-weight:600;color:#818CF8}
.kpi-u{font-size:.78rem;color:#64748B;margin-left:.2rem}
.kpi-l{font-size:.65rem;color:#475569;letter-spacing:.1em;text-transform:uppercase;margin-top:.35rem}
.card{background:#131929;border:1px solid #1e2a3a;border-radius:14px;
  padding:1.2rem 1.4rem;margin-bottom:1rem}
.card-title{font-family:'JetBrains Mono',monospace;font-size:.72rem;font-weight:600;
  color:#818CF8;letter-spacing:.15em;text-transform:uppercase;
  border-bottom:1px solid #1e2a3a;padding-bottom:.5rem;margin-bottom:1rem}
[data-testid="stSidebar"]{background:#0D1220!important;border-right:1px solid #1e2a3a!important}
.stTabs [data-baseweb="tab-list"]{background:#131929;border-radius:12px;padding:4px;gap:2px}
.stTabs [data-baseweb="tab"]{border-radius:9px;padding:.4rem 1.2rem;
  font-size:.78rem;font-weight:500;color:#64748B;letter-spacing:.04em}
.stTabs [aria-selected="true"]{background:#818CF8!important;color:#fff!important}
.stSlider>label{font-size:.8rem!important;color:#94A3B8!important}
.stNumberInput>label{font-size:.8rem!important;color:#94A3B8!important}
hr{border-color:#1e2a3a!important;margin:1rem 0!important}
</style>
""", unsafe_allow_html=True)

# ── PLOTLY: SAFE WRAPPER ──────────────────────────────────────────
_PL = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(19,25,41,0.9)',
    font=dict(family='JetBrains Mono', color='#64748B', size=10),
    margin=dict(l=50, r=16, t=36, b=42),
    hoverlabel=dict(bgcolor='#1e2a3a', font_size=11, font_color='#E2E8F0'),
)

def style_fig(fig, title='', h=320, xt='', yt='', yr=None):
    kw = dict(_PL)
    kw['height'] = h
    if title:
        kw['title'] = dict(text=title, font=dict(color='#94A3B8', size=11,
                                                   family='JetBrains Mono'), x=0.01)
    fig.update_layout(**kw)
    fig.update_xaxes(gridcolor='#1e2a3a', linecolor='#1e2a3a', zerolinecolor='#1e2a3a')
    fig.update_yaxes(gridcolor='#1e2a3a', linecolor='#1e2a3a', zerolinecolor='#1e2a3a')
    if xt: fig.update_xaxes(title_text=xt, title_font=dict(size=10, color='#475569'))
    if yt: fig.update_yaxes(title_text=yt, title_font=dict(size=10, color='#475569'))
    if yr: fig.update_yaxes(range=yr)

# ── PHYSICS ───────────────────────────────────────────────────────
def mission(p):
    Wpl   = p['npax']*(p['wpax']+p['wbag']) + p['ncrew']*205 + p['natt']*200
    Wcrew = p['ncrew']*205 + p['natt']*200
    Wtfo  = p['Wto']*p['Mtfo']
    Rc    = p['R']*1.15078
    W5    = 1/math.exp(Rc/(375*(p['npc']/p['Cpc'])*p['LDc']))
    Vm    = p['Vl']*1.15078
    W6    = 1/math.exp(p['El']/(375*(1/Vm)*(p['npl']/p['Cpl'])*p['LDl']))
    fnames = ['Engine Start','Taxi','Takeoff','Climb','Cruise','Loiter','Descent','Landing']
    fvals  = [0.990,0.995,0.995,0.985,W5,W6,0.985,0.995]
    fracs  = dict(zip(fnames, fvals))
    Mff=1.0
    for v in fvals: Mff*=v
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

# ── DEFAULTS ──────────────────────────────────────────────────────
D = dict(npax=34,wpax=175,wbag=30,ncrew=2,natt=1,Mtfo=0.005,Mr=0.0,
         R=1100,Vl=250,LDc=13,Cpc=0.60,npc=0.85,
         El=0.75,LDl=16,Cpl=0.65,npl=0.77,A=0.3774,B=0.9647)

# ── SIDEBAR ───────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ✈ AeroWeight Pro")
    st.markdown("---")
    st.markdown("**Payload**")
    npax  = st.slider("Passengers",        10, 100, D['npax'])
    wpax  = st.slider("Pax weight (lbs)", 140, 220, D['wpax'])
    wbag  = st.slider("Baggage (lbs)",     10,  60, D['wbag'])
    ncrew = st.slider("Pilots",             1,   4, D['ncrew'])
    natt  = st.slider("Attendants",         0,   4, D['natt'])
    st.markdown("---")
    st.markdown("**Cruise Phase**")
    R_nm = st.slider("Range (nm)",        200, 3000, D['R'],   step=50)
    LDc  = st.slider("L/D cruise",          8,   22, D['LDc'])
    Cpc  = st.slider("Cp cruise",          0.3,  1.0, D['Cpc'], step=0.01)
    npc  = st.slider("np cruise",          0.5, 0.95, D['npc'], step=0.01)
    st.markdown("---")
    st.markdown("**Loiter Phase**")
    El   = st.slider("Endurance (hr)",    0.1,  3.0, D['El'],  step=0.05)
    Vl   = st.slider("Loiter speed (kts)",100,  350, D['Vl'])
    LDl  = st.slider("L/D loiter",          8,   24, D['LDl'])
    Cpl  = st.slider("Cp loiter",          0.3,  1.0, D['Cpl'], step=0.01)
    npl  = st.slider("np loiter",          0.5, 0.95, D['npl'], step=0.01)
    st.markdown("---")
    st.markdown("**Regression Constants**")
    A_v  = st.number_input("A (Table 2.2)", value=D['A'],    step=0.001, format="%.4f")
    B_v  = st.number_input("B (Table 2.2)", value=D['B'],    step=0.001, format="%.4f")
    Mtfo = st.number_input("M_tfo",          value=D['Mtfo'], step=0.001, format="%.4f")

P = dict(npax=npax,wpax=wpax,wbag=wbag,ncrew=ncrew,natt=natt,
         Mtfo=Mtfo,Mr=0.0,R=R_nm,Vl=Vl,LDc=LDc,Cpc=Cpc,npc=npc,
         El=El,LDl=LDl,Cpl=Cpl,npl=npl,A=A_v,B=B_v,Wto=48550)

Wto, RR = solve(P)
S = sens(P, Wto)

# ── HEADER ────────────────────────────────────────────────────────
st.markdown("""
<div class="hdr">
  <div class="hdr-title">Aero<em>Weight</em> Pro</div>
  <div class="hdr-sub">PROPELLER AIRCRAFT · PRELIMINARY SIZING · BREGUET METHOD</div>
</div>
""", unsafe_allow_html=True)

if abs(RR['diff']) < 5:
    st.markdown(f'<div class="ok">✓ &nbsp; Converged &nbsp;|&nbsp; W_TO = {Wto:,.0f} lbs &nbsp;|&nbsp; ΔWE = {RR["diff"]:.2f} lbs</div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div class="warn">⚠ &nbsp; Not converged — ΔWE = {RR["diff"]:.1f} lbs. Adjust parameters.</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── KPI ROW ───────────────────────────────────────────────────────
k1,k2,k3,k4,k5 = st.columns(5)
for col,val,unit,lbl in [
    (k1, f"{Wto:,.0f}",       "lbs", "Gross Weight W_TO"),
    (k2, f"{RR['Mff']:.4f}",  "",    "Fuel Fraction"),
    (k3, f"{RR['WF']:,.0f}",  "lbs", "Total Fuel"),
    (k4, f"{RR['Wpl']:,.0f}", "lbs", "Payload"),
    (k5, f"{RR['WE']:,.0f}",  "lbs", "Empty Weight"),
]:
    with col:
        st.markdown(f"""
        <div class="kpi">
          <div class="kpi-n">{val}<span class="kpi-u">{unit}</span></div>
          <div class="kpi-l">{lbl}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["Mission", "Sensitivity", "Weight Breakdown", "Export"])

# ══════════════════════════════════════════════════════════════════
# TAB 1 — MISSION
# ══════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    colA, colB = st.columns([3, 2], gap="large")

    with colA:
        # Bar chart
        st.markdown('<div class="card"><div class="card-title">Phase Weight Fractions</div>', unsafe_allow_html=True)
        phases = list(RR['fracs'].keys())
        fvals  = list(RR['fracs'].values())
        BAR_C  = ['#818CF8','#6366F1','#4F46E5','#4338CA','#34D399','#10B981','#059669','#047857']
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=phases, y=fvals,
            marker_color=BAR_C,
            text=[f'{v:.4f}' for v in fvals],
            textposition='outside',
            textfont=dict(size=9, color='#94A3B8'),
        ))
        style_fig(fig, h=290, yr=[0.80, 1.02])
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Range sweep
        st.markdown('<div class="card"><div class="card-title">W_TO vs Range Sweep</div>', unsafe_allow_html=True)
        rr = np.linspace(200, 3000, 55)
        ww = []
        for rv in rr:
            try: w,_ = solve({**P,'R':float(rv)}); ww.append(w)
            except: ww.append(float('nan'))
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(
            x=rr, y=ww, mode='lines',
            line=dict(color='#818CF8', width=2.5),
            fill='tozeroy', fillcolor='rgba(129,140,248,0.06)',
        ))
        fig3.add_vline(x=R_nm, line_dash='dot', line_color='#34D399', line_width=1.5,
                       annotation_text=f'Current: {R_nm} nm',
                       annotation_font_color='#34D399', annotation_font_size=10)
        style_fig(fig3, h=250, xt='Range (nm)', yt='W_TO (lbs)')
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with colB:
        # Gauge
        st.markdown('<div class="card"><div class="card-title">W_TO Gauge</div>', unsafe_allow_html=True)
        fig2 = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=Wto,
            delta={'reference': 48550, 'relative': False,
                   'increasing': {'color': '#fb923c'},
                   'decreasing': {'color': '#34d399'}},
            number={'suffix': ' lbs', 'font': {'color': '#818CF8', 'size': 16,
                                                'family': 'JetBrains Mono'}},
            gauge={
                'axis': {'range': [10000, 150000]},
                'bar':  {'color': '#818CF8', 'thickness': 0.22},
                'bgcolor': '#131929', 'borderwidth': 1, 'bordercolor': '#1e2a3a',
                'steps': [
                    {'range': [10000,  50000], 'color': '#052e16'},
                    {'range': [50000, 100000], 'color': '#131929'},
                    {'range': [100000,150000], 'color': '#1c0a00'},
                ],
                'threshold': {'line': {'color': '#fb923c', 'width': 2},
                              'thickness': 0.75, 'value': Wto},
            },
            title={'text': 'Gross Takeoff Weight',
                   'font': {'color': '#475569', 'size': 10, 'family': 'JetBrains Mono'}},
        ))
        fig2.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='JetBrains Mono', color='#64748B'),
            height=255, margin=dict(t=32, b=8, l=12, r=12),
        )
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Convergence table
        st.markdown('<div class="card"><div class="card-title">Convergence Check</div>', unsafe_allow_html=True)
        st.dataframe(pd.DataFrame({
            'Item': ['WE Tentative', 'WE Allowable', 'Delta'],
            'Value (lbs)': [f"{RR['WE']:,.1f}", f"{RR['WEa']:,.1f}",
                            f"{RR['diff']:+.2f}"],
        }), hide_index=True, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Phase fractions table
        st.markdown('<div class="card"><div class="card-title">Phase Fractions Table</div>', unsafe_allow_html=True)
        st.dataframe(pd.DataFrame({
            'Phase': list(RR['fracs'].keys()),
            'Wi / Wi-1': [f"{v:.4f}" for v in RR['fracs'].values()],
        }), hide_index=True, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
# TAB 2 — SENSITIVITY
# ══════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown('<div class="card"><div class="card-title">Range Phase Partials</div>', unsafe_allow_html=True)
        sdr = {'Partial': ['dWTO/dCp', 'dWTO/dnp', 'dWTO/d(L/D)', 'dWTO/dR'],
               'Value':   [f"{S['dCpR']:+,.1f}", f"{S['dnpR']:+,.1f}",
                           f"{S['dLDR']:+,.1f}", f"{S['dR']:+,.2f}"],
               'Units':   ['lbs / (lbs/hp/hr)', 'lbs', 'lbs', 'lbs/nm']}
        st.dataframe(pd.DataFrame(sdr), hide_index=True, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="card"><div class="card-title">Loiter Phase Partials</div>', unsafe_allow_html=True)
        sdl = {'Partial': ['dWTO/dCp', 'dWTO/dnp', 'dWTO/d(L/D)'],
               'Value':   [f"{S['dCpE']:+,.1f}", f"{S['dnpE']:+,.1f}", f"{S['dLDE']:+,.1f}"],
               'Units':   ['lbs / (lbs/hp/hr)', 'lbs', 'lbs']}
        st.dataframe(pd.DataFrame(sdl), hide_index=True, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card"><div class="card-title">Tornado Diagram — ΔW_TO per Unit Change</div>', unsafe_allow_html=True)
    tlbl = ['Cp (range)', 'np (range)', 'L/D (range)', 'Range R',
            'Cp (loiter)', 'np (loiter)', 'L/D (loiter)']
    tval = [S['dCpR'], S['dnpR'], S['dLDR'], S['dR']*R_nm*0.1,
            S['dCpE'], S['dnpE'], S['dLDE']]
    idx  = sorted(range(7), key=lambda i: abs(tval[i]))
    tlbl = [tlbl[i] for i in idx]
    tval = [tval[i] for i in idx]
    fig_t = go.Figure(go.Bar(
        x=tval, y=tlbl, orientation='h',
        marker_color=['#818CF8' if v >= 0 else '#fb923c' for v in tval],
        text=[f'{v:+,.0f}' for v in tval],
        textposition='outside',
        textfont=dict(size=9),
    ))
    fig_t.add_vline(x=0, line_color='#1e2a3a', line_width=1.5)
    style_fig(fig_t, h=340, xt='ΔW_TO (lbs)')
    st.plotly_chart(fig_t, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card"><div class="card-title">3D Surface — W_TO over Cp × L/D (Cruise)</div>', unsafe_allow_html=True)
    cpa = np.linspace(0.40, 0.90, 20)
    lda = np.linspace(9.0, 20.0, 20)
    Z   = np.zeros((len(cpa), len(lda)))
    for i, cp in enumerate(cpa):
        for j, ld in enumerate(lda):
            try: w,_ = solve({**P,'Cpc':float(cp),'LDc':float(ld)}); Z[i,j]=w
            except: Z[i,j]=float('nan')
    fig4 = go.Figure(go.Surface(
        x=lda, y=cpa, z=Z,
        colorscale=[[0,'#0B0F1A'],[0.4,'#1e2a3a'],[0.7,'#818CF8'],[1,'#34D399']],
        opacity=0.92, showscale=True,
        colorbar=dict(tickfont=dict(size=9, color='#64748B'), len=0.7,
                      title=dict(text='W_TO lbs', font=dict(size=9, color='#64748B'))),
    ))
    fig4.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='JetBrains Mono', color='#64748B', size=9),
        title=dict(text='W_TO surface over Cp and L/D',
                   font=dict(color='#94A3B8', size=11, family='JetBrains Mono'), x=0.01),
        scene=dict(
            xaxis=dict(title='L/D', backgroundcolor='#131929',
                       gridcolor='#1e2a3a', linecolor='#1e2a3a'),
            yaxis=dict(title='Cp',  backgroundcolor='#131929',
                       gridcolor='#1e2a3a', linecolor='#1e2a3a'),
            zaxis=dict(title='W_TO (lbs)', backgroundcolor='#131929',
                       gridcolor='#1e2a3a', linecolor='#1e2a3a'),
            bgcolor='#0B0F1A',
        ),
        margin=dict(l=0, r=0, t=45, b=0),
        height=460,
    )
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
# TAB 3 — WEIGHT BREAKDOWN
# ══════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("<br>", unsafe_allow_html=True)
    WE=RR['WE']; WOE=RR['WOE']; WF=RR['WF']
    Wpl=RR['Wpl']; Wcrew=RR['Wcrew']; Wtfo=RR['Wtfo']

    pa, pb = st.columns(2, gap="large")
    with pa:
        st.markdown('<div class="card"><div class="card-title">W_TO Composition</div>', unsafe_allow_html=True)
        fig_p = go.Figure(go.Pie(
            labels=['Empty Weight','Usable Fuel','Trapped Fuel','Crew','Payload'],
            values=[WE, RR['WFu'], Wtfo, Wcrew, Wpl],
            hole=0.55,
            marker=dict(
                colors=['#818CF8','#34D399','#60A5FA','#F59E0B','#F87171'],
                line=dict(color='#0B0F1A', width=2),
            ),
            textfont=dict(size=10, color='#E2E8F0'),
            textinfo='label+percent',
        ))
        fig_p.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='JetBrains Mono', color='#64748B'),
            showlegend=False, height=300,
            margin=dict(t=16, b=10, l=10, r=10),
            annotations=[dict(
                text=f'{Wto:,.0f}<br><span style="font-size:10px">lbs</span>',
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=14, color='#818CF8', family='JetBrains Mono'),
            )],
        )
        st.plotly_chart(fig_p, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with pb:
        st.markdown('<div class="card"><div class="card-title">Weight Through Mission</div>', unsafe_allow_html=True)
        fv = list(RR['fracs'].values())
        pl = list(RR['fracs'].keys()) + ['End']
        cum = [Wto]
        for f in fv: cum.append(cum[-1]*f)
        fig_w = go.Figure()
        fig_w.add_trace(go.Scatter(
            x=pl, y=cum, mode='lines+markers',
            line=dict(color='#818CF8', width=2.5),
            marker=dict(color='#34D399', size=7,
                        line=dict(color='#818CF8', width=1.5)),
            fill='tozeroy', fillcolor='rgba(129,140,248,0.06)',
        ))
        style_fig(fig_w, h=300, xt='Phase', yt='Weight (lbs)')
        st.plotly_chart(fig_w, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card"><div class="card-title">Detailed Weight Summary</div>', unsafe_allow_html=True)
    summary = pd.DataFrame({
        'Component': ['W_TO (Gross)', 'W_E (Empty)', 'W_OE (Operating Empty)',
                      'W_F Total', 'W_F Usable', 'W_tfo (Trapped)', 'W_crew', 'W_payload'],
        'Value (lbs)': [f"{Wto:,.1f}", f"{WE:,.1f}", f"{WOE:,.1f}",
                         f"{WF:,.1f}", f"{RR['WFu']:,.1f}",
                         f"{Wtfo:,.2f}", f"{Wcrew:,.0f}", f"{Wpl:,.0f}"],
        '% of W_TO': [f"{100:.1f}%", f"{WE/Wto*100:.1f}%", f"{WOE/Wto*100:.1f}%",
                       f"{WF/Wto*100:.1f}%", f"{RR['WFu']/Wto*100:.1f}%",
                       f"{Wtfo/Wto*100:.2f}%", f"{Wcrew/Wto*100:.2f}%",
                       f"{Wpl/Wto*100:.1f}%"],
    })
    st.dataframe(summary, hide_index=True, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card"><div class="card-title">W_TO vs Passenger Count</div>', unsafe_allow_html=True)
    pxa = np.arange(5, npax+22, 2); wxr = []
    for n_ in pxa:
        try: w,_ = solve({**P,'npax':int(n_)}); wxr.append(w)
        except: wxr.append(float('nan'))
    fig_px = go.Figure()
    fig_px.add_trace(go.Scatter(
        x=pxa, y=wxr, mode='lines+markers',
        line=dict(color='#34D399', width=2),
        marker=dict(color='#34D399', size=5),
        fill='tozeroy', fillcolor='rgba(52,211,153,0.06)',
    ))
    fig_px.add_vline(x=npax, line_dash='dot', line_color='#F59E0B', line_width=1.5,
                     annotation_text=f'{npax} pax',
                     annotation_font_color='#F59E0B', annotation_font_size=10)
    style_fig(fig_px, h=270, xt='Passengers', yt='W_TO (lbs)')
    st.plotly_chart(fig_px, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
# TAB 4 — EXPORT
# ══════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("<br>", unsafe_allow_html=True)
    e1, e2 = st.columns(2, gap="large")

    with e1:
        st.markdown('<div class="card"><div class="card-title">Download CSV</div>', unsafe_allow_html=True)
        rows = {
            'Parameter': ['W_TO','Mff','W_F','W_payload','W_empty','W_OE',
                          'W_crew','W_tfo','WE_allow','Conv_delta',
                          'dWTO_dCp_R','dWTO_dnp_R','dWTO_dLD_R','dWTO_dR',
                          'dWTO_dCp_E','dWTO_dnp_E','dWTO_dLD_E'],
            'Value': [Wto,RR['Mff'],WF,Wpl,WE,WOE,Wcrew,Wtfo,
                      RR['WEa'],RR['diff'],
                      S['dCpR'],S['dnpR'],S['dLDR'],S['dR'],
                      S['dCpE'],S['dnpE'],S['dLDE']],
            'Units': ['lbs','','lbs','lbs','lbs','lbs','lbs','lbs','lbs','lbs',
                      'lbs/(lbs/hp/hr)','lbs','lbs','lbs/nm',
                      'lbs/(lbs/hp/hr)','lbs','lbs'],
        }
        b = io.StringIO(); pd.DataFrame(rows).to_csv(b, index=False)
        st.download_button("⬇  Download Results CSV", b.getvalue(),
                           "aeroweight_results.csv", "text/csv",
                           use_container_width=True)
        b2 = io.StringIO()
        pd.DataFrame({'Phase': list(RR['fracs'].keys()),
                       'Wi/Wi-1': list(RR['fracs'].values())}).to_csv(b2, index=False)
        st.download_button("⬇  Download Fractions CSV", b2.getvalue(),
                           "aeroweight_fractions.csv", "text/csv",
                           use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with e2:
        st.markdown('<div class="card"><div class="card-title">Download PDF Report</div>', unsafe_allow_html=True)
        def make_pdf():
            buf = io.BytesIO()
            doc = SimpleDocTemplate(buf, pagesize=letter,
                                    leftMargin=0.75*inch, rightMargin=0.75*inch,
                                    topMargin=0.75*inch, bottomMargin=0.75*inch)
            sty = getSampleStyleSheet()
            sT = ParagraphStyle('T', parent=sty['Title'], fontSize=17,
                                 textColor=colors.HexColor('#818CF8'), spaceAfter=6)
            sH = ParagraphStyle('H', parent=sty['Heading2'], fontSize=11,
                                 textColor=colors.HexColor('#34D399'),
                                 spaceBefore=10, spaceAfter=4)
            sB = ParagraphStyle('B', parent=sty['Normal'], fontSize=9, leading=13)
            ts = TableStyle([
                ('BACKGROUND', (0,0),(-1,0), colors.HexColor('#131929')),
                ('TEXTCOLOR',  (0,0),(-1,0), colors.HexColor('#818CF8')),
                ('FONTSIZE',   (0,0),(-1,-1), 9),
                ('GRID',       (0,0),(-1,-1), 0.5, colors.HexColor('#1e2a3a')),
                ('ROWBACKGROUNDS',(0,1),(-1,-1),
                 [colors.white, colors.HexColor('#F8FAFF')]),
            ])
            story = [
                Paragraph("AeroWeight Pro — Mission Report", sT),
                Paragraph("Propeller Aircraft · Breguet Range/Endurance Method", sB),
                Spacer(1, 0.2*inch),
                Paragraph("Mission Parameters", sH),
            ]
            t1 = Table([['Parameter','Value'],
                         ['Passengers', str(npax)], ['Crew', str(ncrew)],
                         ['Range (nm)', str(R_nm)],
                         ['Cruise L/D', str(LDc)],
                         ['Loiter endurance (hr)', str(El)]],
                        colWidths=[3*inch, 3*inch])
            t1.setStyle(ts)
            story += [t1, Spacer(1, 0.15*inch), Paragraph("Weight Summary", sH)]
            t2 = Table(
                [['Component','Value (lbs)','% W_TO']] +
                list(zip(summary['Component'],
                          summary['Value (lbs)'],
                          summary['% of W_TO'])),
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

        st.download_button("⬇  Download PDF Report", make_pdf(),
                           "aeroweight_report.pdf", "application/pdf",
                           use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card"><div class="card-title">Configuration Snapshot</div>', unsafe_allow_html=True)
    st.dataframe(pd.DataFrame({
        'Parameter': list(P.keys()),
        'Value': [str(v) for v in P.values()],
    }), hide_index=True, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
