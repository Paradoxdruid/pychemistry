#!/usr/bin/env python3

"""
Dash web app for fitting Michaelis-Menten enzyme kinetics.
"""

# Imports
import dash
from dash.dependencies import Input, Output
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy
from scipy.optimize import leastsq
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
            "Input x and y data for Michaelis-Menten fitting (use average values from multiple trials)",
            style={"font-family": "Roboto"},
        ),
        dash_table.DataTable(
            id="table-editing-simple",
            columns=([{"id": "X", "name": "X"}] + [{"id": "Y", "name": "Y"}]),
            data=[
                {"X": 0, "Y": 0},
                {"X": 1, "Y": 8},
                {"X": 2, "Y": 9},
                {"X": 3, "Y": 10},
                {"X": 4, "Y": 11},
                {"X": 5, "Y": 12},
            ],
            editable=True,
        ),
        dcc.Graph(id="table-editing-simple-output"),
    ],
    style={"margin": "auto", "width": "50%"},
)

# Functions


def residuals(y, fitinfo):
    """Returns r-squared value of a given regression."""
    fit_error = 0
    fit_variance = 0

    for i in range(len(fitinfo["fvec"])):
        fit_error += (fitinfo["fvec"][i]) ** 2
        fit_variance += (y[i] - numpy.mean(y)) ** 2
    r_squared = 1 - (fit_error / fit_variance)
    return r_squared


@app.callback(
    Output("table-editing-simple-output", "figure"),
    [Input("table-editing-simple", "data"), Input("table-editing-simple", "columns")],
)
def update_graph2(rows, columns):
    """
    Take user data and perform nonlinear regression to Michaelis-Menten model.
    """

    df = pd.DataFrame(rows, columns=[c["name"] for c in columns])

    x = df["X"].astype(float).values
    y = df["Y"].astype(float).values

    def equation(variables, x):
        return (variables[0] * x) / (variables[1] + x)

    def error(variables, x, y):
        return equation(variables, x) - y

    variable_guesses = [numpy.min(y), numpy.max(y), numpy.mean(x)]
    output = leastsq(error, variable_guesses, args=(x, y), full_output=1)
    variables = output[0]
    fitinfo = output[2]
    r_squared = residuals(y, fitinfo)
    x_range = numpy.arange(numpy.min(x), numpy.max(x), abs(numpy.max(x) / 100))

    # Return plots and a data layout
    plot1 = go.Scatter(x=x, y=y, mode="markers")
    plot2 = go.Scatter(x=x_range, y=equation(variables, x_range), mode="lines")
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
                y=0.45,
                xref="paper",
                yref="paper",
                text="Km = {}".format(round(variables[1], 3)),
                showarrow=False,
            ),
            dict(
                x=0.5,
                y=0.40,
                xref="paper",
                yref="paper",
                text="Vmax = {}".format(round(variables[0], 3)),
                showarrow=False,
            ),
        ],
        xaxis=dict(title="Concentration", titlefont=dict(family="Roboto", size=18)),
        yaxis=dict(title="Enzyme Activity", titlefont=dict(family="Roboto", size=18)),
    )
    return {"data": plot_data, "layout": layout}


# Main magic
if __name__ == "__main__":
    app.run_server(debug=True)
