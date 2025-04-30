import streamlit as st  # Streamlit for building the dashboard
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px  # Plotly Express for simple geographic visualizations
from typing import Literal, Optional
import matplotlib.pyplot as plt
import plotly.graph_objects as go

from utils import format_pretty_date  # Custom utility function for formatting dates


def generate_race_figure(df: pd.DataFrame) -> Optional[plt.Figure]:
    """
    Generate a Matplotlib figure showing the daily race progression.
    
    Groups data by skipper and date, using the 'distance_to_finish' column.

    Args:
        df (pd.DataFrame): The filtered race data.
    
    Returns:
        Optional[plt.Figure]: The generated figure, or None if an error occurs.
    """
    if "distance_to_finish" not in df.columns:  # Check if required column exists
        st.error("Column 'distance_to_finish' not found in race data.")
        return None

    try:
        # Group data by skipper and date, and get the minimum distance to finish
        tab = df.groupby(["skipper", "date"])["distance_to_finish"].min().unstack("skipper")
    except KeyError as e:  # Handle missing keys in the data
        st.error(f"Missing key in data: {e}")
        return None
    
    _max = tab.max().max()  # Get the maximum distance to fill missing values
    tab = tab.fillna(_max)  # Fill missing values with the maximum distance
    tab = tab.resample("D").min()  # Resample data to daily frequency
    tab = tab.reset_index(drop=True)  # Reset index for easier plotting
    tab.iloc[0] = _max  # Set the first row to the maximum distance
    tab = tab.sort_values(tab.index[-1], ascending=False, axis=1)  # Sort skippers by final distance

    fig, ax = plt.subplots(figsize=(18, 10))  # Create a Matplotlib figure
    fig.suptitle("Vendée Globe 2024-2025")  # Add a title to the figure
    ax.set_title("Daily Progress of Skippers (Distance To Finish)")  # Add a subtitle
    colors = df.set_index("skipper")["color"].to_dict() if "color" in df.columns else {}  # Map skipper colors

    for i, (skipper, ser) in enumerate(tab.items()):  # Plot each skipper's progress
        if ser.min() == ser.iloc[-1]:  # Check if the skipper has consistent progress
            ax.plot(ser, [i] * len(ser), marker="^", color=colors.get(skipper, "black"))
        else:
            ax.plot(ser, [i] * len(ser), marker="^", lw=0, color=colors.get(skipper, "black"))
            ax.plot(ser.iloc[[0, -1]], [i, i], color=colors.get(skipper, "black"))

    # Annotate the chart with formatted dates
    timeframe_index = df.set_index("date").resample("D").size().index
    days = [format_pretty_date(dt, timeframe_index) for dt in timeframe_index]
    for i, x in enumerate(tab.iloc[:, -1]):
        ax.annotate(days[i], (x, tab.shape[1] - 0.5), fontsize=9)
    ax.set_xlabel("Distance To Finish (nautical miles)")
    ax.invert_xaxis()  # Invert the x-axis for better visualization
    ax.set_yticks(range(len(tab.columns)))  # Set y-axis ticks
    ax.set_yticklabels(tab.columns)
    return fig


