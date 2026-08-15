"""
Limit Order Book and Price-Time Priority Matching Engine.

Features:
- Price-time priority
- Limit orders
- Market orders
- Partial fills
- Order cancellation
- Trade generation
- Best bid / best ask tracking
"""

from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from orders import Order, OrderType, Side


@dataclass
class Trade:
    trade_id: int
    buy_order_id: int
    sell_order_id: int
    price: float
    quantity: int
    timestamp: int

    def __repr__(self) -> str:
        return (
            f"Trade(id={self.trade_id}, "
            f"price={self.price:.2f}, "
            f"quantity={self.quantity}, "
            f"buy={self.buy_order_id}, "
            f"sell={self.sell_order_id})"
        )


class LimitOrderBook:
    """
    Central limit order book using price-time priority.

    Bid side:
        Higher prices have priority.

    Ask side:
        Lower prices have priority.

    At the same price:
        Earlier orders have priority.
    """

    def __init__(self):
        self.bids: Dict[float, deque] = defaultdict(deque)
        self.asks: Dict[float, deque] = defaultdict(deque)

        self.orders: Dict[int, Order] = {}

        self.trade_history: List[Trade] = []

        self.next_order_id = 1
        self.next_trade_id = 1
        self.timestamp = 0

    # ---------------------------------------------------------
    # ORDER CREATION
    # ---------------------------------------------------------

    def create_order(
        self,
        side: Side,
        order_type: OrderType,
        quantity: int,
        price: Optional[float] = None,
    ) -> Order:
        """Create and register a new order."""

        order = Order(
            order_id=self.next_order_id,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
            timestamp=self.timestamp,
        )

        self.orders[order.order_id] = order

        self.next_order_id += 1
        self.timestamp += 1

        return order

    # ---------------------------------------------------------
    # SUBMIT ORDER
    # ---------------------------------------------------------

    def submit_order(
        self,
        side: Side,
        order_type: OrderType,
        quantity: int,
        price: Optional[float] = None,
    ) -> Tuple[Order, List[Trade]]:

        order = self.create_order(
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
        )

        trades = self._match_order(order)

        # Remaining limit quantity becomes resting liquidity.
        if (
            order.remaining_quantity > 0
            and order.active
            and order.order_type == OrderType.LIMIT
        ):
            self._add_to_book(order)

        return order, trades

    # ---------------------------------------------------------
    # MATCHING ENGINE
    # ---------------------------------------------------------

    def _match_order(self, incoming_order: Order) -> List[Trade]:
        trades = []

        while incoming_order.remaining_quantity > 0:

            if incoming_order.side == Side.BUY:
                best_price = self.best_ask()
                opposite_book = self.asks

                if best_price is None:
                    break

                # Limit buy can execute only at ask <= buy limit.
                if incoming_order.order_type == OrderType.LIMIT:
                    if incoming_order.price < best_price:
                        break

            else:
                best_price = self.best_bid()
                opposite_book = self.bids

                if best_price is None:
                    break

                # Limit sell can execute only at bid >= sell limit.
                if incoming_order.order_type == OrderType.LIMIT:
                    if incoming_order.price > best_price:
                        break

            price_level = opposite_book[best_price]

            while (
                price_level
                and incoming_order.remaining_quantity > 0
            ):
                resting_order = price_level[0]

                if not resting_order.active:
                    price_level.popleft()
                    continue

                execution_quantity = min(
                    incoming_order.remaining_quantity,
                    resting_order.remaining_quantity,
                )

                execution_price = resting_order.price

                if incoming_order.side == Side.BUY:
                    buy_order_id = incoming_order.order_id
                    sell_order_id = resting_order.order_id
                else:
                    buy_order_id = resting_order.order_id
                    sell_order_id = incoming_order.order_id

                incoming_order.fill(execution_quantity)
                resting_order.fill(execution_quantity)

                trade = Trade(
                    trade_id=self.next_trade_id,
                    buy_order_id=buy_order_id,
                    sell_order_id=sell_order_id,
                    price=execution_price,
                    quantity=execution_quantity,
                    timestamp=self.timestamp,
                )

                self.trade_history.append(trade)
                trades.append(trade)

                self.next_trade_id += 1
                self.timestamp += 1

                if resting_order.is_filled():
                    price_level.popleft()

            if not price_level:
                del opposite_book[best_price]

        # Market order with unfilled quantity is cancelled.
        if (
            incoming_order.order_type == OrderType.MARKET
            and incoming_order.remaining_quantity > 0
        ):
            incoming_order.cancel()

        return trades

    # ---------------------------------------------------------
    # ADD RESTING ORDER
    # ---------------------------------------------------------

    def _add_to_book(self, order: Order) -> None:
        """Add an unmatched limit order to the appropriate price level."""

        if order.side == Side.BUY:
            self.bids[order.price].append(order)
        else:
            self.asks[order.price].append(order)

    # ---------------------------------------------------------
    # CANCELLATION
    # ---------------------------------------------------------

    def cancel_order(self, order_id: int) -> bool:
        """Cancel an active order."""

        order = self.orders.get(order_id)

        if order is None:
            return False

        if not order.active:
            return False

        order.cancel()

        return True

    # ---------------------------------------------------------
    # BEST PRICES
    # ---------------------------------------------------------

    def best_bid(self) -> Optional[float]:
        """Return highest bid price."""

        active_prices = [
            price
            for price, queue in self.bids.items()
            if any(order.active for order in queue)
        ]

        if not active_prices:
            return None

        return max(active_prices)

    def best_ask(self) -> Optional[float]:
        """Return lowest ask price."""

        active_prices = [
            price
            for price, queue in self.asks.items()
            if any(order.active for order in queue)
        ]

        if not active_prices:
            return None

        return min(active_prices)

    # ---------------------------------------------------------
    # MID PRICE
    # ---------------------------------------------------------

    def mid_price(self) -> Optional[float]:
        """Calculate the mid-market price."""

        bid = self.best_bid()
        ask = self.best_ask()

        if bid is None or ask is None:
            return None

        return (bid + ask) / 2.0

    # ---------------------------------------------------------
    # MARKET DEPTH
    # ---------------------------------------------------------

    def get_depth(self) -> dict:
        """Return aggregated order-book depth."""

        bids = []

        for price in sorted(self.bids.keys(), reverse=True):
            quantity = sum(
                order.remaining_quantity
                for order in self.bids[price]
                if order.active
            )

            if quantity > 0:
                bids.append((price, quantity))

        asks = []

        for price in sorted(self.asks.keys()):
            quantity = sum(
                order.remaining_quantity
                for order in self.asks[price]
                if order.active
            )

            if quantity > 0:
                asks.append((price, quantity))

        return {
            "bids": bids,
            "asks": asks,
        }

    # ---------------------------------------------------------
    # DISPLAY BOOK
    # ---------------------------------------------------------

    def display_book(self, levels: int = 5) -> None:
        """Print top levels of the order book."""

        depth = self.get_depth()

        print("\n" + "=" * 55)
        print("LIMIT ORDER BOOK")
        print("=" * 55)

        print("\nASKS")
        print("-" * 25)

        for price, quantity in depth["asks"][:levels]:
            print(
                f"Price: {price:8.2f} | "
                f"Quantity: {quantity:5d}"
            )

        print("\n" + "-" * 25)

        mid = self.mid_price()

        if mid is not None:
            print(f"Mid Price: {mid:.2f}")

        print("-" * 25)

        print("\nBIDS")
        print("-" * 25)

        for price, quantity in depth["bids"][:levels]:
            print(
                f"Price: {price:8.2f} | "
                f"Quantity: {quantity:5d}"
            )

        print("=" * 55)

    # ---------------------------------------------------------
    # TRADE HISTORY
    # ---------------------------------------------------------

    def print_trade_history(self) -> None:
        """Display executed trades."""

        print("\nEXECUTED TRADES")
        print("-" * 65)

        for trade in self.trade_history:
            print(
                f"Trade {trade.trade_id:3d} | "
                f"Price: {trade.price:8.2f} | "
                f"Qty: {trade.quantity:4d} | "
                f"Buy: {trade.buy_order_id:3d} | "
                f"Sell: {trade.sell_order_id:3d}"
      )
