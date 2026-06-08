# pytest deep dive

**[You can find all the code for this chapter here](https://github.com/samcolmanetti/learn-python-with-tests/tree/main/code/pytest_deep_dive)**

You've already met the basics: `test_*` functions, plain `assert`, and `parametrize`. This
chapter adds the three tools you'll use in almost every suite from here on: fixtures,
`pytest.raises`, and markers. We'll build a tiny `Account` class test-first and pick up each tool
as a requirement forces it.

## The thing we're building

A bank account with a balance. You can deposit and withdraw, deposits and withdrawals have to be
positive, and you can't take out more than you have. We'll grow it one test at a time, and each
new rule will give us a reason to reach for another piece of pytest.

## Write the test first

Start with the happy path: open an account with 100, deposit 50, and the balance is 150. We'll
need a second test for withdrawal too, and both want the same starting account. Rather than build
that account by hand in every test, we name a *fixture*: a function decorated with
`@pytest.fixture`. Any test that names it as a parameter gets its return value, fresh each time.

```python
import pytest

from bank import Account, InsufficientFunds


@pytest.fixture
def account():
    """A fresh account opened with 100. Each test gets its own, with no shared state."""
    return Account(balance=100)


def test_deposit_increases_balance(account):
    account.deposit(50)
    assert account.balance == 150


def test_withdraw_decreases_balance(account):
    account.withdraw(30)
    assert account.balance == 70
```

The fixture is the new idea here. `test_deposit_increases_balance` mutates its `account`, but
`test_withdraw_decreases_balance` still starts from 100: they each called the fixture and got
their own object. That isolation is the whole point. Tests that share mutable state fail in
confusing, order-dependent ways.

## Try to run the test

We've imported `Account` and `InsufficientFunds` from a `bank` module that doesn't exist yet, so
the import is the first thing to break:

```
ImportError: cannot import name 'Account' from 'bank'
```

Listen to the error. It's telling us where to start.

## Write the minimal amount of code for the test to run and check the failing test output

Give it just enough to import and run: a `bank.py` with the two names, and methods that do the
wrong thing on purpose. We store the balance but leave `deposit` and `withdraw` empty, so the
balance never moves. We want to watch the test fail on the value, which proves the test checks
what we think it does.

```python
from __future__ import annotations


class InsufficientFunds(Exception):
    ...


class Account:
    def __init__(self, balance: int = 0) -> None:
        self.balance = balance

    def deposit(self, amount: int) -> None:
        ...

    def withdraw(self, amount: int) -> None:
        ...
```

Run `uv run pytest`:

```
    def test_deposit_increases_balance(account):
        account.deposit(50)
>       assert account.balance == 150
E       assert 100 == 150
E        +  where 100 = <bank.Account object>.balance
```

The test runs and fails on the value, not on a missing name. That's exactly what we want before
writing the real thing.

## Write enough code to make it pass

Make `deposit` and `withdraw` actually move the balance:

```python
    def deposit(self, amount: int) -> None:
        self.balance += amount

    def withdraw(self, amount: int) -> None:
        self.balance -= amount
```

Run the tests again and they're green.

## Refactor

There's little to tidy in a few lines, but it's worth naming the shape. The fixture gives every
test the same clean starting point without repeating `Account(balance=100)` in each one, and the
tests read as three plain statements: arrange, act, assert. Re-run the tests to confirm nothing
moved.

> Put fixtures you want to share across files in a `conftest.py`. pytest discovers them
> automatically with no import needed.

## Testing the error path with `pytest.raises`

Happy-path tests aren't enough. The interesting bugs live in the failure modes: overdrawing,
negative deposits, a negative opening balance. None of those return a value we can assert on. They
raise, so we need a way to assert that code raised.

### Write the test first

`pytest.raises` is a context manager. The `with` block has to raise the named exception or the
test fails. We want two flavours: that overdrawing raises `InsufficientFunds`, and that the
message names the balance, so a reader of the error knows what went wrong.

```python
def test_overdrawing_raises(account):
    with pytest.raises(InsufficientFunds):
        account.withdraw(101)


def test_overdraw_message_mentions_the_balance(account):
    # `match` checks the exception message against a regex.
    with pytest.raises(InsufficientFunds, match=r"balance 100"):
        account.withdraw(500)


def test_negative_opening_balance_is_rejected():
    with pytest.raises(ValueError):
        Account(balance=-1)
```

`match` checks the exception message against a regular expression. It's handy when one exception
type is raised for several reasons and you want to pin down which.

### Try to run the test

Our `withdraw` happily lets the balance go negative and `__init__` accepts anything, so nothing
raises. `pytest.raises` fails when its block *doesn't* raise:

```
    def test_overdrawing_raises(account):
        with pytest.raises(InsufficientFunds):
>           account.withdraw(101)
E           Failed: DID NOT RAISE <class 'bank.InsufficientFunds'>
```

### Write the minimal amount of code for the test to run and check the failing test output

We already have the failing run above. The block ran, nothing raised, and pytest told us so in
plain words. That's the error path proving it isn't covered yet. Now we make it raise for the
right reasons.

### Write enough code to make it pass

Guard the three rules: a negative opening balance, a non-positive amount, and an overdraw. The
overdraw message includes the balance so `match=r"balance 100"` finds it.

```python
class Account:
    def __init__(self, balance: int = 0) -> None:
        if balance < 0:
            raise ValueError("opening balance cannot be negative")
        self.balance = balance

    def deposit(self, amount: int) -> None:
        if amount <= 0:
            raise ValueError("deposit must be positive")
        self.balance += amount

    def withdraw(self, amount: int) -> None:
        if amount <= 0:
            raise ValueError("withdrawal must be positive")
        if amount > self.balance:
            raise InsufficientFunds(f"cannot withdraw {amount} from balance {self.balance}")
        self.balance -= amount
```

The tests pass, error path included.

### Refactor

Nothing to move in the implementation, but notice what the tests bought us. We now describe the
account's contract from both sides: what it does when you use it correctly, and what it refuses to
do when you don't. **Always test the error paths.** The bug that overdraws an account in
production is the one nobody wrote a test for.

## A table of cases with `parametrize`

We rejected a deposit of `0` in the code, but only one test exercises a single bad amount. The
rule should hold for `0`, `-1`, and any other non-positive number. Writing one test per value is
noise. `parametrize` runs the same test body over a table of inputs.

### Write the test first

```python
@pytest.mark.parametrize(
    ("bad_amount"),
    [0, -1, -100],
)
def test_non_positive_deposits_are_rejected(account, bad_amount):
    with pytest.raises(ValueError):
        account.deposit(bad_amount)


@pytest.mark.parametrize(
    ("start", "withdraw", "expected"),
    [
        (100, 100, 0),   # withdraw the whole balance
        (100, 1, 99),
        (50, 25, 25),
    ],
)
def test_withdraw_table(start, withdraw, expected):
    acc = Account(balance=start)
    acc.withdraw(withdraw)
    assert acc.balance == expected
```

Each row becomes its own test case with its own name in the output, so when one fails you see
exactly which input broke. `test_withdraw_table` includes the edge of withdrawing the entire
balance down to `0`, which is the boundary where the overdraw check has to *not* fire.

### Try to run the test

The rules these exercise are already in place from the last cycle, so this run is green straight
away:

```
pytest_deep_dive/test_bank.py ........              [100%]
```

When you add a parametrized test against behaviour you haven't built yet, you'd see one failing
line per row instead. Here the code already honours the contract, so the table just locks it in.

### Write enough code to make it pass

Nothing to write. The implementation from the `pytest.raises` cycle already rejects non-positive
deposits and handles every withdrawal row. The new tests are documentation that runs.

### Refactor

`parametrize` collapsed what could have been six near-identical tests into two readable tables. If
a seventh case occurs to you, it's one more row, not one more function. That's the payoff: the
test body stays fixed and the data does the talking.

## Markers: tag tests to select or skip

One last requirement. Some tests are slow, for example one that loops a thousand deposits to check
they accumulate. We don't want to pay for it on every tight TDD loop, only before committing. A
*marker* labels a test so we can run a subset.

### Write the test first

Custom markers have to be registered in `pyproject.toml`, or pytest warns on every run:

```toml
[tool.pytest.ini_options]
markers = [
    "slow: marks slower tests (deselect with '-m \"not slow\"')",
]
```

Then tag the slow test:

```python
@pytest.mark.slow
def test_many_deposits_accumulate(account):
    for _ in range(1000):
        account.deposit(1)
    assert account.balance == 1100
```

### Try to run the test

Run it on its own to see the marker select it:

```
uv run pytest -m slow
```

```
pytest_deep_dive/test_bank.py .                     [100%]
1 passed, 6 deselected
```

The `-m slow` expression ran the one tagged test and deselected the rest.

### Write enough code to make it pass

The behaviour it checks (a thousand `+1` deposits land at `1100`) already works from the deposit
rule we wrote earlier, so the test is green. The marker doesn't change behaviour. It only changes
which tests a given run selects.

### Refactor

Now the marker earns its keep. During a tight loop you skip the slow test, and before committing
you run everything:

```bash
uv run pytest -m "not slow"   # skip slow tests
uv run pytest                 # the full suite
```

Built-in markers you'll reach for: `@pytest.mark.skip(reason=...)`,
`@pytest.mark.skipif(condition, reason=...)`, and `@pytest.mark.xfail` for known-broken cases.

## Wrapping up

- **Fixtures** give each test isolated, reusable setup. Request them by parameter name, and share
  them across files via `conftest.py`.
- **`pytest.raises`** (optionally with `match`) is how you test error paths. Always test them.
- **`parametrize`** runs one test body over a table of cases, each with its own name in the
  output.
- **Markers** tag tests so you can slice the suite (`-m "not slow"`). Register custom ones in
  `pyproject.toml`.
