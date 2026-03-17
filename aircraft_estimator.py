import streamlit as st
import math
import numpy as np
import pandas as pd
import io

# ------------------ PAGE ------------------
st.set_page_config(page_title="Aircraft Design Tool", layout="wide")

st.title("✈️ Aircraft Design Tool")
st.markdown("### Weight Estimation & Engineering Analysis")

# ------------------ SIDEBAR ------------------
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

    # Fuel fraction
    W5_W4 = 1 / math.exp(Rc / (375 * (np_eff / Cp) * LD))
    Mff = 0.99*0.995*0.995*0.985*W5_W4*0.97*0.985*0.995

    WF = WTO * (1 - Mff)
    WE = WTO - WF - payload - crew - att
    WE_allow = 10 ** ((math.log10(WTO) - A) / B)
    diff = WE_allow - WE

    # ------------------ RESULTS ------------------
    st.subheader("📊 Results")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("WTO (lb)", f"{WTO:,.0f}")
    col2.metric("Fuel (lb)", f"{WF:,.0f}")
    col3.metric("Empty Weight (lb)", f"{WE:,.0f}")
    col4.metric("Allowable WE (lb)", f"{WE_allow:,.0f}")

    st.markdown("---")

    col5, col6 = st.columns(2)
    col5.metric("Fuel Fraction", f"{Mff:.4f}")
    col6.metric("Difference", f"{diff:.2f}")

    # ------------------ GRAPH 1 ------------------
    st.subheader("📈 Effect of Range on Weight")

    ranges = np.linspace(200, 2000, 50)
    weights = []

    for r in ranges:
        W5_W4 = 1 / math.exp(r / (375 * (np_eff / Cp) * LD))
        Mff_temp = 0.99*0.995*0.995*0.985*W5_W4*0.97*0.985*0.995
        WF_temp = WTO * (1 - Mff_temp)
        WE_temp = WTO - WF_temp - payload - crew - att
        weights.append(WE_temp)

    df = pd.DataFrame({
        "Range (mile)": ranges,
        "Empty Weight (lb)": weights
    })

    st.line_chart(df.set_index("Range (mile)"))

    st.caption("X-axis: Range (mile) | Y-axis: Empty Weight (lb)")

    # ------------------ GRAPH 2 ------------------
    st.subheader("📈 Sensitivity to L/D")

    LD_vals = np.linspace(8, 20, 40)
    WTO_vals = []

    for ld in LD_vals:
        W5_W4 = 1 / math.exp(Rc / (375 * (np_eff / Cp) * ld))
        Mff_temp = 0.99*0.995*0.995*0.985*W5_W4*0.97*0.985*0.995

        WTO_temp = WTO
        for _ in range(20):
            WF_temp = WTO_temp * (1 - Mff_temp)
            WE_temp = WTO_temp - WF_temp - payload - crew - att
            WE_allow_temp = 10 ** ((math.log10(WTO_temp) - A) / B)
            WTO_temp += (WE_allow_temp - WE_temp) * 0.5

        WTO_vals.append(WTO_temp)

    df2 = pd.DataFrame({
        "L/D": LD_vals,
        "WTO (lb)": WTO_vals
    })

    st.line_chart(df2.set_index("L/D"))

    st.caption("X-axis: L/D | Y-axis: Takeoff Weight (lb)")

    # ------------------ CONTOUR (بديل بسيط) ------------------
    st.subheader("🎯 Sensitivity Table (بدل Contour)")

    table_data = []

    for ld in [10, 12, 14, 16, 18]:
        for r in [500, 1000, 1500]:
            W5_W4 = 1 / math.exp(r / (375 * (np_eff / Cp) * ld))
            Mff_temp = 0.99*0.995*0.995*0.985*W5_W4*0.97*0.985*0.995
            WTO_temp = WTO * (1 - Mff_temp)
            table_data.append([ld, r, round(WTO_temp, 0)])

    df3 = pd.DataFrame(table_data, columns=["L/D", "Range", "WTO"])
    st.dataframe(df3)

    # ------------------ PDF ------------------
    st.subheader("📄 Export Report")

    if st.button("Generate PDF"):

        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer)
        styles = getSampleStyleSheet()

        content = []

        content.append(Paragraph("Aircraft Design Report", styles["Title"]))
        content.append(Spacer(1, 10))

        content.append(Paragraph(
            "This report presents preliminary aircraft weight estimation results. "
            "The analysis evaluates how mission parameters affect total and empty weight.",
            styles["Normal"]
        ))

        content.append(Spacer(1, 10))
        content.append(Paragraph(f"WTO: {WTO:.2f} lb", styles["Normal"]))
        content.append(Paragraph(f"Empty Weight: {WE:.2f} lb", styles["Normal"]))
        content.append(Paragraph(f"Fuel Fraction: {Mff:.4f}", styles["Normal"]))

        doc.build(content)

        st.download_button(
            "📥 Download PDF",
            buffer.getvalue(),
            file_name="report.pdf",
            mime="application/pdf"
        )

else:
    st.info("👈 Enter inputs and click Run Analysis")
