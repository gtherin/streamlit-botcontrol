from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import dash_daq as daq
import dash_bootstrap_components as dbc
import requests

import dash_bot
import numpy as np
app = Dash(__name__, external_stylesheets=[dbc.themes.MINTY])
app.config.suppress_callback_exceptions=True
# CERULEAN, COSMO, CYBORG, DARKLY, FLATLY, JOURNAL, LITERA, LUMEN, LUX, MATERIA, MINTY, MORPH, 
# PULSE, QUARTZ, SANDSTONE, SIMPLEX, SKETCHY, SLATE, SOLAR, SPACELAB, SUPERHERO, UNITED, VAPOR, YETI, ZEPHYR.


@callback(
    Output('joystick-output-camera', 'children'),
    Input('my-joystick-camera', 'angle'),
    Input('my-joystick-camera', 'force')
)
def update_output(angle, force):
    return [f'Angle is {angle}', html.Br(), f'Force is {force}']


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):

    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        dash_bot.camera.get_iframe(),
                        width={"size": 5},
                    ),
                    dbc.Col(html.Div("  "), width={"size": 3},),
                    dbc.Col(html.Div(
                        dash_bot.pilot.get_widgets() + 
                        dash_bot.camera.get_widgets() + 
                        dash_bot.get_programs_objs()
                    ), width={"size": 3},
                    ),
                ]
            ),
            dbc.Row(dash_bot.music.get_audio_objs()),

        ]
    , className="p-3 bg-light rounded-3")

    #if pathname == "/":
    #    objs.append(html.P("This is the content of the home page!"))


content = html.Div(id="page-content", style={
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
})


app.layout = html.Div([dcc.Location(id="url"), dash_bot.sidebar, content])

if __name__ == '__main__':
    app.run(port=8050, debug=True)#, dev_tools_ui=False)#, host='127.0.0.1')
