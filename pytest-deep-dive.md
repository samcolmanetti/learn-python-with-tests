# pytest deep dive

**[You can find all the code for this chapter here](pytest_deep_dive/)**

You've already met the basics — `test_*` functions, plain `assert`, and `parametrize`. This
chapter adds the three tools you'll use in almost every suite from here on: **fixtures**,
**`pytest.raises`**, and **markers**. We'll test a tiny `Account` class to show each one.

## The subject under test

```python
class InsufficientFunds(Exception):
    ...


class Account:
    def __init__(self, balance=0):
        if balance < 0:
            raise ValueError("opening balance cannot be negative")
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("deposit must be positive")
        self.balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("withdrawal must be positive")
        if amount > self.balance:
            raise InsufficientFunds(f"cannot withdraw {amount} from balance {self.balance}")
        self.balance -= amount
```

## Fixtures: reusable setup, injected by name

A **fixture** is a function decorated with `@pytest.fixture`. Any test that names it as a
parameter receives its return value. Each test gets a **fresh** result, so there's no shared
state to leak between tests.

```python
import pytest

from .bank import Account, InsufficientFunds


@pytest.fixture
def account():
    return Account(balance=100)


def test_deposit_increases_balance(account):
    account.deposit(50)
    assert account.balance == 150


def test_withdraw_decreases_balance(account):
    account.withdraw(30)
    assert account.balance == 70
```

`test_deposit_increases_balance` mutates its `account`, but `test_withdraw_decreases_balance`
still starts from 100 — they each called the fixture and got their own object. That isolation
is the whole point: tests that share mutable state fail in confusing, order-dependent ways.

> Put fixtures you want to share across files in a `conftest.py`; pytest discovers them
> automatically with no import needed.

## `pytest.raises`: testing the error path

Happy-path tests aren't enough — the interesting bugs live in the failure modes. Assert that
code raises with `pytest.raises`:

```python
def test_overdrawing_raises(account):
    with pytest.raises(InsufficientFunds):
        account.withdraw(101)


def test_overdraw_message_mentions_the_balance(account):
    with pytest.raises(InsufficientFunds, match=r"balance 100"):
        account.withdraw(500)
```

The `with` block **must** raise the named exception or the test fails. `match` additionally
checks the message against a regular expression — handy when one exception type is raised for
several reasons and you want to pin down which.

## Markers: tag tests to select or skip

A **marker** labels a test so you can run a subset. Register custom markers in `pyproject.toml`
(otherwise pytest warns):

```toml
[tool.pytest.ini_options]
markers = [
    "slow: marks slower tests (deselect with '-m \"not slow\"')",
]
```

```python
@pytest.mark.slow
def test_many_deposits_accumulate(account):
    for _ in range(1000):
        account.deposit(1)
    assert account.balance == 1100
```

Now you can run the fast suite during tight TDD loops and the full suite before committing:

```bash
pytest -m "not slow"   # skip slow tests
pytest -m slow         # only slow tests
```

Built-in markers you'll reach for: `@pytest.mark.skip(reason=...)`,
`@pytest.mark.skipif(condition, reason=...)`, and `@pytest.mark.xfail` for known-broken cases.

## Putting it together with `parametrize`

Combine markers, fixtures, and `parametrize` freely. Here `parametrize` drives the error-path
test over several bad inputs:

```python
@pytest.mark.parametrize("bad_amount", [0, -1, -100])
def test_non_positive_deposits_are_rejected(account, bad_amount):
    with pytest.raises(ValueError):
        account.deposit(bad_amount)
```

## Wrapping up

- **Fixtures** give each test isolated, reusable setup — request them by parameter name.
- **`pytest.raises`** (optionally with `match`) is how you test error paths; always test them.
- **Markers** tag tests so you can slice the suite (`-m "not slow"`); register custom ones in
  `pyproject.toml`.
- These compose with `parametrize` to keep suites small and expressive.

Next: generate your test cases automatically with [property-based testing](property-based-testing.md).
