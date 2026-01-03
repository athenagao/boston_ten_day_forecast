# boston_ten_day_forecast



# Boston 10-Day Temperature Forecast (Neural Net / MLP)

**Live Demo:** https://bostontendayforecast-xpmmmxdksbm8sm7nurmnf2.streamlit.app/

A lightweight machine-learning baseline that trains an `MLPRegressor` on historical Boston weather (Open-Meteo Archive API) and predicts the next **10 days of daily mean temperature**.  
The model is trained in **°C** and displayed in **°F** for readability.

---

## What you can do in the demo
- Click **Run forecast** to fetch recent history, train the model, and generate a **10-day forecast**
- View:
  - Forecast table (°F)
  - Forecast plot (°F)
  - Held-out test error (MAE by horizon day)
  - Last ~365 days of daily mean temperature (°F)

---

## How it works (high level)
**Data**
- Source: Open-Meteo *Archive API* (hourly)
- Aggregation: hourly → daily features (means/sums)

**Features (daily)**
- temperature (mean, °C)
- relative humidity (mean)
- pressure MSL (mean)
- wind speed (mean)
- precipitation (sum)

**Supervised framing**
- Lookback window: **14 days**
- Forecast horizon: **10 days**
- Target: daily mean temperature (°C)

**Model**
- `StandardScaler` → `MLPRegressor(hidden_layer_sizes=(64, 32), relu, adam)`
- Train/test split: time-based (80/20)
- Metric: MAE per horizon day (reported in °F)

---

## 📁 Repository structure
```text
.
├── app.py                      # Streamlit app (web demo)
├── boston_ten_day_forecast.py   # Original CLI script
├── requirements.txt
└── README.md
