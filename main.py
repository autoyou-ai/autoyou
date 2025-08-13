"""Main entry point for the Kivy ADK application.

This script defines a multi‑screen Kivy application that embeds the
Google Agent Development Kit (ADK) dev UI in a WebView. When the app
starts it launches the ADK web server in the background and
exposes it on `localhost:8000`. The user is presented with a
mandatory splash screen containing terms and conditions; only after
agreeing may they proceed to the rest of the app. A settings screen
allows the user to securely enter and store their Robinhood
credentials, OTP and Google API key using JsonStore for cross-platform
compatibility. The main screen is a simple home page with
navigation to the settings and chat screens. The chat screen hosts
the ADK dev UI inside a WebView.

Key implementation details:

* A `before_agent_callback` in `robinhood_agent/agent.py` returns a
  `Content` object which causes the agent to skip its normal logic and
  immediately reply with "Hello"【812217260560387†L288-L297】. When the
  dev UI interacts with the agent, this callback ensures the
  demonstration agent always responds with a friendly greeting.
* The ADK web server is launched in `on_start()` using
  `subprocess.Popen(["adk", "web", "--no-reload"])`. ADK expects to
  find a module with a global `root_agent` in the current working
  directory; running the server from the project root allows ADK to
  discover the agent defined in `robinhood_agent/agent.py`【118314073243210†L588-L599】.
* User credentials are stored via JsonStore for cross-platform
  compatibility. Fields are left empty if no value has been saved yet.
  When the user taps "Save", the values are persisted in a JSON file
  in the app's user data directory.
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

# Standard library imports
import asyncio
import logging
import os
import subprocess
import sys
import threading
import time
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Optional

# Configure Kivy environment for cross-platform compatibility
os.environ['KIVY_DPI'] = '96'
os.environ['KIVY_METRICS_DENSITY'] = '1'
os.environ['KIVY_WINDOW_ICON'] = ''

# Third-party imports
import uvicorn
from fastapi import FastAPI

# Kivy imports
from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.lang import Builder
from kivy.metrics import dp, sp
from kivy.properties import ObjectProperty, StringProperty
from kivy.storage.jsonstore import JsonStore
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

# ADK imports
from google.adk.cli.fast_api import get_fast_api_app
from google.adk.cli.utils import logs

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



def ensure_env_file_exists():
    """Ensure .env file exists in directory with default values."""
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    
    if not os.path.exists(env_path):
        # Create .env file with default values
        env_content = "GOOGLE_API_KEY='<PLEASE_SET_IN_SETTINGS>'\nROOT_AGENT_MODEL='gemini-2.5-flash'\n"
        
        try:
            with open(env_path, "w", encoding="utf-8") as f:
                f.write(env_content)
            print(f"Created .env file at {env_path}")
        except Exception as e:
            print(f"Error creating .env file: {e}")


# Ensure .env file exists before any imports of robinhood_agent
ensure_env_file_exists()

try:
    # Primary WebView implementation for mobile deployment
    from kivy_garden.webview import WebView
except ImportError:
    WebView = None
    logger.warning("kivy_garden.webview not available - WebView functionality disabled")

try:
    # Alternative WebView implementation
    import webview as pywebview
except ImportError:
    pywebview = None
    logger.info("pywebview not available - using primary WebView only")


SERVICE_NAME = "autoyou_mobile_app"
KEY_USERNAME = "robinhood_username"
KEY_PASSWORD = "robinhood_password"
KEY_OTP = "robinhood_otp"
KEY_API_KEY = "google_api_key"


def get_credentials_store():
    """Get the JsonStore instance for storing credentials."""
    from kivy.app import App
    app = App.get_running_app()
    if app is None:
        # Fallback for when app is not running yet
        data_dir = os.path.expanduser("~/.autoyou")
        os.makedirs(data_dir, exist_ok=True)
    else:
        data_dir = app.user_data_dir
    return JsonStore(os.path.join(data_dir, 'credentials.json'))


def get_credential(key: str) -> str:
    """Get a credential from JsonStore."""
    store = get_credentials_store()
    try:
        return store.get('credentials')[key]
    except KeyError:
        return ""


def set_credential(key: str, value: str):
    """Set a credential in JsonStore."""
    store = get_credentials_store()
    try:
        credentials = store.get('credentials')
    except KeyError:
        credentials = {}
    credentials[key] = value
    store.put('credentials', **credentials)


def delete_credential(key: str):
    """Delete a credential from JsonStore."""
    store = get_credentials_store()
    try:
        credentials = store.get('credentials')
        if key in credentials:
            del credentials[key]
            store.put('credentials', **credentials)
    except KeyError:
        pass

def create_autoyou_web_server(
    host: str = "127.0.0.1",
    port: int = 8000,
    reload: bool = True,
    log_level: str = "INFO",
    allow_origins: Optional[list[str]] = None,
) -> FastAPI:
    """
    Create a customized ADK web server for the AutoYou agent.
    
    Args:
        host: Host to bind the server to
        port: Port to bind the server to
        reload: Whether to enable auto-reload
        log_level: Logging level
        allow_origins: List of allowed CORS origins
        
    Returns:
        FastAPI application instance
    """
    # Setup logging
    logs.setup_adk_logger(getattr(logging, log_level.upper()))
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        """Lifespan context manager for the FastAPI app."""
        print(f"""
