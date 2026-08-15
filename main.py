"""
Limit Order Book & Matching Engine
===================================

Demonstrates:

- Price-time priority
- Market orders
- Limit orders
- Partial fills
- Market microstructure
- Execution simulation
"""

from execution import run_execution_simulation
from metrics import (
    calculate_mid_price,
    calculate_spread,
    calculate_execution_vwap,
    calculate_total_volume,
)


def main():
    print("=" * 60)
    print(" LIMIT ORDER BOOK & MATCHING ENGINE")
    print("=" * 60)

    print("\nRunning execution simulation...")

    book = run_execution_simulation()

    # ---------------------------------------------------------
    # ORDER BOOK
    # ---------------------------------------------------------

    book.display_book()

    # ---------------------------------------------------------
    # MARKET DATA
    # ---------------------------------------------------------

    best_bid = book.best_bid()
    best_ask = book.best_ask()

    mid_price = calculate_mid_price(
        best_bid,
        best_ask,
    )

    spread = calculate_spread(
        best_bid,
        best_ask,
    )

    # ---------------------------------------------------------
    # EXECUTION METRICS
    # ---------------------------------------------------------

    total_volume = calculate_total_volume(
        book.trade_history
    )

    vwap = calculate_execution_vwap(
        book.trade_history
    )

    print("\nMARKET MICROSTRUCTURE")
    print("-" * 40)

    print(
        f"Best Bid          : "
        f"{best_bid:.2f}"
        if best_bid is not None
        else "Best Bid          : None"
    )

    print(
        f"Best Ask          : "
        f"{best_ask:.2f}"
        if best_ask is not None
        else "Best Ask          : None"
    )

    print(
        f"Mid Price         : "
        f"{mid_price:.2f}"
        if mid_price is not None
        else "Mid Price         : None"
    )

    print(
        f"Bid-Ask Spread    : "
        f"{spread:.2f}"
        if spread is not None
        else "Bid-Ask Spread    : None"
    )

    print("\nEXECUTION STATISTICS")
    print("-" * 40)

    print(
        f"Total Trades      : "
        f"{len(book.trade_history)}"
    )

    print(
        f"Total Volume      : "
        f"{total_volume}"
    )

    print(
        f"Execution VWAP    : "
        f"{vwap:.4f}"
    )

    # ---------------------------------------------------------
    # TRADE HISTORY
    # ---------------------------------------------------------

    book.print_trade_history()

    print("\n" + "=" * 60)
    print(" SIMULATION COMPLETED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    main()
