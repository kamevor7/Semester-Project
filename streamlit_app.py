from operator import index

import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime

# Upon opening the app, the Dashboard display the following default series.

# Our dataset
DATA_FILE = 'dataset.csv'
# Default year is the current year
DEFAULT_YEAR = datetime.now().year
# Default series 'CES0000000001' is for Total Nonfarm Employment
DEFAULT_SERIES = 'CES0000000001'

# Series name Update for better visualization
SERIES_NAMES = {
    "CES0000000001": "Total Nonfarm Employment",
    "LNS14000000": "Unemployment Rate",
    "LNS11000000": "Civilian Labor Force",
    "LNS12000000": "Civilian Employment",
    "LNS13000000": "Civilian Unemployment"
}

# Data loading phase
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_FILE)
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    return df

data = load_data()

# Setting Sidebar Filters
st.sidebar.title("Filters")

# Update series names for filtering
series_display_names = {v: k for k, v in SERIES_NAMES.items()}

# Filtering Series
selected_series = st.sidebar.multiselect(
    options=list(SERIES_NAMES.keys()),
    format_func=lambda x: SERIES_NAMES[x],
    default=[DEFAULT_SERIES]
)

# filtering by Year
selected_years = st.sidebar.multiselect(
    options=data['year'].unique(),
    default=[DEFAULT_YEAR]
)

# Selecting different plotting
plot_type = st.sidebar.selectbox(
    options=["Line Chart", "Bar Chart", "Scatter Plot"],
    index=2
)

# Temporal Analysis
st.sidebar.title("Temporal Analysis")

temporal_aggregation = st.sidebar.radio(
    options=["Monthly", "Yearly", "Quarterly"],
    index=0
)

show_trendline = st.sidebar.checkbox("Add Trendline", value=False)

# Filter Data
filtered_data = data[
    (data['series_id'].isin(selected_series)) &
    (data['year'].isin(selected_years))
]

# Temporal Aggregation
def aggregate_data(df, aggregation):
    if aggregation == "Monthly":
        return df.groupby(['year', 'month', 'series_id'])['value'].mean().reset_index()
    elif aggregation == "Yearly":
        return df.groupby(['year', 'series_id'])['value'].mean().reset_index()
    elif aggregation == "Quarterly":
        df['quarter'] = df['date'].dt.quarter
        return df.groupby(['year', 'quarter', 'series_id'])['value'].mean().reset_index()

aggregated_data = aggregate_data(filtered_data, temporal_aggregation)

# Running Dashboard Code
st.title("US Labor Statistics Dashboard")
st.write("Data Visualization")

# Plotting: Line Chart, Bar Chart, Scatter Plot
if not filtered_data.empty:
    if plot_type == "Line Chart":
        chart = alt.Chart(filtered_data).mark_line().encode(
            x='date:T',
            y='value:Q',
            color='series_id:N',
            tooltip=['series_id', 'date:T', 'value:Q']
        )
    elif plot_type == "Bar Chart":
        chart = alt.Chart(filtered_data).mark_bar().encode(
            x='date:T',
            y='value:Q',
            color='series_id:N',
            tooltip=['series_id', 'date:T', 'value:Q']
        )
    elif plot_type == "Scatter Plot":
        chart = alt.Chart(filtered_data).mark_circle().encode(
            x='date:T',
            y='value:Q',
            color='series_id:N',
            size='value:Q',
            tooltip=['series_id', 'date:T', 'value:Q']
        )

    st.altair_chart(chart.properties(width=800, height=400), use_container_width=True)
else:
    st.warning("No data available for the selected filters.")


# Temporal Analysis Section
st.subheader(f"Temporal Analysis: {temporal_aggregation}")
if not aggregated_data.empty:
    temporal_chart = alt.Chart(aggregated_data).mark_line().encode(
        x=alt.X('month:O' if temporal_aggregation == 'Monthly' else 'year:O', title="Time Period"),
        y='value:Q',
        color='series_id:N',
        tooltip=['series_id', 'value:Q', 'year:O']
    )

    # Add Trendline if selected
    if show_trendline:
        temporal_chart = temporal_chart + alt.Chart(aggregated_data).transform_loess(
            'month' if temporal_aggregation == 'Monthly' else 'year',
            'value'
        ).mark_line(color='red', size=2)

    st.altair_chart(temporal_chart.properties(width=800, height=400), use_container_width=True)
else:
    st.warning("No aggregated data available.")