# Classes and dataclasses

**[You can find all the code for this chapter here](https://github.com/samcolmanetti/learn-python-with-tests/tree/main/code/classes_and_dataclasses)**

We're going to build a small value type, `Money`, the long way: writing the constructor,
equality, and a readable representation by hand. Then we'll throw most of that code away and let
`@dataclass` generate it for us, and look at what `frozen=True` buys us when we want to use our
objects in a set or as dict keys.

## Write the test first

A `Money` holds an amount and a currency. We store the amount as whole cents (an `int`) rather
than a float, because floats can't represent money exactly: `0.1 + 0.2` is not `0.3` in floating
point, and that's a bad way to lose someone's rent. So a five-dollar note is `Money(500, "USD")`.

The smallest behaviour is just holding onto those two things.

```python
from money import Money


def test_stores_amount_and_currency():
    fiver = Money(500, "USD")
    assert fiver.amount == 500
    assert fiver.currency == "USD"
```

## Try to run the test

We've imported `Money` from a module that doesn't define it, so the import is what breaks first.

```
ImportError: cannot import name 'Money' from 'classes_and_dataclasses.money'
```

There's no class yet. The error is pointing at exactly the file we need to open.

## Write the minimal amount of code for the test to run and check the failing test output

Here's where I keep the TDD discipline even though it feels silly. We write a `Money` that takes
the arguments but ignores them, stashing fixed wrong values instead. The point isn't to fail, it's
to make the test *run* so we can confirm it fails on the value we care about and not on a typo.

```python
class Money:
    def __init__(self, amount, currency):
        self.amount = 0
        self.currency = ""
```

The `__init__` method is the constructor. Python calls it when you write `Money(500, "USD")`, and
`self` is the new object we're filling in. We're assigning the wrong things to it on purpose.

Run `uv run pytest`:

```
    def test_stores_amount_and_currency():
        fiver = Money(500, "USD")
>       assert fiver.amount == 500
E       assert 0 == 500
E        +  where 0 = <classes_and_dataclasses.money.Money object at 0x109d5f670>.amount
```

It runs, and it fails on the value. That's the green light to write the real thing.

## Write enough code to make it pass

Store the arguments we were handed.

```python
class Money:
    def __init__(self, amount, currency):
        self.amount = amount
        self.currency = currency
```

The test passes. Two lines of constructor and we've got an object that remembers its state.

## Refactor

Nothing to tidy yet, but let me add type hints while the file is small, because the rest of the
book leans on them and they document the shape of the object for free.

```python
from __future__ import annotations


class Money:
    def __init__(self, amount: int, currency: str) -> None:
        self.amount = amount
        self.currency = currency
```

The `from __future__ import annotations` line lets us write modern hints like `list[int]` and keep
the code running on Python 3.9. We'll use it in every file from here on. Re-run the tests to
confirm the hints didn't change behaviour.

## Repeat for new requirements

Money you can't add up isn't much use. Adding two amounts in the same currency should give their
sum, and adding across currencies should be an error, because `Money(500, "USD")` plus
`Money(250, "GBP")` has no sensible answer without an exchange rate.

### Write the test first

```python
def test_add_same_currency():
    assert Money(500, "USD").add(Money(250, "USD")) == Money(750, "USD")


def test_add_different_currency_raises():
    import pytest

    with pytest.raises(ValueError):
        Money(500, "USD").add(Money(250, "GBP"))
```

`pytest.raises` is a context manager that asserts the block inside it raises the given exception.
If no error comes out, the test fails.

### Try to run the test

```
AttributeError: 'Money' object has no attribute 'add'
```

We're calling a method that isn't there yet. Listen to the error: it names the method we owe it.

### Write the minimal amount of code for the test to run and check the failing test output

Add an `add` method that returns a stub. I'll return `self` so the test runs and fails on the
value rather than on a missing attribute.

```python
    def add(self, other: Money) -> Money:
        return self
```

Running `uv run pytest` now gives us a real comparison failure rather than an `AttributeError`,
which is the failing-for-the-right-reason we want. But the comparison itself is about to surprise
us, because two `Money` objects with the same numbers aren't equal yet either. We'll fix `add`
properly now and let equality drive its own cycle next.

### Write enough code to make it pass

The real `add` checks the currencies match, then builds a fresh `Money` with the summed amount. We
return a *new* object rather than mutating `self`, which keeps a `Money` behaving like a value:
adding to it doesn't change it, the way `5 + 3` doesn't change `5`.

```python
    def add(self, other: Money) -> Money:
        if self.currency != other.currency:
            raise ValueError(
                f"cannot add {self.currency} to {other.currency}"
            )
        return Money(self.amount + other.amount, self.currency)
```

`test_add_different_currency_raises` passes now. But `test_add_same_currency` still fails, and the
reason is the `==`, not the addition. That's our next requirement.

### Refactor

Nothing to refactor in `add` itself. The interesting work is the equality it depends on, so let's
go there.

## Repeat for new requirements

Run the same-currency test and read the failure closely.

### Write the test first

We already wrote `test_add_same_currency`, and we want a direct equality test too, plus the cases
that pin down what "equal" means: same numbers are equal, any difference is not, and a `Money` is
never equal to a bare number or string.

```python
def test_equal_by_value():
    assert Money(500, "USD") == Money(500, "USD")


def test_not_equal_when_amount_differs():
    assert Money(500, "USD") != Money(250, "USD")


def test_not_equal_when_currency_differs():
    assert Money(500, "USD") != Money(500, "GBP")


def test_not_equal_to_other_types():
    assert Money(500, "USD") != 500
    assert Money(500, "USD") != "500 USD"
```

### Try to run the test

```
    def test_equal_by_value():
>       assert Money(500, "USD") == Money(500, "USD")
E       AssertionError: assert <classes_and_dataclasses.money.Money object at 0x105ec9370> == <classes_and_dataclasses.money.Money object at 0x105ec93a0>
E        +  where <classes_and_dataclasses.money.Money object at 0x105ec9370> = Money(500, 'USD')
E        +  and   <classes_and_dataclasses.money.Money object at 0x105ec93a0> = Money(500, 'USD')
```

Two objects that look identical compare as unequal. **By default, `==` on a custom object means
"is this the exact same object in memory", not "do these have the same values".** Those are two
different objects, so Python says no, and the two addresses (`0x105ec9370` versus `0x105ec93a0`)
confirm they really are distinct.

### Write the minimal amount of code for the test to run and check the failing test output

To control what `==` means, we define `__eq__`. As a deliberately wrong stub, return `False`
always, so the test still fails but now through *our* method rather than the default one.

```python
    def __eq__(self, other):
        return False
```

`uv run pytest` still fails `test_equal_by_value` on the assertion, which confirms our `__eq__` is
the one being called now. Time to make it tell the truth.

### Write enough code to make it pass

Two `Money` objects are equal when both the amount and the currency match. We also guard the type:
if `other` isn't a `Money`, we return `NotImplemented`, a special value that tells Python "I don't
know how to compare these, ask the other object". That's what makes `Money(500, "USD") != 500`
come out sensibly instead of raising.

```python
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        return self.amount == other.amount and self.currency == other.currency
```

All the equality tests pass, and so does `test_add_same_currency`, because the `==` inside it
finally compares by value.

### Refactor

The class works, but its repr is still the default object soup we saw in the failure output. When a
test fails or you print a `Money` in a debugger, `<...Money object at 0x105ec9370>` tells you
nothing. Let's fix that as its own small cycle.

## Repeat for new requirements

### Write the test first

```python
def test_repr_is_useful():
    assert repr(Money(500, "USD")) == "Money(amount=500, currency='USD')"
```

### Try to run the test

```
    def test_repr_is_useful():
>       assert repr(Money(500, "USD")) == "Money(amount=500, currency='USD')"
E       assert '<classes_and_dataclasses.money.Money object at 0x10a567a30>' == "Money(amount=500, currency='USD')"
E         - Money(amount=500, currency='USD')
E         + <classes_and_dataclasses.money.Money object at 0x10a567a30>
```

`repr` falls back to that address string until we define `__repr__` ourselves.

### Write enough code to make it pass

`__repr__` returns the string you see when you `repr()` an object or look at it in the REPL. The
convention is to make it look like the code that would recreate the object. The `!r` in the f-string
calls `repr` on the currency, which is what puts the quotes around `'USD'`.

```python
    def __repr__(self) -> str:
        return f"Money(amount={self.amount}, currency={self.currency!r})"
```

Green.

### Refactor

Stand back and count what we wrote to get a plain value type: a constructor, an `add`, an `__eq__`
with a type guard, and a `__repr__`. That's a lot of ceremony, and most of it is mechanical. Every
field appears in the constructor, again in `__eq__`, and again in `__repr__`. Add a third field and
you touch three methods. **This is exactly the boilerplate `@dataclass` exists to delete.**

## Repeat for new requirements

Let's build the same value type a second time, with `@dataclass` generating the parts we hand-wrote.
We'll also ask for something the hand-rolled `Money` can't do: be a dict key.

### Write the test first

We want a `DataMoney` that's equal by value and has a readable repr, both for free, plus its own
`add`. Then the new requirement: it should be usable as a dict key and in a set, and you shouldn't be
able to mutate it after construction.

```python
from money import DataMoney, Money


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
```

`test_plain_money_is_not_hashable` looks like an odd thing to assert, but it documents a real Python
rule we're about to lean on. We'll come back to it.

### Try to run the test

The first run fails on the import, the same way `Money` did, because `DataMoney` doesn't exist yet.
Once we write a bare `DataMoney` with no `add`, the next thing to break is the method:

```
AttributeError: 'DataMoney' object has no attribute 'add'
```

### Write the minimal amount of code for the test to run and check the failing test output

Decorate a class with `@dataclass` and list the fields as annotated class attributes. The decorator
reads those annotations and writes `__init__`, `__eq__`, and `__repr__` for us. We'll stub `add` to
return `self` so the suite runs and fails on values rather than on a missing attribute.

```python
from dataclasses import dataclass


@dataclass
class DataMoney:
    amount: int
    currency: str

    def add(self, other: DataMoney) -> DataMoney:
        return self
```

Run `uv run pytest`. The equality and repr tests pass already, generated by the decorator. But
`test_datamoney_is_frozen` and `test_datamoney_is_hashable` fail, because a plain `@dataclass` is
mutable and, being mutable, is not hashable. That's the honest failure that points at the next step.

### Write enough code to make it pass

Two changes. Pass `frozen=True` to the decorator, and write the real `add`.

```python
@dataclass(frozen=True)
class DataMoney:
    amount: int
    currency: str

    def add(self, other: DataMoney) -> DataMoney:
        if self.currency != other.currency:
            raise ValueError(
                f"cannot add {self.currency} to {other.currency}"
            )
        return DataMoney(self.amount + other.amount, self.currency)
```

All the `DataMoney` tests pass now. `frozen=True` does two jobs. It makes assigning to a field after
construction raise `FrozenInstanceError`, which is what `test_datamoney_is_frozen` checks. And
because the fields can no longer change, the dataclass also generates a `__hash__`, so a `DataMoney`
can live in a set or be a dict key. That's `test_datamoney_is_hashable`.

### Refactor

Now look back at `test_plain_money_is_not_hashable`, the one that passed without us doing anything.
**The moment you define `__eq__` on a class, Python sets its `__hash__` to `None`, making instances
unhashable.** Our hand-written `Money` defined `__eq__`, so it lost its hash and can't be a dict key.
That's deliberate on Python's part: if two objects are equal, they must hash equal, and Python won't
guess a hash that respects your custom `__eq__`, so it removes the default one rather than let you
ship a subtly broken set.

`@dataclass(frozen=True)` handles both sides together: it generates an `__eq__` *and* a matching
`__hash__`, because a frozen object's fields can't drift out from under the hash. That pairing, value
equality plus a consistent hash, is the whole reason to reach for a frozen dataclass for a value
type. Re-run the tests one last time and watch them stay green.

## Wrapping up

- **A class bundles state in `__init__` and behaviour in methods**, with `self` as the current
  object.
- **`__eq__` makes `==` compare by value instead of by identity.** Guard the type and return
  `NotImplemented` for unrelated types.
- **Defining `__eq__` makes instances unhashable** (Python sets `__hash__` to `None`), so a plain
  value class can't be a dict key or set member.
- **`@dataclass` generates `__init__`, `__eq__`, and `__repr__`** from the field annotations, so
  you stop hand-writing boilerplate.
- **`@dataclass(frozen=True)` makes instances read-only and hashable**, giving you value equality
  and a consistent hash together. That's the pairing you want for a value type.
