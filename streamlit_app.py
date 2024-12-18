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
# Default color theme, as user will be able to change color them
DEFAULT_COLOR_THEME = 'Light'

# Data loading phase
@st.cache
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
    options=["Line Chart", "Bar Chart", "Scatter Plot"]
)

# Option for Color Them Selection
color_theme = st.sidebar.radio(
    "Select Dashboard Theme",
    options=["Light", "Dark", "Blue", "Green"],
    index=["Light", "Dark", "Blue", "Green"].index(DEFAULT_COLOR_THEME)
)


def apply_theme(theme):
    if theme == "Light":
        st.markdown(
            """
            <style>
            .main { background-color: #ffffff; color: #000000; }
            </style>
            """,
            unsafe_allow_html=True,
        )
    elif theme == "Dark":
        st.markdown(
            """
            <style>
            .main { background-color: #333333; color: #ffffff; }
            </style>
            """,
            unsafe_allow_html=True,
        )
    elif theme == "Blue":
        st.markdown(
            """
            <style>
            .main { background-color: #e6f7ff; color: #003366; }
            </style>
            """,
            unsafe_allow_html=True,
        )
    elif theme == "Green":
        st.markdown(
            """
            <style>
            .main { background-color: #e6ffe6; color: #003300; }
            </style>
            """,
            unsafe_allow_html=True,
        )

apply_theme(color_theme)

# Running Dashboard Code
st.title("US Labor Statistics Dashboard")
st.write("Visualize and explore labor statistics data.")

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

# Display Filtered Data
st.subheader("Filtered Data Table")
st.dataframe(filtered_data)
