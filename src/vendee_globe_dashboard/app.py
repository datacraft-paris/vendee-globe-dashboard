import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

st.title("Dashboard Interactif Vendée Globe")
st.write("Sélectionnez le dashboard à afficher dans la barre latérale.")


infos_api_url = "http://127.0.0.1:8000/infos"
race_api_url = "http://127.0.0.1:8000/race"


try:
    response_infos = requests.get(infos_api_url)
    response_infos.raise_for_status()
    data_infos = response_infos.json()
    df_infos = pd.DataFrame(data_infos)
except Exception as e:
    st.error(f"Erreur lors de la récupération des infos : {e}")
    st.stop()


try:
    response_race = requests.get(race_api_url)
    response_race.raise_for_status()
    data_race = response_race.json()
    df_race = pd.DataFrame(data_race)
    if "date" in df_race.columns:
        df_race["date"] = pd.to_datetime(df_race["date"])
except Exception as e:
    st.error(f"Erreur lors de la récupération des données de race : {e}")
    st.stop()


if "skipper" in df_race.columns and "skipper" in df_infos.columns:
    df = pd.merge(df_race, df_infos, on="skipper", how="left")
else:
    df = df_race.copy()


dashboard_option = st.sidebar.radio(
    "Choisissez le dashboard",
    ("Progression de la course", "Vue sur le globe")
)


if dashboard_option == "Progression de la course":
    st.subheader("Progression de la course")
    if "batch" in df.columns:
        min_batch = int(df["batch"].min())
        max_batch = int(df["batch"].max())
        if min_batch == max_batch:
            st.sidebar.info(f"Un seul batch disponible : {min_batch}")
            start_batch = end_batch = min_batch
        else:
            start_batch, end_batch = st.sidebar.slider(
                "Sélectionnez la plage de batchs",
                min_value=min_batch,
                max_value=max_batch,
                value=(min_batch, max_batch),
                step=1,
            )
        df_filtered = df[df["batch"].between(start_batch, end_batch)]
    else:
        st.sidebar.info("Aucune information de batch n'est disponible.")
        df_filtered = df.copy()

    def pretty_date(dt, timeframe):
        if (dt.day == 1) or (dt == timeframe[0]):
            return dt.strftime('%b')
        elif ((dt.day % 5) == 0) or (dt == timeframe[-1]):
            return dt.strftime('%d')
        return ''

    def show_race(df: pd.DataFrame):
        if "distance_to_finish" not in df.columns:
            st.error("La colonne 'distance_to_finish' n'existe pas dans les données de course.")
            return None

        try:
            tab = df.groupby(["skipper", "date"])["distance_to_finish"].min().unstack("skipper")
        except KeyError as e:
            st.error(f"Clé manquante dans les données : {e}")
            return None

        _max = tab.max().max()
        tab = tab.fillna(_max)
        tab = tab.resample("D").min()
        tab = tab.reset_index(drop=True)
        tab.loc[0] = _max
        tab = tab.sort_values(tab.index[-1], ascending=False, axis=1)

        fig, ax = plt.subplots(figsize=(18, 10))
        fig.suptitle("Vendée Globe 2024-2025")
        ax.set_title("Distance quotidienne parcourue par les skippers (Distance To Finish)")
        colors = df.set_index("skipper")["color"].to_dict() if "color" in df.columns else {}

        for i, (skipper, ser) in enumerate(tab.items()):
            if ser.min() == ser.iloc[-1]:
                ax.plot(ser, [i] * len(ser), marker="^", color=colors.get(skipper, "black"))
            else:
                ax.plot(ser, [i] * len(ser), marker="^", lw=0, color=colors.get(skipper, "black"))
                ax.plot(ser.iloc[[0, -1]], [i, i], color=colors.get(skipper, "black"))

        timeframe_index = df.set_index("date").resample("D").size().index
        days = [pretty_date(dt, timeframe_index) for dt in timeframe_index]
        for i, x in enumerate(tab.iloc[:, -1]):
            ax.annotate(days[i], (x, tab.shape[1]-0.5), fontsize=9)
        ax.set_xlabel("Distance To Finish (milles marins)")
        ax.invert_xaxis()
        ax.set_yticks(range(len(tab.columns)))
        ax.set_yticklabels(tab.columns)
        return fig

    fig1 = show_race(df_filtered)
    if fig1:
        st.pyplot(fig1)


elif dashboard_option == "Vue sur le globe":
    st.subheader("Vue sur le globe")
    def get_skippers(df: pd.DataFrame, start: int, stop: int):
        df_sorted = df.sort_values("distance_to_finish")
        unique_skippers = df_sorted["skipper"].unique()
        return unique_skippers[start:stop]

    total_skippers = len(df["skipper"].unique())
    start_rank, stop_rank = st.sidebar.slider(
        "Sélectionnez le rang des skippers",
        min_value=0,
        max_value=total_skippers,
        value=(0, total_skippers),
        step=1,
    )

    def show_globe(df, start, stop, projection='orthographic'):
        dt = df['date'].max().strftime('%d/%m/%Y %Hh')
        skippers = get_skippers(df, start, stop)
        df2 = (df.loc[lambda df_: df_.skipper.isin(skippers)]
                 .sort_values(['distance_to_finish', 'date'])
                 .astype({"rank": str})
              )
        last_skippers = df2.groupby('skipper')['date'].max()
        ret_skippers = last_skippers.loc[last_skippers != df2['date'].max()].index
        df2.loc[df2.skipper.isin(ret_skippers), "rank"] = "abandon"

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
            title_text=f'Vendée Globe au {dt}<br />rank {start+1} - {stop}',
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

    fig2 = show_globe(df, start_rank, stop_rank)
    if fig2:
        st.plotly_chart(fig2, use_container_width=True)