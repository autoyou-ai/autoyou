"""Main entry point for the Kivy ADK application.

This script defines a multi‑screen Kivy application that embeds the
Google Agent Development Kit (ADK) dev UI in a WebView. When the app
starts it launches the ADK web server in the background and
exposes it on `localhost:8000`. The user is presented with a
mandatory splash screen containing terms and conditions; only after
agreeing may they proceed to the rest of the app. A settings screen
allows the user to securely enter and store their Robinhood
credentials, OTP and Google API key using the system keychain via
the `keyring` library. The main screen is a simple home page with
navigation to the settings and chat screens. The chat screen hosts
the ADK dev UI inside a WebView.

Key implementation details:

* A `before_agent_callback` in `autoyou_agent/agent.py` returns a
  `Content` object which causes the agent to skip its normal logic and
  immediately reply with "Hello"【812217260560387†L288-L297】. When the
  dev UI interacts with the agent, this callback ensures the
  demonstration agent always responds with a friendly greeting.
* The ADK web server is launched in `on_start()` using
  `subprocess.Popen(["adk", "web", "--no-reload"])`. ADK expects to
  find a module with a global `root_agent` in the current working
  directory; running the server from the project root allows ADK to
  discover the agent defined in `autoyou_agent/agent.py`【118314073243210†L588-L599】.
* User credentials are stored via the `keyring` module. This uses
  platform‑specific secure storage (e.g. Keychain on iOS/macOS).
  Fields are left empty if no value has been saved yet. When the
  user taps "Save", the values are persisted under the service name
  ``kivy_adk_app`` and unique keys for each field.
* The WebView is provided by the `kivy_garden.webview` garden widget.
  It points to `http://localhost:8000` by default. If the ADK
  process fails to start or is slow, the user may see a blank page
  initially until the server is ready.

Because the ADK CLI binds to localhost, the web view will work
equally in the iOS simulator and on device. For real devices you may
need to update the URL to `http://127.0.0.1:8000` depending on how
localhost is resolved by WebKit.
"""

from __future__ import annotations

import os
import subprocess
import sys
import threading
import time
from typing import Optional

# Configure Kivy for macOS high-DPI displays
os.environ['KIVY_DPI'] = '96'
os.environ['KIVY_METRICS_DENSITY'] = '1'
os.environ['KIVY_WINDOW_ICON'] = ''

from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp, sp
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle

import keyring

# Import TinyDB session service for initialization
try:
    from autoyou_agent.tinydb_session_service import TinyDBSessionService
except ImportError:
    TinyDBSessionService = None

try:
    # Import the WebView widget from the Kivy garden. The user must
    # install `kivy_garden.webview` via the requirements.txt.
    from kivy_garden.webview import WebView
except Exception as e:  # pragma: no cover
    WebView = None  # fallback placeholder

try:
    # Import pywebview as an alternative to kivy_garden.webview
    import webview as pywebview
except ImportError:
    pywebview = None


SERVICE_NAME = "kivy_adk_app"
KEY_USERNAME = "robinhood_username"
KEY_PASSWORD = "robinhood_password"
KEY_OTP = "robinhood_otp"
KEY_API_KEY = "google_api_key"


