from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import dash_daq as daq
import dash_bootstrap_components as dbc
import numpy as np

from . import pirask
from . import parameters

@callback(
    Output('camera_joystick_output', 'children'),
    Input('camera_joystick', 'force'),
    Input('camera_joystick', 'angle'),
)
def update_output(force, angle):

    if angle >=0 and angle <= 180:
        horizontal = int(-(angle-90) / 3)
        vertical = 0 if force is None else int(force*12)
    else:
        horizontal = int((angle-270) / 3)
        vertical = 0 if force is None else -int(force*12)

    horizontal = int(np.clip(horizontal, -45, 45))
    vertical = int(np.clip(vertical, -45, 45))

    print(f'Angle is {horizontal}, force is {vertical}')
    pirask.send_bot_command(f"camera/{vertical}/{horizontal}", fake=False)
    return [f'Angle is {horizontal}, force is {vertical}']

def get_iframe():
    return html.Iframe(src="http://192.168.1.122:9000/mjpg", style={"height": "500px", "width": "700px"})

def get_widgets():
    return [
        daq.Joystick(id='camera_joystick', label="Pilot Camera", angle=0),
        html.Div(id='camera_joystick_output'),
        ]