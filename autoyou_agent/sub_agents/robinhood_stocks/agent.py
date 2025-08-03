"""
Robinhood Agent
================

This module defines a multi‑tool agent using Google's Agent Development Kit (ADK)
that exposes a suite of read‑only helpers around the `robin_stocks` library. The
functions in this module wrap common Robinhood API calls, such as searching
instruments, retrieving earnings reports, fetching corporate events, obtaining
fundamental metrics, looking up names and quotes, and more.

**Important:** This agent is intentionally limited to read‑only operations.  It
will **not** place or cancel any orders on your behalf.  Executing trades or
other high‑stakes financial activities is outside the scope of this example
and disallowed by policy.

To use this agent you must supply valid Robinhood credentials via environment
variables (`ROBIN_USERNAME`, `ROBIN_PASSWORD`, and optionally `ROBIN_MFA` for
two‑factor authentication).  When a tool is called for the first time it will
log into Robinhood using these credentials and cache the session for the
remainder of the process.

The following capabilities are implemented:

1. **search_stocks** – Searches for instruments matching a keyword.
2. **get_earnings** – Retrieves historical earnings reports for a ticker.
3. **get_corporate_events** – Returns corporate actions such as dividends and splits.
4. **get_financial_metrics** – Fetches fundamentals like P/E ratio and market cap.
5. **get_instrument_details** – Pulls instrument information from a URL.
6. **batch_get_instruments** – Looks up multiple instruments by ticker.
7. **get_real_time_prices** – Obtains the latest price data for one or more symbols.
8. **get_company_name_by_ticker** – Resolves a ticker to a company name.
9. **get_company_name_by_url** – Resolves an instrument URL to a company name.
10. **get_news** – Fetches recent news stories for a symbol.
11. **get_quotes** – Retrieves quote objects for one or more symbols.
"""

from __future__ import annotations

import os
from typing import Any, Dict, List, Optional, Union

try:
    # Import robin_stocks lazily so that this file can be analysed without the
    # package being installed.  At runtime you must have `robin-stocks`
    # available.
    import robin_stocks.robinhood as robinhood
except ImportError:
    robinhood = None  # type: ignore

try:
    # Import ADK components.  These imports will succeed only if
    # google-adk has been installed in your environment.
    from google.adk.agents import Agent
except Exception:
    Agent = None  # type: ignore

from dotenv import load_dotenv
load_dotenv()

__all__ = [
    # Root coordinator agent
    "robinhood_stocks_agent",
    # Sub‑agents for each tool
    "search_stocks_agent",
    "earnings_agent",
    "events_agent",
    "metrics_agent",
    "instrument_details_agent",
    "batch_instruments_agent",
    "prices_agent",
    "name_by_ticker_agent",
    "name_by_url_agent",
    "news_agent",
    "quotes_agent",
    "splits_agent",
    "historicals_agent",
    # Underlying tool functions
    "search_stocks",
    "get_earnings",
    "get_corporate_events",
    "get_financial_metrics",
    "get_instrument_details",
    "batch_get_instruments",
    "get_real_time_prices",
    "get_company_name_by_ticker",
    "get_company_name_by_url",
    "get_news",
    "get_quotes",
    "get_splits",
    "get_stock_historicals",
]


def search_stocks(query: str) -> List[Dict[str, Any]]:
    """Search for instruments by keyword.

    Args:
        query: A search term used to locate potential stock instruments.  This
            could be a ticker symbol, a company name or any partial keyword.

    Returns:
        list: A list of dictionaries for each matching instrument.  Each
        dictionary contains at least the following keys:
        ``symbol`` (ticker symbol), ``name`` (simple or full company name),
        ``instrument_url`` (API URL for the instrument) and ``fundamentals_url``
        (URL for retrieving fundamentals).  Additional fields returned by
        Robinhood are included unmodified.

    Example:

        >>> search_stocks("apple")
        [
            {
                "symbol": "AAPL",
                "name": "Apple",
                "instrument_url": "https://api.robinhood.com/instruments/…/",
                "fundamentals_url": "https://api.robinhood.com/fundamentals/AAPL/",
                ...
            },
            ...
        ]

    """
    
    results: List[Dict[str, Any]] = robinhood.stocks.find_instrument_data(query)  # type: ignore[attr-defined]
    instruments: List[Dict[str, Any]] = []
    for inst in results:
        # Build a simplified view but include the entire record as well
        instruments.append(
            {
                "symbol": inst.get("symbol"),
                "name": inst.get("simple_name") or inst.get("name"),
                "instrument_url": inst.get("url"),
                "fundamentals_url": inst.get("fundamentals"),
                **inst,
            }
        )
    return instruments


