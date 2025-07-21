import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv('processed_sales.csv')
df['Date'] = pd.to_datetime(df['Date'])
df['Region'] = df['Region'].str.lower()

# App
app = dash.Dash(__name__)
app.title = "Pink Morsel Sales Visualiser"

app.layout = html.Div(
    style={'fontFamily': 'Arial, sans-serif', 'backgroundColor': '#f5f5f5', 'padding': '20px'},
    children=[
        html.H1("📊 Pink Morsel Sales Visualiser", style={
            'textAlign': 'center',
            'color': '#2c3e50',
            'marginBottom': '40px'
        }),

        html.Div([
            html.Label("Select Region:", style={'fontWeight': 'bold'}),
            dcc.RadioItems(
                id='region-filter',
                options=[
                    {'label': 'All', 'value': 'all'},
                    {'label': 'North', 'value': 'north'},
                    {'label': 'East', 'value': 'east'},
                    {'label': 'South', 'value': 'south'},
                    {'label': 'West', 'value': 'west'},
                ],
                value='all',
                labelStyle={'display': 'inline-block', 'marginRight': '15px'},
                style={'marginBottom': '30px'}
            ),
        ], style={'textAlign': 'center'}),

        dcc.Graph(id='sales-line-chart'),

        html.P("🔴 The red dashed line marks the price increase on 15th January 2021.",
               style={'textAlign': 'center', 'color': 'gray'})
    ]
)

@app.callback(
    Output('sales-line-chart', 'figure'),
    Input('region-filter', 'value')
)
def update_chart(region):
    if region == 'all':
        filtered_df = df
    else:
        filtered_df = df[df['Region'] == region]

    daily_sales = filtered_df.groupby('Date')['Sales'].sum().reset_index()

    fig = px.line(
        daily_sales,
        x='Date',
        y='Sales',
        title=f"Daily Sales of Pink Morsels ({region.title()})" if region != 'all' else "Daily Sales of Pink Morsels (All Regions)",
        labels={'Date': 'Date', 'Sales': 'Sales ($)'},
        markers=True
    )

    try:
        fig.add_vline(
            x=pd.to_datetime("2018-02-07"),
            line_color="red",
            line_dash="dash",
            annotation_text="Price Increase",
            annotation_position="top left"
        )
    except Exception as e:
        print(f"Error adding vline: {e}")

    return fig

if __name__ == '__main__':
    app.run(debug=True)
