from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import dash_daq as daq
import dash_bootstrap_components as dbc
import numpy as np

from . import pirask
from . import parameters

@callback(
    Output('joystick_pilot_output', 'children'),
    Input('joystick_pilot', 'angle'),
    Input('joystick_pilot', 'force'),
    Input('pilot_speed', 'value')
)
def update_output(angle, force, value):
    if angle >=0 and angle <= 180:
        angle = int(-(angle-90) / 3)
        angle = int(np.clip(angle, -45, 45))
        speed = 0 if force is None else int(force*value*20)
    else:
        angle = int((angle-270) / 3)
        angle = int(np.clip(angle, -45, 45))
        speed = 0 if force is None else -int(force*value*20)

    pirask.send_bot_command(f"jmove/{speed}/{angle}")
    return [f'Angle is {angle}, force is {force}, value is {value}, speed is {speed}']

def get_widgets():

    return [
        daq.Joystick(id='joystick_pilot', label="Pilot Joystick", angle=0),
        html.Div(id='joystick_pilot_output'),
        dcc.Slider(0, 10, 1, value=1, id='pilot_speed'),
        ]