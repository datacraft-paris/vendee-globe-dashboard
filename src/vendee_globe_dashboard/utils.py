import streamlit as st
import requests
import pandas as pd
from typing import Any

def fetch_dataframe(url: str) -> pd.DataFrame:
    """
    Fetch JSON data from a given URL and return it as a pandas DataFrame.
    
    Args:
        url (str): The URL to fetch data from.
    
    Returns:
        pd.DataFrame: DataFrame created from the JSON response.
    
    Raises:
        requests.HTTPError: If the HTTP request returns an error status.
    """

    response = requests.get(url)  # Send a GET request to the specified URL
    data = response.json()  # Parse the JSON response into a Python object

    # Si data est un dict ou vide, afficher un message et retourner un DataFrame vide
    if not isinstance(data, list) or not data:
        st.info("✅ Fin de la course : plus de données à afficher.")
        st.stop()

    return pd.DataFrame(data)  # Convert the parsed JSON data into a pandas DataFrame and return it


def preprocess_race_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess race data by converting the 'date' column to datetime.
    
    Args:
        df (pd.DataFrame): The race DataFrame.
    
    Returns:
        pd.DataFrame: The processed DataFrame.
    """
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])  # Convert the 'date' column to datetime format
    return df


def merge_data(df_race: pd.DataFrame, df_infos: pd.DataFrame) -> pd.DataFrame:
    """
    Merge race and info DataFrames on the 'skipper' column.
    
    Args:
        df_race (pd.DataFrame): Race data.
        df_infos (pd.DataFrame): Static info data.
    
    Returns:
        pd.DataFrame: The merged DataFrame.
    """
    if "skipper" in df_race.columns and "skipper" in df_infos.columns:
        return pd.merge(df_race, df_infos, on="skipper", how="left")  # Merge the two DataFrames on the 'skipper' column using a left join
    return df_race.copy()

def format_pretty_date(dt: pd.Timestamp, timeframe: pd.DatetimeIndex) -> str:
    """
    Format a date into a short string based on the given timeframe.
    
    Args:
        dt (pd.Timestamp): The date to format.
        timeframe (pd.DatetimeIndex): A datetime index for reference.
    
    Returns:
        str: The formatted date string.
    """
    if (dt.day == 1) or (dt == timeframe[0]):  # Check if the date is the first day of the month or the first date in the timeframe
        return dt.strftime('%b')  # Return the abbreviated month name (e.g., 'Jan', 'Feb')
    elif ((dt.day % 5) == 0) or (dt == timeframe[-1]):  # Check if the day is a multiple of 5 or the last date in the timeframe
        return dt.strftime('%d')  # Return the day of the month as a zero-padded string (e.g., '05', '10')
    return ''
