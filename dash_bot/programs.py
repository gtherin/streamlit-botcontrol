from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import dash_daq as daq
import dash_bootstrap_components as dbc

from . import pirask


def get_programs_objs():
    return [
        daq.ToggleSwitch(id='line_following', value=False, label='➿line_following', labelPosition='left'),
        html.Div(id='line_following_output'),
        daq.ToggleSwitch(id='infinite_loop', value=False, label='infinite_loop', labelPosition='left'),
        html.Div(id='infinite_loop_output'),
        daq.ToggleSwitch(id='horn', value=False, label='horn ?', labelPosition='left'),
        html.Div(id='horn_output'),
        daq.ToggleSwitch(id='avoid_obstacles', value=False, label='⛐ avoid_obstacles', labelPosition='left'),
        html.Div(id='avoid_obstacles_output'),
        daq.ToggleSwitch(id='vent', value=False, label='⚙️vent', labelPosition='left'),
        html.Div(id='vent_output'),
        daq.ToggleSwitch(id='take_photo', value=False, label='📷take_photo', labelPosition='left'),
        html.Div(id='take_photo_output'),
    ]

@callback(Output('line_following_output', 'children'), Input('line_following', 'value'))
def update_output(value):
    return ""
    if value:
        return pirask.send_bot_command("start_thread/line_following")
    else:
        return pirask.send_bot_command("stop_thread/line_following")


@callback(Output('infinite_loop_output', 'children'), Input('infinite_loop', 'value'))
def update_output(value):
    return ""
    if value:
        return pirask.send_bot_command("start_thread/infinite_loop")
    else:
        return pirask.send_bot_command("stop_thread/infinite_loop")

@callback(Output('horn_output', 'children'), Input('horn', 'value'))
def update_output(value):
    return ""
    if value:
        return pirask.send_bot_command("start_thread/horn")
    else:
        return pirask.send_bot_command("stop_thread/horn")

@callback(Output('avoid_obstacles_output', 'children'), Input('avoid_obstacles', 'value'))
def update_output(value):
    return ""
    if value:
        return pirask.send_bot_command("start_thread/avoid_obstacles")
    else:
        return pirask.send_bot_command("stop_thread/avoid_obstacles")

@callback(Output('vent_output', 'children'), Input('vent', 'value'))
def update_output(value):
    return ""
    return pirask.send_bot_command("vent")

@callback(Output('take_photo_output', 'children'), Input('take_photo', 'value'))
def update_output(value):
    return ""
    return pirask.send_bot_command("take_photo")


