"""robinhood_login_agent for logging successfully to robinhood account and ensuring account details are accessible"""

import os
from dotenv import load_dotenv

from google.adk import Agent
from google.adk.tools import ToolContext

import robin_stocks.robinhood as r

from . import prompt


# Load environment variables
load_dotenv()

def peform_robinhood_login(tool_context: ToolContext) -> str:
    """
    Perform login to robinhood account
    """
    username = os.getenv("ROBINHOOD_USERNAME")
    password = os.getenv("ROBINHOOD_PASSWORD")

    login = r.login(username, password)
    tool_context.state["robinhood_login"] = login
    if not login:
        return "Login failed"
    login_detail = login.get('detail', '')
    if 'logged in' in login_detail:
        return "Login successful"


robinhood_login_agent = Agent(
    model=os.getenv("ROOT_AGENT_MODEL"),
    name="robinhood_login_agent",
    instruction=prompt.AGENT_INSTRUCTION,
    output_key="login_status",
    tools=[peform_robinhood_login],
)
