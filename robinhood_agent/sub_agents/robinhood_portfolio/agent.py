"""robinhood_portfolio_agent for fetching details about users portfolio in their robinhood account"""

import os
from dotenv import load_dotenv

from google.adk import Agent
from google.adk.tools import ToolContext

import robin_stocks.robinhood as r

from . import prompt

load_dotenv()

# Profile Functions
def load_account_profile() -> dict:
    """Gets the information associated with the accounts profile, including day
    trading information and cash being held by Robinhood.
    
    Args:
        account_number (Optional[str]): The robinhood account number.
        info (Optional[str]): The name of the key whose value is to be returned from the function.
        dataType (Optional[str]): Determines how to filter the data. 'regular' returns the unfiltered data.
            'results' will return data['results']. 'pagination' will return data['results'] and append it with any
            data that is in data['next']. 'indexzero' will return data['results'][0].
    
    Returns:
        dict: The function returns a dictionary of key/value pairs.
            If a string is passed in to the info parameter, then the function will return
            a string corresponding to the value of the key whose name matches the info parameter.
    
    Dictionary Keys:
        - url, portfolio_cash, can_downgrade_to_cash, user, account_number, type, created_at, updated_at,
        - deactivated, deposit_halted, only_position_closing_trades, buying_power, cash_available_for_withdrawal,
        - cash, cash_held_for_orders, uncleared_deposits, sma, sma_held_for_orders, unsettled_funds,
        - unsettled_debit, crypto_buying_power, max_ach_early_access_amount, cash_balances, margin_balances,
        - sweep_enabled, instant_eligibility, option_level, is_pinnacle_account, rhs_account_number, state,
        - active_subscription_id, locked, permanently_deactivated, received_ach_debit_locked, drip_enabled,
        - eligible_for_fractionals, eligible_for_drip, eligible_for_cash_management, cash_management_enabled,
        - option_trading_on_expiration_enabled, cash_held_for_options_collateral, fractional_position_closing_only,
        - user_id, rhs_stock_loan_consent_status
    """
    return r.load_account_profile()

def load_basic_profile() -> dict:
    """Gets the information associated with the personal profile,
    such as phone number, city, marital status, and date of birth.
    
    Args:
        info (Optional[str]): The name of the key whose value is to be returned from the function.
    
    Returns:
        dict: The function returns a dictionary of key/value pairs. If a string
            is passed in to the info parameter, then the function will return a string
            corresponding to the value of the key whose name matches the info parameter.
    
    Dictionary Keys:
        - user, address, city, state, zipcode, phone_number, marital_status, date_of_birth,
        - citizenship, country_of_residence, number_dependents, signup_as_rhs, tax_id_ssn, updated_at
    """
    return r.load_basic_profile()

def load_investment_profile() -> dict:
    """Gets the information associated with the investment profile.
    These are the answers to the questionnaire you filled out when you made your profile.
    
    Args:
        info (Optional[str]): The name of the key whose value is to be returned from the function.
    
    Returns:
        dict: The function returns a dictionary of key/value pairs.
            If a string is passed in to the info parameter, then the function will return
            a string corresponding to the value of the key whose name matches the info parameter.
    
    Dictionary Keys:
        - user, total_net_worth, annual_income, source_of_funds, investment_objective, investment_experience,
        - liquid_net_worth, risk_tolerance, tax_bracket, time_horizon, liquidity_needs, investment_experience_collected,
        - suitability_verified, option_trading_experience, professional_trader, understand_option_spreads,
        - interested_in_options, updated_at
    """
    return r.load_investment_profile()

