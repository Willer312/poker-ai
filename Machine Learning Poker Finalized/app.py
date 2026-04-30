import streamlit as st
import joblib
import pandas as pd
import os

# -----------------------------
# Model download
# -----------------------------

@st.cache_resource
def load_model():
    return joblib.load("poker_complete_model.pkl")

model = load_model()

# -----------------------------
# Card mappings
# -----------------------------

rank_map = {
    "2":2,"3":3,"4":4,"5":5,"6":6,
    "7":7,"8":8,"9":9,
    "T":10,"J":11,"Q":12,"K":13,"A":14
}

suit_map = {
    "c":0,
    "d":1,
    "h":2,
    "s":3
}

stage_map = {
    "Preflop":0,
    "Flop":1,
    "Turn":2,
    "River":3
}

def parse_card(card):
    rank = rank_map[card[0].upper()]
    suit = suit_map[card[1].lower()]
    return rank, suit

# -----------------------------
# UI
# -----------------------------

st.title("Poker AI Assistant")
st.write("Enter cards like **Ah, Ks, Td**")

# Hole cards
hole1 = st.text_input("Hole Card 1")
hole2 = st.text_input("Hole Card 2")

# Flop
st.subheader("Flop")
flop1 = st.text_input("Flop Card 1")
flop2 = st.text_input("Flop Card 2")
flop3 = st.text_input("Flop Card 3")

# Turn
st.subheader("Turn")
turn = st.text_input("Turn Card")

# River
st.subheader("River")
river = st.text_input("River Card")

# -----------------------------
# Prediction
# -----------------------------

if st.button("Get AI Recommendation"):

    r1,s1 = parse_card(hole1)
    r2,s2 = parse_card(hole2)

    suited = int(s1 == s2)
    pair = int(r1 == r2)

    def get_card(card):
        if card == "":
            return 0,0
        return parse_card(card)

    f1r,f1s = get_card(flop1)
    f2r,f2s = get_card(flop2)
    f3r,f3s = get_card(flop3)

    tr,ts = get_card(turn)
    rr,rs = get_card(river)

    # determine stage
    if river != "":
        stage = "River"
    elif turn != "":
        stage = "Turn"
    elif flop1 != "":
        stage = "Flop"
    else:
        stage = "Preflop"

    sample = pd.DataFrame([{
        "rank1": r1,
        "suit1": s1,
        "rank2": r2,
        "suit2": s2,
        "suited": suited,
        "pair": pair,

        "flop1_rank": f1r,
        "flop1_suit": f1s,
        "flop2_rank": f2r,
        "flop2_suit": f2s,
        "flop3_rank": f3r,
        "flop3_suit": f3s,

        "turn_rank": tr,
        "turn_suit": ts,

        "river_rank": rr,
        "river_suit": rs,

        "stage": stage_map[stage]
    }])

    prediction = model.predict(sample)[0]

    st.subheader(f"Stage: {stage}")
    st.success(f"Recommended Action: {prediction.upper()}")
