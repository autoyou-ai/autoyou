from robin_stocks.robinhood.stocks import get_stock_quote_by_symbol
from ..shared_libraries.robinhood.types import Ticker, TickerDetails
from typing import Optional

def get_ticker_details(symbol: str) -> Optional[Ticker]:
    try:
        quote = get_stock_quote_by_symbol(symbol)
        if not quote:
            return None

        # Calculate percent change if possible
        last_price = float(quote.get('last_trade_price', 0)) if quote.get('last_trade_price') else 0
        prev_close = float(quote.get('adjusted_previous_close', 0)) if quote.get('adjusted_previous_close') else 0
        percent_change = '0.00'
        if prev_close > 0:
            percent_change = "{:.2f}".format((last_price - prev_close) * 100 / prev_close)

        # Get extended hours price if available
        extended_hours_price = quote.get('last_extended_hours_trade_price')
        equity = extended_hours_price if extended_hours_price else quote.get('last_trade_price', '0.00')
        
        return Ticker(
            symbol=symbol,
            details=TickerDetails(
                price=quote.get('last_trade_price', '0.00'),
                quantity=quote.get('ask_size', '0'),
                average_buy_price=quote.get('adjusted_previous_close', '0.00'),
                equity=equity,
                percent_change=percent_change,
                intraday_percent_change=percent_change,  # Using same percent change as we don't have intraday data
                equity_change=quote.get('last_extended_hours_trade_price', quote.get('last_trade_price', '0.00')),
                type='stock',
                name=quote.get('symbol', symbol),
                id=quote.get('instrument', ''),
                pe_ratio=quote.get('pe_ratio', 'N/A'),
                percentage=quote.get('adjusted_previous_close', '0.00')
            )
        )
    except Exception as e:
        print(f"Error fetching ticker details: {e}")
        return None


def get_multiple_ticker_details(symbols: list[str]) -> list[Optional[Ticker]]:
    """
    Get details for multiple stock tickers.
    
    Args:
        symbols: A list of stock ticker symbols.
        
    Returns:
        A list of Ticker objects with details for each symbol.
    """
    tickers = []
    for symbol in symbols:
        ticker = get_ticker_details(symbol)
        if ticker:
            tickers.append(ticker)
    return tickers