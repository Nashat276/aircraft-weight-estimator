import streamlit as st
import math
import numpy as np
import pandas as pd
import io
import plotly.express as px
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
import tempfile

# ------------------ PAGE ------------------
st.set_page_config(page_title="Aircraft Design Pro", layout="wide")

st.title("✈️ Aircraft Design Cockpit")
st.markdown("### Engineering Analysis Tool")

# ------------------ INPUTS ------------------
st.sidebar.header("⚙️ Inputs")

passengers = st.sidebar.number_input("Passengers", value=34)
Rc = st.sidebar.number_input("Range (mile)", value=1265.0)
LD = st.sidebar.number_input("L/D", value=13.0)
Cp = st.sidebar.number_input("Cp", value=0.6)
np_eff = st.sidebar.number_input("ηp", value=0.85)
WTO = st.sidebar.number_input("WTO Guess", value=48550.0)

# Constants
A = 0.3774
B = 0.9647
payload = passengers * (175 + 30)
crew = 615
att = 242.75

# ------------------ RUN ------------------
if st.button("🚀 Run Analysis"):

    # ------------------ CALC ------------------
    W5_W4 = 1 / math.exp(Rc / (375 * (np_eff / Cp) * LD))
    Mff = 0.99*0.995*0.995*0.985*W5_W4*0.97*0.985*0.995

    WF = WTO * (1 - Mff)
    WE = WTO - WF - payload - crew - att
    WE_allow = 10 ** ((math.log10(WTO) - A) / B)

    # ------------------ RESULTS ------------------
    st.subheader("📊 Results")
    col1, col2, col3 = st.columns(3)
    col1.metric("WTO (lb)", f"{WTO:,.0f}")
    col2.metric("Empty Weight (lb)", f"{WE:,.0f}")
    col3.metric("Fuel Fraction", f"{Mff:.3f}")

    # ------------------ GRAPH 1 ------------------
    st.subheader("📈 Range vs Empty Weight")

    ranges = np.linspace(200, 2000, 50)
    weights = []

    for r in ranges:
        W5_W4 = 1 / math.exp(r / (375 * (np_eff / Cp) * LD))
        Mff_temp = 0.99*0.995*0.995*0.985*W5_W4*0.97*0.985*0.995
        WF_temp = WTO * (1 - Mff_temp)
        WE_temp = WTO - WF_temp - payload - crew - att
        weights.append(WE_temp)

    df = pd.DataFrame({"Range (mile)": ranges, "Empty Weight (lb)": weights})

    fig1 = px.line(
        df,
        x="Range (mile)",
        y="Empty Weight (lb)",
        title="Effect of Range on Weight"
    )

    st.plotly_chart(fig1, use_container_width=True)

    # ------------------ CONTOUR ------------------
    st.subheader("🎯 Contour Plot")

    LD_vals = np.linspace(8, 20, 25)
    R_vals = np.linspace(200, 2000, 25)

    Z = []
    for ld in LD_vals:
        row = []
        for r in R_vals:
            W5_W4 = 1 / math.exp(r / (375 * (np_eff / Cp) * ld))
            Mff_temp = 0.99*0.995*0.995*0.985*W5_W4*0.97*0.985*0.995
            WTO_temp = WTO * (1 - Mff_temp)
            row.append(WTO_temp)
        Z.append(row)

    fig2 = px.imshow(
        Z,
        x=R_vals,
        y=LD_vals,
        labels=dict(x="Range (mile)", y="L/D", color="WTO"),
        title="Sensitivity Contour"
    )

    st.plotly_chart(fig2, use_container_width=True)

    # ------------------ PDF ------------------
    st.subheader("📄 Export PDF")

    if st.button("Generate PDF"):

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer)
        styles = getSampleStyleSheet()

        content = []
        content.append(Paragraph("Aircraft Design Report", styles["Title"]))
        content.append(Spacer(1, 10))

        content.append(Paragraph(
            "This report explains how mission parameters affect aircraft weight.",
            styles["Normal"]
        ))

        content.append(Spacer(1, 10))
        content.append(Paragraph(f"WTO: {WTO:.2f} lb", styles["Normal"]))
        content.append(Paragraph(f"Empty Weight: {WE:.2f} lb", styles["Normal"]))

        # حفظ الرسم
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        fig1.write_image(tmp.name)

        content.append(Spacer(1, 10))
        content.append(Paragraph("Range vs Weight Graph", styles["Heading2"]))
        content.append(Image(tmp.name, width=400, height=250))

        doc.build(content)

        st.download_button(
            "📥 Download PDF",
            buffer.getvalue(),
            file_name="report.pdf"
        )

else:
    st.info("👈 اضغط Run Analysis")