def get_earnings(symbol: str) -> List[Dict[str, Any]]:
    """Retrieve historical earnings reports for a given stock ticker.

    Args:
        symbol: The stock ticker (e.g., ``"AAPL"``).

    Returns:
        list: A list of dictionaries representing each quarterly earnings
        report.  Each dictionary includes fields such as ``year``, ``quarter``,
        ``eps`` (earnings per share), ``report`` (datetime of the report) and
        ``call`` (URL to the earnings call).  If no earnings are found the
        returned list will be empty.

    """
    
    earnings: List[Dict[str, Any]] = robinhood.stocks.get_earnings(symbol)  # type: ignore[attr-defined]
    return earnings


def get_corporate_events(symbol: str) -> List[Dict[str, Any]]:
    """Fetch corporate actions such as dividends or stock splits for a ticker.

    Args:
        symbol: The stock ticker to query (e.g., ``"MSFT"``).

    Returns:
        list: A list of event dictionaries returned by
        :func:`robinhood.stocks.get_events`.  Each event may describe a
        dividend, split or other corporate action.  The raw data includes
        execution dates and other fields.  An empty list indicates that no
        events were found for the symbol.

    Note:
        This endpoint returns events only for securities you currently or
        previously held in your account.  It is not a general corporate
        actions lookup for arbitrary tickers.

    """
    
    events: List[Dict[str, Any]] = robinhood.stocks.get_events(symbol)  # type: ignore[attr-defined]
    return events


def get_financial_metrics(symbols: List[str]) -> List[Dict[str, Any]]:
    """Fetch fundamental financial metrics for one or more tickers.

    Args:
        symbols: A single ticker symbol or a list of tickers.  The symbols
            should be uppercase (e.g., ``"GOOG"`` or ``["GOOG", "MSFT"]``).

    Returns:
        list: A list of dictionaries corresponding to each symbol.  Each
        dictionary contains fundamental data such as ``pe_ratio``, ``market_cap``,
        ``volume``, ``high_52_weeks``, ``low_52_weeks``, and descriptive
        information.  The list is ordered in the same order as the input.

    """
    
    metrics: List[Dict[str, Any]] = robinhood.stocks.get_fundamentals(symbols)  # type: ignore[attr-defined]
    return metrics


def get_instrument_details(url: str, info: str = "") -> Dict[str, Any]:
    """Retrieve details about an instrument using its API URL.

    Args:
        url: The instrument URL returned by search or quotes functions.  It
            typically has the form ``https://api.robinhood.com/instruments/<id>/``.
        info: Optional.  When provided, this acts as a key to extract a
            specific value from the instrument record (e.g., ``"symbol"`` or
            ``"name"``).  If omitted, the full instrument dictionary is
            returned.

    Returns:
        dict or Any: If ``info`` is ``None``, the return value is a dictionary
        containing all instrument fields.  Otherwise, the value associated
        with the ``info`` key is returned, or ``None`` if not present.

    """
    
    # Interpret an empty string as ``info=None`` to avoid Union types in the
    # function signature.  The ADK's function declaration schema does not
    # support AnyOf/Union types, so optional parameters must be encoded via
    # sentinel values.
    info_param: Optional[str] = info or None  # type: ignore[assignment]
    details = robinhood.stocks.get_instrument_by_url(url, info=info_param)  # type: ignore[attr-defined]
    # Always return a dictionary.  If a specific field was requested, wrap the
    # scalar value into a dict under the ``info`` key for consistency.
    if info_param is not None and not isinstance(details, dict):
        return {info_param: details}
    return details  # type: ignore[return-value]


