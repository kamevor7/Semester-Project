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
# Default series 'CES0000000001' is for Total non-farmers workers
DEFAULT_SERIES = 'CES0000000001'

# Data loading phase
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_FILE)
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    return df

data = load_data()

# Setting Sidebar Filters
st.sidebar.title("Filters")

selected_series = st.sidebar.multiselect(
    "Select Data Series",
    options=data['series_id'].unique(),
    default=[DEFAULT_SERIES]
)

selected_years = st.sidebar.multiselect(
    "Select Year(s)",
    options=data['year'].unique(),
    default=[DEFAULT_YEAR]
)

plot_type = st.sidebar.selectbox(
    "Select Plot Type",
    options=["Line Chart", "Bar Chart", "Scatter Plot"],
    index=2
)

# Running Dashboard Code
st.title("US Labor Statistics Dashboard")
st.write("Data Visualization")

# Data Filter
filtered_data = data[
    (data['series_id'].isin(selected_series)) &
    (data['year'].isin(selected_years))
]

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
