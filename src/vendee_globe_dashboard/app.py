import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh

from utils import fetch_dataframe, preprocess_race_data, merge_data 
from dashboard import display_globe_dashboard, display_progression_dashboard

st.set_page_config(page_title="Interactive Vendée Globe Dashboard", layout="wide")

st_autorefresh(interval=60000, key="dashboard_autorefresh")

st.title("Interactive Vendée Globe Dashboard")

# API endpoints
infos_api_url: str = "http://127.0.0.1:8000/infos"
race_api_url: str = "http://127.0.0.1:8000/race"

try:
    df_infos: pd.DataFrame = fetch_dataframe(infos_api_url)
except Exception as e:
    st.error(f"Error fetching infos data: {e}")
    st.stop()

try:
    df_race: pd.DataFrame = fetch_dataframe(race_api_url)
    df_race = preprocess_race_data(df_race)
except Exception as e:
    st.error(f"Error fetching race data: {e}")
    st.stop()

# Merge static info with race data on the 'skipper' column
df: pd.DataFrame = merge_data(df_race, df_infos)

# Use top navigation via tabs for switching pages
tabs = st.tabs(["Race Progression", "Globe View"])
with tabs[0]:
    display_progression_dashboard(df)
with tabs[1]:
    display_globe_dashboard(df)