def load_portfolio_profile() -> dict:
    """Gets the information associated with the portfolios profile,
    such as withdrawable amount, market value of account, and excess margin.
    
    Args:
        account_number (Optional[str]): The robinhood account number.
        info (Optional[str]): The name of the key whose value is to be returned from the function.
    
    Returns:
        dict: The function returns a dictionary of key/value pairs.
            If a string is passed in to the info parameter, then the function will return
            a string corresponding to the value of the key whose name matches the info parameter.
    
    Dictionary Keys:
        - url, account, start_date, market_value, equity, extended_hours_market_value, extended_hours_equity,
        - extended_hours_portfolio_equity, last_core_market_value, last_core_equity, last_core_portfolio_equity,
        - excess_margin, excess_maintenance, excess_margin_with_uncleared_deposits, excess_maintenance_with_uncleared_deposits,
        - equity_previous_close, portfolio_equity_previous_close, adjusted_equity_previous_close,
        - adjusted_portfolio_equity_previous_close, withdrawable_amount, unwithdrawable_deposits, unwithdrawable_grants
    """
    return r.load_portfolio_profile()

def load_security_profile() -> dict:
    """Gets the information associated with the security profile.
    
    Args:
        info (Optional[str]): The name of the key whose value is to be returned from the function.
    
    Returns:
        dict: The function returns a dictionary of key/value pairs.
            If a string is passed in to the info parameter, then the function will return
            a string corresponding to the value of the key whose name matches the info parameter.
    
    Dictionary Keys:
        - user, object_to_disclosure, sweep_consent, control_person, control_person_security_symbol,
        - security_affiliated_employee, security_affiliated_firm_relationship, security_affiliated_firm_name,
        - security_affiliated_person_name, security_affiliated_address, security_affiliated_address_subject,
        - security_affiliated_requires_duplicates, stock_loan_consent_status, agreed_to_rhs, agreed_to_rhs_margin,
        - rhs_stock_loan_consent_status, updated_at
    """
    return r.load_security_profile()

def load_user_profile() -> dict:
    """Gets the information associated with the user profile,
    such as username, email, and links to the urls for other profiles.
    
    Args:
        info (Optional[str]): The name of the key whose value is to be returned from the function.
    
    Returns:
        dict: The function returns a dictionary of key/value pairs.
            If a string is passed in to the info parameter, then the function will return
            a string corresponding to the value of the key whose name matches the info parameter.
    
    Dictionary Keys:
        - url, id, id_info, username, email, email_verified, first_name, last_name, origin,
        - profile_name, created_at
    """
    return r.load_user_profile()

# Account Functions
def load_phoenix_account() -> dict:
    """Returns unified information about your account."""
    return r.load_phoenix_account()

def get_all_positions() -> list:
    """Returns a list containing every position ever traded.
    
    Args:
        info (Optional[str]): Will filter the results to get a specific value.
    
    Returns:
        list: Returns a list of dictionaries of key/value pairs for each ticker. If info parameter is provided,
            a list of strings is returned where the strings are the value of the key that matches info.
    
    Dictionary Keys:
        - url, instrument, account, account_number, average_buy_price, pending_average_buy_price, quantity,
        - intraday_average_buy_price, intraday_quantity, shares_held_for_buys, shares_held_for_sells,
        - shares_held_for_stock_grants, shares_held_for_options_collateral, shares_held_for_options_events,
        - shares_pending_from_options_events, updated_at, created_at
    """
    return r.get_all_positions()

def get_open_stock_positions() -> list:
    """Returns a list of stocks that are currently held.
    
    Args:
        account_number (Optional[str]): The robinhood account number.
        info (Optional[str]): Will filter the results to get a specific value.
    
    Returns:
        list: Returns a list of dictionaries of key/value pairs for each ticker. If info parameter is provided,
            a list of strings is returned where the strings are the value of the key that matches info.
    
    Dictionary Keys:
        - url, instrument, account, account_number, average_buy_price, pending_average_buy_price, quantity,
        - intraday_average_buy_price, intraday_quantity, shares_held_for_buys, shares_held_for_sells,
        - shares_held_for_stock_grants, shares_held_for_options_collateral, shares_held_for_options_events,
        - shares_pending_from_options_events, updated_at, created_at
    """
    return r.get_open_stock_positions()

