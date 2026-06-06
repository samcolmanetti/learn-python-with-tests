# Test organization

**[You can find all the code for this chapter here](https://github.com/samcolmanetti/learn-python-with-tests/tree/main/code/test_organization)**

A test suite is code too, and it rots like any other code if you let it. This chapter builds a
small `ShoppingCart` and, alongside it, a test file that stays readable as the suite grows:
fixtures for setup, `parametrize` for the boring repetition, a `conftest.py` to share, and a
marker to keep the slow tests out of your fast loop.

We'll write the cart test-first as usual, and each new requirement is an excuse to reach for one
more organizing tool. The cart is deliberately tiny. The point is the shape of the tests around it.

One naming note before we start: the module under test is `cart.py`, not `test_cart.py`. `pytest`
collects every `test_*.py` file as tests, so if you name your *production* module `test_`-anything
it gets dragged into the test run. Keep the module and its tests as a pair: `cart.py` and
`test_cart.py`.

## Write the test first

The smallest behaviour: a brand-new cart is empty. We'll keep prices in whole cents so the
arithmetic stays exact and we never have to argue with a float.

In `test_organization/test_cart.py`:

```python
from cart import ShoppingCart


def test_new_cart_is_empty():
    cart = ShoppingCart()
    assert cart.total() == 0
    assert cart.quantity("apple") == 0
```

A new cart costs nothing and holds nothing. That's the behaviour, and it pins down two methods we
haven't written: `total` and `quantity`.

## Try to run the test

```
ImportError: cannot import name 'ShoppingCart' from 'test_organization.cart'
```

There's no `ShoppingCart` to import yet. The import is the first thing to break, which is exactly
the error we want to see first.

## Write the minimal amount of code for the test to run and check the failing test output

Give it a class with the two methods, both stubbed to return `0`. This is wrong on purpose. We
want the test to *run* so we can watch it fail on a value, which proves the test checks what we
think it does.

In `test_organization/cart.py`:

```python
from __future__ import annotations


class ShoppingCart:
    def __init__(self) -> None:
        pass

    def quantity(self, name: str) -> int:
        return 0

    def total(self) -> int:
        return 0
```

Here both stubs happen to return `0`, and an empty cart *is* empty, so this one actually passes.
That's fine. An empty cart returning zero is the correct behaviour, even from a stub. The next
test is where the stub falls over.

## Repeat for new requirements

Now make it hold something. Adding one apple at 50 cents should leave one apple in the cart and a
total of 50.

### Write the test first

```python
def test_add_one_item():
    # Arrange: a fresh cart.
    cart = ShoppingCart()
    # Act:
    cart.add("apple", price=50)
    # Assert:
    assert cart.quantity("apple") == 1
    assert cart.total() == 50
```

Notice the three comments. That's *arrange-act-assert*: set up the world, do the one thing you're
testing, then check what happened. You don't have to write the comments out every time (we'll drop
them once the shape is obvious), but every test should have those three phases in that order, and a
test that does two unrelated "act" steps is usually two tests wearing a trench coat.

### Try to run the test

```
    def test_add_one_item():
        # Arrange: a fresh cart.
        cart = ShoppingCart()
        # Act:
        cart.add("apple", price=50)
        # Assert:
>       assert cart.quantity("apple") == 1
E       AssertionError: assert 0 == 1
E        +  where 0 = quantity('apple')
```

There's no `add` method, so the first failure is actually an `AttributeError` on `cart.add`. Once
we add a stub `add` that does nothing, the failure moves to the line above: `quantity` still
returns the stubbed `0`. The test fails on the value, not on a missing name. Good.

### Write enough code to make it pass

Store quantities and prices in two dicts, and add to them.

```python
from __future__ import annotations


class ShoppingCart:
    def __init__(self) -> None:
        self._quantities: dict[str, int] = {}
        self._prices: dict[str, int] = {}

    def add(self, name: str, price: int, quantity: int = 1) -> None:
        self._prices[name] = price
        self._quantities[name] = self._quantities.get(name, 0) + quantity

    def quantity(self, name: str) -> int:
        return self._quantities.get(name, 0)

    def total(self) -> int:
        return sum(self._prices[name] * count for name, count in self._quantities.items())
```

