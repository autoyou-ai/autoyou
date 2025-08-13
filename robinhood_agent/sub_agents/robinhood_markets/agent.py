"""Robinhood Markets Agent
================

This module defines a multi‑tool agent using Google's Agent Development Kit (ADK)
that exposes a suite of read‑only helpers around the `robin_stocks.robinhood.markets` library. The
functions in this module wrap common Robinhood API calls for market information, such as
retrieving market hours, getting top movers, finding stocks by market tag, and more.

**Important:** This agent is intentionally limited to read‑only operations. It
will **not** place or cancel any orders on your behalf. Executing trades or
other high‑stakes financial activities is outside the scope of this example
and disallowed by policy.

To use this agent you must supply valid Robinhood credentials via environment
variables (`ROBIN_USERNAME`, `ROBIN_PASSWORD`, and optionally `ROBIN_MFA` for
two‑factor authentication). When a tool is called for the first time it will
log into Robinhood using these credentials and cache the session for the
remainder of the process.

The following capabilities are implemented:

1. **get_all_stocks_from_market_tag** – Returns all stocks that match a tag category.
2. **get_currency_pairs** – Returns currency pairs available for trading.
3. **get_market_hours** – Returns market hours for a specific date.
4. **get_market_next_open_hours** – Returns the next open trading day after today.
5. **get_market_next_open_hours_after_date** – Returns the next open trading day after a specified date.
6. **get_market_today_hours** – Returns today's market hours.
7. **get_markets** – Returns a list of available markets.
8. **get_top_100** – Returns the top 100 stocks on Robinhood.
9. **get_top_movers** – Returns the top 20 movers on Robinhood.
10. **get_top_movers_sp500** – Returns the top S&P500 movers up or down for the day.
"""

from __future__ import annotations

import os
from typing import Any, Dict, List, Optional, Union

try:
    # Import robin_stocks lazily so that this file can be analysed without the
    # package being installed. At runtime you must have `robin-stocks`
    # available.
    import robin_stocks.robinhood.markets as rh_markets
except ImportError:
    rh_markets = None  # type: ignore

try:
    # Import ADK components. These imports will succeed only if
    # google-adk has been installed in your environment.
    from google.adk.agents import Agent
except Exception:
    Agent = None  # type: ignore

from .prompt import AGENT_INSTRUCTION

from dotenv import load_dotenv
load_dotenv()

__all__ = [
    # Root coordinator agent
    "robinhood_markets_agent",
    # Market data sub-agents
    "get_all_stocks_from_market_tag_agent",
    "get_top_100_agent",
    "get_top_movers_agent",
    "get_top_movers_sp500_agent",
    "get_currency_pairs_agent",
    # Market information sub-agents
    "get_markets_agent",
    "get_market_hours_agent",
    "get_market_today_hours_agent",
    "get_market_next_open_hours_agent",
    "get_market_next_open_hours_after_date_agent",
    # Underlying tool functions
    "get_all_stocks_from_market_tag",
    "get_currency_pairs",
    "get_market_hours",
    "get_market_next_open_hours",
    "get_market_next_open_hours_after_date",
    "get_market_today_hours",
    "get_markets",
    "get_top_100",
    "get_top_movers",
    "get_top_movers_sp500",
]

# Define all market-related functions as wrappers
def get_all_stocks_from_market_tag(tag: str, info: str = "") -> List[Dict[str, Any]]:
    """Returns all the stock quote information that matches a tag category.
    
    Args:
        tag: The category to filter for. Examples include 'biopharmaceutical', 
            'upcoming-earnings', 'most-popular-under-25', and 'technology'.
        info: Optional. When provided, this acts as a key to extract a
            specific value from each stock record. If omitted, the full
            dictionary is returned for each stock.
    
    Returns:
        list: A list of dictionaries with stock quote information for the tag category.
        Each dictionary contains fields such as symbol, name, price, and other
        trading information. If info parameter is provided, a list of specific values
        is returned instead.
    """
    info_param: Optional[str] = info or None  # type: ignore[assignment]
    results: List[Dict[str, Any]] = rh_markets.get_all_stocks_from_market_tag(tag, info=info_param)  # type: ignore[attr-defined]
    # If a specific field was requested, ensure each element is wrapped in a
    # dictionary keyed by ``info`` for consistency across tool outputs.
    if info_param is not None and not isinstance(results[0], dict) if results else False:
        return [{info_param: r} for r in results]
    return results