def get_dividends() -> list:
    """Returns a list of dividend transactions that include information such as the percentage rate,
    amount, shares of held stock, and date paid.
    
    Args:
        info (Optional[str]): Will filter the results to get a specific value.
    
    Returns:
        list: Returns a list of dictionaries of key/value pairs for each dividend payment. If info parameter is provided,
            a list of strings is returned where the strings are the value of the key that matches info.
    
    Dictionary Keys:
        - id, url, account, instrument, amount, rate, position, withholding, record_date, payable_date,
        - paid_at, state, nra_withholding, drip_enabled
    """
    return r.get_dividends()

def get_total_dividends() -> float:
    """Returns a float number representing the total amount of dividends paid to the account.
    
    Returns:
        float: Total dollar amount of dividends paid to the account as a 2 precision float.
    """
    return r.get_total_dividends()

def get_linked_bank_accounts() -> list:
    """Returns all linked bank accounts.
    
    Args:
        info (Optional[str]): Will filter the results to get a specific value.
    
    Returns:
        list: Returns a list of dictionaries of key/value pairs for each bank.
    """
    return r.get_linked_bank_accounts()

def get_bank_account_info(id: str) -> dict:
    """Returns a single dictionary of bank information.
    
    Args:
        id (str): The bank id.
        info (Optional[str]): Will filter the results to get a specific value.
    
    Returns:
        dict: Returns a dictionary of key/value pairs for the bank. If info parameter is provided,
            the value of the key that matches info is extracted.
    """
    return r.get_bank_account_info(id=id)

def get_bank_transfers() -> list:
    """Returns all bank transfers made for the account."""
    return r.get_bank_transfers()

def get_card_transactions() -> list:
    """Returns all debit card transactions made on the account."""
    return r.get_card_transactions()

def get_day_trades() -> list:
    """Returns recent day trades."""
    return r.get_day_trades()

def get_documents() -> list:
    """Returns a list of documents that have been released by Robinhood to the account."""
    return r.get_documents()

def get_interest_payments() -> list:
    """Returns a list of interest payments."""
    return r.get_interest_payments()

def get_latest_notification() -> dict:
    """Returns the time of the latest notification."""
    return r.get_latest_notification()

def get_margin_calls() -> list:
    """Returns either all margin calls or margin calls for a specific stock."""
    return r.get_margin_calls()

def get_margin_interest() -> list:
    """Returns a list of margin interest."""
    return r.get_margin_interest()

def get_notifications() -> list:
    """Returns a list of notifications."""
    return r.get_notifications()

def get_referrals() -> list:
    """Returns a list of referrals."""
    return r.get_referrals()

def get_stock_loan_payments() -> list:
    """Returns a list of loan payments."""
    return r.get_stock_loan_payments()

def get_subscription_fees() -> list:
    """Returns a list of subscription fees."""
    return r.get_subscription_fees()

def get_all_watchlists() -> list:
    """Returns a list of all watchlists that have been created.
    
    Args:
        info (Optional[str]): Will filter the results to get a specific value.
    
    Returns:
        list: Returns a list of dictionaries of key/value pairs for each watchlist.
    """
    return r.get_all_watchlists()

def get_watchlist_by_name(name: str = "My First List") -> list:
    """Returns a list of information related to the stocks in a single watchlist.
    
    Args:
        name (Optional[str]): The name of the watchlist to get data from. Defaults to "My First List".
        info (Optional[str]): Will filter the results to get a specific value.
    
    Returns:
        list: Returns a list of dictionaries that contain the instrument urls and a url that references itself.
    """
    return r.get_watchlist_by_name(name=name)

def post_symbols_to_watchlist(inputSymbols, name: str = "My First List") -> list:
    """Posts multiple stock tickers to a watchlist.
    
    Args:
        inputSymbols (str or list): May be a single stock ticker or a list of stock tickers.
        name (Optional[str]): The name of the watchlist to post data to. Defaults to "My First List".
    
    Returns:
        list: Returns result of the post request.
    """
    return r.post_symbols_to_watchlist(inputSymbols=inputSymbols, name=name)

