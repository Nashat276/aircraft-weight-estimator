import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import math
import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch

st.set_page_config(page_title="AeroNova Simulator X", page_icon="✈", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap');
html, body, [class*="css"] { background-color: #050A14 !important; color: #C8D8F0 !important; }
.stApp { background: linear-gradient(135deg, #050A14 0%, #0A1628 50%, #050A14 100%); }
.main-title { font-family:'Orbitron',monospace; font-size:2.2rem; font-weight:900;
    background:linear-gradient(90deg,#00D4FF,#8A2BE2,#00D4FF); background-size:200%;
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    animation:shimmer 3s infinite; text-align:center; letter-spacing:0.12em; }
@keyframes shimmer { 0%{background-position:0%} 100%{background-position:200%} }
.subtitle { font-family:'Share Tech Mono',monospace; color:#4FC3F7; text-align:center;
    font-size:0.8rem; letter-spacing:0.25em; margin-bottom:1.5rem; }
.metric-card { background:linear-gradient(135deg,#0D1F35,#0A1628); border:1px solid #00D4FF33;
    border-radius:12px; padding:1.2rem; text-align:center; margin-bottom:0.5rem; }
.metric-value { font-family:'Orbitron',monospace; font-size:1.7rem; font-weight:700; color:#00D4FF; }
.metric-unit { font-size:0.85rem; color:#4FC3F7; }
.metric-label { font-family:'Share Tech Mono',monospace; font-size:0.65rem; color:#7B9CC8;
    letter-spacing:0.12em; margin-top:0.3rem; }
.sec-hdr { font-family:'Orbitron',monospace; font-size:0.85rem; font-weight:700; color:#8A2BE2;
    letter-spacing:0.18em; border-bottom:1px solid #8A2BE230; padding-bottom:0.35rem;
    margin-bottom:0.9rem; text-transform:uppercase; }
.status-ok { background:#00FF8820; border:1px solid #00FF8860; border-radius:8px;
    padding:0.5rem 1rem; font-family:'Share Tech Mono',monospace; font-size:0.85rem; color:#00FF88; }
.status-warn { background:#FF880020; border:1px solid #FF880060; border-radius:8px;
    padding:0.5rem 1rem; font-family:'Share Tech Mono',monospace; font-size:0.85rem; color:#FF8800; }
[data-testid="stSidebar"] { background:linear-gradient(180deg,#07111F,#0A1628) !important;
    border-right:1px solid #00D4FF20 !important; }
</style>
""", unsafe_allow_html=True)

PBGX = dict(gridcolor='#00D4FF12', linecolor='#00D4FF30', color='#C8D8F0')

def mk_layout(title='', height=350, xt='', yt='', yrange=None):
    d = dict(
        paper_bgcolor='rgba(5,10,20,0)',
        plot_bgcolor='rgba(10,22,40,0.7)',
        font=dict(family='Share Tech Mono', color='#C8D8F0', size=11),
        margin=dict(l=55, r=20, t=45, b=45),
        xaxis=dict(PBGX),
        yaxis=dict(PBGX),
    )
    if title:  d['title']  = dict(text=title, font=dict(color='#4FC3F7', size=13))
    if height: d['height'] = height
    if xt:     d['xaxis']['title'] = xt
    if yt:     d['yaxis']['title'] = yt
    if yrange: d['yaxis']['range'] = yrange
    return d

def compute_mission(p):
    Wpl   = p['n_pax']*(p['w_pax']+p['w_bag']) + p['n_crew']*205 + p['n_att']*200
    Wcrew = p['n_crew']*205 + p['n_att']*200
    Wtfo  = p['Wto_guess']*p['Mtfo']
    Rc    = p['range_nm']*1.15078
    W5    = 1/math.exp(Rc/(375*(p['np_c']/p['Cp_c'])*p['LD_c']))
    Vm    = p['V_lkts']*1.15078
    W6    = 1/math.exp(p['E_l']/(375*(1/Vm)*(p['np_l']/p['Cp_l'])*p['LD_l']))
    fracs = dict(zip(['Engine Start','Taxi','Takeoff','Climb','Cruise','Loiter','Descent','Landing'],
                     [0.990,0.995,0.995,0.985,W5,W6,0.985,0.995]))
    Mff = 1.0
    for v in fracs.values(): Mff *= v
    WF_used = p['Wto_guess']*(1-Mff)
    WF      = WF_used + p['Wto_guess']*p['Mres']*(1-Mff) + Wtfo
    WOE     = p['Wto_guess'] - WF - Wpl
    WE      = WOE - Wtfo - Wcrew
    WE_all  = 10**((math.log10(p['Wto_guess'])-p['A'])/p['B'])
    return dict(Wpl=Wpl,Wcrew=Wcrew,Wtfo=Wtfo,Mff=Mff,WF=WF,WF_used=WF_used,
                WOE=WOE,WE=WE,WE_all=WE_all,diff=WE_all-WE,fracs=fracs)

def solve_wto(p, tol=1.0, n=200):
    pp=dict(p); lo,hi=5000.0,500000.0; r={}
    for _ in range(n):
        mid=(lo+hi)/2; pp['Wto_guess']=mid; r=compute_mission(pp)
        if abs(r['diff'])<tol: break
        if r['diff']>0: hi=mid
        else: lo=mid
    return mid,r

def sens_calc(p,Wto):
    Rc=p['range_nm']*1.15078; Vm=p['V_lkts']*1.15078
    Mff=compute_mission({**p,'Wto_guess':Wto})['Mff']
    D=p['n_pax']*(p['w_pax']+p['w_bag'])+p['n_crew']*205*2+p['n_att']*200
    C=1-(1+p['Mres'])*(1-Mff)-p['Mtfo']
    dn=C*Wto*(1-p['B'])-D
    F=(-p['B']*Wto**2*(1+p['Mres'])*Mff)/dn if abs(dn)>1e-6 else 0
    E=p['E_l']
    return dict(
        dCp_R= F*Rc/(375*p['np_c']*p['LD_c']),
        dnp_R=-F*Rc*p['Cp_c']/(375*p['np_c']**2*p['LD_c']),
        dLD_R=-F*Rc*p['Cp_c']/(375*p['np_c']*p['LD_c']**2),
        dR=   F*p['Cp_c']/(375*p['np_c']*p['LD_c']),
        dCp_E= F*E*Vm/(375*p['np_l']*p['LD_l']),
        dnp_E=-F*E*Vm*p['Cp_l']/(375*p['np_l']**2*p['LD_l']),
        dLD_E=-F*E*Vm*p['Cp_l']/(375*p['np_l']*p['LD_l']**2),
    )

DEF = dict(n_pax=34,w_pax=175,w_bag=30,n_crew=2,n_att=1,Mtfo=0.005,Mres=0.0,
           range_nm=1100,V_lkts=250,LD_c=13,Cp_c=0.60,np_c=0.85,
           E_l=0.75,LD_l=16,Cp_l=0.65,np_l=0.77,A=0.3774,B=0.9647)

with st.sidebar:
    st.markdown('<div class="main-title" style="font-size:1rem">PARAMETERS</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-hdr">PAYLOAD</div>', unsafe_allow_html=True)
    n_pax  = st.slider("Passengers",        10, 100, DEF['n_pax'])
    w_pax  = st.slider("Pax weight (lbs)", 140, 220, DEF['w_pax'])
    w_bag  = st.slider("Baggage (lbs)",     10,  60, DEF['w_bag'])
    n_crew = st.slider("Pilots",             1,   4, DEF['n_crew'])
    n_att  = st.slider("Attendants",         0,   4, DEF['n_att'])
    st.markdown('<div class="sec-hdr">CRUISE</div>', unsafe_allow_html=True)
    range_nm = st.slider("Range (nm)",      200,3000, DEF['range_nm'], step=50)
    LD_c     = st.slider("Cruise L/D",        8,  22, DEF['LD_c'])
    Cp_c     = st.slider("Cp cruise",        0.3, 1.0, DEF['Cp_c'],  step=0.01)
    np_c     = st.slider("np cruise",        0.5,0.95, DEF['np_c'],  step=0.01)
    st.markdown('<div class="sec-hdr">LOITER</div>', unsafe_allow_html=True)
    E_l    = st.slider("Endurance (hr)",    0.1, 3.0, DEF['E_l'],  step=0.05)
    V_lkts = st.slider("Loiter speed (kts)",100, 350, DEF['V_lkts'])
    LD_l   = st.slider("Loiter L/D",          8,  24, DEF['LD_l'])
    Cp_l   = st.slider("Cp loiter",          0.3, 1.0, DEF['Cp_l'],  step=0.01)
    np_l   = st.slider("np loiter",          0.5,0.95, DEF['np_l'],  step=0.01)
    st.markdown('<div class="sec-hdr">REGRESSION</div>', unsafe_allow_html=True)
    A_c  = st.number_input("A", value=DEF['A'],    step=0.001, format="%.4f")
    B_c  = st.number_input("B", value=DEF['B'],    step=0.001, format="%.4f")
    Mtfo = st.number_input("M_tfo", value=DEF['Mtfo'], step=0.001, format="%.4f")

P = dict(n_pax=n_pax,w_pax=w_pax,w_bag=w_bag,n_crew=n_crew,n_att=n_att,
         Mtfo=Mtfo,Mres=0.0,range_nm=range_nm,V_lkts=V_lkts,
         LD_c=LD_c,Cp_c=Cp_c,np_c=np_c,E_l=E_l,
         LD_l=LD_l,Cp_l=Cp_l,np_l=np_l,A=A_c,B=B_c,Wto_guess=48550)

Wto,R = solve_wto(P)
S = sens_calc(P,Wto)

st.markdown('<h1 class="main-title">AERONOVA SIMULATOR X</h1>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">PROPELLER-DRIVEN AIRCRAFT PRELIMINARY SIZING - BREGUET</div>', unsafe_allow_html=True)
if abs(R['diff'])<5:
    st.markdown(f'<div class="status-ok">CONVERGED - WE = {R["diff"]:.2f} lbs | W_TO = {Wto:,.0f} lbs</div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div class="status-warn">DELTA: {R["diff"]:.1f} lbs</div>', unsafe_allow_html=True)
st.markdown("---")

tab1,tab2,tab3,tab4 = st.tabs(["MISSION SIZING","SENSITIVITY","WEIGHT BREAKDOWN","EXPORT"])

with tab1:
    c1,c2,c3,c4 = st.columns(4)
    for col,val,unit,lbl in [
        (c1,f"{Wto:,.0f}","lbs","GROSS WEIGHT W_TO"),
        (c2,f"{R['Mff']:.4f}","","FUEL FRACTION"),
        (c3,f"{R['WF']:,.0f}","lbs","TOTAL FUEL"),
        (c4,f"{R['Wpl']:,.0f}","lbs","PAYLOAD"),
    ]:
        with col:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{val} <span class="metric-unit">{unit}</span></div><div class="metric-label">{lbl}</div></div>', unsafe_allow_html=True)

    st.markdown("&nbsp;")
    ca,cb = st.columns([1.1,0.9])
    with ca:
        st.markdown('<div class="sec-hdr">WEIGHT FRACTIONS</div>', unsafe_allow_html=True)
        phases = list(R['fracs'].keys())
        fracs  = list(R['fracs'].values())
        fig = go.Figure()
        fig.add_trace(go.Bar(x=phases,y=fracs,
            marker_color=['#8A2BE2','#7B6FD4','#6BB4C6','#00D4FF','#00C4EE','#00FF88','#00D070','#00B060'],
            text=[f'{v:.4f}' for v in fracs], textposition='outside',
            textfont=dict(size=10,color='#C8D8F0')))
        fig.update_layout(**mk_layout('Phase Weight Fractions',340,yrange=[0.80,1.02]))
        st.plotly_chart(fig,use_container_width=True)
    with cb:
        st.markdown('<div class="sec-hdr">GAUGE</div>', unsafe_allow_html=True)
        fig2=go.Figure(go.Indicator(mode="gauge+number+delta",value=Wto,
            delta={'reference':48550,'relative':False,'font':{'color':'#00FF88','size':14}},
            number={'suffix':' lbs','font':{'color':'#00D4FF','size':20}},
            gauge={'axis':{'range':[10000,150000]},'bar':{'color':'#00D4FF','thickness':0.25},
                   'bgcolor':'#0A1628','borderwidth':1,'bordercolor':'#00D4FF30',
                   'steps':[{'range':[10000,50000],'color':'#00FF8810'},
                             {'range':[50000,100000],'color':'#00D4FF10'},
                             {'range':[100000,150000],'color':'#FF3CAC10'}],
                   'threshold':{'line':{'color':'#FF3CAC','width':2},'thickness':0.75,'value':Wto}},
            title={'text':'W_TO'}))
        fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Share Tech Mono',color='#C8D8F0'),
            height=280,margin=dict(t=30,b=10,l=20,r=20))
        st.plotly_chart(fig2,use_container_width=True)
        st.dataframe(pd.DataFrame({
            'Parameter':['WE Tentative','WE Allowable','Delta'],
            'Value (lbs)':[f"{R['WE']:,.1f}",f"{R['WE_all']:,.1f}",f"{R['diff']:+.2f}"]}),
            hide_index=True,use_container_width=True)

    st.markdown('<div class="sec-hdr">W_TO vs RANGE</div>', unsafe_allow_html=True)
    rng_arr=np.linspace(200,3000,50); wto_arr=[]
    for rv in rng_arr:
        try:
            w,_=solve_wto({**P,'range_nm':float(rv)}); wto_arr.append(w)
        except: wto_arr.append(float('nan'))
    fig3=go.Figure()
    fig3.add_trace(go.Scatter(x=rng_arr,y=wto_arr,mode='lines',
        line=dict(color='#00D4FF',width=2.5),fill='tozeroy',fillcolor='rgba(0,212,255,0.05)'))
    fig3.add_vline(x=range_nm,line_dash='dash',line_color='#FF3CAC',line_width=1.5,
        annotation_text=f'{range_nm} nm',annotation_font_color='#FF3CAC')
    fig3.update_layout(**mk_layout('W_TO vs Range',320,xt='Range (nm)',yt='W_TO (lbs)'))
    st.plotly_chart(fig3,use_container_width=True)

with tab2:
    st.markdown('<div class="sec-hdr">SENSITIVITY PARTIALS</div>', unsafe_allow_html=True)
    col1,col2=st.columns(2)
    with col1:
        st.markdown("**Range phase**")
        s_data_r={'Partial':['dWTO/dCp','dWTO/dnp','dWTO/d(L/D)','dWTO/dR'],
                  'Value':[f"{S['dCp_R']:+,.1f}",f"{S['dnp_R']:+,.1f}",
                           f"{S['dLD_R']:+,.1f}",f"{S['dR']:+,.2f}"],
                  'Units':['lbs/(lbs/hp/hr)','lbs','lbs','lbs/nm']}
        st.dataframe(pd.DataFrame(s_data_r),hide_index=True,use_container_width=True)
    with col2:
        st.markdown("**Loiter phase**")
        s_data_l={'Partial':['dWTO/dCp','dWTO/dnp','dWTO/d(L/D)'],
                  'Value':[f"{S['dCp_E']:+,.1f}",f"{S['dnp_E']:+,.1f}",f"{S['dLD_E']:+,.1f}"],
                  'Units':['lbs/(lbs/hp/hr)','lbs','lbs']}
        st.dataframe(pd.DataFrame(s_data_l),hide_index=True,use_container_width=True)

    st.markdown('<div class="sec-hdr">TORNADO</div>', unsafe_allow_html=True)
    t_lbl=['Cp(R)','np(R)','LD(R)','R','Cp(E)','np(E)','LD(E)']
    t_val=[S['dCp_R'],S['dnp_R'],S['dLD_R'],S['dR']*range_nm*0.1,S['dCp_E'],S['dnp_E'],S['dLD_E']]
    order=sorted(range(7),key=lambda i:abs(t_val[i]))
    t_lbl=[t_lbl[i] for i in order]; t_val=[t_val[i] for i in order]
    fig_t=go.Figure(go.Bar(x=t_val,y=t_lbl,orientation='h',
        marker_color=['#00D4FF' if v>=0 else '#FF3CAC' for v in t_val],
        text=[f'{v:+,.0f}' for v in t_val],textposition='outside',textfont=dict(size=10)))
    fig_t.add_vline(x=0,line_color='#C8D8F060',line_width=1)
    fig_t.update_layout(**mk_layout('Tornado: dW_TO per unit change',380,xt='dW_TO (lbs)'))
    st.plotly_chart(fig_t,use_container_width=True)

    st.markdown('<div class="sec-hdr">3D SURFACE</div>', unsafe_allow_html=True)
    cp_arr=np.linspace(0.40,0.90,18); ld_arr=np.linspace(9.0,20.0,18)
    Z=np.zeros((len(cp_arr),len(ld_arr)))
    for i,cp in enumerate(cp_arr):
        for j,ld in enumerate(ld_arr):
            try:
                w,_=solve_wto({**P,'Cp_c':float(cp),'LD_c':float(ld)}); Z[i,j]=w
            except: Z[i,j]=float('nan')
    fig4=go.Figure(go.Surface(x=ld_arr,y=cp_arr,z=Z,
        colorscale=[[0,'#050A14'],[0.35,'#0A1628'],[0.65,'#00D4FF'],[1,'#8A2BE2']],
        opacity=0.90,showscale=True))
    fig4.update_layout(paper_bgcolor='rgba(5,10,20,0)',
        font=dict(family='Share Tech Mono',color='#C8D8F0',size=10),
        title=dict(text='W_TO over Cp and L/D',font=dict(color='#4FC3F7',size=13)),
        scene=dict(xaxis=dict(title='L/D'),yaxis=dict(title='Cp'),zaxis=dict(title='W_TO (lbs)')),
        margin=dict(l=0,r=0,t=50,b=0),height=500)
    st.plotly_chart(fig4,use_container_width=True)

with tab3:
    WE=R['WE']; WOE=R['WOE']; WF=R['WF']
    Wpl=R['Wpl']; Wcrew=R['Wcrew']; Wtfo=R['Wtfo']
    cp1,cp2=st.columns(2)
    with cp1:
        st.markdown('<div class="sec-hdr">BREAKDOWN</div>', unsafe_allow_html=True)
        fig_pie=go.Figure(go.Pie(
            labels=['Empty','Fuel (usable)','Trapped Fuel','Crew','Payload'],
            values=[WE,R['WF_used'],Wtfo,Wcrew,Wpl],hole=0.5,
            marker=dict(colors=['#8A2BE2','#00D4FF','#FF6B35','#00FF88','#FFD700'],
                        line=dict(color='#050A14',width=2)),
            textfont=dict(size=11),textinfo='label+percent'))
        fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Share Tech Mono',color='#C8D8F0'),
            title=dict(text='W_TO Breakdown',font=dict(color='#4FC3F7',size=13)),
            showlegend=False,height=320,margin=dict(t=40,b=10,l=10,r=10),
            annotations=[dict(text=f'{Wto:,.0f}<br>lbs',x=0.5,y=0.5,
                showarrow=False,font=dict(size=13,color='#00D4FF'))])
        st.plotly_chart(fig_pie,use_container_width=True)
    with cp2:
        st.markdown('<div class="sec-hdr">MISSION TRACE</div>', unsafe_allow_html=True)
        fv=list(R['fracs'].values()); pl=list(R['fracs'].keys())+['End']
        cum=[Wto]
        for f in fv: cum.append(cum[-1]*f)
        fig_w=go.Figure()
        fig_w.add_trace(go.Scatter(x=pl,y=cum,mode='lines+markers',
            line=dict(color='#00D4FF',width=2.5),marker=dict(color='#8A2BE2',size=8)))
        fig_w.update_layout(**mk_layout('Weight Through Mission',320,xt='Phase',yt='Weight (lbs)'))
        st.plotly_chart(fig_w,use_container_width=True)

    st.markdown('<div class="sec-hdr">WEIGHT SUMMARY</div>', unsafe_allow_html=True)
    summary=pd.DataFrame({
        'Component':['W_TO','W_E','W_OE','W_F total','W_F usable','W_tfo','W_crew','W_payload'],
        'Value (lbs)':[f"{Wto:,.1f}",f"{WE:,.1f}",f"{WOE:,.1f}",f"{WF:,.1f}",
                        f"{R['WF_used']:,.1f}",f"{Wtfo:,.2f}",f"{Wcrew:,.0f}",f"{Wpl:,.0f}"],
        '% W_TO':[f"{100:.1f}%",f"{WE/Wto*100:.1f}%",f"{WOE/Wto*100:.1f}%",
                   f"{WF/Wto*100:.1f}%",f"{R['WF_used']/Wto*100:.1f}%",
                   f"{Wtfo/Wto*100:.2f}%",f"{Wcrew/Wto*100:.2f}%",f"{Wpl/Wto*100:.1f}%"]})
    st.dataframe(summary,hide_index=True,use_container_width=True)

    st.markdown('<div class="sec-hdr">W_TO vs PASSENGERS</div>', unsafe_allow_html=True)
    pax_r=np.arange(5,n_pax+20,2); wto_r=[]
    for np_ in pax_r:
        try:
            w,_=solve_wto({**P,'n_pax':int(np_)}); wto_r.append(w)
        except: wto_r.append(float('nan'))
    fig_pr=go.Figure()
    fig_pr.add_trace(go.Scatter(x=pax_r,y=wto_r,mode='lines+markers',
        line=dict(color='#00FF88',width=2),marker=dict(size=5),
        fill='tozeroy',fillcolor='rgba(0,255,136,0.04)'))
    fig_pr.add_vline(x=n_pax,line_dash='dot',line_color='#FFD700',line_width=1.5,
        annotation_text=f'{n_pax} pax',annotation_font_color='#FFD700')
    fig_pr.update_layout(**mk_layout('W_TO vs Passengers',300,xt='Passengers',yt='W_TO (lbs)'))
    st.plotly_chart(fig_pr,use_container_width=True)

with tab4:
    st.markdown('<div class="sec-hdr">EXPORT</div>', unsafe_allow_html=True)
    ce1,ce2=st.columns(2)
    with ce1:
        rows={'Parameter':['W_TO','Mff','W_F','W_payload','W_empty','W_OE','W_crew','W_tfo',
                            'WE_allow','Conv_delta','dCp_R','dnp_R','dLD_R','dR',
                            'dCp_E','dnp_E','dLD_E'],
              'Value':[Wto,R['Mff'],WF,Wpl,WE,WOE,Wcrew,Wtfo,R['WE_all'],R['diff'],
                       S['dCp_R'],S['dnp_R'],S['dLD_R'],S['dR'],
                       S['dCp_E'],S['dnp_E'],S['dLD_E']],
              'Units':['lbs','','lbs','lbs','lbs','lbs','lbs','lbs','lbs','lbs',
                       'lbs/(lbs/hp/hr)','lbs','lbs','lbs/nm',
                       'lbs/(lbs/hp/hr)','lbs','lbs']}
        buf=io.StringIO(); pd.DataFrame(rows).to_csv(buf,index=False)
        st.download_button("DOWNLOAD CSV",buf.getvalue(),"aeronova.csv","text/csv",use_container_width=True)
        buf2=io.StringIO()
        pd.DataFrame({'Phase':list(R['fracs'].keys()),'Wi/Wi-1':list(R['fracs'].values())}).to_csv(buf2,index=False)
        st.download_button("DOWNLOAD FRACTIONS",buf2.getvalue(),"fractions.csv","text/csv",use_container_width=True)
    with ce2:
        def make_pdf():
            buf=io.BytesIO()
            doc=SimpleDocTemplate(buf,pagesize=letter,
                leftMargin=0.75*inch,rightMargin=0.75*inch,
                topMargin=0.75*inch,bottomMargin=0.75*inch)
            styles=getSampleStyleSheet()
            sT=ParagraphStyle('T',parent=styles['Title'],fontSize=17,
                textColor=colors.HexColor('#00D4FF'),spaceAfter=6)
            sH=ParagraphStyle('H',parent=styles['Heading2'],fontSize=11,
                textColor=colors.HexColor('#8A2BE2'),spaceBefore=10,spaceAfter=4)
            sB=ParagraphStyle('B',parent=styles['Normal'],fontSize=9,leading=13)
            ts=TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#0A1628')),
                ('TEXTCOLOR',(0,0),(-1,0),colors.HexColor('#00D4FF')),
                ('FONTSIZE',(0,0),(-1,-1),9),
                ('GRID',(0,0),(-1,-1),0.5,colors.HexColor('#334466')),
                ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#F5F8FF')])])
            story=[Paragraph("AeroNova Simulator X",sT),
                   Paragraph("Propeller Aircraft Sizing (Breguet)",sB),
                   Spacer(1,0.2*inch),Paragraph("Mission Parameters",sH)]
            t1=Table([['Parameter','Value'],['Passengers',str(n_pax)],['Crew',str(n_crew)],
                       ['Range (nm)',str(range_nm)],['Cruise L/D',str(LD_c)],
                       ['Endurance (hr)',str(E_l)]],colWidths=[3*inch,3*inch])
            t1.setStyle(ts)
            story+=[t1,Spacer(1,0.15*inch),Paragraph("Weight Summary",sH)]
            t2=Table([['Component','Value (lbs)','% W_TO']]+
                list(zip(summary['Component'],summary['Value (lbs)'],summary['% W_TO'])),
                colWidths=[3*inch,1.5*inch,1.5*inch])
            t2.setStyle(ts)
            story+=[t2,Spacer(1,0.15*inch),Paragraph("Sensitivity Partials",sH)]
            t3=Table([['Partial','Value','Units']]+
                list(zip(s_data_r['Partial'],s_data_r['Value'],s_data_r['Units']))+
                list(zip(s_data_l['Partial'],s_data_l['Value'],s_data_l['Units'])),
                colWidths=[2.5*inch,2*inch,1.5*inch])
            t3.setStyle(ts)
            story.append(t3)
            doc.build(story); buf.seek(0); return buf.read()
        st.download_button("DOWNLOAD PDF",make_pdf(),"aeronova.pdf","application/pdf",use_container_width=True)

    st.markdown("---")
    st.dataframe(pd.DataFrame({'Param':list(P.keys()),'Value':[str(v) for v in P.values()]}),
        hide_index=True,use_container_width=True)
