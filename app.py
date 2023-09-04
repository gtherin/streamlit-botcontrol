import time
import requests
import streamlit as st
import streamlit.components.v1 as components

# from streamlit_botcontrol import bot_control

st.set_page_config(
    page_title="🤖 Streamlit Bot Control",
    initial_sidebar_state="expanded",
    layout="wide",
)

default_data = {
    "music": "nothing",
    "video_color": "blue",
    "music_volume": 60,
    "bot_port": 9001,
    "video_port": 9000,
    "is_on": False,
    "video_color_is": False,
    "bot_ip": "192.168.0.47",
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
    print(command)
    if send_request:
        r = requests.get(command)
        print(r.text)


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


def main():
    st.sidebar.header("🤖Streamlit Bot Control")
    st.sidebar.text_input("IP", key="bot_ip")
    st.sidebar.number_input("Port", key="bot_port", step=1)
    if not st.session_state["is_on"]:
        st.sidebar.button(
            "Connect to the bot",
            type="primary",
            on_click=lambda: set_var("is_on", True),
        )
        st.sidebar.write(f"Status : 💥 server is not connected")
    else:
        battery = 6
        battery_text = "🔋" * battery + "🪫" * (10 - battery)  # 🔵⭕⚪ 🔗💥
        st.sidebar.button(
            "Disconnect to the bot",
            type="primary",
            on_click=lambda: set_var("is_on", False),
        )
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
        """<small>[streamlit-botcontrol](https://github.com/guydegnol/streamlit-botcontrol)  | Sep 2023 | [Guillaume Therin](https://guydegnol.github.io/)</small>""",
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
        st.button(
            "➿line_following",
            type="primary",
            on_click=lambda: send_bot_command("line_following"),
            disabled=not st.session_state.is_on,
        )

    components.iframe("http://192.168.0.47:9000/mjpg", width=700, height=500)

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
