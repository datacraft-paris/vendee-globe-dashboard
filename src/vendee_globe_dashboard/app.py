import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh

from utils import fetch_dataframe, preprocess_race_data, merge_data 
from dashboard import display_globe_dashboard, display_event_timeline, display_foil_impact

# --- Configuration ---
# Set the Streamlit page configuration
st.set_page_config(page_title="Interactive Vendée Globe Dashboard", layout="wide")

# Automatically refresh the dashboard every 10 seconds
st_autorefresh(interval=10000, key="dashboard_autorefresh")

# Set the title of the dashboard
st.title("Interactive Vendée Globe Dashboard")

# --- Data Loading ---
# Define API endpoints for fetching data
infos_api_url: str = "http://127.0.0.1:8000/infos"
race_api_url: str = "http://127.0.0.1:8000/race"

# Fetch and load the "infos" data from the API
try:
    df_infos: pd.DataFrame = fetch_dataframe(infos_api_url)
except Exception as e:
    # Display an error message if fetching fails and stop execution
    st.error(f"Error fetching infos data: {e}")
    st.stop()

# Fetch and preprocess the "race" data from the API
try:
    df_race: pd.DataFrame = fetch_dataframe(race_api_url) # Function from utils to fetch data
    df_race = preprocess_race_data(df_race) # Function from utils to preprocess data
except Exception as e:
    # Display an error message if fetching fails and stop execution
    st.error(f"Error fetching race data: {e}")
    st.stop()

# Merge the "infos" and "race" data into a single DataFrame using the function from utils
df: pd.DataFrame = merge_data(df_race, df_infos)

# --- Tabs / Navigation ---
# Create tabs for navigation between different dashboard views
tabs = st.tabs(["Event Timeline", "Globe View", "Impact of Foil"])

# --- Page 1 : Event Timeline ---
# Display the "Event Timeline" dashboard in the first tab
with tabs[0]:
    display_event_timeline(df)

# --- Page 2 : Globe ---
# Display the "Globe View" dashboard in the second tab
with tabs[1]:
    display_globe_dashboard(df)

# --- Page 3 : Impact of Foil ---
# Display the "Foil's Impact" dashboard in the third tab
with tabs[2]:
    display_foil_impact(df)
