import streamlit as st
import math
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# ---------------- UI ----------------
st.set_page_config(page_title="AeroDesign Solver Pro", layout="wide")

st.markdown("""
<style>
.main { background-color: #0b0d11; color: #00d4ff; }
h1 { text-align:center; }
</style>
""", unsafe_allow_html=True)

st.title("✈️ AeroDesign Solver Pro")

# ---------------- INPUTS ----------------
st.sidebar.header("🛠️ Design Inputs")

rc = st.sidebar.number_input("Range (miles)", value=1265.8)
pax = st.sidebar.number_input("Passengers", value=34)

ld = st.sidebar.number_input("L/D", value=13.0)
cp = st.sidebar.number_input("Cp", value=0.6)
eta = st.sidebar.number_input("ηp", value=0.85)

payload = pax * 205
crew = 615
attendants = 242.75

# Raymer constants (correct form)
A = 0.3774
B = 0.9647

# ---------------- FUNCTIONS ----------------
def fuel_fraction():
    """Full mission fuel fraction"""
    
    # Segments
    warmup = 0.990
    climb = 0.995
    cruise = math.exp(-rc / (375 * (eta / cp) * ld))
    loiter = 0.985
    landing = 0.995
    
    mff = warmup * climb * cruise * loiter * landing
    return mff

def weights(wto):
    
    mff = fuel_fraction()
    
    wf = wto * (1 - mff)
    
    we_calc = wto - wf - payload - crew - attendants
    
    # ✅ corrected equation
    we_allow = 10 ** (A + B * math.log10(wto))
    
    return we_calc, we_allow, wf, mff

# ---------------- SOLVER ----------------
def solve():
    
    wto = 40000.0
    
    for i in range(200):
        we_c, we_a, _, _ = weights(wto)
        
        error = we_a - we_c
        
        if abs(error) < 1:
            break
        
        # stable update
        wto = wto + error * 0.5
    
    return wto

# ---------------- RUN ----------------
if st.button("🚀 Solve Aircraft"):

    wto = solve()
    we_c, we_a, wf, mff = weights(wto)

    st.success(f"✅ Converged WTO = {wto:,.0f} lb")

    col1, col2, col3 = st.columns(3)
    col1.metric("WTO", f"{wto:,.0f}")
    col2.metric("Fuel Weight", f"{wf:,.0f}")
    col3.metric("Fuel Fraction", f"{mff:.3f}")

    # ---------------- GRAPH ----------------
    st.subheader("📈 Convergence Graph")

    w_range = np.linspace(wto*0.8, wto*1.2, 50)

    we_calc_list = []
    we_allow_list = []

    for w in w_range:
        wc, wa, _, _ = weights(w)
        we_calc_list.append(wc)
        we_allow_list.append(wa)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=w_range,
        y=we_calc_list,
        name="Calculated WE",
        mode='lines'
    ))

    fig.add_trace(go.Scatter(
        x=w_range,
        y=we_allow_list,
        name="Allowable WE",
        mode='lines'
    ))

    fig.add_vline(x=wto)

    fig.update_layout(
        template="plotly_dark",
        xaxis_title="Takeoff Weight (WTO)",
        yaxis_title="Empty Weight (WE)"
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("👈 اضغط Solve")
