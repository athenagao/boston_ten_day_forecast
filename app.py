import streamlit as st
from datetime import date, timedelta

import numpy as np
import pandas as pd
import requests
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor

LAT, LON = 42.3601, -71.0589
LOOKBACK_DAYS = 14
HORIZON_DAYS = 10
YEARS_OF_HISTORY_DEFAULT = 5
TIMEZONE = "America/New_York"

def c_to_f(x):
    return (x * 9 / 5) + 32

def fetch_openmeteo_daily(start_d: date, end_d: date) -> pd.DataFrame:
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": LAT,
        "longitude": LON,
        "start_date": start_d.isoformat(),
        "end_date": end_d.isoformat(),
        "hourly": ",".join([
            "temperature_2m",
            "relative_humidity_2m",
            "pressure_msl",
            "wind_speed_10m",
            "precipitation",
        ]),
        "timezone": TIMEZONE,
    }

    r = requests.get(url, params=params, timeout=60)
    r.raise_for_status()
    j = r.json()

    hourly = j.get("hourly", {})
    if "time" not in hourly:
        raise RuntimeError(f"Open-Meteo returned unexpected payload: keys={list(j.keys())}")

    df = pd.DataFrame({
        "time": pd.to_datetime(hourly["time"]),
        "temp_c": hourly.get("temperature_2m"),
        "rhum": hourly.get("relative_humidity_2m"),
        "pres": hourly.get("pressure_msl"),
        "wspd": hourly.get("wind_speed_10m"),
        "prcp": hourly.get("precipitation"),
    }).set_index("time")

    daily = pd.DataFrame({
        "temp_c": df["temp_c"].resample("D").mean(),
        "rhum": df["rhum"].resample("D").mean(),
        "pres": df["pres"].resample("D").mean(),
        "wspd": df["wspd"].resample("D").mean(),
        "prcp": df["prcp"].resample("D").sum(),
    }).dropna()

    return daily

def build_supervised(df: pd.DataFrame, feature_cols, target_col: str, lookback: int, horizon: int):
    values = df[feature_cols].to_numpy(dtype=float)
    target = df[target_col].to_numpy(dtype=float).reshape(-1)
    idx = df.index

    X_list, y_list, d_list = [], [], []
    for i in range(lookback, len(df) - horizon):
        X_list.append(values[i - lookback:i].reshape(-1))
        y_list.append(target[i:i + horizon].ravel())
        d_list.append(idx[i])

    return np.vstack(X_list), np.vstack(y_list), pd.to_datetime(pd.Index(d_list))

def format_date_axis(ax):
    locator = mdates.AutoDateLocator(minticks=4, maxticks=8)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(locator))

@st.cache_data(ttl=6 * 60 * 60, show_spinner=False)
def train_and_forecast(years_of_history: int, horizon_day: int):
    end_d = date.today() - timedelta(days=1)
    start_d = end_d - timedelta(days=365 * years_of_history)

    data = fetch_openmeteo_daily(start_d, end_d)
    data = data.interpolate(limit_direction="both").dropna()

feature_cols = ["temp_c", "rhum", "pres", "wspd", "prcp"]

cat > app.py << 'EOF'
import streamlit as st
from datetime import date, timedelta

import numpy as np
import pandas as pd
import requests
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor

LAT, LON = 42.3601, -71.0589
LOOKBACK_DAYS = 14
HORIZON_DAYS = 10
YEARS_OF_HISTORY_DEFAULT = 5
TIMEZONE = "America/New_York"

def c_to_f(x):
    return (x * 9 / 5) + 32

def fetch_openmeteo_daily(start_d: date, end_d: date) -> pd.DataFrame:
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": LAT,
        "longitude": LON,
        "start_date": start_d.isoformat(),
        "end_date": end_d.isoformat(),
        "hourly": ",".join([
            "temperature_2m",
            "relative_humidity_2m",
            "pressure_msl",
            "wind_speed_10m",
            "precipitation",
        ]),
        "timezone": TIMEZONE,
    }

    r = requests.get(url, params=params, timeout=60)
    r.raise_for_status()
    j = r.json()

    hourly = j.get("hourly", {})
    if "time" not in hourly:
        raise RuntimeError(f"Open-Meteo returned unexpected payload: keys={list(j.keys())}")

    df = pd.DataFrame({
        "time": pd.to_datetime(hourly["time"]),
        "temp_c": hourly.get("temperature_2m"),
        "rhum": hourly.get("relative_humidity_2m"),
        "pres": hourly.get("pressure_msl"),
        "wspd": hourly.get("wind_speed_10m"),
        "prcp": hourly.get("precipitation"),
    }).set_index("time")

    daily = pd.DataFrame({
        "temp_c": df["temp_c"].resample("D").mean(),
        "rhum": df["rhum"].resample("D").mean(),
        "pres": df["pres"].resample("D").mean(),
        "wspd": df["wspd"].resample("D").mean(),
        "prcp": df["prcp"].resample("D").sum(),
    }).dropna()

    return daily

