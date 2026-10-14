import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="EV Expansion Helper", layout="wide")

# (1) Title with team name
st.title("Qiu Yuxin — EV Expansion Helper")

# (2) One-line caption: who it's for + what decision it supports
st.caption(
    "For the European expansion manager at a charging network operator, "
    "to decide which country to prioritize for new stations next quarter."
)

# (6) Data period + intended refresh frequency
st.caption("Data period: 2025. Intended refresh frequency: once every night.")

@st.cache_data
def load_data():
    df = pd.read_csv("ev_stations_2025.csv", parse_dates=["date_added"])
    df = df[df["country"].notna()]
    df = df[df["num_connectors"].fillna(0) > 0]
    df["month"] = df["date_added"].dt.to_period("M").dt.to_timestamp()
    return df

df = load_data()

# (5) At least one filter the decision-maker would actually use
st.sidebar.header("Filters")
countries = sorted(df["country"].unique())
default_index = countries.index("FR") if "FR" in countries else 0
selected = st.sidebar.selectbox("Country to evaluate", countries, index=default_index)
top_n = st.sidebar.slider("Show top N countries", 5, 20, 10)

sub = df[df["country"] == selected]

# (3) A row of headline metrics with st.metric
c1, c2, c3, c4 = st.columns(4)
c1.metric("Stations in " + selected, f"{len(sub):,}")
c2.metric("Total countries", f"{df['country'].nunique()}")
c3.metric("Total stations", f"{len(df):,}")
c4.metric("Operators in " + selected, f"{sub['operator'].nunique()}")

# (4) At least one supporting chart
st.subheader("1. Existing stations by country")
counts = df.groupby("country")["id"].count().sort_values(ascending=False).head(top_n)
fig1, ax1 = plt.subplots(figsize=(10, 4))
counts.plot(kind="bar", ax=ax1, color="#4C78A8")
ax1.set_ylabel("Number of stations")
ax1.set_xlabel("")
st.pyplot(fig1)
st.caption("Shows which markets are already crowded and which are still empty.")

st.subheader(f"2. Monthly new stations in {selected}")
monthly = sub.groupby("month")["id"].count()
fig2, ax2 = plt.subplots(figsize=(10, 4))
monthly.plot(ax=ax2, marker="o", color="#F58518")
ax2.set_ylabel("New stations")
ax2.set_xlabel("")
st.pyplot(fig2)
st.caption("Shows whether this market is accelerating or already slowing down.")

st.subheader(f"3. Connector types in {selected}")
types = (
    sub["connector_types"].dropna()
    .str.split("|").explode().str.strip()
    .value_counts().head(8)
)
fig3, ax3 = plt.subplots(figsize=(10, 4))
types.plot(kind="barh", ax=ax3, color="#54A24B")
ax3.set_xlabel("Count")
st.pyplot(fig3)
st.caption("Helps decide which connector to build at new sites.")