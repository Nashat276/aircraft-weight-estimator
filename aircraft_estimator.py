# زر الحساب
if st.button("🚀 Calculate"):

    # Payload
    Wpl = passengers * (passenger_weight + baggage_weight)

    # Debug (مهم)
    st.write("Inputs:", Rc, LD_cruise, Cp_cruise, np_cruise)

    # Mission fractions
    W1_W0 = 0.99
    W2_W1 = 0.995
    W3_W2 = 0.995
    W4_W3 = 0.985

    # Cruise
    W5_W4 = 1 / math.exp(Rc / (375 * (np_cruise / Cp_cruise) * LD_cruise))

    # Loiter
    W6_W5 = 1 / math.exp(E_loiter / (375 * (1 / V_loiter) * (np_loiter / Cp_loiter) * LD_loiter))

    W7_W6 = 0.985
    W8_W7 = 0.995

    # Total fuel fraction
    Mff = W1_W0 * W2_W1 * W3_W2 * W4_W3 * W5_W4 * W6_W5 * W7_W6 * W8_W7

    # Fuel weight
    WF = WTO_guess * (1 - Mff)

    # Weights
    WOE = WTO_guess - WF - Wpl
    WE = WOE - attendant_weight - crew_weight

    # ✅ IMPORTANT FIX
    WE_allow = math.exp((math.log(WTO_guess) - A) / B)

    diff = WE_allow - WE

    # Debug values
    st.write("W5/W4 =", W5_W4)
    st.write("W6/W5 =", W6_W5)
    st.write("Mff =", Mff)

    # Results
    st.write("Fuel Fraction:", Mff)
    st.write("Fuel Weight:", WF)
    st.write("Empty Weight:", WE)
    st.write("Allowable WE:", WE_allow)
    st.write("Difference:", diff)
