import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="EV Expansion Helper", layout="wide")
st.title("Which country should we expand into next quarter?")
st.caption("Data refreshes once every night.")

@st.cache_data
def load_data():
    df = pd.read_csv("ev_stations_2025.csv", parse_dates=["date_added"])
    df = df[df["country"].notna()]
    df = df[df["num_connectors"].fillna(0) > 0]
    df["month"] = df["date_added"].dt.to_period("M").dt.to_timestamp()
    return df

df = load_data()

# ---------- 左侧边栏（Sidebar） ----------
st.sidebar.header("Filters")

countries = sorted(df["country"].unique())
default_index = countries.index("FR") if "FR" in countries else 0
selected = st.sidebar.selectbox(
    "Country to evaluate",
    countries,
    index=default_index,
)

# 第二个筛选器：连接器类型（示例，可按需删）
connector_options = ["ALL"] + sorted(
    df["connector_types"].dropna().str.split("|").explode().str.strip().unique()
)
connector_choice = st.sidebar.selectbox("Connector type", connector_options)

# 第三个控件：显示前 N 个国家
top_n = st.sidebar.slider("Show top N countries", 5, 20, 10)

st.sidebar.markdown("---")
st.sidebar.caption("Data source: ev_stations_2025.csv")

# ---------- 应用筛选 ----------
sub = df[df["country"] == selected]
if connector_choice != "ALL":
    sub = sub[sub["connector_types"].fillna("").str.contains(connector_choice)]

# ---------- 图 1 ----------
st.subheader("1. Existing stations by country")
counts = df.groupby("country")["id"].count().sort_values(ascending=False).head(top_n)
fig1, ax1 = plt.subplots(figsize=(10, 4))
counts.plot(kind="bar", ax=ax1, color="#4C78A8")
ax1.set_ylabel("Number of stations")
ax1.set_xlabel("")
st.pyplot(fig1)
st.caption("Shows which markets are already crowded and which are still empty.")

# ---------- 图 2 ----------
st.subheader(f"2. Monthly new stations in {selected}")
monthly = sub.groupby("month")["id"].count()
fig2, ax2 = plt.subplots(figsize=(10, 4))
monthly.plot(ax=ax2, marker="o", color="#F58518")
ax2.set_ylabel("New stations")
ax2.set_xlabel("")
st.pyplot(fig2)
st.caption("Shows whether this market is accelerating or already slowing down.")

# ---------- 图 3 ----------
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

# ---------- 结论 ----------
last_month_count = monthly.iloc[-1] if len(monthly) else 0
top_connector = types.index[0] if len(types) else "no data"
st.markdown(
    f"**{selected}** currently has **{len(sub)}** stations, "
    f"with **{last_month_count}** added in the most recent month. "
    f"The most common connector is **{top_connector}**."
)
