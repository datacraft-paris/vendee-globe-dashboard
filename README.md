# Vendee Globe Dashboard

This repository provides an interactive Streamlit dashboard that fetches and visualizes data from a custom Vendée Globe API. It allows you to monitor race progression and see the participants’ positions on a globe.

## Features

**Race Progression Viewer** : Visualize the evolution of each skipper's position and distance to finish, updated live from the API.

**Globe View with Plotly** : View the geographical trajectory of all skippers on an interactive globe map.

**Foil Impact Analysis** : Compare metrics like vmg_24h or speed between boats with and without foils using dynamic visual analytics.

**Auto-Refreshing Dashboard** : Refreshes automatically every 10 seconds to stay in sync with API batch updates.

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
