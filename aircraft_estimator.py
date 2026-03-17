import streamlit as st
import math
import numpy as np
import plotly.graph_objects as go
from fpdf import FPDF

# --- 1. PRESTIGE UI DESIGN (Professional Aero Theme) ---
st.set_page_config(page_title="AeroOptimizer Ultra | Professional Sizing", layout="wide")

st.markdown("""
    <style>
    /* Dark Aero Theme - Cockpit Feel */
    .main { background-color: #0B0F19; color: #E2E8F0; }
    
    /* Sidebar: Professional Contrast */
    section[data-testid="stSidebar"] {
        background-color: #161B22 !important;
        border-right: 2px solid #58A6FF;
    }
    section[data-testid="stSidebar"] label, section[data-testid="stSidebar"] p {
        color: #58A6FF !important; /* Cyber Blue */
        font-weight: 700 !important;
        text-transform: uppercase;
        font-size: 13px !important;
    }
    
    /* Metrics: Glowing Border */
    div[data-testid="stMetric"] {
        background: #1C2128;
        border: 1px solid #30363D;
        border-left: 5px solid #58A6FF;
        border-radius: 8px;
        padding: 15px;
    }
    
    /* Inputs Styling */
    .stNumberInput input {
        background-color: #0D1117 !important;
        color: #FFFFFF !important;
        border: 1px solid #30363D !important;
    }
    
    h1, h2, h3 { color: #58A6FF; font-family: 'Inter', sans-serif; letter-spacing: -1px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR: THE ENGINEERING DASHBOARD ---
# إضافة أيقونة طائرة لتعزيز الهوية البصرية
st.sidebar.markdown("### ✈️ FLIGHT DESIGN CONFIG")

with st.sidebar:
    st.markdown("---")
    wto_input = st.number_input("Design WTO (lbs)", value=48550.0, step=100.0)
    
    with st.expander("📦 PAYLOAD & CREW UNITS", expanded=True):
        pax = st.number_input("PAX Count", value=34)
        w_pax_calc = pax * 205
        w_crew_fixed = st.number_input("Crew Weight (lbs)", value=615.0)
        d_val_final = w_pax_calc + w_crew_fixed

    with st.expander("🚀 MISSION SPECS (TABLE 2.20)", expanded=True):
        rc = st.number_input("Range (mi)", value=1265.8)
        ld_c = st.number_input("Cruise L/D", value=13.0)
        cp_c = st.number_input("Cruise SFC (Cp)", value=0.6)
        np_c = st.number_input("Prop ηp", value=0.85)

    with st.expander("🔄 LOITER & RESERVES", expanded=False):
        eltr = st.number_input("Loiter (hrs)", value=0.75)
        ld_l = st.number_input("Loiter L/D", value=16.0)
        cp_l = st.number_input("Loiter SFC", value=0.65)
        m_res = st.number_input("M_res Factor", value=0.05)
        m_tfo = st.number_input("TFO Ratio", value=0.005)

# --- 3. PHYSICS ENGINE (TABLE 2.20 COMPLIANT) ---
def run_solver(wto):
    # Mission Fuel Fractions
    f_phases = 0.990 * 0.995 * 0.995 * 0.985 
    f_cruise = 1 / math.exp(rc / (375 * (np_c / cp_c) * ld_c))
    f_loiter = 1 / math.exp(eltr / (375 * (0.80 / cp_l) * ld_l))
    f_land = 0.985 * 0.995
    mff = f_phases * f_cruise * f_loiter * f_land
    
    # Matching Logic (Eq 2.22)
    c_val = 1 - (1 + m_res) * (1 - mff) - m_tfo
    wf = wto * (1 - mff)
    we_req = wto - wf - d_val_final - (m_tfo * wto)
    we_allow = 10**((math.log10(wto) - 0.3774) / 0.9647)
    
    # Growth Factor (F) & Sensitivity
    num_f = -0.9647 * (wto**2) * (1 + m_res) * mff
    den_f = (c_val * wto * (1 - 0.9647)) - d_val_final
    f_growth = num_f / den_f if den_f != 0 else 0
    
    dw_dr = (f_growth * cp_c) / (375 * np_c * ld_c)
    dw_dcp = (f_growth * rc) / (375 * np_c * ld_c)
    
    # Return explicit dictionary to prevent KeyError
    return {
        "mff": mff, "f_growth": f_growth, "c_val": c_val,
        "we_req": we_req, "we_allow": we_allow, "wf": wf,
        "dw_dr": dw_dr, "dw_dcp": dw_dcp, "d_val": d_val_final
    }

res = run_solver(wto_input)

# --- 4. MAIN INTERFACE ---
# صورة جمالية تعبر عن الطيران والاحترافية اللوجستية
st.image("https://images.unsplash.com/photo-1540962351504-03099e0a754b?q=80&w=2000", use_column_width=True)
st.title("🛡️ AeroOptimizer Ultra | Design Suite")
st.markdown("##### Sizing, Convergence & Sensitivity Matrix | Academic & Professional Standard")
st.divider()

# Metrics Dashboard
c1, c2, c3, c4 = st.columns(4)
c1.metric("Mission Fuel Fraction", f"{res['mff']:.4f}")
c2.metric("Growth Factor (F)", f"{res['f_growth']:,.2f}")
c3.metric("Efficiency Factor (C)", f"{res['c_val']:.4f}")
error = res['we_req'] - res['we_allow']
c4.metric("Convergence Delta", f"{error:,.1f} lb", delta=error, delta_color="inverse")

st.divider()

# Graphical Section
col_map, col_data = st.columns([2, 1])

with col_map:
    st.subheader("🌐 Weight Convergence Analysis")
    
    w_axis = np.linspace(35000, 75000, 100)
    sweep = [run_solver(w) for w in w_axis]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=w_axis, y=[x['we_req'] for x in sweep], name='Mission Required WE', line=dict(color='#58A6FF', width=4)))
    fig.add_trace(go.Scatter(x=w_axis, y=[x['we_allow'] for x in sweep], name='Structural Allowable WE', line=dict(color='#F85149', width=4, dash='dot')))
    fig.add_trace(go.Scatter(x=[wto_input], y=[res['we_req']], mode='markers', marker=dict(size=15, color='#3FB950', symbol='diamond'), name='Design Point'))
    
    fig.update_layout(plot_bgcolor='#0D1117', paper_bgcolor='#0B0F19', font_color='#8B949E', margin=dict(l=0,r=0,t=20,b=0))
    fig.update_xaxes(showgrid=True, gridcolor='#30363D', title="WTO (lbs)")
    fig.update_yaxes(showgrid=True, gridcolor='#30363D', title="WE (lbs)")
    st.plotly_chart(fig, use_container_width=True)

with col_data:
    st.subheader("📑 Analysis Breakdown")
    # تم حل مشكلة KeyError هنا باستخدام اسم المتغير الصحيح
    st.write(f"**Payload Asset (D):** {res['d_val']:,.1f} lbs")
    st.write(f"**Total Fuel (Wf):** {res['wf']:,.1f} lbs")
    st.info("The convergence point is where the airframe's mission fuel needs meet its structural limits.")

st.divider()

# Sensitivity Section
st.subheader("📉 Design Sensitivity (Table 2.20)")
sc1, sc2 = st.columns(2)
sc1.metric("Range Penalty (dW/dR)", f"{res['dw_dr']:.4f} lbs/mi")
sc2.metric("Efficiency Penalty (dW/dCp)", f"{res['dw_dcp']:,.1f} lbs/unit")

# --- 5. THE MASTER PDF REPORT ---
def generate_pdf(d):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_draw_color(88, 166, 255)
    pdf.rect(5, 5, 200, 287)
    
    pdf.set_fill_color(22, 27, 34)
    pdf.rect(5, 5, 200, 45, 'F')
    pdf.set_text_color(88, 166, 255)
    pdf.set_font("Arial", 'B', 20)
    pdf.cell(0, 25, "AIRCRAFT MASTER DESIGN REPORT", ln=True, align='C')
    pdf.set_font("Arial", 'I', 11)
    pdf.cell(0, 5, "Quantitative Master Sizing & Sensitivity Matrix", ln=True, align='C')
    
    pdf.set_text_color(0, 0, 0)
    pdf.ln(25)
    
    sections = [
        ("1. DESIGN METHODOLOGY", "Details the multidisciplinary sizing logic by iterating WTO against fuel fractions and structural weight constants."),
        ("2. CONFIGURATION MATRIX", f"Selected WTO: {wto_input:,.1f} lbs\nMission Range: {rc} miles\nPayload D: {d_val_final:,.1f} lbs"),
        ("3. CONVERGENCE SUMMARY", f"Mission Fuel Fraction: {d['mff']:.4f}\nGrowth Factor F: {d['f_growth']:.2f}\nStructural Delta: {d['we_req'] - d['we_allow']:,.1f} lbs"),
        ("4. SENSITIVITY DERIVATIVES", f"dW/dR (Range): {d['dw_dr']:.4f} lbs/mi\ndW/dCp (SFC): {d['dw_dcp']:.2f} lbs/unit")
    ]
    
    for title, content in sections:
        pdf.set_font("Arial", 'B', 14)
        pdf.set_fill_color(241, 245, 249)
        pdf.cell(0, 10, f" {title}", ln=True, fill=True)
        pdf.set_font("Arial", '', 11)
        pdf.multi_cell(0, 7, content)
        pdf.ln(5)

    return pdf.output(dest='S').encode('latin-1', 'ignore')

st.divider()
st.download_button("📥 DOWNLOAD MASTER DESIGN PACKAGE (PDF)", data=generate_pdf(res), file_name="Aero_Master_Design.pdf")
