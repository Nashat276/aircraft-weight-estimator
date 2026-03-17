import streamlit as st
import math
import numpy as np
import plotly.graph_objects as go
from fpdf import FPDF

# --- 1. RADICAL GLASS-AERO UI DESIGN ---
st.set_page_config(page_title="AeroOptimizer Ultra | Professional Sizing", layout="wide")

st.markdown("""
    <style>
    /* Main Background with a faded, transparent airplane theme */
    .stApp {
        background: linear-gradient(rgba(11, 14, 20, 0.9), rgba(11, 14, 20, 0.9)), 
                    url('https://www.transparenttextures.com/patterns/carbon-fibre.png'),
                    url('https://images.unsplash.com/photo-1517976487492-5750f3195933?q=80&w=2000');
        background-size: cover;
        background-attachment: fixed;
        color: #E2E8F0;
    }
    
    /* Sidebar: Professional Contrast with Blur Effect */
    section[data-testid="stSidebar"] {
        background-color: rgba(22, 27, 34, 0.95) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(88, 166, 255, 0.3);
    }
    section[data-testid="stSidebar"] label, section[data-testid="stSidebar"] p {
        color: #58A6FF !important; /* Cyber Blue */
        font-weight: 700 !important;
        text-transform: uppercase;
        font-size: 13px !important;
    }
    
    /* Transparent Metrics Cards */
    div[data-testid="stMetric"] {
        background: rgba(28, 33, 40, 0.6);
        backdrop-filter: blur(5px);
        border: 1px solid rgba(88, 166, 255, 0.2);
        border-left: 5px solid #58A6FF;
        border-radius: 12px;
        padding: 20px;
    }
    
    /* Customizing Headings */
    h1, h2, h3 { 
        color: #58A6FF; 
        text-shadow: 0px 0px 10px rgba(88, 166, 255, 0.3);
    }
    
    /* Faded Image Overlay Effect */
    .faded-aero {
        opacity: 0.15;
        position: fixed;
        top: 10%;
        right: 5%;
        z-index: -1;
        width: 40%;
    }
    </style>
    
    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Airplane_silhouette.svg/640px-Airplane_silhouette.svg.png" class="faded-aero">
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR: THE ENGINEERING DASHBOARD ---
st.sidebar.markdown("### 🛠️ DESIGN COMMAND")

with st.sidebar:
    st.markdown("---")
    wto_input = st.number_input("Design WTO (lbs)", value=48550.0, step=50.0)
    
    with st.expander("📦 PAYLOAD & ASSETS", expanded=True):
        pax = st.number_input("PAX Count", value=34)
        w_pax_total = pax * 205
        w_crew = st.number_input("Crew Weight", value=615.0)
        d_val_input = w_pax_total + w_crew

    with st.expander("🚀 CRUISE (Table 2.20)", expanded=True):
        rc = st.number_input("Range (mi)", value=1265.8)
        ld_c = st.number_input("Cruise L/D", value=13.0)
        cp_c = st.number_input("SFC (Cp)", value=0.6)
        np_c = st.number_input("Prop ηp", value=0.85)

    with st.expander("🛡️ SAFETY & RESERVES", expanded=False):
        eltr = st.number_input("Endurance (hrs)", value=0.75)
        ld_l = st.number_input("Loiter L/D", value=16.0)
        cp_l = st.number_input("Loiter SFC", value=0.65)
        m_res = st.number_input("Reserves Factor", value=0.05)
        m_tfo = st.number_input("TFO Ratio", value=0.005)

# --- 3. PHYSICS ENGINE (TABLE 2.20 COMPLIANT) ---
def run_solver(wto):
    # Mission Fuel Fractions
    f_p = 0.990 * 0.995 * 0.995 * 0.985 
    f_c = 1 / math.exp(rc / (375 * (np_c / cp_c) * ld_c))
    f_l = 1 / math.exp(eltr / (375 * (0.80 / cp_l) * ld_l))
    f_e = 0.985 * 0.995
    mff = f_p * f_c * f_l * f_e
    
    # Equation 2.22 Logic
    c_val = 1 - (1 + m_res) * (1 - mff) - m_tfo
    wf = wto * (1 - mff)
    we_req = wto - wf - d_val_input - (m_tfo * wto)
    we_allow = 10**((math.log10(wto) - 0.3774) / 0.9647)
    
    # Sensitivity & Growth Factor
    num_f = -0.9647 * (wto**2) * (1 + m_res) * mff
    den_f = (c_val * wto * (1 - 0.9647)) - d_val_input
    f_growth = num_f / den_f if den_f != 0 else 0
    
    dw_dr = (f_growth * cp_c) / (375 * np_c * ld_c)
    dw_dcp = (f_growth * rc) / (375 * np_c * ld_c)
    
    return {
        "mff": mff, "f_growth": f_growth, "c_val": c_val,
        "we_req": we_req, "we_allow": we_allow, "wf": wf,
        "dw_dr": dw_dr, "dw_dcp": dw_dcp, "d_val": d_val_input
    }

res = run_solver(wto_input)

# --- 4. MAIN INTERFACE ---
st.title("🛡️ AeroOptimizer Ultra | Design Suite")
st.markdown("##### High-Fidelity Sizing & Sensitivity Analysis | Engineering Command Center")
st.divider()

# Top Metrics Row
c1, c2, c3, c4 = st.columns(4)
c1.metric("Mission Mff", f"{res['mff']:.4f}")
c2.metric("Growth Factor (F)", f"{res['f_growth']:,.2f}")
c3.metric("Efficiency (C)", f"{res['c_val']:.4f}")
delta = res['we_req'] - res['we_allow']
c4.metric("Convergence Delta", f"{delta:,.1f} lb", delta=delta, delta_color="inverse")

st.divider()

# Graphical Section
col_plot, col_info = st.columns([2, 1])

with col_plot:
    st.subheader("🌐 Convergence Map")
    
    w_axis = np.linspace(35000, 75000, 100)
    sweep = [run_solver(w) for w in w_axis]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=w_axis, y=[x['we_req'] for x in sweep], name='Mission Required WE', line=dict(color='#58A6FF', width=4)))
    fig.add_trace(go.Scatter(x=w_axis, y=[x['we_allow'] for x in sweep], name='Structural Allowable WE', line=dict(color='#F85149', width=4, dash='dot')))
    fig.add_trace(go.Scatter(x=[wto_input], y=[res['we_req']], mode='markers', marker=dict(size=14, color='#3FB950', symbol='diamond'), name='Design Point'))
    
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#8B949E', margin=dict(l=0,r=0,t=20,b=0))
    fig.update_xaxes(showgrid=True, gridcolor='rgba(255,255,255,0.1)', title="WTO (lbs)")
    fig.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.1)', title="WE (lbs)")
    st.plotly_chart(fig, use_container_width=True)

with col_info:
    st.subheader("📑 Design Summary")
    st.write(f"**Payload Asset (D):** {res['d_val']:,.1f} lbs")
    st.write(f"**Calculated Fuel (Wf):** {res['wf']:,.1f} lbs")
    st.info("Technical equilibrium is reached where the blue and red curves intersect.")

st.divider()

# Sensitivity Table 2.20
st.subheader("📉 Sensitivity Analysis (Table 2.20)")
sc1, sc2 = st.columns(2)
sc1.metric("Range Penalty (dW/dR)", f"{res['dw_dr']:.4f} lbs/mi")
sc2.metric("SFC Penalty (dW/dCp)", f"{res['dw_dcp']:,.1f} lbs/unit")

# --- 5. THE MASTER PDF PACKAGE ---
def generate_pdf(d):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_draw_color(88, 166, 255)
    pdf.rect(5, 5, 200, 287)
    
    pdf.set_fill_color(13, 17, 23)
    pdf.rect(5, 5, 200, 45, 'F')
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", 'B', 20)
    pdf.cell(0, 20, "AIRCRAFT MASTER DESIGN REPORT", ln=True, align='C')
