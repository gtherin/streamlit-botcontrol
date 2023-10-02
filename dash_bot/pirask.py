from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import dash_daq as daq
import dash_bootstrap_components as dbc
import requests

from . import parameters

#@callback(Output('connect_camera_switch_output', 'children'), Input('connect_camera_switch', 'value'))
def send_bot_command(command, fake=False):
    command = f"http://{parameters.default['bot_ip']}:{parameters.default['bot_port']}/{command}"
    print(command)
    return command
    if not fake:
        r = requests.get(command)
        print(r.text)
    return command
