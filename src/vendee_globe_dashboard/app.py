import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh
from pandas.api.types import is_numeric_dtype
import ipywidgets as widgets

import plotly.graph_objects as go
from utils import fetch_dataframe, preprocess_race_data, merge_data 
from dashboard import display_globe_dashboard, display_progression_dashboard, impact_foil_on_column

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
tabs = st.tabs(["Race Progression", "Globe View", "Foil's Impact"])

# --- Page 1 : Progression ---
# Display the "Race Progression" dashboard in the first tab
with tabs[0]:
    display_progression_dashboard(df) # Function from dashboard.py

# --- Page 2 : Globe ---
# Display the "Globe View" dashboard in the second tab
with tabs[1]:
    display_globe_dashboard(df) # Function from dashboard.py

# --- Page 3 : Impact of Foil ---
# Display the "Foil's Impact" dashboard in the third tab
with tabs[2]:
    st.subheader("Impact of foil on a metric")

    # Identify numeric columns in the DataFrame
    num_cols = [col for col in df.columns if is_numeric_dtype(df[col])]
    
    # Set a default column for analysis (prefer 'vmg_24h' if available)
    default_col = 'vmg_24h' if 'vmg_24h' in num_cols else num_cols[0]

    # Dropdown to select a numeric column for analysis
    col = st.selectbox("Column:", num_cols, index=num_cols.index(default_col))
    
    # Dropdown to select an aggregation function (currently only 'mean')
    aggfunc = st.selectbox("Aggregation:", ['mean'], index=0)
    
    # Radio buttons to select the scale (currently only 'date')
    scale = st.radio("Scale:", ['date'], index=0)

    # Call the function to display the impact of foil on the selected column
    impact_foil_on_column(df=df, column=col, aggfunc=aggfunc, scale=scale) # Function from dashboard.py