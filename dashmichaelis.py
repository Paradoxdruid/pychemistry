#!/usr/bin/env python3

"""
Dash web app for fitting Michaelis-Menten enzyme kinetics.
"""

# Imports
import dash
from dash.dependencies import Input, Output, State
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy
from scipy.optimize import curve_fit
import plotly.graph_objs as go

# Set CSS
external_css = [
    "https://unpkg.com/normalize.css@8.0.0/normalize.css",
    "https://fonts.googleapis.com/css?family=Roboto",
]

# Initialize app
app = dash.Dash(__name__, external_stylesheets=external_css)

server = app.server

app.layout = html.Div(
    [
        html.H1(
            "Bonham Code: Michaelis-Menten Fitting", style={"font-family": "Roboto"}
        ),
        html.Div(
            "Input x and y data (with replicates) for Michaelis-Menten fitting",
            style={"font-family": "Roboto"},
        ),
        html.Div(
            dcc.Input(id="x-axis", value="Concentration", type="text"),
            style={"font-family": "Roboto"},
        ),
        html.Div(
            dcc.Input(id="y-axis", value="Enzyme Activity", type="text"),
            style={"font-family": "Roboto"},
        ),
        html.Div(
            [html.Button("Add Column", id="adding-rows-button", n_clicks=0)],
            style={"font-family": "Roboto"},
        ),
        dash_table.DataTable(
            id="adding-rows-table",
            columns=(
                [{"id": "X", "name": "X"}]
                + [{"id": "Y1", "name": "Y1"}]
                + [{"id": "Y2", "name": "Y2"}]
            ),
            data=[
                {"X": 0, "Y1": 0, "Y2": 1},
                {"X": 1, "Y1": 8, "Y2": 7},
                {"X": 2, "Y1": 9, "Y2": 10},
                {"X": 3, "Y1": 10, "Y2": 11},
                {"X": 4, "Y1": 11, "Y2": 12},
                {"X": 5, "Y1": 12, "Y2": 13},
            ],
            editable=True,
            row_deletable=True,
        ),
        html.Button(
            "Add Row",
            id="editing-rows-button",
            n_clicks=0,
            style={"font-family": "Roboto"},
        ),
        dcc.Graph(id="adding-rows-graph"),
    ],
    style={"margin": "auto", "width": "50%"},
)

# Functions


@app.callback(
    Output("adding-rows-table", "data"),
    [Input("editing-rows-button", "n_clicks")],
    [State("adding-rows-table", "data"), State("adding-rows-table", "columns")],
)
def add_row(n_clicks, rows, columns):
    if n_clicks > 0:
        rows.append({c["id"]: 0 for c in columns})
    return rows


@app.callback(
    Output("adding-rows-table", "columns"),
    [Input("adding-rows-button", "n_clicks")],
    [State("adding-rows-table", "columns")],
)
def update_columns(n_clicks, existing_columns):
    if n_clicks > 0:
        count = 2 + n_clicks
        counter = f"Y{count}"
        existing_columns.append(
            {"id": counter, "name": counter, "editable": True, "deletable": True}
        )
    return existing_columns


@app.callback(
    Output("adding-rows-graph", "figure"),
    [
        Input("adding-rows-table", "data"),
        Input("adding-rows-table", "columns"),
        Input("x-axis", "value"),
        Input("y-axis", "value"),
    ],
)
def update_graph(rows, columns, x_title, y_title):
    """
    Take user data and perform nonlinear regression to Michaelis-Menten model.
    """

    df = pd.DataFrame(rows, columns=[c["name"] for c in columns])

    x = df["X"].astype(float).values

    # Clean up y data
    ys = df.iloc[:, 1:]
    ys = ys.replace("", 0)
    ys = ys.fillna(0)
    ys = ys.astype(float).values
    y = ys.mean(axis=1)
    y_std = ys.std(axis=1)
    y_std = [value if value > 0 else 0.00000001 for value in y_std]
    # FIXME: fitting fails with zero std values; this is a kludge

    def equation(x, a, b):
        return (a * x) / (b + x)

    # Fit the equation
    variable_guesses = [numpy.max(y), numpy.min(y)]  # FIXME: better guesses!
    variables, cov = curve_fit(equation, x, y, p0=variable_guesses, sigma=y_std)
    var_errors = numpy.sqrt(numpy.diag(cov))
    r_squared = 1 - (
        numpy.sum(y - equation(x, *variables)) / numpy.sum((y - numpy.mean(y)) ** 2)
    )

    # Calculate useful range for plotting
    x_range = numpy.arange(numpy.min(x), numpy.max(x), abs(numpy.max(x) / 100))

    # Return plots and a data layout
    plot1 = go.Scatter(
        x=x, y=y, mode="markers", error_y=dict(type="data", array=y_std, visible=True)
    )
    plot2 = go.Scatter(x=x_range, y=equation(x_range, *variables), mode="lines")
    plot_data = [plot1, plot2]
    layout = go.Layout(
        title="Michaelis-Menten Fit",
        width=600,
        annotations=[
            dict(
                x=0.5,
                y=0.5,
                xref="paper",
                yref="paper",
                text="R squared = {}".format(round(r_squared, 3)),
                showarrow=False,
            ),
            dict(
                x=0.5,
                y=0.44,
                xref="paper",
                yref="paper",
                text="Km = {0} \u00B1 {1}".format(
                    round(variables[1], 3), round(var_errors[1], 3)
                ),
                showarrow=False,
            ),
            dict(
                x=0.5,
                y=0.38,
                xref="paper",
                yref="paper",
                text="Vmax = {0} \u00B1 {1}".format(
                    round(variables[0], 3), round(var_errors[0], 3)
                ),
                showarrow=False,
            ),
        ],
        xaxis=dict(title=x_title, titlefont=dict(family="Roboto", size=18)),
        yaxis=dict(title=y_title, titlefont=dict(family="Roboto", size=18)),
    )
    return {"data": plot_data, "layout": layout}


# Main magic
if __name__ == "__main__":
    app.run_server(debug=True)
