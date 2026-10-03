import pandas as pd
import plotly.express as px
import streamlit as st
from scipy.stats import f_oneway

# PAGE CONFIGURATION

st.set_page_config(
    page_title = "6G SMART FACTORY ANALYTICS",
    layout = "wide"
)

# LOADING DATA
@st.cache_data                            # decorator to cache the data for better performance
def load_data():                          #creating loading data method
    df = pd.read_csv("data/6GNetworkAnalysis.csv")
    return df

df = load_data()                          #creating df object to call the method

# TITLE

st.title("6G SMART FACTORY NETWORK ANALYTICS")

st.markdown(
    """
    **Impact of 6G Network Performance on Manufacturing Efficiency
    in Smart Factories**
    
    This dashboard analyzes whether network latency and packet loss
    are associated with changes in manufacturing efficiency,
    production speed, operational errors, and quality-control defects.  


    """
)

# SIDEBAR FILTERS

st.sidebar.header("Filter Options")

# Efficiency Status Filter

efficiency_options = sorted(df['Efficiency_Status'].dropna().unique())            #i.e. Eff Status filter option will contain unique entries of 'eff_stat' column, dropping all the null rows

selected_efficiency = st.sidebar.multiselect(
    "Efficiency Status",
    options = efficiency_options,
    default = efficiency_options
)

# Operation Mode

operation_options = sorted(df['Operation_Mode'].dropna().unique())

selected_operation = st.sidebar.multiselect(
    "Operation Mode",
    options = operation_options,
    default = operation_options
)

#Network Quality

network_quality_options = [
    x for x in ['High', 'Medium', 'Low']
    if x in df['Network_Quality'].unique()
]

selected_network_quality = st.sidebar.multiselect(
    "Network Quality",
    options = network_quality_options,
    default = network_quality_options
)

# APPLY FILTERS

filtered_df = df[
    (df['Efficiency_Status'].isin(selected_efficiency)) &
    (df['Operation_Mode'].isin(selected_operation)) &
    (df['Network_Quality'].isin(selected_network_quality))
].copy()

st.sidebar.markdown("---")

st.sidebar.write(
    f"**Observations Displayed:**{len(filtered_df):,}",
)
# handling Empty Filter Results
if filtered_df.empty:

    st.warning(
        "No available options for the selected filter." \
        "Please adjust the filters."
    )

    st.stop()

# SECTION 1 - NETWORK PERFORMANCE OVERVIEW
st.header("1. Network Performance Overview")

#KPI CALLS
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Average Latency (ms)",
    f"{filtered_df['Network_Latency_ms'].mean():.2f}ms"
)
col2.metric(
    "Average Packet Loss (%)",
    f"{filtered_df['Packet_Loss_%'].mean():.2f}"
)
col3.metric(
    "Average Production Speed",
    f"{filtered_df['Production_Speed_units_per_hr'].mean():.2f} units/hr"
)
col4.metric(
    "Observations",
    f"{len(filtered_df):,}"
)

#Network Distributions
col1, col2 = st.columns(2)

#Latency Distribution
with col1:

    fig_latency = px.histogram(
        filtered_df,
        x = "Network_Latency_ms",
        nbins = 30,
        title = "Network Latency Distribution",
        labels = {
            "Network_Latency_ms": "Latency (ms)"
        }
    )

    fig_latency.update_layout(
        showlegend = False
    )

    st.plotly_chart(
        fig_latency,
        use_container_width=True
    )

#Packet Loss Distribution
with col2:

    fig_packet_loss = px.histogram(
        filtered_df,
        x = "Packet_Loss_%",
        nbins = 29,
        title = "Packet Loss Distribution",
        labels = {
            "Packet_Loss_%" : "Packet Loss (%)"
        }
    )

    fig_packet_loss.update_layout(
        showlegend = False
    )

    st.plotly_chart(
        fig_packet_loss,
        use_container_width=True
    )

# SECTION 2 - NETWORK VS EFFICIENCY

st.header("2. Network Performance vs Manufacturing Efficiency")

#Efficiency Distribution across Latency Bands
latency_efficiency = pd.crosstab(
    filtered_df['Latency_Band'],
    filtered_df['Efficiency_Status'],
    normalize="index"
).reset_index()

