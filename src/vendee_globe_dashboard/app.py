import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh
from pandas.api.types import is_numeric_dtype
import ipywidgets as widgets

import plotly.graph_objects as go
from utils import fetch_dataframe, preprocess_race_data, merge_data 
from dashboard import display_globe_dashboard, display_progression_dashboard, impact_foil_on_column

# --- Configuration ---
st.set_page_config(page_title="Interactive Vendée Globe Dashboard", layout="wide")
st_autorefresh(interval=10000, key="dashboard_autorefresh")
st.title("Interactive Vendée Globe Dashboard")

# --- Chargement des données ---
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

# --- Tabs / Navigation ---
tabs = st.tabs(["Race Progression", "Globe View", "Foil's Impact"])

# --- Page 1 : Progression ---
with tabs[0]:
    display_progression_dashboard(df)

# --- Page 2 : Globe ---
with tabs[1]:
    display_globe_dashboard(df)

# --- Page 3 : Impact du foil ---
with tabs[2]:
    st.subheader("Impact du foil sur une métrique")

    # Colonnes numériques
    num_cols = [col for col in df.columns if is_numeric_dtype(df[col])]
    default_col = 'vmg_24h' if 'vmg_24h' in num_cols else num_cols[0]

    col = st.selectbox("Colonne :", num_cols, index=num_cols.index(default_col))
    aggfunc = st.selectbox("Agrégation :", ['mean'], index=0)
    scale = st.radio("Échelle :", ['date'], index=0)

    impact_foil_on_column(df=df, column=col, aggfunc=aggfunc, scale=scale)