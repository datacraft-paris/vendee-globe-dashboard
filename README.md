# vendee-globe-dashboard

Vendée Globe Dashboard is a Streamlit-based interactive dashboard that visualizes race data and skipper/boat information from the Vendée Globe API.
It offers real-time tracking, visual race progression, global mapping, and an analytical view of foil impact on performance.
🚀 Features

    Race Progression Viewer
    Visualize the evolution of each skipper's position and distance to finish, updated live from the API.

    Globe View with Plotly
    View the geographical trajectory of all skippers on an interactive globe map.

    Foil Impact Analysis
    Compare metrics like vmg_24h or speed between boats with and without foils using dynamic visual analytics.

    Auto-Refreshing Dashboard
    Refreshes automatically every 10 seconds to stay in sync with API batch updates.

📦 Installation
1. Create a project with uv

```bash
uv init name_project --lib
cd name_project
uv venv
source venv/bin/activate
```

Replace `name_project` with the name of your project.

2. Run the Dashboard

Make sure the Vendée Globe API is running on http://127.0.0.1:8000.

Then start the dashboard in name_project/src/name_project:

```bash
cd src/name_project
streamlit run app.py
```

📊 Available Views
🟩 Race Progression

Visualizes daily progress for each skipper using Matplotlib. Skippers are ranked based on their final distance to finish.

🌍 Globe View

An interactive Plotly map showing the real-time position and route of all skippers. Color-coded and zoomable.

🛠️ Foil Impact

Compare metrics (e.g., VMG, speed) between boats with and without foils over time.

📥 Data Sources

This dashboard consumes data from the Vendée Globe API:

    GET /infos → Static data: skipper names, boats, foil presence, colors

    GET /race → Live race data, updated in batches every 5 seconds