def build_supervised(df: pd.DataFrame, feature_cols, target_col: str, lookback: int, horizon: int):
    values = df[feature_cols].to_numpy(dtype=float)
    target = df[target_col].to_numpy(dtype=float).reshape(-1)
    idx = df.index

    X_list, y_list, d_list = [], [], []
    for i in range(lookback, len(df) - horizon):
        X_list.append(values[i - lookback:i].reshape(-1))
        y_list.append(target[i:i + horizon].ravel())
        d_list.append(idx[i])

    return np.vstack(X_list), np.vstack(y_list), pd.to_datetime(pd.Index(d_list))

def format_date_axis(ax):
    locator = mdates.AutoDateLocator(minticks=4, maxticks=8)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(locator))

@st.cache_data(ttl=6 * 60 * 60, show_spinner=False)
def train_and_forecast(years_of_history: int, horizon_day: int):
    end_d = date.today() - timedelta(days=1)
    start_d = end_d - timedelta(days=365 * years_of_history)

    data = fetch_openmeteo_daily(start_d, end_d)
    data = data.interpolate(limit_direction="both").dropna()

    feature_cols = ["temp_c", "rhum", "pres", "wspd", "prcp"]
    target_col = "temp_c"

    X, y_c, y_start_dates = build_supervised(data, feature_cols, target_col, LOOKBACK_DAYS, HORIZON_DAYS)

    split = int(len(X) * 0.8)
    X_train, y_train_c = X[:split], y_c[:split]
    X_test,  y_test_c  = X[split:], y_c[split:]
    d_test = y_start_dates[split:]

    model = Pipeline([
        ("scaler", StandardScaler()),
        ("mlp", MLPRegressor(
            hidden_layer_sizes=(64, 32),
            activation="relu",
            solver="adam",
            max_iter=1200,
            early_stopping=True,
            n_iter_no_change=30,
            random_state=42
        ))
    ])
    model.fit(X_train, y_train_c)

    pred_test_c = model.predict(X_test)
    mae_c = np.mean(np.abs(pred_test_c - y_test_c), axis=0)
    mae_f = mae_c * 9 / 5

    latest = data.iloc[-LOOKBACK_DAYS:][feature_cols].to_numpy(dtype=float).reshape(1, -1)
    fc_c = model.predict(latest).ravel()
    fc_f = c_to_f(fc_c)

    forecast_dates = pd.date_range(
        start=data.index[-1] + pd.Timedelta(days=1),
        periods=HORIZON_DAYS,
        freq="D"
    )

    forecast_df = pd.DataFrame({"Date": forecast_dates.date, "Forecast (°F)": np.round(fc_f, 1)})
    mae_df = pd.DataFrame({"Horizon day": list(range(1, HORIZON_DAYS + 1)), "MAE (°F)": np.round(mae_f, 2)})

    k = int(horizon_day)
    j = k - 1
    N = min(250, len(y_test_c))
    d0 = pd.to_datetime(d_test[-N:])
    x_dates = d0 + pd.to_timedelta(j, unit="D")

    avp_df = pd.DataFrame({
        "Date": x_dates,
        "Actual (°F)": c_to_f(y_test_c[-N:, j]),
        "Predicted (°F)": c_to_f(pred_test_c[-N:, j]),
    })

    return data, forecast_df, mae_df, avp_df

st.set_page_config(page_title="Boston 10-Day Temp Forecast", page_icon="🌡️")
st.title("🌡️ Boston 10-Day Temperature Forecast (MLP)")
st.write("Trains an MLP on Open-Meteo archive data (°C internally), displays forecast in °F.")

years = st.slider("Years of history", 2, 10, YEARS_OF_HISTORY_DEFAULT, 1)
horizon_day = st.selectbox("Actual vs Predicted horizon day", list(range(1, 11)), index=0)

if st.button("Run forecast"):
    with st.spinner("Fetching data + training model..."):
        data, forecast_df, mae_df, avp_df = train_and_forecast(years, horizon_day)

    st.subheader("Forecast")
    st.dataframe(forecast_df, use_container_width=True)

    st.subheader("Forecast chart")
    fig1, ax1 = plt.subplots()
    ax1.plot(pd.to_datetime(forecast_df["Date"]), forecast_df["Forecast (°F)"], marker="o")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Temp (°F)")
    format_date_axis(ax1)
    fig1.autofmt_xdate()
    st.pyplot(fig1)

    st.subheader("Model error on held-out test set")
    st.dataframe(mae_df, use_container_width=True)

    st.subheader(f"Actual vs Predicted (Day +{horizon_day})")
    fig3, ax3 = plt.subplots()
    ax3.plot(avp_df["Date"], avp_df["Actual (°F)"], label="Actual")
    ax3.plot(avp_df["Date"], avp_df["Predicted (°F)"], label="Predicted")
    ax3.set_xlabel("Date")
    ax3.set_ylabel("Temp (°F)")
    format_date_axis(ax3)
    fig3.autofmt_xdate()
    ax3.legend()
    st.pyplot(fig3)

    st.subheader("Last ~365 days of daily mean temperature (°F)")
    hist = data.tail(365).copy()
    hist["temp_f"] = c_to_f(hist["temp_c"])
    fig2, ax2 = plt.subplots()
    ax2.plot(hist.index, hist["temp_f"])
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Temp (°F)")
    format_date_axis(ax2)
    fig2.autofmt_xdate()
    st.pyplot(fig2)
