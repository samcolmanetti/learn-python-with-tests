import pytest

from .bank import Account, InsufficientFunds

# ----- Fixtures: reusable, named setup injected by parameter name ----------------------


@pytest.fixture
def account():
    """A fresh account opened with 100. Each test gets its own — no shared state."""
    return Account(balance=100)


def test_deposit_increases_balance(account):
    account.deposit(50)
    assert account.balance == 150


def test_withdraw_decreases_balance(account):
    account.withdraw(30)
    assert account.balance == 70


# ----- raises: asserting the error path -----------------------------------------------


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


# ----- parametrize: one test, a table of cases ----------------------------------------


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


# ----- markers: tag tests to select or skip them --------------------------------------


@pytest.mark.slow
def test_many_deposits_accumulate(account):
    for _ in range(1000):
        account.deposit(1)
    assert account.balance == 1100
