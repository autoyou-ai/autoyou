"""robinhood_options_agent for fetching options information from Robinhood"""

import os
from typing import Any, Dict, List, Optional, Union
from dotenv import load_dotenv

from google.adk import Agent

import robin_stocks.robinhood as r

from . import prompt

# Load environment variables
load_dotenv()

__all__ = [
    # Root coordinator agent
    "robinhood_options_agent",
    # Options search sub-agents
    "find_options_by_expiration_agent",
    "find_options_by_expiration_and_strike_agent",
    "find_options_by_specific_profitability_agent",
    "find_options_by_strike_agent",
    "find_tradable_options_agent",
    "get_market_options_agent",
    "get_chains_agent",
    # Position management sub-agents
    "get_aggregate_open_positions_agent",
    "get_aggregate_positions_agent",
    "get_all_option_positions_agent",
    "get_open_option_positions_agent",
    # Data analysis sub-agents
    "get_option_historicals_agent",
    "get_option_market_data_agent",
    "get_option_instrument_data_agent",
    # Underlying tool functions
    "find_options_by_expiration",
    "find_options_by_expiration_and_strike",
    "find_options_by_specific_profitability",
    "find_options_by_strike",
    "find_tradable_options",
    "get_market_options",
    "get_all_option_positions",
    "get_open_option_positions",
    "get_chains",
    "get_option_historicals",
    "get_option_market_data_by_id",
    "get_option_market_data",
    "get_option_instrument_data_by_id",
    "get_option_instrument_data",
    "get_aggregate_open_positions",
    "get_aggregate_positions",
]


