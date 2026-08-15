"""
Execution simulation for the Limit Order Book.

Generates a sequence of deterministic market and limit orders
to demonstrate order matching and partial execution.
"""

from orders import OrderType, Side
from order_book import LimitOrderBook


def run_execution_simulation() -> LimitOrderBook:
    """
    Run a deterministic execution simulation.

    The scenario demonstrates:
    - Resting liquidity
    - Price-time priority
    - Market order execution
    - Partial fills
    - Limit order crossing
    """

    book = LimitOrderBook()

    # ---------------------------------------------------------
    # INITIAL SELL LIQUIDITY
    # ---------------------------------------------------------

    book.submit_order(
        side=Side.SELL,
        order_type=OrderType.LIMIT,
        quantity=5,
        price=100.00,
    )

    book.submit_order(
        side=Side.SELL,
        order_type=OrderType.LIMIT,
        quantity=7,
        price=100.00,
    )

    book.submit_order(
        side=Side.SELL,
        order_type=OrderType.LIMIT,
        quantity=10,
        price=100.50,
    )

    # ---------------------------------------------------------
    # INITIAL BUY LIQUIDITY
    # ---------------------------------------------------------

    book.submit_order(
        side=Side.BUY,
        order_type=OrderType.LIMIT,
        quantity=8,
        price=99.50,
    )

    book.submit_order(
        side=Side.BUY,
        order_type=OrderType.LIMIT,
        quantity=10,
        price=99.00,
    )

    # ---------------------------------------------------------
    # MARKET BUY
    # ---------------------------------------------------------

    # Buys 5 at 100.00 and 7 at 100.00,
    # then 3 at 100.50.
    book.submit_order(
        side=Side.BUY,
        order_type=OrderType.MARKET,
        quantity=15,
    )

    # ---------------------------------------------------------
    # CROSSING LIMIT SELL
    # ---------------------------------------------------------

    # This sell order can execute against bids at 99.50.
    book.submit_order(
        side=Side.SELL,
        order_type=OrderType.LIMIT,
        quantity=5,
        price=99.50,
    )

    # ---------------------------------------------------------
    # PARTIAL FILL EXAMPLE
    # ---------------------------------------------------------

    # Only part of the available quantity is consumed.
    book.submit_order(
        side=Side.BUY,
        order_type=OrderType.LIMIT,
        quantity=12,
        price=100.50,
    )

    return book
