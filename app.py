import pandas as pd
import dash
from dash import html, dcc, Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc

df = pd.read_csv("ventas.csv")

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
app.title = "Dashboard de Ventas Tecnológicas"

app.layout = dbc.Container([
    html.H1("Dashboard de Ventas Globales", className="my-4 text-center"),

    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                df['Año'].unique(), df['Año'].unique()[0],
                id='filtro-año', clearable=False
            )
        ], width=4),
        dbc.Col([
            dcc.Dropdown(
                df['Región'].unique(), df['Región'].unique()[0],
                id='filtro-region', clearable=False
            )
        ], width=4),
        dbc.Col([
            dcc.Dropdown(
                df['Categoría'].unique(), df['Categoría'].unique()[0],
                id='filtro-categoria', clearable=False
            )
        ], width=4),
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(dcc.Graph(id="grafico-linea"), width=8),
        dbc.Col(dcc.Graph(id="grafico-top5"), width=4),
    ]),

    dbc.Row([
        dbc.Col(dcc.Graph(id="grafico-pie"))
    ])
], fluid=True)

@app.callback(
    Output("grafico-linea", "figure"),
    Output("grafico-top5", "figure"),
    Output("grafico-pie", "figure"),
    Input("filtro-año", "value"),
    Input("filtro-region", "value"),
    Input("filtro-categoria", "value"),
)
def actualizar_graficos(año, region, categoria):
    df_filtrado = df[(df["Año"] == año) & (df["Región"] == region) & (df["Categoría"] == categoria)]

    fig_linea = px.line(df_filtrado, x="Mes", y="Ventas", title="Ventas Mensuales")
    top5 = df_filtrado.groupby("Producto")["Ventas"].sum().nlargest(5).reset_index()
    fig_top5 = px.bar(top5, x="Ventas", y="Producto", orientation='h', title="Top 5 Productos")
    fig_pie = px.pie(df_filtrado, names="Producto", values="Ventas", title="Participación por Producto")

    return fig_linea, fig_top5, fig_pie

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 8050))
    app.run_server(host="0.0.0.0", port=port)
