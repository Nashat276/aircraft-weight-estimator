import streamlit as st
import math
import numpy as np
import plotly.graph_objects as go
from fpdf import FPDF

# --- 1. PAGE CONFIGURATION (Clean Native Look) ---
st.set_page_config(page_title="Aircraft Sizing Tool", layout="wide")

# --- 2. CORE SIZING SOLVER ---
def calculate_sizing(wto_guess, range_mi, sfc, ld_cruise, pax, crew_wt):
    # Fixed Parameters
    m_res = 0.05
    m_tfo = 0.005
    eta_prop = 0.85
    
    # Payload Asset (D)
    payload_wt = pax * 205
    d_val = payload_wt + crew_wt
    
    # Mission Fractions
    f_startup = 0.980 # Combined start/taxi/takeoff/climb
    f_cruise = 1 / math.exp(range_mi / (375 * (eta_prop / sfc) * ld_cruise))
    f_loiter = 0.990 # Assumed fixed fraction for simplicity
    f_land = 0.985
    mff = f_startup * f_cruise * f_loiter * f_land
    
    # Weight Matching
    wf = wto_guess * (1 - mff)
    we_req = wto_guess - wf - d_val - (m_tfo * wto_guess)
    we_allow = 10**((math.log10(wto_guess) - 0.3774) / 0.9647)
    
    # Sensitivity (Growth Factor F)
    c_factor = 1 - (1 + m_res) * (1 - mff) - m_tfo
    num_f = -0.9647 * (wto_guess**2) * (1 + m_res) * mff
    den_f = (c_factor * wto_guess * (1 - 0.9647)) - d_val
    f_growth = num_f / den_f if den_f != 0 else 0
    
    dw_dr = (f_growth * sfc) / (375 * eta_prop * ld_cruise)
    dw_dcp = (f_growth * range_mi) / (375 * eta_prop * ld_cruise)

    # Return comprehensive dictionary
    return {
        "mff": mff, "f_growth": f_growth, "we_req": we_req, 
        "we_allow": we_allow, "wf": wf, "d_val": d_val,
        "dw_dr": dw_dr, "dw_dcp": dw_dcp, "wto": wto_guess
    }

# --- 3. SIDEBAR: CLEAN INPUTS ---
with st.sidebar:
    st.header("Input Parameters")
    
    st.subheader("Weights")
    wto_in = st.number_input("Design WTO (lbs)", min_value=10000.0, value=48550.0, step=100.0)
    
    st.subheader("Payload & Crew")
    pax_in = st.number_input("Number of Passengers", min_value=0, value=34, step=1)
    crew_in = st.number_input("Crew Weight (lbs)", min_value=0.0, value=615.0, step=10.0)
    
    st.subheader("Aerodynamics & Mission")
    range_in = st.number_input("Range (mi)", min_value=100.0, value=1265.8, step=10.0)
    sfc_in = st.number_input("SFC (lb/hp/hr)", min_value=0.1, value=0.6, step=0.05)
    ld_in = st.number_input("Cruise L/D", min_value=5.0, value=13.0, step=0.5)

# Execute Calculations
res = calculate_sizing(wto_in, range_in, sfc_in, ld_in, pax_in, crew_in)

# --- 4. MAIN LAYOUT ---
st.title("Conceptual Aircraft Sizing")
st.markdown("A clean, MDAO-based weight estimation and sensitivity analysis tool.")
st.divider()

# KPI Metrics (Native Streamlit)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Fuel Fraction (Mff)", f"{res['mff']:.4f}")
col2.metric("Growth Factor (F)", f"{res['f_growth']:.2f}")
col3.metric("Payload Factor (D)", f"{res['d_val']:,.1f} lbs")

convergence_delta = res['we_req'] - res['we_allow']
col4.metric("Convergence Delta", f"{convergence_delta:,.1f} lbs", 
            delta=f"{convergence_delta:,.1f}", delta_color="inverse")

st.divider()

# Main Content Tabs
tab1, tab2, tab3 = st.tabs(["Convergence Plot", "Detailed Breakdown", "Export Report"])

with tab1:
    st.subheader("Weight Convergence Analysis")
    # Clean Plotly White Template
    w_range = np.linspace(30000, 70000, 50)
    sweep_data = [calculate_sizing(w, range_in, sfc_in, ld_in, pax_in, crew_in) for w in w_range]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=w_range, y=[x['we_req'] for x in sweep_data], 
                             name='Required WE', line=dict(color='blue', width=2)))
    fig.add_trace(go.Scatter(x=w_range, y=[x['we_allow'] for x in sweep_data], 
                             name='Allowable WE', line=dict(color='red', width=2, dash='dash')))
    fig.add_trace(go.Scatter(x=[wto_in], y=[res['we_req']], 
                             mode='markers', marker=dict(size=10, color='green'), name='Design Point'))
    
    fig.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=30, b=20),
                      xaxis_title="Gross Weight (WTO) [lbs]", yaxis_title="Empty Weight (WE) [lbs]")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Weight & Sensitivity Log")
    col_w, col_s = st.columns(2)
    
    with col_w:
        st.markdown("**Weight Components**")
        st.dataframe({
            "Component": ["Payload + Crew (D)", "Mission Fuel (Wf)", "Empty Weight (Required)", "Empty Weight (Allowable)"],
            "Value (lbs)": [f"{res['d_val']:,.1f}", f"{res['wf']:,.1f}", f"{res['we_req']:,.1f}", f"{res['we_allow']:,.1f}"]
        }, hide_index=True, use_container_width=True)

    with col_s:
        st.markdown("**Sensitivity Derivatives**")
        st.dataframe({
            "Parameter": ["Range Penalty (dW/dR)", "SFC Penalty (dW/dCp)"],
            "Value": [f"{res['dw_dr']:.4f} lbs/mi", f"{res['dw_dcp']:.2f} lbs/unit"]
        }, hide_index=True, use_container_width=True)

with tab3:
    st.subheader("Technical Report")
    st.write("Generate a clean PDF summary of the current design configuration.")
    
    def create_pdf(data):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "AIRCRAFT SIZING REPORT", ln=True, align='C')
        pdf.ln(10)
        
        pdf.set_font("Arial", '', 12)
        lines = [
            f"Target Gross Weight (WTO): {data['wto']:,.1f} lbs",
            f"Payload Factor (D): {data['d_val']:,.1f} lbs",
            f"Mission Fuel Fraction (Mff): {data['mff']:.4f}",
            f"Growth Factor (F): {data['f_growth']:.2f}",
            f"Convergence Delta: {data['we_req'] - data['we_allow']:,.1f} lbs",
            "--------------------------------------------------",
            f"Range Sensitivity (dW/dR): {data['dw_dr']:.4f} lbs/mi",
            f"SFC Sensitivity (dW/dCp): {data['dw_dcp']:.2f} lbs/unit"
        ]
        
        for line in lines:
            pdf.cell(0, 10, line, ln=True)
            
        return pdf.output(dest='S').encode('latin-1')

    st.download_button(
        label="Download PDF Report",
        data=create_pdf(res),
        file_name="Aircraft_Sizing_Report.pdf",
        mime="application/pdf"
    )