latency_efficiency = latency_efficiency.melt(
    id_vars = "Latency_Band",
    var_name = "Efficiency_Status",
    value_name = "Percentage"
)

fig_latency_eff = px.bar(
    latency_efficiency,
    x = "Latency_Band",
    y = "Percentage",
    color = "Efficiency_Status",
    barmode = "stack",
    title = "Efficiency Distribution across Latency Bands",
    labels = {
        "Latency_Band": "Latency Band",
        "Percentage": "Percentage"
    }
)

fig_latency_eff.update_yaxes(tickformat = ".0%")

st.plotly_chart(
    fig_latency_eff,
    use_container_width=True
)

#Effiiciency Distribution across Packet Loss Bands
packet_efficiency = pd.crosstab(
    filtered_df['Packet_Loss_Band'],
    filtered_df['Efficiency_Status'],
    normalize="index"
).reset_index()

packet_efficiency = packet_efficiency.melt(
    id_vars = "Packet_Loss_Band",
    var_name = "Efficiency_Status",
    value_name = "Percentage"
)

fig_packet_eff = px.bar(
    packet_efficiency,
    x = "Packet_Loss_Band",
    y = "Percentage",
    color = "Efficiency_Status",
    barmode = "stack",
    title = "Efficiency Distribution across Packet Loss Bands",
    labels={
        "Packet_Loss_Band": "Packet Loss Band",
        "Percentage": "Percentage"
    }
)

fig_packet_eff.update_yaxes(tickformat = ".0%")

st.plotly_chart(
    fig_packet_eff,
    use_container_width=True
)

# SECTION 3 - QUALITY & ERROR IMPACT

st.header("3. Quality & Error Impact")

col1,col2 = st.columns(2)

# Packet Loss vs Error Rate
with col1:
    fig_error = px.scatter(
        filtered_df,
        x = "Packet_Loss_%",
        y = "Error_Rate_%",
        opacity = 0.35,
        title = "Packet Loss vs Operational Error Rate",
        labels = {
            "Packet_Loss_%":"Packet Loss (%)",
            "Error_Rate_%" : "Error Rate (%)"
        }
    )

    st.plotly_chart(
        fig_error,
        use_container_width=True
    )

# Packet Loss vs Defect Rate

with col2:
    fig_defect = px.scatter(
        filtered_df,
        x = "Packet_Loss_%",
        y = "Quality_Control_Defect_Rate_%",
        opacity = 0.35,
        title = "Packet Loss vs Quality-Control Defect Rate",
        labels = {
            "Packet_Loss_%" : "Packet Loss (%)",
            "Quality_Control_Defect_Rate_%" : "Defect Rate (%)"
        }
    )

    st.plotly_chart(
            fig_defect,
            use_container_width=True
    )

# SECTION 4 - PRODUCTION PERFORMANCE

st.header("4. Production Performance")

fig_prod = px.scatter(
    filtered_df,
    x = "Network_Latency_ms",
    y = "Production_Speed_units_per_hr",
    color = "Efficiency_Status",
    opacity = 0.5,
    title = "Network Latency vs Production Performance",
    labels = {
        "Network_Latency_ms" : "Network Latency (ms)",
        "Production_Speed_units_per_hr" : "Production Speed (units per hr)"
    }
)

st.plotly_chart(
    fig_prod,
    use_container_width=True
)

# SECTION 5 - Statistical Findings

st.header("5. Statistical Findings")

def eta_squared(groups):
    groups = [group.dropna() for group in groups if len(group.dropna()) > 0]

    if len(groups) < 2:
        return float("nan")

    all_values = pd.concat(groups)

    grand_mean = all_values.mean()

    ss_between = sum(
        len(group) * (group.mean() - grand_mean) ** 2
        for group in groups
    )

    ss_total = sum(
        ((group - grand_mean) ** 2).sum()
        for group in groups
    )

    if ss_total == 0:
        return 0

    return ss_between / ss_total

# Latency groups
latency_groups_production = [
    group["Production_Speed_units_per_hr"]
    for _, group in filtered_df.groupby(
        "Latency_Band",
        observed=True
    )
]

latency_groups_error = [
    group["Error_Rate_%"]
    for _, group in filtered_df.groupby(
        "Latency_Band",
        observed=True
    )
]