def get_currency_pairs(info: str = "") -> List[Dict[str, Any]]:
    """Returns currency pairs available for trading on Robinhood.
    
    Args:
        info: Optional. When provided, this acts as a key to extract a
            specific value from each currency pair record. If omitted, the full
            dictionary is returned for each pair.
    
    Returns:
        list: A list of dictionaries with currency pair information.
        Each dictionary contains fields such as asset_currency, quote_currency,
        display_only, tradability, and other trading information. If info parameter
        is provided, a list of specific values is returned instead.
    """
    info_param: Optional[str] = info or None  # type: ignore[assignment]
    results: List[Dict[str, Any]] = rh_markets.get_currency_pairs(info=info_param)  # type: ignore[attr-defined]
    # If a specific field was requested, ensure each element is wrapped in a
    # dictionary keyed by ``info`` for consistency across tool outputs.
    if info_param is not None and not isinstance(results[0], dict) if results else False:
        return [{info_param: r} for r in results]
    return results

def get_market_hours(market: str, date: str, info: str = "") -> Dict[str, Any]:
    """Returns the opening and closing hours of a specific market on a specific date.
    
    Args:
        market: The 'mic' value for the market. Can be found using get_markets().
        date: The date you want to get information for. Format is YYYY-MM-DD.
        info: Optional. When provided, this acts as a key to extract a
            specific value from the market hours record. If omitted, the full
            dictionary is returned.
    
    Returns:
        dict: A dictionary with market hours information for the specified date.
        Contains fields such as is_open, opens_at, closes_at, extended_opens_at,
        extended_closes_at, and other schedule information. If info parameter
        is provided, only the specific value is returned.
    """
    info_param: Optional[str] = info or None  # type: ignore[assignment]
    result: Dict[str, Any] = rh_markets.get_market_hours(market, date, info=info_param)  # type: ignore[attr-defined]
    # If a specific field was requested, ensure it's wrapped in a
    # dictionary keyed by ``info`` for consistency across tool outputs.
    if info_param is not None and not isinstance(result, dict):
        return {info_param: result}
    return result

def get_market_next_open_hours(market: str, info: str = "") -> Dict[str, Any]:
    """Returns the opening and closing hours for the next open trading day after today.
    
    Args:
        market: The 'mic' value for the market. Can be found using get_markets().
        info: Optional. When provided, this acts as a key to extract a
            specific value from the market hours record. If omitted, the full
            dictionary is returned.
    
    Returns:
        dict: A dictionary with next open market hours information.
        Contains fields such as is_open, opens_at, closes_at, extended_opens_at,
        extended_closes_at, date, and other schedule information. If info parameter
        is provided, only the specific value is returned.
    """
    info_param: Optional[str] = info or None  # type: ignore[assignment]
    result: Dict[str, Any] = rh_markets.get_market_next_open_hours(market, info=info_param)  # type: ignore[attr-defined]
    # If a specific field was requested, ensure it's wrapped in a
    # dictionary keyed by ``info`` for consistency across tool outputs.
    if info_param is not None and not isinstance(result, dict):
        return {info_param: result}
    return result

def get_market_next_open_hours_after_date(market: str, date: str, info: str = "") -> Dict[str, Any]:
    """Returns the opening and closing hours for the next open trading day after a specified date.
    
    Args:
        market: The 'mic' value for the market. Can be found using get_markets().
        date: The date you want to find the next available trading day after. Format is YYYY-MM-DD.
        info: Optional. When provided, this acts as a key to extract a
            specific value from the market hours record. If omitted, the full
            dictionary is returned.
    
    Returns:
        dict: A dictionary with next open market hours after the specified date.
        Contains fields such as is_open, opens_at, closes_at, extended_opens_at,
        extended_closes_at, date, and other schedule information. If info parameter
        is provided, only the specific value is returned.
    """
    info_param: Optional[str] = info or None  # type: ignore[assignment]
    result: Dict[str, Any] = rh_markets.get_market_next_open_hours_after_date(market, date, info=info_param)  # type: ignore[attr-defined]
    # If a specific field was requested, ensure it's wrapped in a
    # dictionary keyed by ``info`` for consistency across tool outputs.
    if info_param is not None and not isinstance(result, dict):
        return {info_param: result}
    return result