def start_adk_web_server() -> subprocess.Popen:
    """Launch the ADK dev UI as a background subprocess.

    ADK needs to run in the parent directory of the agent package so that
    it can automatically discover `root_agent`. This helper starts
    `adk web` with `--no-reload` to disable the auto‑reloader (which
    can create multiple processes)【118314073243210†L588-L599】. The caller is
    responsible for terminating the returned process when the app
    closes.

    Returns:
        A ``subprocess.Popen`` object representing the running
        server process.
    """
    # Determine the project root: the directory containing this
    # main.py file. ADK should be executed from here so it finds the
    # `autoyou_agent` package in ``sys.path``.
    project_root = os.path.dirname(os.path.abspath(__file__))

    # Build the command. `--no-reload` avoids the NotImplementedError on
    # some platforms and prevents multiple server instances from
    # spawning. See ADK documentation for details【118314073243210†L588-L599】.
    cmd = [
        sys.executable,
        "-m",
        "google.adk.cli.adk_cli",
        "web",
        "--no-reload",
    ]
    # Fall back to the shorter `adk` command if available in PATH.
    try:
        # Check if 'adk' is executable in PATH
        _ = subprocess.run(
            ["adk", "--help"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        cmd = ["adk", "web", "--no-reload"]
    except Exception:
        pass

    # Launch the process. We detach stdio so that the Kivy app does not
    # block. The server will log to the console of the iOS host when
    # running via Xcode.
    process = subprocess.Popen(
        cmd,
        cwd=project_root,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
    )
    return process


class SplashScreen(Screen):
    """Splash screen with terms and conditions.

    Displays the contents of ``assets/terms.txt`` in a scrollable
    view and provides an "I Agree" button to continue. The user must
    accept the terms before proceeding. Once accepted, this screen
    transitions to the settings screen for first‑time setup or
    directly to the home screen if credentials already exist.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Main layout with responsive padding
        layout = BoxLayout(
            orientation="vertical",
            padding=[dp(20), dp(30), dp(20), dp(20)],  # left, top, right, bottom
            spacing=dp(20)
        )
        
        # Title header
        title_label = Label(
            text="Terms and Conditions",
            font_size=sp(44),
            size_hint=(1, None),
            height=dp(100),
            halign="center",
            valign="middle",
            bold=True,
            color=(0.2, 0.2, 0.2, 1)
        )
        title_label.bind(size=lambda instance, value: setattr(instance, "text_size", value))
        layout.add_widget(title_label)
        
        # Load the terms from the assets folder
        terms_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "terms.txt")
        try:
            with open(terms_path, "r", encoding="utf-8") as f:
                terms_text = f.read()
        except FileNotFoundError:
            terms_text = "Terms and conditions could not be found."

        # Scrollable view for long text with better sizing
        scroll = ScrollView(
            size_hint=(1, 1),  # Take available space
            do_scroll_x=False,
            do_scroll_y=True,
            bar_width=dp(10),
            scroll_type=['bars', 'content']
        )
        
        # Container for the terms text with proper sizing
        terms_container = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            padding=[dp(15), dp(15)]
        )
        terms_container.bind(minimum_height=terms_container.setter('height'))
        
        terms_label = Label(
            text=terms_text,
            markup=False,  # Disable markup for cleaner rendering
            size_hint_y=None,
            halign="left",
            valign="top",
            font_size=sp(26),
            line_height=1.2,
            color=(0.3, 0.3, 0.3, 1)
        )
        
        # Simple and reliable text sizing
        def update_label_size(instance, *args):
            # Set text_size to container width minus padding
            container_width = scroll.width - dp(30)  # Account for padding
            if container_width > 0:
                terms_label.text_size = (container_width, None)
        
        # Bind to scroll view size changes for proper text wrapping
        scroll.bind(size=update_label_size)
        terms_label.bind(texture_size=lambda instance, value: setattr(instance, "height", value[1]))
        
        terms_container.add_widget(terms_label)
        scroll.add_widget(terms_container)
        layout.add_widget(scroll)

        # Button container for better spacing
        button_container = BoxLayout(
            orientation="vertical",
            size_hint=(1, None),
            height=dp(120),
            padding=[dp(0), dp(10), dp(0), dp(0)]
        )
        
        # Accept button with better styling and guaranteed clickability
        accept_btn = Button(
            text="I Agree",
            size_hint=(1, None),
            height=dp(80),
            font_size=sp(32),
            background_color=(0.2, 0.7, 0.2, 1),  # Green color
            background_normal='',  # Remove default background
            bold=True
        )
        accept_btn.bind(on_release=self.on_accept)
        
        button_container.add_widget(accept_btn)
        layout.add_widget(button_container)

        self.add_widget(layout)

    def on_accept(self, instance):
        """Handle acceptance of the terms and navigate forward."""
        app: KivyAdkApp = App.get_running_app()  # type: ignore[assignment]
        # Determine next screen: if credentials exist, go to home; else go to settings
        existing_user = keyring.get_password(SERVICE_NAME, KEY_USERNAME)
        if existing_user:
            app.manager.current = "home"
        else:
            app.manager.current = "settings"


class SettingsScreen(Screen):
    """Screen allowing the user to enter and save credentials.

    Contains text inputs for the Robinhood username, password, OTP and
    Google API key. Values are saved into the system keyring using
    ``keyring.set_password``. A "Save" button persists the data and
    then returns to the home screen.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.inputs: dict[str, TextInput] = {}
        
        # Main scrollable container for better mobile experience
        scroll = ScrollView(
            size_hint=(1, 1),
            do_scroll_x=False,
            do_scroll_y=True
        )
        
        # Main layout with responsive padding
        layout = BoxLayout(
            orientation="vertical",
            padding=[dp(25), dp(40), dp(25), dp(25)],
            spacing=dp(20),
            size_hint_y=None
        )
        layout.bind(minimum_height=layout.setter('height'))
        
        # Title header
        title_label = Label(
            text="Settings",
            font_size=sp(28),
            size_hint=(1, None),
            height=dp(60),
            halign="center",
            valign="middle",
            bold=True
        )
        title_label.bind(size=lambda instance, value: setattr(instance, "text_size", value))
        layout.add_widget(title_label)
        
        # Subtitle
        subtitle_label = Label(
            text="Enter your credentials below",
            font_size=sp(16),
            size_hint=(1, None),
            height=dp(40),
            halign="center",
            valign="middle",
            color=(0.7, 0.7, 0.7, 1)
        )
        subtitle_label.bind(size=lambda instance, value: setattr(instance, "text_size", value))
        layout.add_widget(subtitle_label)
        
        fields = [
            ("Robinhood Username", KEY_USERNAME, False),
            ("Robinhood Password", KEY_PASSWORD, True),
            ("One‑Time Password (OTP)", KEY_OTP, True),
            ("Google API Key", KEY_API_KEY, False),
        ]
        
        for label_text, key, password in fields:
            # Field container
            field_layout = BoxLayout(
                orientation="vertical",
                size_hint=(1, None),
                height=dp(80),
                spacing=dp(5)
            )
            
            # Label with better styling
            label = Label(
                text=label_text,
                size_hint=(1, None),
                height=dp(30),
                halign="left",
                valign="middle",
                font_size=sp(16),
                color=(0.2, 0.2, 0.2, 1)
            )
            label.bind(size=lambda instance, value: setattr(instance, "text_size", value))
            
            # Input field with better mobile styling
            input_field = TextInput(
                text=keyring.get_password(SERVICE_NAME, key) or "",
                multiline=False,
                password=password,
                size_hint=(1, None),
                height=dp(45),
                font_size=sp(16),
                padding=[dp(15), dp(10)],
                background_color=(0.95, 0.95, 0.95, 1),
                foreground_color=(0.2, 0.2, 0.2, 1)
            )
            
            self.inputs[key] = input_field
            field_layout.add_widget(label)
            field_layout.add_widget(input_field)
            layout.add_widget(field_layout)
        
        # Add some spacing before the save button
        layout.add_widget(Widget(size_hint=(1, None), height=dp(20)))
        
        # Save button with better mobile styling
        save_btn = Button(
            text="Save Settings",
            size_hint=(1, None),
            height=dp(55),
            font_size=sp(18),
            background_color=(0.2, 0.7, 0.2, 1),  # Green color
            bold=True
        )
        save_btn.bind(on_release=self.on_save)
        layout.add_widget(save_btn)
        
        # Back button
        back_btn = Button(
            text="Back to Home",
            size_hint=(1, None),
            height=dp(45),
            font_size=sp(16),
            background_color=(0.6, 0.6, 0.6, 1)  # Gray color
        )
        back_btn.bind(on_release=lambda x: setattr(App.get_running_app().manager, "current", "home"))
        layout.add_widget(back_btn)
        
        scroll.add_widget(layout)
        self.add_widget(scroll)

    def on_save(self, instance):
        """Persist the credentials and navigate to home."""
        for key, input_field in self.inputs.items():
            value = input_field.text.strip()
            if value:
                keyring.set_password(SERVICE_NAME, key, value)
            else:
                # If the user clears a field, remove it from the keyring
                try:
                    keyring.delete_password(SERVICE_NAME, key)
                except keyring.errors.PasswordDeleteError:
                    pass
        app: KivyAdkApp = App.get_running_app()  # type: ignore[assignment]
        app.manager.current = "home"


class HomeScreen(Screen):
    """Simple landing page after the splash and settings.

    Provides navigation to the settings screen and the chat screen.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Main layout with responsive padding
        layout = BoxLayout(
            orientation="vertical",
            padding=[dp(30), dp(50), dp(30), dp(30)],
            spacing=dp(25)
        )
        
        # App title/logo area
        title_label = Label(
            text="ADK Demo App",
            font_size=sp(72),
            size_hint=(1, None),
            height=dp(120),
            halign="center",
            valign="middle",
            bold=True,
            color=(0.2, 0.2, 0.2, 1)
        )
        title_label.bind(size=lambda instance, value: setattr(instance, "text_size", value))
        layout.add_widget(title_label)
        
        # Welcome message
        welcome_label = Label(
            text="Welcome! Choose an option below to get started.",
            font_size=sp(40),
            size_hint=(1, None),
            height=dp(100),
            halign="center",
            valign="middle",
            color=(0.5, 0.5, 0.5, 1)
        )
        welcome_label.bind(size=lambda instance, value: setattr(instance, "text_size", value))
        layout.add_widget(welcome_label)
        
        # Add some spacing
        layout.add_widget(Widget(size_hint=(1, None), height=dp(30)))
        
        # Chat button with icon-like styling
        btn_chat = Button(
            text="💬 Open Chat",
            size_hint=(1, None),
            height=dp(120),
            font_size=sp(48),
            background_color=(0.2, 0.6, 1, 1),  # Blue
            bold=True
        )
        btn_chat.bind(on_release=self.go_to_chat)
        layout.add_widget(btn_chat)
        
        # Settings button
        btn_settings = Button(
            text="⚙️ Settings",
            size_hint=(1, None),
            height=dp(120),
            font_size=sp(48),
            background_color=(0.7, 0.7, 0.7, 1),  # Gray
            bold=True
        )
        btn_settings.bind(on_release=self.go_to_settings)
        layout.add_widget(btn_settings)
        
        # Add flexible space to push content up
        layout.add_widget(Widget(size_hint=(1, 1)))
        
        self.add_widget(layout)
    
    def go_to_chat(self, instance):
        """Navigate to the chat screen."""
        app = App.get_running_app()
        app.manager.current = "chat"
    
    def go_to_settings(self, instance):
        """Navigate to the settings screen."""
        app = App.get_running_app()
        app.manager.current = "settings"


class ChatScreen(Screen):
    """Screen hosting the ADK web UI in a WebView."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Main layout
        layout = BoxLayout(orientation="vertical")
        
        # Top navigation bar
        nav_bar = BoxLayout(
            orientation="horizontal",
            size_hint=(1, None),
            height=dp(60),
            padding=[dp(10), dp(5)],
            spacing=dp(10)
        )
        
        # Back button
        back_btn = Button(
            text="← Back",
            size_hint=(None, 1),
            width=dp(140),
            font_size=sp(36),
            background_color=(0.6, 0.6, 0.6, 1)
        )
        back_btn.bind(on_release=lambda x: setattr(App.get_running_app().manager, "current", "home"))
        nav_bar.add_widget(back_btn)
        
        # Title
        nav_title = Label(
            text="Chat Interface",
            font_size=sp(44),
            halign="center",
            valign="middle",
            bold=True
        )
        nav_title.bind(size=lambda instance, value: setattr(instance, "text_size", value))
        nav_bar.add_widget(nav_title)
        
        # Settings button
        settings_btn = Button(
            text="⚙️",
            size_hint=(None, 1),
            width=dp(100),
            font_size=sp(40),
            background_color=(0.7, 0.7, 0.7, 1)
        )
        settings_btn.bind(on_release=lambda x: setattr(App.get_running_app().manager, "current", "settings"))
        nav_bar.add_widget(settings_btn)
        
        layout.add_widget(nav_bar)
        
        # Create content area with Safari launcher
        content_layout = BoxLayout(
            orientation="vertical",
            padding=[dp(20), dp(20)],
            spacing=dp(20)
        )
        
        # Welcome message
        welcome_label = Label(
            text="ADK Chat Interface",
            font_size=sp(56),
            halign="center",
            valign="middle",
            bold=True,
            color=(0.2, 0.6, 1, 1)
        )
        welcome_label.bind(size=lambda instance, value: setattr(instance, "text_size", value))
        content_layout.add_widget(welcome_label)
        
        # Description
        desc_label = Label(
            text="Click the button below to open the ADK interface in your browser.",
            font_size=sp(36),
            halign="center",
            valign="middle",
            color=(0.7, 0.7, 0.7, 1)
        )
        desc_label.bind(size=lambda instance, value: setattr(instance, "text_size", value))
        content_layout.add_widget(desc_label)
        
        # WebView launch button
        webview_btn = Button(
            text="🌐 Open ADK Interface",
            size_hint=(1, None),
            height=dp(120),
            font_size=sp(44),
            background_color=(0.2, 0.6, 1, 1),
            bold=True
        )
        webview_btn.bind(on_release=self.open_in_safari)
        content_layout.add_widget(webview_btn)
        
        # Alternative URL display
        url_label = Label(
            text="Direct URL: http://localhost:8000/dev-ui/?app=autoyou_agent",
            font_size=sp(32),
            halign="center",
            valign="middle",
            color=(0.6, 0.6, 0.6, 1)
        )
        url_label.bind(size=lambda instance, value: setattr(instance, "text_size", value))
        content_layout.add_widget(url_label)
        
        layout.add_widget(content_layout)
        self.add_widget(layout)
    
    def open_in_safari(self, instance):
        """Open the ADK interface using platform-specific WebView."""
        import platform
        url = "http://localhost:8000/dev-ui/?app=autoyou_agent"
        
        system = platform.system().lower()
        
        try:
            if system == 'ios':
                # Use iOS native WebView
                from ios import IOSWebView
                webview = IOSWebView()
                webview.load_url(url)
            elif system == 'android':
                # Use Android WebView
                from webview import WebView as AndroidWebView
                AndroidWebView(url)
            else:
                # Fallback for macOS/desktop - use webbrowser module
                import webbrowser
                webbrowser.open(url)
        except ImportError as e:
            print(f"Platform-specific WebView not available: {e}")
            # Fallback to webbrowser module
            import webbrowser
            webbrowser.open(url)
        except Exception as e:
            print(f"Error opening WebView: {e}")
            # Final fallback
            import webbrowser
            webbrowser.open(url)
    

    



class KivyAdkApp(App):
    """Main application class."""

    manager: ScreenManager
    _adk_process: Optional[subprocess.Popen] = None

    def build(self) -> ScreenManager:
        # Configure window for better resizing flexibility
        # Set minimum window size to ensure proper text rendering
        Window.minimum_width = dp(350)  # Adequate minimum width for text
        Window.minimum_height = dp(500)  # Adequate minimum height
        
        # Allow the window to be resizable
        Window.resizable = True
        
        # Set a reasonable default size for better initial experience
        Window.size = (dp(400), dp(600))  # Better default size
        
        # Fix for macOS touch coordinate issues
        if sys.platform == 'darwin':  # macOS
            Window.allow_screensaver = True
            # Ensure proper coordinate mapping
            from kivy.config import Config
            Config.set('graphics', 'multisamples', '0')
        
        # Create the screen manager and add screens
        self.manager = ScreenManager()
        self.manager.add_widget(SplashScreen(name="splash"))
        self.manager.add_widget(SettingsScreen(name="settings"))
        self.manager.add_widget(HomeScreen(name="home"))
        self.manager.add_widget(ChatScreen(name="chat"))
        self.manager.current = "splash"
        return self.manager

    def on_start(self) -> None:
        """Start the ADK dev server and initialize TinyDB when the app launches."""
        # Initialize TinyDB session service
        if TinyDBSessionService:
            try:
                # Initialize the session service to create the database file
                session_service = TinyDBSessionService("autoyou_sessions.json")
                print("TinyDB session service initialized successfully")
            except Exception as e:
                print(f"Failed to initialize TinyDB session service: {e}")
        
        # Launch the ADK server in a background thread to avoid blocking the UI
        def launch_server():
            self._adk_process = start_adk_web_server()

        threading.Thread(target=launch_server, daemon=True).start()

    def on_stop(self) -> None:
        """Terminate the ADK server when the app exits."""
        if self._adk_process and self._adk_process.poll() is None:
            try:
                self._adk_process.terminate()
            except Exception:
                pass


if __name__ == "__main__":
    KivyAdkApp().run()