def batch_get_instruments(symbols: List[str]) -> List[Dict[str, Any]]:
    """Fetch instrument objects for multiple tickers.

    Args:
        symbols: A single ticker or list of tickers to look up.

    Returns:
        list: A list of instrument dictionaries, one per symbol.  Each
        dictionary includes URLs for quotes, fundamentals, splits and other
        metadata.  The order corresponds to the input order.

    """
    
    instruments = robinhood.stocks.get_instruments_by_symbols(symbols)  # type: ignore[attr-defined]
    return instruments


def get_real_time_prices(
    symbols: List[str],
    price_type: str = "",
    include_extended_hours: bool = True,
) -> List[str]:
    """Obtain the most recent trade prices for one or more symbols.

    Args:
        symbols: A single ticker or a list of tickers.
        price_type: Optional.  If set to ``"ask_price"`` or ``"bid_price"``,
            retrieves that price instead of the last trade price.  When
            provided, ``include_extended_hours`` is ignored.
        include_extended_hours: Whether to include extended trading hours
            pricing when ``price_type`` is ``None``.  Default is ``True``.

    Returns:
        list: A list of price strings corresponding to each input symbol.  The
        values are strings because that is how Robinhood returns prices.

    """
    
    # ``price_type`` is an empty string by default; interpret that as None for
    # the underlying library call.  See ``get_instrument_details`` for why we
    # avoid Optional types here.
    price_param: Optional[str] = price_type or None  # type: ignore[assignment]
    prices = robinhood.stocks.get_latest_price(symbols, priceType=price_param, includeExtendedHours=include_extended_hours)  # type: ignore[attr-defined]
    return prices


def get_company_name_by_ticker(symbol: str) -> str:
    """Look up the company name associated with a ticker symbol.

    Args:
        symbol: The ticker symbol (e.g., ``"TSLA"``).

    Returns:
        str: The company’s simple name if available; otherwise the full name.

    """
    
    name: str = robinhood.stocks.get_name_by_symbol(symbol)  # type: ignore[attr-defined]
    return name


def get_company_name_by_url(url: str) -> str:
    """Look up the company name associated with an instrument URL.

    Args:
        url: The full instrument URL as returned by search or quotes tools.

    Returns:
        str: The company’s simple name if available; otherwise the full name.

    """
    
    name: str = robinhood.stocks.get_name_by_url(url)  # type: ignore[attr-defined]
    return name


def get_news(symbol: str) -> List[Dict[str, Any]]:
    """Fetch recent news articles for a given stock ticker.

    Args:
        symbol: The stock ticker symbol (e.g., ``"NFLX"``).

    Returns:
        list: A list of dictionaries representing news stories.  Each dictionary
        contains fields such as ``title``, ``summary``, ``published_at``,
        ``url`` and other metadata.  The list is empty if no news is found.

    """
    
    news: List[Dict[str, Any]] = robinhood.stocks.get_news(symbol)  # type: ignore[attr-defined]
    return news


def get_quotes(symbols: List[str], info: str = "") -> List[Any]:
    """Retrieve complete quote objects for one or more symbols.

    Args:
        symbols: A single ticker or list of tickers.
        info: Optional.  When provided, this should be the key to extract
            from each quote (e.g., ``"last_trade_price"``, ``"bid_price"``,
            etc.).  If omitted, the full quote dictionary is returned for
            each symbol.

    Returns:
        list: A list of quote dictionaries or specific values if ``info`` is
        specified.  The order of the list corresponds to the input order.

    """
    
    info_param: Optional[str] = info or None  # type: ignore[assignment]
    quotes: List[Any] = robinhood.stocks.get_quotes(symbols, info=info_param)  # type: ignore[attr-defined]
    # If a specific field was requested, ensure each element is wrapped in a
    # dictionary keyed by ``info`` for consistency across tool outputs.
    if info_param is not None:
        return [{info_param: q} for q in quotes]
    return quotes


