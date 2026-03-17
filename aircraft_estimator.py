import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import math
import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

# --- 1. CONFIGURATION & THEME ---
st.set_page_config(page_title="AeroNova: Aircraft Estimator", layout="wide")

# تصميم Cyber-Dark ليتناسب مع AeroNova Simulator X
st.markdown("""
<style>
    .stApp { background-color: #050A14; color: #C8D8F0; }
    .main-title { color: #00D4FF; font-family: 'Orbitron', sans-serif; text-align: center; text-shadow: 0 0 10px #00D4FF; }
    .stMetric { background: rgba(0, 212, 255, 0.05); border: 1px solid #7000ff; border-radius: 10px; padding: 10px; }
</style>
""", unsafe_allow_html=True)

# --- 2. PROTECTED PHYSICS ENGINE ---
def compute_mission_logic(p):
    """محرك حسابي محمي من الأخطاء الرياضية (Division by Zero, Log Errors)"""
    try:
        # Payload and Crew
        Wpl = (p['n_pax'] * (p['w_pax'] + p['w_bag'])) + p['n_crew'] * 205 + (p['n_att'] * 200)
        Wcrew = p['n_crew'] * 205 + p['n_att'] * 200
        Wtfo = p['Wto_guess'] * p['Mtfo']

        # Mission Fractions (Breguet Range Eq)
        Rc_sm = p['range_nm'] * 1.15078
        denom = (375 * (p['np_cruise'] / p['Cp_cruise']) * p['LD_cruise'])
        
        if denom <= 0: return None # حماية من القيم الصفرية أو السالبة
        
        f_cruise = math.exp(-Rc_sm / denom)
        mff = 0.970 * f_cruise * 0.990 # Standard mission profile fractions
        
        wf = p['Wto_guess'] * (1 - mff) * (1 + p['Mres'])
        we_tent = p['Wto_guess'] - wf - Wpl - Wtfo - Wcrew
        
        # حماية اللوغاريتم لـ Statistical Empty Weight
        if p['Wto_guess'] <= 0: return None
        we_allow = 10 ** ((math.log10(p['Wto_guess']) - p['A']) / p['B'])
        
        return {
            'Wpl': Wpl, 'WF': wf, 'WE': we_tent, 
            'WE_allow': we_allow, 'diff': we_allow - we_tent, 
            'Mff': mff
        }
    except Exception:
        return None

def solve_convergence(params):
    """خوارزمية التقارب (Bisection Method) مع حدود أمان"""
    lo, hi = 5000, 800000 
    for _ in range(100):
        mid = (lo + hi) / 2
        params['Wto_guess'] = mid
        res = compute_mission_logic(params)
        if res is None: return None, None
        if abs(res['diff']) < 1.0: return mid, res
        if res['diff'] > 0: hi = mid
        else: lo = mid
    return mid, res

# --- 3. UI SIDEBAR ---
st.sidebar.markdown("### ✈️ Design Parameters")
n_pax = st.sidebar.slider("Passengers", 10, 100, 34)
range_nm = st.sidebar.slider("Range (nm)", 200, 3500, 1265)
sfc_val = st.sidebar.number_input("SFC (Cp)", value=0.6, format="%.3f")

# القاموس الهندسي (Engineering Dictionary)
params = {
    'n_pax': n_pax, 'w_pax': 175, 'w_bag': 30, 'n_crew': 2, 'n_att': 1,
    'Mtfo': 0.005, 'Mres': 0.05, 'range_nm': range_nm, 'np_cruise': 0.85,
    'Cp_cruise': sfc_val, 'LD_cruise': 13.5, 'A': 0.3774, 'B': 0.9647
}

# --- 4. EXECUTION & DISPLAY ---
st.markdown('<h1 class="main-title">AERONOVA ESTIMATOR X</h1>', unsafe_allow_html=True)

wto_final, result = solve_convergence(params)

if wto_final is None:
    st.error("🚨 Calculation Error: Impossible Mission Geometry. Check SFC or L/D.")
else:
    # 1. Metrics Layout
    c1, c2, c3 = st.columns(3)
    c1.metric("Takeoff Weight (WTO)", f"{wto_final:,.0f} lbs")
    c2.metric("Fuel Weight (WF)", f"{result['WF']:,.0f} lbs")
    c3.metric("Empty Weight (WE)", f"{result['WE']:,.0f} lbs")

    # 2. Results Table
    st.markdown("### 📊 Performance Summary")
    summary_data = {
        "Weight Component": ["Gross Weight", "Empty Weight (Tentative)", "Empty Weight (Allowable)", "Payload", "Total Fuel"],
        "Value (lbs)": [f"{wto_final:,.1f}", f"{result['WE']:,.1f}", f"{result['WE_allow']:,.1f}", f"{result['Wpl']:,.1f}", f"{result['WF']:,.1f}"]
    }
    df_summary = pd.DataFrame(summary_data)
    st.table(df_summary)

    # 3. PDF Export Logic
    def export_to_pdf(df):
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = [
            Paragraph("AeroNova Simulator X: Aircraft Estimation Report", styles['Title']),
            Spacer(1, 20),
            Paragraph(f"Design Point: {n_pax} Passengers | {range_nm} nm Range", styles['Normal']),
            Spacer(1, 15)
        ]
        
        # Formatting Table for ReportLab
        data = [df.columns.to_list()] + df.values.tolist()
        t = Table(data, colWidths=[3*io.inch, 2*io.inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#00D4FF')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold')
        ]))
        elements.append(t)
        doc.build(elements)
        return buffer.getvalue()

    st.markdown("---")
    if st.button("📥 Generate Engineering Report (PDF)"):
        pdf_bytes = export_to_pdf(df_summary)
        st.download_button(label="Download PDF", data=pdf_bytes, file_name="Aircraft_Estimation_Report.pdf", mime="application/pdf")

# --- 5. VISUALIZATION ---
st.markdown("### 📈 Weight Sizing Chart")
w_range = np.linspace(20000, 100000, 50)
we_req_list, we_allow_list = [], []

for w in w_range:
    params['Wto_guess'] = w
    r = compute_mission_logic(params)
    if r:
        we_req_list.append(r['WE'])
        we_allow_list.append(r['WE_allow'])
    else:
        we_req_list.append(np.nan)
        we_allow_list.append(np.nan)

fig = go.Figure()
fig.add_trace(go.Scatter(x=w_range, y=we_req_list, name="Required WE (Mission)", line=dict(color='#00D4FF', width=3)))
fig.add_trace(go.Scatter(x=w_range, y=we_allow_list, name="Allowable WE (Stat)", line=dict(color='#7000ff', width=3, dash='dash')))
fig.update_layout(template="plotly_dark", xaxis_title="Gross Weight (lbs)", yaxis_title="Empty Weight (lbs)", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig, use_container_width=True)
