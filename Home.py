import streamlit as st

st.set_page_config(page_title="Home - EV Stations", page_icon="⚡", layout="centered")

st.title("EV Stations")
st.write("Welcome to the EV Stations multipage app. This home page gives a quick intro and a button to open the app page you added in the pages/ folder.")

st.markdown("---")
st.subheader("Get started")

if st.button("Open App"):
    try:
        st.switch_page("pages/app.py")
    except Exception:
        st.warning("Navigation to the app page is not available in this environment. Please use the sidebar to open the App page.")

st.info("You can also use the sidebar page picker to switch between pages.")
