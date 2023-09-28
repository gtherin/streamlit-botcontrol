import time
import requests
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image, ImageDraw

from streamlit_botcontrol import streamlit_botcontrol

st.set_page_config(
    page_title="Streamlit Bot Control",
    initial_sidebar_state="expanded",
    page_icon="🤖",
    layout="wide",
)

if "joy_on" not in st.session_state:
    st.session_state["joy_x"] = 0
    st.session_state["joy_y"] = 0
    st.session_state["joy_on"] = False

import time
import numpy as np


default_data = {
    "music": "nothing",
    "video_color": "blue",
    "music_volume": 60,
    "bot_port": 9001,
    "video_port": 9000,
    "is_on": False,
    "video_color_is": False,
    "bot_ip": "192.168.1.122",
}

for k, v in default_data.items():
    if k not in st.session_state:
        st.session_state[k] = v


def send_bot_command(command, from_state=None, fake=False):
    if from_state is not None:
        command = command.replace("STATE", str(st.session_state[from_state]))
    command = f"http://{st.session_state.bot_ip}:{st.session_state.bot_port}/{command}"

    if not (send_request := st.session_state["is_on"] and not fake):
        command = "💥🚧" + command

    st.toast(command, icon="⚙️")
    if send_request:
        r = requests.get(command)
        print(r.text)


def send_bot_thread(command):
    if st.session_state[command]:
        command = "start_thread/" + command
    else:
        command = "stop_thread/" + command
    send_bot_command(command)


def send_video_command(command):
    if "video_color" == command:
        st.session_state.video_color_is = True

    if "video_color" in command:
        color = st.session_state.video_color if st.session_state.video_color_is else "off"
        command = f"video_color/{color.replace('#', 'DIEZ_')}"
    else:
        status = st.session_state[command]
        command = f"{command}/on" if status else f"{command}/off"

    send_bot_command(command)


def set_var(variable, value):
    st.session_state[variable] = value


def generate_targets():
    from cairosvg import svg2png

    caliases = dict(
        zip(
            ["purple", "red", "orange", "blue", "green", "yellow", "black"],
            ["#581845", "#C70039", "#FF5733", "#4F77AA", "#52DE97", "#FBE555", "black"],
        )
    )

    def generate(color, tcolor, text, filename):
        tcolor, color = caliases[tcolor], caliases[color]
        x0 = 44

        svg2png(bytestring=f"""<svg xmlns="http://www.w3.org/2000/svg" width="300" height="300">\n
<style>
        .Rrrrr {{font: bold 40px serif;fill: {tcolor};}}
</style>
<path fill="#FFF" stroke="{color}" stroke-width="50" d="m149,25a125,125 0 1,0 2,0zm2,100a25,25 0 1,1-2,0z"/>
<line x1="150" y1="0" x2="150" y2="300" stroke="{caliases['blue']}" stroke-width="3" />
<line x1="0" y1="150" x2="300" y2="150" stroke="{caliases['blue']}" stroke-width="3" />
<line x1="{x0}" y1="{x0}" x2="{300-x0}" y2="{300-x0}" stroke="{caliases['blue']}" stroke-width="3" />
<line x1="{x0}" y1="{300-x0}" x2="{300-x0}" y2="{x0}" stroke="{caliases['blue']}" stroke-width="3" />
{text}\n</svg>""", write_to=filename)

    generate("green", 'red', '<text x="60" y="160" class="Rrrrr">Camera</text>', "joy_camera.png")
    generate("orange", 'purple', '<text x="60" y="160" class="Rrrrr">Remote</text>', "joy_remote.png")


def get_ellipse_coords(point: tuple[int, int]) -> tuple[int, int, int, int]:
    center = point
    radius = 10
    return (center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius)

