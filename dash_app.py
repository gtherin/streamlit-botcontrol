from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import dash_daq as daq
import dash_bootstrap_components as dbc
import requests

import dash_bot
import numpy as np
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions=True


@callback(
    Output('joystick-output-camera', 'children'),
    Input('my-joystick-camera', 'angle'),
    Input('my-joystick-camera', 'force')
)
def update_output(angle, force):
    return [f'Angle is {angle}', html.Br(), f'Force is {force}']


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):

    objs = [html.H1(children='My little robot', style={'textAlign':'center'})]

    #if pathname == "/":
    #    objs.append(html.P("This is the content of the home page!"))

    objs += dash_bot.pilot.get_widgets()
    objs += dash_bot.camera.get_widgets()
    objs += dash_bot.get_programs_objs()
    objs += dash_bot.music.get_audio_objs()

    # If the user tries to reach a different page, return a 404 message
    return html.Div(objs, className="p-3 bg-light rounded-3")

content = html.Div(id="page-content", style={
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
})


app.layout = html.Div([dcc.Location(id="url"), dash_bot.sidebar, content])

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    dff = df[df.country==value]
    return px.line(dff, x='year', y='pop')


if __name__ == '__main__':
    app.run(port=8050, debug=True)#, dev_tools_ui=False)#, host='127.0.0.1')
