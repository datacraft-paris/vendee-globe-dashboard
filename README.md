# Vendee Globe Dashboard

This repository provides an interactive Streamlit dashboard that fetches and visualizes data from a custom Vendée Globe API. It allows you to monitor race progression and see the participants’ positions on a globe.

## Features

**Event Detection and Timeline** : Identify key events during the race, such as sudden change in speed, rank and visualize them on an interactive timeline.

**Globe View with Plotly** : View the geographical trajectory of all skippers on an interactive globe map.

**Foil Impact Analysis** : Compare metrics like vmg_24h or speed between boats with and without foils using dynamic visual analytics.

### Advanced Projects

1. **Globe View**

Visualize the real-time position and route of all skippers on a 3D globe or 2D map.
Integrate it with a time slider to display their progression throughout the race.

**Skills** : geographic plotting, projection control, data filtering

**Tech** : plotly.line_geo, projection=orthographic, hover_data, resample('D')

2. **Foil Impact Analysis**

Analyze the impact of foils on boat performance by comparing metrics such as `vmg_24h` or speed between foil-equipped and non-foil boats. Use dynamic visual analytics to uncover insights:

- **Mean evolution** of a selected performance metric over time.

- **Visual differences** between foil and non-foil boats, highlighted with filled areas.

- **Customizable metric selection** for comparison (default: `vmg_24h`).

Display results as an interactive Plotly chart with timeline comparisons and differential zones.

**Skills**: data grouping, dynamic metric selection, dual trace comparison 

**Tech**: `st.selectbox`, `groupby()`, `mean()`, `plotly.graph_objects`, conditional area chart

3. **Event Detection and Timeline**

Detect and highlight critical race events, such as:

- **Sudden drop in speed (potential incident)**

- **Big gain in rank**

- **Boat abandonment (no more data after a date)**

Display them as a timeline or alert list for rich narrative insight.

**Skills** : data slicing, condition detection, dynamic annotations

**Tech** : rolling(), diff(), conditional plots, timeline components

## Data Sources

This dashboard consumes data from the Vendée Globe API :

**GET /infos** → Static data: skipper names, boats, foil presence, colors, etc

**GET /race** → Live race data, updated in batches every 5 seconds

## Getting Started

### **1. Clone the repository**
```bash
git clone https://github.com/datacraft-paris/vendee-globe-dashboard.git
cd vendee-globe-dashboard
```

### **2. Create and activate a virtual environment with UV**

#### **Navigate to the Project Directory**

Before executing the following commands, ensure you are in the project directory and have checked out the correct branch:

```bash
git checkout <branch-name>
``` 
Replace `<branch-name>` with the branch you want to work on.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync
source .venv/bin/activate
```

### **3. Start the app**

Make sure the Vendée Globe API is running on http://127.0.0.1:8000 with :

```bash
uvicorn main:app --reload
```

Then start the dashboard in vendee-globe-dashboard/src/vendee_globe_dashboard/:

```bash
cd src/vendee_globe_dashboard/
streamlit run app.py
```
