import os
import datetime
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext

# Load environment variables
load_dotenv()

from . import prompt
from .sub_agents.robinhood_login import robinhood_login_agent
from .sub_agents.robinhood_portfolio import robinhood_portfolio_agent
from .sub_agents.robinhood_stocks import robinhood_stocks_agent
from .sub_agents.robinhood_options import robinhood_options_agent
from .sub_agents.robinhood_markets import robinhood_markets_agent
from .sub_agents.robinhood_orders import robinhood_orders_agent
from .tinydb_session_service import TinyDBSessionService

def setup_before_agent_call(callback_context: CallbackContext):
    """Setup the agent."""

    # setting up database settings in session.state
    if "robinhood_settings" not in callback_context.state:
        callback_context.state["robinhood_settings"] = dict()
    
    # Initialize session service flag for tracking (avoid storing the object directly)
    if "session_service_initialized" not in callback_context.state:
        callback_context.state["session_service_initialized"] = True


root_agent = Agent(
    name="autoyou_agent",
    model=os.getenv("ROOT_AGENT_MODEL"),
    description=(
        "Agent to interactively chat with your Trading accounts to get insights and place simple trades"
    ),
    instruction=prompt.AUTOYOU_AGENT_INSTRUCTIONS,
    sub_agents=[
        robinhood_login_agent, 
        robinhood_portfolio_agent, 
        robinhood_stocks_agent, 
        robinhood_options_agent,
        robinhood_orders_agent,
        robinhood_markets_agent
    ],
    before_agent_callback=setup_before_agent_call,
)