latency_groups_defect = [
    group["Quality_Control_Defect_Rate_%"]
    for _, group in filtered_df.groupby(
        "Latency_Band",
        observed=True
    )
]

# Packet-loss groups
packet_groups_production = [
    group["Production_Speed_units_per_hr"]
    for _, group in filtered_df.groupby(
        "Packet_Loss_Band",
        observed=True
    )
]

packet_groups_error = [
    group["Error_Rate_%"]
    for _, group in filtered_df.groupby(
        "Packet_Loss_Band",
        observed=True
    )
]

packet_groups_defect = [
    group["Quality_Control_Defect_Rate_%"]
    for _, group in filtered_df.groupby(
        "Packet_Loss_Band",
        observed=True
    )
]

# Calculating ANOVA p-values
def calculate_anova(groups):

    groups = [
        group.dropna()
        for group in groups
        if len(group.dropna()) > 0
    ]

    if len(groups) < 2:
        return float("nan")

    try:
        _, p_value = f_oneway(*groups)
        return p_value

    except:
        return float("nan")


p_latency_production = calculate_anova(
    latency_groups_production
)

p_latency_error = calculate_anova(
    latency_groups_error
)

p_latency_defect = calculate_anova(
    latency_groups_defect
)

p_packet_production = calculate_anova(
    packet_groups_production
)

p_packet_error = calculate_anova(
    packet_groups_error
)

p_packet_defect = calculate_anova(
    packet_groups_defect
)

# Calculate Eta Squared
eta_latency_production = eta_squared(
    latency_groups_production
)

eta_latency_error = eta_squared(
    latency_groups_error
)

eta_latency_defect = eta_squared(
    latency_groups_defect
)

eta_packet_production = eta_squared(
    packet_groups_production
)

eta_packet_error = eta_squared(
    packet_groups_error
)

eta_packet_defect = eta_squared(
    packet_groups_defect
)

# Create results table
results = pd.DataFrame({

    "Analysis": [
        "Latency → Production",
        "Latency → Error",
        "Latency → Defect",
        "Packet Loss → Production",
        "Packet Loss → Error",
        "Packet Loss → Defect"
    ],

    "p-value": [
        p_latency_production,
        p_latency_error,
        p_latency_defect,
        p_packet_production,
        p_packet_error,
        p_packet_defect
    ],

    "η² Effect Size": [
        eta_latency_production,
        eta_latency_error,
        eta_latency_defect,
        eta_packet_production,
        eta_packet_error,
        eta_packet_defect
    ]

})


results["Significant?"] = results["p-value"].apply(
    lambda p: (
        "Yes"
        if pd.notna(p) and p < 0.05
        else "No"
    )
)


st.dataframe(
    results.round({
        "p-value": 6,
        "η² Effect Size": 6
    }),
    use_container_width=True,
    hide_index=True
)

# SECTION 6 - KEY PERFORMANCE INDICATORS

st.header("6. Key Performance Indicators")

# Latency Sensitivity
latency_band_production = (
    filtered_df
    .groupby("Latency_Band", observed=True)
    ["Production_Speed_units_per_hr"]
    .mean()
)

if len(latency_band_production) >= 2:

    latency_sensitivity = (
        latency_band_production.iloc[-1]
        -
        latency_band_production.iloc[0]
    ) / (
        filtered_df["Network_Latency_ms"].max()
        -
        filtered_df["Network_Latency_ms"].min()
    )

else:

    latency_sensitivity = float("nan")

# Packet-Loss Impact Ratio
packet_band_production = (
    filtered_df
    .groupby("Packet_Loss_Band", observed=True)
    ["Production_Speed_units_per_hr"]
    .mean()
)

if len(packet_band_production) >= 2:

    lowest_packet_loss_production = (
        packet_band_production.iloc[0]
    )

    highest_packet_loss_production = (
        packet_band_production.iloc[-1]
    )

    packet_loss_impact = (
        (
            highest_packet_loss_production
            -
            lowest_packet_loss_production
        )
        /
        lowest_packet_loss_production
    ) * 100

else:

    packet_loss_impact = float("nan")

# Display
col1, col2 = st.columns(2)


