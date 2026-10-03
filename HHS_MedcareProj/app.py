import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# PAGE CONFIGURATION
st.set_page_config(
    page_title="UAC Capacity & Care Load Analytics",
    layout="wide"
)

# LOAD DATA
@st.cache_data
def load_data():
    df = pd.read_csv("notebooks/Cleaned_HHS_Care_Dataset.csv")

    # Converting Date column to datetime
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # Removing rows where Date couldn't be parsed
    df = df.dropna(subset=["Date"])

    # Converting anomaly indicators to boolean
    df['Transfer_Exceeds_CBP'] = (
        df['Transfer_Exceeds_CBP'].astype(str).str.lower().isin(['true','1','yes'])
    )

    df['Discharge_Exceeds_HHS'] = (
        df['Discharge_Exceeds_HHS'].astype(str).str.lower().isin(['true','1','yes'])
    )

    #Reconstructing Binary Anomaly Flag
    df['Anomaly_Flag'] = (
        df['Transfer_Exceeds_CBP'] | df['Discharge_Exceeds_HHS'].astype(int)
    )

    return df

df = load_data()

# TITLE
st.title("System Capacity & Care Load Analytics")
st.subheader("Unaccompanied Children Care System")

st.markdown(
    """
    **Analytical dashboard for monitoring care load, inflow-outflow
    balance, capacity pressure, anomalies, and forecasting across
    the CBP–HHS care pipeline.**
    """
)

# SIDEBAR
st.sidebar.header("Dashboard Controls")

min_date = df["Date"].min()
max_date = df["Date"].max()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if len(date_range) == 2:

    start_date = pd.Timestamp(date_range[0])
    end_date = pd.Timestamp(date_range[1])

    filtered_df = df[
        (df["Date"] >= start_date)
        & (df["Date"] <= end_date)
    ].copy()

else:

    filtered_df = df.copy()


granularity = st.sidebar.selectbox(
    "Time Granularity",
    ["Daily", "Weekly", "Monthly"]
)


metric = st.sidebar.selectbox(
    "Primary Load Metric",
    [
        "HHS_Care",
        "CBP_Custody",
        "Total_System_Load"
    ]
)


metric_labels = {
    "HHS_Care": "HHS Care",
    "CBP_Custody": "CBP Custody",
    "Total_System_Load": "Total System Load"
}

# KPI CALCULATIONS
latest = filtered_df.iloc[-1]

average_hhs = filtered_df["HHS_Care"].mean()
maximum_hhs = filtered_df["HHS_Care"].max()

average_transfers = filtered_df["HHS_Transfers"].mean()
average_discharges = filtered_df["HHS_Discharges"].mean()

average_net_intake = filtered_df["Net_Intake"].mean()

positive_net = (
    filtered_df["Net_Intake"] > 0
).sum()

negative_net = (
    filtered_df["Net_Intake"] < 0
).sum()

anomaly_count = int(filtered_df["Anomaly_Flag"].sum())

anomaly_percentage = (
    anomaly_count / len(filtered_df) * 100
    if len(filtered_df) > 0
    else 0
)

# KPI CARDS
st.header("System Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Current HHS Care",
    f"{latest['HHS_Care']:,.0f}"
)

col2.metric(
    "Current CBP Custody",
    f"{latest['CBP_Custody']:,.0f}"
)

col3.metric(
    "Total System Load",
    f"{latest['Total_System_Load']:,.0f}"
)

col4.metric(
    "Current Net Intake",
    f"{latest['Net_Intake']:,.0f}"
)


col5, col6, col7, col8 = st.columns(4)

col5.metric(
    "Average HHS Care",
    f"{average_hhs:,.0f}"
)

col6.metric(
    "Maximum HHS Care",
    f"{maximum_hhs:,.0f}"
)

col7.metric(
    "Average Net Intake",
    f"{average_net_intake:,.1f}"
)

col8.metric(
    "Anomaly Rate",
    f"{anomaly_percentage:.2f}%"
)

# TIME AGGREGATION
if granularity == "Daily":

    plot_df = filtered_df.copy()

elif granularity == "Weekly":

    plot_df = (
        filtered_df
        .set_index("Date")
        .resample("W-SUN")
        .agg({
            "HHS_Care": "mean",
            "CBP_Custody": "mean",
            "Total_System_Load": "mean",
            "HHS_Transfers": "sum",
            "HHS_Discharges": "sum",
            "Net_Intake": "sum"
        })
        .reset_index()
    )

