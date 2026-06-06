import time

import pytest

from .cart import ShoppingCart


def test_new_cart_is_empty(cart: ShoppingCart):
    # The `cart` fixture lives in conftest.py; pytest injects a fresh one here.
    assert cart.total() == 0
    assert cart.quantity("apple") == 0


def test_add_one_item(cart: ShoppingCart):
    # Arrange: a fresh cart (from the fixture).
    # Act:
    cart.add("apple", price=50)
    # Assert:
    assert cart.quantity("apple") == 1
    assert cart.total() == 50


def test_adding_same_item_accumulates_quantity(cart: ShoppingCart):
    cart.add("apple", price=50, quantity=2)
    cart.add("apple", price=50, quantity=3)

    assert cart.quantity("apple") == 5
    assert cart.total() == 250


def test_total_sums_across_items(stocked_cart: ShoppingCart):
    # `stocked_cart` already has 3 apples at 50 and 1 bread at 200.
    assert stocked_cart.total() == 3 * 50 + 200


@pytest.mark.parametrize(
    ("percent", "expected"),
    [
        (0, 350),
        (10, 315),
        (50, 175),
        (100, 0),
    ],
)
def test_apply_discount(stocked_cart: ShoppingCart, percent: int, expected: int):
    stocked_cart.apply_discount(percent)
    assert stocked_cart.total() == expected


@pytest.mark.parametrize(
    ("price", "quantity"),
    [
        (50, 0),
        (50, -1),
        (-10, 1),
    ],
)
def test_add_rejects_bad_arguments(cart: ShoppingCart, price: int, quantity: int):
    with pytest.raises(ValueError):
        cart.add("apple", price=price, quantity=quantity)


@pytest.mark.parametrize("percent", [-1, 101])
def test_discount_rejects_out_of_range(cart: ShoppingCart, percent: int):
    with pytest.raises(ValueError):
        cart.apply_discount(percent)


@pytest.mark.slow
def test_total_stays_correct_under_many_adds(cart: ShoppingCart):
    # A stand-in for the kind of test that's genuinely slow (here a tiny sleep so it's
    # deterministic and fast, but tagged so `-m "not slow"` can skip it).
    time.sleep(0.05)
    for _ in range(1000):
        cart.add("apple", price=1)
    assert cart.quantity("apple") == 1000
    assert cart.total() == 1000