def get_market_today_hours(market: str, info: str = "") -> Dict[str, Any]:
    """Returns the opening and closing hours for the market today.
    
    Args:
        market: The 'mic' value for the market. Can be found using get_markets().
        info: Optional. When provided, this acts as a key to extract a
            specific value from the market hours record. If omitted, the full
            dictionary is returned.
    
    Returns:
        dict: A dictionary with today's market hours information.
        Contains fields such as is_open, opens_at, closes_at, extended_opens_at,
        extended_closes_at, date, and other schedule information. If info parameter
        is provided, only the specific value is returned.
    """
    info_param: Optional[str] = info or None  # type: ignore[assignment]
    result: Dict[str, Any] = rh_markets.get_market_today_hours(market, info=info_param)  # type: ignore[attr-defined]
    # If a specific field was requested, ensure it's wrapped in a
    # dictionary keyed by ``info`` for consistency across tool outputs.
    if info_param is not None and not isinstance(result, dict):
        return {info_param: result}
    return result

def get_markets(info: str = "") -> Union[List[Dict[str, Any]], Dict[str, Any]]:
    """Returns a list of available markets.
    
    Args:
        info: Optional. When provided, this acts as a key to extract a
            specific value from each market record. If omitted, the full
            list of dictionaries is returned.
    
    Returns:
        list: A list of dictionaries with market information if info is not provided.
        Each dictionary contains fields such as mic, operating_mic, acronym, name,
        city, country, timezone, and website. If info parameter is provided, a
        dictionary mapping market identifiers to the requested info field is returned.
    """
    info_param: Optional[str] = info or None  # type: ignore[assignment]
    result = rh_markets.get_markets(info=info_param)  # type: ignore[attr-defined]
    # If a specific field was requested but the result is not a dict,
    # wrap it in a dictionary keyed by ``info`` for consistency
    if info_param is not None and not isinstance(result, dict):
        return {info_param: result}
    return result

def get_top_100(info: str = "") -> Union[List[Dict[str, Any]], Dict[str, Any]]:
    """Returns the top 100 stocks on Robinhood.
    
    Args:
        info: Optional. When provided, this acts as a key to extract a
            specific value from each stock record. If omitted, the full
            list of dictionaries is returned.
    
    Returns:
        list: A list of dictionaries with information about the top 100 stocks if info is not provided.
        Each dictionary contains fields such as symbol, name, price, and other stock information.
        If info parameter is provided, a dictionary mapping stock identifiers to the requested
        info field is returned.
    """
    info_param: Optional[str] = info or None  # type: ignore[assignment]
    result = rh_markets.get_top_100(info=info_param)  # type: ignore[attr-defined]
    # If a specific field was requested but the result is not a dict,
    # wrap it in a dictionary keyed by ``info`` for consistency
    if info_param is not None and not isinstance(result, dict):
        return {info_param: result}
    return result


def get_top_movers(direction: str, info: str = "") -> Union[List[Dict[str, Any]], Dict[str, Any]]:
    """Returns the top movers up or down for the day.
    
    Args:
        direction: The direction to filter for, either 'up' or 'down'.
        info: Optional. When provided, this acts as a key to extract a
            specific value from each stock record. If omitted, the full
            list of dictionaries is returned.
    
    Returns:
        list: A list of dictionaries with information about the top moving stocks if info is not provided.
        Each dictionary contains fields such as symbol, name, price_movement, and other stock information.
        If info parameter is provided, a dictionary mapping stock identifiers to the requested
        info field is returned.
    """
    info_param: Optional[str] = info or None  # type: ignore[assignment]
    result = rh_markets.get_top_movers(direction, info=info_param)  # type: ignore[attr-defined]
    # If a specific field was requested but the result is not a dict,
    # wrap it in a dictionary keyed by ``info`` for consistency
    if info_param is not None and not isinstance(result, dict):
        return {info_param: result}
    return result


