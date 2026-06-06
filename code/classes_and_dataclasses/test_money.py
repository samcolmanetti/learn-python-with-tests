from money import DataMoney, Money


def test_stores_amount_and_currency():
    fiver = Money(500, "USD")
    assert fiver.amount == 500
    assert fiver.currency == "USD"


def test_add_same_currency():
    assert Money(500, "USD").add(Money(250, "USD")) == Money(750, "USD")


def test_add_different_currency_raises():
    import pytest

    with pytest.raises(ValueError):
        Money(500, "USD").add(Money(250, "GBP"))


def test_equal_by_value():
    assert Money(500, "USD") == Money(500, "USD")


def test_not_equal_when_amount_differs():
    assert Money(500, "USD") != Money(250, "USD")


def test_not_equal_when_currency_differs():
    assert Money(500, "USD") != Money(500, "GBP")


def test_not_equal_to_other_types():
    assert Money(500, "USD") != 500
    assert Money(500, "USD") != "500 USD"


def test_repr_is_useful():
    assert repr(Money(500, "USD")) == "Money(amount=500, currency='USD')"


def test_datamoney_equal_by_value():
    assert DataMoney(500, "USD") == DataMoney(500, "USD")


def test_datamoney_repr():
    assert repr(DataMoney(500, "USD")) == "DataMoney(amount=500, currency='USD')"


def test_datamoney_add():
    assert DataMoney(500, "USD").add(DataMoney(250, "USD")) == DataMoney(750, "USD")


def test_datamoney_is_frozen():
    import dataclasses

    import pytest

    coin = DataMoney(500, "USD")
    with pytest.raises(dataclasses.FrozenInstanceError):
        coin.amount = 999


def test_datamoney_is_hashable():
    wallet = {DataMoney(500, "USD"): "a five", DataMoney(100, "USD"): "a dollar"}
    assert wallet[DataMoney(500, "USD")] == "a five"
    assert len({DataMoney(500, "USD"), DataMoney(500, "USD")}) == 1


def test_plain_money_is_not_hashable():
    import pytest

    with pytest.raises(TypeError):
        {Money(500, "USD"): "nope"}
