import os
import streamlit
import streamlit.components.v1 as components

# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
_RELEASE = not ("DEV_MODE" in os.environ["DEV_MODE"] and os.environ["DEV_MODE"] == "True")

# Declare a Streamlit component. `declare_component` returns a function
# that is used to create instances of the component. We're naming this
# function "_component_func", with an underscore prefix, because we don't want
# to expose it directly to users. Instead, we will create a custom wrapper
# function, below, that will serve as our component's public API.

# It's worth noting that this call to `declare_component` is the
# *only thing* you need to do to create the binding between Streamlit and
# your component frontend. Everything else we do in this file is simply a
# best practice.


if not _RELEASE:
    # Pass `url` here to tell Streamlit that the component will be served
    _component_func = components.declare_component("bot_control", url="http://localhost:3001")
else:
    # When we're distributing a production version of the component, we'll
    # replace the `url` param with `path`, and point it to the component's
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend-react/build")
    _component_func = components.declare_component("bot_control", path=build_dir)


def bot_control(name, key=None):
    """Create a new instance of "bot_control".

    Parameters
    ----------
    name: str
        The name of the thing we're saying hello to. The component will display
        the text "Hello, {name}!"
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.

    Returns
    -------
    int
        The number of times the component's "Click Me" button has been clicked.
        (This is the value passed to `Streamlit.setComponentValue` on the
        frontend.)

    """
    # "default" is a special argument that specifies the initial return
    # value of the component before the user has interacted with it.
    direction = _component_func(name=name, key=key, default=0)

    directions = {1: "UP", 2: "DOWN", 3: "LEFT", 4: "RIGHT", 5: "STOP"}

    return directions[direction]


# Add some test code to play with the component while it's in development.
# During development, we can run this just as we would any other Streamlit
if not _RELEASE:
    import streamlit as st

    st.subheader("Component with constant args")

    # Create an instance of our component with a constant `name` arg, and
    # print its output value.
    num_clicks = bot_control("World")
    print("FFFFFFFFFFFFFF", num_clicks, "GGGGGGGGGGGG")

    st.markdown("You've clicked %s times!" % int(num_clicks))

    st.markdown("---")
    st.subheader("Component with variable args")

    # Create a second instance of our component whose `name` arg will vary
    # based on a text_input widget.
    #
    # We use the special "key" argument to assign a fixed identity to this
    # component instance. By default, when a component's arguments change,
    # it is considered a new instance and will be re-mounted on the frontend
    # and lose its current state. In this case, we want to vary the component's
    # "name" argument without having it get recreated.
    name_input = st.text_input("Enter a name", value="Streamlit")
    num_clicks = bot_control(name_input, key="foo")
    st.markdown("You've clicked %s times!" % int(num_clicks))
    st.write(num_clicks)
