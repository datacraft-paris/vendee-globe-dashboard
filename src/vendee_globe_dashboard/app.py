import streamlit as st
import requests
import pandas as pd


st.title("Dashboard Vendée Globe - Données Brutes")


api_url = "http://127.0.0.1:8000/race"

try:
    response = requests.get(api_url)
    response.raise_for_status()
    data = response.json()
except Exception as e:
    st.error(f"Erreur lors de la récupération des données : {e}")
    data = None


if data:
    st.subheader("Données JSON brutes")
    st.json(data)

    
    if isinstance(data, list):
        df = pd.DataFrame(data)
        st.subheader("Données sous forme de DataFrame")
        st.dataframe(df)
    elif isinstance(data, dict):
        st.write("Dictionnaire complet :", data)