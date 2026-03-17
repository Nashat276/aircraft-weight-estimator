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
from reportlab.lib.units import inch

# --- 1. CONFIGURATION & STYLES ---
st.set_page_config(page_title="AeroNova Simulator X", layout="wide")

# تعريف التنسيق الصحيح للمحاور (تم حذف المفاتيح المسببة للأخطاء)
AXIS_STYLE = dict(
    showgrid=True,
    gridcolor='#1f2937',
    zeroline=False,
    tickfont=dict(color='#C8D8F0', size=10),
    title_font=dict(color='#00D4FF', size=12)
)

def apply_base(fig, title_text='', height=340):
    """دالة تنسيق الرسوم البيانية - مصححة لتجنب ValueError"""
    fig.update_layout(
        title=dict(text=title_text, font=dict(color='#00D4FF', size=16)),
        height=height,
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=40, r=20, t=60, b=40)
    )
    # استخدام التحديث بشكل منفصل لكل محور لضمان الاستقرار
    fig.update_xaxes(**AXIS_STYLE)
    fig.update_yaxes(**AXIS_STYLE)

# --- 2. PHYSICS ENGINE ---
def compute_mission(p):
    try:
        Wpl = (p['n_pax'] * (p['w_pax'] + p['w_bag'])) + p['n_crew'] * 205 + (p['n_att'] * 200)
        Wcrew = p['n_crew'] * 205 + p['n_att'] * 200
        Wtfo = p['Wto_guess'] * p['Mtfo']

        Rc_sm = p['range_nm'] * 1.15078
        denom = (375 * (p['np_cruise'] / p['Cp_cruise']) * p['LD_cruise'])
        if denom <= 0: return None
        
        f_cruise = math.exp(-Rc_sm / denom)
        mff = 0.970 * f_cruise * 0.990 
        
        wf = p['Wto_guess'] * (1 - mff) * (1 + p['Mres'])
        we_tent = p['Wto_guess'] - wf - Wpl - Wtfo - Wcrew
        
        # حماية اللوغاريتم
        wto_safe = max(100, p['Wto_guess'])
        we_allow = 10 ** ((math.log10(wto_safe) - p['A']) / p['B'])
        
        return {
            'Wpl': Wpl, 'WF': wf, 'WE': we_tent, 'WE_allow': we_allow, 
            'diff': we_allow - we_tent, 'Mff': mff,
            'fractions': {'Start': 0.99, 'Climb': 0.98, 'Cruise': round(f_cruise, 3), 'Landing': 0.99}
        }
    except: return None

def solve_wto(params):
    lo, hi = 5000, 800000
    for _ in range(50):
        mid = (lo + hi) / 2
        params['Wto_guess'] = mid
        res = compute_mission(params)
        if res is None: break
        if abs(res['diff']) < 1.0: return mid, res
        if res['diff'] > 0: hi = mid
        else: lo = mid
    return mid, res

# --- 3. UI & DISPLAY ---
st.markdown("<h1 style='text-align: center; color: #00D4FF;'>AERONOVA ESTIMATOR X</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.header("Parameters")
    pax = st.slider("Passengers", 10, 100, 34)
    dist = st.slider("Range (nm)", 200, 3000, 1200)
    sfc = st.number_input("SFC", value=0.6)

params = {
    'n_pax': pax, 'w_pax': 175, 'w_bag': 30, 'n_crew': 2, 'n_att': 1,
    'Mtfo': 0.005, 'Mres': 0.05, 'range_nm': dist, 'np_cruise': 0.85,
    'Cp_cruise': sfc, 'LD_cruise': 13, 'A': 0.3774, 'B': 0.9647
}

wto_final, result = solve_wto(params)

if result:
    c1, c2, c3 = st.columns(3)
    c1.metric("Gross Weight", f"{wto_final:,.0f} lb")
    c2.metric("Empty Weight", f"{result['WE']:,.0f} lb")
    c3.metric("Fuel Weight", f"{result['WF']:,.0f} lb")

    # --- رسم بياني باستخدام دالة apply_base المصححة ---
    st.write("### Mission Weight Fractions")
    fig = go.Figure(go.Bar(
        x=list(result['fractions'].keys()), 
        y=list(result['fractions'].values()),
        marker_color='#00D4FF'
    ))
    
    # استدعاء الدالة (هنا كان الخطأ 333)
    apply_base(fig, title_text='Phase Weight Fractions', height=340)
    fig.update_yaxes(range=[0.80, 1.02]) # تعيين المدى بشكل آمن
    
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("⚠️ يرجى مراجعة المدخلات، لم يتم الوصول لنقطة تقارب.")
