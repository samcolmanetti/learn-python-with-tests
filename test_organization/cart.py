"""A tiny ``ShoppingCart`` used to demonstrate how to organize a test suite.

The class itself is small on purpose. The interesting part is the test file next to it
(``test_cart.py``), which shows a fixture, ``parametrize``, the arrange-act-assert shape, and a
marker for the one slow test.

Prices are in whole cents so the arithmetic stays exact (no floats).
"""

from __future__ import annotations


class ShoppingCart:
    def __init__(self) -> None:
        self._quantities: dict[str, int] = {}
        self._prices: dict[str, int] = {}

    def add(self, name: str, price: int, quantity: int = 1) -> None:
        """Add ``quantity`` of an item priced at ``price`` cents each."""
        if quantity <= 0:
            raise ValueError("quantity must be positive")
        if price < 0:
            raise ValueError("price must not be negative")
        self._prices[name] = price
        self._quantities[name] = self._quantities.get(name, 0) + quantity

    def quantity(self, name: str) -> int:
        return self._quantities.get(name, 0)

    def total(self) -> int:
        """Total price in cents."""
        return sum(self._prices[name] * count for name, count in self._quantities.items())

    def apply_discount(self, percent: int) -> None:
        """Reduce every stored price by ``percent`` percent, rounding down."""
        if not 0 <= percent <= 100:
            raise ValueError("percent must be between 0 and 100")
        for name in self._prices:
            self._prices[name] = self._prices[name] * (100 - percent) // 100
