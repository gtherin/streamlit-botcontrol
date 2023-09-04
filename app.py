import time
import requests
import streamlit as st
import streamlit.components.v1 as components

# from streamlit_botcontrol import bot_control

st.set_page_config(
    page_title="🤖 Streamlit Bot Control",
    initial_sidebar_state="expanded", layout="wide",
)

if "music" not in st.session_state:
    st.session_state.music = "nothing"
if "music_volume" not in st.session_state:
    st.session_state["music_volume"] = 60
if "video_color" not in st.session_state:
    st.session_state["video_color"] = "blue" # #ff0000
if "video_color_is" not in st.session_state:
    st.session_state.video_color_is = False
if "bot_ip" not in st.session_state:
    st.session_state["bot_ip"] = "192.168.0.47"
if "bot_port" not in st.session_state:
    st.session_state["bot_port"] = 9001
if "video_port" not in st.session_state:
    st.session_state["video_port"] = 9000
if "is_server_on" not in st.session_state:
    st.session_state["is_server_on"] = True


def send_bot_command(command, from_state=None, fake=False):
    if from_state is not None:
        command = command.replace("STATE", str(st.session_state[from_state]))
    command = f"http://{st.session_state.bot_ip}:{st.session_state.bot_port}/{command}"

    if not (send_request := st.session_state["is_server_on"] and not fake):
        command = "💥🚧" + command

    st.toast(command, icon="⚙️")
    print(command)
    if send_request:
        r = requests.get(command)
        print(r.text)


def send_video_command(command):
    if "video_color" == command:
        st.session_state.video_color_is =True

    if "video_color" in command:
        color = st.session_state.video_color if st.session_state.video_color_is else "off"
        command = f"video_color/{color.replace('#', 'DIEZ_')}"
    else:
        status = st.session_state[command]
        command = f"{command}/on" if status else f"{command}/off"

    send_bot_command(command)


def main():
    st.sidebar.header("🤖Streamlit Bot Control")
    st.sidebar.text_input("IP", key="bot_ip")
    st.sidebar.number_input("Port", key="bot_port", step=1)
    if not st.session_state["is_server_on"]:
        st.sidebar.write(f"Status : 💥 server is not connected")
    else:
        battery = 6
        battery_text = "🔋" * battery + "🪫" * (10 - battery) #🔵⭕⚪ 🔗💥
        st.sidebar.write(f"Status : {battery_text}")

    is_camera_on = st.sidebar.checkbox("🎥Switch on/off the camera", value=True)
    with st.sidebar.expander("🎥 Camera settings", expanded=is_camera_on):
        st.checkbox(
            "🫠Do face recognition ?",
            key="video_face_is",
            on_change=lambda: send_video_command("video_face_is"),
        )
        st.checkbox(
            "🏳️‍🌈Do detect colors ?",
            key="video_color_is",
            on_change=lambda: send_video_command("video_color_is"),
        )

        if 1:
            colors = ["red", "orange", "yellow", "green", "blue", "purple"]
            st.selectbox(
                "Pick color :",
                colors,
                key="video_color",
                on_change=lambda: send_video_command("video_color"), disabled=not st.session_state.video_color_is
            )
        else:
            st.color_picker(
                "Pick color :",
                key="video_color",
                on_change=lambda: send_video_command("video_color"), disabled=not st.session_state.video_color_is
            )
        st.checkbox(
            "📷Do recognize objects ?",
            key="video_object_is",
            on_change=lambda: send_video_command("video_object_is"),
        )

    st.sidebar.markdown("""<hr>""", unsafe_allow_html=True)
    st.sidebar.markdown(
        """<small>[streamlit-botcontrol](https://github.com/guydegnol/streamlit-botcontrol)  | Sep 2023 | [Guillaume Therin](https://guydegnol.github.io/)</small>""",
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns(9)
    with col1:
        st.subheader("Left")
        st.button("🚙:arrow_upper_left:", type="primary", on_click=lambda: send_bot_command("move/20/30/500"))
        st.button("🚙:arrow_left:", type="primary", on_click=lambda: send_bot_command("move/20/30/500"))
        st.button("🚙:arrow_lower_left:", type="primary", on_click=lambda: send_bot_command("move/-20/-30/500"))
    with col2:
        st.subheader("Middle")
        st.button("🚙:arrow_up:", type="primary", on_click=lambda: send_bot_command("move/50/0/500"))
        st.button("🚙:arrows_counterclockwise:", type="primary", on_click=lambda: send_bot_command("move/0/0/500"))
        st.button("🚙:arrow_down:", type="primary", on_click=lambda: send_bot_command("move/-20/0/500"))
    with col3:
        st.subheader("Right")
        st.button("🚙:arrow_upper_right:", type="primary", on_click=lambda: send_bot_command("move/20/-30/500"))
        st.button("🚙:arrow_right:", type="primary", on_click=lambda: send_bot_command("move/20/-30/500"))
        st.button("🚙:arrow_lower_right:", type="primary", on_click=lambda: send_bot_command("move/-20/30/500"))


    with col7:
        st.button("🎥:arrow_up:", type="primary", on_click=lambda: send_bot_command("servo/UP/10"))
        st.button("🎥:arrow_down:", type="primary", on_click=lambda: send_bot_command("servo/DOWN/10"))
    with col8:
        st.button("🎥:arrow_left:", type="primary", on_click=lambda: send_bot_command("servo/LEFT/10"))
    with col9:
        st.button("🎥:arrow_right:", type="primary", on_click=lambda: send_bot_command("servo/RIGHT/10"))

    if st.button("⚙️vent", type="primary", on_click=lambda: send_bot_command("vent")):
        st.write("Very cool")



    components.iframe("http://192.168.0.47:9000/mjpg", width=700, height=500)


    col1, col2 = st.columns(2)
    with col1:
        musics = ["nothing", "peace", "power", "spry"]
        st.selectbox(
            "Select a music to play",
            musics,
            key="music",
            on_change=lambda: send_bot_command("music_play/STATE", from_state="music"),
        )

    with col2:
        st.slider(
            "Music level",
            0,
            100,
            key="music_volume",
            on_change=lambda: send_bot_command("music_volume/STATE", from_state="music_volume"),
        )

    col1, col2 = st.columns(2)

    with col1:
        st.text_input("Read the previous text", key="play_text")

    with col2:
        if st.button(
            "Say that text",
            type="primary",
            on_click=lambda: send_bot_command("say_text/STATE", from_state="play_text"),
        ):
            st.write("Why hello there")


if __name__ == "__main__":
    main()
