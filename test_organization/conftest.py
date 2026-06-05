"""Fixtures shared across this folder's tests.

pytest finds ``conftest.py`` automatically. Any fixture defined here is available to every test
in this directory (and below it) without importing anything.
"""

import pytest

from .cart import ShoppingCart


@pytest.fixture
def cart() -> ShoppingCart:
    """A fresh, empty cart for each test that asks for one."""
    return ShoppingCart()


@pytest.fixture
def stocked_cart(cart: ShoppingCart) -> ShoppingCart:
    """A cart pre-loaded with a couple of items. Fixtures can depend on fixtures."""
    cart.add("apple", price=50, quantity=3)
    cart.add("bread", price=200, quantity=1)
    return cart