def delete_symbols_from_watchlist(inputSymbols, name: str = "My First List") -> list:
    """Deletes multiple stock tickers from a watchlist.
    
    Args:
        inputSymbols (str or list): May be a single stock ticker or a list of stock tickers.
        name (Optional[str]): The name of the watchlist to delete data from. Defaults to "My First List".
    
    Returns:
        list: Returns result of the delete request.
    """
    return r.delete_symbols_from_watchlist(inputSymbols=inputSymbols, name=name)

def get_wire_transfers() -> list:
    """Returns a list of wire transfers.
    
    Args:
        info (Optional[str]): Will filter the results to get a specific value.
    
    Returns:
        list: Returns a list of dictionaries of key/value pairs for each wire transfer. If info parameter is provided,
            a list of strings is returned where the strings are the value of the key that matches info.
    """
    return r.get_wire_transfers()

def build_robinhood_portfolio(with_dividends: bool = False) -> dict:
    """Builds a structured JSON representation of the current Portfolio.
    
    Args:
        with_dividends (bool): True if you want to include dividend information. Defaults to False.
    
    Returns:
        dict: Returns a dictionary where the keys are the stock tickers and the value is another dictionary
            that has the stock price, quantity held, equity, percent change, equity change, type, name, id, pe ratio,
            percentage of portfolio, and average buy price.
    """
    return r.build_holdings(with_dividends=with_dividends)

def build_user_profile() -> dict:
    """Builds a dictionary of important information regarding the user account.
    
    Args:
        account_number (Optional[str]): The robinhood account number.
    
    Returns:
        dict: Returns a dictionary that has total equity, extended hours equity, cash, and dividend total.
    """
    return r.build_user_profile()

def get_portfolio_holdings_and_summary() -> dict:
    """Retrieve the current portfolio holdings and account summary.

    This tool returns two pieces of information about the logged‑in user's
    account: ``holdings`` (a dictionary keyed by stock ticker) and
    ``summary`` (the user profile).  It also includes the Phoenix account
    summary if available.
    
    Returns:
        dict: Dictionary containing holdings, summary, and phoenix_summary
    """
    try:
        holdings = r.account.build_holdings()
        profile = r.account.build_user_profile()
        phoenix_account_info = r.account.load_phoenix_account()
        return {
            "holdings": holdings,
            "summary": profile,
            "phoenix_summary": phoenix_account_info,
        }
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve portfolio: {e}")

def get_all_stock_positions_detailed() -> list:
    """Returns a list containing every position ever traded.
    
    Returns:
        list: List of all positions ever traded in the account
    """
    return r.account.get_all_positions()

def get_open_stock_positions_detailed() -> list:
    """Returns a list of stocks that are currently held (open positions).
    
    Returns:
        list: List of currently held stock positions
    """
    return r.account.get_open_stock_positions()

# Profile Sub-agents
load_account_profile_agent = Agent(
    model="gemini-2.5-flash",
    name="load_account_profile_agent",
    description="Get account profile information including day trading info and cash held by Robinhood",
    instruction="You are a specialized agent for retrieving Robinhood account profile information. Use the load_account_profile tool to get detailed account information including buying power, cash balances, margin info, and account settings.",
    tools=[load_account_profile],
    )

load_basic_profile_agent = Agent(
    model="gemini-2.5-flash",
    name="load_basic_profile_agent",
    description="Get personal profile information like phone number, address, and personal details",
    instruction="You are a specialized agent for retrieving Robinhood basic profile information. Use the load_basic_profile tool to get personal information like phone number, address, marital status, and date of birth.",
    tools=[load_basic_profile],
    )

load_investment_profile_agent = Agent(
    model="gemini-2.5-flash",
    name="load_investment_profile_agent",
    description="Get investment profile information from account questionnaire responses",
    instruction="You are a specialized agent for retrieving Robinhood investment profile information. Use the load_investment_profile tool to get investment questionnaire responses including risk tolerance, investment experience, and financial information.",
    tools=[load_investment_profile],
    )

