#!/usr/bin/env python3

"""
App to quickly solve buffer titration and adjustment problems.
"""

# Imports
import PySimpleGUI as sg  # Requires version 4.0 or greater

# import PySimpleGUIQt as sg  # Alternate backend

# Functions


def app_view():
    """
    Create the GUI and send values to the buffer_solver, process updates.
    """

    # Define our Layout
    layout = [
        [
            sg.Text("Buffer initial concentration (M):"),
            sg.Input(do_not_clear=True, default_text="1.0", key="_BINIT_"),
        ],
        [
            sg.Text("Buffer final concentration (M):"),
            sg.Input(do_not_clear=True, default_text="0.2", key="_BFIN_"),
        ],
        [
            sg.Text("Buffer pKa:"),
            sg.Input(do_not_clear=True, default_text="8.0", key="_PKA_"),
        ],
        [
            sg.Text("Total volume of final solution (L):"),
            sg.Input(do_not_clear=True, default_text="2.0", key="_VOL_"),
        ],
        [
            sg.Text("Stock concentration of HCl (M):"),
            sg.Input(do_not_clear=True, default_text="6.0", key="_HCL_"),
        ],
        [
            sg.Text("Stock concentration of NaOH (M):"),
            sg.Input(do_not_clear=True, default_text="6.0", key="_NAOH_"),
        ],
        [
            sg.Text("Initial pH:"),
            sg.Input(do_not_clear=True, default_text="8.2", key="_PHINIT_"),
        ],
        [
            sg.Text("Final pH:"),
            sg.Input(do_not_clear=True, default_text="7.6", key="_PHFIN_"),
        ],
        [sg.Button("Show Recipe", key="SHOW"), sg.Button("Exit")],
        [sg.Text("")],
        [
            sg.Text(
                "                                                                               \n\
                                                                                                \n\
                                                                                                \n\
                                                                                                \n\
                                                                                                ",
                key="_OUTPUT_",
            )  # BUG: Needed empty space for Tkinter update method to work
        ],
    ]

    # Launch the app window
    window = sg.Window("Buffer Adjustment App", layout, size=(300, 375))

    # Event loop
    while True:
        event, values = window.Read()
        # Capture program exit
        if event is None or event == "Exit":
            break
        # Capture button presses
        if event == "SHOW":
            recipe = buffer_solver(
                values["_BINIT_"],
                values["_BFIN_"],
                values["_PKA_"],
                values["_VOL_"],
                values["_HCL_"],
                values["_NAOH_"],
                values["_PHINIT_"],
                values["_PHFIN_"],
            )
            # update the "output" element to be the recipe
            window.Element("_OUTPUT_").Update(recipe)
    # Clean up when finished
    window.Close()


def buffer_solver(
    buffer_conc_initial,
    buffer_conc_final,
    buffer_pKa,
    total_volume,
    HCl_stock_conc,
    NaOH_stock_conc,
    initial_pH,
    final_pH,
):
    """
    Take in buffer adjustment parameters and return an adjustment recipe.
    """

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

    # Perform buffer math

    # First find moles of buffer and volume of buffer:
    buffer_volume = (buffer_conc_final * total_volume) / buffer_conc_initial
    moles_of_buffer = buffer_volume * buffer_conc_initial

    # Then, find initial conditions:
    initial_ratio = 10 ** (initial_pH - buffer_pKa)
    initial_HA = moles_of_buffer / (1.0 + initial_ratio)

    # Then, final conditions:
    final_ratio = 10 ** (final_pH - buffer_pKa)
    final_HA = moles_of_buffer / (1.0 + final_ratio)

    # Then, solve for delta-HA:
    difference = final_HA - initial_HA
    if difference == 0.0:  # Catch no-change situations
        return "Invalid conditions"

    # Set titrant
    if difference < 0.0:
        titrant = "NaOH"
        difference = abs(difference)
        volume_titrant = difference / NaOH_stock_conc
    else:
        titrant = "HCl"
        volume_titrant = difference / HCl_stock_conc

    # Solve for volume of water
    volume_water = total_volume - (volume_titrant + buffer_volume)

    # Catch invalid recipe conditions
    if (volume_water <= 0.0) or (volume_titrant <= 0.0):
        return "Invalid conditions"

    # Return functional recipe
    return (
        "Buffer recipe:\nadd {0} liters stock buffer, \n{1} liters of stock {2},\nand {3} liters of water"
    ).format(
        round(buffer_volume, 4),
        round(volume_titrant, 4),
        titrant,
        round(volume_water, 4),
    )


# Main magic
if __name__ == "__main__":
    app_view()
