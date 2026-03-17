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
.top-bar{display:flex;align-items:center;gap:12px;padding:1.2rem 0 .6rem 0;border-bottom:1px solid #1E2535;margin-bottom:1.4rem}
.logo{font-family:'JetBrains Mono',monospace;font-size:1.5rem;font-weight:600;color:#fff;letter-spacing:.04em}
.logo em{color:#818CF8;font-style:normal}
.tag{font-size:.7rem;color:#64748B;letter-spacing:.18em;margin-top:.1rem}
.ok{background:#0F2318;border:1px solid #16A34A40;border-radius:10px;
  padding:.55rem 1.1rem;font-family:'JetBrains Mono',monospace;font-size:.8rem;color:#4ADE80;margin-bottom:1rem}
.warn{background:#1E1208;border:1px solid #EA580C40;border-radius:10px;
  padding:.55rem 1.1rem;font-family:'JetBrains Mono',monospace;font-size:.8rem;color:#FB923C;margin-bottom:1rem}
.kcard{background:#111827;border:1px solid #1E2535;border-radius:14px;
  padding:1.1rem 1.3rem;text-align:center}
.kcard:hover{border-color:#818CF840;transition:.2s}
.kv{font-family:'JetBrains Mono',monospace;font-size:1.55rem;font-weight:600;color:#818CF8;line-height:1.1}
.ku{font-size:.75rem;color:#94A3B8;margin-left:.2rem}
.kl{font-size:.62rem;color:#64748B;letter-spacing:.1em;margin-top:.35rem;text-transform:uppercase}
.card{background:#111827;border:1px solid #1E2535;border-radius:14px;padding:1.2rem 1.4rem;margin-bottom:1rem}
.card-title{font-family:'JetBrains Mono',monospace;font-size:.72rem;color:#818CF8;
  letter-spacing:.14em;text-transform:uppercase;margin-bottom:.9rem;
  padding-bottom:.4rem;border-bottom:1px solid #1E2535}
[data-testid="stSidebar"]{background:#080C15!important;border-right:1px solid #1E2535!important}
.stTabs [data-baseweb="tab-list"]{background:#111827;border-radius:10px;padding:3px;gap:2px}
.stTabs [data-baseweb="tab"]{border-radius:8px;font-size:.78rem;font-weight:500;
  color:#64748B;padding:.45rem 1.2rem}
.stTabs [aria-selected="true"]{background:#818CF8!important;color:#fff!important}
div.stDownloadButton>button{background:#181F2E!important;border:1px solid #818CF840!important;
  color:#818CF8!important;border-radius:10px!important;font-size:.8rem!important;
  font-weight:500!important;width:100%!important;padding:.6rem!important}
div.stDownloadButton>button:hover{background:#818CF820!important;border-color:#818CF8!important}
</style>
""", unsafe_allow_html=True)

# ── Plotly base (ZERO xaxis/yaxis in update_layout) ──────────────────────────
_B = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='#0F1623',
    font=dict(family='JetBrains Mono', color='#94A3B8', size=10),
    margin=dict(l=50, r=16, t=36, b=40),
    hoverlabel=dict(bgcolor='#1E2535', font_size=11),
)
_AX = dict(gridcolor='#1E2535', linecolor='#1E2535', zerolinecolor='#1E2535')

def pfig(fig, title='', h=300, xt='', yt='', yr=None):
    kw = dict(_B)
    if title: kw['title'] = dict(text=title, font=dict(color='#C7D2FE', size=11,
                                  family='JetBrains Mono'), x=0.01, pad=dict(l=4))
    kw['height'] = h
    fig.update_layout(**kw)
    fig.update_xaxes(**_AX)
    fig.update_yaxes(**_AX)
    if xt: fig.update_xaxes(title_text=xt, title_font=dict(size=9, color='#64748B'))
    if yt: fig.update_yaxes(title_text=yt, title_font=dict(size=9, color='#64748B'))
    if yr: fig.update_yaxes(range=yr)
    return fig

# ── Physics ───────────────────────────────────────────────────────────────────
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
    WFu  = p['Wto']*(1-Mff)
    WF   = WFu + p['Wto']*p['Mr']*(1-Mff) + Wtfo
    WOE  = p['Wto'] - WF - Wpl
    WE   = WOE - Wtfo - Wcrew
    WEa  = 10**((math.log10(p['Wto'])-p['A'])/p['B'])
    return dict(Wpl=Wpl,Wcrew=Wcrew,Wtfo=Wtfo,Mff=Mff,WF=WF,WFu=WFu,
                WOE=WOE,WE=WE,WEa=WEa,diff=WEa-WE,
                fracs=dict(zip(fnames,fvals)))

def solve(p, tol=0.5, n=300):
    pp=dict(p)
    # good initial bracket: estimate Wto from payload fraction
    # start bisection with confirmed opposite signs
    pp['Wto']=10000; r_lo=mission(pp)
    pp['Wto']=500000; r_hi=mission(pp)
    if r_lo['diff']*r_hi['diff']>0:
        # fallback sweep
        for w0 in [20000,40000,60000,80000,100000,150000,200000]:
            pp['Wto']=w0; r0=mission(pp)
            if r0['diff']*r_hi['diff']<0:
                r_lo=r0; break
    lo,hi=pp['Wto'] if r_lo['diff']<0 else 10000, 500000
    r={}
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

# ── Sidebar ───────────────────────────────────────────────────────────────────
D = dict(npax=34,wpax=175,wbag=30,ncrew=2,natt=1,Mtfo=0.005,Mr=0.0,
         R=1100,Vl=250,LDc=13,Cpc=0.60,npc=0.85,
         El=0.75,LDl=16,Cpl=0.65,npl=0.77,A=0.3774,B=0.9647)

with st.sidebar:
    st.markdown('<div class="logo">AERO<em>WEIGHT</em> PRO</div>', unsafe_allow_html=True)
    st.markdown('<div class="tag">PRELIMINARY SIZING TOOL</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("**Payload**")
    npax  = st.slider("Passengers",       10,100,D['npax'])
    wpax  = st.slider("Pax weight (lbs)",140,220,D['wpax'])
    wbag  = st.slider("Baggage (lbs)",    10, 60,D['wbag'])
    ncrew = st.slider("Pilots",            1,  4,D['ncrew'])
    natt  = st.slider("Attendants",        0,  4,D['natt'])

    st.markdown("---")
    st.markdown("**Cruise**")
    R_nm = st.slider("Range (nm)",      200,3000,D['R'],step=50)
    LDc  = st.slider("L/D",              8,  22,D['LDc'])
    Cpc  = st.slider("Cp (lbs/hp/hr)", 0.3, 1.0,D['Cpc'],step=0.01)
    npc  = st.slider("Prop efficiency", 0.5,0.95,D['npc'],step=0.01)

    st.markdown("---")
    st.markdown("**Loiter**")
    El   = st.slider("Endurance (hr)",  0.1, 3.0,D['El'],step=0.05)
    Vl   = st.slider("Speed (kts)",     100, 350,D['Vl'])
    LDl  = st.slider("L/D",              8,  24,D['LDl'])
    Cpl  = st.slider("Cp (lbs/hp/hr)", 0.3, 1.0,D['Cpl'],step=0.01)
    npl  = st.slider("Prop efficiency", 0.5,0.95,D['npl'],step=0.01)

    st.markdown("---")
    st.markdown("**Regression Constants**")
    A_v  = st.number_input("A",    value=D['A'],   step=0.001,format="%.4f")
    B_v  = st.number_input("B",    value=D['B'],   step=0.001,format="%.4f")
    Mtfo = st.number_input("M_tfo",value=D['Mtfo'],step=0.001,format="%.4f")

P = dict(npax=npax,wpax=wpax,wbag=wbag,ncrew=ncrew,natt=natt,
         Mtfo=Mtfo,Mr=0.0,R=R_nm,Vl=Vl,LDc=LDc,Cpc=Cpc,npc=npc,
         El=El,LDl=LDl,Cpl=Cpl,npl=npl,A=A_v,B=B_v,Wto=48550)

Wto, RR = solve(P)
S = sens(P, Wto)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="top-bar">
  <div>
    <div class="logo">AERO<em>WEIGHT</em> PRO</div>
    <div class="tag">BREGUET RANGE / ENDURANCE  ·  PROPELLER AIRCRAFT PRELIMINARY SIZING</div>
  </div>
</div>
""", unsafe_allow_html=True)

if abs(RR['diff']) < 5:
    st.markdown(f'<div class="ok">✓  Converged  —  W_TO = {Wto:,.0f} lbs  |  ΔWE = {RR["diff"]:.2f} lbs</div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div class="warn">⚠  Not converged  —  ΔWE = {RR["diff"]:.1f} lbs  (check inputs)</div>', unsafe_allow_html=True)

# KPI row
k1,k2,k3,k4,k5 = st.columns(5)
for col,val,unit,lbl in [
    (k1, f"{Wto:,.0f}",       "lbs", "Gross Weight W_TO"),
    (k2, f"{RR['Mff']:.4f}",  "",    "Fuel Fraction Mff"),
    (k3, f"{RR['WF']:,.0f}",  "lbs", "Total Fuel"),
    (k4, f"{RR['Wpl']:,.0f}", "lbs", "Payload"),
    (k5, f"{RR['WE']:,.0f}",  "lbs", "Empty Weight W_E"),
]:
    with col:
        st.markdown(f'<div class="kcard"><div class="kv">{val}<span class="ku">{unit}</span></div><div class="kl">{lbl}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
tab1, tab2, tab3, tab4 = st.tabs(["  Mission  ","  Sensitivity  ","  Weight Breakdown  ","  Export  "])

# ═══════════════════════════════════════════════════════════════════
# TAB 1
# ═══════════════════════════════════════════════════════════════════
with tab1:
    colA, colB = st.columns([3,2], gap="medium")

    with colA:
        # Bar chart
        st.markdown('<div class="card"><div class="card-title">Phase Weight Fractions</div>', unsafe_allow_html=True)
        phases = list(RR['fracs'].keys())
        fvals  = list(RR['fracs'].values())
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=phases, y=fvals,
            marker_color=['#818CF8','#818CF8','#818CF8','#818CF8',
                          '#34D399','#34D399','#818CF8','#818CF8'],
            text=[f'{v:.4f}' for v in fvals],
            textposition='outside',
            textfont=dict(size=9, color='#94A3B8'),
        ))
        pfig(fig, h=280, yr=[0.80, 1.02])
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Range sweep
        st.markdown('<div class="card"><div class="card-title">W_TO vs Range</div>', unsafe_allow_html=True)
        rr = np.linspace(200,3000,50); ww=[]
        for rv in rr:
            try: w,_=solve({**P,'R':float(rv)}); ww.append(w)
            except: ww.append(float('nan'))
        fig3=go.Figure()
        fig3.add_trace(go.Scatter(x=rr,y=ww,mode='lines',
            line=dict(color='#818CF8',width=2.5),
            fill='tozeroy',fillcolor='rgba(129,140,248,0.07)'))
        fig3.add_vline(x=R_nm,line_dash='dot',line_color='#34D399',line_width=1.5,
            annotation_text=f'Current: {R_nm} nm',annotation_font_color='#34D399',
            annotation_font_size=9)
        pfig(fig3, h=240, xt='Range (nm)', yt='W_TO (lbs)')
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with colB:
        # Gauge
        st.markdown('<div class="card"><div class="card-title">W_TO Gauge</div>', unsafe_allow_html=True)
        fig2=go.Figure(go.Indicator(
            mode="gauge+number",
            value=Wto,
            number={'suffix':' lbs','font':{'color':'#818CF8','size':16,'family':'JetBrains Mono'}},
            gauge={
                'axis':{'range':[0,120000],'tickfont':{'size':8},'tickcolor':'#1E2535'},
                'bar':{'color':'#818CF8','thickness':0.2},
                'bgcolor':'#0F1623','borderwidth':1,'bordercolor':'#1E2535',
                'steps':[
                    {'range':[0,     40000],'color':'#0F2318'},
                    {'range':[40000, 80000],'color':'#111827'},
                    {'range':[80000,120000],'color':'#1E1208'},
                ],
                'threshold':{'line':{'color':'#FB923C','width':2},'thickness':0.75,'value':Wto},
            },
            title={'text':'Gross Takeoff Weight','font':{'color':'#64748B','size':9,'family':'JetBrains Mono'}},
        ))
        fig2.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='JetBrains Mono',color='#94A3B8'),
            height=250,margin=dict(t=30,b=5,l=10,r=10))
        st.plotly_chart(fig2,use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Convergence
        st.markdown('<div class="card"><div class="card-title">Convergence Check</div>', unsafe_allow_html=True)
        st.dataframe(pd.DataFrame({
            'Item':['WE Tentative','WE Allowable','Difference'],
            'Value (lbs)':[f"{RR['WE']:,.1f}",f"{RR['WEa']:,.1f}",f"{RR['diff']:+.2f}"],
        }), hide_index=True, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Phase table
        st.markdown('<div class="card"><div class="card-title">Phase Fractions Table</div>', unsafe_allow_html=True)
        st.dataframe(pd.DataFrame({
            'Phase': list(RR['fracs'].keys()),
            'Wi / Wi-1': [f"{v:.4f}" for v in RR['fracs'].values()],
        }), hide_index=True, use_container_width=True)
        st.markdown(f'<br><b style="font-family:JetBrains Mono;color:#818CF8">Mff = {RR["Mff"]:.5f}</b>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# TAB 2
# ═══════════════════════════════════════════════════════════════════
with tab2:
    c1,c2 = st.columns(2, gap="medium")
    with c1:
        st.markdown('<div class="card"><div class="card-title">Range Phase Partials</div>', unsafe_allow_html=True)
        sdr={'Partial':['∂WTO/∂Cp','∂WTO/∂ηp','∂WTO/∂(L/D)','∂WTO/∂R'],
             'Value':[f"{S['dCpR']:+,.1f}",f"{S['dnpR']:+,.1f}",
                      f"{S['dLDR']:+,.1f}",f"{S['dR']:+,.2f}"],
             'Units':['lbs/(lbs/hp/hr)','lbs','lbs','lbs/nm']}
        st.dataframe(pd.DataFrame(sdr),hide_index=True,use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="card"><div class="card-title">Loiter Phase Partials</div>', unsafe_allow_html=True)
        sdl={'Partial':['∂WTO/∂Cp','∂WTO/∂ηp','∂WTO/∂(L/D)'],
             'Value':[f"{S['dCpE']:+,.1f}",f"{S['dnpE']:+,.1f}",f"{S['dLDE']:+,.1f}"],
             'Units':['lbs/(lbs/hp/hr)','lbs','lbs']}
        st.dataframe(pd.DataFrame(sdl),hide_index=True,use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card"><div class="card-title">Tornado Chart — Most Influential Parameters</div>', unsafe_allow_html=True)
    tlbl=['Cp (Range)','ηp (Range)','L/D (Range)','Range','Cp (Loiter)','ηp (Loiter)','L/D (Loiter)']
    tval=[S['dCpR'],S['dnpR'],S['dLDR'],S['dR']*R_nm*0.1,S['dCpE'],S['dnpE'],S['dLDE']]
    idx=sorted(range(7),key=lambda i:abs(tval[i]))
    tlbl=[tlbl[i] for i in idx]; tval=[tval[i] for i in idx]
    fig_t=go.Figure(go.Bar(
        x=tval,y=tlbl,orientation='h',
        marker_color=['#818CF8' if v>=0 else '#FB923C' for v in tval],
        text=[f'{v:+,.0f} lbs' for v in tval],
        textposition='outside',textfont=dict(size=9)))
    fig_t.add_vline(x=0,line_color='#1E2535',line_width=1.5)
    pfig(fig_t,h=340,xt='Change in W_TO (lbs)')
    st.plotly_chart(fig_t,use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card"><div class="card-title">3D Surface — W_TO over Cp and L/D (Cruise)</div>', unsafe_allow_html=True)
    cpa=np.linspace(0.40,0.90,20); lda=np.linspace(9.0,20.0,20)
    Z=np.zeros((len(cpa),len(lda)))
    for i,cp in enumerate(cpa):
        for j,ld in enumerate(lda):
            try: w,_=solve({**P,'Cpc':float(cp),'LDc':float(ld)}); Z[i,j]=w
            except: Z[i,j]=float('nan')
    fig4=go.Figure(go.Surface(
        x=lda,y=cpa,z=Z,
        colorscale=[[0,'#0B0F1A'],[0.4,'#1E2535'],[0.75,'#818CF8'],[1,'#34D399']],
        opacity=0.92,showscale=True,
        colorbar=dict(tickfont=dict(size=8,color='#64748B'),len=0.65,thickness=12)))
    fig4.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='JetBrains Mono',color='#94A3B8',size=9),
        title=dict(text='W_TO over Cp × L/D',font=dict(color='#C7D2FE',size=11,
                    family='JetBrains Mono'),x=0.01),
        scene=dict(
            xaxis=dict(title='L/D',backgroundcolor='#0F1623',
                       gridcolor='#1E2535',linecolor='#1E2535'),
            yaxis=dict(title='Cp', backgroundcolor='#0F1623',
                       gridcolor='#1E2535',linecolor='#1E2535'),
            zaxis=dict(title='W_TO (lbs)',backgroundcolor='#0F1623',
                       gridcolor='#1E2535',linecolor='#1E2535'),
            bgcolor='#0B0F1A',
        ),
        margin=dict(l=0,r=0,t=40,b=0),height=460)
    st.plotly_chart(fig4,use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# TAB 3
# ═══════════════════════════════════════════════════════════════════
with tab3:
    WE=RR['WE'];WOE=RR['WOE'];WF=RR['WF']
    Wpl=RR['Wpl'];Wcrew=RR['Wcrew'];Wtfo=RR['Wtfo']

    pa,pb=st.columns(2,gap="medium")
    with pa:
        st.markdown('<div class="card"><div class="card-title">Weight Breakdown</div>', unsafe_allow_html=True)
        fig_p=go.Figure(go.Pie(
            labels=['Empty Weight','Usable Fuel','Trapped Fuel','Crew','Payload'],
            values=[WE,RR['WFu'],Wtfo,Wcrew,Wpl],hole=0.55,
            marker=dict(colors=['#818CF8','#34D399','#60A5FA','#A78BFA','#4ADE80'],
                        line=dict(color='#0B0F1A',width=2)),
            textfont=dict(size=10),textinfo='label+percent'))
        fig_p.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='JetBrains Mono',color='#94A3B8'),
            showlegend=False,height=300,margin=dict(t=10,b=10,l=10,r=10),
            annotations=[dict(text=f'{Wto:,.0f}<br>lbs',x=0.5,y=0.5,
                showarrow=False,font=dict(size=12,color='#818CF8',family='JetBrains Mono'))])
        st.plotly_chart(fig_p,use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with pb:
        st.markdown('<div class="card"><div class="card-title">Weight Through Mission</div>', unsafe_allow_html=True)
        fv=list(RR['fracs'].values()); pl=list(RR['fracs'].keys())+['Landing']
        cum=[Wto]
        for f in fv: cum.append(cum[-1]*f)
        fig_w=go.Figure()
        fig_w.add_trace(go.Scatter(x=pl,y=cum,mode='lines+markers',
            line=dict(color='#818CF8',width=2.5),
            marker=dict(color='#34D399',size=7,line=dict(color='#818CF8',width=1.5)),
            fill='tozeroy',fillcolor='rgba(129,140,248,0.05)'))
        pfig(fig_w,h=300,xt='Phase',yt='Weight (lbs)')
        st.plotly_chart(fig_w,use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card"><div class="card-title">Weight Summary</div>', unsafe_allow_html=True)
    summary=pd.DataFrame({
        'Component':['W_TO  (Gross)','W_E   (Empty)','W_OE  (Op. Empty)',
                     'W_F   (Total Fuel)','W_F   (Usable)','W_tfo','W_crew','W_payload'],
        'lbs':[f"{Wto:,.0f}",f"{WE:,.0f}",f"{WOE:,.0f}",
               f"{WF:,.0f}",f"{RR['WFu']:,.0f}",
               f"{Wtfo:,.0f}",f"{Wcrew:,.0f}",f"{Wpl:,.0f}"],
        '% of W_TO':[f"{100:.1f}%",f"{WE/Wto*100:.1f}%",f"{WOE/Wto*100:.1f}%",
                     f"{WF/Wto*100:.1f}%",f"{RR['WFu']/Wto*100:.1f}%",
                     f"{Wtfo/Wto*100:.2f}%",f"{Wcrew/Wto*100:.2f}%",
                     f"{Wpl/Wto*100:.1f}%"]})
    st.dataframe(summary,hide_index=True,use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card"><div class="card-title">W_TO vs Number of Passengers</div>', unsafe_allow_html=True)
    pxa=np.arange(5,npax+22,2); wxr=[]
    for n_ in pxa:
        try: w,_=solve({**P,'npax':int(n_)}); wxr.append(w)
        except: wxr.append(float('nan'))
    fig_px=go.Figure()
    fig_px.add_trace(go.Scatter(x=pxa,y=wxr,mode='lines+markers',
        line=dict(color='#34D399',width=2),marker=dict(size=5,color='#818CF8'),
        fill='tozeroy',fillcolor='rgba(52,211,153,0.05)'))
    fig_px.add_vline(x=npax,line_dash='dot',line_color='#818CF8',line_width=1.5,
        annotation_text=f'Current: {npax} pax',annotation_font_color='#818CF8',
        annotation_font_size=9)
    pfig(fig_px,h=260,xt='Number of Passengers',yt='W_TO (lbs)')
    st.plotly_chart(fig_px,use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# TAB 4
# ═══════════════════════════════════════════════════════════════════
with tab4:
    e1,e2=st.columns(2,gap="medium")
    with e1:
        st.markdown('<div class="card"><div class="card-title">Download Data</div>', unsafe_allow_html=True)
        rows={'Parameter':['W_TO','Mff','W_F','W_payload','W_empty','W_OE',
                            'W_crew','W_tfo','WE_allow','Conv_delta',
                            'dWTO_dCp_range','dWTO_dnp_range','dWTO_dLD_range','dWTO_dR',
                            'dWTO_dCp_loiter','dWTO_dnp_loiter','dWTO_dLD_loiter'],
              'Value':[Wto,RR['Mff'],WF,Wpl,WE,WOE,Wcrew,Wtfo,RR['WEa'],RR['diff'],
                       S['dCpR'],S['dnpR'],S['dLDR'],S['dR'],
                       S['dCpE'],S['dnpE'],S['dLDE']],
              'Units':['lbs','','lbs','lbs','lbs','lbs','lbs','lbs','lbs','lbs',
                       'lbs/(lbs/hp/hr)','lbs','lbs','lbs/nm',
                       'lbs/(lbs/hp/hr)','lbs','lbs']}
        b=io.StringIO(); pd.DataFrame(rows).to_csv(b,index=False)
        st.download_button("⬇  Download Results (CSV)",b.getvalue(),
            "aeroweight_results.csv","text/csv",use_container_width=True)
        b2=io.StringIO()
        pd.DataFrame({'Phase':list(RR['fracs'].keys()),
                       'Wi/Wi-1':list(RR['fracs'].values())}).to_csv(b2,index=False)
        st.download_button("⬇  Download Phase Fractions (CSV)",b2.getvalue(),
            "aeroweight_fractions.csv","text/csv",use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with e2:
        st.markdown('<div class="card"><div class="card-title">Download PDF Report</div>', unsafe_allow_html=True)
        def make_pdf():
            buf=io.BytesIO()
            doc=SimpleDocTemplate(buf,pagesize=letter,
                leftMargin=.75*inch,rightMargin=.75*inch,
                topMargin=.75*inch,bottomMargin=.75*inch)
            sty=getSampleStyleSheet()
            sT=ParagraphStyle('T',parent=sty['Title'],fontSize=17,
                textColor=colors.HexColor('#818CF8'),spaceAfter=6)
            sH=ParagraphStyle('H',parent=sty['Heading2'],fontSize=11,
                textColor=colors.HexColor('#34D399'),spaceBefore=12,spaceAfter=4)
            sB=ParagraphStyle('B',parent=sty['Normal'],fontSize=9,leading=13)
            ts=TableStyle([
                ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#1E2535')),
                ('TEXTCOLOR',(0,0),(-1,0),colors.HexColor('#818CF8')),
                ('FONTSIZE',(0,0),(-1,-1),9),
                ('GRID',(0,0),(-1,-1),.4,colors.HexColor('#E2E8F0')),
                ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#F8FAFC')])])
            story=[Paragraph("AeroWeight Pro — Mission Report",sT),
                   Paragraph("Propeller-Driven Aircraft · Breguet Method",sB),
                   Spacer(1,.2*inch),Paragraph("Mission Inputs",sH)]
            t1=Table([['Parameter','Value'],
                       ['Passengers',str(npax)],['Crew',str(ncrew)],
                       ['Range (nm)',str(R_nm)],['Cruise L/D',str(LDc)],
                       ['Loiter endurance (hr)',str(El)]],
                      colWidths=[3*inch,3*inch])
            t1.setStyle(ts)
            story+=[t1,Spacer(1,.15*inch),Paragraph("Weight Summary",sH)]
            t2=Table([['Component','lbs','% W_TO']]+
                list(zip(summary['Component'],summary['lbs'],summary['% of W_TO'])),
                colWidths=[3*inch,1.5*inch,1.5*inch])
            t2.setStyle(ts)
            story+=[t2,Spacer(1,.15*inch),Paragraph("Sensitivity Partials",sH)]
            t3=Table([['Partial','Value','Units']]+
                list(zip(sdr['Partial'],sdr['Value'],sdr['Units']))+
                list(zip(sdl['Partial'],sdl['Value'],sdl['Units'])),
                colWidths=[2.5*inch,2*inch,1.5*inch])
            t3.setStyle(ts); story.append(t3)
            doc.build(story); buf.seek(0); return buf.read()
        st.download_button("⬇  Download PDF Report",make_pdf(),
            "aeroweight_report.pdf","application/pdf",use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card"><div class="card-title">Current Configuration</div>', unsafe_allow_html=True)
    st.dataframe(pd.DataFrame({'Parameter':list(P.keys()),
                                'Value':[str(v) for v in P.values()]}),
        hide_index=True,use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
