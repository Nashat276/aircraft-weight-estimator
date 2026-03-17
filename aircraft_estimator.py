import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import math
import io

# ---------------- CONFIG ----------------
st.set_page_config(page_title="AeroNova Simulator X", page_icon="✈", layout="wide")

# ---------------- STYLE ----------------
st.markdown("""
<style>
body {background-color:#0A1628;color:white}
.main-title {text-align:center;font-size:28px;font-weight:bold;color:#00D4FF}
</style>
""", unsafe_allow_html=True)

# ---------------- FUNCTIONS ----------------
def compute_mission(p):
    Wpl = p['n_pax'] * (p['w_pax'] + p['w_bag'])
    Wcrew = p['n_crew'] * 205 + p['n_att'] * 200
    Wtfo = p['Wto_guess'] * p['Mtfo']

    Rc = p['range_nm'] * 1.15078
    W5 = 1 / math.exp(Rc / (375 * (p['np_c'] / p['Cp_c']) * p['LD_c']))

    Vm = p['V_lkts'] * 1.15078
    W6 = 1 / math.exp(p['E_l'] / (375 * (1 / Vm) * (p['np_l'] / p['Cp_l']) * p['LD_l']))

    fracs = {
        'Start': 0.99,
        'Taxi': 0.995,
        'Takeoff': 0.995,
        'Climb': 0.985,
        'Cruise': W5,
        'Loiter': W6,
        'Landing': 0.995
    }

    Mff = 1.0
    for v in fracs.values():
        Mff *= v

    WF = p['Wto_guess'] * (1 - Mff)
    WOE = p['Wto_guess'] - WF - Wpl
    WE = WOE - Wtfo - Wcrew

    WE_all = 10 ** ((math.log10(p['Wto_guess']) - p['A']) / p['B'])

    return {
        'Wpl': Wpl,
        'WF': WF,
        'Mff': Mff,
        'WE': WE,
        'WE_all': WE_all,
        'diff': WE_all - WE
    }


def solve_wto(p):
    lo, hi = 5000, 200000

    for _ in range(100):
        mid = (lo + hi) / 2
        p['Wto_guess'] = mid
        r = compute_mission(p)

        if abs(r['diff']) < 1:
            break

        if r['diff'] > 0:
            hi = mid
        else:
            lo = mid

    return mid, r


# ---------------- SIDEBAR ----------------
st.sidebar.header("Inputs")

n_pax = st.sidebar.slider("Passengers", 10, 100, 30)
range_nm = st.sidebar.slider("Range (nm)", 200, 3000, 1000)
LD_c = st.sidebar.slider("L/D", 8, 20, 12)
Cp_c = st.sidebar.slider("Cp", 0.3, 1.0, 0.6)

# ---------------- PARAMETERS ----------------
P = dict(
    n_pax=n_pax,
    w_pax=175,
    w_bag=30,
    n_crew=2,
    n_att=1,
    Mtfo=0.005,
    range_nm=range_nm,
    V_lkts=250,
    LD_c=LD_c,
    Cp_c=Cp_c,
    np_c=0.85,
    E_l=0.75,
    LD_l=16,
    Cp_l=0.65,
    np_l=0.77,
    A=0.3774,
    B=0.9647,
    Wto_guess=50000
)

# ---------------- SOLVE ----------------
Wto, R = solve_wto(P)

# ---------------- UI ----------------
st.markdown('<div class="main-title">AERONOVA SIMULATOR</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

col1.metric("W_TO", f"{Wto:,.0f} lbs")
col2.metric("Fuel", f"{R['WF']:,.0f} lbs")
col3.metric("Payload", f"{R['Wpl']:,.0f} lbs")

# ---------------- PLOT ----------------
x = np.linspace(200, 3000, 30)
y = []

for r in x:
    P['range_nm'] = r
    w, _ = solve_wto(P)
    y.append(w)

fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y))

fig.update_layout(
    title="W_TO vs Range",
    xaxis_title="Range",
    yaxis_title="Weight"
)

st.plotly_chart(fig, use_container_width=True)
