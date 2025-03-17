import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from typing import Optional

from utils import format_pretty_date, get_skippers_for_globe, get_filtered_by_batch


def generate_race_figure(df: pd.DataFrame) -> Optional[plt.Figure]:
    """
    Generate a Matplotlib figure showing the daily race progression.
    
    Groups data by skipper and date, and uses the 'distance_to_finish' column.
    
    Args:
        df (pd.DataFrame): The filtered race data.
    
    Returns:
        Optional[plt.Figure]: The generated figure, or None if an error occurs.
    """
    if "distance_to_finish" not in df.columns:
        st.error("Column 'distance_to_finish' not found in race data.")
        return None

    try:
        tab = df.groupby(["skipper", "date"])["distance_to_finish"].min().unstack("skipper")
    except KeyError as e:
        st.error(f"Missing key in data: {e}")
        return None

    _max = tab.max().max()
    tab = tab.fillna(_max)
    tab = tab.resample("D").min()
    tab = tab.reset_index(drop=True)
    tab.loc[0] = _max
    tab = tab.sort_values(tab.index[-1], ascending=False, axis=1)

    fig, ax = plt.subplots(figsize=(18, 10))
    fig.suptitle("Vendée Globe 2024-2025")
    ax.set_title("Daily Progress of Skippers (Distance To Finish)")
    colors = df.set_index("skipper")["color"].to_dict() if "color" in df.columns else {}

    for i, (skipper, ser) in enumerate(tab.items()):
        if ser.min() == ser.iloc[-1]:
            ax.plot(ser, [i] * len(ser), marker="^", color=colors.get(skipper, "black"))
        else:
            ax.plot(ser, [i] * len(ser), marker="^", lw=0, color=colors.get(skipper, "black"))
            ax.plot(ser.iloc[[0, -1]], [i, i], color=colors.get(skipper, "black"))

    timeframe_index = df.set_index("date").resample("D").size().index
    days = [format_pretty_date(dt, timeframe_index) for dt in timeframe_index]
    for i, x in enumerate(tab.iloc[:, -1]):
        ax.annotate(days[i], (x, tab.shape[1] - 0.5), fontsize=9)
    ax.set_xlabel("Distance To Finish (nautical miles)")
    ax.invert_xaxis()
    ax.set_yticks(range(len(tab.columns)))
    ax.set_yticklabels(tab.columns)
    return fig

def generate_globe_figure(df: pd.DataFrame, start: int, stop: int, projection: str = 'orthographic') -> px.line_geo:
    """
    Generate a Plotly geographic line chart for skippers in the specified rank range.
    
    Args:
        df (pd.DataFrame): The merged DataFrame.
        start (int): Starting rank index.
        stop (int): Ending rank index.
        projection (str): Map projection type.
    
    Returns:
        px.line_geo: The generated Plotly figure.
    """
    dt = df['date'].max().strftime('%d/%m/%Y %Hh')
    skippers = get_skippers_for_globe(df, start, stop)
    
    # Filter for selected skippers and sort by distance_to_finish and date
    df2 = df.loc[df['skipper'].isin(skippers)].copy()
    df2 = df2.sort_values(['distance_to_finish', 'date'])
    
    # Ensure 'rank' column exists; if not, create it as an empty column.
    if "rank" not in df2.columns:
        df2["rank"] = ""
    else:
        df2["rank"] = df2["rank"].astype(str)
    
    # Mark skippers as "abandon" if they don't have the latest date.
    last_dates = df2.groupby('skipper')['date'].max()
    ret_skippers = last_dates[last_dates != df2['date'].max()].index
    df2.loc[df2['skipper'].isin(ret_skippers), "rank"] = "abandon"

    fig = px.line_geo(
        df2,
        lat='latitude',
        lon='longitude',
        hover_name="skipper",
        hover_data={'skipper': False, 'voilier': True, 'rank': True},
        color='skipper',
        projection=projection
    )
    fig.update_geos(
        projection=dict(rotation=dict(lat=df2['latitude'].iloc[0], lon=df2['longitude'].iloc[0]))
    )
    fig.update_layout(
        showlegend=True,
        height=500,
        title_text=f'Vendée Globe as of {dt}<br />Rank {start+1} - {stop}',
        geo=dict(
            showland=True,
            showcountries=True,
            showocean=True,
            countrywidth=0.5,
            landcolor='tan',
            lakecolor='aliceblue',
            oceancolor='aliceblue',
            lonaxis=dict(
                showgrid=True,
                gridcolor='rgb(102, 102, 102)',
                gridwidth=0.5
            ),
            lataxis=dict(
                showgrid=True,
                gridcolor='rgb(102, 102, 102)',
                gridwidth=0.5
            )
        )
    )
    fig.update_layout(
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Rockwell"
        )
    )
    return fig


def display_progression_dashboard(df: pd.DataFrame) -> None:
    """
    Display the race progression dashboard using a Matplotlib chart.
    
    Args:
        df (pd.DataFrame): The merged DataFrame.
    """
    st.subheader("Race Progression")
    if "batch" in df.columns:
        min_batch = int(df["batch"].min())
        max_batch = int(df["batch"].max())
        if min_batch == max_batch:
            st.sidebar.info(f"Only one batch available: {min_batch}")
            start_batch = end_batch = min_batch
        else:
            start_batch, end_batch = st.sidebar.slider(
                "Select batch range",
                min_value=min_batch,
                max_value=max_batch,
                value=(min_batch, max_batch),
                step=1,
            )
        df_filtered = get_filtered_by_batch(df, start_batch, end_batch)
    else:
        st.sidebar.info("No batch information available.")
        df_filtered = df.copy()

    fig = generate_race_figure(df_filtered)
    if fig:
        st.pyplot(fig)


def display_globe_dashboard(df: pd.DataFrame) -> None:
    """
    Display the globe view dashboard using a Plotly geographic chart.
    
    Args:
        df (pd.DataFrame): The merged DataFrame.
    """
    st.subheader("Globe View")
    total_skippers: int = len(df["skipper"].unique())
    start_rank, stop_rank = st.sidebar.slider(
        "Select skippers rank range",
        min_value=0,
        max_value=total_skippers,
        value=(0, total_skippers),
        step=1,
    )
    fig = generate_globe_figure(df, start_rank, stop_rank)
    if fig:
        st.plotly_chart(fig, use_container_width=True)