load_portfolio_profile_agent = Agent(
    model="gemini-2.5-flash",
    name="load_portfolio_profile_agent",
    description="Get portfolio profile information including market value and equity details",
    instruction="You are a specialized agent for retrieving Robinhood portfolio profile information. Use the load_portfolio_profile tool to get portfolio metrics like market value, equity, withdrawable amounts, and margin information.",
    tools=[load_portfolio_profile],
    )

load_security_profile_agent = Agent(
    model="gemini-2.5-flash",
    name="load_security_profile_agent",
    description="Get security profile information and compliance details",
    instruction="You are a specialized agent for retrieving Robinhood security profile information. Use the load_security_profile tool to get security and compliance information including control person status and affiliated relationships.",
    tools=[load_security_profile],
    )

load_user_profile_agent = Agent(
    model="gemini-2.5-flash",
    name="load_user_profile_agent",
    description="Get user profile information including username, email, and profile links",
    instruction="You are a specialized agent for retrieving Robinhood user profile information. Use the load_user_profile tool to get basic user information like username, email, name, and profile creation details.",
    tools=[load_user_profile],
    )

# Account Sub-agents
load_phoenix_account_agent = Agent(
    model="gemini-2.5-flash",
    name="load_phoenix_account_agent",
    description="Get unified account information including buying power and equity details",
    instruction="You are a specialized agent for retrieving unified Robinhood account information. Use the load_phoenix_account tool to get comprehensive account data including buying power, equity, cash balances, and portfolio metrics.",
    tools=[load_phoenix_account],
    )

get_all_positions_agent = Agent(
    model="gemini-2.5-flash",
    name="get_all_positions_agent",
    description="Get all positions ever traded in the account",
    instruction="You are a specialized agent for retrieving all Robinhood positions. Use the get_all_positions tool to get comprehensive position data for every stock position ever held in the account.",
    tools=[get_all_positions],
    )

get_open_stock_positions_agent = Agent(
    model="gemini-2.5-flash",
    name="get_open_stock_positions_agent",
    description="Get currently held stock positions",
    instruction="You are a specialized agent for retrieving current Robinhood stock positions. Use the get_open_stock_positions tool to get detailed information about stocks currently held in the account.",
    tools=[get_open_stock_positions],
    )

get_dividends_agent = Agent(
    model="gemini-2.5-flash",
    name="get_dividends_agent",
    description="Get dividend transaction history and details",
    instruction="You are a specialized agent for retrieving Robinhood dividend information. Use the get_dividends tool to get detailed dividend transaction history including amounts, rates, and payment dates.",
    tools=[get_dividends],
    )

get_total_dividends_agent = Agent(
    model="gemini-2.5-flash",
    name="get_total_dividends_agent",
    description="Get total dividend amount received",
    instruction="You are a specialized agent for calculating total Robinhood dividends. Use the get_total_dividends tool to get the total dollar amount of dividends received in the account.",
    tools=[get_total_dividends],
    )

get_bank_accounts_agent = Agent(
    model="gemini-2.5-flash",
    name="get_bank_accounts_agent",
    description="Get linked bank account information",
    instruction="You are a specialized agent for retrieving Robinhood linked bank account information. Use the get_linked_bank_accounts tool to get information about bank accounts linked to the Robinhood account.",
    tools=[get_linked_bank_accounts],
    )

get_bank_transfers_agent = Agent(
    model="gemini-2.5-flash",
    name="get_bank_transfers_agent",
    description="Get bank transfer history and details",
    instruction="You are a specialized agent for retrieving Robinhood bank transfer information. Use the get_bank_transfers tool to get detailed information about deposits and withdrawals between bank accounts and Robinhood.",
    tools=[get_bank_transfers],
    )