def find_options_by_expiration(inputSymbols: str, expirationDate: str, 
                              optionType: Optional[str] = None, 
                              info: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Returns a list of all the option orders that match the search parameters

    Args:
        inputSymbols: The ticker of either a single stock or a list of stocks.
        expirationDate: Represents the expiration date in the format YYYY-MM-DD.
        optionType: Can be either 'call' or 'put' or leave blank to get both.
        info: Will filter the results to get a specific value.

    Returns:
        Returns a list of dictionaries of key/value pairs for all options of the stock that match the search parameters.
        If info parameter is provided, a list of strings is returned where the strings are the value of the key that matches info.
    """
    return r.options.find_options_by_expiration(inputSymbols, expirationDate, optionType, info)


def find_options_by_expiration_and_strike(inputSymbols: str, expirationDate: str, 
                                         strikePrice: str, optionType: Optional[str] = None, 
                                         info: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Returns a list of all the option orders that match the search parameters

    Args:
        inputSymbols: The ticker of either a single stock or a list of stocks.
        expirationDate: Represents the expiration date in the format YYYY-MM-DD.
        strikePrice: Represents the strike price to filter for.
        optionType: Can be either 'call' or 'put' or leave blank to get both.
        info: Will filter the results to get a specific value.

    Returns:
        Returns a list of dictionaries of key/value pairs for all options of the stock that match the search parameters.
        If info parameter is provided, a list of strings is returned where the strings are the value of the key that matches info.
    """
    return r.options.find_options_by_expiration_and_strike(inputSymbols, expirationDate, strikePrice, optionType, info)


def find_options_by_specific_profitability(inputSymbols: Union[str, List[str]], 
                                          expirationDate: Optional[str] = None, 
                                          strikePrice: Optional[str] = None, 
                                          optionType: Optional[str] = None, 
                                          typeProfit: str = 'chance_of_profit_short', 
                                          profitFloor: float = 0.0, 
                                          profitCeiling: float = 1.0, 
                                          info: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Returns a list of option market data for several stock tickers that match a range of profitability.

    Args:
        inputSymbols: May be a single stock ticker or a list of stock tickers.
        expirationDate: Represents the expiration date in the format YYYY-MM-DD. Leave as None to get all available dates.
        strikePrice: Represents the price of the option. Leave as None to get all available strike prices.
        optionType: Can be either 'call' or 'put' or leave blank to get both.
        typeProfit: Will either be "chance_of_profit_short" or "chance_of_profit_long".
        profitFloor: The lower percentage on scale 0 to 1.
        profitCeiling: The higher percentage on scale 0 to 1.
        info: Will filter the results to get a specific value.

    Returns:
        Returns a list of dictionaries of key/value pairs for all stock option market data.
        If info parameter is provided, a list of strings is returned where the strings are the value of the key that matches info.
    """
    return r.options.find_options_by_specific_profitability(
        inputSymbols, expirationDate, strikePrice, optionType, 
        typeProfit, profitFloor, profitCeiling, info
    )


def find_options_by_strike(inputSymbols: str, strikePrice: str, 
                          optionType: Optional[str] = None, 
                          info: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Returns a list of all the option orders that match the search parameters

    Args:
        inputSymbols: The ticker of either a single stock or a list of stocks.
        strikePrice: Represents the strike price to filter for.
        optionType: Can be either 'call' or 'put' or leave blank to get both.
        info: Will filter the results to get a specific value.

    Returns:
        Returns a list of dictionaries of key/value pairs for all options of the stock that match the search parameters.
        If info parameter is provided, a list of strings is returned where the strings are the value of the key that matches info.
    """
    return r.options.find_options_by_strike(inputSymbols, strikePrice, optionType, info)


def find_tradable_options(symbol: str, expirationDate: Optional[str] = None, 
                         strikePrice: Optional[str] = None, 
                         optionType: Optional[str] = None, 
                         info: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Returns a list of all available options for a stock.

    Args:
        symbol: The ticker of the stock.
        expirationDate: Represents the expiration date in the format YYYY-MM-DD.
        strikePrice: Represents the strike price of the option.
        optionType: Can be either 'call' or 'put' or left blank to get both.
        info: Will filter the results to get a specific value.

    Returns:
        Returns a list of dictionaries of key/value pairs for all calls of the stock.
        If info parameter is provided, a list of strings is returned where the strings are the value of the key that matches info.
    """
    return r.options.find_tradable_options(symbol, expirationDate, strikePrice, optionType, info)


def get_aggregate_open_positions(info: Optional[str] = None, 
                                account_number: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Collapses all open option positions for a stock into a single dictionary.

    Args:
        info: Will filter the results to get a specific value.
        account_number: The account number to get positions for.

    Returns:
        Returns a list of dictionaries of key/value pairs for each order.
        If info parameter is provided, a list of strings is returned where the strings are the value of the key that matches info.
    """
    return r.options.get_aggregate_open_positions(info, account_number)


def get_aggregate_positions(info: Optional[str] = None, 
                            account_number: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Collapses all option orders for stocks into a single dictionary.

    Args:
        info: Will filter the results to get a specific value.
        account_number: The robinhood account number.

    Returns:
        Returns a list of dictionaries of key/value pairs for each order. If info parameter is provided, 
        a list of strings is returned where the strings are the value of the key that matches info.
    """
    return r.options.get_aggregate_positions(info, account_number)


def get_market_options(inputSymbols: Union[str, List[str]], 
                      expirationDate: Optional[str] = None, 
                      strikePrice: Optional[str] = None, 
                      optionType: Optional[str] = None, 
                      info: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Returns a list of option market data for several stock tickers.

    Args:
        inputSymbols: May be a single stock ticker or a list of stock tickers.
        expirationDate: Represents the expiration date in the format YYYY-MM-DD.
        strikePrice: Represents the price of the option.
        optionType: Can be either 'call' or 'put' or leave blank to get both.
        info: Will filter the results to get a specific value.

    Returns:
        Returns a list of dictionaries of key/value pairs for all stock option market data.
    """
    return r.options.get_market_options(inputSymbols, expirationDate, strikePrice, optionType, info)


def get_all_option_positions(info: Optional[str] = None, 
                            account_number: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Returns all option positions ever held for the account.

    Args:
        info: Will filter the results to get a specific value.
        account_number: The robinhood account number.

    Returns:
        Returns a list of dictionaries of key/value pairs for each option position.
    """
    return r.options.get_all_option_positions(info, account_number)


def get_open_option_positions(account_number: Optional[str] = None, 
                             info: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Returns all open option positions for the account.

    Args:
        account_number: The robinhood account number.
        info: Will filter the results to get a specific value.

    Returns:
        Returns a list of dictionaries of key/value pairs for each open option position.
    """
    return r.options.get_open_option_positions(account_number, info)


def get_chains(symbol: str, info: Optional[str] = None) -> Dict[str, Any]:
    """
    Returns the chain information of an option.

    Args:
        symbol: The ticker of the stock.
        info: Will filter the results to get a specific value.

    Returns:
        Returns a dictionary of key/value pairs for the option chain.
    """
    return r.options.get_chains(symbol, info)


def get_option_historicals(symbol: str, expirationDate: str, strikePrice: str, 
                          optionType: str, interval: str = '5minute', 
                          span: str = 'week', bounds: str = 'regular', 
                          info: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Returns the data that is used to make the graphs.

    Args:
        symbol: The ticker of the stock.
        expirationDate: Represents the expiration date in the format YYYY-MM-DD.
        strikePrice: Represents the price of the option.
        optionType: Can be either 'call' or 'put'.
        interval: Interval to retrieve data for. Values are '5minute', '10minute', 'hour', 'day', 'week'.
        span: Sets the range of the data to be either 'day', 'week', 'year', or '5year'.
        bounds: Represents if graph will include extended trading hours or just regular trading hours.
        info: Will filter the results to get a specific value.

    Returns:
        Returns a list of dictionaries where each dictionary represents a different time.
    """
    return r.options.get_option_historicals(symbol, expirationDate, strikePrice, optionType, interval, span, bounds, info)


def get_option_market_data_by_id(id: str, info: Optional[str] = None) -> Dict[str, Any]:
    """
    Returns the option market data for a stock, including the greeks, by the option id.

    Args:
        id: The id of the stock.
        info: Will filter the results to get a specific value.

    Returns:
        Returns a dictionary of key/value pairs for the stock.
    """
    return r.options.get_option_market_data_by_id(id, info)


def get_option_market_data(inputSymbols: Union[str, List[str]], 
                          expirationDate: str, strikePrice: str, 
                          optionType: str, info: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Returns the option market data for the stock option, including the greeks.

    Args:
        inputSymbols: May be a single stock ticker or a list of stock tickers.
        expirationDate: Represents the expiration date in the format YYYY-MM-DD.
        strikePrice: Represents the price of the option.
        optionType: Can be either 'call' or 'put'.
        info: Will filter the results to get a specific value.

    Returns:
        Returns a list of dictionaries of key/value pairs for all stock option market data.
    """
    return r.options.get_option_market_data(inputSymbols, expirationDate, strikePrice, optionType, info)


def get_option_instrument_data_by_id(id: str, info: Optional[str] = None) -> Dict[str, Any]:
    """
    Returns the option instrument information by the option id.

    Args:
        id: The id of the stock.
        info: Will filter the results to get a specific value.

    Returns:
        Returns a dictionary of key/value pairs for the stock.
    """
    return r.options.get_option_instrument_data_by_id(id, info)


def get_option_instrument_data(symbol: str, expirationDate: str, 
                              strikePrice: str, optionType: str, 
                              info: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Returns the option instrument data for the stock option.

    Args:
        symbol: The ticker of the stock.
        expirationDate: Represents the expiration date in the format YYYY-MM-DD.
        strikePrice: Represents the price of the option.
        optionType: Can be either 'call' or 'put'.
        info: Will filter the results to get a specific value.

    Returns:
        Returns a list of dictionaries of key/value pairs for all stock option instrument data.
    """
    return r.options.get_option_instrument_data(symbol, expirationDate, strikePrice, optionType, info)


# Define specialized sub-agents, each exposing a single tool. These agents
# describe the expected inputs, how to call the underlying tool, and how to
# present the JSON results to the user.
if Agent is not None:
    # Use an environment variable to determine which Vertex model to use, with
    # a sensible default. Sub-agents inherit this model unless overridden.
    _MODEL_NAME = "gemini-2.5-flash"

    find_options_by_expiration_agent = Agent(
        model=_MODEL_NAME,
        name="find_options_by_expiration_agent",
        instruction=(
            "This sub-agent finds options by expiration date for a given stock ticker. "
            "It invokes the `find_options_by_expiration` tool with the required parameters. "
            "Required parameters: inputSymbols (ticker symbol), expirationDate (YYYY-MM-DD format). "
            "Optional parameters: optionType ('call' or 'put', leave blank for both), "
            "info (specific field to extract from results). "
            "After calling the tool, provide a clear summary "
            "of the options found, including strike prices, premiums, and key metrics."
        ),
        description=(
            "Finds options contracts by expiration date for a specific stock ticker. "
            "Supports filtering by option type (call/put) and extracting specific fields."
        ),
        tools=[find_options_by_expiration],
    )

    find_options_by_expiration_and_strike_agent = Agent(
        model=_MODEL_NAME,
        name="find_options_by_expiration_and_strike_agent",
        instruction=(
            "This sub-agent finds options by both expiration date and strike price for a given stock ticker. "
            "It invokes the `find_options_by_expiration_and_strike` tool with the required parameters. "
            "Required parameters: inputSymbols (ticker symbol), expirationDate (YYYY-MM-DD format), "
            "strikePrice (strike price to filter for). "
            "Optional parameters: optionType ('call' or 'put', leave blank for both), "
            "info (specific field to extract from results). "
            "After calling the tool, provide a clear summary "
            "of the specific options found, including premiums, bid/ask spreads, and volume."
        ),
        description=(
            "Finds options contracts by both expiration date and strike price for a specific stock ticker. "
            "Supports filtering by option type (call/put) and extracting specific fields."
        ),
        tools=[find_options_by_expiration_and_strike],
    )

    find_options_by_specific_profitability_agent = Agent(
        model=_MODEL_NAME,
        name="find_options_by_specific_profitability_agent",
        instruction=(
            "This sub-agent finds options by profitability metrics for one or more stock tickers. "
            "It invokes the `find_options_by_specific_profitability` tool with the required parameters. "
            "Required parameters: inputSymbols (single ticker or list), typeProfit ('chance_of_profit_short' or 'chance_of_profit_long'), "
            "profitFloor (lower percentage 0-1), profitCeiling (higher percentage 0-1). "
            "Optional parameters: expirationDate (YYYY-MM-DD format), strikePrice, optionType ('call' or 'put'), "
            "info (specific field to extract from results). "
            "After calling the tool, provide a clear summary "
            "of the profitable options found, highlighting the profitability metrics and key details."
        ),
        description=(
            "Finds options contracts by profitability metrics within specified ranges. "
            "Supports filtering by expiration, strike price, option type, and extracting specific fields."
        ),
        tools=[find_options_by_specific_profitability],
    )

    find_options_by_strike_agent = Agent(
        model=_MODEL_NAME,
        name="find_options_by_strike_agent",
        instruction=(
            "This sub-agent finds options by strike price for a given stock ticker. "
            "It invokes the `find_options_by_strike` tool with the required parameters. "
            "Required parameters: inputSymbols (ticker symbol), strikePrice (strike price to filter for). "
            "Optional parameters: optionType ('call' or 'put', leave blank for both), "
            "info (specific field to extract from results). "
            "After calling the tool, provide a clear summary "
            "of the options found at the specified strike price, including different expiration dates and premiums."
        ),
        description=(
            "Finds options contracts by strike price for a specific stock ticker. "
            "Supports filtering by option type (call/put) and extracting specific fields."
        ),
        tools=[find_options_by_strike],
    )

    find_tradable_options_agent = Agent(
        model=_MODEL_NAME,
        name="find_tradable_options_agent",
        instruction=(
            "This sub-agent finds all available tradable options for a given stock ticker. "
            "It invokes the `find_tradable_options` tool with the required parameters. "
            "Required parameters: symbol (ticker symbol). "
            "Optional parameters: expirationDate (YYYY-MM-DD format), strikePrice, "
            "optionType ('call' or 'put', leave blank for both), info (specific field to extract from results). "
            "After calling the tool, provide a comprehensive summary "
            "of all available options, organized by expiration dates and strike prices."
        ),
        description=(
            "Finds all available tradable options contracts for a specific stock ticker. "
            "Supports filtering by expiration, strike price, option type, and extracting specific fields."
        ),
        tools=[find_tradable_options],
    )

    get_aggregate_open_positions_agent = Agent(
        model=_MODEL_NAME,
        name="get_aggregate_open_positions_agent",
        instruction=(
            "This sub-agent retrieves and aggregates all open option positions in the user's account. "
            "It invokes the `get_aggregate_open_positions` tool with optional parameters. "
            "Optional parameters: info (specific field to extract from results), "
            "account_number (specific account to query). "
            "After calling the tool, provide a clear summary "
            "of all open positions, including quantities, current values, and P&L information."
        ),
        description=(
            "Retrieves and collapses all open option positions for stocks into aggregated view. "
            "Provides current portfolio positions with profit/loss information."
        ),
        tools=[get_aggregate_open_positions],
    )

    get_aggregate_positions_agent = Agent(
        model=_MODEL_NAME,
        name="get_aggregate_positions_agent",
        instruction=(
            "This sub-agent retrieves and aggregates all option orders (both open and closed) in the user's account. "
            "It invokes the `get_aggregate_positions` tool with optional parameters. "
            "Optional parameters: info (specific field to extract from results), "
            "account_number (specific account to query). "
            "After calling the tool, provide a comprehensive summary "
            "of all option orders, including historical trades, current positions, and overall performance."
        ),
        description=(
            "Retrieves and collapses all option orders for stocks into aggregated view. "
            "Provides complete trading history and position information."
        ),
        tools=[get_aggregate_positions],
    )

    get_market_options_agent = Agent(
        model=_MODEL_NAME,
        name="get_market_options_agent",
        instruction=(
            "This sub-agent retrieves option market data for one or more stock tickers. "
            "It invokes the `get_market_options` tool with the required parameters. "
            "Required parameters: inputSymbols (single ticker or list). "
            "Optional parameters: expirationDate (YYYY-MM-DD format), strikePrice, "
            "optionType ('call' or 'put'), info (specific field to extract from results). "
            "After calling the tool, provide a clear summary "
            "of the market data including bid/ask prices, volume, and other key metrics."
        ),
        description=(
            "Retrieves option market data for stocks including pricing, volume, and trading information. "
            "Supports filtering by expiration, strike price, and option type."
        ),
        tools=[get_market_options],
    )

    get_all_option_positions_agent = Agent(
        model=_MODEL_NAME,
        name="get_all_option_positions_agent",
        instruction=(
            "This sub-agent retrieves all option positions ever held in the user's account. "
            "It invokes the `get_all_option_positions` tool with optional parameters. "
            "Optional parameters: info (specific field to extract from results), "
            "account_number (specific account to query). "
            "After calling the tool, provide a comprehensive summary "
            "of all historical option positions, including closed and current positions."
        ),
        description=(
            "Retrieves complete history of all option positions ever held in the account. "
            "Provides comprehensive trading history and position information."
        ),
        tools=[get_all_option_positions],
    )

    get_open_option_positions_agent = Agent(
        model=_MODEL_NAME,
        name="get_open_option_positions_agent",
        instruction=(
            "This sub-agent retrieves all currently open option positions in the user's account. "
            "It invokes the `get_open_option_positions` tool with optional parameters. "
            "Optional parameters: account_number (specific account to query), "
            "info (specific field to extract from results). "
            "After calling the tool, provide a clear summary "
            "of all open positions, including quantities, current values, and unrealized P&L."
        ),
        description=(
            "Retrieves all currently open option positions in the account. "
            "Provides current portfolio positions with real-time information."
        ),
        tools=[get_open_option_positions],
    )

    get_chains_agent = Agent(
        model=_MODEL_NAME,
        name="get_chains_agent",
        instruction=(
            "This sub-agent retrieves option chain information for a specific stock ticker. "
            "It invokes the `get_chains` tool with the required parameters. "
            "Required parameters: symbol (ticker symbol). "
            "Optional parameters: info (specific field to extract from results). "
            "After calling the tool, provide a clear summary "
            "of the option chain including available expiration dates, strike prices, and chain metadata."
        ),
        description=(
            "Retrieves option chain information for a specific stock ticker. "
            "Provides comprehensive chain data including available strikes and expirations."
        ),
        tools=[get_chains],
    )

    get_option_historicals_agent = Agent(
        model=_MODEL_NAME,
        name="get_option_historicals_agent",
        instruction=(
            "This sub-agent retrieves historical price data for a specific option contract. "
            "It invokes the `get_option_historicals` tool with the required parameters. "
            "Required parameters: symbol (ticker), expirationDate (YYYY-MM-DD), strikePrice, optionType ('call' or 'put'). "
            "Optional parameters: interval ('5minute', '10minute', 'hour', 'day', 'week'), "
            "span ('day', 'week', 'year', '5year'), bounds ('regular' or 'extended'), "
            "info (specific field to extract from results). "
            "After calling the tool, provide a clear summary "
            "of the historical price movements, trends, and key data points."
        ),
        description=(
            "Retrieves historical price data for specific option contracts. "
            "Supports various time intervals and spans for detailed analysis."
        ),
        tools=[get_option_historicals],
    )

    get_option_market_data_agent = Agent(
        model=_MODEL_NAME,
        name="get_option_market_data_agent",
        instruction=(
            "This sub-agent retrieves detailed market data for option contracts including Greeks. "
            "It invokes the `get_option_market_data` tool with the required parameters. "
            "Required parameters: inputSymbols (single ticker or list), expirationDate (YYYY-MM-DD), "
            "strikePrice, optionType ('call' or 'put'). "
            "Optional parameters: info (specific field to extract from results). "
            "After calling the tool, provide a detailed summary "
            "of the market data including Greeks (delta, gamma, theta, vega), implied volatility, and pricing."
        ),
        description=(
            "Retrieves detailed option market data including Greeks and implied volatility. "
            "Provides comprehensive analysis data for option contracts."
        ),
        tools=[get_option_market_data],
    )

    get_option_instrument_data_agent = Agent(
        model=_MODEL_NAME,
        name="get_option_instrument_data_agent",
        instruction=(
            "This sub-agent retrieves option contract specifications and instrument data. "
            "It invokes the `get_option_instrument_data` tool with the required parameters. "
            "Required parameters: symbol (ticker), expirationDate (YYYY-MM-DD), strikePrice, optionType ('call' or 'put'). "
            "Optional parameters: info (specific field to extract from results). "
            "After calling the tool, provide a clear summary "
            "of the contract specifications including settlement type, exercise style, and contract details."
        ),
        description=(
            "Retrieves option contract specifications and instrument data. "
            "Provides detailed contract information and specifications."
        ),
        tools=[get_option_instrument_data],
    )

robinhood_options_agent = Agent(
    model=_MODEL_NAME,
    name="robinhood_options_agent",
    instruction=(
        "This is the main coordinator agent for Robinhood options operations. "
        "Based on the user's request, delegate to the appropriate specialized sub-agent:\n\n"
        "**Options Search Agents:**\n"
        "• **find_options_by_expiration_agent**: For finding options by expiration date\n"
        "• **find_options_by_expiration_and_strike_agent**: For finding options by both expiration and strike\n"
        "• **find_options_by_specific_profitability_agent**: For finding options by profitability metrics\n"
        "• **find_options_by_strike_agent**: For finding options by strike price\n"
        "• **find_tradable_options_agent**: For finding all available options for a stock\n"
        "• **get_market_options_agent**: For getting market data for options\n"
        "• **get_chains_agent**: For getting option chain information\n\n"
        "**Position Management Agents:**\n"
        "• **get_aggregate_open_positions_agent**: For viewing current open option positions\n"
        "• **get_aggregate_positions_agent**: For viewing all option trading history\n"
        "• **get_all_option_positions_agent**: For viewing all historical option positions\n"
        "• **get_open_option_positions_agent**: For viewing current open positions\n\n"
        "**Data Analysis Agents:**\n"
        "• **get_option_historicals_agent**: For historical price data of specific options\n"
        "• **get_option_market_data_agent**: For detailed market data including Greeks\n"
        "• **get_option_instrument_data_agent**: For option contract specifications\n\n"
        "Analyze the user's request to determine which sub-agent is most appropriate. "
        "If the user asks about current positions, use the position management agents. "
        "If they want to search for new options to trade, use the search agents. "
        "If they need historical data or detailed analysis, use the data analysis agents. "
        "Always explain which sub-agent you're using and why."
    ),
    description=(
        "Main coordinator for Robinhood options operations. Provides comprehensive options trading "
        "capabilities including searching for options by various criteria (expiration, strike, profitability), "
        "finding all tradable options for stocks, managing current option positions, and analyzing "
        "historical data. Supports both calls and puts, with detailed filtering and analysis capabilities."
    ),
    sub_agents=[
        find_options_by_expiration_agent,
        find_options_by_expiration_and_strike_agent,
        find_options_by_specific_profitability_agent,
        find_options_by_strike_agent,
        find_tradable_options_agent,
        get_aggregate_open_positions_agent,
        get_aggregate_positions_agent,
        get_market_options_agent,
        get_all_option_positions_agent,
        get_open_option_positions_agent,
        get_chains_agent,
        get_option_historicals_agent,
        get_option_market_data_agent,
        get_option_instrument_data_agent,
    ],
    output_key="options_data",
)