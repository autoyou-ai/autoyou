"""robinhood_orders_agent for placing and cancelling orders on Robinhood"""

import os
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv

from google.adk import Agent

import robin_stocks.robinhood as r

from . import prompt
from .prompt import AGENT_INSTRUCTION

# Load environment variables
load_dotenv()

# Model name for sub-agents
_MODEL_NAME = os.getenv("ROOT_AGENT_MODEL")

# Load Phoenix Account function
def load_phoenix_account() -> dict:
    """Returns unified information about your account."""
    return r.load_phoenix_account()

# Order Confirmation Function
def confirm_order_details(order_summary: str) -> Dict[str, Any]:
    """
    Presents order details to user for confirmation before execution.
    
    Args:
        order_summary: A detailed summary of the order to be placed
        
    Returns:
        Dictionary containing confirmation status and user response
    """
    return {
        "confirmation_required": True,
        "order_summary": order_summary,
        "message": "Please review the order details above and confirm if you want to proceed. Type 'yes', 'confirm', or 'proceed' to execute the order.",
        "status": "awaiting_confirmation"
    }

# Order Management Functions

def load_phoenix_account() -> Dict[str, Any]:
    """
    Loads and returns comprehensive account information from Robinhood.
    
    Returns:
        Dict containing account information with keys:
        - account_number: The account number
        - buying_power: Available buying power
        - cash: Cash balance
        - day_trade_buying_power: Day trading buying power
        - max_ach_early_access_amount: Maximum ACH early access amount
        - cash_available_for_withdrawal: Cash available for withdrawal
        - cash_held_for_orders: Cash held for pending orders
        - uncleared_deposits: Amount of uncleared deposits
        - unsettled_funds: Amount of unsettled funds
        - withdrawable_amount: Amount available for withdrawal
        - gold_buying_power: Gold account buying power (if applicable)
        - option_buying_power: Options buying power
        - And many other account-related fields
    """
    return r.account.load_phoenix_account()

__all__ = [
    # Root coordinator agent
    "robinhood_orders_agent",
    # Account management
    "load_phoenix_account",
    # Order confirmation
    "confirm_order_details",
    # Cancellation sub-agents
    "cancel_all_crypto_orders_agent",
    "cancel_all_option_orders_agent",
    "cancel_all_stock_orders_agent",
    "cancel_crypto_order_agent",
    "cancel_option_order_agent",
    "cancel_stock_order_agent",
    # Order information sub-agents
    "find_stock_orders_agent",
    "get_all_crypto_orders_agent",
    "get_all_open_crypto_orders_agent",
    "get_all_option_orders_agent",
    "get_all_open_option_orders_agent",
    "get_all_stock_orders_agent",
    "get_all_open_stock_orders_agent",
    "get_crypto_order_info_agent",
    "get_option_order_info_agent",
    "get_stock_order_info_agent",
    # Order placement sub-agents - Stocks
    "order_buy_market_agent",
    "order_buy_limit_agent",
    "order_buy_stop_limit_agent",
    "order_buy_stop_loss_agent",
    "order_buy_trailing_stop_agent",
    "order_sell_market_agent",
    "order_sell_limit_agent",
    "order_sell_stop_limit_agent",
    "order_sell_stop_loss_agent",
    "order_sell_trailing_stop_agent",
    # Order placement sub-agents - Fractional
    "order_buy_fractional_by_price_agent",
    "order_buy_fractional_by_quantity_agent",
    "order_sell_fractional_by_price_agent",
    "order_sell_fractional_by_quantity_agent",
    # Order placement sub-agents - Crypto
    "order_buy_crypto_by_price_agent",
    "order_buy_crypto_by_quantity_agent",
    "order_buy_crypto_limit_agent",
    "order_buy_crypto_limit_by_price_agent",
    "order_sell_crypto_by_price_agent",
    "order_sell_crypto_by_quantity_agent",
    "order_sell_crypto_limit_agent",
    "order_sell_crypto_limit_by_price_agent",
    # Order placement sub-agents - Options
    "order_buy_option_limit_agent",
    "order_buy_option_stop_limit_agent",
    "order_sell_option_limit_agent",
    "order_sell_option_stop_limit_agent",
    "order_option_credit_spread_agent",
    "order_option_debit_spread_agent",
    # Generic order sub-agents
    "order_trailing_stop_agent",
    # Underlying tool functions
    "cancel_all_crypto_orders",
    "cancel_all_option_orders",
    "cancel_all_stock_orders",
    "cancel_crypto_order",
    "cancel_option_order",
    "cancel_stock_order",
    "find_stock_orders",
    "get_all_crypto_orders",
    "get_all_open_crypto_orders",
    "get_all_option_orders",
    "get_all_open_option_orders",
    "get_all_stock_orders",
    "get_all_open_stock_orders",
    "get_crypto_order_info",
    "get_option_order_info",
    "get_stock_order_info",
    "order_buy_crypto_by_price",
    "order_buy_crypto_by_quantity",
    "order_buy_crypto_limit",
    "order_buy_crypto_limit_by_price",
    "order_buy_fractional_by_price",
    "order_buy_fractional_by_quantity",
    "order_buy_limit",
    "order_buy_market",
    "order_buy_option_limit",
    "order_buy_option_stop_limit",
    "order_buy_stop_limit",
    "order_buy_stop_loss",
    "order_buy_trailing_stop",
    "order_option_credit_spread",
    "order_option_debit_spread",
    "order_option_spread",
    "order_sell_crypto_by_price",
    "order_sell_crypto_by_quantity",
    "order_sell_crypto_limit",
    "order_sell_crypto_limit_by_price",
    "order_sell_fractional_by_price",
    "order_sell_fractional_by_quantity",
    "order_sell_limit_price",
    "order_sell_stock_market",
    "order_sell_option_limit",
    "order_sell_option_stop_limit",
    "order_sell_stop_limit",
    "order_sell_stop_loss",
    "order_sell_trailing_stop",
    "order_trailing_stop",
]


# Cancellation Functions
def cancel_all_crypto_orders() -> Dict[str, Any]:
    """
    Cancels all crypto orders.

    Returns:
        Dictionary containing information about the canceled orders.
    """
    return r.orders.cancel_all_crypto_orders()


def cancel_all_option_orders(account_number: Optional[str] = None) -> Dict[str, Any]:
    """
    Cancels all option orders.

    Args:
        account_number: The account number to cancel orders for.

    Returns:
        Dictionary containing information about the canceled orders.
    """
    return r.orders.cancel_all_option_orders(account_number)


def cancel_all_stock_orders(account_number: Optional[str] = None) -> Dict[str, Any]:
    """
    Cancels all stock orders.

    Args:
        account_number: The account number to cancel orders for.

    Returns:
        Dictionary containing information about the canceled orders.
    """
    return r.orders.cancel_all_stock_orders(account_number)


def cancel_crypto_order(order_id: str) -> Dict[str, Any]:
    """
    Cancels a specific crypto order.

    Args:
        order_id: The ID of the order to cancel.

    Returns:
        Dictionary containing information about the canceled order.
    """
    return r.orders.cancel_crypto_order(order_id)


def cancel_option_order(order_id: str) -> Dict[str, Any]:
    """
    Cancels a specific option order.

    Args:
        order_id: The ID of the order to cancel.

    Returns:
        Dictionary containing information about the canceled order.
    """
    return r.orders.cancel_option_order(order_id)


def cancel_stock_order(order_id: str) -> Dict[str, Any]:
    """
    Cancels a specific stock order.

    Args:
        order_id: The ID of the order to cancel.

    Returns:
        Dictionary containing information about the canceled order.
    """
    return r.orders.cancel_stock_order(order_id)