Run `uv run pytest` and both tests are green.

### Refactor

Nothing to tidy in the code yet. But look at the two tests: each opens with
`cart = ShoppingCart()`. That's one line now, and it'll be the same line at the top of every test
we write from here on. **Duplicated setup is the thing fixtures exist to remove**, so let's reach
for one.

A *fixture* is a function pytest calls for you and passes in by name. You declare it once, then any
test that wants a fresh cart just takes a `cart` argument.

```python
import pytest

from cart import ShoppingCart


@pytest.fixture
def cart():
    return ShoppingCart()


def test_new_cart_is_empty(cart):
    assert cart.total() == 0
    assert cart.quantity("apple") == 0


def test_add_one_item(cart):
    cart.add("apple", price=50)
    assert cart.quantity("apple") == 1
    assert cart.total() == 50
```

pytest sees the `cart` parameter, finds the fixture with that name, calls it, and hands the result
in. The setup line is gone from every test.

The part that trips people up: **each test gets its own fresh `cart`**. The fixture function runs
again for every test that asks for it, so one test can't pollute another's cart. That isolation is
the whole reason we don't just make a module-level `cart` variable.

Re-run the tests. Still green, and now there's no duplicated setup to drift out of sync.

## Repeat for new requirements

Our next requirement is a discount. `apply_discount(10)` should knock 10 percent off every price,
rounding down to whole cents. Before we can test that cleanly, we want a cart that already has a
few things in it, so we don't repeat the same three `add` calls in test after test.

### Write the test first

This is a second fixture, and it's allowed to depend on the first. A cart with some stock in it:

```python
@pytest.fixture
def stocked_cart(cart):
    cart.add("apple", price=50, quantity=3)
    cart.add("bread", price=200, quantity=1)
    return cart


def test_total_sums_across_items(stocked_cart):
    assert stocked_cart.total() == 3 * 50 + 200
```

`stocked_cart` takes `cart` as an argument, so pytest builds a fresh `cart` first, then passes it
in here for stocking. **Fixtures composing on other fixtures is how you build up test setup in
layers** instead of one giant setup function.

Now the discount itself. The behaviour is the same shape four times: apply a percentage, check the
total. Writing four near-identical test functions is exactly the repetition `parametrize` removes.

```python
@pytest.mark.parametrize(
    ("percent", "expected"),
    [
        (0, 350),
        (10, 315),
        (50, 175),
        (100, 0),
    ],
)
def test_apply_discount(stocked_cart, percent, expected):
    stocked_cart.apply_discount(percent)
    assert stocked_cart.total() == expected
```

`stocked_cart` starts at 350 cents (three apples at 50, one bread at 200). One discount of 10
percent rounds 50 down to 45 and 200 down to 180, giving `3 * 45 + 180 == 315`. The four rows are
four independent test cases sharing one body.

### Try to run the test

`apply_discount` doesn't exist yet, so every row errors the same way:

```
E       AttributeError: 'ShoppingCart' object has no attribute 'apply_discount'
```

One missing method, reported once per parametrized row. That's the tell that all four cases are
real, separate tests: pytest runs the body four times, once per row.

### Write enough code to make it pass

Add the method. Integer `//` gives us the round-down for free.

```python
    def apply_discount(self, percent: int) -> None:
        for name in self._prices:
            self._prices[name] = self._prices[name] * (100 - percent) // 100
```

Run `uv run pytest` and watch the four rows go green. pytest names each one by its arguments:

```
test_cart.py::test_apply_discount[0-350] PASSED
test_cart.py::test_apply_discount[10-315] PASSED
test_cart.py::test_apply_discount[50-175] PASSED
test_cart.py::test_apply_discount[100-0] PASSED
```

When one case breaks, the `[10-315]` in the name tells you *which* case without you adding a single
`print`. That readable id is half the reason to parametrize instead of looping inside one test: a
loop that fails on the third iteration gives you one failure and no idea which input caused it.

### Refactor

The validation is missing. `add` should refuse a non-positive quantity or a negative price, and
`apply_discount` should refuse a percentage outside 0 to 100. That's error behaviour, and error
behaviour deserves tests too. `parametrize` plus `pytest.raises` reads nicely here:

```python
@pytest.mark.parametrize(
    ("price", "quantity"),
    [
        (50, 0),
        (50, -1),
        (-10, 1),
    ],
)
def test_add_rejects_bad_arguments(cart, price, quantity):
    with pytest.raises(ValueError):
        cart.add("apple", price=price, quantity=quantity)
```

Then make them pass by guarding the inputs:

```python
    def add(self, name: str, price: int, quantity: int = 1) -> None:
        if quantity <= 0:
            raise ValueError("quantity must be positive")
        if price < 0:
            raise ValueError("price must not be negative")
        self._prices[name] = price
        self._quantities[name] = self._quantities.get(name, 0) + quantity

    def apply_discount(self, percent: int) -> None:
        if not 0 <= percent <= 100:
            raise ValueError("percent must be between 0 and 100")
        for name in self._prices:
            self._prices[name] = self._prices[name] * (100 - percent) // 100
```

Re-run the tests. Green, including the error cases, with the tests as the safety net that says our
guards reject the right things and nothing else.

## Repeat for new requirements

Two more things tidy a real suite: sharing fixtures across files, and quarantining slow tests.

### Move shared fixtures to conftest.py

Right now `cart` and `stocked_cart` live at the top of `test_cart.py`. The moment a second test
file wants a `cart`, you'd be tempted to copy them. Don't. Put shared fixtures in a file named
`conftest.py` next to your tests, and **pytest makes every fixture in it available to every test in
that directory and below, with no import**.

Create `test_organization/conftest.py`:

```python
import pytest

from cart import ShoppingCart


@pytest.fixture
def cart():
    return ShoppingCart()


@pytest.fixture
def stocked_cart(cart):
    cart.add("apple", price=50, quantity=3)
    cart.add("bread", price=200, quantity=1)
    return cart
```

Then delete those two fixture definitions from `test_cart.py`. The tests don't change at all:
they still take `cart` and `stocked_cart` by name. pytest discovers `conftest.py` automatically, so
there's no `import` line for it, and there shouldn't be. I find that magic mildly unsettling the
first time, but it's the one place pytest's auto-discovery earns its keep.

Run `uv run pytest`. Same passes, fixtures now shared.

### Mark the slow test

Suppose one test is genuinely slow (a big import, a sleep, a thousand operations). You don't want
it in the loop you run on every save. Tag it with a *marker* so you can deselect it.

```python
import time


@pytest.mark.slow
def test_total_stays_correct_under_many_adds(cart):
    time.sleep(0.05)
    for _ in range(1000):
        cart.add("apple", price=1)
    assert cart.quantity("apple") == 1000
    assert cart.total() == 1000
```

`@pytest.mark.slow` attaches the label `slow` to this test. Register the marker in
`pyproject.toml` so pytest doesn't warn about an unknown one:

```toml
[tool.pytest.ini_options]
markers = [
    "slow: marks slower tests (deselect with '-m \"not slow\"')",
]
```

Now your fast inner loop skips it with `uv run pytest -m "not slow"`:

```
13 passed, 1 deselected in 0.10s
```

The slow test is still there, still run by CI with a plain `uv run pytest`, but it's out of the way
while you're working. **A fast test suite is one you actually run**, so make the common command the
fast one. A suite that takes two minutes is a suite you'll start skipping, and a suite you skip
isn't protecting you.

## Wrapping up

- **A fixture is shared setup pytest injects by name**, and each test gets a fresh one, which keeps
  tests isolated from each other.
- **Fixtures can depend on fixtures**, so you build setup in layers (`stocked_cart` on top of
  `cart`) instead of one tangled setup function.
- **`conftest.py` shares fixtures across every test file in a directory** with no import. pytest
  finds it for you.
- **`parametrize` turns N near-identical tests into one body plus a table of cases**, and each row
  gets a readable id like `[10-315]` so a failure tells you which input broke.
- **Arrange-act-assert** is the shape of a good test: set up, do one thing, check one outcome.
- **Markers let you tag and deselect tests** (`-m "not slow"`), so your inner loop stays fast and
  the slow tests still run in CI.

Next: [pytest deep dive](pytest-deep-dive.md), which goes further into fixture scopes, ids, and the
flags that make pytest's output tell you exactly what broke.
