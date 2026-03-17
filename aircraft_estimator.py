import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math, io
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.units import cm

st.set_page_config(
    page_title="AeroSizer Pro",
    page_icon="✈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
*{box-sizing:border-box}
html,body,[class*="css"]{
    background:#F8FAFC!important;
    color:#1E293B!important;
    font-family:'Inter',sans-serif!important;
}
.stApp{background:#F8FAFC!important}

/* HEADER */
.hdr{background:#0F172A;border-radius:10px;padding:.9rem 1.5rem;
  display:flex;align-items:center;justify-content:space-between;margin-bottom:1.2rem}
.hdr-name{font-family:'JetBrains Mono',monospace;font-size:1.1rem;
  font-weight:500;color:#fff;letter-spacing:.05em}
.hdr-name b{color:#38BDF8}
.hdr-desc{font-size:.68rem;color:#94A3B8;letter-spacing:.12em;
  text-transform:uppercase;margin-top:.12rem;font-family:'JetBrains Mono',monospace}
.hdr-pill{background:#1E3A5F;color:#7DD3FC;font-size:.65rem;
  font-family:'JetBrains Mono',monospace;padding:.3rem .7rem;
  border-radius:5px;border:1px solid #2563EB30;letter-spacing:.08em}

/* STATUS */
.s-ok{background:#F0FDF4;border-left:3px solid #22C55E;border-radius:0 8px 8px 0;
  padding:.5rem 1rem;font-family:'JetBrains Mono',monospace;font-size:.78rem;
  color:#16A34A;margin-bottom:1rem}
.s-err{background:#FFF7ED;border-left:3px solid #F97316;border-radius:0 8px 8px 0;
  padding:.5rem 1rem;font-family:'JetBrains Mono',monospace;font-size:.78rem;
  color:#EA580C;margin-bottom:1rem}

/* KPI */
.krow{display:grid;grid-template-columns:repeat(5,1fr);gap:10px;margin-bottom:1.2rem}
.kpi{background:#fff;border:1px solid #E2E8F0;border-radius:10px;
  padding:.85rem 1rem;border-top:2px solid #38BDF8}
.kv{font-family:'JetBrains Mono',monospace;font-size:1.35rem;
  font-weight:500;color:#0F172A;line-height:1}
.ku{font-size:.72rem;color:#64748B;margin-left:.18rem}
.kl{font-size:.6rem;color:#94A3B8;letter-spacing:.09em;
  margin-top:.28rem;text-transform:uppercase}

/* CARD */
.card{background:#fff;border:1px solid #E2E8F0;border-radius:10px;
  padding:1rem 1.2rem;margin-bottom:.9rem}
.ct{font-family:'JetBrains Mono',monospace;font-size:.68rem;font-weight:500;
  color:#38BDF8;letter-spacing:.13em;text-transform:uppercase;
  padding-bottom:.5rem;border-bottom:1px solid #F1F5F9;margin-bottom:.8rem}

/* SIDEBAR */
[data-testid="stSidebar"]{background:#fff!important;border-right:1px solid #E2E8F0!important}
.sb-logo{font-family:'JetBrains Mono',monospace;font-size:.95rem;font-weight:500;
  color:#0F172A;letter-spacing:.04em}
.sb-logo b{color:#38BDF8}
.sb-tag{font-size:.6rem;color:#94A3B8;letter-spacing:.14em;
  text-transform:uppercase;margin-bottom:.9rem;font-family:'JetBrains Mono',monospace}
.sb-sec{font-size:.63rem;font-weight:600;color:#38BDF8;letter-spacing:.15em;
  text-transform:uppercase;padding:.45rem 0 .35rem 0;
  border-bottom:1px solid #F1F5F9;margin:.5rem 0 .6rem 0;
  font-family:'JetBrains Mono',monospace}

/* TABS */
.stTabs [data-baseweb="tab-list"]{background:#fff;border-radius:8px;
  padding:3px;border:1px solid #E2E8F0;gap:2px;margin-bottom:.9rem}
.stTabs [data-baseweb="tab"]{border-radius:6px;font-size:.76rem;
  font-weight:500;color:#64748B;padding:.38rem 1rem}
.stTabs [aria-selected="true"]{background:#0F172A!important;color:#fff!important}

/* DOWNLOAD */
div.stDownloadButton>button{background:#0F172A!important;color:#fff!important;
  border:none!important;border-radius:8px!important;font-size:.78rem!important;
  font-weight:500!important;padding:.5rem .9rem!important;width:100%!important}
div.stDownloadButton>button:hover{background:#1E3A5F!important}

/* TABLE TWEAK */
[data-testid="stDataFrame"] iframe{border-radius:8px}
</style>
""", unsafe_allow_html=True)

# ── PLOTLY THEME ─────────────────────────────────────────────────
_B = dict(
    paper_bgcolor='rgba(255,255,255,0)',
    plot_bgcolor='#FAFBFC',
    font=dict(family='JetBrains Mono', color='#475569', size=9.5),
    margin=dict(l=54, r=14, t=32, b=42),
    hoverlabel=dict(bgcolor='#0F172A', font_color='#fff',
                    font_size=10, font_family='JetBrains Mono'),
)
_AX = dict(gridcolor='#F1F5F9', linecolor='#E2E8F0', zerolinecolor='#E2E8F0')

def pfig(fig, title='', h=230, xt='', yt='', yr=None):
    kw = dict(_B); kw['height'] = h
    if title:
        kw['title'] = dict(text=title,
                           font=dict(color='#0F172A', size=10, family='JetBrains Mono'),
                           x=0.01)
    fig.update_layout(**kw)
    fig.update_xaxes(**_AX)
    fig.update_yaxes(**_AX)
    if xt: fig.update_xaxes(title_text=xt, title_font=dict(size=8.5, color='#94A3B8'))
    if yt: fig.update_yaxes(title_text=yt, title_font=dict(size=8.5, color='#94A3B8'))
    if yr: fig.update_yaxes(range=yr)
    return fig

# ── PHYSICS ──────────────────────────────────────────────────────
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
    Mff = 1.0
    for v in fvals: Mff *= v
    WFu = p['Wto']*(1-Mff)
    WF  = WFu + p['Wto']*p['Mr']*(1-Mff) + Wtfo
    WOE = p['Wto'] - WF - Wpl
    WE  = WOE - Wtfo - Wcrew
    WEa = 10**((math.log10(p['Wto'])-p['A'])/p['B'])
    return dict(Wpl=Wpl,Wcrew=Wcrew,Wtfo=Wtfo,Mff=Mff,
                WF=WF,WFu=WFu,WOE=WOE,WE=WE,WEa=WEa,
                diff=WEa-WE,fracs=dict(zip(fnames,fvals)))

def solve(p, tol=0.5, n=300):
    pp = dict(p)
    # test sign at boundaries
    pp['Wto']=8000;  r_lo=mission(pp)
    pp['Wto']=400000; r_hi=mission(pp)
    lo,hi = 8000.0, 400000.0
    if r_lo['diff']*r_hi['diff'] > 0:
        # sweep to find sign change
        for w0 in [12000,20000,35000,55000,80000,120000,180000,260000]:
            pp['Wto']=w0; r0=mission(pp)
            if r0['diff']*r_hi['diff'] < 0:
                lo=w0; break
    r={}
    for _ in range(n):
        m=(lo+hi)/2; pp['Wto']=m; r=mission(pp)
        if abs(r['diff'])<tol: break
        if r['diff']>0: hi=m
        else: lo=m
    return m,r

def sens(p,Wto):
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

# ── DEFAULTS ─────────────────────────────────────────────────────
D = dict(npax=34,wpax=175,wbag=30,ncrew=2,natt=1,Mtfo=0.005,Mr=0.0,
         R=1100,Vl=250,LDc=13,Cpc=0.60,npc=0.85,
         El=0.75,LDl=16,Cpl=0.65,npl=0.77,A=0.3774,B=0.9647)

# ── SIDEBAR ──────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sb-logo">AERO<b>SIZER</b> PRO</div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-tag">Preliminary Weight Estimation</div>', unsafe_allow_html=True)

    st.markdown('<div class="sb-sec">Cabin & Crew</div>', unsafe_allow_html=True)
    npax  = st.slider("Passengers",           10, 150, D['npax'])
    wpax  = st.slider("Passenger weight (lbs)",140,230, D['wpax'])
    wbag  = st.slider("Baggage weight (lbs)",  10, 70,  D['wbag'])
    ncrew = st.slider("Flight crew",            1,  4,  D['ncrew'])
    natt  = st.slider("Cabin attendants",       0,  6,  D['natt'])

    st.markdown('<div class="sb-sec">Cruise Segment</div>', unsafe_allow_html=True)
    R_nm = st.slider("Design range (nm)",    200,4000,D['R'],step=50)
    LDc  = st.slider("L/D ratio",              8,  24, D['LDc'])
    Cpc  = st.slider("SFC  Cp (lbs/hp/hr)", 0.3, 1.0, D['Cpc'],step=0.01)
    npc  = st.slider("Prop efficiency  η",  0.50,0.95, D['npc'],step=0.01)

    st.markdown('<div class="sb-sec">Loiter / Reserve</div>', unsafe_allow_html=True)
    El   = st.slider("Endurance (hr)",       0.1, 4.0, D['El'],step=0.05)
    Vl   = st.slider("Loiter speed (kts)",   100, 350, D['Vl'])
    LDl  = st.slider("L/D ratio",              8,  26, D['LDl'])
    Cpl  = st.slider("SFC  Cp (lbs/hp/hr)", 0.3, 1.0, D['Cpl'],step=0.01)
    npl  = st.slider("Prop efficiency  η",  0.50,0.95, D['npl'],step=0.01)

    st.markdown('<div class="sb-sec">Regression Constants</div>', unsafe_allow_html=True)
    st.caption("Raymer Table 2.2 — turboprop transport")
    A_v  = st.number_input("A",     value=D['A'],    step=0.001,format="%.4f")
    B_v  = st.number_input("B",     value=D['B'],    step=0.001,format="%.4f")
    Mtfo = st.number_input("M_tfo", value=D['Mtfo'], step=0.001,format="%.4f")

P = dict(npax=npax,wpax=wpax,wbag=wbag,ncrew=ncrew,natt=natt,
         Mtfo=Mtfo,Mr=0.0,R=R_nm,Vl=Vl,LDc=LDc,Cpc=Cpc,npc=npc,
         El=El,LDl=LDl,Cpl=Cpl,npl=npl,A=A_v,B=B_v,Wto=48550)

Wto, RR = solve(P)
S = sens(P, Wto)
conv = abs(RR['diff']) < 5

# ── HEADER ───────────────────────────────────────────────────────
st.markdown(f"""
<div class="hdr">
  <div>
    <div class="hdr-name">AERO<b>SIZER</b> PRO</div>
    <div class="hdr-desc">Preliminary Aircraft Weight Estimation · Breguet Method · Propeller-Driven Aircraft</div>
  </div>
  <div class="hdr-pill">Raymer / Roskam · Rev. 2025</div>
</div>
""", unsafe_allow_html=True)

if conv:
    st.markdown(f'<div class="s-ok">✓  Converged  ·  W_TO = {Wto:,.0f} lbs  ·  Mff = {RR["Mff"]:.5f}  ·  ΔWE = {RR["diff"]:+.1f} lbs</div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div class="s-err">⚠  Not converged  ·  ΔWE = {RR["diff"]:+.0f} lbs  ·  Check inputs or regression constants</div>', unsafe_allow_html=True)

# KPI row
WE=RR['WE']; WOE=RR['WOE']; WF=RR['WF']
Wpl=RR['Wpl']; Wcrew=RR['Wcrew']; Wtfo=RR['Wtfo']

k1,k2,k3,k4,k5 = st.columns(5)
for col,val,unit,lbl in [
    (k1, f"{Wto:,.0f}",       "lbs", "Gross Takeoff  W_TO"),
    (k2, f"{RR['Mff']:.5f}",  "",    "Fuel Fraction  Mff"),
    (k3, f"{WF:,.0f}",        "lbs", "Total Fuel  W_F"),
    (k4, f"{Wpl:,.0f}",       "lbs", "Payload  W_PL"),
    (k5, f"{WE:,.0f}",        "lbs", "Empty Weight  W_E"),
]:
    with col:
        st.markdown(f'<div class="kpi"><div class="kv">{val}<span class="ku">{unit}</span></div><div class="kl">{lbl}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── TABS ─────────────────────────────────────────────────────────
tab1,tab2,tab3,tab4 = st.tabs([
    "  Mission Sizing  ",
    "  Sensitivity Analysis  ",
    "  Weight Breakdown  ",
    "  Export  "
])

# ════════════════════════════════════════════
# TAB 1 — MISSION SIZING
# ════════════════════════════════════════════
with tab1:

    # ── Row 1: fractions table + convergence ──
    r1a, r1b = st.columns([3,2], gap="medium")

    with r1a:
        st.markdown('<div class="card"><div class="ct">Phase Weight Fractions — Mission Profile</div>', unsafe_allow_html=True)

        phases = list(RR['fracs'].keys())
        fvals  = list(RR['fracs'].values())
        cum    = [1.0]
        for f in fvals: cum.append(cum[-1]*f)

        # Combined subplot: bar + cumulative line
        fig_m = make_subplots(
            rows=1, cols=2,
            column_widths=[0.6, 0.4],
            subplot_titles=["Wi / Wi-1 per phase", "Cumulative weight fraction"],
        )
        bar_clr = ['#38BDF8' if p not in ('Cruise','Loiter') else '#10B981' for p in phases]
        fig_m.add_trace(go.Bar(
            x=phases, y=fvals,
            marker_color=bar_clr,
            marker_line_color='#fff', marker_line_width=0.8,
            text=[f'{v:.4f}' for v in fvals],
            textposition='outside', textfont=dict(size=8),
            name='Wi/Wi-1',
        ), row=1, col=1)

        cum_phases = ['Start']+phases
        fig_m.add_trace(go.Scatter(
            x=cum_phases, y=cum,
            mode='lines+markers',
            line=dict(color='#0EA5E9', width=2),
            marker=dict(color='#0F172A', size=5, line=dict(color='#0EA5E9',width=1.5)),
            fill='tozeroy', fillcolor='rgba(14,165,233,0.07)',
            name='Cumulative',
        ), row=1, col=2)

        fig_m.update_layout(
            paper_bgcolor='rgba(255,255,255,0)',
            plot_bgcolor='#FAFBFC',
            height=230,
            showlegend=False,
            margin=dict(l=40, r=10, t=36, b=36),
        )
        fig_m.update_xaxes(**_AX)
        fig_m.update_yaxes(**_AX)
        fig_m.update_yaxes(range=[0.78, 1.03], row=1, col=1)
        fig_m.update_yaxes(range=[0.70, 1.05], row=1, col=2)
        fig_m.update_annotations(font_size=9, font_color='#475569',
                                  font_family='JetBrains Mono')
        st.plotly_chart(fig_m, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with r1b:
        st.markdown('<div class="card"><div class="ct">Sizing Convergence Check</div>', unsafe_allow_html=True)
        conv_data = {
            'Item': ['W_E Tentative','W_E Allowable','ΔWE','Mff','W_TO'],
            'Value': [
                f"{RR['WE']:,.0f} lbs",
                f"{RR['WEa']:,.0f} lbs",
                f"{RR['diff']:+.1f} lbs",
                f"{RR['Mff']:.5f}",
                f"{Wto:,.0f} lbs",
            ],
            '': ['—','—', '✓' if conv else '✗','—','—'],
        }
        st.dataframe(pd.DataFrame(conv_data), hide_index=True, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card"><div class="ct">Payload Breakdown</div>', unsafe_allow_html=True)
        st.dataframe(pd.DataFrame({
            'Item': [f'{npax} passengers',f'@ {wpax}+{wbag} lbs','Crew (×{ncrew})',f'Attendants (×{natt})','Total payload'],
            'Weight (lbs)': [
                f"{npax*(wpax+wbag):,.0f}",
                "pax+bag",
                f"{ncrew*205:,.0f}",
                f"{natt*200:,.0f}",
                f"{Wpl:,.0f}",
            ],
        }), hide_index=True, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Row 2: range sweep + pax sweep ──
    r2a, r2b = st.columns(2, gap="medium")

    with r2a:
        st.markdown('<div class="card"><div class="ct">Parametric — W_TO vs Design Range</div>', unsafe_allow_html=True)
        rr_arr = np.linspace(200,4000,60); ww_arr=[]
        for rv in rr_arr:
            try: w,_=solve({**P,'R':float(rv)}); ww_arr.append(w)
            except: ww_arr.append(float('nan'))
        fig_r=go.Figure()
        fig_r.add_trace(go.Scatter(
            x=rr_arr, y=ww_arr, mode='lines',
            line=dict(color='#38BDF8',width=2),
            fill='tozeroy', fillcolor='rgba(56,189,248,0.07)',
            name='W_TO',
        ))
        fig_r.add_vline(x=R_nm, line_dash='dash', line_color='#F59E0B', line_width=1.2,
                        annotation_text=f'{R_nm} nm',
                        annotation_font_color='#B45309', annotation_font_size=8.5)
        fig_r.add_scatter(x=[R_nm], y=[Wto], mode='markers',
                          marker=dict(color='#F59E0B',size=9,
                                      line=dict(color='#fff',width=1.5)),
                          showlegend=False)
        pfig(fig_r, h=210, xt='Range (nm)', yt='W_TO (lbs)')
        st.plotly_chart(fig_r, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with r2b:
        st.markdown('<div class="card"><div class="ct">Parametric — W_TO vs Passenger Count</div>', unsafe_allow_html=True)
        pxa=np.arange(5,npax+30,2); wxr=[]
        for n_ in pxa:
            try: w,_=solve({**P,'npax':int(n_)}); wxr.append(w)
            except: wxr.append(float('nan'))
        fig_px=go.Figure()
        fig_px.add_trace(go.Scatter(
            x=pxa, y=wxr, mode='lines',
            line=dict(color='#10B981',width=2),
            fill='tozeroy', fillcolor='rgba(16,185,129,0.07)',
        ))
        fig_px.add_vline(x=npax, line_dash='dash', line_color='#F59E0B', line_width=1.2,
                         annotation_text=f'{npax} pax',
                         annotation_font_color='#B45309', annotation_font_size=8.5)
        fig_px.add_scatter(x=[npax], y=[Wto], mode='markers',
                           marker=dict(color='#F59E0B',size=9,
                                       line=dict(color='#fff',width=1.5)),
                           showlegend=False)
        pfig(fig_px, h=210, xt='Passengers', yt='W_TO (lbs)')
        st.plotly_chart(fig_px, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════
# TAB 2 — SENSITIVITY
# ════════════════════════════════════════════
with tab2:

    # Tables side by side
    s1, s2 = st.columns(2, gap="medium")
    with s1:
        st.markdown('<div class="card"><div class="ct">Range Phase — Breguet Partials  (Eq. 2.49–2.51)</div>', unsafe_allow_html=True)
        sdr={'Partial':['∂W_TO/∂Cp','∂W_TO/∂ηp','∂W_TO/∂(L/D)','∂W_TO/∂R'],
             'Value':[f"{S['dCpR']:+,.0f}",f"{S['dnpR']:+,.0f}",
                      f"{S['dLDR']:+,.0f}",f"{S['dR']:+,.1f}"],
             'Units':['lbs/(lbs/hp/hr)','lbs','lbs','lbs/nm'],
             'Eq.':['2.49','2.50','2.51','2.45']}
        st.dataframe(pd.DataFrame(sdr),hide_index=True,use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with s2:
        st.markdown('<div class="card"><div class="ct">Loiter Phase — Breguet Partials</div>', unsafe_allow_html=True)
        sdl={'Partial':['∂W_TO/∂Cp','∂W_TO/∂ηp','∂W_TO/∂(L/D)'],
             'Value':[f"{S['dCpE']:+,.0f}",f"{S['dnpE']:+,.0f}",f"{S['dLDE']:+,.0f}"],
             'Units':['lbs/(lbs/hp/hr)','lbs','lbs'],
             'Eq.':['—','—','—']}
        st.dataframe(pd.DataFrame(sdl),hide_index=True,use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Tornado chart
    st.markdown('<div class="card"><div class="ct">Tornado Chart — ΔW_TO Sensitivity Ranking</div>', unsafe_allow_html=True)
    tlbl=['Cp · Range','ηp · Range','L/D · Range','Range R',
          'Cp · Loiter','ηp · Loiter','L/D · Loiter']
    tval=[S['dCpR'],S['dnpR'],S['dLDR'],S['dR']*R_nm*0.1,
          S['dCpE'],S['dnpE'],S['dLDE']]
    idx=sorted(range(7),key=lambda i:abs(tval[i]))
    tlbl=[tlbl[i] for i in idx]; tval=[tval[i] for i in idx]
    fig_t=go.Figure()
    fig_t.add_trace(go.Bar(
        x=tval, y=tlbl, orientation='h',
        marker_color=['#38BDF8' if v>=0 else '#F87171' for v in tval],
        marker_line_color='#fff', marker_line_width=0.5,
        text=[f'{abs(v):,.0f} lbs' for v in tval],
        textposition='outside', textfont=dict(size=8.5),
    ))
    fig_t.add_vline(x=0, line_color='#CBD5E1', line_width=1)
    pfig(fig_t, h=260, xt='ΔW_TO (lbs)  —  Blue = increases gross weight  ·  Red = decreases gross weight')
    st.plotly_chart(fig_t, use_container_width=True)
    st.markdown("""
<div style="font-size:.75rem;color:#64748B;margin-top:.2rem;font-family:JetBrains Mono,monospace">
Note: R sensitivity scaled to 10% of design range change.  All values in lbs per unit parameter change.
</div>
""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 3D surface — compact
    st.markdown('<div class="card"><div class="ct">3D Parametric Surface — W_TO  =  f(Cp, L/D)  at Cruise</div>', unsafe_allow_html=True)
    cpa=np.linspace(0.35,0.95,22); lda=np.linspace(8,22,22)
    Z=np.zeros((len(cpa),len(lda)))
    for i,cp in enumerate(cpa):
        for j,ld in enumerate(lda):
            try: w,_=solve({**P,'Cpc':float(cp),'LDc':float(ld)}); Z[i,j]=w
            except: Z[i,j]=float('nan')
    fig4=go.Figure(go.Surface(
        x=lda,y=cpa,z=Z,
        colorscale=[[0,'#EFF6FF'],[0.5,'#38BDF8'],[1,'#0369A1']],
        opacity=0.90, showscale=True,
        contours=dict(z=dict(show=True,color='rgba(0,0,0,0.08)',width=1)),
        colorbar=dict(len=0.65,thickness=10,
                      tickfont=dict(size=8,color='#475569',family='JetBrains Mono')),
    ))
    fig4.update_layout(
        paper_bgcolor='rgba(255,255,255,0)',
        font=dict(family='JetBrains Mono',color='#475569',size=9),
        scene=dict(
            xaxis=dict(title='L/D',backgroundcolor='#F8FAFC',
                       gridcolor='#E2E8F0',linecolor='#E2E8F0'),
            yaxis=dict(title='Cp',backgroundcolor='#F8FAFC',
                       gridcolor='#E2E8F0',linecolor='#E2E8F0'),
            zaxis=dict(title='W_TO (lbs)',backgroundcolor='#F8FAFC',
                       gridcolor='#E2E8F0',linecolor='#E2E8F0'),
            bgcolor='#FAFBFC',
            camera=dict(eye=dict(x=1.6,y=-1.6,z=0.9)),
        ),
        margin=dict(l=0,r=0,t=10,b=0),height=380,
    )
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════
# TAB 3 — WEIGHT BREAKDOWN
# ════════════════════════════════════════════
with tab3:

    w1, w2 = st.columns([5,4], gap="medium")

    with w1:
        # Full weight statement table
        st.markdown('<div class="card"><div class="ct">Weight Statement</div>', unsafe_allow_html=True)
        summary=pd.DataFrame({
            'Component':[
                'W_TO  Gross takeoff weight',
                'W_E   Empty weight',
                'W_OE  Operating empty',
                'W_F   Total fuel',
                'W_F   Usable fuel',
                'W_tfo Trapped fuel & oil',
                'W_crew Flight & cabin crew',
                'W_PL  Payload',
            ],
            'lbs':[f"{Wto:,.0f}",f"{WE:,.0f}",f"{WOE:,.0f}",
                   f"{WF:,.0f}",f"{RR['WFu']:,.0f}",
                   f"{Wtfo:,.0f}",f"{Wcrew:,.0f}",f"{Wpl:,.0f}"],
            'Fraction':[
                "1.00000",
                f"{WE/Wto:.5f}",f"{WOE/Wto:.5f}",
                f"{WF/Wto:.5f}",f"{RR['WFu']/Wto:.5f}",
                f"{Wtfo/Wto:.5f}",f"{Wcrew/Wto:.5f}",f"{Wpl/Wto:.5f}",
            ],
            '% W_TO':[
                "100.00%",
                f"{WE/Wto*100:.2f}%",f"{WOE/Wto*100:.2f}%",
                f"{WF/Wto*100:.2f}%",f"{RR['WFu']/Wto*100:.2f}%",
                f"{Wtfo/Wto*100:.3f}%",f"{Wcrew/Wto*100:.3f}%",
                f"{Wpl/Wto*100:.2f}%",
            ],
        })
        st.dataframe(summary, hide_index=True, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Mission weight trace
        st.markdown('<div class="card"><div class="ct">Aircraft Weight Through Mission</div>', unsafe_allow_html=True)
        fv=list(RR['fracs'].values()); pl=['Ramp']+list(RR['fracs'].keys())
        cum=[Wto]
        for f in fv: cum.append(cum[-1]*f)
        fuel_burn=[cum[0]-c for c in cum]
        fig_w=make_subplots(rows=1,cols=2,
            subplot_titles=['Gross weight (lbs)','Fuel burned (lbs)'])
        fig_w.add_trace(go.Scatter(
            x=pl,y=cum,mode='lines+markers',
            line=dict(color='#38BDF8',width=2),
            marker=dict(color='#0F172A',size=5,line=dict(color='#38BDF8',width=1.5)),
            fill='tozeroy',fillcolor='rgba(56,189,248,0.06)',name='Weight'),row=1,col=1)
        fig_w.add_trace(go.Scatter(
            x=pl,y=fuel_burn,mode='lines+markers',
            line=dict(color='#F59E0B',width=2),
            marker=dict(color='#0F172A',size=5,line=dict(color='#F59E0B',width=1.5)),
            fill='tozeroy',fillcolor='rgba(245,158,11,0.06)',name='Fuel burned'),row=1,col=2)
        fig_w.update_layout(
            paper_bgcolor='rgba(255,255,255,0)',
            plot_bgcolor='#FAFBFC',
            height=210, showlegend=False,
            margin=dict(l=40,r=10,t=34,b=34),
        )
        fig_w.update_xaxes(**_AX)
        fig_w.update_yaxes(**_AX)
        fig_w.update_annotations(font_size=9,font_color='#475569',font_family='JetBrains Mono')
        st.plotly_chart(fig_w, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with w2:
        # Donut
        st.markdown('<div class="card"><div class="ct">W_TO Component Breakdown</div>', unsafe_allow_html=True)
        fig_p=go.Figure(go.Pie(
            labels=['Empty Weight','Usable Fuel','Trapped Fuel','Crew','Payload'],
            values=[WE,RR['WFu'],Wtfo,Wcrew,Wpl],
            hole=0.56,
            marker=dict(
                colors=['#0EA5E9','#38BDF8','#7DD3FC','#10B981','#34D399'],
                line=dict(color='#fff',width=2)),
            textfont=dict(size=9.5,family='JetBrains Mono'),
            textinfo='label+percent',
            rotation=90,
        ))
        fig_p.update_layout(
            paper_bgcolor='rgba(255,255,255,0)',
            font=dict(family='JetBrains Mono',color='#475569'),
            showlegend=False, height=270,
            margin=dict(t=10,b=10,l=10,r=10),
            annotations=[dict(
                text=f'<b>{Wto:,.0f}</b><br>lbs total',
                x=0.5,y=0.5,showarrow=False,
                font=dict(size=11,color='#0F172A',family='JetBrains Mono')
            )],
        )
        st.plotly_chart(fig_p, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Key ratios
        st.markdown('<div class="card"><div class="ct">Key Design Ratios</div>', unsafe_allow_html=True)
        st.dataframe(pd.DataFrame({
            'Ratio':[
                'Payload / W_TO',
                'Fuel / W_TO',
                'Empty / W_TO',
                'OEW / W_TO',
                'Payload / Empty',
            ],
            'Value':[
                f"{Wpl/Wto:.4f}",
                f"{WF/Wto:.4f}",
                f"{WE/Wto:.4f}",
                f"{WOE/Wto:.4f}",
                f"{Wpl/WE:.4f}",
            ],
        }), hide_index=True, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Phase fraction table
        st.markdown('<div class="card"><div class="ct">Phase Fraction Detail</div>', unsafe_allow_html=True)
        st.dataframe(pd.DataFrame({
            'Phase': list(RR['fracs'].keys()),
            'Wi/Wi-1': [f"{v:.4f}" for v in RR['fracs'].values()],
            'Source': ['T2.1','T2.1','T2.1','Fig2.2','Eq2.9','Eq2.11','T2.1','T2.1'],
        }), hide_index=True, use_container_width=True)
        st.markdown(f'<div style="font-family:JetBrains Mono;font-size:.78rem;color:#374151;margin-top:.5rem">Mff = <b style="color:#0EA5E9">{RR["Mff"]:.6f}</b></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════
# TAB 4 — EXPORT
# ════════════════════════════════════════════
with tab4:
    e1, e2 = st.columns([1,1], gap="medium")

    with e1:
        st.markdown('<div class="card"><div class="ct">Export — Spreadsheet (CSV)</div>', unsafe_allow_html=True)
        rows={
            'Parameter':['W_TO','Mff','W_F_total','W_F_usable','W_payload','W_empty',
                          'W_OE','W_crew','W_tfo','WE_allowable','delta_WE',
                          'dWTO_dCp_R','dWTO_dnp_R','dWTO_dLD_R','dWTO_dR',
                          'dWTO_dCp_E','dWTO_dnp_E','dWTO_dLD_E'],
            'Value':[Wto,RR['Mff'],WF,RR['WFu'],Wpl,WE,WOE,Wcrew,Wtfo,
                     RR['WEa'],RR['diff'],
                     S['dCpR'],S['dnpR'],S['dLDR'],S['dR'],
                     S['dCpE'],S['dnpE'],S['dLDE']],
            'Units':['lbs','—','lbs','lbs','lbs','lbs','lbs','lbs','lbs','lbs','lbs',
                     'lbs/(lbs/hp/hr)','lbs','lbs','lbs/nm',
                     'lbs/(lbs/hp/hr)','lbs','lbs'],
        }
        b=io.StringIO(); pd.DataFrame(rows).to_csv(b,index=False)
        st.download_button("⬇  Download Results  (CSV)",b.getvalue(),
                           "aerosizer_results.csv","text/csv",use_container_width=True)
        st.markdown("<br>", unsafe_allow_html=True)
        b2=io.StringIO()
        pd.DataFrame({'Phase':list(RR['fracs'].keys()),
                       'Wi/Wi-1':list(RR['fracs'].values()),
                       'Source':['T2.1','T2.1','T2.1','Fig2.2','Eq2.9','Eq2.11','T2.1','T2.1'],
                       }).to_csv(b2,index=False)
        st.download_button("⬇  Download Phase Fractions  (CSV)",b2.getvalue(),
                           "aerosizer_fractions.csv","text/csv",use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card"><div class="ct">Active Configuration</div>', unsafe_allow_html=True)
        st.dataframe(pd.DataFrame({
            'Parameter':list(P.keys()),
            'Value':[str(v) for v in P.values()]}),
            hide_index=True,use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with e2:
        st.markdown('<div class="card"><div class="ct">Export — Formal Report  (PDF / A4)</div>', unsafe_allow_html=True)
        st.markdown("""
<div style="font-size:.8rem;color:#475569;line-height:1.75;font-family:Inter,sans-serif">
Report includes:<br>
&nbsp; &nbsp;① &nbsp;Mission inputs &amp; configuration<br>
&nbsp; &nbsp;② &nbsp;Sizing convergence verification<br>
&nbsp; &nbsp;③ &nbsp;Full weight statement (8 components)<br>
&nbsp; &nbsp;④ &nbsp;Phase weight fractions with source references<br>
&nbsp; &nbsp;⑤ &nbsp;Breguet sensitivity partials (Table 2.20)<br>
&nbsp; &nbsp;⑥ &nbsp;Key design ratios
</div>
<br>
""", unsafe_allow_html=True)
        def make_pdf():
            buf=io.BytesIO()
            doc=SimpleDocTemplate(buf,pagesize=A4,
                leftMargin=2*cm,rightMargin=2*cm,topMargin=2*cm,bottomMargin=2*cm)
            sty=getSampleStyleSheet()
            def ps(nm,**kw): return ParagraphStyle(nm,parent=sty['Normal'],**kw)
            sT=ps('T',fontSize=18,fontName='Helvetica-Bold',
                   textColor=colors.HexColor('#0F172A'),spaceAfter=2)
            sSub=ps('S',fontSize=8.5,textColor=colors.HexColor('#64748B'),spaceAfter=14)
            sH=ps('H',fontSize=10.5,fontName='Helvetica-Bold',
                   textColor=colors.HexColor('#0369A1'),spaceBefore=14,spaceAfter=5)
            sB=ps('B',fontSize=8.5,leading=13,textColor=colors.HexColor('#374151'))
            ts=TableStyle([
                ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#0F172A')),
                ('TEXTCOLOR',(0,0),(-1,0),colors.white),
                ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
                ('FONTNAME',(0,1),(-1,-1),'Helvetica'),
                ('FONTSIZE',(0,0),(-1,-1),8),
                ('GRID',(0,0),(-1,-1),0.35,colors.HexColor('#CBD5E1')),
                ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#F8FAFC')]),
                ('LEFTPADDING',(0,0),(-1,-1),5),
                ('RIGHTPADDING',(0,0),(-1,-1),5),
                ('TOPPADDING',(0,0),(-1,-1),3.5),
                ('BOTTOMPADDING',(0,0),(-1,-1),3.5),
            ])
            story=[
                Paragraph("AeroSizer Pro", sT),
                Paragraph("Preliminary Aircraft Weight Estimation · Breguet Method · Propeller-Driven", sSub),
                HRFlowable(width="100%",thickness=1.5,color=colors.HexColor('#38BDF8')),
                Spacer(1,.2*cm),
                Paragraph("1.  Mission Inputs", sH),
            ]
            t1=Table([['Parameter','Value','Parameter','Value'],
                ['Passengers',str(npax),'Design range (nm)',str(R_nm)],
                ['Pax wt (lbs)',str(wpax),'Loiter endurance (hr)',str(El)],
                ['Baggage (lbs)',str(wbag),'Cruise L/D',str(LDc)],
                ['Flight crew',str(ncrew),'Loiter L/D',str(LDl)],
                ['Cabin att.',str(natt),'SFC Cp cruise',str(Cpc)],
                ['A (regr.)',f'{A_v:.4f}','SFC Cp loiter',str(Cpl)],
                ['B (regr.)',f'{B_v:.4f}','M_tfo',str(Mtfo)]],
                colWidths=[4.2*cm,2.8*cm,4.2*cm,2.8*cm])
            t1.setStyle(ts)
            story+=[t1,Spacer(1,.15*cm)]
            story.append(Paragraph("2.  Sizing Result", sH))
            story.append(Paragraph(
                f"W_TO = <b>{Wto:,.0f} lbs</b> &nbsp;|&nbsp; Mff = {RR['Mff']:.5f}"
                f" &nbsp;|&nbsp; ΔWE = {RR['diff']:+.1f} lbs &nbsp;|&nbsp; "
                f"Status: {'CONVERGED' if conv else 'NOT CONVERGED'}", sB))
            story+=[Spacer(1,.1*cm),Paragraph("3.  Weight Statement", sH)]
            t2=Table([['Component','lbs','Fraction','% W_TO']]+
                list(zip(summary['Component'],summary['lbs'],
                          summary['Fraction'],summary['% W_TO'])),
                colWidths=[7.5*cm,2.5*cm,2.5*cm,1.5*cm])
            t2.setStyle(ts)
            story+=[t2,Spacer(1,.1*cm)]
            story.append(Paragraph("4.  Phase Weight Fractions", sH))
            t3=Table([['Phase','Wi / Wi-1','Source']]+
                list(zip(list(RR['fracs'].keys()),
                          [f"{v:.5f}" for v in RR['fracs'].values()],
                          ['T2.1','T2.1','T2.1','Fig2.2','Eq2.9','Eq2.11','T2.1','T2.1'])),
                colWidths=[5*cm,3*cm,3*cm])
            t3.setStyle(ts)
            story+=[t3,Spacer(1,.1*cm)]
            story.append(Paragraph("5.  Sensitivity Partials  (Breguet — Table 2.20)", sH))
            all_partials=(
                list(zip(sdr['Partial'],sdr['Value'],sdr['Units'],sdr['Eq.']))+
                list(zip(sdl['Partial'],sdl['Value'],sdl['Units'],sdl['Eq.'])))
            t4=Table([['Partial','Value','Units','Eq.']]+all_partials,
                colWidths=[4*cm,2.5*cm,4*cm,1.5*cm])
            t4.setStyle(ts)
            story.append(t4)
            doc.build(story); buf.seek(0); return buf.read()

        st.download_button("⬇  Generate & Download PDF  (A4)",
            make_pdf(),"aerosizer_report.pdf","application/pdf",use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