# Order Information Functions
def find_stock_orders(symbol: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Returns a list of orders that match the symbol passed in.

    Args:
        symbol: The symbol to search for.

    Returns:
        A list of orders matching the symbol.
    """
    return r.orders.find_stock_orders(symbol)


def get_all_crypto_orders() -> List[Dict[str, Any]]:
    """
    Returns a list of all crypto orders.

    Returns:
        A list of all crypto orders.
    """
    return r.orders.get_all_crypto_orders()


def get_all_open_crypto_orders() -> List[Dict[str, Any]]:
    """
    Returns a list of all open crypto orders.

    Returns:
        A list of all open crypto orders.
    """
    return r.orders.get_all_open_crypto_orders()


def get_all_option_orders(info: Optional[str] = None, account_number: Optional[str] = None, start_date: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Returns a list of all option orders.

    Args:
        info: Will filter the results to get a specific value.
        account_number: The account number to get orders for.
        start_date: Sets the date of when to start returning orders.

    Returns:
        A list of all option orders.
    """
    return r.orders.get_all_option_orders(info, account_number, start_date)


def get_all_open_option_orders(info: Optional[str] = None, account_number: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Returns a list of all open option orders.

    Args:
        info: Will filter the results to get a specific value.
        account_number: The account number to get orders for.

    Returns:
        A list of all open option orders.
    """
    return r.orders.get_all_open_option_orders(info, account_number)


def get_all_stock_orders(info: Optional[str] = None, account_number: Optional[str] = None, start_date: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Returns a list of all stock orders.

    Args:
        info: Will filter the results to get a specific value.
        account_number: The account number to get orders for.
        start_date: Sets the date of when to start returning orders.

    Returns:
        A list of all stock orders.
    """
    return r.orders.get_all_stock_orders(info, account_number, start_date)


def get_all_open_stock_orders(info: Optional[str] = None, account_number: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Returns a list of all open stock orders.

    Args:
        info: Will filter the results to get a specific value.
        account_number: The account number to get orders for.

    Returns:
        A list of all open stock orders.
    """
    return r.orders.get_all_open_stock_orders(info, account_number)


def get_crypto_order_info(order_id: str) -> Dict[str, Any]:
    """
    Returns the information for a specific crypto order.

    Args:
        order_id: The ID of the order to get information for.

    Returns:
        Dictionary containing information about the order.
    """
    return r.orders.get_crypto_order_info(order_id)


def get_option_order_info(order_id: str) -> Dict[str, Any]:
    """
    Returns the information for a specific option order.

    Args:
        order_id: The ID of the order to get information for.

    Returns:
        Dictionary containing information about the order.
    """
    return r.orders.get_option_order_info(order_id)


def get_stock_order_info(order_id: str) -> Dict[str, Any]:
    """
    Returns the information for a specific stock order.

    Args:
        order_id: The ID of the order to get information for.

    Returns:
        Dictionary containing information about the order.
    """
    return r.orders.get_stock_order_info(order_id)


# Order Placement Functions - Stocks
def order_buy_market(symbol: str, quantity: float, account_number: Optional[str] = None, timeInForce: str = 'gtc',
                    extendedHours: bool = False, jsonify: bool = True) -> Dict[str, Any]:
    """
    Submits a market order to buy a stock.

    Args:
        symbol: The stock ticker of the stock to purchase.
        quantity: The number of stocks to buy.
        account_number: The account number to place the order for.
        timeInForce: 'gtc' = good until cancelled, 'gfd' = good for the day, 'ioc' = immediate or cancel, 'opg' = execute at opening.
        extendedHours: Whether to allow trading during extended hours.
        jsonify: If set to False, function will return the request object which contains status code and headers.

    Returns:
        Dictionary containing information regarding the purchase of stocks, such as the order id, the state of order (queued, confirmed, filled, failed, canceled, etc.).
    """
    return r.orders.order_buy_market(symbol, quantity, account_number, timeInForce, extendedHours, jsonify)


def order_buy_limit(symbol: str, quantity: float, limitPrice: float, account_number: Optional[str] = None, timeInForce: str = 'gtc',
                   extendedHours: bool = False, jsonify: bool = True) -> Dict[str, Any]:
    """
    Submits a limit order to buy a stock.

    Args:
        symbol: The stock ticker of the stock to purchase.
        quantity: The number of stocks to buy.
        limitPrice: The maximum price you're willing to pay per share.
        account_number: The account number to place the order for.
        timeInForce: 'gtc' = good until cancelled, 'gfd' = good for the day, 'ioc' = immediate or cancel, 'opg' = execute at opening.
        extendedHours: Whether to allow trading during extended hours.
        jsonify: If set to False, function will return the request object which contains status code and headers.

    Returns:
        Dictionary containing information regarding the purchase of stocks, such as the order id, the state of order (queued, confirmed, filled, failed, canceled, etc.).
    """
    return r.orders.order_buy_limit(symbol, quantity, limitPrice, account_number, timeInForce, extendedHours, jsonify)


def order_buy_stop_limit(symbol: str, quantity: float, limitPrice: float, stopPrice: float, account_number: Optional[str] = None,
                        timeInForce: str = 'gtc', extendedHours: bool = False, jsonify: bool = True) -> Dict[str, Any]:
    """
    Submits a stop limit order to buy a stock.

    Args:
        symbol: The stock ticker of the stock to purchase.
        quantity: The number of stocks to buy.
        limitPrice: The maximum price you're willing to pay per share.
        stopPrice: The price at which the stop trigger converts to a limit order.
        account_number: The account number to place the order for.
        timeInForce: 'gtc' = good until cancelled, 'gfd' = good for the day, 'ioc' = immediate or cancel, 'opg' = execute at opening.
        extendedHours: Whether to allow trading during extended hours.
        jsonify: If set to False, function will return the request object which contains status code and headers.

    Returns:
        Dictionary containing information regarding the purchase of stocks, such as the order id, the state of order (queued, confirmed, filled, failed, canceled, etc.).
    """
    return r.orders.order_buy_stop_limit(symbol, quantity, limitPrice, stopPrice, account_number, timeInForce, extendedHours, jsonify)


def order_buy_stop_loss(symbol: str, quantity: float, stopPrice: float, account_number: Optional[str] = None,
                       timeInForce: str = 'gtc', extendedHours: bool = False, jsonify: bool = True) -> Dict[str, Any]:
    """
    Submits a stop loss order to buy a stock.

    Args:
        symbol: The stock ticker of the stock to purchase.
        quantity: The number of stocks to buy.
        stopPrice: The price at which the order converts to a market order.
        account_number: The account number to place the order for.
        timeInForce: 'gtc' = good until cancelled, 'gfd' = good for the day, 'ioc' = immediate or cancel, 'opg' = execute at opening.
        extendedHours: Whether to allow trading during extended hours.
        jsonify: If set to False, function will return the request object which contains status code and headers.

    Returns:
        Dictionary containing information regarding the purchase of stocks, such as the order id, the state of order (queued, confirmed, filled, failed, canceled, etc.).
    """
    return r.orders.order_buy_stop_loss(symbol, quantity, stopPrice, account_number, timeInForce, extendedHours, jsonify)


def order_buy_trailing_stop(symbol: str, quantity: float, trailAmount: float, trailType: str = 'percentage',
                           timeInForce: str = 'gtc', extendedHours: bool = False, jsonify: bool = True) -> Dict[str, Any]:
    """
    Submits a trailing stop order to buy a stock.

    Args:
        symbol: The stock ticker of the stock to purchase.
        quantity: The number of stocks to buy.
        trailAmount: The trailing amount of the stop price. If trailType is 'percentage', this is a percentage. If trailType is 'price', this is a dollar amount.
        trailType: Either 'percentage' or 'price'.
        timeInForce: 'gtc' = good until cancelled, 'gfd' = good for the day, 'ioc' = immediate or cancel, 'opg' = execute at opening.
        extendedHours: Whether to allow trading during extended hours.
        jsonify: If set to False, function will return the request object which contains status code and headers.

    Returns:
        Dictionary containing information regarding the purchase of stocks, such as the order id, the state of order (queued, confirmed, filled, failed, canceled, etc.).
    """
    return r.orders.order_buy_trailing_stop(symbol, quantity, trailAmount, trailType, timeInForce, extendedHours, jsonify)


def order_sell_stock_market(symbol: str, quantity: float, account_number: Optional[str] = None, timeInForce: str = 'gtc',
                          extendedHours: bool = False, jsonify: bool = True) -> Dict[str, Any]:
    """
    Submits a market order to sell a stock.

    Args:
        symbol: The stock ticker of the stock to sell.
        quantity: The number of stocks to sell.
        account_number: The account number to place the order for.
        timeInForce: 'gtc' = good until cancelled, 'gfd' = good for the day, 'ioc' = immediate or cancel, 'opg' = execute at opening.
        extendedHours: Whether to allow trading during extended hours.
        jsonify: If set to False, function will return the request object which contains status code and headers.

    Returns:
        Dictionary containing information regarding the selling of stocks, such as the order id, the state of order (queued, confirmed, filled, failed, canceled, etc.).
    """
    return r.orders.order_sell_market(symbol, quantity, account_number, timeInForce, extendedHours, jsonify)


def order_sell_limit_price(symbol: str, quantity: float, limitPrice: float, account_number: Optional[str] = None, timeInForce: str = 'gtc',
                    extendedHours: bool = False, jsonify: bool = True) -> Dict[str, Any]:
    """
    Submits a limit order to sell a stock.

    Args:
        symbol: The stock ticker of the stock to sell.
        quantity: The number of stocks to sell.
        limitPrice: The minimum price you're willing to sell per share.
        account_number: The account number to place the order for.
        timeInForce: 'gtc' = good until cancelled, 'gfd' = good for the day, 'ioc' = immediate or cancel, 'opg' = execute at opening.
        extendedHours: Whether to allow trading during extended hours.
        jsonify: If set to False, function will return the request object which contains status code and headers.

    Returns:
        Dictionary containing information regarding the selling of stocks, such as the order id, the state of order (queued, confirmed, filled, failed, canceled, etc.).
    """
    return r.orders.order_sell_limit(symbol, quantity, limitPrice, account_number, timeInForce, extendedHours, jsonify)


def order_sell_stop_limit(symbol: str, quantity: float, limitPrice: float, stopPrice: float, account_number: Optional[str] = None,
                         timeInForce: str = 'gtc', extendedHours: bool = False, jsonify: bool = True) -> Dict[str, Any]:
    """
    Submits a stop limit order to sell a stock.

    Args:
        symbol: The stock ticker of the stock to sell.
        quantity: The number of stocks to sell.
        limitPrice: The minimum price you're willing to sell per share.
        stopPrice: The price at which the stop trigger converts to a limit order.
        account_number: The account number to place the order for.
        timeInForce: 'gtc' = good until cancelled, 'gfd' = good for the day, 'ioc' = immediate or cancel, 'opg' = execute at opening.
        extendedHours: Whether to allow trading during extended hours.
        jsonify: If set to False, function will return the request object which contains status code and headers.

    Returns:
        Dictionary containing information regarding the selling of stocks, such as the order id, the state of order (queued, confirmed, filled, failed, canceled, etc.).
    """
    return r.orders.order_sell_stop_limit(symbol, quantity, limitPrice, stopPrice, account_number, timeInForce, extendedHours, jsonify)


def order_sell_stop_loss(symbol: str, quantity: float, stopPrice: float, account_number: Optional[str] = None,
                        timeInForce: str = 'gtc', extendedHours: bool = False, jsonify: bool = True) -> Dict[str, Any]:
    """
    Submits a stop loss order to sell a stock.

    Args:
        symbol: The stock ticker of the stock to sell.
        quantity: The number of stocks to sell.
        stopPrice: The price at which the order converts to a market order.
        account_number: The account number to place the order for.
        timeInForce: 'gtc' = good until cancelled, 'gfd' = good for the day, 'ioc' = immediate or cancel, 'opg' = execute at opening.
        extendedHours: Whether to allow trading during extended hours.
        jsonify: If set to False, function will return the request object which contains status code and headers.

    Returns:
        Dictionary containing information regarding the selling of stocks, such as the order id, the state of order (queued, confirmed, filled, failed, canceled, etc.).
    """
    return r.orders.order_sell_stop_loss(symbol, quantity, stopPrice, account_number, timeInForce, extendedHours, jsonify)


def order_sell_trailing_stop(symbol: str, quantity: float, trailAmount: float, trailType: str = 'percentage',
                            timeInForce: str = 'gtc', extendedHours: bool = False, jsonify: bool = True) -> Dict[str, Any]:
    """
    Submits a trailing stop order to sell a stock.

    Args:
        symbol: The stock ticker of the stock to sell.
        quantity: The number of stocks to sell.
        trailAmount: The trailing amount of the stop price. If trailType is 'percentage', this is a percentage. If trailType is 'price', this is a dollar amount.
        trailType: Either 'percentage' or 'price'.
        timeInForce: 'gtc' = good until cancelled, 'gfd' = good for the day, 'ioc' = immediate or cancel, 'opg' = execute at opening.
        extendedHours: Whether to allow trading during extended hours.
        jsonify: If set to False, function will return the request object which contains status code and headers.

    Returns:
        Dictionary containing information regarding the selling of stocks, such as the order id, the state of order (queued, confirmed, filled, failed, canceled, etc.).
    """
    return r.orders.order_sell_trailing_stop(symbol, quantity, trailAmount, trailType, timeInForce, extendedHours, jsonify)


# Order Placement Functions - Fractional Shares
def order_buy_fractional_by_quantity(symbol: str, quantity: float, account_number: Optional[str] = None, timeInForce: str = 'gfd',
                                    extendedHours: bool = False, jsonify: bool = True) -> Dict[str, Any]:
    """
    Submits a market order to buy a fractional quantity of shares.

    Args:
        symbol: The stock ticker of the stock to purchase.
        quantity: The number of shares to buy as a decimal.
        account_number: The account number to place the order for.
        timeInForce: 'gtc' = good until cancelled, 'gfd' = good for the day, 'ioc' = immediate or cancel, 'opg' = execute at opening.
        extendedHours: Whether to allow trading during extended hours.
        jsonify: If set to False, function will return the request object which contains status code and headers.

    Returns:
        Dictionary containing information regarding the purchase of stocks, such as the order id, the state of order (queued, confirmed, filled, failed, canceled, etc.).
    """
    return r.orders.order_buy_fractional_by_quantity(symbol, quantity, account_number, timeInForce, extendedHours, jsonify)


def order_buy_fractional_by_price(symbol: str, amountInDollars: float, account_number: Optional[str] = None, timeInForce: str = 'gfd',
                                 extendedHours: bool = False, jsonify: bool = True, market_hours: str = 'regular_hours') -> Dict[str, Any]:
    """
    Submits a market order to buy a certain dollar value worth of shares.

    Args:
        symbol: The stock ticker of the stock to purchase.
        amountInDollars: The amount in dollars that you want to purchase.
        account_number: The account number to place the order for.
        timeInForce: 'gtc' = good until cancelled, 'gfd' = good for the day, 'ioc' = immediate or cancel, 'opg' = execute at opening.
        extendedHours: Whether to allow trading during extended hours.
        jsonify: If set to False, function will return the request object which contains status code and headers.
        market_hours: The market hours for the order.

    Returns:
        Dictionary containing information regarding the purchase of stocks, such as the order id, the state of order (queued, confirmed, filled, failed, canceled, etc.).
    """
    return r.orders.order_buy_fractional_by_price(symbol, amountInDollars, account_number, timeInForce, extendedHours, jsonify, market_hours)


def order_sell_fractional_by_quantity(symbol: str, quantity: float, account_number: Optional[str] = None, timeInForce: str = 'gfd',
                                     priceType: str = 'bid_price', extendedHours: bool = False, jsonify: bool = True, market_hours: str = 'regular_hours') -> Dict[str, Any]:
    """
    Submits a market order to sell a fractional quantity of shares.

    Args:
        symbol: The stock ticker of the stock to sell.
        quantity: The number of shares to sell as a decimal.
        account_number: The account number to place the order for.
        timeInForce: 'gtc' = good until cancelled, 'gfd' = good for the day, 'ioc' = immediate or cancel, 'opg' = execute at opening.
        priceType: The price type for the order.
        extendedHours: Whether to allow trading during extended hours.
        jsonify: If set to False, function will return the request object which contains status code and headers.
        market_hours: The market hours for the order.

    Returns:
        Dictionary containing information regarding the selling of stocks, such as the order id, the state of order (queued, confirmed, filled, failed, canceled, etc.).
    """
    return r.orders.order_sell_fractional_by_quantity(symbol, quantity, account_number, timeInForce, priceType, extendedHours, jsonify, market_hours)


def order_sell_fractional_by_price(symbol: str, amountInDollars: float, account_number: Optional[str] = None, timeInForce: str = 'gfd',
                                  extendedHours: bool = False, jsonify: bool = True) -> Dict[str, Any]:
    """
    Submits a market order to sell a certain dollar value worth of shares.

    Args:
        symbol: The stock ticker of the stock to sell.
        amountInDollars: The amount in dollars that you want to sell.
        account_number: The account number to place the order for.
        timeInForce: 'gtc' = good until cancelled, 'gfd' = good for the day, 'ioc' = immediate or cancel, 'opg' = execute at opening.
        extendedHours: Whether to allow trading during extended hours.
        jsonify: If set to False, function will return the request object which contains status code and headers.

    Returns:
        Dictionary containing information regarding the selling of stocks, such as the order id, the state of order (queued, confirmed, filled, failed, canceled, etc.).
    """
    return r.orders.order_sell_fractional_by_price(symbol, amountInDollars, account_number, timeInForce, extendedHours, jsonify)


# Order Placement Functions - Crypto
def order_buy_crypto_by_quantity(symbol: str, quantity: float, timeInForce: str = 'gtc',
                                jsonify: bool = True) -> Dict[str, Any]:
    """
    Submits a market order to buy a certain quantity of crypto.

    Args:
        symbol: The crypto ticker of the crypto to purchase.
        quantity: The amount of crypto to buy.
        timeInForce: 'gtc' = good until cancelled, 'gfd' = good for the day, 'ioc' = immediate or cancel, 'opg' = execute at opening.
        jsonify: If set to False, function will return the request object which contains status code and headers.

    Returns:
        Dictionary containing information regarding the purchase of crypto, such as the order id, the state of order (queued, confirmed, filled, failed, canceled, etc.).
    """
    return r.orders.order_buy_crypto_by_quantity(symbol, quantity, timeInForce, jsonify)


def order_buy_crypto_by_price(symbol: str, amountInDollars: float, timeInForce: str = 'gtc',
                             jsonify: bool = True) -> Dict[str, Any]:
    """
    Submits a market order to buy a certain amount of crypto in dollars.

    Args:
        symbol: The crypto ticker of the crypto to purchase.
        amountInDollars: The amount in dollars that you want to purchase.
        timeInForce: 'gtc' = good until cancelled, 'gfd' = good for the day, 'ioc' = immediate or cancel, 'opg' = execute at opening.
        jsonify: If set to False, function will return the request object which contains status code and headers.

    Returns:
        Dictionary containing information regarding the purchase of crypto, such as the order id, the state of order (queued, confirmed, filled, failed, canceled, etc.).
    """
    return r.orders.order_buy_crypto_by_price(symbol, amountInDollars, timeInForce, jsonify)


def order_buy_crypto_limit(symbol: str, quantity: float, limitPrice: float, timeInForce: str = 'gtc',
                          jsonify: bool = True) -> Dict[str, Any]:
    """
    Submits a limit order to buy a certain quantity of crypto.

    Args:
        symbol: The crypto ticker of the crypto to purchase.
        quantity: The amount of crypto to buy.
        limitPrice: The maximum price you're willing to pay per unit of crypto.
        timeInForce: 'gtc' = good until cancelled, 'gfd' = good for the day, 'ioc' = immediate or cancel, 'opg' = execute at opening.
        jsonify: If set to False, function will return the request object which contains status code and headers.

    Returns:
        Dictionary containing information regarding the purchase of crypto, such as the order id, the state of order (queued, confirmed, filled, failed, canceled, etc.).
    """
    return r.orders.order_buy_crypto_limit(symbol, quantity, limitPrice, timeInForce, jsonify)


def order_buy_crypto_limit_by_price(symbol: str, amountInDollars: float, limitPrice: float, timeInForce: str = 'gtc',
                                   jsonify: bool = True) -> Dict[str, Any]:
    """
    Submits a limit order to buy a certain amount of crypto in dollars.

    Args:
        symbol: The crypto ticker of the crypto to purchase.
        amountInDollars: The amount in dollars that you want to purchase.
        limitPrice: The maximum price you're willing to pay per unit of crypto.
        timeInForce: 'gtc' = good until cancelled, 'gfd' = good for the day, 'ioc' = immediate or cancel, 'opg' = execute at opening.
        jsonify: If set to False, function will return the request object which contains status code and headers.

    Returns:
        Dictionary containing information regarding the purchase of crypto, such as the order id, the state of order (queued, confirmed, filled, failed, canceled, etc.).
    """
    return r.orders.order_buy_crypto_limit_by_price(symbol, amountInDollars, limitPrice, timeInForce, jsonify)


def order_sell_crypto_by_quantity(symbol: str, quantity: float, timeInForce: str = 'gtc',
                                 jsonify: bool = True) -> Dict[str, Any]:
    """
    Submits a market order to sell a certain quantity of crypto.

    Args:
        symbol: The crypto ticker of the crypto to sell.
        quantity: The amount of crypto to sell.
        timeInForce: 'gtc' = good until cancelled, 'gfd' = good for the day, 'ioc' = immediate or cancel, 'opg' = execute at opening.
        jsonify: If set to False, function will return the request object which contains status code and headers.

    Returns:
        Dictionary containing information regarding the selling of crypto, such as the order id, the state of order (queued, confirmed, filled, failed, canceled, etc.).
    """
    return r.orders.order_sell_crypto_by_quantity(symbol, quantity, timeInForce, jsonify)


def order_sell_crypto_by_price(symbol: str, amountInDollars: float, timeInForce: str = 'gtc',
                              jsonify: bool = True) -> Dict[str, Any]:
    """
    Submits a market order to sell a certain amount of crypto in dollars.

    Args:
        symbol: The crypto ticker of the crypto to sell.
        amountInDollars: The amount in dollars that you want to sell.
        timeInForce: 'gtc' = good until cancelled, 'gfd' = good for the day, 'ioc' = immediate or cancel, 'opg' = execute at opening.
        jsonify: If set to False, function will return the request object which contains status code and headers.

    Returns:
        Dictionary containing information regarding the selling of crypto, such as the order id, the state of order (queued, confirmed, filled, failed, canceled, etc.).
    """
    return r.orders.order_sell_crypto_by_price(symbol, amountInDollars, timeInForce, jsonify)


def order_sell_crypto_limit(symbol: str, quantity: float, limitPrice: float, timeInForce: str = 'gtc',
                           jsonify: bool = True) -> Dict[str, Any]:
    """
    Submits a limit order to sell a certain quantity of crypto.

    Args:
        symbol: The crypto ticker of the crypto to sell.
        quantity: The amount of crypto to sell.
        limitPrice: The minimum price you're willing to sell per unit of crypto.
        timeInForce: 'gtc' = good until cancelled, 'gfd' = good for the day, 'ioc' = immediate or cancel, 'opg' = execute at opening.
        jsonify: If set to False, function will return the request object which contains status code and headers.

    Returns:
        Dictionary containing information regarding the selling of crypto, such as the order id, the state of order (queued, confirmed, filled, failed, canceled, etc.).
    """
    return r.orders.order_sell_crypto_limit(symbol, quantity, limitPrice, timeInForce, jsonify)


def order_sell_crypto_limit_by_price(symbol: str, amountInDollars: float, limitPrice: float, timeInForce: str = 'gtc',
                                    jsonify: bool = True) -> Dict[str, Any]:
    """
    Submits a limit order to sell a certain amount of crypto in dollars.

    Args:
        symbol: The crypto ticker of the crypto to sell.
        amountInDollars: The amount in dollars that you want to sell.
        limitPrice: The minimum price you're willing to sell per unit of crypto.
        timeInForce: 'gtc' = good until cancelled, 'gfd' = good for the day, 'ioc' = immediate or cancel, 'opg' = execute at opening.
        jsonify: If set to False, function will return the request object which contains status code and headers.

    Returns:
        Dictionary containing information regarding the selling of crypto, such as the order id, the state of order (queued, confirmed, filled, failed, canceled, etc.).
    """
    return r.orders.order_sell_crypto_limit_by_price(symbol, amountInDollars, limitPrice, timeInForce, jsonify)


# Order Placement Functions - Options
def order_buy_option_limit(positionEffect: str, creditOrDebit: str, price: float, symbol: str, quantity: int,
                          expirationDate: str, strike: float, optionType: str = 'both', account_number: Optional[str] = None,
                          timeInForce: str = 'gtc', jsonify: bool = True) -> Dict[str, Any]:
    """
    Submits a limit order to buy or sell an option.

    Args:
        positionEffect: Either 'open' for a buy to open effect or 'close' for a buy to close effect.
        creditOrDebit: Either 'debit' or 'credit'.
        price: The limit price to trigger a buy of the option.
        symbol: The stock ticker of the underlying asset.
        quantity: The number of options to buy.
        expirationDate: The expiration date of the option in 'YYYY-MM-DD' format.
        strike: The strike price of the option.
        optionType: Either 'call' or 'put'.
        timeInForce: 'gtc' = good until cancelled, 'gfd' = good for the day, 'ioc' = immediate or cancel, 'opg' = execute at opening.
        jsonify: If set to False, function will return the request object which contains status code and headers.
        account_number: The account number to place the order for.

    Returns:
        Dictionary containing information regarding the purchase of the option, such as the order id, the state of order (queued, confirmed, filled, failed, canceled, etc.).
    """
    return r.orders.order_buy_option_limit(positionEffect, creditOrDebit, price, symbol, quantity,
                                           expirationDate, strike, optionType, account_number, timeInForce, jsonify)


def order_sell_option_limit(positionEffect: str, creditOrDebit: str, price: float, symbol: str, quantity: int,
                           expirationDate: str, strike: float, optionType: str = 'both', account_number: Optional[str] = None,
                           timeInForce: str = 'gtc', jsonify: bool = True) -> Dict[str, Any]:
    """
    Submits a limit order to buy or sell an option.

    Args:
        positionEffect: Either 'open' for a sell to open effect or 'close' for a sell to close effect.
        creditOrDebit: Either 'debit' or 'credit'.
        price: The limit price to trigger a sell of the option.
        symbol: The stock ticker of the underlying asset.
        quantity: The number of options to sell.
        expirationDate: The expiration date of the option in 'YYYY-MM-DD' format.
        strike: The strike price of the option.
        optionType: Either 'call' or 'put'.
        timeInForce: 'gtc' = good until cancelled, 'gfd' = good for the day, 'ioc' = immediate or cancel, 'opg' = execute at opening.
        jsonify: If set to False, function will return the request object which contains status code and headers.
        account_number: The account number to place the order for.

    Returns:
        Dictionary containing information regarding the selling of the option, such as the order id, the state of order (queued, confirmed, filled, failed, canceled, etc.).
    """
    return r.orders.order_sell_option_limit(positionEffect, creditOrDebit, price, symbol, quantity,
                                           expirationDate, strike, optionType, account_number, timeInForce, jsonify)


def order_buy_option_stop_limit(positionEffect: str, creditOrDebit: str, limitPrice: float, stopPrice: float,
                                symbol: str, quantity: int, expirationDate: str, strike: float, optionType: str = 'both',
                                account_number: Optional[str] = None, timeInForce: str = 'gtc', jsonify: bool = True) -> Dict[str, Any]:
    """
    Submits a stop limit order to buy an option.

    Args:
        positionEffect: Either 'open' for a buy to open effect or 'close' for a buy to close effect.
        creditOrDebit: Either 'debit' or 'credit'.
        limitPrice: The limit price to trigger a buy of the option.
        stopPrice: The stop price to trigger a buy of the option.
        symbol: The stock ticker of the underlying asset.
        quantity: The number of options to buy.
        expirationDate: The expiration date of the option in 'YYYY-MM-DD' format.
        strike: The strike price of the option.
        optionType: Either 'call' or 'put'.
        timeInForce: 'gtc' = good until cancelled, 'gfd' = good for the day, 'ioc' = immediate or cancel, 'opg' = execute at opening.
        jsonify: If set to False, function will return the request object which contains status code and headers.
        account_number: The account number to place the order for.

    Returns:
        Dictionary containing information regarding the purchase of the option, such as the order id, the state of order (queued, confirmed, filled, failed, canceled, etc.).
    """
    return r.orders.order_buy_option_stop_limit(positionEffect, creditOrDebit, limitPrice, stopPrice,
                                               symbol, quantity, expirationDate, strike, optionType,
                                               account_number, timeInForce, jsonify)


def order_sell_option_stop_limit(positionEffect: str, creditOrDebit: str, limitPrice: float, stopPrice: float,
                                 symbol: str, quantity: int, expirationDate: str, strike: float, optionType: str = 'both',
                                 account_number: Optional[str] = None, timeInForce: str = 'gtc', jsonify: bool = True) -> Dict[str, Any]:
    """
    Submits a stop limit order to sell an option.

    Args:
        positionEffect: Either 'open' for a sell to open effect or 'close' for a sell to close effect.
        creditOrDebit: Either 'debit' or 'credit'.
        limitPrice: The limit price to trigger a sell of the option.
        stopPrice: The stop price to trigger a sell of the option.
        symbol: The stock ticker of the underlying asset.
        quantity: The number of options to sell.
        expirationDate: The expiration date of the option in 'YYYY-MM-DD' format.
        strike: The strike price of the option.
        optionType: Either 'call' or 'put'.
        timeInForce: 'gtc' = good until cancelled, 'gfd' = good for the day, 'ioc' = immediate or cancel, 'opg' = execute at opening.
        jsonify: If set to False, function will return the request object which contains status code and headers.
        account_number: The account number to place the order for.

    Returns:
        Dictionary containing information regarding the selling of the option, such as the order id, the state of order (queued, confirmed, filled, failed, canceled, etc.).
    """
    return r.orders.order_sell_option_stop_limit(positionEffect, creditOrDebit, limitPrice, stopPrice,
                                                symbol, quantity, expirationDate, strike, optionType,
                                                account_number, timeInForce, jsonify)


def order_option_spread(direction: str, price: float, symbol: str, quantity: int, spread: dict, 
                       account_number: Optional[str] = None, timeInForce: str = 'gtc', jsonify: bool = True) -> Dict[str, Any]:
    """
    Submits a limit order to open or close a spread position.

    Args:
        direction: Either 'debit' for a buy to open effect or 'credit' for a sell to open effect.
        price: The limit price to trigger the spread order.
        symbol: The stock ticker of the underlying asset.
        quantity: The number of spreads to buy or sell.
        spread: A dictionary of spread options with keys: expirationDate, strike, optionType, effect, action.
        account_number: The account number to place the order for.
        timeInForce: 'gtc' = good until cancelled, 'gfd' = good for the day, 'ioc' = immediate or cancel, 'opg' = execute at opening.
        jsonify: If set to False, function will return the request object which contains status code and headers.

    Returns:
        Dictionary containing information regarding the purchase or sale of the spread, such as the order id, the state of order (queued, confirmed, filled, failed, canceled, etc.).
    """
    return r.orders.order_option_spread(direction, price, symbol, quantity, spread, account_number, timeInForce, jsonify)


def order_option_credit_spread(price: float, symbol: str, quantity: int, spread: dict, 
                              timeInForce: str = 'gtc', account_number: Optional[str] = None, jsonify: bool = True) -> Dict[str, Any]:
    """
    Submits a limit order to open a credit spread position.

    Args:
        price: The limit price to trigger the credit spread order.
        symbol: The stock ticker of the underlying asset.
        quantity: The number of spreads to sell.
        spread: A dictionary of spread options with keys: expirationDate, strike, optionType, effect, action.
        timeInForce: 'gtc' = good until cancelled, 'gfd' = good for the day, 'ioc' = immediate or cancel, 'opg' = execute at opening.
        account_number: The account number to place the order for.
        jsonify: If set to False, function will return the request object which contains status code and headers.

    Returns:
        Dictionary containing information regarding the sale of the credit spread, such as the order id, the state of order (queued, confirmed, filled, failed, canceled, etc.).
    """
    return r.orders.order_option_credit_spread(price, symbol, quantity, spread, timeInForce, account_number, jsonify)


def order_option_debit_spread(price: float, symbol: str, quantity: int, spread: dict, 
                             timeInForce: str = 'gtc', account_number: Optional[str] = None, jsonify: bool = True) -> Dict[str, Any]:
    """
    Submits a limit order to open a debit spread position.

    Args:
        price: The limit price to trigger the debit spread order.
        symbol: The stock ticker of the underlying asset.
        quantity: The number of spreads to buy.
        spread: A dictionary of spread options with keys: expirationDate, strike, optionType, effect, action.
        timeInForce: 'gtc' = good until cancelled, 'gfd' = good for the day, 'ioc' = immediate or cancel, 'opg' = execute at opening.
        account_number: The account number to place the order for.
        jsonify: If set to False, function will return the request object which contains status code and headers.

    Returns:
        Dictionary containing information regarding the purchase of the debit spread, such as the order id, the state of order (queued, confirmed, filled, failed, canceled, etc.).
    """
    return r.orders.order_option_debit_spread(price, symbol, quantity, spread, timeInForce, account_number, jsonify)


# Generic Order Functions
def order(symbol: str, quantity: float, side: str, limitPrice: Optional[float] = None,
         stopPrice: Optional[float] = None, account_number: Optional[str] = None, timeInForce: str = 'gtc', 
         extendedHours: bool = False, jsonify: bool = True, market_hours: str = 'regular_hours') -> Dict[str, Any]:
    """
    Submits a generic order for stocks.

    Args:
        symbol: The stock ticker of the stock to trade.
        quantity: The number of stocks to trade.
        side: Either 'buy' or 'sell'.
        limitPrice: The limit price to trigger a trade of the stock.
        stopPrice: The stop price to trigger a trade of the stock.
        account_number: The account number to place the order for.
        timeInForce: 'gtc' = good until cancelled, 'gfd' = good for the day, 'ioc' = immediate or cancel, 'opg' = execute at opening.
        extendedHours: Whether to allow trading during extended hours.
        jsonify: If set to False, function will return the request object which contains status code and headers.
        market_hours: 'regular_hours' for regular trading hours, 'extended_hours' for extended hours.

    Returns:
        Dictionary containing information regarding the trade of stocks, such as the order id, the state of order (queued, confirmed, filled, failed, canceled, etc.).
    """
    return r.orders.order(symbol, quantity, side, limitPrice, stopPrice, account_number, timeInForce, extendedHours, jsonify, market_hours)


def order_crypto(symbol: str, side: str, quantityOrPrice: float, amountIn: str = "quantity", 
                limitPrice: Optional[float] = None, timeInForce: str = "gtc", jsonify: bool = True) -> Dict[str, Any]:
    """
    Submits a generic order for crypto.

    Args:
        symbol: The crypto ticker of the crypto to trade.
        side: Either 'buy' or 'sell'.
        quantityOrPrice: The amount of crypto to trade or the amount in dollars to trade.
        amountIn: Either 'quantity' or 'price'.
        limitPrice: The limit price to trigger a trade of the crypto.
        timeInForce: 'gtc' = good until cancelled, 'gfd' = good for the day, 'ioc' = immediate or cancel, 'opg' = execute at opening.
        jsonify: If set to False, function will return the request object which contains status code and headers.

    Returns:
        Dictionary containing information regarding the trade of crypto, such as the order id, the state of order (queued, confirmed, filled, failed, canceled, etc.).
    """
    return r.orders.order_crypto(symbol, side, quantityOrPrice, amountIn, limitPrice, timeInForce, jsonify)


def order_trailing_stop(symbol: str, quantity: float, side: str, trailAmount: float,
                       trailType: str = 'percentage', account_number: Optional[str] = None, timeInForce: str = 'gtc', 
                       extendedHours: bool = False, jsonify: bool = True) -> Dict[str, Any]:
    """
    Submits a generic trailing stop order for stocks.

    Args:
        symbol: The stock ticker of the stock to trade.
        quantity: The number of stocks to trade.
        side: Either 'buy' or 'sell'.
        trailAmount: The trailing amount of the stop price. If trailType is 'percentage', this is a percentage. If trailType is 'price', this is a dollar amount.
        trailType: Either 'percentage' or 'price'.
        account_number: The account number to place the order for.
        timeInForce: 'gtc' = good until cancelled, 'gfd' = good for the day, 'ioc' = immediate or cancel, 'opg' = execute at opening.
        extendedHours: Whether to allow trading during extended hours.
        jsonify: If set to False, function will return the request object which contains status code and headers.

    Returns:
        Dictionary containing information regarding the trade of stocks, such as the order id, the state of order (queued, confirmed, filled, failed, canceled, etc.).
    """
    return r.orders.order_trailing_stop(symbol, quantity, side, trailAmount, trailType, account_number, timeInForce, extendedHours, jsonify)


# Sub-agents for Cancellation Functions
cancel_all_crypto_orders_agent = Agent(
    disallow_transfer_to_peers = True,
    disallow_transfer_to_parent = True,
    name="cancel_all_crypto_orders_agent",
    description="Cancels all open crypto orders",
    instruction="You are a specialized agent for canceling all open cryptocurrency orders. Use load_phoenix_account to get account information and use it as account_number.",
    tools=[load_phoenix_account, cancel_all_crypto_orders]
)

cancel_all_option_orders_agent = Agent(
    disallow_transfer_to_peers = True,
    disallow_transfer_to_parent = True,
    name="cancel_all_option_orders_agent",
    description="Cancels all open option orders",
    instruction="You are a specialized agent for canceling all open option orders. Use load_phoenix_account to get account information and use the account_number from the response when calling cancel_all_option_orders.",
    tools=[load_phoenix_account, cancel_all_option_orders]
)

cancel_all_stock_orders_agent = Agent(
    disallow_transfer_to_peers = True,
    disallow_transfer_to_parent = True,
    name="cancel_all_stock_orders_agent",
    description="Cancels all open stock orders",
    instruction="You are a specialized agent for canceling all open stock orders. Use load_phoenix_account to get account information and use the account_number from the response when calling cancel_all_stock_orders.",
    tools=[load_phoenix_account, cancel_all_stock_orders]
)

cancel_crypto_order_agent = Agent(
    disallow_transfer_to_peers = True,
    disallow_transfer_to_parent = True,
    name="cancel_crypto_order_agent",
    description="Cancels a specific crypto order by order ID",
    instruction="You are a specialized agent for canceling specific cryptocurrency orders. Use load_phoenix_account to get account information.",
    tools=[load_phoenix_account, cancel_crypto_order]
)

cancel_option_order_agent = Agent(
    disallow_transfer_to_peers = True,
    disallow_transfer_to_parent = True,
    name="cancel_option_order_agent",
    description="Cancels a specific option order by order ID",
    instruction="You are a specialized agent for canceling specific option orders. Use load_phoenix_account to get account information and use the account_number from the response when calling cancel_option_order.",
    tools=[load_phoenix_account, cancel_option_order]
)

cancel_stock_order_agent = Agent(
    disallow_transfer_to_peers = True,
    disallow_transfer_to_parent = True,
    name="cancel_stock_order_agent",
    description="Cancels a specific stock order by order ID",
    instruction="You are a specialized agent for canceling specific stock orders. Use load_phoenix_account to get account information and use the account_number from the response when calling cancel_stock_order.",
    tools=[load_phoenix_account, cancel_stock_order]
)

# Sub-agents for Order Information Functions
find_stock_orders_agent = Agent(
    disallow_transfer_to_peers = True,
    disallow_transfer_to_parent = True,
    name="find_stock_orders_agent",
    description="Finds stock orders based on the specified parameters",
    instruction="You are a specialized agent for finding stock orders. Use load_phoenix_account to get account information and use the account_number from the response when calling find_stock_orders.",
    tools=[load_phoenix_account, find_stock_orders]
)

get_all_crypto_orders_agent = Agent(
    disallow_transfer_to_peers = True,
    disallow_transfer_to_parent = True,
    name="get_all_crypto_orders_agent",
    description="Gets all crypto orders",
    instruction="You are a specialized agent for retrieving all cryptocurrency orders. Call get_all_crypto_orders function.",
    tools=[load_phoenix_account, get_all_crypto_orders]
)

get_all_open_crypto_orders_agent = Agent(
    disallow_transfer_to_peers = True,
    disallow_transfer_to_parent = True,
    name="get_all_open_crypto_orders_agent",
    description="Gets all open crypto orders",
    instruction="You are a specialized agent for retrieving all open cryptocurrency orders. Call get_all_open_crypto_orders function.",
    tools=[load_phoenix_account, get_all_open_crypto_orders]
)

get_all_option_orders_agent = Agent(
    disallow_transfer_to_peers = True,
    disallow_transfer_to_parent = True,
    name="get_all_option_orders_agent",
    description="Gets all option orders",
    instruction="You are a specialized agent for retrieving all option orders. Use load_phoenix_account to get account information and use the account_number from the response when calling get_all_option_orders.",
    tools=[load_phoenix_account, get_all_option_orders]
)

get_all_open_option_orders_agent = Agent(
    disallow_transfer_to_peers = True,
    disallow_transfer_to_parent = True,
    name="get_all_open_option_orders_agent",
    description="Gets all open option orders",
    instruction="You are a specialized agent for retrieving all open option orders. Use load_phoenix_account to get account information and use the account_number from the response when calling get_all_open_option_orders.",
    tools=[load_phoenix_account, get_all_open_option_orders]
)

get_all_stock_orders_agent = Agent(
    disallow_transfer_to_peers = True,
    disallow_transfer_to_parent = True,
    name="get_all_stock_orders_agent",
    description="Gets all stock orders",
    instruction="You are a specialized agent for retrieving all stock orders. Use load_phoenix_account to get account information and use the account_number from the response when calling get_all_stock_orders.",
    tools=[load_phoenix_account, get_all_stock_orders]
)

get_all_open_stock_orders_agent = Agent(
    disallow_transfer_to_peers = True,
    disallow_transfer_to_parent = True,
    name="get_all_open_stock_orders_agent",
    description="Gets all open stock orders",
    instruction="You are a specialized agent for retrieving all open stock orders. Use load_phoenix_account to get account information and use the account_number from the response when calling get_all_open_stock_orders.",
    tools=[load_phoenix_account, get_all_open_stock_orders]
)

get_crypto_order_info_agent = Agent(
    disallow_transfer_to_peers = True,
    disallow_transfer_to_parent = True,
    name="get_crypto_order_info_agent",
    description="Gets information about a specific crypto order by order ID",
    instruction="You are a specialized agent for retrieving specific cryptocurrency order information. Use load_phoenix_account to get account information and then call get_crypto_order_info.",
    tools=[load_phoenix_account, get_crypto_order_info]
)

get_option_order_info_agent = Agent(
    disallow_transfer_to_peers = True,
    disallow_transfer_to_parent = True,
    name="get_option_order_info_agent",
    description="Gets information about a specific option order by order ID",
    instruction="You are a specialized agent for retrieving specific option order information. Use load_phoenix_account to get account information and then call get_option_order_info.",
    tools=[load_phoenix_account, get_option_order_info]
)

get_stock_order_info_agent = Agent(
    disallow_transfer_to_peers = True,
    disallow_transfer_to_parent = True,
    name="get_stock_order_info_agent",
    description="Gets information about a specific stock order by order ID",
    instruction="You are a specialized agent for retrieving specific stock order information. Use load_phoenix_account to get account information, and then call get_stock_order_info",
    tools=[load_phoenix_account, get_stock_order_info]
)

# Sub-agents for Stock Order Placement Functions
order_buy_limit_agent = Agent(
    disallow_transfer_to_peers = True,
    disallow_transfer_to_parent = True,
    name="order_buy_limit_agent",
    description="Places a limit buy order for stocks",
    instruction="You are a specialized agent for placing limit buy orders for stocks. Use load_phoenix_account to get account information, and use the account_number from load_phoenix_account when calling order_buy_limit function. Ensure the user provides: symbol (stock ticker), quantity (number of shares), and limitPrice (maximum price per share). Optional parameters include timeInForce (default 'gtc'), extendedHours (default False), and jsonify (default True).",

    tools=[load_phoenix_account, order_buy_limit]
)

order_buy_market_agent = Agent(
    disallow_transfer_to_peers = True,
    disallow_transfer_to_parent = True,
    name="order_buy_market_agent",
    description="Places a market buy order for stocks",
    instruction="You are a specialized agent for placing market buy orders for stocks. Use load_phoenix_account tool to get account information, and use the account_number from load_phoenix_account when calling order_buy_market function. Ensure the user provides: symbol (stock ticker) and quantity (number of shares). Optional parameters include timeInForce (default 'gtc'), extendedHours (default False), and jsonify (default True).",
    tools=[load_phoenix_account, order_buy_market],
)

order_buy_stop_limit_agent = Agent(
    disallow_transfer_to_peers = True,
    disallow_transfer_to_parent = True,
    name="order_buy_stop_limit_agent",
    description="Places a stop limit buy order for stocks",
    instruction="You are a specialized agent for placing stop limit buy orders for stocks. Use load_phoenix_account to get account information, and use the account_number from load_phoenix_account when calling order_buy_stop_limit function. Ensure the user provides: symbol (stock ticker), quantity (number of shares), stopPrice (trigger price), and limitPrice (maximum price per share). Optional parameters include timeInForce (default 'gtc'), extendedHours (default False), and jsonify (default True).",
    tools=[load_phoenix_account, order_buy_stop_limit]
)

order_buy_stop_loss_agent = Agent(
    disallow_transfer_to_peers = True,
    disallow_transfer_to_parent = True,
    name="order_buy_stop_loss_agent",
    description="Places a stop loss buy order for stocks",
    instruction="You are a specialized agent for placing stop loss buy orders for stocks. Use load_phoenix_account to get account information, and use the account_number from load_phoenix_account when calling order_buy_stop_loss. Ensure the user provides: symbol (stock ticker), quantity (number of shares), and stopPrice (trigger price for market order). Optional parameters include timeInForce (default 'gtc'), extendedHours (default False), and jsonify (default True).",
    tools=[load_phoenix_account, order_buy_stop_loss]
)

order_buy_trailing_stop_agent = Agent(
    disallow_transfer_to_peers = True,
    disallow_transfer_to_parent = True,
    name="order_buy_trailing_stop_agent",
    description="Places a trailing stop buy order for stocks",
    instruction="You are a specialized agent for placing trailing stop buy orders for stocks. Use load_phoenix_account to get account information, and use the account_number from load_phoenix_account when calling order_buy_trailing_stop. Ensure the user provides: symbol (stock ticker), quantity (number of shares), trailAmount (trailing amount), and optionally trailType ('percentage' or 'price', default 'percentage'). Optional parameters include timeInForce (default 'gtc'), extendedHours (default False), and jsonify (default True).",
    tools=[load_phoenix_account, order_buy_trailing_stop]
)

order_sell_limit_agent = Agent(
    disallow_transfer_to_peers = True,
    disallow_transfer_to_parent = True,
    name="order_sell_limit_agent",
    description="Places a limit sell order for stocks",
    instruction="You are a specialized agent for placing limit sell orders for stocks. Use load_phoenix_account to get account information, and use the account_number from load_phoenix_account when calling order_sell_limit_price. Ensure the user provides: symbol (stock ticker), quantity (number of shares), and limitPrice (minimum price per share). Optional parameters include timeInForce (default 'gtc'), extendedHours (default False), and jsonify (default True).",
    tools=[load_phoenix_account, order_sell_limit_price]
)

order_sell_market_agent = Agent(
    disallow_transfer_to_peers = True,
    disallow_transfer_to_parent = True,
    name="order_sell_market_agent",
    description="Places a market sell order for stocks",
    instruction="You are a specialized agent for placing market sell orders for stocks. Use load_phoenix_account to get account information, and use the account_number from load_phoenix_account when calling order_sell_stock_market. Ensure the user provides: symbol (stock ticker) and quantity (number of shares). Optional parameters include timeInForce (default 'gtc'), extendedHours (default False), and jsonify (default True).",
    tools=[load_phoenix_account, order_sell_stock_market]
)

order_sell_stop_limit_agent = Agent(
    disallow_transfer_to_peers = True,
    disallow_transfer_to_parent = True,
    name="order_sell_stop_limit_agent",
    description="Places a stop limit sell order for stocks",
    instruction="You are a specialized agent for placing stop limit sell orders for stocks. Use load_phoenix_account to get account information, and use the account_number from load_phoenix_account when calling order_sell_stop_limit. Ensure the user provides: symbol (stock ticker), quantity (number of shares), stopPrice (trigger price), and limitPrice (minimum price per share). Optional parameters include timeInForce (default 'gtc'), extendedHours (default False), and jsonify (default True).",
    tools=[load_phoenix_account, order_sell_stop_limit]
)

order_sell_stop_loss_agent = Agent(
    disallow_transfer_to_peers = True,
    disallow_transfer_to_parent = True,
    name="order_sell_stop_loss_agent",
    description="Places a stop loss sell order for stocks",
    instruction="You are a specialized agent for placing stop loss sell orders for stocks. Use load_phoenix_account to get account information, and use the account_number from load_phoenix_account when calling order_sell_stop_loss. Ensure the user provides: symbol (stock ticker), quantity (number of shares), and stopPrice (trigger price for market order). Optional parameters include timeInForce (default 'gtc'), extendedHours (default False), and jsonify (default True).",
    tools=[load_phoenix_account, order_sell_stop_loss]
)

order_sell_trailing_stop_agent = Agent(
    disallow_transfer_to_peers = True,
    disallow_transfer_to_parent = True,
    name="order_sell_trailing_stop_agent",
    description="Places a trailing stop sell order for stocks",
    instruction="You are a specialized agent for placing trailing stop sell orders for stocks. Use load_phoenix_account to get account information, and use the account_number from load_phoenix_account when calling order_sell_trailing_stop. Ensure the user provides: symbol (stock ticker), quantity (number of shares), trailAmount (trailing amount), and optionally trailType ('percentage' or 'price', default 'percentage'). Optional parameters include timeInForce (default 'gtc'), extendedHours (default False), and jsonify (default True).",
    tools=[load_phoenix_account, order_sell_trailing_stop]
)

# Sub-agents for Fractional Share Order Functions
order_buy_fractional_by_quantity_agent = Agent(
    disallow_transfer_to_peers = True,
    disallow_transfer_to_parent = True,
    name="order_buy_fractional_by_quantity_agent",
    description="Places a fractional buy order for stocks by quantity",
    instruction="You are a specialized agent for placing fractional buy orders by share quantity for stocks. Use load_phoenix_account to get account information, and use the account_number from load_phoenix_account when calling order_buy_fractional_by_quantity. Ensure the user provides: symbol (stock ticker) and quantity (fractional number of shares). Optional parameters include timeInForce (default 'gtc'), extendedHours (default False), and jsonify (default True).",
    tools=[load_phoenix_account, order_buy_fractional_by_quantity]
)

order_buy_fractional_by_price_agent = Agent(
    disallow_transfer_to_peers = True,
    disallow_transfer_to_parent = True,
    name="order_buy_fractional_by_price_agent",
    description="Places a fractional buy order for stocks by price",
    instruction="You are a specialized agent for placing fractional buy orders by dollar amount for stocks. Use load_phoenix_account to get account information, and use the account_number from load_phoenix_account when calling order_buy_fractional_by_price. Ensure the user provides: symbol (stock ticker) and amountInDollars (dollar amount to invest). Optional parameters include timeInForce (default 'gtc'), extendedHours (default False), and jsonify (default True).",
    tools=[load_phoenix_account, order_buy_fractional_by_price]
)

order_sell_fractional_by_quantity_agent = Agent(
    disallow_transfer_to_peers = True,
    disallow_transfer_to_parent = True,
    name="order_sell_fractional_by_quantity_agent",
    description="Places a fractional sell order for stocks by quantity",
    instruction="You are a specialized agent for placing fractional sell orders by share quantity for stocks. Use load_phoenix_account to get account information, and use the account_number from load_phoenix_account when calling order_sell_fractional_by_quantity. Ensure the user provides: symbol (stock ticker) and quantity (fractional number of shares). Optional parameters include timeInForce (default 'gtc'), extendedHours (default False), and jsonify (default True).",
    tools=[load_phoenix_account, order_sell_fractional_by_quantity]
)

order_sell_fractional_by_price_agent = Agent(
    disallow_transfer_to_peers = True,
    disallow_transfer_to_parent = True,
    name="order_sell_fractional_by_price_agent",
    description="Places a fractional sell order for stocks by price",
    instruction="You are a specialized agent for placing fractional sell orders by dollar amount for stocks. Use load_phoenix_account to get account information, and use the account_number from load_phoenix_account when calling order_sell_fractional_by_price. Ensure the user provides: symbol (stock ticker) and amountInDollars (dollar amount to sell). Optional parameters include timeInForce (default 'gtc'), extendedHours (default False), and jsonify (default True).",
    tools=[load_phoenix_account, order_sell_fractional_by_price]
)

# Sub-agents for Crypto Order Functions
order_buy_crypto_by_price_agent = Agent(
    disallow_transfer_to_peers = True,
    disallow_transfer_to_parent = True,
    name="order_buy_crypto_by_price_agent",
    description="Places a buy order for crypto by price",
    instruction="You are a specialized agent for placing cryptocurrency buy orders by dollar amount. Use load_phoenix_account to get account information. Ensure the user provides: symbol (crypto ticker) and amountInDollars (dollar amount to invest). Optional parameters include timeInForce (default 'gtc') and jsonify (default True).",
    tools=[load_phoenix_account, order_buy_crypto_by_price]
)

order_buy_crypto_by_quantity_agent = Agent(
    disallow_transfer_to_peers = True,
    disallow_transfer_to_parent = True,
    name="order_buy_crypto_by_quantity_agent",
    description="Places a buy order for crypto by quantity",
    instruction="You are a specialized agent for placing cryptocurrency buy orders by quantity. Use load_phoenix_account to get account information. Ensure the user provides: symbol (crypto ticker) and quantity (amount of crypto to buy). Optional parameters include timeInForce (default 'gtc') and jsonify (default True).",
    tools=[load_phoenix_account, order_buy_crypto_by_quantity]
)

order_buy_crypto_limit_agent = Agent(
    disallow_transfer_to_peers = True,
    disallow_transfer_to_parent = True,
    name="order_buy_crypto_limit_agent",
    description="Places a limit buy order for crypto by quantity",
    instruction="You are a specialized agent for placing cryptocurrency limit buy orders by quantity. Use load_phoenix_account to get account information. Ensure the user provides: symbol (crypto ticker), quantity (amount of crypto to buy), and limitPrice (maximum price per unit). Optional parameters include timeInForce (default 'gtc') and jsonify (default True).",
    tools=[load_phoenix_account, order_buy_crypto_limit]
)

order_buy_crypto_limit_by_price_agent = Agent(
    disallow_transfer_to_peers = True,
    disallow_transfer_to_parent = True,
    name="order_buy_crypto_limit_by_price_agent",
    description="Places a limit buy order for crypto by price",
    instruction="You are a specialized agent for placing cryptocurrency limit buy orders by dollar amount. Use load_phoenix_account to get account information. Ensure the user provides: symbol (crypto ticker), amountInDollars (dollar amount to invest), and limitPrice (maximum price per unit). Optional parameters include timeInForce (default 'gtc') and jsonify (default True).",
    tools=[load_phoenix_account, order_buy_crypto_limit_by_price]
)

order_sell_crypto_by_price_agent = Agent(
    disallow_transfer_to_peers = True,
    disallow_transfer_to_parent = True,
    name="order_sell_crypto_by_price_agent",
    description="Places a sell order for crypto by price",
    instruction="You are a specialized agent for placing cryptocurrency sell orders by dollar amount. Use load_phoenix_account to get account information. Ensure the user provides: symbol (crypto ticker) and amountInDollars (dollar amount to sell). Optional parameters include timeInForce (default 'gtc') and jsonify (default True).",
    tools=[load_phoenix_account, order_sell_crypto_by_price]
)

order_sell_crypto_by_quantity_agent = Agent(
    disallow_transfer_to_peers = True,
    disallow_transfer_to_parent = True,
    name="order_sell_crypto_by_quantity_agent",
    description="Places a sell order for crypto by quantity",
    instruction="You are a specialized agent for placing cryptocurrency sell orders by quantity. Use load_phoenix_account to get account information. Ensure the user provides: symbol (crypto ticker) and quantity (amount of crypto to sell). Optional parameters include timeInForce (default 'gtc') and jsonify (default True).",
    tools=[load_phoenix_account, order_sell_crypto_by_quantity]
)

order_sell_crypto_limit_agent = Agent(
    disallow_transfer_to_peers = True,
    disallow_transfer_to_parent = True,
    name="order_sell_crypto_limit_agent",
    description="Places a limit sell order for crypto by quantity",
    instruction="You are a specialized agent for placing cryptocurrency limit sell orders by quantity. Use load_phoenix_account to get account information. Ensure the user provides: symbol (crypto ticker), quantity (amount of crypto to sell), and limitPrice (minimum price per unit). Optional parameters include timeInForce (default 'gtc') and jsonify (default True).",
    tools=[load_phoenix_account, order_sell_crypto_limit]
)

order_sell_crypto_limit_by_price_agent = Agent(
    disallow_transfer_to_peers = True,
    disallow_transfer_to_parent = True,
    name="order_sell_crypto_limit_by_price_agent",
    description="Places a limit sell order for crypto by price",
    instruction="You are a specialized agent for placing cryptocurrency limit sell orders by dollar amount. Use load_phoenix_account to get account information. Ensure the user provides: symbol (crypto ticker), amountInDollars (dollar amount to sell), and limitPrice (minimum price per unit). Optional parameters include timeInForce (default 'gtc') and jsonify (default True).",
    tools=[load_phoenix_account, order_sell_crypto_limit_by_price]
)

# Sub-agents for Option Order Functions
order_buy_option_limit_agent = Agent(
    disallow_transfer_to_peers = True,
    disallow_transfer_to_parent = True,
    name="order_buy_option_limit_agent",
    description="Places a limit buy order for options",
    instruction="You are a specialized agent for placing options limit buy orders. Use load_phoenix_account to get account information, and use the account_number from load_phoenix_account when calling order_buy_option_limit. Ensure the user provides: positionEffect ('open' or 'close'), creditOrDebit ('debit' for buying), price (limit price), symbol (underlying stock ticker), quantity (number of contracts), expirationDate (YYYY-MM-DD format), strike (strike price), and optionType ('call' or 'put'). Optional parameters include timeInForce (default 'gtc') and jsonify (default True).",
    tools=[load_phoenix_account, order_buy_option_limit]
)

order_buy_option_stop_limit_agent = Agent(
    disallow_transfer_to_peers = True,
    disallow_transfer_to_parent = True,
    name="order_buy_option_stop_limit_agent",
    description="Places a stop limit buy order for options",
    instruction="You are a specialized agent for placing options stop limit buy orders. Use load_phoenix_account to get account information, and use the account_number from load_phoenix_account when calling order_buy_option_stop_limit. Ensure the user provides: positionEffect ('open' or 'close'), creditOrDebit ('debit' for buying), limitPrice (limit price), stopPrice (trigger price), symbol (underlying stock ticker), quantity (number of contracts), expirationDate (YYYY-MM-DD format), strike (strike price), and optionType ('call' or 'put'). Optional parameters include timeInForce (default 'gtc') and jsonify (default True).",
    tools=[load_phoenix_account, order_buy_option_stop_limit]
)

order_sell_option_limit_agent = Agent(
    disallow_transfer_to_peers = True,
    disallow_transfer_to_parent = True,
    name="order_sell_option_limit_agent",
    description="Places a limit sell order for options",
    instruction="You are a specialized agent for placing options limit sell orders. Use load_phoenix_account to get account information, and use the account_number from load_phoenix_account when calling order_sell_option_limit. Ensure the user provides: positionEffect ('open' or 'close'), creditOrDebit ('credit' for selling), price (limit price), symbol (underlying stock ticker), quantity (number of contracts), expirationDate (YYYY-MM-DD format), strike (strike price), and optionType ('call' or 'put'). Optional parameters include timeInForce (default 'gtc') and jsonify (default True).",
    tools=[load_phoenix_account, order_sell_option_limit]
)

order_sell_option_stop_limit_agent = Agent(
    disallow_transfer_to_peers = True,
    disallow_transfer_to_parent = True,
    name="order_sell_option_stop_limit_agent",
    description="Places a stop limit sell order for options",
    instruction="You are a specialized agent for placing options stop limit sell orders. Use load_phoenix_account to get account information, and use the account_number from load_phoenix_account when calling order_sell_option_stop_limit. Ensure the user provides: positionEffect ('open' or 'close'), creditOrDebit ('credit' for selling), limitPrice (limit price), stopPrice (trigger price), symbol (underlying stock ticker), quantity (number of contracts), expirationDate (YYYY-MM-DD format), strike (strike price), and optionType ('call' or 'put'). Optional parameters include timeInForce (default 'gtc') and jsonify (default True).",
    tools=[load_phoenix_account, order_sell_option_stop_limit]
)

order_option_spread_agent = Agent(
    disallow_transfer_to_peers = True,
    disallow_transfer_to_parent = True,
    name="order_option_spread_agent",
    description="Places an option spread order",
    instruction="You are a specialized agent for placing options spread orders. Use load_phoenix_account to get account information, and use the account_number from load_phoenix_account when calling order_option_spread. This is a complex multi-leg options strategy. Ensure the user provides all required parameters for the spread configuration including legs, prices, quantities, and expiration details.",
    tools=[load_phoenix_account, order_option_spread]
)

order_option_credit_spread_agent = Agent(
    disallow_transfer_to_peers = True,
    disallow_transfer_to_parent = True,
    name="order_option_credit_spread_agent",
    description="Places an option credit spread order",
    instruction="You are a specialized agent for placing options credit spread orders. Use load_phoenix_account to get account information, and use the account_number from load_phoenix_account when calling order_option_credit_spread. This strategy involves selling a higher premium option and buying a lower premium option of the same type. Ensure the user provides all required parameters for both legs of the spread.",
    tools=[load_phoenix_account, order_option_credit_spread]
)

order_option_debit_spread_agent = Agent(
    disallow_transfer_to_peers = True,
    disallow_transfer_to_parent = True,
    name="order_option_debit_spread_agent",
    description="Places an option debit spread order",
    instruction="You are a specialized agent for placing options debit spread orders. Use load_phoenix_account to get account information, and use the account_number from load_phoenix_account when calling order_option_debit_spread. This strategy involves buying a higher premium option and selling a lower premium option of the same type. Ensure the user provides all required parameters for both legs of the spread.",
    tools=[load_phoenix_account, order_option_debit_spread]
)

# Sub-agents for Generic Order Functions
order_agent = Agent(
    disallow_transfer_to_peers = True,
    disallow_transfer_to_parent = True,
    name="order_agent",
    description="Places a generic order for stocks",
    instruction="You are a specialized agent for placing generic stock orders. Use load_phoenix_account to get account information, and use the account_number from load_phoenix_account when calling order. This is a flexible order function that can handle various order types. Ensure the user provides: symbol (stock ticker), quantity (number of shares), and side ('buy' or 'sell'). Additional parameters may be required based on order type such as limitPrice, stopPrice, timeInForce, etc.",
    tools=[load_phoenix_account, order]
)

order_crypto_agent = Agent(
    disallow_transfer_to_peers = True,
    disallow_transfer_to_parent = True,
    name="order_crypto_agent",
    description="Places a generic order for crypto",
    instruction="You are a specialized agent for placing generic cryptocurrency orders. Use load_phoenix_account to get account information, and use the account_number from load_phoenix_account when calling order_crypto. This is a flexible order function that can handle various crypto order types. Ensure the user provides: symbol (crypto ticker), quantity (amount of crypto), and side ('buy' or 'sell'). Additional parameters may be required based on order type such as price, timeInForce, etc.",
    tools=[load_phoenix_account, order_crypto]
)

order_trailing_stop_agent = Agent(
    disallow_transfer_to_peers = True,
    disallow_transfer_to_parent = True,
    name="order_trailing_stop_agent",
    description="Places a generic trailing stop order for stocks",
    instruction="You are a specialized agent for placing trailing stop orders for stocks. Use load_phoenix_account to get account information, and use the account_number from load_phoenix_account when calling order_trailing_stop. This is a flexible trailing stop function. Ensure the user provides: symbol (stock ticker), quantity (number of shares), side ('buy' or 'sell'), and trailAmount (trailing amount). Additional parameters may include trailType ('percentage' or 'price'), timeInForce, etc.",
    tools=[load_phoenix_account, order_trailing_stop],
)

# Main Robinhood Orders Agent
robinhood_orders_agent = Agent(
    name="robinhood_orders_agent",
    description="Handles placing and cancelling orders for stocks, options, and crypto on Robinhood",
    instruction=AGENT_INSTRUCTION,
    tools=[confirm_order_details],
    sub_agents=[
        # Cancellation Sub-agents
        cancel_all_crypto_orders_agent,
        cancel_all_option_orders_agent,
        cancel_all_stock_orders_agent,
        cancel_crypto_order_agent,
        cancel_option_order_agent,
        cancel_stock_order_agent,
        
        # Order Information Sub-agents
        find_stock_orders_agent,
        get_all_crypto_orders_agent,
        get_all_open_crypto_orders_agent,
        get_all_option_orders_agent,
        get_all_open_option_orders_agent,
        get_all_stock_orders_agent,
        get_all_open_stock_orders_agent,
        get_crypto_order_info_agent,
        get_option_order_info_agent,
        get_stock_order_info_agent,
        
        # Stock Order Placement Sub-agents
        order_buy_limit_agent,
        order_buy_market_agent,
        order_buy_stop_limit_agent,
        order_buy_stop_loss_agent,
        order_buy_trailing_stop_agent,
        order_sell_limit_agent,
        order_sell_market_agent,
        order_sell_stop_limit_agent,
        order_sell_stop_loss_agent,
        order_sell_trailing_stop_agent,
        
        # Fractional Share Order Sub-agents
        order_buy_fractional_by_quantity_agent,
        order_buy_fractional_by_price_agent,
        order_sell_fractional_by_quantity_agent,
        order_sell_fractional_by_price_agent,
        
        # Crypto Order Sub-agents
        order_buy_crypto_by_price_agent,
        order_buy_crypto_by_quantity_agent,
        order_buy_crypto_limit_agent,
        order_buy_crypto_limit_by_price_agent,
        order_sell_crypto_by_price_agent,
        order_sell_crypto_by_quantity_agent,
        order_sell_crypto_limit_agent,
        order_sell_crypto_limit_by_price_agent,
        
        # Option Order Sub-agents
        order_buy_option_limit_agent,
        order_buy_option_stop_limit_agent,
        order_sell_option_limit_agent,
        order_sell_option_stop_limit_agent,
        order_option_spread_agent,
        order_option_credit_spread_agent,
        order_option_debit_spread_agent,
        
        # Generic Order Sub-agents
        order_agent,
        order_crypto_agent,
        order_trailing_stop_agent
    ]
)