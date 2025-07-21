import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px
import plotly.graph_objects as go

# Load and preprocess the data
df = pd.read_csv('processed_sales.csv')
df['Date'] = pd.to_datetime(df['Date'])

# Aggregate sales per day
daily_sales = df.groupby('Date')['Sales'].sum().reset_index()

# Create the line chart
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=daily_sales['Date'],
    y=daily_sales['Sales'],
    mode='lines+markers',
    name='Sales',
    line=dict(color='blue'),
    marker=dict(size=6)
))

# Add a vertical line on the date of price increase
fig.add_shape(
    type='line',
    x0=pd.to_datetime('2021-01-15'), x1=pd.to_datetime('2021-01-15'),
    y0=0, y1=max(daily_sales['Sales']),
    line=dict(color="red", width=2, dash="dash")
)

# Add annotation for the price increase
fig.add_annotation(
    x=pd.to_datetime('2021-01-15'),
    y=max(daily_sales['Sales']) * 0.95,
    text="Price Increase",
    showarrow=True,
    arrowhead=1,
    ax=0,
    ay=-40,
    font=dict(color="red")
)

# Update axis labels and title
fig.update_layout(
    title="Daily Sales of Pink Morsels",
    xaxis_title="Date",
    yaxis_title="Sales ($)",
    template="plotly_white"
)

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "Pink Morsel Sales Visualizer"

# Define app layout
app.layout = html.Div([
    html.H1("📊 Pink Morsel Sales Visualizer", style={'textAlign': 'center'}),
    dcc.Graph(figure=fig),
    html.P(
        "The red dashed line marks the price increase on 15th January 2021.",
        style={'textAlign': 'center', 'color': 'gray'}
    )
])

# Run app
if __name__ == '__main__':
    app.run(debug=True)
