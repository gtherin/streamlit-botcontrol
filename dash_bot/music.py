from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import dash_daq as daq
import dash_bootstrap_components as dbc

from . import pirask

def get_music_objs():
    return [
            daq.ToggleSwitch(id='music_switch', value=False, label='🎶Switch on/off the music', labelPosition='left'),
            html.Div(id='music_switch_output'),
            dcc.Dropdown(["peace", "power", "spry"], None, id='music_song'),
            html.Div(id='music_song_output'),
            dcc.Slider(0, 100, 10, value=60, id='music_level'),
            html.Div(id='music_level_output'),
        ]

@callback(Output('music_switch_output', 'children'), Input('music_switch', 'value'))
def update_output(value):
    return f"Status : {value}"

@callback(Output('music_song_output', 'children'), Input('music_song', 'value'))
def update_output(music_song):
    if music_song is None:
        return pirask.send_bot_command(f"music_play/off", fake=True)
    else:
        return pirask.send_bot_command(f"say_text/{music_song}", fake=True)

@callback(Output('music_level_output', 'children'), Input('music_level', 'value'))
def update_output(music_level):
    return pirask.send_bot_command(f"music_play/{music_level}", fake=True)


def get_audio_objs():
    return [
            dcc.Dropdown(["francais", "anglais"], None, id='language'),
            html.Div(id='language_output'),
            daq.ToggleSwitch(id='play_text', value=False, label='🎶play_text', labelPosition='left'),
            html.Div(id='play_text_output'),
        ]


@callback(Output('play_text_output', 'children'), Input('play_text', 'value'))
def update_output(play_text):
    return pirask.send_bot_command(f"say_text/{play_text}", fake=True)
