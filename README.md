# Kivy ADK iOS Demo App

This repository contains a simple Kivy application that wraps Google’s Agent Development Kit (ADK) Dev UI inside a native iOS app.  It was designed for macOS Ventura 13.7 and is compatible with Xcode 15.2.  The application demonstrates how to start the ADK development server from within Python, display a splash screen with terms and conditions, collect credentials on a settings screen and then render the ADK web UI inside a WebView.

## Features

* **Splash screen** – The app starts with a full screen splash page that explains that this software is provided for educational purposes only.  Users must accept the terms and conditions before continuing.
* **Settings screen** – A dedicated settings page allows you to securely store a Robinhood username, password, optional one‑time passcode (OTP) and a Google API key.  Values are persisted with the [`keyring`](https://pypi.org/project/keyring/) library which stores secrets in the macOS keychain.  Non‑secret preferences (such as whether an OTP is required) are stored in a small JSON file.
* **Embedded ADK UI** – When you navigate to the chat view, the application automatically spawns the `adk web` server in the background.  A WebView then loads the local development UI on `http://127.0.0.1:8000`.  According to Google’s quickstart documentation the Dev UI can be launched by running `adk web` and then visiting the URL provided (usually `http://localhost:8000`)【179694710804837†L575-L589】.
* **Demo agent** – The included agent (`adk_agent/agent.py`) registers a simple ADK LLM agent called `hello_agent` which always returns the string “Hello.”  It uses a `before_agent_callback` to short‑circuit the LLM call and return a static `google.genai.types.Content` object.  The ADK callback documentation shows that returning a `types.Content` instance from the `before_agent_callback` will skip the usual LLM invocation【208299303522157†L221-L256】.

## File layout

```
kivy_adk_app/
├── adk_agent/
│   ├── __init__.py       – exposes the `root_agent` object for ADK
│   └── agent.py         – defines the `hello_agent` and callback
├── assets/
│   └── terms.txt        – text displayed on the splash screen
├── main.py              – Kivy application entry point
├── requirements.txt     – Python dependencies
└── README.md            – this document
```

## Running locally

1. **Install dependencies**.  Create a virtual environment and install the requirements:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt

   # Install the webview widget from Kivy Garden (only required once)
   pip install kivy_garden
   garden install webview
   ```

2. **Run the app**.  Execute `python main.py`.  When you open the chat page for the first time the app will launch the ADK development server and embed it in a WebView.  The ADK UI allows you to choose the `hello_agent` from the drop‑down menu and interact with it.  Because the agent’s `before_agent_callback` always returns “Hello,” every message you send will receive that response.

## iOS packaging

This project is structured to work with [kivy‑ios](https://kivy.org/doc/stable/guide/packaging-ios.html).  On your Mac you can build an Xcode project as follows:

```bash
# Install kivy‑ios (requires Homebrew, Xcode command line tools and a python3 interpreter)
git clone https://github.com/kivy/kivy-ios
cd kivy-ios
python3 -m pip install -r requirements.txt

# Build the required recipes
python3 toolchain.py build python3 kivy pygments openssl certifi pillow sdl2_image sdl2_mixer sdl2_ttf

# Create an Xcode project for the app.  Replace /path/to/kivy_adk_app with the actual path.
python3 toolchain.py create ios kivy_adk_app /path/to/kivy_adk_app

# Open the generated Xcode project and run on the simulator or device
open apps/kivy_adk_app-ios/kivy_adk_app.xcodeproj
```

For convenience a minimal `buildozer.spec` is also provided, although it is **not** required for packaging through `kivy‑ios`.  It demonstrates the necessary requirements and can be used to build an iOS package if you prefer Buildozer on macOS.

## Warning about trading functionality

The included agent is only a placeholder.  When you later replace the demo agent with a real trading agent, ensure that you comply with all applicable regulations and that users are clearly informed about the risks involved.  This repository currently displays a terms and conditions message during startup but you must update the wording to reflect your actual use case.
