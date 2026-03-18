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
                                 Table, TableStyle, HRFlowable, KeepTogether)
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

st.set_page_config(page_title="AeroSizer Pro", page_icon="✈", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500;600&display=swap');
*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] {
    background: #F5F7FA !important;
    color: #1A1D2E !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stApp { background: #F5F7FA !important; }

.card { background:#fff; border:1px solid #E2E8F0; border-radius:12px;
  padding:1.1rem 1.3rem; margin-bottom:0.9rem; }
.ct { font-family:'DM Mono',monospace; font-size:0.66rem; font-weight:500;
  color:#0369A1; letter-spacing:0.13em; text-transform:uppercase;
  padding-bottom:0.5rem; border-bottom:1px solid #F1F5F9; margin-bottom:0.8rem; }
.cn { font-size:0.74rem; color:#94A3B8; line-height:1.6; margin-top:0.5rem; }

.kpi { background:#fff; border:1px solid #BAE6FD; border-radius:12px;
  padding:1.1rem 1.2rem; border-top:3px solid #0EA5E9;
  box-shadow:0 2px 10px rgba(14,165,233,0.10); }
.kv { font-family:'DM Mono',monospace; font-size:1.65rem; font-weight:600;
  color:#0369A1; line-height:1.1; }
.ku { font-size:0.75rem; color:#64748B; margin-left:0.2rem; font-weight:400; }
.kl { font-size:0.62rem; color:#64748B; letter-spacing:0.09em;
  margin-top:0.35rem; text-transform:uppercase; font-weight:500; }

.s-ok { background:#F0FDF4; border-left:3px solid #22C55E; border-radius:0 8px 8px 0;
  padding:0.55rem 1.1rem; font-family:'DM Mono',monospace; font-size:0.78rem;
  color:#15803D; margin-bottom:1.2rem; }
.s-err { background:#FFF7ED; border-left:3px solid #F97316; border-radius:0 8px 8px 0;
  padding:0.55rem 1.1rem; font-family:'DM Mono',monospace; font-size:0.78rem;
  color:#C2410C; margin-bottom:1.2rem; }

[data-testid="stSidebar"] { background:#fff !important; border-right:1px solid #E2E8F0 !important; }
.sb-sec { font-family:'DM Mono',monospace; font-size:0.61rem; font-weight:500;
  color:#0369A1; letter-spacing:0.15em; text-transform:uppercase;
  padding:0.4rem 0 0.32rem; border-bottom:1px solid #F1F5F9; margin:0.55rem 0 0.6rem; }

.stTabs [data-baseweb="tab-list"] { background:#fff; border-radius:9px;
  padding:3px; border:1px solid #E2E8F0; gap:2px; margin-bottom:0.9rem; }
.stTabs [data-baseweb="tab"] { border-radius:6px; font-size:0.78rem; font-weight:500;
  color:#64748B; padding:0.38rem 1rem; }
.stTabs [aria-selected="true"] { background:#0D1B2A !important; color:#fff !important; }

div.stDownloadButton > button { background:#0D1B2A !important; color:#fff !important;
  border:none !important; border-radius:8px !important; font-size:0.78rem !important;
  font-weight:500 !important; padding:0.5rem 1rem !important; width:100% !important; }
div.stDownloadButton > button:hover { background:#1B2B4B !important; }

[data-testid="stSidebar"] div.stButton > button {
  background:linear-gradient(135deg,#0369A1,#0EA5E9) !important;
  color:#fff !important; border:none !important; border-radius:9px !important;
  font-size:0.85rem !important; font-weight:600 !important;
  padding:0.65rem !important; width:100% !important;
  box-shadow:0 2px 8px rgba(14,165,233,0.3) !important; }
</style>
""", unsafe_allow_html=True)

# ── Plotly theme ──────────────────────────────────────────────────
_B = dict(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='#FAFBFC',
          font=dict(family='DM Mono', color='#475569', size=9.5),
          margin=dict(l=52,r=14,t=30,b=40),
          hoverlabel=dict(bgcolor='#0D1B2A',font_color='#fff',font_size=10))
_AX = dict(gridcolor='#F1F5F9', linecolor='#E2E8F0', zerolinecolor='#E2E8F0')

def pf(fig, h=220, xt='', yt='', yr=None):
    fig.update_layout(**_B, height=h)
    fig.update_xaxes(**_AX)
    fig.update_yaxes(**_AX)
    if xt: fig.update_xaxes(title_text=xt, title_font=dict(size=8, color='#94A3B8'))
    if yt: fig.update_yaxes(title_text=yt, title_font=dict(size=8, color='#94A3B8'))
    if yr: fig.update_yaxes(range=yr)
    return fig

# ── Physics ───────────────────────────────────────────────────────
def mission(p):
    Wpl   = p['npax']*(p['wpax']+p['wbag']) + p['ncrew']*205 + p['natt']*200
    Wcrew = p['ncrew']*205 + p['natt']*200
    Wtfo  = p['Wto']*p['Mtfo']
    Rc    = p['R']*1.15078
    W5    = 1.0/math.exp(Rc / (375.0*(p['npc']/p['Cpc'])*p['LDc']))
    Vm    = p['Vl']*1.15078
    W6    = 1.0/math.exp(p['El'] / (375.0*(1.0/Vm)*(p['npl']/p['Cpl'])*p['LDl']))
    fn = ['Engine Start','Taxi','Takeoff','Climb','Cruise','Loiter','Descent','Landing']
    fv = [0.990, 0.995, 0.995, 0.985, W5, W6, 0.985, 0.995]
    Mff = 1.0
    for v in fv: Mff *= v
    WFu = p['Wto']*(1.0-Mff)
    WF  = WFu + p['Wto']*p['Mr']*(1.0-Mff) + Wtfo
    WOE = p['Wto'] - WF - Wpl
    WE  = WOE - Wtfo - Wcrew
    WEa = 10.0**((math.log10(p['Wto'])-p['A'])/p['B'])
    return dict(Wpl=Wpl, Wcrew=Wcrew, Wtfo=Wtfo, Mff=Mff,
                WF=WF, WFu=WFu, WOE=WOE, WE=WE, WEa=WEa,
                diff=WEa-WE, fracs=dict(zip(fn,fv)))

def solve(p, tol=0.2, n=500):
    pp = dict(p)
    prev_d, prev_w, lo, hi = None, None, None, None
    for w in range(8000, 500001, 2000):
        pp['Wto'] = float(w)
        d = mission(pp)['diff']
        if prev_d is not None and prev_d*d <= 0:
            lo, hi = float(prev_w), float(w); break
        prev_d, prev_w = d, w
    if lo is None:
        pp['Wto'] = 48550.0; return 48550.0, mission(pp)
    for _ in range(n):
        m=(lo+hi)/2.0; pp['Wto']=m; r=mission(pp)
        if abs(r['diff'])<tol: return m, r
        if r['diff']>0: lo=m
        else: hi=m
    return m, mission(pp)

def sens(p, Wto):
    Rc  = p['R']*1.15078
    Vm  = p['Vl']*1.15078
    Mff = mission({**p,'Wto':Wto})['Mff']
    Wpl = p['npax']*(p['wpax']+p['wbag'])+p['ncrew']*205+p['natt']*200
    Wcrew=p['ncrew']*205+p['natt']*200
    C  = 1.0-(1.0+p['Mr'])*(1.0-Mff)-p['Mtfo']
    D  = Wpl+Wcrew
    dn = C*Wto*(1.0-p['B'])-D
    F  = (-p['B']*Wto**2*(1.0+p['Mr'])*Mff)/dn if abs(dn)>1e-6 else 0.0
    E  = p['El']
    return dict(
        dCpR=  F*Rc/(375.0*p['npc']*p['LDc']),
        dnpR= -F*Rc*p['Cpc']/(375.0*p['npc']**2*p['LDc']),
        dLDR= -F*Rc*p['Cpc']/(375.0*p['npc']*p['LDc']**2),
        dR=    F*p['Cpc']/(375.0*p['npc']*p['LDc']),
        dCpE=  F*E*Vm/(375.0*p['npl']*p['LDl']),
        dnpE= -F*E*Vm*p['Cpl']/(375.0*p['npl']**2*p['LDl']),
        dLDE= -F*E*Vm*p['Cpl']/(375.0*p['npl']*p['LDl']**2),
    )

# ── Defaults & sidebar ────────────────────────────────────────────
D = dict(npax=34,wpax=175,wbag=30,ncrew=2,natt=1,Mtfo=0.005,Mr=0.0,
         R=1100,Vl=250,LDc=13,Cpc=0.60,npc=0.85,
         El=0.75,LDl=16,Cpl=0.65,npl=0.77,A=0.3774,B=0.9647)

with st.sidebar:
    st.markdown('<div style="font-family:DM Mono,monospace;font-size:1rem;font-weight:500;color:#0D1B2A">AERO<span style="color:#0EA5E9">SIZER</span> PRO</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-family:DM Mono,monospace;font-size:0.6rem;color:#94A3B8;letter-spacing:0.14em;text-transform:uppercase;margin-bottom:1rem">Aircraft Weight Estimation</div>', unsafe_allow_html=True)

    st.markdown('<div class="sb-sec">Cabin & Crew</div>', unsafe_allow_html=True)
    npax  = st.number_input("Passengers",              1,  400, D['npax'],  step=1)
    wpax  = st.number_input("Passenger weight (lbs)", 100, 300, D['wpax'],  step=5)
    wbag  = st.number_input("Baggage weight (lbs)",    0,  100, D['wbag'],  step=5)
    ncrew = st.number_input("Flight crew",              1,    6, D['ncrew'], step=1)
    natt  = st.number_input("Cabin attendants",         0,   10, D['natt'],  step=1)

    st.markdown('<div class="sb-sec">Cruise Segment</div>', unsafe_allow_html=True)
    R_nm = st.number_input("Design range (nm)",     100,  6000, D['R'],           step=50)
    LDc  = st.number_input("Cruise L/D",            4.0,  30.0, float(D['LDc']), step=0.5, format="%.1f")
    Cpc  = st.number_input("Cruise SFC Cp (lbs/hp/hr)", 0.20, 1.20, D['Cpc'],    step=0.01, format="%.2f")
    npc  = st.number_input("Cruise prop. eff. η_p", 0.30, 0.98, D['npc'],        step=0.01, format="%.2f")

    st.markdown('<div class="sb-sec">Loiter / Reserve</div>', unsafe_allow_html=True)
    El   = st.number_input("Loiter endurance (hr)", 0.10,  6.0, D['El'],          step=0.05, format="%.2f")
    Vl   = st.number_input("Loiter speed (kts)",      60,  400, D['Vl'],          step=5)
    LDl  = st.number_input("Loiter L/D",             4.0, 30.0, float(D['LDl']), step=0.5, format="%.1f")
    Cpl  = st.number_input("Loiter SFC Cp (lbs/hp/hr)", 0.20, 1.20, D['Cpl'],    step=0.01, format="%.2f")
    npl  = st.number_input("Loiter prop. eff. η_p", 0.30, 0.98, D['npl'],        step=0.01, format="%.2f")

    st.markdown('<div class="sb-sec">Sizing Constants — Raymer T2.2</div>', unsafe_allow_html=True)
    A_v  = st.number_input("Constant A", 0.0,  2.0, D['A'],    step=0.001, format="%.4f")
    B_v  = st.number_input("Constant B", 0.1,  2.0, D['B'],    step=0.001, format="%.4f")
    Mtfo = st.number_input("M_tfo",      0.0, 0.05, D['Mtfo'], step=0.001, format="%.3f")
    Wto_g= st.number_input("W_TO initial guess (lbs)", 5000, 500000, 48550, step=1000)

    st.markdown("<br>", unsafe_allow_html=True)
    calc = st.button("⟳  Calculate", use_container_width=True, type="primary")

# ── FIX: Build current param dict and always recalculate when inputs change ──
P = dict(npax=int(npax), wpax=float(wpax), wbag=float(wbag),
         ncrew=int(ncrew), natt=int(natt), Mtfo=float(Mtfo), Mr=0.0,
         R=float(R_nm), Vl=float(Vl), LDc=float(LDc), Cpc=float(Cpc), npc=float(npc),
         El=float(El), LDl=float(LDl), Cpl=float(Cpl), npl=float(npl),
         A=float(A_v), B=float(B_v), Wto=float(Wto_g))

# ── KEY FIX: recalculate whenever P changes, not just when button pressed ──
P_key = str(sorted(P.items()))
if 'res' not in st.session_state or st.session_state.get('P_key') != P_key or calc:
    Wto, RR = solve(P)
    S = sens(P, Wto)
    st.session_state['res']   = (Wto, RR, S, dict(P))
    st.session_state['P_key'] = P_key
else:
    Wto, RR, S, _ = st.session_state['res']

conv  = abs(RR['diff']) < 5
WE    = RR['WE'];  WOE = RR['WOE']; WF  = RR['WF']
Wpl   = RR['Wpl']; Wcrew=RR['Wcrew']; Wtfo_r=RR['Wtfo']

# ── HERO card ─────────────────────────────────────────────────────
_sc = '#15803D' if conv else '#C2410C'
_sb = '#F0FDF4' if conv else '#FFF7ED'
_st = '✓ converged' if conv else '⚠ check inputs'
st.markdown(f"""
<div style="background:#fff;border:1px solid #BAE6FD;border-radius:14px;
  border-left:5px solid #0EA5E9;padding:0.8rem 1.5rem;margin-bottom:0.9rem;
  display:flex;align-items:center;justify-content:space-between;
  box-shadow:0 2px 10px rgba(14,165,233,0.08)">
  <div style="font-family:'DM Mono',monospace;font-size:1.55rem;font-weight:700;
    color:#0D1B2A;letter-spacing:0.02em;line-height:1">
    AERO<span style="color:#0EA5E9">SIZER</span> PRO
  </div>
  <div style="background:{_sb};color:{_sc};font-family:'DM Mono',monospace;
    font-size:0.68rem;font-weight:600;padding:0.28rem 0.85rem;
    border-radius:20px;letter-spacing:0.07em">{_st}</div>
</div>
""", unsafe_allow_html=True)

# ── status bar ──
if conv:
    st.markdown(f'<div class="s-ok">✓  Converged  ·  W_TO = {Wto:,.0f} lbs  ·  Mff = {RR["Mff"]:.5f}  ·  ΔWE = {RR["diff"]:+.1f} lbs</div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div class="s-err">⚠  Not converged  ·  ΔWE = {RR["diff"]:+.0f} lbs  ·  Adjust inputs or regression constants A, B</div>', unsafe_allow_html=True)

# ── KPI row ──
_kpi_data = [
    (f"{Wto:,.0f}",      "lbs", "Gross Takeoff W_TO",  "#0369A1", "#EFF8FF", "#0EA5E9"),
    (f"{RR['Mff']:.5f}", "",    "Fuel Fraction Mff",   "#0D1B2A", "#F8FAFC", "#94A3B8"),
    (f"{WF:,.0f}",       "lbs", "Total Fuel W_F",      "#0D1B2A", "#F8FAFC", "#94A3B8"),
    (f"{Wpl:,.0f}",      "lbs", "Payload W_PL",        "#0D1B2A", "#F8FAFC", "#94A3B8"),
    (f"{WE:,.0f}",       "lbs", "Empty Weight W_E",    "#0D1B2A", "#F8FAFC", "#94A3B8"),
]
k1,k2,k3,k4,k5 = st.columns(5)
for col,(val,unit,lbl,vc,bg,top) in zip([k1,k2,k3,k4,k5], _kpi_data):
    with col:
        st.markdown(f"""
        <div style="background:{bg};border:1px solid #E2E8F0;border-radius:12px;
          padding:1rem 1.1rem;border-top:3px solid {top};
          box-shadow:0 2px 8px rgba(0,0,0,0.05)">
          <div style="font-family:'DM Mono',monospace;font-size:1.6rem;font-weight:700;
            color:{vc};line-height:1.1">{val}
            <span style="font-size:0.72rem;color:#64748B;font-weight:400;margin-left:2px">{unit}</span>
          </div>
          <div style="font-size:0.62rem;color:#64748B;letter-spacing:0.08em;
            margin-top:0.4rem;text-transform:uppercase;font-weight:500">{lbl}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
tab1,tab2,tab3,tab4,tab5 = st.tabs(["  ① Mission Sizing  ","  ② Sensitivity  ","  ③ Weight Breakdown  ","  ④ Export  ","  ⑤ References  "])

# ════════════════════════════════════════════
# TAB 1
# ════════════════════════════════════════════
with tab1:
    c1,c2 = st.columns([3,2], gap="medium")
    with c1:
        st.markdown('<div class="card"><div class="ct">Mission Phase Weight Fractions — Wi / Wi-1</div>', unsafe_allow_html=True)
        phases = list(RR['fracs'].keys())
        fvals  = list(RR['fracs'].values())
        cum    = [1.0]
        for f in fvals: cum.append(cum[-1]*f)
        fig_m = make_subplots(rows=1,cols=2,column_widths=[0.58,0.42],
            subplot_titles=["Wi / Wi-1  per phase","Cumulative fraction"])
        clr = ['#0EA5E9' if p not in ('Cruise','Loiter') else '#10B981' for p in phases]
        fig_m.add_trace(go.Bar(x=phases,y=fvals,marker_color=clr,
            marker_line_color='#fff',marker_line_width=0.8,
            text=[f'{v:.4f}' for v in fvals],textposition='outside',textfont=dict(size=7.5)),
            row=1,col=1)
        fig_m.add_trace(go.Scatter(x=['Start']+phases,y=cum,mode='lines+markers',
            line=dict(color='#0EA5E9',width=2),
            marker=dict(color='#0D1B2A',size=4,line=dict(color='#0EA5E9',width=1.5)),
            fill='tozeroy',fillcolor='rgba(14,165,233,0.07)'),row=1,col=2)
        fig_m.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='#FAFBFC',
            height=230,showlegend=False,margin=dict(l=38,r=10,t=32,b=34))
        fig_m.update_xaxes(**_AX); fig_m.update_yaxes(**_AX)
        fig_m.update_yaxes(range=[0.78,1.03],row=1,col=1)
        fig_m.update_yaxes(range=[0.70,1.05],row=1,col=2)
        fig_m.update_annotations(font_size=8.5,font_color='#475569',font_family='DM Mono')
        st.plotly_chart(fig_m,use_container_width=True)
        st.markdown('<div class="cn">Blue = fixed fractions (Raymer Table 2.1) · <b>Green</b> = Breguet equations (Eq. 2.9 & 2.11). Product gives Mff.</div></div>', unsafe_allow_html=True)

        st.markdown('<div class="card"><div class="ct">Parametric — W_TO vs Design Range</div>', unsafe_allow_html=True)
        rr_arr=np.linspace(200,min(2800,float(R_nm)*2.5),55); ww_arr=[]
        for rv in rr_arr:
            try:
                w,r=solve({**P,'R':float(rv)})
                ww_arr.append(w if abs(r['diff'])<50 else float('nan'))
            except: ww_arr.append(float('nan'))
        fig_r=go.Figure()
        fig_r.add_trace(go.Scatter(x=rr_arr,y=ww_arr,mode='lines',
            line=dict(color='#0EA5E9',width=2),
            fill='tozeroy',fillcolor='rgba(14,165,233,0.06)'))
        fig_r.add_vline(x=float(R_nm),line_dash='dash',line_color='#F59E0B',line_width=1.2,
            annotation_text=f'{int(R_nm)} nm',annotation_font_color='#B45309',annotation_font_size=8)
        fig_r.add_scatter(x=[float(R_nm)],y=[Wto],mode='markers',
            marker=dict(color='#F59E0B',size=8,line=dict(color='#fff',width=1.5)),showlegend=False)
        pf(fig_r,h=195,xt='Range (nm)',yt='W_TO (lbs)')
        st.plotly_chart(fig_r,use_container_width=True)
        st.markdown('<div class="cn">Nonlinear growth — more range → more fuel → heavier aircraft → even more fuel needed (Breguet penalty). Design point in amber.</div></div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="card"><div class="ct">Sizing Convergence</div>', unsafe_allow_html=True)
        st.dataframe(pd.DataFrame({
            'Parameter':['W_E Tentative','W_E Allowable','ΔWE','Mff','Status'],
            'Value':[f"{RR['WE']:,.0f} lbs",f"{RR['WEa']:,.0f} lbs",
                     f"{RR['diff']:+.1f} lbs",f"{RR['Mff']:.5f}",
                     '✓ OK' if conv else '✗ Retry'],
        }),hide_index=True,use_container_width=True)
        st.markdown('<div class="cn">Converged when W_E_tentative ≈ W_E_allowable. ΔWE < 0.5 lbs accepted.</div></div>', unsafe_allow_html=True)

        st.markdown('<div class="card"><div class="ct">Phase Fractions Detail</div>', unsafe_allow_html=True)
        src={'Engine Start':'T2.1','Taxi':'T2.1','Takeoff':'T2.1','Climb':'Fig2.2',
             'Cruise':'Eq 2.9','Loiter':'Eq 2.11','Descent':'T2.1','Landing':'T2.1'}
        st.dataframe(pd.DataFrame({
            'Phase':list(RR['fracs'].keys()),
            'Wi/Wi-1':[f"{v:.4f}" for v in RR['fracs'].values()],
            'Ref':[src[p] for p in RR['fracs'].keys()],
        }),hide_index=True,use_container_width=True)
        st.markdown(f'<div style="font-family:DM Mono,monospace;font-size:0.78rem;background:#EFF8FF;border-radius:7px;padding:0.4rem 0.8rem;margin-top:0.4rem;color:#0369A1">Mff = {RR["Mff"]:.6f}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card"><div class="ct">Payload Breakdown</div>', unsafe_allow_html=True)
        pld=int(npax)*(int(wpax)+int(wbag))
        st.dataframe(pd.DataFrame({
            'Item':[f'{npax} pax × ({wpax}+{wbag} lbs)',
                    f'Crew × {ncrew} × 205 lbs',
                    f'Cabin att. × {natt} × 200 lbs','Total W_PL'],
            'lbs':[f"{pld:,.0f}",f"{int(ncrew)*205:,.0f}",
                   f"{int(natt)*200:,.0f}",f"{Wpl:,.0f}"],
        }),hide_index=True,use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════
# TAB 2
# ════════════════════════════════════════════
with tab2:
    st.markdown('<div class="card"><div class="ct">What sensitivity analysis means</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.8rem;color:#374151;line-height:1.65">Each partial ∂W_TO/∂y tells you: <b>if parameter y changes by one unit, how many pounds does gross weight change?</b> Large negative value = improving this parameter reduces W_TO significantly (design lever). The tornado chart ranks parameters by influence magnitude.</div></div>', unsafe_allow_html=True)

    sa,sb = st.columns(2,gap="medium")
    with sa:
        st.markdown('<div class="card"><div class="ct">Cruise Phase — Breguet Partials (Eq. 2.49–2.51)</div>', unsafe_allow_html=True)
        sdr={'Partial':['∂W_TO/∂Cp (cruise)','∂W_TO/∂η_p (cruise)','∂W_TO/∂(L/D) (cruise)','∂W_TO/∂R'],
             'Value':[f"{S['dCpR']:+,.0f}",f"{S['dnpR']:+,.0f}",f"{S['dLDR']:+,.0f}",f"{S['dR']:+,.1f}"],
             'Units':['lbs/(lbs/hp/hr)','lbs','lbs','lbs/nm'],
             'Eq.':['2.49','2.50','2.51','2.45']}
        st.dataframe(pd.DataFrame(sdr),hide_index=True,use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with sb:
        st.markdown('<div class="card"><div class="ct">Loiter Phase — Breguet Partials</div>', unsafe_allow_html=True)
        sdl={'Partial':['∂W_TO/∂Cp (loiter)','∂W_TO/∂η_p (loiter)','∂W_TO/∂(L/D) (loiter)'],
             'Value':[f"{S['dCpE']:+,.0f}",f"{S['dnpE']:+,.0f}",f"{S['dLDE']:+,.0f}"],
             'Units':['lbs/(lbs/hp/hr)','lbs','lbs'],
             'Eq.':['—','—','—']}
        st.dataframe(pd.DataFrame(sdl),hide_index=True,use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card"><div class="ct">Tornado Chart — Parameter Influence Ranking</div>', unsafe_allow_html=True)
    tlbl=['Cp · Cruise','η_p · Cruise','L/D · Cruise','Range R','Cp · Loiter','η_p · Loiter','L/D · Loiter']
    tval=[S['dCpR'],S['dnpR'],S['dLDR'],S['dR']*float(R_nm)*0.1,S['dCpE'],S['dnpE'],S['dLDE']]
    idx=sorted(range(7),key=lambda i:abs(tval[i]))
    tlbl=[tlbl[i] for i in idx]; tval=[tval[i] for i in idx]
    fig_t=go.Figure(go.Bar(x=tval,y=tlbl,orientation='h',
        marker_color=['#0EA5E9' if v>=0 else '#F87171' for v in tval],
        marker_line_color='#fff',marker_line_width=0.5,
        text=[f'{abs(v):,.0f} lbs' for v in tval],textposition='outside',textfont=dict(size=9)))
    fig_t.add_vline(x=0,line_color='#CBD5E1',line_width=1)
    pf(fig_t,h=270,xt='ΔW_TO (lbs) per unit change')
    st.plotly_chart(fig_t,use_container_width=True)
    st.markdown('<div class="cn">Blue = increases W_TO · Red = decreases W_TO (good). Range sensitivity shown for 10% of design range.</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="card"><div class="ct">3D Parametric Surface — W_TO = f(Cp, L/D) at Cruise</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.74rem;color:#94A3B8;font-family:DM Mono,monospace;margin-bottom:0.5rem">Rotate · Hover for values · All other parameters fixed</div>', unsafe_allow_html=True)
    cpa=np.linspace(0.35,0.90,20); lda=np.linspace(8,22,20)
    Z=np.zeros((len(cpa),len(lda)))
    for i,cp in enumerate(cpa):
        for j,ld in enumerate(lda):
            try:
                w,r=solve({**P,'Cpc':float(cp),'LDc':float(ld)})
                Z[i,j]=w if abs(r['diff'])<50 else float('nan')
            except: Z[i,j]=float('nan')
    fig4=go.Figure(go.Surface(x=lda,y=cpa,z=Z,
        colorscale=[[0,'#EFF8FF'],[0.4,'#38BDF8'],[0.75,'#0369A1'],[1,'#1E3A5F']],
        opacity=0.92,showscale=True,
        colorbar=dict(len=0.65,thickness=10,tickfont=dict(size=8,color='#475569'))))
    fig4.update_layout(paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='DM Mono',color='#475569',size=9),
        scene=dict(xaxis=dict(title='L/D',backgroundcolor='#F8FAFC',gridcolor='#E2E8F0',linecolor='#E2E8F0'),
                   yaxis=dict(title='Cp',backgroundcolor='#F8FAFC',gridcolor='#E2E8F0',linecolor='#E2E8F0'),
                   zaxis=dict(title='W_TO (lbs)',backgroundcolor='#F8FAFC',gridcolor='#E2E8F0',linecolor='#E2E8F0'),
                   bgcolor='#FAFBFC',camera=dict(eye=dict(x=1.5,y=-1.5,z=0.8))),
        margin=dict(l=0,r=0,t=8,b=0),height=390)
    st.plotly_chart(fig4,use_container_width=True)
    st.markdown('<div class="cn">Bottom-left corner (low Cp, high L/D) = minimum W_TO design space. Cliff = no solution boundary.</div></div>', unsafe_allow_html=True)

# ════════════════════════════════════════════
# TAB 3
# ════════════════════════════════════════════
with tab3:
    w1,w2 = st.columns([5,4],gap="medium")
    with w1:
        st.markdown('<div class="card"><div class="ct">Complete Weight Statement</div>', unsafe_allow_html=True)
        summary=pd.DataFrame({
            'Component':['W_TO — Gross takeoff','W_E — Empty weight','W_OE — Op. empty',
                         'W_F — Total fuel','W_F — Usable fuel','W_tfo — Trapped fuel+oil',
                         'W_crew — Flight+cabin crew','W_PL — Payload'],
            'lbs':[f"{Wto:,.0f}",f"{WE:,.0f}",f"{WOE:,.0f}",f"{WF:,.0f}",
                   f"{RR['WFu']:,.0f}",f"{Wtfo_r:,.0f}",f"{Wcrew:,.0f}",f"{Wpl:,.0f}"],
            'Fraction':["1.00000",f"{WE/Wto:.5f}",f"{WOE/Wto:.5f}",f"{WF/Wto:.5f}",
                        f"{RR['WFu']/Wto:.5f}",f"{Wtfo_r/Wto:.5f}",f"{Wcrew/Wto:.5f}",f"{Wpl/Wto:.5f}"],
            '% W_TO':["100%",f"{WE/Wto*100:.2f}%",f"{WOE/Wto*100:.2f}%",f"{WF/Wto*100:.2f}%",
                      f"{RR['WFu']/Wto*100:.2f}%",f"{Wtfo_r/Wto*100:.3f}%",
                      f"{Wcrew/Wto*100:.3f}%",f"{Wpl/Wto*100:.2f}%"],
        })
        st.dataframe(summary,hide_index=True,use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card"><div class="ct">Weight & Fuel Burn Through Mission</div>', unsafe_allow_html=True)
        fv=list(RR['fracs'].values()); pl=['Ramp']+list(RR['fracs'].keys())
        cum=[Wto]
        for f in fv: cum.append(cum[-1]*f)
        burn=[cum[0]-c for c in cum]
        fig_w=make_subplots(rows=1,cols=2,subplot_titles=['Gross weight (lbs)','Fuel burned (lbs)'])
        fig_w.add_trace(go.Scatter(x=pl,y=cum,mode='lines+markers',
            line=dict(color='#0EA5E9',width=2),
            marker=dict(color='#0D1B2A',size=4,line=dict(color='#0EA5E9',width=1.5)),
            fill='tozeroy',fillcolor='rgba(14,165,233,0.06)'),row=1,col=1)
        fig_w.add_trace(go.Scatter(x=pl,y=burn,mode='lines+markers',
            line=dict(color='#F59E0B',width=2),
            marker=dict(color='#0D1B2A',size=4,line=dict(color='#F59E0B',width=1.5)),
            fill='tozeroy',fillcolor='rgba(245,158,11,0.06)'),row=1,col=2)
        fig_w.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='#FAFBFC',
            height=205,showlegend=False,margin=dict(l=38,r=10,t=30,b=32))
        fig_w.update_xaxes(**_AX); fig_w.update_yaxes(**_AX)
        fig_w.update_annotations(font_size=8.5,font_color='#475569',font_family='DM Mono')
        st.plotly_chart(fig_w,use_container_width=True)
        st.markdown('<div class="cn">Cruise and loiter consume the most fuel. The steep fuel-burn segments validate the Breguet fractions.</div></div>', unsafe_allow_html=True)

    with w2:
        st.markdown('<div class="card"><div class="ct">W_TO Composition</div>', unsafe_allow_html=True)
        fig_p=go.Figure(go.Pie(
            labels=['Empty','Usable Fuel','Trapped Fuel','Crew','Payload'],
            values=[WE,RR['WFu'],Wtfo_r,Wcrew,Wpl],hole=0.54,
            marker=dict(colors=['#0EA5E9','#38BDF8','#7DD3FC','#10B981','#34D399'],
                        line=dict(color='#fff',width=2)),
            textfont=dict(size=9,family='DM Mono'),textinfo='label+percent',rotation=90))
        fig_p.update_layout(paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='DM Mono',color='#475569'),showlegend=False,
            height=260,margin=dict(t=8,b=8,l=8,r=8),
            annotations=[dict(text=f'<b>{Wto:,.0f}</b><br>lbs',x=0.5,y=0.5,
                showarrow=False,font=dict(size=12,color='#0D1B2A',family='DM Mono'))])
        st.plotly_chart(fig_p,use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card"><div class="ct">Key Design Ratios</div>', unsafe_allow_html=True)
        st.dataframe(pd.DataFrame({
            'Ratio':['W_PL / W_TO','W_F / W_TO','W_E / W_TO','W_OE / W_TO','W_PL / W_E'],
            'Value':[f"{Wpl/Wto:.4f}",f"{WF/Wto:.4f}",f"{WE/Wto:.4f}",f"{WOE/Wto:.4f}",f"{Wpl/WE:.4f}"],
            'Typical':['0.10–0.25','0.20–0.45','0.45–0.65','0.50–0.70','0.15–0.40'],
        }),hide_index=True,use_container_width=True)
        st.markdown('<div class="cn">W_PL/W_E > 0.25 = commercially viable. W_PL/W_TO > 0.15 = efficient design.</div></div>', unsafe_allow_html=True)

        st.markdown('<div class="card"><div class="ct">W_TO vs Passengers</div>', unsafe_allow_html=True)
        pxa=np.arange(5,int(npax)+28,2); wxr=[]
        for n_ in pxa:
            try:
                w,r=solve({**P,'npax':int(n_)})
                wxr.append(w if abs(r['diff'])<50 else float('nan'))
            except: wxr.append(float('nan'))
        fig_px=go.Figure()
        fig_px.add_trace(go.Scatter(x=pxa,y=wxr,mode='lines',
            line=dict(color='#10B981',width=2),fill='tozeroy',fillcolor='rgba(16,185,129,0.06)'))
        fig_px.add_vline(x=int(npax),line_dash='dot',line_color='#F59E0B',line_width=1.2,
            annotation_text=f'{int(npax)} pax',annotation_font_color='#B45309',annotation_font_size=8)
        pf(fig_px,h=185,xt='Passengers',yt='W_TO (lbs)')
        st.plotly_chart(fig_px,use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════
# TAB 4 — EXPORT
# ════════════════════════════════════════════
with tab4:
    e1,e2 = st.columns([1,1],gap="medium")
    with e1:
        st.markdown('<div class="card"><div class="ct">Download Data — CSV</div>', unsafe_allow_html=True)
        rows={'Parameter':['W_TO','Mff','W_F_total','W_F_usable','W_payload','W_empty','W_OE',
                            'W_crew','W_tfo','WE_allow','delta_WE',
                            'dWTO_dCp_R','dWTO_dnp_R','dWTO_dLD_R','dWTO_dR',
                            'dWTO_dCp_E','dWTO_dnp_E','dWTO_dLD_E'],
              'Value':[Wto,RR['Mff'],WF,RR['WFu'],Wpl,WE,WOE,Wcrew,Wtfo_r,
                       RR['WEa'],RR['diff'],
                       S['dCpR'],S['dnpR'],S['dLDR'],S['dR'],
                       S['dCpE'],S['dnpE'],S['dLDE']],
              'Units':['lbs','','lbs','lbs','lbs','lbs','lbs','lbs','lbs','lbs','lbs',
                       'lbs/(lbs/hp/hr)','lbs','lbs','lbs/nm',
                       'lbs/(lbs/hp/hr)','lbs','lbs']}
        b=io.StringIO(); pd.DataFrame(rows).to_csv(b,index=False)
        st.download_button("⬇  Full Results (CSV)",b.getvalue(),"aerosizer_results.csv","text/csv",use_container_width=True)
        b2=io.StringIO()
        pd.DataFrame({'Phase':list(RR['fracs'].keys()),
                       'Wi/Wi-1':list(RR['fracs'].values()),
                       'Ref':['T2.1','T2.1','T2.1','Fig2.2','Eq2.9','Eq2.11','T2.1','T2.1']
                       }).to_csv(b2,index=False)
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button("⬇  Phase Fractions (CSV)",b2.getvalue(),"aerosizer_fractions.csv","text/csv",use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card"><div class="ct">Active Configuration</div>', unsafe_allow_html=True)
        st.dataframe(pd.DataFrame({'Parameter':list(P.keys()),'Value':[str(v) for v in P.values()]}),
            hide_index=True,use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with e2:
        st.markdown('<div class="card"><div class="ct">Generate PDF Report — A4 Engineering Format</div>', unsafe_allow_html=True)
        st.markdown("""<div style="font-size:0.8rem;color:#374151;line-height:1.75">
Report sections:<br>
&nbsp; ① Title block & document control<br>
&nbsp; ② Methodology overview<br>
&nbsp; ③ All mission inputs<br>
&nbsp; ④ Sizing result & convergence<br>
&nbsp; ⑤ Complete weight statement<br>
&nbsp; ⑥ Phase weight fractions<br>
&nbsp; ⑦ Key design ratios<br>
&nbsp; ⑧ Sensitivity partials<br>
&nbsp; ⑨ References
</div><br>""", unsafe_allow_html=True)

        def make_pdf():
            buf = io.BytesIO()
            doc = SimpleDocTemplate(buf, pagesize=A4,
                leftMargin=2.0*cm, rightMargin=2.0*cm,
                topMargin=2.2*cm, bottomMargin=2.2*cm)
            PW = 17.0*cm

            sty = getSampleStyleSheet()
            def ps(nm, **kw):
                return ParagraphStyle(nm, parent=sty['Normal'], **kw)

            # ── Colour palette ──
            C_NAVY   = colors.HexColor('#0D1B2A')
            C_BLUE   = colors.HexColor('#0369A1')
            C_SKY    = colors.HexColor('#0EA5E9')
            C_GRAY   = colors.HexColor('#475569')
            C_LGRAY  = colors.HexColor('#94A3B8')
            C_RULE   = colors.HexColor('#CBD5E1')
            C_FAINT  = colors.HexColor('#F8FAFC')
            C_STRIPE = colors.HexColor('#EFF8FF')
            C_GREEN  = colors.HexColor('#15803D' if conv else '#C2410C')
            C_WHITE  = colors.white

            # ── Typography ──
            sTITLE = ps('TI', fontSize=20, fontName='Helvetica-Bold',
                        textColor=C_NAVY, leading=26, spaceBefore=0, spaceAfter=4, alignment=TA_LEFT)
            sDOCNUM= ps('DN', fontSize=7.5, fontName='Helvetica',
                        textColor=C_LGRAY, leading=11, spaceAfter=0, alignment=TA_RIGHT)
            sSUB   = ps('SU', fontSize=8.5, textColor=C_GRAY, leading=13, spaceAfter=2)
            sH1    = ps('H1', fontSize=10, fontName='Helvetica-Bold',
                        textColor=C_BLUE, spaceBefore=12, spaceAfter=4)
            sH2    = ps('H2', fontSize=8.5, fontName='Helvetica-Bold',
                        textColor=C_NAVY, spaceBefore=7, spaceAfter=3)
            sBODY  = ps('BO', fontSize=8.0, textColor=C_GRAY, leading=12.5)
            sMONO  = ps('MO', fontSize=7.5, fontName='Helvetica',
                        textColor=C_BLUE, leading=11)
            sSTATUS= ps('ST', fontSize=8.5, fontName='Helvetica-Bold',
                        textColor=C_GREEN, spaceAfter=4)
            sREF   = ps('RF', fontSize=7.5, textColor=C_GRAY, leading=11.5)
            sCAP   = ps('CA', fontSize=7.0, textColor=C_LGRAY, leading=10,
                        spaceBefore=2, spaceAfter=6, alignment=TA_LEFT)

            # ── Engineering table style ──
            def make_ts(hdr_bg=C_NAVY, alt=True):
                ts = TableStyle([
                    # Header
                    ('BACKGROUND',   (0,0), (-1,0), hdr_bg),
                    ('TEXTCOLOR',    (0,0), (-1,0), C_WHITE),
                    ('FONTNAME',     (0,0), (-1,0), 'Helvetica-Bold'),
                    ('FONTSIZE',     (0,0), (-1,-1), 7.5),
                    ('LEADING',      (0,0), (-1,-1), 11),
                    # Data rows
                    ('FONTNAME',     (0,1), (-1,-1), 'Helvetica'),
                    ('TEXTCOLOR',    (0,1), (-1,-1), C_GRAY),
                    # Grid — thin hairlines
                    ('GRID',         (0,0), (-1,-1), 0.25, C_RULE),
                    ('LINEBELOW',    (0,0), (-1,0),  0.8,  C_SKY),
                    # Padding
                    ('LEFTPADDING',  (0,0), (-1,-1), 5),
                    ('RIGHTPADDING', (0,0), (-1,-1), 5),
                    ('TOPPADDING',   (0,0), (-1,-1), 3.5),
                    ('BOTTOMPADDING',(0,0), (-1,-1), 3.5),
                    ('VALIGN',       (0,0), (-1,-1), 'MIDDLE'),
                ])
                if alt:
                    ts.add('ROWBACKGROUNDS', (0,1), (-1,-1), [C_WHITE, C_FAINT])
                return ts

            # ── helper: thin horizontal rule ──
            def rule(w=PW, t=0.5, c=C_RULE):
                return HRFlowable(width=w, thickness=t, color=c, spaceAfter=4, spaceBefore=4)

            story = []

            # ════════════════════════════════════════
            # TITLE BLOCK — engineering drawing style
            # ════════════════════════════════════════
            title_data = [
                [
                    Paragraph("<b>AEROSIZER PRO</b>", ps('TX',
                        fontSize=18, fontName='Helvetica-Bold',
                        textColor=C_NAVY, leading=22)),
                    Paragraph(
                        "DOCUMENT NO: ASP-001<br/>"
                        "REVISION: A<br/>"
                        "CLASS: Conceptual Design<br/>"
                        "STATUS: " + ("RELEASED" if conv else "PRELIMINARY"),
                        ps('TX2', fontSize=7.5, textColor=C_LGRAY,
                           leading=11, alignment=TA_RIGHT))
                ],
            ]
            title_tbl = Table(title_data, colWidths=[PW*0.62, PW*0.38])
            title_tbl.setStyle(TableStyle([
                ('VALIGN',         (0,0), (-1,-1), 'MIDDLE'),
                ('LEFTPADDING',    (0,0), (-1,-1), 0),
                ('RIGHTPADDING',   (0,0), (-1,-1), 0),
                ('TOPPADDING',     (0,0), (-1,-1), 0),
                ('BOTTOMPADDING',  (0,0), (-1,-1), 0),
            ]))
            story.append(title_tbl)
            story.append(HRFlowable(width=PW, thickness=2.5, color=C_SKY,
                                    spaceAfter=3, spaceBefore=5))

            # Sub-header row
            sub_data = [[
                Paragraph("Preliminary Aircraft Weight Estimation — Propeller-Driven Transport", sSUB),
                Paragraph("Breguet Range / Endurance Method  ·  Raymer 2018 Ch.2", sSUB),
            ]]
            sub_tbl = Table(sub_data, colWidths=[PW*0.60, PW*0.40])
            sub_tbl.setStyle(TableStyle([
                ('VALIGN',(0,0),(-1,-1),'TOP'),
                ('LEFTPADDING',(0,0),(-1,-1),0),
                ('RIGHTPADDING',(0,0),(-1,-1),0),
                ('TOPPADDING',(0,0),(-1,-1),1),
                ('BOTTOMPADDING',(0,0),(-1,-1),1),
                ('ALIGN',(1,0),(1,-1),'RIGHT'),
            ]))
            story.append(sub_tbl)
            story.append(HRFlowable(width=PW, thickness=0.4, color=C_RULE,
                                    spaceAfter=10, spaceBefore=3))

            # ════════════════════════════════
            # SECTION 1 — Methodology
            # ════════════════════════════════
            story.append(Paragraph("1   Methodology", sH1))
            story.append(rule())
            story.append(Paragraph(
                "The iterative Breguet weight-fraction method (Raymer 2018, §2.3) determines the "
                "gross takeoff weight W_TO for a propeller-driven aircraft. "
                "W_TO is solved by bisection until the tentative empty weight W_E equals the "
                "regression allowable W_E = 10^{(log₁₀W_TO − A) / B}. "
                "The mission fuel fraction Mff is the product of all phase fractions W_i/W_{i-1}. "
                "Variable phases (cruise, loiter) are evaluated with the Breguet propeller equations; "
                "fixed phases use Raymer Table 2.1 constants.",
                sBODY))
            story.append(Spacer(1, 0.15*cm))

            # Equation box
            eq_data = [
                ["Cruise (Eq. 2.9)",  "W₅/W₄ = 1 / exp[ R·Cp / (375·η_p·L/D) ]"],
                ["Loiter (Eq. 2.11)", "W₆/W₅ = 1 / exp[ E·Cp / (375·(1/V)·η_p·L/D) ]"],
                ["Regression",        "log₁₀(W_E) = A + B · log₁₀(W_TO)             (Raymer T2.2)"],
            ]
            eq_tbl = Table(eq_data, colWidths=[PW*0.24, PW*0.76])
            eq_tbl.setStyle(TableStyle([
                ('BACKGROUND',   (0,0), (-1,-1), C_STRIPE),
                ('BACKGROUND',   (0,0), (0,-1),  colors.HexColor('#DBEAFE')),
                ('FONTNAME',     (0,0), (0,-1),  'Helvetica-Bold'),
                ('FONTNAME',     (1,0), (1,-1),  'Helvetica'),
                ('FONTSIZE',     (0,0), (-1,-1), 7.5),
                ('TEXTCOLOR',    (0,0), (0,-1),  C_BLUE),
                ('TEXTCOLOR',    (1,0), (1,-1),  C_NAVY),
                ('GRID',         (0,0), (-1,-1), 0.25, C_RULE),
                ('LEFTPADDING',  (0,0), (-1,-1), 6),
                ('RIGHTPADDING', (0,0), (-1,-1), 6),
                ('TOPPADDING',   (0,0), (-1,-1), 3),
                ('BOTTOMPADDING',(0,0), (-1,-1), 3),
                ('LINEAFTER',    (0,0), (0,-1),  1.0, C_SKY),
            ]))
            story.append(eq_tbl)
            story.append(sCAP.__class__('EQ-CAP',parent=sty['Normal'],
                fontSize=7.0, textColor=C_LGRAY, leading=10,
                spaceBefore=2, spaceAfter=8))
            story.append(Paragraph(
                "R in statute miles; Cp in lbs/hp/hr; η_p = propeller efficiency; "
                "E in hours; V in mph; R = range in statute miles.",
                sCAP))

            # ════════════════════════════════
            # SECTION 2 — Inputs
            # ════════════════════════════════
            story.append(Paragraph("2   Mission Inputs", sH1))
            story.append(rule())
            CW4 = [PW*0.30, PW*0.17, PW*0.30, PW*0.17]
            t1 = Table([
                ['Parameter',          'Value',         'Parameter',          'Value'],
                ['Passengers',          str(int(npax)),  'Design range (nm)',   str(int(R_nm))],
                ['Pax body wt (lbs)',   str(int(wpax)),  'Loiter endur. (hr)',  f'{float(El):.2f}'],
                ['Baggage wt (lbs)',    str(int(wbag)),  'Loiter speed (kts)',  str(int(Vl))],
                ['Flight crew',         str(int(ncrew)), 'Cruise L/D',          f'{float(LDc):.1f}'],
                ['Cabin attendants',    str(int(natt)),  'Loiter L/D',          f'{float(LDl):.1f}'],
                ['Reg. constant A',     f'{float(A_v):.4f}', 'Cruise SFC Cp',   f'{float(Cpc):.2f}'],
                ['Reg. constant B',     f'{float(B_v):.4f}', 'Loiter SFC Cp',   f'{float(Cpl):.2f}'],
                ['Trapped fuel M_tfo',  f'{float(Mtfo):.3f}','Cruise η_p',      f'{float(npc):.2f}'],
                ['Reserve ratio M_r',   '0.000',         'Loiter η_p',          f'{float(npl):.2f}'],
            ], colWidths=CW4)
            t1.setStyle(make_ts(hdr_bg=C_NAVY))
            story.append(t1)
            story.append(Spacer(1, 0.2*cm))

            # ════════════════════════════════
            # SECTION 3 — Result
            # ════════════════════════════════
            story.append(Paragraph("3   Sizing Result & Convergence", sH1))
            story.append(rule())

            # Result summary box
            res_data = [
                ['W_TO (lbs)', 'Mff', 'ΔW_E (lbs)', 'Convergence'],
                [f'{Wto:,.0f}', f'{RR["Mff"]:.5f}', f'{RR["diff"]:+.1f}',
                 'CONVERGED ✓' if conv else 'NOT CONVERGED ✗'],
            ]
            res_tbl = Table(res_data, colWidths=[PW*0.26]*4)
            res_tbl.setStyle(TableStyle([
                ('BACKGROUND',   (0,0), (-1,0), C_NAVY),
                ('TEXTCOLOR',    (0,0), (-1,0), C_WHITE),
                ('FONTNAME',     (0,0), (-1,0), 'Helvetica-Bold'),
                ('FONTNAME',     (0,1), (-1,1), 'Helvetica-Bold'),
                ('FONTSIZE',     (0,0), (-1,-1), 8),
                ('TEXTCOLOR',    (0,1), (2,1),  C_BLUE),
                ('TEXTCOLOR',    (3,1), (3,1),  C_GREEN),
                ('BACKGROUND',   (0,1), (-1,1), C_STRIPE),
                ('GRID',         (0,0), (-1,-1), 0.4, C_RULE),
                ('LINEBELOW',    (0,0), (-1,0),  1.0, C_SKY),
                ('ALIGN',        (0,0), (-1,-1), 'CENTER'),
                ('VALIGN',       (0,0), (-1,-1), 'MIDDLE'),
                ('TOPPADDING',   (0,0), (-1,-1), 5),
                ('BOTTOMPADDING',(0,0), (-1,-1), 5),
            ]))
            story.append(res_tbl)
            story.append(Spacer(1, 0.2*cm))

            # ════════════════════════════════
            # SECTION 4 — Weight Statement
            # ════════════════════════════════
            story.append(Paragraph("4   Complete Weight Statement", sH1))
            story.append(rule())
            CWS = [PW*0.42, PW*0.17, PW*0.20, PW*0.17]
            ws_rows = [['Component', 'lbs', 'Fraction W/W_TO', '% W_TO']]
            for comp, lbs_val, frac_val, pct_val in zip(
                    summary['Component'], summary['lbs'],
                    summary['Fraction'],  summary['% W_TO']):
                ws_rows.append([comp, lbs_val, frac_val, pct_val])
            t2 = Table(ws_rows, colWidths=CWS)
            t2.setStyle(make_ts())
            # Highlight W_TO row
            t2.setStyle(TableStyle([
                ('FONTNAME',  (0,1),(-1,1),'Helvetica-Bold'),
                ('TEXTCOLOR', (0,1),(-1,1), C_NAVY),
                ('BACKGROUND',(0,1),(-1,1), colors.HexColor('#DBEAFE')),
            ]))
            story.append(t2)
            story.append(Spacer(1, 0.2*cm))

            # ════════════════════════════════
            # SECTION 5 — Phase Fractions
            # ════════════════════════════════
            story.append(Paragraph("5   Phase Weight Fractions", sH1))
            story.append(rule())
            CPF = [PW*0.28, PW*0.17, PW*0.20, PW*0.17, PW*0.18]

            # Cumulative Mff product column
            cum_mff = [1.0]
            for v in RR['fracs'].values():
                cum_mff.append(round(cum_mff[-1]*v, 6))

            t3 = Table(
                [['Phase', 'Wᵢ / Wᵢ₋₁', 'Cumul. Mff', 'Type', 'Reference']] +
                list(zip(
                    list(RR['fracs'].keys()),
                    [f"{v:.5f}" for v in RR['fracs'].values()],
                    [f"{c:.5f}" for c in cum_mff[1:]],
                    ['Fixed','Fixed','Fixed','Fixed','Variable','Variable','Fixed','Fixed'],
                    ['Raymer T2.1','Raymer T2.1','Raymer T2.1','Raymer Fig2.2',
                     'Breguet Eq 2.9','Breguet Eq 2.11','Raymer T2.1','Raymer T2.1']
                )),
                colWidths=CPF)
            t3.setStyle(make_ts())
            # Highlight Breguet rows
            t3.setStyle(TableStyle([
                ('BACKGROUND', (0,6),(- 1,6), colors.HexColor('#F0FDF4')),
                ('BACKGROUND', (0,7),(-1,7),  colors.HexColor('#F0FDF4')),
                ('TEXTCOLOR',  (3,6),(3,6),   colors.HexColor('#15803D')),
                ('TEXTCOLOR',  (3,7),(3,7),   colors.HexColor('#15803D')),
                ('FONTNAME',   (0,6),(-1,6),  'Helvetica-Bold'),
                ('FONTNAME',   (0,7),(-1,7),  'Helvetica-Bold'),
            ]))
            story.append(t3)
            story.append(Paragraph(
                f"Final mission fuel fraction: Mff = {RR['Mff']:.6f}  "
                f"(product of all 8 phase fractions above)",
                sCAP))
            story.append(Spacer(1, 0.15*cm))

            # ════════════════════════════════
            # SECTION 6 — Design Ratios
            # ════════════════════════════════
            story.append(Paragraph("6   Key Design Ratios", sH1))
            story.append(rule())

            ratio_rows = [
                ['Ratio', 'Value', 'Typical Range', 'Assessment'],
            ]
            ratio_def = [
                ('W_PL / W_TO', Wpl/Wto, '0.10 – 0.25'),
                ('W_F  / W_TO', WF/Wto,  '0.20 – 0.45'),
                ('W_E  / W_TO', WE/Wto,  '0.45 – 0.65'),
                ('W_OE / W_TO', WOE/Wto, '0.50 – 0.70'),
                ('W_PL / W_E',  Wpl/WE,  '0.15 – 0.40'),
            ]
            for name, val, typ in ratio_def:
                lo_t, hi_t = [float(x) for x in typ.replace(' ','').split('–')]
                ok = lo_t <= val <= hi_t
                assess = '✓ In range' if ok else ('▲ Above' if val > hi_t else '▼ Below')
                ratio_rows.append([name, f'{val:.4f}', typ, assess])

            CWR = [PW*0.26, PW*0.16, PW*0.25, PW*0.22]
            t_r = Table(ratio_rows, colWidths=CWR)
            t_r.setStyle(make_ts())
            story.append(t_r)
            story.append(Spacer(1, 0.2*cm))

            # ════════════════════════════════
            # SECTION 7 — Sensitivity
            # ════════════════════════════════
            story.append(Paragraph("7   Sensitivity Analysis — Breguet Partial Derivatives", sH1))
            story.append(rule())
            story.append(Paragraph(
                "Each partial derivative ∂W_TO/∂y quantifies the change in gross takeoff weight "
                "per unit change in parameter y, with all other parameters held constant. "
                "Negative values indicate design levers that reduce W_TO.",
                sBODY))
            story.append(Spacer(1, 0.1*cm))

            all_p = (
                list(zip(sdr['Partial'], sdr['Value'], sdr['Units'], sdr['Eq.'])) +
                list(zip(sdl['Partial'], sdl['Value'], sdl['Units'], sdl['Eq.']))
            )
            CWP = [PW*0.36, PW*0.16, PW*0.32, PW*0.12]
            t4 = Table([['Partial Derivative', 'Value', 'Units', 'Ref.']] + all_p,
                       colWidths=CWP)
            t4.setStyle(make_ts())
            # Colour negative values green (good)
            for row_idx, row in enumerate(all_p, start=1):
                try:
                    val = float(row[1].replace(',','').replace('+',''))
                    if val < 0:
                        t4.setStyle(TableStyle([
                            ('TEXTCOLOR', (1, row_idx), (1, row_idx),
                             colors.HexColor('#15803D')),
                        ]))
                except: pass
            story.append(t4)
            story.append(Spacer(1, 0.2*cm))

            # ════════════════════════════════
            # SECTION 8 — References
            # ════════════════════════════════
            story.append(Paragraph("8   References", sH1))
            story.append(rule())
            CWF = [PW*0.08, PW*0.92]
            refs = [
                ['[1]', 'Raymer, D.P. (2018). Aircraft Design: A Conceptual Approach, 6th Ed. AIAA Education Series. — Primary reference for all equations, weight fractions, and regression constants.'],
                ['[2]', 'Roskam, J. (2003). Airplane Design, Part I: Preliminary Sizing. DAR Corporation. — Alternative regression constants and cross-validation methodology.'],
                ['[3]', 'Breguet, L. (1923). Calcul du Poids de Combustible Consommé par un Avion. Comptes Rendus, Paris. — Original derivation of range and endurance equations.'],
                ['[4]', 'Nicolai & Carichner (2010). Fundamentals of Aircraft and Airship Design. AIAA Education Series.'],
                ['[5]', 'MIL-HDBK-516C (2014). Airworthiness Certification Criteria. U.S. DoD. — Weight definitions consistent with FAA/EASA standards.'],
            ]
            t5 = Table([['Ref.', 'Citation']] + refs, colWidths=CWF)
            t5.setStyle(make_ts(hdr_bg=colors.HexColor('#334155')))
            story.append(t5)

            # Footer note
            story.append(Spacer(1, 0.3*cm))
            story.append(HRFlowable(width=PW, thickness=0.5, color=C_RULE))
            story.append(Paragraph(
                "DISCLAIMER: This report is generated by AeroSizer Pro for conceptual-level "
                "preliminary sizing only. Results are not certified for regulatory or structural "
                "analysis. All weights in lbs (avoirdupois). Raymer 2018 Eq. 2.9 applies to "
                "propeller-driven aircraft only.",
                ps('DIS', fontSize=6.5, textColor=C_LGRAY, leading=9.5, spaceBefore=3)))

            doc.build(story)
            buf.seek(0)
            return buf.read()

        st.download_button("⬇  Generate & Download PDF (A4)", make_pdf(),
            "aerosizer_report.pdf", "application/pdf", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════
# TAB 5 — REFERENCES
# ════════════════════════════════════════════
with tab5:
    st.markdown('<div style="font-family:DM Mono,monospace;font-size:0.95rem;font-weight:600;color:#0D1B2A;margin-bottom:1rem">Equations & Methods</div>', unsafe_allow_html=True)
    eq1,eq2 = st.columns(2,gap="medium")
    with eq1:
        for code,title,eq,desc in [
            ("Eq. 2.9","Cruise Weight Fraction — Breguet Propeller Range",
             "W5/W4 = 1 / exp[ R·Cp / (375·η_p·L/D) ]",
             "R in statute miles, Cp in lbs/hp/hr, η_p = prop. efficiency. "
             "Source: Raymer (2018) Eq. 2.9"),
            ("Eq. 2.11","Loiter Weight Fraction — Breguet Propeller Endurance",
             "W6/W5 = 1 / exp[ E·Cp / (375·(1/V)·η_p·L/D) ]",
             "E in hours, V in mph. Reserve fuel segment. Source: Raymer (2018) Eq. 2.11"),
            ("Eq. 2.45","W_TO Sensitivity to Range",
             "∂W_TO/∂R = F · Cp / (375·η_p·L/D)",
             "F = sizing multiplier (Eq. 2.44). Source: Raymer (2018) Eq. 2.45"),
        ]:
            st.markdown(f"""<div class="card">
            <div class="ct">{code} — {title}</div>
            <div style="font-family:DM Mono,monospace;font-size:0.78rem;color:#0369A1;
              background:#EFF8FF;padding:0.4rem 0.75rem;border-radius:6px;margin-bottom:0.45rem">{eq}</div>
            <div class="cn" style="margin-top:0">{desc}</div>
            </div>""", unsafe_allow_html=True)

    with eq2:
        for code,title,eq,desc in [
            ("Eq. 2.49","∂W_TO / ∂Cp  (cruise)",
             "∂W_TO/∂Cp = F·R / (375·η_p·L/D)",
             "Positive: higher SFC increases W_TO. Source: Raymer (2018) Table 2.20"),
            ("Eq. 2.50","∂W_TO / ∂η_p  (cruise)",
             "∂W_TO/∂η_p = −F·R·Cp / (375·η_p²·L/D)",
             "Negative: better propeller efficiency reduces W_TO. Source: Raymer (2018) Table 2.20"),
            ("Eq. 2.51","∂W_TO / ∂(L/D)  (cruise)",
             "∂W_TO/∂(L/D) = −F·R·Cp / (375·η_p·(L/D)²)",
             "Usually the largest driver. Higher L/D strongly reduces W_TO. Source: Raymer (2018) Table 2.20"),
        ]:
            st.markdown(f"""<div class="card">
            <div class="ct">{code} — {title}</div>
            <div style="font-family:DM Mono,monospace;font-size:0.78rem;color:#0369A1;
              background:#EFF8FF;padding:0.4rem 0.75rem;border-radius:6px;margin-bottom:0.45rem">{eq}</div>
            <div class="cn" style="margin-top:0">{desc}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<div style="font-family:DM Mono,monospace;font-size:0.95rem;font-weight:600;color:#0D1B2A;margin:1.2rem 0 0.8rem">Bibliography</div>', unsafe_allow_html=True)
    for num,title,detail in [
        ("[1]","Raymer, D.P. — Aircraft Design: A Conceptual Approach, 6th Ed. (2018)",
         "AIAA Education Series. Primary reference for all equations, weight fractions, and regression constants. Chapter 2: Sizing from a Conceptual Sketch."),
        ("[2]","Roskam, J. — Airplane Design, Part I: Preliminary Sizing (2003)",
         "DAR Corporation. Alternative regression constants and mission analysis methodology. Used for cross-validation."),
        ("[3]","Breguet, L. — Calcul du Poids de Combustible Consommé par un Avion (1923)",
         "Comptes Rendus de l'Académie des Sciences. Original derivation of range and endurance equations."),
        ("[4]","Nicolai & Carichner — Fundamentals of Aircraft and Airship Design (2010)",
         "AIAA Education Series. Additional preliminary sizing methods for transport aircraft."),
        ("[5]","MIL-HDBK-516C — Airworthiness Certification Criteria (2014)",
         "U.S. Department of Defense. Weight definitions (W_TO, W_OE) consistent with FAA/EASA standards."),
    ]:
        st.markdown(f"""<div class="card" style="padding:0.75rem 1rem;margin-bottom:0.55rem">
        <div style="display:flex;gap:0.75rem;align-items:flex-start">
          <span style="font-family:DM Mono,monospace;font-size:0.7rem;font-weight:500;color:#0369A1;
            flex-shrink:0;background:#EFF8FF;padding:0.15rem 0.5rem;border-radius:4px">{num}</span>
          <div>
            <div style="font-size:0.82rem;font-weight:600;color:#0D1B2A;margin-bottom:0.18rem">{title}</div>
            <div style="font-size:0.74rem;color:#64748B;line-height:1.55">{detail}</div>
          </div>
        </div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div style="font-family:DM Mono,monospace;font-size:0.95rem;font-weight:600;color:#0D1B2A;margin:1.2rem 0 0.8rem">Assumptions & Limitations</div>', unsafe_allow_html=True)
    for t,d in [
        ("Propeller-driven only","Breguet Eq. 2.9 / 2.11 in this form apply to propeller aircraft. Jet aircraft require TSFC-based equations."),
        ("Historical regression","A and B are statistical fits to historical data. Most accurate for turboprop transports in the 10,000–150,000 lbs class."),
        ("Conceptual level only","No structural sizing, drag polar computation, or propulsion matching is performed."),
        ("Fixed phase fractions","Engine start, taxi, takeoff, climb, descent, landing use Raymer Table 2.1 fixed values."),
        ("Reserve policy","Loiter segment represents FAR/ICAO reserve. No alternate divert distance is modeled."),
    ]:
        st.markdown(f"""<div style="margin-bottom:0.6rem;padding:0.6rem 1rem;background:#fff;
          border:1px solid #E2E8F0;border-radius:10px;border-left:3px solid #0EA5E9">
          <div style="font-size:0.78rem;font-weight:600;color:#0369A1;margin-bottom:0.15rem">▸ {t}</div>
          <div style="font-size:0.75rem;color:#475569;line-height:1.55">{d}</div>
        </div>""", unsafe_allow_html=True)
