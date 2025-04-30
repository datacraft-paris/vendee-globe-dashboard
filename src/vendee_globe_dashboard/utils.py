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
    response = requests.get(url)
    response.raise_for_status()
    data: Any = response.json()
    return pd.DataFrame(data)


def preprocess_race_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess race data by converting the 'date' column to datetime.
    
    Args:
        df (pd.DataFrame): The race DataFrame.
    
    Returns:
        pd.DataFrame: The processed DataFrame.
    """
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])
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
        return pd.merge(df_race, df_infos, on="skipper", how="left")
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
    if (dt.day == 1) or (dt == timeframe[0]):
        return dt.strftime('%b')
    elif ((dt.day % 5) == 0) or (dt == timeframe[-1]):
        return dt.strftime('%d')
    return ''