import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"
import React, { ReactNode } from "react"
import { useState } from 'react';
//import {Joystick} from "./Joystick"
//import {Game} from "./TicTacToe"


enum InteractionEvents {
  PointerDown = "pointerdown",
  PointerMove = "pointermove",
  PointerUp = "pointerup"
}


interface State {
  numClicksU: number
  numClicksD: number
  numClicksL: number
  numClicksR: number
  isFocused: boolean
}

/**
 * This is a React-based component template. The `render()` function is called
 * automatically when your component should be re-rendered.
 */
class BotControl extends StreamlitComponentBase<State> {
  public state = { numClicksU: 0, numClicksD: 0, numClicksL: 0, numClicksR: 0, isFocused: false }

  public render = (): ReactNode => {
    // Arguments that are passed to the plugin in Python are accessible
    // via `this.props.args`. Here, we access the "name" arg.
    const name = this.props.args["name"]

    // Streamlit sends us a theme object via props that we can use to ensure
    // that our component has visuals that match the active theme in a
    // streamlit app.
    const { theme } = this.props
    const style: React.CSSProperties = {}
    const joyStyle = {
      width: '200px',
      height: '200px',
      margin: '50px',
    };

    // Maintain compatibility with older versions of Streamlit that don't send
    // a theme object.
    if (theme) {
      // Use the theme object to style our button border. Alternatively, the
      // theme style is defined in CSS vars.
      const borderStyling = `1px solid ${this.state.isFocused ? theme.primaryColor : "gray"
        }`
      style.border = borderStyling
      style.outline = borderStyling
    }

    // Show a button and some text.
    // When the button is clicked, we'll increment our "numClicks" state
    // variable, and send its new value back to Streamlit, where it'll
    // be available to the Python program.
    //return Game();

    return (
      <span>
        Bonjour, {name}! &nbsp;
        <button
          style={style}
          onClick={this.onClickedU}
          disabled={this.props.disabled}
          onFocus={this._onFocus}
          onBlur={this._onBlur}
        >
          Go up
        </button>
        <button
          style={style}
          onClick={this.onClickedD}
          disabled={this.props.disabled}
          onFocus={this._onFocus}
          onBlur={this._onBlur}
        >
          Go down
        </button>
        <button
          style={style}
          onClick={this.onClickedL}
          disabled={this.props.disabled}
          onFocus={this._onFocus}
          onBlur={this._onBlur}
        >
          Go left
        </button>
        <button
          style={style}
          onClick={this.onClickedR}
          disabled={this.props.disabled}
          onFocus={this._onFocus}
          onBlur={this._onBlur}
        >
          Go right
        </button>
        <div id="joy2Div" style={joyStyle}></div>
		<div>
			Posizione X:<input id="joy3PosizioneX" type="text" /><br />
			Posizione Y:<input id="joy3PosizioneY" type="text" /><br />
			Direzione:<input id="joy3Direzione" type="text" /><br />
			X :<input id="joy3X" type="text" />
			Y :<input id="joy3Y" type="text" />
		</div>
      </span>
    )
  }

  /** Click handler for our "Click Me!" button. */
  private onClickedU = (): void => {
    // Increment state.numClicks, and pass the new value back to
    // Streamlit via `Streamlit.setComponentValue`.
    this.setState(
      prevState => ({ numClicksU: 1 }),
      () => Streamlit.setComponentValue(this.state.numClicksU)
    )
  }
  private onClickedD = (): void => {
    // Increment state.numClicks, and pass the new value back to
    // Streamlit via `Streamlit.setComponentValue`.
    this.setState(
      prevState => ({ numClicksD: 2 }),
      () => Streamlit.setComponentValue(this.state.numClicksD)
    )
  }
  private onClickedL = (): void => {
    // Increment state.numClicks, and pass the new value back to
    // Streamlit via `Streamlit.setComponentValue`.
    this.setState(
      prevState => ({ numClicksL: 3 }),
      () => Streamlit.setComponentValue(this.state.numClicksL)
    )
  }
  private onClickedR = (): void => {
    // Increment state.numClicks, and pass the new value back to
    // Streamlit via `Streamlit.setComponentValue`.
    this.setState(
      prevState => ({ numClicksR: 4 }),
      () => Streamlit.setComponentValue(this.state.numClicksR)
    )
  }

  /** Focus handler for our "Click Me!" button. */
  private _onFocus = (): void => {
    this.setState({ isFocused: true })
  }

  /** Blur handler for our "Click Me!" button. */
  private _onBlur = (): void => {
    this.setState({ isFocused: false })
  }
}

// "withStreamlitConnection" is a wrapper function. It bootstraps the
// connection between your component and the Streamlit app, and handles
// passing arguments from Python -> Component.
//
// You don't need to edit withStreamlitConnection (but you're welcome to!).
export default withStreamlitConnection(BotControl)

//export default withStreamlitConnection(Joystick)