get_bank_account_info_agent = Agent(
    model="gemini-2.5-flash",
    name="get_bank_account_info_agent",
    description="Get specific bank account information by ID",
    instruction="You are a specialized agent for retrieving specific Robinhood bank account information. Use the get_bank_account_info tool to get detailed information about a specific bank account by its ID.",
    tools=[get_bank_account_info],
    )

get_card_transactions_agent = Agent(
    model="gemini-2.5-flash",
    name="get_card_transactions_agent",
    description="Get debit card transaction history",
    instruction="You are a specialized agent for retrieving Robinhood debit card transactions. Use the get_card_transactions tool to get detailed information about debit card transactions made on the account.",
    tools=[get_card_transactions],
    )

get_day_trades_agent = Agent(
    model="gemini-2.5-flash",
    name="get_day_trades_agent",
    description="Get recent day trading activity",
    instruction="You are a specialized agent for retrieving Robinhood day trading information. Use the get_day_trades tool to get information about recent day trades.",
    tools=[get_day_trades],
    )

get_documents_agent = Agent(
    model="gemini-2.5-flash",
    name="get_documents_agent",
    description="Get account documents released by Robinhood",
    instruction="You are a specialized agent for retrieving Robinhood account documents. Use the get_documents tool to get a list of documents that have been released by Robinhood to the account.",
    tools=[get_documents],
    )

get_interest_payments_agent = Agent(
    model="gemini-2.5-flash",
    name="get_interest_payments_agent",
    description="Get interest payment history",
    instruction="You are a specialized agent for retrieving Robinhood interest payments. Use the get_interest_payments tool to get a list of interest payments.",
    tools=[get_interest_payments],
    )

get_latest_notification_agent = Agent(
    model="gemini-2.5-flash",
    name="get_latest_notification_agent",
    description="Get the latest notification timestamp",
    instruction="You are a specialized agent for retrieving the latest Robinhood notification. Use the get_latest_notification tool to get the time of the latest notification.",
    tools=[get_latest_notification],
    )

get_margin_calls_agent = Agent(
    model="gemini-2.5-flash",
    name="get_margin_calls_agent",
    description="Get margin call information",
    instruction="You are a specialized agent for retrieving Robinhood margin calls. Use the get_margin_calls tool to get information about margin calls.",
    tools=[get_margin_calls],
    )

get_margin_interest_agent = Agent(
    model="gemini-2.5-flash",
    name="get_margin_interest_agent",
    description="Get margin interest payment history",
    instruction="You are a specialized agent for retrieving Robinhood margin interest. Use the get_margin_interest tool to get a list of margin interest payments.",
    tools=[get_margin_interest],
    )

get_notifications_agent = Agent(
    model="gemini-2.5-flash",
    name="get_notifications_agent",
    description="Get account notifications",
    instruction="You are a specialized agent for retrieving Robinhood notifications. Use the get_notifications tool to get a list of notifications.",
    tools=[get_notifications],
    )

get_referrals_agent = Agent(
    model="gemini-2.5-flash",
    name="get_referrals_agent",
    description="Get referral information",
    instruction="You are a specialized agent for retrieving Robinhood referrals. Use the get_referrals tool to get a list of referrals.",
    tools=[get_referrals],
    )

get_stock_loan_payments_agent = Agent(
    model="gemini-2.5-flash",
    name="get_stock_loan_payments_agent",
    description="Get stock loan payment history",
    instruction="You are a specialized agent for retrieving Robinhood stock loan payments. Use the get_stock_loan_payments tool to get a list of loan payments.",
    tools=[get_stock_loan_payments],
    )

get_subscription_fees_agent = Agent(
    model="gemini-2.5-flash",
    name="get_subscription_fees_agent",
    description="Get subscription fee history",
    instruction="You are a specialized agent for retrieving Robinhood subscription fees. Use the get_subscription_fees tool to get a list of subscription fees.",
    tools=[get_subscription_fees],
    )