with col1:

    if pd.notna(latency_sensitivity):

        st.metric(
            "Latency Sensitivity",
            f"{latency_sensitivity:.4f} units/hr/ms"
        )

    else:

        st.metric(
            "Latency Sensitivity",
            "N/A"
        )

    st.caption(
        "Change in mean production speed per millisecond "
        "across the observed latency range."
    )


with col2:

    if pd.notna(packet_loss_impact):

        st.metric(
            "Packet-Loss Impact",
            f"{packet_loss_impact:.2f}%"
        )

    else:

        st.metric(
            "Packet-Loss Impact",
            "N/A"
        )

    st.caption(
        "Percentage difference in mean production speed "
        "between the lowest and highest packet-loss bands."
    )

# SECTION 7 - OPTIMIZATION INSIGHTS

st.header("7. 6G Optimization Insights")

# Determine statistical significance
latency_production_sig = (
    pd.notna(p_latency_production)
    and p_latency_production < 0.05
)

latency_error_sig = (
    pd.notna(p_latency_error)
    and p_latency_error < 0.05
)

latency_defect_sig = (
    pd.notna(p_latency_defect)
    and p_latency_defect < 0.05
)

packet_production_sig = (
    pd.notna(p_packet_production)
    and p_packet_production < 0.05
)

packet_error_sig = (
    pd.notna(p_packet_error)
    and p_packet_error < 0.05
)

packet_defect_sig = (
    pd.notna(p_packet_defect)
    and p_packet_defect < 0.05
)

# Dynamic findings
if latency_production_sig:

    latency_production_text = (
        f"Latency bands show a statistically significant "
        f"difference in production speed "
        f"(p = {p_latency_production:.4f})."
    )

else:

    latency_production_text = (
        f"No statistically significant difference in "
        f"production speed was detected across latency "
        f"bands (p = {p_latency_production:.4f})."
    )


if latency_error_sig:

    latency_error_text = (
        f"Latency bands show a statistically significant "
        f"difference in operational error rate "
        f"(p = {p_latency_error:.4f})."
    )

else:

    latency_error_text = (
        f"No statistically significant difference in "
        f"operational error rate was detected across "
        f"latency bands (p = {p_latency_error:.4f})."
    )


if packet_error_sig:

    packet_error_text = (
        f"Packet-loss bands show a statistically significant "
        f"difference in operational error rate "
        f"(p = {p_packet_error:.4f})."
    )

else:

    packet_error_text = (
        f"No statistically significant difference in "
        f"operational error rate was detected across "
        f"packet-loss bands (p = {p_packet_error:.4f})."
    )


if latency_defect_sig:

    latency_defect_text = (
        f"Latency bands show a statistically significant "
        f"difference in defect rate "
        f"(p = {p_latency_defect:.4f})."
    )

else:

    latency_defect_text = (
        f"No statistically significant difference in "
        f"defect rate was detected across latency bands "
        f"(p = {p_latency_defect:.4f})."
    )


if packet_defect_sig:

    packet_defect_text = (
        f"Packet-loss bands show a statistically significant "
        f"difference in defect rate "
        f"(p = {p_packet_defect:.4f})."
    )

else:

    packet_defect_text = (
        f"No statistically significant difference in "
        f"defect rate was detected across packet-loss bands "
        f"(p = {p_packet_defect:.4f})."
    )

# Dynamic dashboard interpretation
st.info(
    f"""
**Current Filtered Dataset**

• Observations analyzed: {len(filtered_df):,}

• Latency range:
  {filtered_df['Network_Latency_ms'].min():.2f}–{filtered_df['Network_Latency_ms'].max():.2f} ms

• Packet-loss range:
  {filtered_df['Packet_Loss_%'].min():.2f}–{filtered_df['Packet_Loss_%'].max():.2f}%


**Production Efficiency**

{latency_production_text}

**Latency → Operational Errors**

{latency_error_text}

**Packet Loss → Operational Errors**

{packet_error_text}


**Latency → Quality-Control Defects**

{latency_defect_text}

**Packet Loss → Quality-Control Defects**

{packet_defect_text}


**Interpretation**

Statistical significance is evaluated at α = 0.05.

A statistically significant result does not necessarily imply
a practically important effect. The η² effect size should therefore
be considered alongside the p-value when interpreting the result.
"""
)

# FOOTER
st.markdown("---")

st.caption(
    "Smart Factory 6G Network Analytics"
)