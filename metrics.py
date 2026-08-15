"""
Market microstructure and execution metrics.
"""

from typing import Optional


def calculate_spread(
    best_bid: Optional[float],
    best_ask: Optional[float],
) -> Optional[float]:
    """Calculate bid-ask spread."""

    if best_bid is None or best_ask is None:
        return None

    return best_ask - best_bid


def calculate_mid_price(
    best_bid: Optional[float],
    best_ask: Optional[float],
) -> Optional[float]:
    """Calculate mid price."""

    if best_bid is None or best_ask is None:
        return None

    return (best_bid + best_ask) / 2.0


def calculate_execution_vwap(trades) -> float:
    """
    Calculate volume-weighted average execution price.

    VWAP = sum(price * quantity) / sum(quantity)
    """

    if not trades:
        return 0.0

    total_value = sum(
        trade.price * trade.quantity
        for trade in trades
    )

    total_quantity = sum(
        trade.quantity
        for trade in trades
    )

    if total_quantity == 0:
        return 0.0

    return total_value / total_quantity


def calculate_total_volume(trades) -> int:
    """Calculate total executed volume."""

    return sum(
        trade.quantity
        for trade in trades
    )


def calculate_execution_cost(
    trades,
    benchmark_price: float,
) -> float:
    """
    Calculate execution cost relative to a benchmark.

    Positive value means buying above the benchmark or
    selling below the benchmark.
    """

    if not trades:
        return 0.0

    cost = 0.0

    for trade in trades:
        if trade.buy_order_id:
            cost += (
                trade.price - benchmark_price
            ) * trade.quantity

    return cost