def get_splits(symbol: str, info: str = "") -> List[Dict[str, Any]]:
    """Returns the date, divisor, and multiplier for when a stock split occurred.

    Args:
        symbol: The stock ticker (e.g., ``"AAPL"``).  
        info: Optional. When provided, this acts as a key to extract a
            specific value from each split record (e.g., ``"execution_date"``,
            ``"divisor"``, or ``"multiplier"``). If omitted, the full split
            dictionary is returned for each record.

    Returns:
        list: A list of dictionaries representing each stock split. Each dictionary
        contains fields such as ``execution_date``, ``divisor``, and ``multiplier``.
        If no splits are found the returned list will be empty.

    """
    
    info_param: Optional[str] = info or None  # type: ignore[assignment]
    splits: List[Dict[str, Any]] = robinhood.stocks.get_splits(symbol, info=info_param)  # type: ignore[attr-defined]
    # If a specific field was requested, ensure each element is wrapped in a
    # dictionary keyed by ``info`` for consistency across tool outputs.
    if info_param is not None and not isinstance(splits[0], dict) if splits else False:
        return [{info_param: s} for s in splits]
    return splits


def get_stock_historicals(
    symbols: List[str],
    interval: str = "hour",
    span: str = "week",
    bounds: str = "regular",
    info: str = ""
) -> List[Dict[str, Any]]:
    """Retrieve historical price data for one or more stock tickers.

    Args:
        symbols: A single ticker or list of tickers.
        interval: Optional. The time interval between data points. Valid values are
            ``"5minute"``, ``"10minute"``, ``"hour"``, ``"day"``, or ``"week"``.
            Default is ``"hour"``.
        span: Optional. The total time span of data to retrieve. Valid values are
            ``"day"``, ``"week"``, ``"month"``, ``"3month"``, ``"year"``, or
            ``"5year"``. Default is ``"week"``.
        bounds: Optional. Whether to include extended trading hours data.
            Valid values are ``"extended"``, ``"trading"``, or ``"regular"``.
            Default is ``"regular"``.
        info: Optional. When provided, this acts as a key to extract a
            specific value from each historical data point (e.g., ``"open_price"``,
            ``"close_price"``, or ``"volume"``). If omitted, the full data
            dictionary is returned for each point.

    Returns:
        list: A list of dictionaries representing historical price data points.
        Each dictionary contains fields such as ``begins_at``, ``open_price``,
        ``close_price``, ``high_price``, ``low_price``, and ``volume``.
        If multiple symbols are provided, the data points are concatenated
        with a ``symbol`` field indicating which ticker they belong to.

    Note:
        The ``bounds`` parameter can only be set to ``"extended"`` or
        ``"trading"`` when ``span`` is set to ``"day"``.

    """
    
    info_param: Optional[str] = info or None  # type: ignore[assignment]
    historicals: List[Dict[str, Any]] = robinhood.stocks.get_stock_historicals(
        symbols, interval=interval, span=span, bounds=bounds, info=info_param
    )  # type: ignore[attr-defined]
    # If a specific field was requested, ensure each element is wrapped in a
    # dictionary keyed by ``info`` for consistency across tool outputs.
    if info_param is not None and not isinstance(historicals[0], dict) if historicals else False:
        return [{info_param: h} for h in historicals]
    return historicals


