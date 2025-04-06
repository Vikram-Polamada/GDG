import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time

# Add custom CSS for spacing between graphs
st.markdown(
    """
    <style>
    .streamlit-expanderHeader {
        margin-bottom: 20px;  /* Adds space below each graph */
    }
    .block-container {
        padding: 20px 20px 20px 20px;  /* Adjust overall padding for better spacing */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Load the CSV data
df = pd.read_csv(r'C:\Users\vikra\OneDrive\Desktop\project\weather_data1.csv')

# Convert 'Date & Time' column to datetime
df['Date & Time'] = pd.to_datetime(df['Date & Time'])

# Define the parameters and their corresponding column names
parameters = {
    'Temperature': 'Temp - °C',
    'Absolute Pressure': 'Absolute Pressure - mm Hg',
    'Humidity': 'Hum - %',
    'Average Wind Speed': 'Avg Wind Speed - m/s',
    'Rain': 'Rain - mm'
}

# Set up the main title
st.title("Dynamic Weather Plots")

# Function to create a Plotly plot for the selected parameter
def plot_to_plotly(data, y_label, title):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data['Date & Time'],
        y=data[y_label],
        mode='lines+markers',
        name=title,
        marker=dict(size=8),
        line=dict(width=2)
    ))

    # Set x-axis properties
    fig.update_layout(
        title=title,
        title_font=dict(size=18),  # Adjust the title font size
        xaxis_title='Date & Time',
        yaxis_title=title,
        xaxis_tickformat='%Y-%m-%d %H:%M',
        xaxis=dict(tickangle=-45),
        template='plotly',
        margin=dict(l=40, r=40, t=40, b=40),
        width=1600  # Explicitly set a larger width for each graph
    )

    return fig

# Initialize starting point and step size
start = 0
step = 10

# Create placeholders for the 2x2 layout, so the graphs persist in the layout
row1_col1, row1_col2 = st.columns([2, 2], gap="large")  # Increase column width ratio for larger graphs
row2_col1, row2_col2 = st.columns([2, 2], gap="large")

# Create empty placeholders for each chart
with row1_col1:
    temp_placeholder = st.empty()
with row1_col2:
    humidity_placeholder = st.empty()
with row2_col1:
    pressure_placeholder = st.empty()
with row2_col2:
    wind_speed_placeholder = st.empty()

# Loop through the entire dataset continuously until all rows are displayed
while start < len(df):
    # Get the next 10 data points (or remaining points if fewer than 10)
    data = df.iloc[start:start + step]

    # Update Temperature plot in the first column of the first row
    temp_plot = plot_to_plotly(data, parameters['Temperature'], 'Temperature')
    temp_placeholder.plotly_chart(temp_plot, use_container_width=False)  # Disable container width for custom sizing

    # Update Humidity plot in the second column of the first row
    humidity_plot = plot_to_plotly(data, parameters['Humidity'], 'Humidity')
    humidity_placeholder.plotly_chart(humidity_plot, use_container_width=False)

    # Update Absolute Pressure plot in the first column of the second row
    pressure_plot = plot_to_plotly(data, parameters['Absolute Pressure'], 'Absolute Pressure')
    pressure_placeholder.plotly_chart(pressure_plot, use_container_width=False)

    # Update Average Wind Speed plot in the second column of the second row
    wind_speed_plot = plot_to_plotly(data, parameters['Average Wind Speed'], 'Average Wind Speed')
    wind_speed_placeholder.plotly_chart(wind_speed_plot, use_container_width=False)

    # Increment start for the next interval
    start += step
    time.sleep(7)  # Wait for 7 seconds before starting the next batch of updates
