"""robinhood_login_agent for logging successfully to robinhood account and ensuring account details are accessible"""

import os
from kivy.storage.jsonstore import JsonStore
from dotenv import load_dotenv

from google.adk import Agent
from google.adk.tools import ToolContext

import robin_stocks.robinhood as r

# Load environment variables
load_dotenv()

from . import prompt


# JsonStore service and key constants (matching main.py)
SERVICE_NAME = "autoyou_mobile_app"
KEY_USERNAME = "robinhood_username"
KEY_PASSWORD = "robinhood_password"


def get_credentials_store():
    """Get the JsonStore instance for storing credentials."""
    try:
        from kivy.app import App
        app = App.get_running_app()
        if app is None:
            # Fallback for when app is not running yet
            data_dir = os.path.expanduser("~/.autoyou")
            os.makedirs(data_dir, exist_ok=True)
        else:
            data_dir = app.user_data_dir
    except:
        # Fallback for when Kivy app is not available
        data_dir = os.path.expanduser("~/.autoyou")
        os.makedirs(data_dir, exist_ok=True)
    return JsonStore(os.path.join(data_dir, 'credentials.json'))


def get_credential(key: str) -> str:
    """Get a credential from JsonStore."""
    store = get_credentials_store()
    try:
        return store.get('credentials')[key]
    except KeyError:
        return ""


def peform_robinhood_login(tool_context: ToolContext) -> str:
    """
    Perform login to robinhood account
    """
    username = get_credential(KEY_USERNAME)
    password = get_credential(KEY_PASSWORD)

    login = r.login(username, password)
    tool_context.state["robinhood_login"] = login
    if not login:
        return "Login failed"
    login_detail = login.get('detail', '')
    if 'logged in' in login_detail:
        return "Login successful"


robinhood_login_agent = Agent(
    model="gemini-2.5-flash",
    name="robinhood_login_agent",
    instruction=prompt.AGENT_INSTRUCTION,
    output_key="login_status",
    tools=[peform_robinhood_login],
)