def generate_globe_figure_date(df: pd.DataFrame, projection: str = 'orthographic') -> px.line_geo:
    """
    Generate a Plotly geographic line chart for skippers based on a filtered date range.

    Args:
        df (pd.DataFrame): The filtered DataFrame for a specific date range.
        projection (str): Map projection type.
    
    Returns:
        px.line_geo: The generated Plotly figure.
    """
    dt = df['date'].max().strftime('%d/%m/%Y %Hh')  # Format the latest date for the title
    df2 = df.sort_values(['distance_to_finish', 'date']).copy()  # Sort data for plotting

    if "rank" not in df2.columns:  # Ensure 'rank' column exists
        df2["rank"] = ""
    else:
        df2["rank"] = df2["rank"].astype(str)  # Convert rank to string

    # Mark skippers as "abandon" if they don't have the latest date
    last_dates = df2.groupby('skipper')['date'].max()
    ret_skippers = last_dates[last_dates != df2['date'].max()].index # Identify skippers who abandoned
    df2.loc[df2['skipper'].isin(ret_skippers), "rank"] = "abandon"

    # Create a geographic line chart
    fig = px.line_geo(
        df2,
        lat='latitude',
        lon='longitude',
        hover_name="skipper",
        hover_data={'skipper': False, 'voilier': True, 'rank': True},
        color='skipper',
        projection=projection
    )
    # Update map projection and layout
    fig.update_geos(
        projection=dict(rotation=dict(lat=df2['latitude'].iloc[0], lon=df2['longitude'].iloc[0]))
    )
    fig.update_layout(
        showlegend=True,
        height=500,
        title_text=f'Vendée Globe as of {dt}',
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
    Display the race progression dashboard using a Matplotlib chart filtered by datetime.
        
    Args:
        df (pd.DataFrame): The merged DataFrame.
    """
    st.subheader("Race Progression")  # Add a section header
    if "date" in df.columns:  # Check if the 'date' column exists
        unique_datetimes = sorted(df["date"].unique())  # Get unique dates for filtering

        # Add a slider to select a date range
        start_dt, end_dt = st.select_slider(
            "Select datetime range",
            options=unique_datetimes,
            value=(unique_datetimes[0], unique_datetimes[-1]),
            format_func=lambda dt: dt.strftime("%m/%d/%Y %H:%M"),
            key="race_datetime_slider"
        )

        # Filter data based on the selected date range
        df_filtered = df[(df["date"] >= start_dt) & (df["date"] <= end_dt)]
    else:
        st.info("No datetime information available.")  # Inform the user if no date column exists
        df_filtered = df.copy()

    fig = generate_race_figure(df_filtered)  # Generate the race progression figure
    if fig:
        st.pyplot(fig)  # Display the figure in Streamlit


def display_globe_dashboard(df: pd.DataFrame) -> None:
    """
    Display the globe view dashboard using a Plotly geographic chart filtered by datetime.
        
    Args:
        df (pd.DataFrame): The merged DataFrame.
    """
    st.subheader("Globe View")  # Add a section header
    if "date" in df.columns:  # Check if the 'date' column exists
        unique_datetimes = sorted(df["date"].unique())  # Get unique dates for filtering

        # Add a slider to select a date range
        start_dt, end_dt = st.select_slider(
            "Select datetime range",
            options=unique_datetimes,
            value=(unique_datetimes[0], unique_datetimes[-1]),
            format_func=lambda dt: dt.strftime("%m/%d/%Y %H:%M"),
            key="globe_datetime_slider"
        )

        # Filter data based on the selected date range
        df_filtered = df[(df["date"] >= start_dt) & (df["date"] <= end_dt)]
    else:
        st.info("No datetime information available.")  # Inform the user if no date column exists
        df_filtered = df.copy()

    fig = generate_globe_figure_date(df_filtered)  # Generate the globe view figure
    if fig:
        st.plotly_chart(fig, use_container_width=True)  # Display the figure in Streamlit


def impact_foil_on_column(
    df: pd.DataFrame,
    column: str,
    aggfunc: Literal['mean'],
    scale: Literal['date']
) -> Optional[None]:
    """
    Displays a Plotly chart showing the impact of foils on a numerical metric
    over time or distance.
    
    Args:
        df (pd.DataFrame): Merged race and skipper data.
        column (str): Numerical column to analyze.
        aggfunc (str): Aggregation method (currently supports only 'mean').
        scale (str): X-axis scale, 'date'.

    Returns:
        None. Displays the chart in Streamlit.
    """
    # Data selection and preparation
    tab = df[[scale, 'foil', column]].copy().sort_values(scale) # Sort data by the selected scale
    tab['foil'] = tab['foil'].map({1: 'with foil', 0: 'without foil'})  # Map foil values to labels

    grouped = tab.groupby([scale, 'foil'])  # Group data by scale and foil status

    if aggfunc == 'mean':  # Apply the aggregation function
        tab = grouped.mean()
    else:
        raise ValueError(f"Unsupported aggregation function: {aggfunc}")  # Handle unsupported functions

    tab = tab.unstack().droplevel(0, axis=1)  # Reshape data for plotting

    # Extract data for the chart
    x = tab.index
    y_with = tab.get('with foil')
    y_without = tab.get('without foil')
    diff = y_with - y_without  # Calculate the difference between with and without foil

    # Create a Plotly figure
    fig = go.Figure()

    # Add traces for with foil, without foil, and the difference
    fig.add_trace(go.Scatter(x=x, y=y_with, mode='lines+markers', name='With foil'))
    fig.add_trace(go.Scatter(x=x, y=y_without, mode='lines+markers', name='Without foil'))
    fig.add_trace(go.Scatter(
        x=x,
        y=diff,
        fill='tozeroy',
        mode='none',
        name='Difference (with - without)',
        opacity=0.3,
        fillcolor='lightblue'
    ))

    # Update layout with titles and labels
    fig.update_layout(
        title=f'Impact of foil on "{column}" ({aggfunc})',
        xaxis_title=scale,
        yaxis_title=f"{column} ({aggfunc})",
        legend_title="Foil",
        template='plotly_white',
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)  # Display the chart in Streamlit
