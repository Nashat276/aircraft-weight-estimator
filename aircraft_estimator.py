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

# --- CONFIGURATION ---
st.set_page_config(page_title="AeroNova Simulator X", page_icon="✈", layout="wide")

# --- CSS STYLING ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Share+Tech+Mono&display=swap');
    .stApp { background-color: #050A14; color: #C8D8F0; }
    .main-title { font-family: 'Orbitron', sans-serif; font-size: 2.5rem; color: #00D4FF; text-align: center; margin-bottom: 20px; }
    .section-header { font-family: 'Orbitron', sans-serif; color: #8A2BE2; border-bottom: 1px solid #8A2BE240; padding-bottom: 5px; margin-top: 20px; }
</style>
""", unsafe_allow_html=True)

# --- PHYSICS ENGINE ---
def compute_mission(p):
    try:
        Wpl = (p['n_pax'] * (p['w_pax'] + p['w_bag'])) + p['n_crew'] * 205 + (p['n_att'] * 200)
        Wcrew = p['n_crew'] * 205 + p['n_att'] * 200
        Wtfo = p['Wto_guess'] * p['Mtfo']

        # Weight fractions
        W1_Wto, W2_W1, W3_W2, W4_W3 = 0.990, 0.995, 0.995, 0.985
        Rc_sm = p['range_nm'] * 1.15078
        V_mph = p['V_loiter_kts'] * 1.15078
        
        # Cruise & Loiter (Breguet)
        W5_W4 = 1.0 / math.exp(Rc_sm / (375 * (p['np_cruise'] / p['Cp_cruise']) * p['LD_cruise']))
        W6_W5 = 1.0 / math.exp(p['E_loiter'] / (375 * (1.0 / V_mph) * (p['np_loiter'] / p['Cp_loiter']) * p['LD_loiter']))
        W7_W6, W8_W7 = 0.985, 0.995

        Mff = W1_Wto * W2_W1 * W3_W2 * W4_W3 * W5_W4 * W6_W5 * W7_W6 * W8_W7
        WF = p['Wto_guess'] * (1 - Mff) * (1 + p['Mres']) + Wtfo
        WE_tent = p['Wto_guess'] - WF - Wpl - Wtfo - Wcrew
        WE_allow = 10 ** ((math.log10(max(1, p['Wto_guess'])) - p['A']) / p['B'])
        
        return {
            'Wpl': Wpl, 'WF': WF, 'WE': WE_tent, 'WE_allow': WE_allow, 
            'diff': WE_allow - WE_tent, 'Mff': Mff,
            'fractions': {'Engine Start': W1_Wto, 'Taxi': W2_W1, 'Takeoff': W3_W2, 'Climb': W4_W3, 'Cruise': W5_W4, 'Loiter': W6_W5, 'Descent': W7_W6, 'Landing': W8_W7}
        }
    except: return None

def solve_wto(params):
    lo, hi = 5000, 500000
    for _ in range(50):
        mid = (lo + hi) / 2
        params['Wto_guess'] = mid
        res = compute_mission(params)
        if res is None: break
        if abs(res['diff']) < 1.0: return mid, res
        if res['diff'] > 0: hi = mid
        else: lo = mid
    return mid, res

# --- SHARED LAYOUT ---
PLOTLY_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Share Tech Mono', color='#C8D8F0')
)

# --- SIDEBAR INPUTS ---
with st.sidebar:
    st.markdown("### DESIGN INPUTS")
    pax = st.slider("Passengers", 10, 100, 34)
    dist = st.slider("Range (nm)", 200, 3000, 1100)
    sfc = st.number_input("SFC (lb/hp/hr)", value=0.6, format="%.3f")
    ld_c = st.slider("Cruise L/D", 8, 20, 13)

params = {
    'n_pax': pax, 'w_pax': 175, 'w_bag': 30, 'n_crew': 2, 'n_att': 1,
    'Mtfo': 0.005, 'Mres': 0.05, 'range_nm': dist, 'V_cruise_kts': 250, 'LD_cruise': ld_c, 
    'Cp_cruise': sfc, 'np_cruise': 0.85, 'E_loiter': 0.75, 'V_loiter_kts': 200, 
    'LD_loiter': 16, 'Cp_loiter': 0.65, 'np_loiter': 0.77, 'A': 0.3774, 'B': 0.9647
}

# --- MAIN EXECUTION ---
st.markdown('<h1 class="main-title">✈ AERONOVA ESTIMATOR X</h1>', unsafe_allow_html=True)
Wto, result = solve_wto(params)

if result:
    tab1, tab2 = st.tabs(["📊 MISSION ANALYSIS", "📑 EXPORT REPORT"])
    
    with tab1:
        c1, c2, c3 = st.columns(3)
        c1.metric("Gross Weight (WTO)", f"{Wto:,.0f} lb")
        c2.metric("Fuel Fraction (Mff)", f"{result['Mff']:.4f}")
        c3.metric("Empty Weight (WE)", f"{result['WE']:,.0f} lb")

        st.markdown('<div class="section-header">WEIGHT FRACTIONS</div>', unsafe_allow_html=True)
        
        # --- FIXED CHART (THE CAUSE OF THE ERROR) ---
        fig = go.Figure(go.Bar(
            x=list(result['fractions'].keys()), 
            y=list(result['fractions'].values()),
            marker_color='#00D4FF'
        ))
        
        # تصحيح السطر 409: فصل الـ Layout عن الـ Y-axis range
        fig.update_layout(
            **PLOTLY_LAYOUT,
            title=dict(text='Mission Phase Weight Fractions', font=dict(color='#4FC3F7', size=16))
        )
        # الطريقة الصحيحة لتعيين المدى بدون ValueError
        fig.update_yaxes(range=[0.80, 1.02], gridcolor='#1f2937')
        
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.markdown('<div class="section-header">PDF GENERATION</div>', unsafe_allow_html=True)
        
        def generate_pdf(res, wto):
            buf = io.BytesIO()
            doc = SimpleDocTemplate(buf, pagesize=letter)
            styles = getSampleStyleSheet()
            elements = [Paragraph("AeroNova Simulator X - Report", styles['Title']), Spacer(1, 12)]
            
            data = [
                ["Parameter", "Value"],
                ["Gross Weight (WTO)", f"{wto:,.1f} lb"],
                ["Fuel Weight", f"{res['WF']:,.1f} lb"],
                ["Empty Weight", f"{res['WE']:,.1f} lb"],
                ["Payload", f"{res['Wpl']:,.1f} lb"]
            ]
            t = Table(data, colWidths=[3*inch, 2*inch])
            t.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.black), ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke), ('GRID',(0,0),(-1,-1),0.5,colors.grey)]))
            elements.append(t)
            doc.build(elements)
            return buf.getvalue()

        if st.button("Download Engineering Report"):
            pdf_bytes = generate_pdf(result, Wto)
            st.download_button("Download PDF", data=pdf_bytes, file_name="AeroNova_Report.pdf", mime="application/pdf")

else:
    st.error("🚨 Convergence Failed: المدخلات الحالية غير منطقية فيزيائياً.")
