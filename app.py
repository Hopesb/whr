from dash import dcc, html, Dash, callback, dash_table
from dash.dependencies import Input, Output
import plotly_express as px
import pandas as pd
import os


# Initialize Dash app
app = Dash(__name__)
server = app.server

# Load and process dataset
filepath = "Dataset/whr2023.csv"
df = pd.read_csv(filepath)

# Compute average happiness score per country
country_score = df.groupby(["iso alpha", "Country name"])["Happiness score"].mean().reset_index()

# Layout
app.layout = html.Div(
    children=[
        # Header
        html.H1("World Happiness Dashboard (2023)", style={
            "textAlign": "center",
            "color": "#2c3e50",
            "fontSize": "48px",
            "fontWeight": "bold",
            "marginBottom": "10px"
        }),

        html.Hr(style={
            "borderTop": "3px solid #2980b9",
            "width": "80%",
            "margin": "auto"
        }),

        html.H2("Explore Global Happiness and Economic Metrics", style={
            "textAlign": "center",
            "color": "#34495e",
            "fontSize": "32px",
            "marginBottom": "30px"
        }),

        # Overview
        html.Div([
            html.H3("📊 Dashboard Overview", style={
                "color": "#2c3e50",
                "fontSize": "24px",
                "marginTop": "10px"
            }),
            html.P("This interactive dashboard visualizes the 2023 World Happiness Report data. Explore key indicators like happiness scores and GDP per capita by country.",
                   style={"lineHeight": "1.8", "fontSize": "16px", "color": "#555"}),
            html.Ul([
                html.Li("✅ Filter and view specific columns of the dataset."),
                html.Li("📈 See top countries by Happiness Score and GDP."),
                html.Li("🌍 Analyze happiness distribution on a global map.")
            ], style={"fontSize": "16px", "color": "#555", "marginBottom": "20px"})
        ]),

        # Data Table
        html.Div([
            html.Label("Select Columns to Display:", style={"fontWeight": "bold", "marginBottom": "5px"}),
            dcc.Dropdown(
                options=[{"label": col, "value": col} for col in df.columns],
                value=["Country name", "iso alpha", "Happiness score"],
                multi=True,
                id="selected_columns",
                style={"marginBottom": "15px"}
            ),
            dash_table.DataTable(
                id="table",
                page_size=10,
                style_table={"overflowX": "auto"},
                style_cell={
                    "textAlign": "left",
                    "padding": "8px",
                    "fontFamily": "Segoe UI, Arial, sans-serif",
                    "fontSize": "14px"
                },
                style_header={
                    "backgroundColor": "#2980b9",
                    "color": "white",
                    "fontWeight": "bold"
                },
                style_data_conditional=[
                    {
                        "if": {"state": "active"},
                        "backgroundColor": "#e8f4f8",
                        "border": "1px solid #ccc"
                    }
                ]
            )
        ], style={
            "backgroundColor": "#ecf0f1",
            "padding": "20px",
            "borderRadius": "10px",
            "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)",
            "marginBottom": "30px"
        }),

        # Bar Graphs
        html.Div([
            html.Label("Select Top N Countries:", style={"fontWeight": "bold"}),
            dcc.Input(
                id="no_columns",
                type="number",
                value=5,
                min=1,
                step=1,
                placeholder="Enter number of countries",
                style={"marginBottom": "20px", "width": "30%"}
            ),
            dcc.Graph(id="happiness_score"),
            dcc.Graph(id="gdp_per_capita")
        ], style={
            "backgroundColor": "#fdfefe",
            "padding": "20px",
            "borderRadius": "10px",
            "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
            "marginBottom": "30px"
        }),

        # Choropleth Map
        html.Div([
            dcc.Graph(
                figure=px.choropleth(
                    data_frame=country_score,
                    locations="iso alpha",
                    color="Happiness score",
                    color_continuous_scale=px.colors.sequential.Viridis,
                    title="Happiness Rate by Country (2023)",
                    hover_data=["Country name"],
                    height=600,
                    projection="natural earth"
                )
            )
        ], style={
            "border": "1px solid #ccc",
            "borderRadius": "10px",
            "padding": "15px",
            "backgroundColor": "#fafafa"
        }),

        # Footer
        html.Div([
            html.Hr(style={"marginTop": "40px", "marginBottom": "10px"}),
            html.P("Dashboard by Shodolamu Opeyemi Philip · Built with Dash and Plotly",
                   style={"textAlign": "center", "color": "#777", "fontSize": "14px"}),
            
            html.P([
                "Connect with me on ",
                html.A("LinkedIn", href="www.linkedin.com/in/shodolamu-opeyemi-a53240203", target="_blank", style={"color": "#2980b9", "textDecoration": "none"}),
                " or reach out via ",
                html.A("Email", href="mailto:hope.sb001@gmail.com", style={"color": "#2980b9", "textDecoration": "none"}),
                "."
            ], style={"textAlign": "center", "color": "#555", "fontSize": "14px", "marginTop": "5px"})
        ])

    ],
    style={
        "maxWidth": "1000px",
        "margin": "auto",
        "padding": "20px",
        "fontFamily": "Segoe UI, Arial, sans-serif"
    }
)

# Callbacks

@callback(
    Output("table", "data"),
    Input("selected_columns", "value")
)
def update_table(selected_columns):
    return df[selected_columns].to_dict("records")


@callback(
    Output("happiness_score", "figure"),
    Output("gdp_per_capita", "figure"),
    Input("no_columns", "value")
)
def update_graphs(top_n):
    # Top N by Happiness
    top_happiness = df.groupby("Country name")["Happiness score"].mean().sort_values().tail(top_n)
    happiness_fig = px.bar(
        x=top_happiness.index,
        y=top_happiness.values,
        color=top_happiness.values,
        title=f"Top {top_n} Countries by Happiness Score (2023)",
        labels={"x": "Country", "y": "Happiness Score"}
    )

    # Top N by GDP
    top_gdp = df.groupby("Country name")["Logged GDP per capita"].mean().sort_values().tail(top_n)
    gdp_fig = px.bar(
        x=top_gdp.index,
        y=top_gdp.values,
        color=top_gdp.values,
        title=f"Top {top_n} Countries by GDP per Capita (2023)",
        labels={"x": "Country", "y": "GDP per Capita"}
    )

    return happiness_fig, gdp_fig


# Run app
if __name__ == '__main__':
    app.run(debug=True)
