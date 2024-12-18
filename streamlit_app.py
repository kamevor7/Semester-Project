import streamlit as st
import pandas as pd
import altair as alt

DATA_FILE = 'dataset.csv'

# Load data
@st.cache
def load_data():
    return pd.read_csv(DATA_FILE)

data = load_data()

# Dashboard
st.title("US Labor Statistics Dashboard")

st.sidebar.title("Filters")
series_selected = st.sidebar.multiselect(
    "Select Data Series",
    options=data['series_id'].unique(),
    default=data['series_id'].unique()
)

filtered_data = data[data['series_id'].isin(series_selected)]

# Plot data
chart = alt.Chart(filtered_data).mark_line().encode(
    x='date:T',
    y='value:Q',
    color='series_id:N'
).properties(
    title="Labor Statistics Over Time",
    width=800,
    height=400
)

st.altair_chart(chart, use_container_width=True)

st.dataframe(filtered_data)