get_wire_transfers_agent = Agent(
    model="gemini-2.5-flash",
    name="get_wire_transfers_agent",
    description="Get wire transfer history",
    instruction="You are a specialized agent for retrieving Robinhood wire transfers. Use the get_wire_transfers tool to get a list of wire transfers.",
    tools=[get_wire_transfers],
    )

get_portfolio_holdings_and_summary_agent = Agent(
    model="gemini-2.5-flash",
    name="get_portfolio_holdings_and_summary_agent",
    description="Get comprehensive portfolio holdings and account summary",
    instruction="You are a specialized agent for retrieving comprehensive Robinhood portfolio information. Use the get_portfolio_holdings_and_summary tool to get holdings, user profile summary, and Phoenix account information in one call.",
    tools=[get_portfolio_holdings_and_summary],
    )

get_all_stock_positions_detailed_agent = Agent(
    model="gemini-2.5-flash",
    name="get_all_stock_positions_detailed_agent",
    description="Get detailed information about all positions ever traded",
    instruction="You are a specialized agent for retrieving all historical Robinhood positions. Use the get_all_stock_positions_detailed tool to get a comprehensive list of every position ever traded in the account.",
    tools=[get_all_stock_positions_detailed],
    )

get_open_stock_positions_detailed_agent = Agent(
    model="gemini-2.5-flash",
    name="get_open_stock_positions_detailed_agent",
    description="Get detailed information about currently held stock positions",
    instruction="You are a specialized agent for retrieving current Robinhood stock positions. Use the get_open_stock_positions_detailed tool to get detailed information about stocks currently held in the account.",
    tools=[get_open_stock_positions_detailed],
    )

get_all_watchlists_agent = Agent(
    model="gemini-2.5-flash",
    name="get_all_watchlists_agent",
    description="Get all watchlists in the account",
    instruction="You are a specialized agent for retrieving Robinhood watchlists. Use the get_all_watchlists tool to get information about all watchlists in the account.",
    tools=[get_all_watchlists],
    )

get_watchlist_by_name_agent = Agent(
    model="gemini-2.5-flash",
    name="get_watchlist_by_name_agent",
    description="Get a specific watchlist by name",
    instruction="You are a specialized agent for retrieving a specific Robinhood watchlist. Use the get_watchlist_by_name tool to get information about a watchlist by its name.",
    tools=[get_watchlist_by_name],
    )

post_symbols_to_watchlist_agent = Agent(
    model="gemini-2.5-flash",
    name="post_symbols_to_watchlist_agent",
    description="Add symbols to a watchlist",
    instruction="You are a specialized agent for adding symbols to a Robinhood watchlist. Use the post_symbols_to_watchlist tool to add symbols to a specified watchlist.",
    tools=[post_symbols_to_watchlist],
    )

delete_symbols_from_watchlist_agent = Agent(
    model="gemini-2.5-flash",
    name="delete_symbols_from_watchlist_agent",
    description="Remove symbols from a watchlist",
    instruction="You are a specialized agent for removing symbols from a Robinhood watchlist. Use the delete_symbols_from_watchlist tool to remove symbols from a specified watchlist.",
    tools=[delete_symbols_from_watchlist],
    )

build_portfolio_agent = Agent(
    model="gemini-2.5-flash",
    name="build_portfolio_agent",
    description="Build comprehensive portfolio holdings summary",
    instruction="You are a specialized agent for building comprehensive Robinhood portfolio summaries. Use the build_robinhood_portfolio tool to create detailed portfolio holdings with performance metrics and position details. If any specific question about a single stock is listed, only parse and return the specific details on what the user wants.",
    tools=[build_robinhood_portfolio],
    )

build_user_profile_agent = Agent(
    model="gemini-2.5-flash",
    name="build_user_profile_agent",
    description="Build comprehensive user account summary",
    instruction="You are a specialized agent for building comprehensive Robinhood user account summaries. Use the build_user_profile tool to create detailed account summaries with equity, cash, and dividend information.",
    tools=[build_user_profile],
    )

