from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import dash_daq as daq
import dash_bootstrap_components as dbc


from .music import get_music_objs
from .video import get_video_objs
from . import pirask


# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "18rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

@callback(Output("ipport_output", "children"), Input("ip_input", "value"), Input("port_input", "value"))
def update_output(ip_input, port_input):
    return f'Robot ip is {ip_input}:{port_input}'

sidebar = html.Div(
    [
        html.P("🤖Streamlit Bot Control", className="lead"),
        html.Hr(),
        dcc.Input(id="ip_input", type="text", placeholder="192.168.1.122", debounce=True),
        dcc.Input(id="port_input", type="text", placeholder="9001", debounce=True),
        html.Div(id="ipport_output"),

        daq.ToggleSwitch(id='connect_robot_switch', value=False, label='Robot connection switch', labelPosition='left'),
        html.Div(id='connect_robot_switch_output'),

    ] + get_video_objs() + get_music_objs() + [

        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Page 1", href="/page-1", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

@callback(Output('connect_robot_switch_output', 'children'), Input('connect_robot_switch', 'value'))
def update_output(value):
    if value:
        battery = 4
        battery_text = "🔋" * battery + "🪫" * (8 - battery)  # 🔵⭕⚪ 🔗💥
        return f"Status : {battery_text}"
    else:
        return "💥 server is not connected"