def get_top_movers_sp500(direction: str, info: str = "") -> Union[List[Dict[str, Any]], Dict[str, Any]]:
    """Returns the top movers up or down in the S&P 500 for the day.
    
    Args:
        direction: The direction to filter for, either 'up' or 'down'.
        info: Optional. When provided, this acts as a key to extract a
            specific value from each stock record. If omitted, the full
            list of dictionaries is returned.
    
    Returns:
        list: A list of dictionaries with information about the top moving S&P 500 stocks if info is not provided.
        Each dictionary contains fields such as symbol, name, price_movement, and other stock information.
        If info parameter is provided, a dictionary mapping stock identifiers to the requested
        info field is returned.
    """
    info_param: Optional[str] = info or None  # type: ignore[assignment]
    result = rh_markets.get_top_movers_sp500(direction, info=info_param)  # type: ignore[attr-defined]
    # If a specific field was requested but the result is not a dict,
    # wrap it in a dictionary keyed by ``info`` for consistency
    if info_param is not None and not isinstance(result, dict):
        return {info_param: result}
    return result

# Create individual sub-agents for each market function
get_all_stocks_from_market_tag_agent = Agent(
    name="get_all_stocks_from_market_tag_agent",
    description="Retrieves stocks by market tag categories",
    tools=[get_all_stocks_from_market_tag],
    instruction="""
    You are a specialized agent for retrieving stocks by market tag categories.
    
    Use the get_all_stocks_from_market_tag function to find stocks that match specific categories like:
    - 'biopharmaceutical' - biotech and pharmaceutical companies
    - 'upcoming-earnings' - companies with upcoming earnings announcements
    - 'most-popular-under-25' - popular stocks under $25
    - 'technology' - technology sector stocks
    
    The function returns comprehensive quote information including prices, volumes, and trading status.
    You can optionally filter results by providing an 'info' parameter to get specific data fields.
    """
)

get_currency_pairs_agent = Agent(
    name="get_currency_pairs_agent",
    description="Retrieves cryptocurrency currency pairs available for trading",
    tools=[get_currency_pairs],
    instruction="""
    You are a specialized agent for retrieving cryptocurrency currency pairs.
    
    Use the get_currency_pairs function to get information about available currency pairs for trading.
    This includes details like asset currency, quote currency, trading limits, and tradability status.
    You can filter results by providing an 'info' parameter to get specific data fields.
    """
)

get_market_hours_agent = Agent(
    name="get_market_hours_agent",
    description="Retrieves market hours for specific dates",
    tools=[get_market_hours],
    instruction="""
    You are a specialized agent for retrieving market hours for specific dates.
    
    Use the get_market_hours function to get opening/closing times for any market on any date (past or future).
    Requires:
    - market: The 'mic' value (use get_markets() to find available markets)
    - date: Format YYYY-MM-DD
    
    Returns information about regular and extended trading hours, and whether the market is open.
    """
)

get_market_next_open_hours_agent = Agent(
    name="get_market_next_open_hours_agent",
    description="Finds the next open trading day after today",
    tools=[get_market_next_open_hours],
    instruction="""
    You are a specialized agent for finding the next open trading day.
    
    Use the get_market_next_open_hours function to get the opening/closing hours for the next trading day after today.
    Requires the market 'mic' value (use get_markets() to find available markets).
    
    Useful for planning trades and understanding when markets will next be available.
    """
)

get_market_next_open_hours_after_date_agent = Agent(
    name="get_market_next_open_hours_after_date_agent",
    description="Finds the next open trading day after a specific date",
    tools=[get_market_next_open_hours_after_date],
    instruction="""
    You are a specialized agent for finding the next open trading day after a specific date.
    
    Use the get_market_next_open_hours_after_date function to get the next trading day after any specified date.
    Requires:
    - market: The 'mic' value (use get_markets() to find available markets)
    - date: Format YYYY-MM-DD (the date after which to find the next trading day)
    
    Useful for planning future trades and understanding market schedules.
    """
)