def main():

    if 1:
        generate_targets()
    from PIL import Image

    col1, col2 = st.columns(2)
    with col1:
        with Image.open("joy_remote.png") as img:
            draw_remote = ImageDraw.Draw(img)
            value_remote = streamlit_botcontrol("joy_remote.png", width=250, key="joy_remote")

        st.session_state["joy_on"] = value_remote
        if st.session_state["joy_on"]:

            xmax, ymax = 225, 225
            xmiddle, ymiddle = int(0.5*xmax), int(0.5*ymax)
            xs = np.linspace(value_remote["x"], xmiddle, 3)
            ys = np.linspace(value_remote["y"], ymiddle, 3)

            xcs, yxc = int(200*(value_remote["x"]-xmiddle)/xmax), int(-200*(value_remote["y"]-ymiddle)/ymax)
            st.write(f"move/{yxc}/{xcs}/500")
            send_bot_command(f"move/{yxc}/{xcs}/200")
            st.write(f"{xcs}, {yxc}")

            for t in range(3):
                point = xs[t], ys[t]
                point = xmiddle, ymiddle

                coords = get_ellipse_coords(point)
                draw_remote.ellipse(coords, fill="blue")
            st.session_state["joy_on"] = False
        
        st.write(value_remote)

    with col2:
        with Image.open("joy_camera.png") as img:
            draw_camera = ImageDraw.Draw(img)
            value_camera = streamlit_botcontrol("joy_camera.png", width=250, key="joy_camera")

        st.session_state["joy_on"] = value_camera
        if st.session_state["joy_on"]:

            xmax, ymax = 225, 225
            xmiddle, ymiddle = int(0.5*xmax), int(0.5*ymax)
            xs = np.linspace(value_camera["x"], xmiddle, 3)
            ys = np.linspace(value_camera["y"], ymiddle, 3)

            xcs, yxc = int(200*(value_camera["x"]-xmiddle)/xmax), int(-200*(value_camera["y"]-ymiddle)/ymax)
            st.write(f"move/{yxc}/{xcs}/500")
            send_bot_command(f"move/{yxc}/{xcs}/200")
            #send_bot_command("servo/UP/10")
            #send_bot_command("servo/DOWN/10")
            #send_bot_command("servo/LEFT/10")

            st.write(f"{xcs}, {yxc}")

            for t in range(3):
                point = xs[t], ys[t]
                point = xmiddle, ymiddle

                coords = get_ellipse_coords(point)
                draw_remote.ellipse(coords, fill="blue")
            st.session_state["joy_on"] = False

        st.write(value_camera)






    st.sidebar.header("🤖Streamlit Bot Control")
    st.sidebar.text_input("IP", key="bot_ip")
    st.sidebar.number_input("Port", key="bot_port", step=1)
    if not st.session_state["is_on"]:
        st.sidebar.button("Connect to the bot", type="primary", on_click=lambda: set_var("is_on", True))
        st.sidebar.write(f"Status : 💥 server is not connected")
    else:
        battery = 6
        battery_text = "🔋" * battery + "🪫" * (10 - battery)  # 🔵⭕⚪ 🔗💥
        st.sidebar.button("Disconnect to the bot", type="primary", on_click=lambda: set_var("is_on", False))
        st.sidebar.write(f"Status : {battery_text}")

    is_camera_on = st.sidebar.checkbox("🎥Switch on/off the camera", value=True, disabled=not st.session_state.is_on)
    with st.sidebar.expander("🎥 Camera settings", expanded=is_camera_on):
        st.checkbox(
            "🫠Do face recognition ?",
            key="video_face_is",
            on_change=lambda: send_video_command("video_face_is"),
            disabled=not st.session_state.is_on,
        )
        st.checkbox(
            "🏳️‍🌈Do detect colors ?",
            key="video_color_is",
            on_change=lambda: send_video_command("video_color_is"),
            disabled=not st.session_state.is_on,
        )

        if 1:
            colors = ["red", "orange", "yellow", "green", "blue", "purple"]
            st.selectbox(
                "Pick color :",
                colors,
                key="video_color",
                on_change=lambda: send_video_command("video_color"),
                disabled=not st.session_state.video_color_is,
            )
        else:
            st.color_picker(
                "Pick color :",
                key="video_color",
                on_change=lambda: send_video_command("video_color"),
                disabled=not st.session_state.video_color_is,
            )
        st.checkbox(
            "📷Do recognize objects ?",
            key="video_object_is",
            on_change=lambda: send_video_command("video_object_is"),
            disabled=not st.session_state.is_on,
        )

    is_music_on = st.sidebar.checkbox("🎶Switch on/off the music", value=True, disabled=not st.session_state.is_on)
    with st.sidebar.expander("🎶 Music settings", expanded=is_music_on):
        musics = ["nothing", "peace", "power", "spry"]
        st.selectbox(
            "Select a music to play",
            musics,
            key="music",
            on_change=lambda: send_bot_command("music_play/STATE", from_state="music"),
            disabled=not st.session_state.is_on,
        )

        st.slider(
            "Music level",
            0,
            100,
            key="music_volume",
            on_change=lambda: send_bot_command("music_volume/STATE", from_state="music_volume"),
            disabled=not st.session_state.is_on,
        )

    st.sidebar.markdown("""<hr>""", unsafe_allow_html=True)
    st.sidebar.markdown(
        """<small>[streamlit-botcontrol](https://github.com/gtherin/streamlit-botcontrol)  | Sep 2023 | [Guillaume Therin](https://guydegnol.github.io/)</small>""",
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns(9)
    with col1:
        st.subheader("Left")
        st.button(
            "🚙:arrow_upper_left:",
            type="primary",
            on_click=lambda: send_bot_command("move/20/-30/500"),
            disabled=not st.session_state.is_on,
        )
        st.button(
            "🚙:arrow_left:",
            type="primary",
            on_click=lambda: send_bot_command("move/20/-30/500"),
            disabled=not st.session_state.is_on,
        )
        st.button(
            "🚙:arrow_lower_left:",
            type="primary",
            on_click=lambda: send_bot_command("move/-20/-30/500"),
            disabled=not st.session_state.is_on,
        )
    with col2:
        st.subheader("Middle")
        st.button(
            "🚙:arrow_up:",
            type="primary",
            on_click=lambda: send_bot_command("move/50/0/500"),
            disabled=not st.session_state.is_on,
        )
        st.button(
            "🚙:arrows_counterclockwise:",
            type="primary",
            on_click=lambda: send_bot_command("move/0/0/500"),
            disabled=not st.session_state.is_on,
        )
        st.button(
            "🚙:arrow_down:",
            type="primary",
            on_click=lambda: send_bot_command("move/-20/0/500"),
            disabled=not st.session_state.is_on,
        )
    with col3:
        st.subheader("Right")
        st.button(
            "🚙:arrow_upper_right:",
            type="primary",
            on_click=lambda: send_bot_command("move/20/30/500"),
            disabled=not st.session_state.is_on,
        )
        st.button(
            "🚙:arrow_right:",
            type="primary",
            on_click=lambda: send_bot_command("move/20/30/500"),
            disabled=not st.session_state.is_on,
        )
        st.button(
            "🚙:arrow_lower_right:",
            type="primary",
            on_click=lambda: send_bot_command("move/20/30/500"),
            disabled=not st.session_state.is_on,
        )

    with col6:
        st.subheader("Camera")
        st.subheader("Up")
        st.subheader("Down")
        st.subheader("Various")

    with col7:
        st.subheader("Tilt")
        st.button(
            "🎥:arrow_up:",
            type="primary",
            on_click=lambda: send_bot_command("servo/UP/10"),
            disabled=not st.session_state.is_on,
        )
        st.button(
            "🎥:arrow_down:",
            type="primary",
            on_click=lambda: send_bot_command("servo/DOWN/10"),
            disabled=not st.session_state.is_on,
        )
    with col8:
        st.subheader("Left")
        st.button(
            "🎥:arrow_left:",
            type="primary",
            on_click=lambda: send_bot_command("servo/LEFT/10"),
            disabled=not st.session_state.is_on,
        )
        st.button(
            "⚙️vent", type="primary", on_click=lambda: send_bot_command("vent"), disabled=not st.session_state.is_on
        )
        st.button(
            "⛐ avoid_obstacles",
            type="primary",
            on_click=lambda: send_bot_command("avoid_obstacles"),
            disabled=not st.session_state.is_on,
        )
    with col9:
        st.subheader("Right")
        st.button(
            "🎥:arrow_right:",
            type="primary",
            on_click=lambda: send_bot_command("servo/RIGHT/10"),
            disabled=not st.session_state.is_on,
        )
        st.button(
            "📷take_photo",
            type="primary",
            on_click=lambda: send_bot_command("take_photo"),
            disabled=not st.session_state.is_on,
        )
        if 0:
            st.button(
                "➿line_following",
                type="primary",
                on_click=lambda: send_bot_command("line_following"),
                disabled=not st.session_state.is_on,
            )

    st.toggle("➿line_following", key="line_following", on_change=lambda: send_bot_thread("line_following"))
    st.toggle("infinite_loop", key="infinite_loop", on_change=lambda: send_bot_thread("infinite_loop"))
    st.toggle("horn", key="horn", on_change=lambda: send_bot_thread("horn"))

    if 0:
        import streamlit_toggle as tog

        tog.st_toggle_switch(
            label="Label",
            key="Key1",
            on_color="primary",
        )

    components.iframe("http://192.168.1.122:9000/mjpg", width=700, height=500)

    col1, col2, col3 = st.columns(3)

    with col1:
        languages = ["francais", "anglais"]
        st.selectbox("Select language :", languages, key="language")
    with col2:
        st.text_input("Read the previous text", key="play_text")

    with col3:
        st.button(
            "Say that text",
            type="primary",
            on_click=lambda: send_bot_command("say_text/STATE", from_state="play_text"),
            disabled=not st.session_state.is_on,
        )


if __name__ == "__main__":
    main()