# Root coordinator agent
robinhood_portfolio_agent = Agent(
    model="gemini-2.5-flash",
    name="robinhood_portfolio_agent",
    instruction=prompt.AGENT_INSTRUCTION,
    output_key="portfolio_details",
    sub_agents=[
        load_account_profile_agent,
        load_basic_profile_agent,
        load_investment_profile_agent,
        load_portfolio_profile_agent,
        load_security_profile_agent,
        load_user_profile_agent,
        load_phoenix_account_agent,
        get_all_positions_agent,
        get_open_stock_positions_agent,
        get_dividends_agent,
        get_total_dividends_agent,
        get_bank_accounts_agent,
        get_bank_account_info_agent,
        get_bank_transfers_agent,
        get_card_transactions_agent,
        get_day_trades_agent,
        get_documents_agent,
        get_interest_payments_agent,
        get_latest_notification_agent,
        get_margin_calls_agent,
        get_margin_interest_agent,
        get_notifications_agent,
        get_referrals_agent,
        get_stock_loan_payments_agent,
        get_subscription_fees_agent,
        get_wire_transfers_agent,
        get_portfolio_holdings_and_summary_agent,
        get_all_stock_positions_detailed_agent,
        get_open_stock_positions_detailed_agent,
        get_all_watchlists_agent,
        get_watchlist_by_name_agent,
        post_symbols_to_watchlist_agent,
        delete_symbols_from_watchlist_agent,
        build_portfolio_agent,
        build_user_profile_agent,
    ],
)

# Export list
__all__ = [
    "load_account_profile",
    "load_basic_profile",
    "load_investment_profile",
    "load_portfolio_profile",
    "load_security_profile",
    "load_user_profile",
    "load_phoenix_account",
    "get_all_positions",
    "get_open_stock_positions",
    "get_dividends",
    "get_total_dividends",
    "get_linked_bank_accounts",
    "get_bank_account_info",
    "get_bank_transfers",
    "get_card_transactions",
    "get_day_trades",
    "get_documents",
    "get_interest_payments",
    "get_latest_notification",
    "get_margin_calls",
    "get_margin_interest",
    "get_notifications",
    "get_referrals",
    "get_stock_loan_payments",
    "get_subscription_fees",
    "get_all_watchlists",
    "get_watchlist_by_name",
    "post_symbols_to_watchlist",
    "delete_symbols_from_watchlist",
    "get_wire_transfers",
    "get_portfolio_holdings_and_summary",
    "get_all_stock_positions_detailed",
    "get_open_stock_positions_detailed",
    "build_robinhood_portfolio",
    "build_user_profile",
    "load_account_profile_agent",
    "load_basic_profile_agent",
    "load_investment_profile_agent",
    "load_portfolio_profile_agent",
    "load_security_profile_agent",
    "load_user_profile_agent",
    "load_phoenix_account_agent",
    "get_all_positions_agent",
    "get_open_stock_positions_agent",
    "get_dividends_agent",
    "get_total_dividends_agent",
    "get_bank_accounts_agent",
    "get_bank_account_info_agent",
    "get_bank_transfers_agent",
    "get_card_transactions_agent",
    "get_day_trades_agent",
    "get_documents_agent",
    "get_interest_payments_agent",
    "get_latest_notification_agent",
    "get_margin_calls_agent",
    "get_margin_interest_agent",
    "get_notifications_agent",
    "get_referrals_agent",
    "get_stock_loan_payments_agent",
    "get_subscription_fees_agent",
    "get_wire_transfers_agent",
    "get_portfolio_holdings_and_summary_agent",
    "get_all_stock_positions_detailed_agent",
    "get_open_stock_positions_detailed_agent",
    "get_all_watchlists_agent",
    "get_watchlist_by_name_agent",
    "post_symbols_to_watchlist_agent",
    "delete_symbols_from_watchlist_agent",
    "build_portfolio_agent",
    "build_user_profile_agent",
    "robinhood_portfolio_agent",
]
