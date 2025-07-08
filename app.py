from dash import dcc, html, Dash, callback, dash_table
from dash.dependencies import Input, Output
import plotly_express as px
import pandas as pd
import os


app = Dash(__name__)

server = app.server

filepath = "Dataset/whr2023.csv"
df = pd.read_csv(filepath)
country_score = df.groupby(["iso alpha", "Country name"])["Happiness score"].mean().reset_index()

app.layout = html.Div(
    [
        html.H1("Web Application Dash Deployment", style={
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

        html.H2("Exploring World Happiness Rate in 2023", style={
            "textAlign": "center",
            "color": "#34495e",
            "fontSize": "32px",
            "marginBottom": "30px"
        }),

        html.Div([
            html.Label("Select Columns to Display:", style={"fontWeight": "bold"}),
            dcc.Dropdown(
                [col for col in df.columns],
                value=["Country name", "iso alpha", "Happiness score"],
                multi=True,
                id="selected_columns",
                style={"marginBottom": "15px"}
            ),
            dash_table.DataTable(
                page_size=10,
                id="table",
                style_table={"overflowX": "auto"},
                style_cell={
                    "textAlign": "left",
                    "padding": "8px",
                    "fontFamily": "Arial",
                },
                style_header={
                    "backgroundColor": "#2980b9",
                    "color": "white",
                    "fontWeight": "bold"
                },
            )
        ], style={
            "backgroundColor": "#ecf0f1",
            "padding": "20px",
            "borderRadius": "10px",
            "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)",
            "marginBottom": "30px"
        }),

        html.Div([
            html.Label("Select Top N Countries:", style={"fontWeight": "bold"}),
            dcc.Input(
                value=5,
                type="number",
                placeholder="Number of Countries",
                id="no_columns",
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
                    projection='natural earth'
                )
            )
        ], style={
            "border": "1px solid #ccc",
            "borderRadius": "10px",
            "padding": "15px",
            "backgroundColor": "#fafafa"
        })
    ],
    style={
        "maxWidth": "1000px",
        "margin": "auto",
        "padding": "20px"
    }
)


@callback(
    Output("table", "data"),
    Input("selected_columns", "value")
)
def filtercolumns(columns):
    return df[columns].to_dict("records")


@callback(
    Output("happiness_score", "figure"),
    Output("gdp_per_capita", "figure"),
    Input("no_columns", "value")
)
def plot_happiness_score(top_n):
    top_n_df = (df.groupby("Country name")["Happiness score"].mean()
                .sort_values().tail(top_n))
    top_n_df_gdp = (df.groupby("Country name")["Logged GDP per capita"].mean()
                    .sort_values().tail(top_n))
    fig1 = px.bar(data_frame=top_n_df,
                  x=top_n_df.index,
                  y=top_n_df.values,
                  color=top_n_df.values,
                  title=f"Top {top_n} Happiness Country in 2023")
    fig1.update_layout(yaxis_title="Happiness score", xaxis_title="Country")
    fig2 = px.bar(data_frame=top_n_df_gdp,
                  x=top_n_df_gdp.index,
                  y=top_n_df_gdp.values,
                  color=top_n_df_gdp.values,
                  title=f"Top {top_n} GDP per capita in 2023")
    fig2.update_layout(yaxis_title="GDP per capita", xaxis_title="Country")
    return fig1, fig2


if __name__ == '__main__':
    app.run(debug=True)