+-----------------------------------------------------------------------------+
| AutoYou ADK Web Server started                                              |
|                                                                             |
| Agent: AutoYou Trading Agent                                                |
| Location: robinhood_agent/agent.py                                            |
| Access at: http://{host}:{port}/dev-ui/?app=robinhood_agent{" " * (25 - len(host) - len(str(port)))}|
+-----------------------------------------------------------------------------+
""")
        yield  # Startup is done, now app is running
        print("""
+-----------------------------------------------------------------------------+
| AutoYou ADK Web Server shutting down...                                     |
+-----------------------------------------------------------------------------+
""")
    
    # Get the agents directory (current directory containing robinhood_agent)
    current_dir = Path(__file__).parent.resolve()
    agents_dir = str(current_dir)
    
    logger.info(f"AutoYou agents directory: {agents_dir}")
    
    # Create the FastAPI app using ADK's get_fast_api_app
    app = get_fast_api_app(
        agents_dir=agents_dir,
        session_service_uri=None,  # Use in-memory session service
        artifact_service_uri=None,  # Use in-memory artifact service
        memory_service_uri=None,   # Use in-memory memory service
        eval_storage_uri=None,     # Use local eval storage
        allow_origins=allow_origins or ["*"],  # Allow all origins for development
        web=True,                  # Enable web UI
        trace_to_cloud=False,      # Disable cloud tracing for local development
        lifespan=lifespan,
        a2a=False,                 # Disable A2A protocol
        host=host,
        port=port,
        reload_agents=False,       # Disable agent hot-reloading to avoid YAML config issues
    )
    
    return app

def start_adk_web_server(
    host: str = "127.0.0.1",
    port: int = 8000,
    reload: bool = False,
    log_level: str = "INFO"
) -> threading.Thread:
    """Launch the ADK web server in a background thread.

    This starts the customized ADK web server that directly points to
    the AutoYou agent, providing the full ADK interface and chat functionality.
    The server runs in a separate thread to avoid blocking the Kivy UI.

    Args:
        host: Host to bind the server to (default: 127.0.0.1)
        port: Port to bind the server to (default: 8000)
        reload: Whether to enable auto-reload (default: False for production)
        log_level: Logging level (default: INFO)

    Returns:
        A ``threading.Thread`` object representing the running
        server thread.
    """
    def run_server():
        try:
            app = create_autoyou_web_server(
                host=host,
                port=port,
                reload=reload,
                log_level=log_level,
            )
        
            # Configure uvicorn
            config = uvicorn.Config(
                app,
                host=host,
                port=port,
                reload=reload,
                log_level=log_level.lower(),
            )
            
            # Run the server
            server = uvicorn.Server(config)
            server.run()
        except Exception as e:
            print(f"Error starting ADK web server: {e}")
    
    # Start server in background thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    return server_thread


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
        terms_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "terms.txt")
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
        existing_user = get_credential(KEY_USERNAME)
        if existing_user:
            app.manager.current = "home"
        else:
            app.manager.current = "settings"


class SettingsScreen(Screen):
    """Screen allowing the user to enter and save credentials.

    Contains text inputs for the Robinhood username, password, OTP and
    Google API key. Values are saved using JsonStore for cross-platform
    compatibility. A "Save" button persists the data and then returns
    to the home screen.
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
                text=get_credential(key) or "",
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
        google_api_key = None
        
        for key, input_field in self.inputs.items():
            value = input_field.text.strip()
            if value:
                set_credential(key, value)
                # Store Google API key for .env file update
                if key == KEY_API_KEY:
                    google_api_key = value
            else:
                # If the user clears a field, remove it from the credentials
                delete_credential(key)
        
        # Update .env file in robinhood_agent directory if Google API key is provided
        if google_api_key:
            self._update_env_file(google_api_key)
        
        app: KivyAdkApp = App.get_running_app()  # type: ignore[assignment]
        app.manager.current = "home"
    
    def _update_env_file(self, google_api_key: str):
        """Update or create .env file in robinhood_agent directory with Google API key."""
        env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
        
        # Content for the .env file
        env_content = f"GOOGLE_API_KEY='{google_api_key}'\nROOT_AGENT_MODEL='gemini-2.5-flash'\n"
        os.environ["GOOGLE_API_KEY"] = google_api_key
        try:
            with open(env_path, "w", encoding="utf-8") as f:
                f.write(env_content)
        except Exception as e:
            print(f"Error writing .env file: {e}")


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
            text="Robinhood Chat Trading Agent",
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
            text="Robinhood Chat Trading Agent",
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
            text="Click the button below to open the chat interface in your browser.",
            font_size=sp(36),
            halign="center",
            valign="middle",
            color=(0.7, 0.7, 0.7, 1)
        )
        desc_label.bind(size=lambda instance, value: setattr(instance, "text_size", value))
        content_layout.add_widget(desc_label)
        
        # WebView launch button
        webview_btn = Button(
            text="🌐 Open Chat Interface",
            size_hint=(1, None),
            height=dp(120),
            font_size=sp(44),
            background_color=(0.2, 0.6, 1, 1),
            bold=True
        )
        webview_btn.bind(on_release=self.open_in_browser)
        content_layout.add_widget(webview_btn)
        
        # Alternative URL display
        url_label = Label(
            text="Direct URL: http://localhost:8000",
            font_size=sp(32),
            halign="center",
            valign="middle",
            color=(0.6, 0.6, 0.6, 1)
        )
        url_label.bind(size=lambda instance, value: setattr(instance, "text_size", value))
        content_layout.add_widget(url_label)
        
        layout.add_widget(content_layout)
        self.add_widget(layout)
    
    def open_in_browser(self, instance):
        """Open the chat interface using platform-specific WebView."""
        import platform
        import webbrowser
        
        # Use 127.0.0.1 for better mobile compatibility
        url = "http://127.0.0.1:8000/dev-ui/?app=robinhood_agent"
        
        system = platform.system().lower()
        logger.info(f"Opening WebView on platform: {system}")
        
        try:
            # Check for Kivy platform detection first
            from kivy.utils import platform as kivy_platform
            
            if kivy_platform == 'android':
                # Android-specific WebView handling
                try:
                    from android.runnable import run_on_ui_thread
                    from jnius import autoclass, cast
                    
                    # Use Android WebView through Pyjnius
                    WebView = autoclass('android.webkit.WebView')
                    activity = autoclass('org.kivy.android.PythonActivity').mActivity
                    
                    @run_on_ui_thread
                    def open_webview():
                        webview = WebView(activity)
                        webview.loadUrl(url)
                    
                    open_webview()
                    logger.info("Opened Android WebView successfully")
                    return
                except ImportError:
                    logger.warning("Android WebView not available, using fallback")
            
            elif kivy_platform == 'ios':
                # iOS-specific WebView handling
                try:
                    from pyobjus import autoclass
                    
                    # Use iOS WebView through PyObjus
                    NSURL = autoclass('NSURL')
                    NSURLRequest = autoclass('NSURLRequest')
                    WKWebView = autoclass('WKWebView')
                    
                    webview = WKWebView.alloc().init()
                    nsurl = NSURL.URLWithString_(url)
                    request = NSURLRequest.requestWithURL_(nsurl)
                    webview.loadRequest_(request)
                    
                    logger.info("Opened iOS WebView successfully")
                    return
                except ImportError:
                    logger.warning("iOS WebView not available, using fallback")
            
            # Fallback to system default browser
            webbrowser.open(url)
            logger.info("Opened in system default browser")
            
        except Exception as e:
            logger.error(f"Error opening WebView: {e}")
            # Final fallback to system browser
            try:
                webbrowser.open(url)
                logger.info("Fallback to system browser successful")
            except Exception as fallback_error:
                logger.error(f"All WebView methods failed: {fallback_error}")
                # Show error message to user
                from kivy.uix.popup import Popup
                popup = Popup(
                    title='Error',
                    content=Label(text=f'Cannot open WebView.\nPlease visit {url} manually.'),
                    size_hint=(0.8, 0.4)
                )
                popup.open()
    

    



class KivyAdkApp(App):
    """Main application class."""

    manager: ScreenManager
    _web_server_thread: Optional[threading.Thread] = None

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
        """Start the uvicorn web server and initialize TinyDB when the app launches."""        
        
        # Launch the ADK web server in a background thread
        try:
            self._web_server_thread = start_adk_web_server()
            print("ADK web server started in background thread")
        except Exception as e:
            print(f"Failed to start ADK web server: {e}")

    def on_stop(self) -> None:
        """Clean up when the app exits."""
        if self._web_server_thread and self._web_server_thread.is_alive():
            try:
                print("Web server will terminate when app exits (daemon thread)")
            except Exception as e:
                print(f"Error during web server cleanup: {e}")


def main():
    """Main entry point for the AutoYou Kivy application."""
    try:
        # Initialize and run the Kivy application
        app = KivyAdkApp()
        app.run()
    except Exception as e:
        logger.error(f"Failed to start AutoYou application: {e}")
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()