# Define specialized sub‑agents, each exposing a single tool.  These agents
# describe the expected inputs, how to call the underlying tool, and how to
# present the JSON results to the user.
if Agent is not None:
    # Use an environment variable to determine which Vertex model to use, with
    # a sensible default.  Sub‑agents inherit this model unless overridden.
    _MODEL_NAME = os.getenv("ROOT_AGENT_MODEL", "gemini-2.5-flash")

    search_stocks_agent = Agent(
        model=_MODEL_NAME,
        name="search_stocks_agent",
        instruction=(
            "This sub‑agent searches for stock instruments matching a keyword. Accept a "
            "single input `query` which can be a ticker symbol or part of a company name. "
            "Call the `search_stocks` tool with the provided query and return the JSON "
            "results. In your user‑facing answer, list each instrument’s symbol, name and "
            "fundamentals URL in a readable format."
        ),
        description="Searches instruments by keyword using the search_stocks tool.",
        tools=[search_stocks],
    )

    earnings_agent = Agent(
        model=_MODEL_NAME,
        name="earnings_agent",
        instruction=(
            "This sub‑agent retrieves historical earnings reports for a given ticker. "
            "Accept a single input `symbol` (e.g. 'AAPL'), call the `get_earnings` tool, "
            "and return the JSON array of earnings. Summarize each entry by stating the "
            "year, quarter, EPS (earnings per share) and report date in a human‑readable "
            "format."
        ),
        description="Fetches quarterly earnings data via the get_earnings tool.",
        tools=[get_earnings],
    )

    events_agent = Agent(
        model=_MODEL_NAME,
        name="events_agent",
        instruction=(
            "This sub‑agent returns corporate events such as dividends or splits for a "
            "ticker you own or have owned. Accept an input `symbol`, call the "
            "`get_corporate_events` tool and return the JSON list of events. Provide a "
            "friendly description of each event including the type (dividend or split) "
            "and its execution date."
        ),
        description="Looks up dividends and splits using the get_corporate_events tool.",
        tools=[get_corporate_events],
    )

    metrics_agent = Agent(
        model=_MODEL_NAME,
        name="financial_metrics_agent",
        instruction=(
            "This sub‑agent fetches fundamental metrics for one or more tickers. Accept a "
            "list of stock symbols under `symbols`. Call the `get_financial_metrics` tool "
            "with the list and return the JSON response. For the user, present the key "
            "metrics for each symbol (e.g., P/E ratio, market cap, volume, 52‑week high "
            "and low) in an easy‑to‑read table or bullet list."
        ),
        description="Retrieves fundamentals like P/E ratio and market cap using get_financial_metrics.",
        tools=[get_financial_metrics],
    )

    instrument_details_agent = Agent(
        model=_MODEL_NAME,
        name="instrument_details_agent",
        instruction=(
            "This sub‑agent retrieves details about an instrument via its API URL. Accept "
            "two inputs: `url` (the instrument’s API URL) and `info` (optional field name "
            "to extract). Call the `get_instrument_details` tool. Return the JSON result. "
            "If `info` is provided, extract that field from the result; otherwise return "
            "the full dictionary. Summarize the key attributes (symbol, name, tradeable, etc.) "
            "for the user."
        ),
        description="Gets instrument details via URL using get_instrument_details.",
        tools=[get_instrument_details],
    )

    batch_instruments_agent = Agent(
        model=_MODEL_NAME,
        name="batch_instruments_agent",
        instruction=(
            "This sub‑agent performs a batch lookup of multiple instruments. Accept a list "
            "of tickers under `symbols`. Call the `batch_get_instruments` tool and return "
            "its JSON output. Present the important fields from each instrument (e.g., symbol, "
            "name and quote URL) in a clear, structured list."
        ),
        description="Batch fetches instrument objects using batch_get_instruments.",
        tools=[batch_get_instruments],
    )

    prices_agent = Agent(
        model=_MODEL_NAME,
        name="real_time_prices_agent",
        instruction=(
            "This sub‑agent fetches the latest trade prices for one or more symbols. Accept a "
            "list `symbols`, a string `price_type` (leave empty for last trade price, or set "
            "to 'ask_price'/'bid_price'), and a boolean `include_extended_hours` to include "
            "after‑hours prices. Call the `get_real_time_prices` tool with these parameters. "
            "Return the raw JSON list of price strings and then report the prices in a readable "
            "format alongside their corresponding symbols."
        ),
        description="Obtains latest prices via get_real_time_prices.",
        tools=[get_real_time_prices],
    )

    name_by_ticker_agent = Agent(
        model=_MODEL_NAME,
        name="company_name_by_ticker_agent",
        instruction=(
            "This sub‑agent finds the company name given a ticker symbol. Accept a single "
            "input `symbol`, call the `get_company_name_by_ticker` tool, and return the name "
            "as JSON. For the user, simply state the company name corresponding to the ticker."
        ),
        description="Resolves a ticker to a company name using get_company_name_by_ticker.",
        tools=[get_company_name_by_ticker],
    )

    name_by_url_agent = Agent(
        model=_MODEL_NAME,
        name="company_name_by_url_agent",
        instruction=(
            "This sub‑agent finds the company name given an instrument URL. Accept a single "
            "input `url`, call the `get_company_name_by_url` tool and return the name. "
            "Present the company’s name clearly to the user."
        ),
        description="Resolves an instrument URL to a company name using get_company_name_by_url.",
        tools=[get_company_name_by_url],
    )

    news_agent = Agent(
        model=_MODEL_NAME,
        name="news_agent",
        instruction=(
            "This sub‑agent fetches recent news stories for a given ticker. Accept an input "
            "`symbol`, call the `get_news` tool, and return its JSON list. In your answer, "
            "summarize each article with its headline, publication date and URL."
        ),
        description="Fetches news articles for a ticker using get_news.",
        tools=[get_news],
    )

    quotes_agent = Agent(
        model=_MODEL_NAME,
        name="quotes_agent",
        instruction=(
            "This sub‑agent retrieves full quote data for one or more symbols. Accept a list "
            "`symbols` and an optional string `info` to request a specific field (e.g., "
            "'last_trade_price'). Call the `get_quotes` tool and return the JSON response. "
            "If `info` is provided, report only that value for each symbol; otherwise include "
            "key fields such as last trade, bid and ask prices in your user‑facing summary."
        ),
        description="Gets quote objects via get_quotes.",
        tools=[get_quotes],
    )

    splits_agent = Agent(
        model=_MODEL_NAME,
        name="splits_agent",
        instruction=(
            "This sub‑agent retrieves stock split information for a given ticker. Accept a "
            "single input `symbol` (e.g. 'AAPL') and an optional string `info` to request a "
            "specific field. Call the `get_splits` tool and return the JSON array of splits. "
            "Summarize each entry by stating the execution date, divisor, and multiplier in a "
            "human‑readable format. If no splits are found, clearly indicate this to the user."
        ),
        description="Fetches stock split data via the get_splits tool.",
        tools=[get_splits],
    )

    historicals_agent = Agent(
        model=_MODEL_NAME,
        name="historicals_agent",
        instruction=(
            "This sub‑agent retrieves historical price data for one or more tickers. Accept "
            "inputs: `symbols` (a list of tickers), `interval` (time between data points), "
            "`span` (total time range), `bounds` (trading hours type), and optional `info` "
            "(specific field to extract). Call the `get_stock_historicals` tool with these "
            "parameters and return the JSON response. Present the data in a clear, structured "
            "format showing the time periods and corresponding price information."
        ),
        description="Retrieves historical price data using get_stock_historicals.",
        tools=[get_stock_historicals],
    )

    