get_market_today_hours_agent = Agent(
    name="get_market_today_hours_agent",
    description="Retrieves today's market hours",
    tools=[get_market_today_hours],
    instruction="""
    You are a specialized agent for retrieving today's market hours.
    
    Use the get_market_today_hours function to get opening/closing times for any market today.
    Requires the market 'mic' value (use get_markets() to find available markets).
    
    Returns information about regular and extended trading hours for today, and whether the market is currently open.
    """
)

get_markets_agent = Agent(
    name="get_markets_agent",
    description="Retrieves available markets information",
    tools=[get_markets],
    instruction="""
    You are a specialized agent for retrieving available markets information.
    
    Use the get_markets function to get a list of all available markets and their details.
    This includes market identifiers (mic), names, locations, timezones, and websites.
    
    This is often the first step when you need market 'mic' values for other market-related functions.
    """
)

get_top_100_agent = Agent(
    name="get_top_100_agent",
    description="Retrieves the Top 100 stocks on Robinhood",
    tools=[get_top_100],
    instruction="""
    You are a specialized agent for retrieving the Top 100 stocks on Robinhood.
    
    Use the get_top_100 function to get comprehensive quote information for the most popular stocks.
    Returns detailed market data including prices, volumes, and trading status for the top 100 stocks.
    You can filter results by providing an 'info' parameter to get specific data fields.
    """
)

get_top_movers_agent = Agent(
    name="get_top_movers_agent",
    description="Retrieves the top moving stocks on Robinhood",
    tools=[get_top_movers],
    instruction="""
    You are a specialized agent for retrieving the top moving stocks on Robinhood.
    
    Use the get_top_movers function to get information about stocks with the largest price movements.
    Requires a direction parameter ('up' or 'down') to filter for stocks moving in that direction.
    Returns detailed market data about the top 20 movers including price changes and percentage movements.
    """
)

get_top_movers_sp500_agent = Agent(
    name="get_top_movers_sp500_agent",
    description="Retrieves the top moving S&P 500 stocks",
    tools=[get_top_movers_sp500],
    instruction="""
    You are a specialized agent for retrieving the top moving S&P 500 stocks.
    
    Use the get_top_movers_sp500 function to get information about S&P 500 stocks with the largest price movements.
    Requires a direction parameter ('up' or 'down') to filter for stocks moving in that direction.
    Returns detailed market data about the top S&P 500 movers including price changes and percentage movements.
    """
)

# Main coordinator agent for robinhood markets
robinhood_markets_agent = Agent(
    model="gemini-2.5-flash",
    name="robinhood_markets_agent",
    description="Provides access to Robinhood market data and information",
    instruction=AGENT_INSTRUCTION,
    sub_agents=[
        # Market data and listings
        get_all_stocks_from_market_tag_agent,
        get_top_100_agent,
        get_top_movers_agent,
        get_top_movers_sp500_agent,
        get_currency_pairs_agent,
        # Market information and schedules
        get_markets_agent,
        get_market_hours_agent,
        get_market_today_hours_agent,
        get_market_next_open_hours_agent,
        get_market_next_open_hours_after_date_agent,
    ]
)

__all__ = [
    # Main coordinator agent
    "robinhood_markets_agent",
    
    # Market data sub-agents
    "get_all_stocks_from_market_tag_agent",
    "get_top_100_agent",
    "get_currency_pairs_agent",
    "get_top_movers_agent",
    "get_top_movers_sp500_agent",
    
    # Market information sub-agents
    "get_markets_agent",
    "get_market_hours_agent",
    "get_market_next_open_hours_agent",
    "get_market_next_open_hours_after_date_agent",
    "get_market_today_hours_agent",
    
    # Underlying tool functions
    "get_all_stocks_from_market_tag",
    "get_currency_pairs",
    "get_market_hours",
    "get_market_next_open_hours",
    "get_market_next_open_hours_after_date",
    "get_market_today_hours",
    "get_markets",
    "get_top_100",
    "get_top_movers",
    "get_top_movers_sp500",
]