from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import dash_daq as daq
import dash_bootstrap_components as dbc

from . import pirask


def get_video_objs():
    return [
        daq.ToggleSwitch(id='connect_camera_switch', value=False, label='🎥Switch on/off the camera', labelPosition='left'),
        html.Div(id='connect_camera_switch_output'),

        daq.ToggleSwitch(id='video_face_switch', value=False, label='🫠Do face recognition ?', labelPosition='left'),
        html.Div(id='video_face_switch_output'),

        daq.ToggleSwitch(id='video_color_switch', value=False, label='🏳️‍🌈Do detect colors ?', labelPosition='left'),
        html.Div(id='video_color_switch_output'),

        dcc.Dropdown(["red", "orange", "yellow", "green", "blue", "purple"], None, id='video_color'),
        html.Div(id='video_color_output'),

        daq.ToggleSwitch(id='video_object_switch', value=False, label='📷Do recognize objects ?', labelPosition='left'),
        html.Div(id='video_object_switch_output'),
    ]

@callback(Output('connect_camera_switch_output', 'children'), Input('connect_camera_switch', 'value'))
def update_output(value):
    return f"Status : {value}"

@callback(Output('video_face_switch_output', 'children'), Input('video_face_switch', 'value'))
def update_output(value):
    if value:
        return pirask.send_bot_command("video_face_is/on", fake=True)
    else:
        return pirask.send_bot_command("video_face_is/off", fake=True)


@callback(Output('video_color_switch_output', 'children'), Input('video_color_switch', 'value'))
def update_output(value):
    if value:
        return pirask.send_bot_command("video_color_is/on", fake=True)
    else:
        return pirask.send_bot_command("video_color_is/off", fake=True)

@callback(Output('video_color_output', 'children'), Input('video_color', 'value'))
def update_output(value):
    return f'You have selected {value}'

@callback(Output('video_object_switch_output', 'children'), Input('video_object_switch', 'value'))
def update_output(value):
    return f"Status : {value}"
