# Vendee Globe Dashboard

This repository provides an interactive Streamlit dashboard that fetches and visualizes data from a custom Vendée Globe API. It allows you to monitor race progression and see the participants’ positions on a globe.

Features

- Interactive Race Progression: updates on each skipper’s distance to finish.
- Globe Visualization: Explore a 3D map view to track the real-time location of skippers.
- Automatic Refresh.

## Getting Started

### **1. Clone the repository**
```bash
git clone https://github.com/your-username/vendee-globe-dashboard.git
cd vendee-globe-dashboard
```

### **2. Create and activate a virtual environment with UV**

run : 
`curl -LsSf https://astral.sh/uv/install.sh | sh`

then run :   `uv sync`

finaly : `source .venv/bin/activate`

### **3. Start the app**

`streamlit run app.py`
