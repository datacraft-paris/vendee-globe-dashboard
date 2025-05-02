# Vendee Globe Dashboard : Data Visualization Projects

This repository presents six ready-to-build project ideas based on the Vendée Globe API, which provides real-time and static data on skippers, boats, and race progression.
The projects are organized by difficulty level and aim to help you explore and visualize the race in creative and insightful ways.

## Choose Your Own Visualization Adventure

You can:

- **Pick a project based on your current skill level**

- **Mix and match ideas to build something original**

- **Use your imagination to design your own analysis using the rich Vendée Globe dataset**

### Easy Projects

1. **Real-Time Podium Display**

Display the current top 3 skippers based on distance_to_finish.
Show their names, boats, and how close they are to the finish line — perfect for a real-time race dashboard.

**Skills** : basic Streamlit layout and filtering

 **Tech** : st.metric, df.sort_values()


2. **Daily Distance Leaderboard**

Show a simple bar chart of distance to finish for all skippers on a selected day.
This snapshot helps visualize the spread of the fleet at any moment.

**Skills** : basic plotting with Plotly or Matplotlib

**Tech** : st.select_slider, px.bar, df[df['date'] == selected_date]


### Intermediate Projects

3. **Interactive Skipper Profile**

Let users select a skipper from a dropdown and view:

 - **Boat and skipper info**

- **Evolution of speed, rank, or distance**

- **Trajectory on a map**

This is a great way to focus on individual performance and storytelling.

**Skills** : interactivity with widgets, subsetting, simple plotting

**Tech** : st.selectbox, line_chart, scatter_geo


4. **Two-Skipper Comparison Tool**

Compare two skippers side-by-side on:

- **Speed over time**

- **Rank progression**

- **Distance left**

Display graphs and key metrics in parallel using st.columns() to make the comparison clear and engaging.

**Skills** : multi-filtering, conditional plotting, layout logic

**Tech** : Plotly, Streamlit layout components


### Advanced Projects

5. **Globe View**

Visualize the real-time position and route of all skippers on a 3D globe or 2D map.
Integrate it with a time slider to display their progression throughout the race.

**Skills** : geographic plotting, projection control, data filtering

**Tech** : plotly.line_geo, projection=orthographic, hover_data, resample('D')


6. **Event Detection and Timeline**

Detect and highlight critical race events, such as:

- **Sudden drop in speed (potential incident)**

- **Big gain in rank**

- **Boat abandonment (no more data after a date)**

Display them as a timeline or alert list for rich narrative insight.

**Skills** : data slicing, condition detection, dynamic annotations

**Tech** : rolling(), diff(), conditional plots, timeline components

Ready to Build

Choose the project that fits your interest and level or create your own!


## Installation
1. **Create a project with uv**

```bash
uv init name_project --lib
cd name_project
uv venv
source venv/bin/activate
```

Replace `name_project` with the name of your project.

2. **Run the Dashboard**

Make sure the Vendée Globe API is running on http://127.0.0.1:8000.

Then start the dashboard in name_project/src/name_project:

```bash
cd src/name_project
streamlit run app.py
```
