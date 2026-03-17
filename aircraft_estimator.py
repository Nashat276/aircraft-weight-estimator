import streamlit as st
import math
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from fpdf import FPDF
import io

# --- 1. THEME & UI SETUP ---
st.set_page_config(page_title="Aircraft Design Suite | Professional Edition", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #F8FAFC; }
    div[data-testid="stMetric"] { background-color: #FFFFFF; border-left: 5px solid #0F172A; border-radius: 4px; }
    .stSidebar { background-color: #0F172A !important; }
    h1, h2, h3 { color: #0F172A; font-family: 'Inter', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR: FULL MISSION INPUTS (All Parameters) ---
st.sidebar.title("🛠️ Design Parameters")

with st.sidebar:
    st.subheader("1. Design Driver")
    # WTO moved to inputs as requested
    wto_input = st.number_input("Take-off Weight (WTO) - lbs", value=48550.0, step=100.0, help="The primary variable for weight convergence.")

    with st.sidebar.expander("2. Payload & Crew Details", expanded=False):
        pax = st.number_input("Passenger Count", value=34)
        w_pax_unit = 205 # Includes baggage
        w_pl = pax * w_pax_unit
        w_crew = st.number_input("Total Crew Weight (lbs)", value=615.0)
        d_val = w_pl + w_crew

    with st.sidebar.expander("3. Mission & Fuel Specs", expanded=False):
        rc = st.number_input("Cruise Range (miles)", value=1265.8)
        eltr = st.number_input("Loiter Endurance (hrs)", value=0.75)
        m_res = st.number_input("Reserve Fuel Factor", value=0.05)
        m_tfo = st.number_input("Trapped Fuel Factor (TFO)", value=0.005)

    with st.sidebar.expander("4. Aerodynamic Efficiency", expanded=False):
        ld_c = st.number_input("L/D Ratio (Cruise)", value=13.0)
        np_c = st.number_input("Prop Efficiency (ηp)", value=0.85)
        cp_c = st.number_input("SFC (Cp) - lbs/hp/hr", value=0.6)
        ld_l = st.number_input("L/D Ratio (Loiter)", value=16.0)
        cp_l = st.number_input("SFC (Loiter)", value=0.65)

# --- 3. COMPUTATIONAL ENGINE (MDAO Logic) ---
def run_sizing_logic(wto):
    # Mission Phase Fractions (Step-by-Step as per Homework)
    f1 = 0.990 * 0.995 * 0.995 * 0.985 # Engine start to Climb
    f_cruise = 1 / math.exp(rc / (375 * (np_c / cp_c) * ld_c))
    f_loiter = 0.970 
    f_land = 0.985 * 0.995
    mff = f1 * f_cruise * f_loiter * f_land
    
    # Matching Equations
    wf = wto * (1 - mff)
    we_required = wto - wf - d_val - (m_tfo * wto)
    # Structural Constraint (Statistical Model)
    we_allowable = 10**((math.log10(wto) - 0.3774) / 0.9647)
    
    # Sensitivity Coefficients (F-Factor)
    c_val = 1 - (1 + m_res) * (1 - mff) - m_tfo
    f_growth = (-0.9647 * (wto**2) * (1 + m_res) * mff) / ((c_val * wto * (1 - 0.9647)) - d_val)
    
    # Partial Derivatives
    dw_dr = (f_growth * cp_c) / (375 * np_c * ld_c)
    dw_dcp = (f_growth * rc) / (375 * np_c * ld_c)
    
    return locals()

res = run_sizing_logic(wto_input)

# --- 4. DASHBOARD PRESENTATION ---
st.title("Aeronautical Systems Design Dashboard")
st.markdown("---")

# Row 1: Key Performance Metrics
c1, c2, c3, c4 = st.columns(4)
c1.metric("Mission Fuel Fraction", f"{res['mff']:.4f}")
c2.metric("Growth Factor (F)", f"{res['f_growth']:,.2f}")
c3.metric("Current WTO", f"{wto_input:,.0f} lb")
error = res['we_required'] - res['we_allowable']
c4.metric("Convergence Delta", f"{error:,.1f} lb", delta=error, delta_color="inverse")

# Row 2: Graphical Analysis
st.subheader("📈 Design Feasibility & Weight Convergence Map")

w_axis = np.linspace(35000, 75000, 100)
sweep = [run_sizing_logic(w) for w in w_axis]

fig = go.Figure()
fig.add_trace(go.Scatter(x=w_axis, y=[x['we_required'] for x in sweep], name='Mission Required Weight', line=dict(color='#2563EB', width=4)))
fig.add_trace(go.Scatter(x=w_axis, y=[x['we_allowable'] for x in sweep], name='Structural Allowable Weight', line=dict(color='#DC2626', width=4, dash='dot')))
fig.add_trace(go.Scatter(x=[wto_input], y=[res['we_required']], mode='markers', marker=dict(size=15, color='#10B981'), name='Your Design Point'))

fig.update_layout(plot_bgcolor='white', hovermode='x unified', margin=dict(l=0,r=0,t=40,b=0))
fig.update_xaxes(showgrid=True, gridcolor='#E2E8F0', title="WTO (lbs)")
fig.update_yaxes(showgrid=True, gridcolor='#E2E8F0', title="WE (lbs)")
st.plotly_chart(fig, use_container_width=True)

# Row 3: Sensitivity Matrix
st.subheader("📉 Sensitivity Matrix (dW/dX)")
sc1, sc2 = st.columns(2)
sc1.info(f"**Range Sensitivity (dW/dR):** {res['dw_dr']:.4f} lbs/mi")
sc2.info(f"**SFC Sensitivity (dW/dCp):** {res['dw_dcp']:.2f} lbs/unit")

# --- 5. THE MASTER PDF DOCUMENT (Professional Formatting) ---
def generate_master_pdf(d):
    pdf = FPDF()
    pdf.add_page()
    
    # Background and Border
    pdf.set_draw_color(15, 23, 42)
    pdf.rect(5, 5, 200, 287)
    
    # Header
    pdf.set_fill_color(15, 23, 42)
    pdf.rect(5, 5, 200, 35, 'F')
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", 'B', 20)
    pdf.cell(0, 15, "AIRCRAFT PRELIMINARY DESIGN DOCUMENT", ln=True, align='C')
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(0, 10, "Technical Specification & Weight Convergence Analysis", ln=True, align='C')
    
    # Body Text
    pdf.set_text_color(0, 0, 0)
    pdf.ln(15)
    
    # SECTION 1: METHODOLOGY
    pdf.set_font("Arial", 'B', 14)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(0, 10, " 1. DESIGN METHODOLOGY", ln=True, fill=True)
    pdf.set_font("Arial", '', 11)
    pdf.multi_cell(0, 7, (
        "This analysis follows the multidisciplinary design optimization (MDAO) process for fixed-wing aircraft. "
        "The objective is to find the equilibrium point where the mission fuel requirements and structural "
        "integrity constraints converge. We use the Breguet Range equation and statistical weight modeling "
        "to validate the feasibility of the chosen Take-off Weight (WTO)."
    ))
    pdf.ln(5)
    
    # SECTION 2: INPUT SUMMARY
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, " 2. INPUT CONFIGURATION", ln=True, fill=True)
    pdf.set_font("Arial", '', 11)
    col_w = 95
    pdf.cell(col_w, 8, f"Selected WTO: {wto_input:,.1f} lbs", ln=0)
    pdf.cell(col_w, 8, f"Design Range: {rc} miles", ln=1)
    pdf.cell(col_w, 8, f"Passenger Count: {pax}", ln=0)
    pdf.cell(col_w, 8, f"Fixed Weight (D): {d_val:,.1f} lbs", ln=1)
    pdf.cell(col_w, 8, f"Cruise L/D: {ld_c}", ln=0)
    pdf.cell(col_w, 8, f"Prop Efficiency: {np_c}", ln=1)
    pdf.ln(5)
    
    # SECTION 3: WEIGHT CONVERGENCE & THE GRAPH
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, " 3. CONVERGENCE ANALYSIS & VISUALIZATION", ln=True, fill=True)
    pdf.set_font("Arial", '', 11)
    pdf.multi_cell(0, 7, (
        "The Weight Equilibrium Chart (provided in the digital suite) illustrates two primary curves: "
        "1. The 'Required WE' curve represents the mission's demand for fuel and payload. "
        "2. The 'Allowable WE' curve represents the structural limits based on current aerospace materials. "
        f"At your selected WTO ({wto_input:,.1f} lbs), the convergence error is {error:,.1f} lbs. "
        "A successful design requires this error to be zero (the intersection point)."
    ))
    pdf.ln(5)
    
    # SECTION 4: SENSITIVITY & GROWTH
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, " 4. GROWTH FACTOR & SENSITIVITY", ln=True, fill=True)
    pdf.set_font("Arial", '', 11)
    pdf.multi_cell(0, 7, (
        f"The Sensitivity Growth Factor (F = {res['f_growth']:.2f}) indicates how 'penalizing' weight additions are. "
        f"Based on our derivatives, adding 1 mile of range increases WTO by {res['dw_dr']:.4f} lbs. "
        "This data allows engineers to perform trade-off studies between mission performance and aircraft size."
    ))
    
    return pdf.output(dest='S').encode('latin-1', 'ignore')

st.divider()
st.download_button("📥 DOWNLOAD COMPREHENSIVE DESIGN DOCUMENT (PDF)", 
                   data=generate_master_pdf(res), 
                   file_name="Aircraft_Master_Package.pdf")
