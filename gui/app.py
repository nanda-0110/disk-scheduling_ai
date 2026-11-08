import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from engine.metrics import run_all
from ml.dataset import extract_features

st.set_page_config(page_title="AI Disk Scheduling", layout="wide")
st.title("AI-Based Disk Scheduling Simulator")


def parse_requests(text, disk_size):
    try:
        reqs = [int(x) for x in text.replace(",", " ").split()]
    except ValueError:
        return None, "Requests must be whole numbers."
    if not reqs:
        return None, "Enter at least one request."
    if any(r < 0 or r >= disk_size for r in reqs):
        return None, f"All requests must be between 0 and {disk_size - 1}."
    return reqs, None


def ai_predict(reqs, head):
    model, cols = joblib.load(ROOT / "ml" / "model.pkl")
    feats = pd.DataFrame([extract_features(reqs, head)])[cols]
    return model.predict(feats)[0]


st.sidebar.header("Input")
req_text = st.sidebar.text_area("Disk requests (comma or space separated)", "98, 183, 37, 122, 14, 124, 65, 67")
head = st.sidebar.number_input("Initial head position", min_value=0, value=53, step=1)
disk_size = st.sidebar.number_input("Disk size (tracks)", min_value=10, value=200, step=10)
direction = st.sidebar.selectbox("Direction (SCAN / C-SCAN)", ["right", "left"])
run = st.sidebar.button("Run simulation")

if run:
    reqs, error = parse_requests(req_text, disk_size)
    if error:
        st.error(error)
    elif head >= disk_size:
        st.error(f"Head position must be below {disk_size}.")
    else:
        summary = run_all(reqs, int(head), int(disk_size), direction)

        table = pd.DataFrame(
            {
                name: {
                    "Total seek": d["total_seek"],
                    "Avg seek": d["avg_seek"],
                    "Throughput": d["throughput"],
                }
                for name, d in summary.items()
            }
        ).T
        st.subheader("Performance metrics")
        st.dataframe(table, use_container_width=True)

        best_real = min(summary, key=lambda a: summary[a]["total_seek"])
        ai_pick = ai_predict(reqs, int(head))
        c1, c2, c3 = st.columns(3)
        c1.metric("AI predicted best", ai_pick)
        c2.metric("Actual best (lowest seek)", best_real)
        c3.metric("AI correct?", "Yes" if ai_pick == best_real else "No")

        st.subheader("Total seek time comparison")
        fig, ax = plt.subplots(figsize=(7, 3.5))
        names = list(summary.keys())
        totals = [summary[n]["total_seek"] for n in names]
        colors = ["tab:green" if n == ai_pick else "tab:blue" for n in names]
        ax.bar(names, totals, color=colors)
        ax.set_ylabel("Total seek time")
        ax.set_title("Green bar = AI pick")
        st.pyplot(fig)

        st.subheader("Head movement (service order)")
        cols = st.columns(2)
        for i, name in enumerate(names):
            path = [int(head)] + summary[name]["order"]
            fig, ax = plt.subplots(figsize=(5, 3))
            ax.plot(range(len(path)), path, marker="o")
            ax.set_title(name)
            ax.set_xlabel("Step")
            ax.set_ylabel("Track")
            cols[i % 2].pyplot(fig)
else:
    st.info("Enter requests in the sidebar and click **Run simulation**.")