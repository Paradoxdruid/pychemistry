# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

# Set up dash server
app = dash.Dash()
app.title = "Buffer Adjustment Calculator"
server = app.server  # Expert server for use by Passenger framework

# Set up graphical layout
app.layout = html.Div(
    [
        html.H1("Buffer Titration Solving", style={"font-family": "Roboto"}),
        html.Div(
            "Input Buffer Initial concentration (M)", style={"font-family": "Roboto"}
        ),
        dcc.Input(id="buff_init_conc", type="text", value="1.0"),
        html.Div(
            "Input Buffer Final concentration (M)", style={"font-family": "Roboto"}
        ),
        dcc.Input(id="buff_final_conc", type="text", value="0.15"),
        html.Div("Input Buffer pKa", style={"font-family": "Roboto"}),
        dcc.Input(id="buff_pka", type="text", value="8.0"),
        html.Div("Input Final Volume of Solution (L)", style={"font-family": "Roboto"}),
        dcc.Input(id="final_volume", type="text", value="1.5"),
        html.Div(
            "Input stock HCl (or strong acid titrant) concentration (M)",
            style={"font-family": "Roboto"},
        ),
        dcc.Input(id="hcl_conc", type="text", value="12.0"),
        html.Div(
            "Input stock NaOH (or strong base titrant) concentration (M)",
            style={"font-family": "Roboto"},
        ),
        dcc.Input(id="naoh_conc", type="text", value="10.0"),
        html.Div("Input Initial Solution pH", style={"font-family": "Roboto"}),
        dcc.Input(id="init_ph", type="text", value="7.0"),
        html.Div("Input Final Solution pH", style={"font-family": "Roboto"}),
        dcc.Input(id="final_ph", type="text", value="8.3"),
        html.Button(id="submit-button", n_clicks=0, children="Submit"),
        html.Div(id="output-div", style={"font-family": "Roboto"}),
    ],
    style={"margin": "auto", "width": "50%"},
)


@app.callback(
    Output(component_id="output-div", component_property="children"),
    [Input("submit-button", "n_clicks")],
    [
        State("buff_init_conc", "value"),
        State("buff_final_conc", "value"),
        State("buff_pka", "value"),
        State("final_volume", "value"),
        State("hcl_conc", "value"),
        State("naoh_conc", "value"),
        State("init_ph", "value"),
        State("final_ph", "value"),
    ],
)
def Buffer_Solver(
    n_clicks,
    buffer_conc_initial,
    buffer_conc_final,
    buffer_pKa,
    total_volume,
    HCl_stock_conc,
    NaOH_stock_conc,
    initial_pH,
    final_pH,
):
    # Sanitize input and catch unusable input
    try:
        buffer_conc_initial = float(buffer_conc_initial)
        buffer_conc_final = float(buffer_conc_final)
        buffer_pKa = float(buffer_pKa)
        total_volume = float(total_volume)
        HCl_stock_conc = float(HCl_stock_conc)
        NaOH_stock_conc = float(NaOH_stock_conc)
        initial_pH = float(initial_pH)
        final_pH = float(final_pH)
    except ValueError:
        return "Invalid input values, try again"

    # Remove common nonsense conditions
    if not (0.0 < buffer_conc_initial <= 100.0):
        return "Invalid initial buffer concentration"
    if not (0.0 < buffer_conc_final <= 100.0):
        return "Invalid final buffer concentration"
    if not (0.0 < HCl_stock_conc <= 100.0):
        return "Invalid HCl concentration"
    if not (0.0 < NaOH_stock_conc <= 100.0):
        return "Invalid NaOH concentration"
    if buffer_conc_final > buffer_conc_initial:
        return "Can't increase concentration through dilution"
    if not (0.0 < buffer_pKa <= 100.0):
        return "Invalid pKa value"
    if not (0.0 < initial_pH <= 20.0):
        return "Invalid initial pH"
    if not (0.0 < final_pH <= 20.0):
        return "Invalid final pH"

    # First find moles of buffer and volume of buffer:
    buffer_volume = (buffer_conc_final * total_volume) / buffer_conc_initial
    moles_of_buffer = buffer_volume * buffer_conc_initial

    # Then, find initial conditions:
    initial_ratio = 10 ** (initial_pH - buffer_pKa)
    initial_HA = moles_of_buffer / (1 + initial_ratio)

    # Then, final conditions:
    final_ratio = 10 ** (final_pH - buffer_pKa)
    final_HA = moles_of_buffer / (1 + final_ratio)

    # Then, solve for titrant:
    difference = final_HA - initial_HA

    # Set titrant
    if difference < 0:
        titrant = "NaOH"
        difference = abs(difference)
        volume_titrant = difference / NaOH_stock_conc
    else:
        titrant = "HCl"
        volume_titrant = difference / HCl_stock_conc

    # Solve for volume of water
    volume_water = total_volume - (volume_titrant + buffer_volume)

    # Return functional recipe
    return (
        "Buffer recipe: add {0} liters stock buffer, "
        "{1} liters of stock {2}, and {3} liters of water"
    ).format(
        round(buffer_volume, 4),
        round(volume_titrant, 4),
        titrant,
        round(volume_water, 4),
    )


external_css = [
    "https://unpkg.com/normalize.css@8.0.0/normalize.css",
    "https://fonts.googleapis.com/css?family=Roboto",
]


for css in external_css:
    app.css.append_css({"external_url": css})


# Main magic
if __name__ == "__main__":
    app.run_server(debug=True)
