import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh

from utils import fetch_dataframe, preprocess_race_data, merge_data 
from dashboard import display_globe_dashboard, display_progression_dashboard


st_autorefresh(interval=60000, limit=100, key="dashboard_autorefresh")
st.title("Interactive Vendée Globe Dashboard")
st.write("Choose a dashboard from the sidebar.")

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

df: pd.DataFrame = merge_data(df_race, df_infos)

dashboard_option: str = st.sidebar.radio(
    "Choose a dashboard",
    ("Race Progression", "Globe View")
)

if dashboard_option == "Race Progression":
    display_progression_dashboard(df)
elif dashboard_option == "Globe View":
    display_globe_dashboard(df)
