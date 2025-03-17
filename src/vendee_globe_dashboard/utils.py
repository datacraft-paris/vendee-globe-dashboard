import requests
import pandas as pd
from typing import List

def fetch_dataframe(url: str) -> pd.DataFrame:
    """
    Fetch JSON data from a given URL and return it as a pandas DataFrame.
    
    Args:
        url (str): The URL to fetch data from.
    
    Returns:
        pd.DataFrame: DataFrame created from the JSON response.
    
    Raises:
        requests.HTTPError: If the HTTP request returned an unsuccessful status code.
    """
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return pd.DataFrame(data)


def preprocess_race_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess the race data by converting the 'date' column to datetime.
    
    Args:
        df (pd.DataFrame): The race DataFrame.
    
    Returns:
        pd.DataFrame: The processed DataFrame with 'date' as datetime.
    """
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])
    return df


def merge_data(df_race: pd.DataFrame, df_infos: pd.DataFrame) -> pd.DataFrame:
    """
    Merge the race and infos DataFrames on the 'skipper' column.
    
    Args:
        df_race (pd.DataFrame): Race data.
        df_infos (pd.DataFrame): Static info data.
    
    Returns:
        pd.DataFrame: Merged DataFrame.
    """
    if "skipper" in df_race.columns and "skipper" in df_infos.columns:
        return pd.merge(df_race, df_infos, on="skipper", how="left")
    return df_race.copy()


def get_filtered_by_batch(df: pd.DataFrame, start_batch: int, end_batch: int) -> pd.DataFrame:
    """
    Filter the DataFrame based on a batch range.
    
    Args:
        df (pd.DataFrame): The DataFrame to filter.
        start_batch (int): The starting batch number.
        end_batch (int): The ending batch number.
    
    Returns:
        pd.DataFrame: Filtered DataFrame.
    """
    if "batch" in df.columns:
        return df[df["batch"].between(start_batch, end_batch)]
    return df.copy()


def format_pretty_date(dt: pd.Timestamp, timeframe: pd.DatetimeIndex) -> str:
    """
    Format a date into a short string based on the given timeframe.
    
    Args:
        dt (pd.Timestamp): The date to format.
        timeframe (pd.DatetimeIndex): A datetime index used for reference.
    
    Returns:
        str: Formatted date string.
    """
    if (dt.day == 1) or (dt == timeframe[0]):
        return dt.strftime('%b')
    elif ((dt.day % 5) == 0) or (dt == timeframe[-1]):
        return dt.strftime('%d')
    return ''

def get_skippers_for_globe(df: pd.DataFrame, start: int, stop: int) -> List[str]:
    """
    Return a list of skippers sorted by 'distance_to_finish', sliced between start and stop indices.
    
    Args:
        df (pd.DataFrame): The merged DataFrame.
        start (int): Start index.
        stop (int): Stop index.
    
    Returns:
        List[str]: List of skipper names.
    """
    df_sorted = df.sort_values("distance_to_finish")
    return list(df_sorted["skipper"].unique()[start:stop])