else:
    # If ADK cannot be imported (e.g., during type checking without the package),
    # expose None placeholders for agents to avoid NameError at import time.
    search_stocks_agent = None  # type: ignore
    earnings_agent = None  # type: ignore
    events_agent = None  # type: ignore
    metrics_agent = None  # type: ignore
    instrument_details_agent = None  # type: ignore
    batch_instruments_agent = None  # type: ignore
    prices_agent = None  # type: ignore
    name_by_ticker_agent = None  # type: ignore
    name_by_url_agent = None  # type: ignore
    news_agent = None  # type: ignore
    quotes_agent = None  # type: ignore
    splits_agent = None  # type: ignore
    historicals_agent = None  # type: ignore

# Coordinator agent that delegates to sub‑agents.  It contains no direct tools.
robinhood_stocks_agent = Agent(
    model=_MODEL_NAME,
    name="robinhood_stocks_agent",
    instruction=(
        "You are a finance assistant responsible for routing user requests to the "
        "appropriate sub‑agent. Do not call any tools yourself. Instead, when a user "
        "asks a question, determine which sub‑agent’s capabilities match the request and "
        "delegate the task. Return the sub‑agent’s result to the user. Do not attempt to "
        "place or modify trades."
    ),
    description="Root coordinator agent for Robinhood read‑only operations.",
    sub_agents=[
        search_stocks_agent,
        earnings_agent,
        events_agent,
        metrics_agent,
        instrument_details_agent,
        batch_instruments_agent,
        prices_agent,
        name_by_ticker_agent,
        name_by_url_agent,
        news_agent,
        quotes_agent,
        splits_agent,
        historicals_agent,
    ],
)