else:

    plot_df = (
        filtered_df
        .set_index("Date")
        .resample("ME")
        .agg({
            "HHS_Care": "mean",
            "CBP_Custody": "mean",
            "Total_System_Load": "mean",
            "HHS_Transfers": "sum",
            "HHS_Discharges": "sum",
            "Net_Intake": "sum"
        })
        .reset_index()
    )

# SYSTEM LOAD TREND
st.header("System Load Trends")

fig = px.line(
    plot_df,
    x="Date",
    y=metric,
    title=f"{metric_labels[metric]} Over Time",
    labels={
        "Date": "Date",
        metric: metric_labels[metric]
    }
)

fig.update_layout(
    hovermode="x unified",
    height=500
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# CBP VS HHS
# ============================================================

st.header("CBP vs HHS Care Load")

comparison_df = plot_df[
    ["Date", "CBP_Custody", "HHS_Care"]
].melt(
    id_vars="Date",
    var_name="System",
    value_name="Children"
)

comparison_df["System"] = comparison_df["System"].map({
    "CBP_Custody": "CBP Custody",
    "HHS_Care": "HHS Care"
})


fig = px.line(
    comparison_df,
    x="Date",
    y="Children",
    color="System",
    title="CBP Custody vs HHS Care Load",
    labels={
        "Date": "Date",
        "Children": "Children Under Care",
        "System": "Care System"
    }
)

fig.update_layout(
    hovermode="x unified",
    height=500
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# TRANSFERS VS DISCHARGES
# ============================================================

st.header("Care Pipeline Flows")

flow_df = plot_df[
    [
        "Date",
        "HHS_Transfers",
        "HHS_Discharges"
    ]
].melt(
    id_vars="Date",
    var_name="Flow",
    value_name="Children"
)

flow_df["Flow"] = flow_df["Flow"].map({
    "HHS_Transfers": "HHS Transfers",
    "HHS_Discharges": "HHS Discharges"
})


fig = px.line(
    flow_df,
    x="Date",
    y="Children",
    color="Flow",
    title="HHS Transfers vs Discharges",
    labels={
        "Date": "Date",
        "Children": "Children",
        "Flow": "Flow Type"
    }
)

fig.update_layout(
    hovermode="x unified",
    height=500
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# NET INTAKE
st.header("Net Intake & Capacity Pressure")

fig = px.bar(
    plot_df,
    x="Date",
    y="Net_Intake",
    title="Net Intake Pressure",
    labels={
        "Date": "Date",
        "Net_Intake": "Net Intake"
    }
)

fig.add_hline(
    y=0,
    line_dash="dash"
)

fig.update_layout(
    height=500
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# CUMULATIVE NET INTAKE
cumulative_df = filtered_df.copy()

cumulative_df["Cumulative_Net_Intake"] = (
    cumulative_df["Net_Intake"].cumsum()
)


fig = px.line(
    cumulative_df,
    x="Date",
    y="Cumulative_Net_Intake",
    title="Cumulative Net Intake",
    labels={
        "Date": "Date",
        "Cumulative_Net_Intake": "Cumulative Net Intake"
    }
)

fig.update_layout(
    hovermode="x unified",
    height=450
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ROLLING CAPACITY LOAD
st.header("Capacity Stress Monitoring")

rolling_df = filtered_df.copy()

rolling_df["Rolling_7D_Load"] = (
    rolling_df["Total_System_Load"]
    .rolling(7)
    .mean()
)

rolling_df["Rolling_14D_Load"] = (
    rolling_df["Total_System_Load"]
    .rolling(14)
    .mean()
)


rolling_long = rolling_df[
    [
        "Date",
        "Total_System_Load",
        "Rolling_7D_Load",
        "Rolling_14D_Load"
    ]
].melt(
    id_vars="Date",
    var_name="Metric",
    value_name="Load"
)


rolling_long["Metric"] = rolling_long["Metric"].map({
    "Total_System_Load": "Total System Load",
    "Rolling_7D_Load": "7-Day Rolling Load",
    "Rolling_14D_Load": "14-Day Rolling Load"
})


fig = px.line(
    rolling_long,
    x="Date",
    y="Load",
    color="Metric",
    title="System Load and Rolling Averages",
    labels={
        "Date": "Date",
        "Load": "Children",
        "Metric": "Metric"
    }
)

fig.update_layout(
    hovermode="x unified",
    height=500
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ANOMALIES
st.header("Data Quality & Operational Anomalies")

anomalies = filtered_df[
    filtered_df["Anomaly_Flag"] == 1
].copy()


if len(anomalies) > 0:

    st.warning(
        f"{len(anomalies)} anomalous observations detected "
        f"within the selected period."
    )

    st.dataframe(
        anomalies[
            [
                "Date",
                "CBP_Custody",
                "HHS_Transfers",
                "HHS_Care",
                "HHS_Discharges",
                "Transfer_Exceeds_CBP",
                "Discharge_Exceeds_HHS"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

else:

    st.success(
        "No flagged operational anomalies in the selected period."
    )

# FORECASTING
st.header("HHS Care Load Forecast")

st.markdown(
    """
    Forecasting compares a persistence-based **Naive baseline**,
    **SARIMA**, and **XGBoost** using a chronological test period.
    """
)


# Weekly forecasting data
weekly = (
    df
    .set_index("Date")
    .resample("W-SUN")
    .agg({
        "HHS_Care": "mean"
    })
    .reset_index()
)


# Naive test-period forecast
split_index = int(len(weekly) * 0.80)

forecast_train = weekly.iloc[:split_index].copy()
forecast_test = weekly.iloc[split_index:].copy()

forecast_test["Naive_Forecast"] = (
    weekly["HHS_Care"]
    .shift(1)
    .iloc[forecast_test.index]
)


forecast_plot = forecast_test.copy()

forecast_long = forecast_plot[
    [
        "Date",
        "HHS_Care",
        "Naive_Forecast"
    ]
].melt(
    id_vars="Date",
    var_name="Series",
    value_name="HHS Care Load"
)


forecast_long["Series"] = forecast_long["Series"].map({
    "HHS_Care": "Actual HHS Care",
    "Naive_Forecast": "Naive Forecast"
})


fig = px.line(
    forecast_long,
    x="Date",
    y="HHS Care Load",
    color="Series",
    title="Actual vs Naive HHS Care Forecast",
    labels={
        "Date": "Week",
        "HHS Care Load": "Children",
        "Series": "Series"
    }
)

fig.update_layout(
    hovermode="x unified",
    height=500
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# Forecast metrics
forecast_results = pd.DataFrame({
    "Model": [
        "Naive Baseline",
        "SARIMA",
        "XGBoost"
    ],
    "MAE": [
        37.21,
        229.75,
        192.99
    ],
    "RMSE": [
        45.16,
        283.74,
        231.10
    ],
    "MAPE (%)": [
        1.66,
        10.82,
        9.04
    ]
})


st.subheader("Forecast Model Performance")

st.dataframe(
    forecast_results.style.format({
        "MAE": "{:.2f}",
        "RMSE": "{:.2f}",
        "MAPE (%)": "{:.2f}%"
    }),
    use_container_width=True,
    hide_index=True
)


st.success(
    "Best-performing model: Naive Baseline "
    "(MAPE = 1.66%)"
)


# FUTURE FORECAST
st.subheader("Next 4 Weeks — Baseline Forecast")

latest_hhs = weekly["HHS_Care"].iloc[-1]

future_dates = pd.date_range(
    start=weekly["Date"].iloc[-1] + pd.Timedelta(days=7),
    periods=4,
    freq="W-SUN"
)

future_forecast = pd.DataFrame({
    "Date": future_dates,
    "Forecast_HHS_Care": latest_hhs
})


fig = px.line(
    future_forecast,
    x="Date",
    y="Forecast_HHS_Care",
    markers=True,
    title="Four-Week HHS Care Load Forecast",
    labels={
        "Date": "Week",
        "Forecast_HHS_Care": "Forecast HHS Care"
    }
)

fig.update_layout(
    height=400
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# Footer
st.divider()

st.caption(
    "System Capacity & Care Load Analytics for Unaccompanied Children | "
    "Analytical dashboard developed for healthcare capacity monitoring "
    "and forecasting."
)