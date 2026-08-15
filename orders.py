"""
Order definitions for the Limit Order Book & Matching Engine.

Supports:
- Limit orders
- Market orders
- Buy and sell sides
- Price-time priority
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class Side(Enum):
    BUY = "BUY"
    SELL = "SELL"


class OrderType(Enum):
    LIMIT = "LIMIT"
    MARKET = "MARKET"


@dataclass
class Order:
    order_id: int
    side: Side
    order_type: OrderType
    quantity: int
    price: Optional[float] = None

    remaining_quantity: int = field(init=False)
    timestamp: int = 0
    active: bool = True

    def __post_init__(self):
        if self.quantity <= 0:
            raise ValueError("Order quantity must be positive.")

        if self.order_type == OrderType.LIMIT:
            if self.price is None or self.price <= 0:
                raise ValueError(
                    "Limit orders must have a positive price."
                )

        self.remaining_quantity = self.quantity

    def is_filled(self) -> bool:
        """Return True when the order is completely filled."""
        return self.remaining_quantity == 0

    def cancel(self) -> None:
        """Cancel the remaining quantity of the order."""
        self.active = False

    def fill(self, quantity: int) -> None:
        """Reduce remaining quantity after an execution."""
        if quantity <= 0:
            raise ValueError("Fill quantity must be positive.")

        if quantity > self.remaining_quantity:
            raise ValueError("Fill quantity exceeds remaining quantity.")

        self.remaining_quantity -= quantity

        if self.remaining_quantity == 0:
            self.active = False

    def __repr__(self) -> str:
        return (
            f"Order(id={self.order_id}, "
            f"side={self.side.value}, "
            f"type={self.order_type.value}, "
            f"price={self.price}, "
            f"remaining={self.remaining_quantity})"
        )
